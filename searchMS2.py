import os, sys, argparse
import numpy as np
from pyteomics import mgf

parser = argparse.ArgumentParser()

parser.add_argument('--i',
					help = 'Input MGF file',
					type = str)
parser.add_argument('--o',
					help = 'Output file',
					type = str)
parser.add_argument('--mzTol',
					help = 'm/z tolerance used when searching for fragments (+/- m/z)',
					type = float,
					default = 0.08)
parser.add_argument('--NLS',
					help = 'Search for charge adjusted neutral loss',
					type = float)
parser.add_argument('--transition',
					help = 'Search for pairs of peaks with defined mass transitions',
					type = float)
parser.add_argument('--EIC',
					help = 'plot EIC of this m/z from MS2 spectra',
					type = float)
parser.add_argument('--getMD',
					help = 'get mass defect of precursor ion',
					action = 'store_true')


class Spectrum(object):
	def __init__(self, index, rt, charge, precursor, precursor_intensity, mzs, ints):
		self.index = index
		self.rt = rt
		self.charge = charge
		self.precursor = precursor
		self.precursor_intensity = precursor_intensity
		self.mzs = mzs
		self.ints = ints

def reader(in_file):
	with mgf.read(in_file) as spectra:
		for n, spec in enumerate(spectra):
			params = spec['params']
			rt = float(params['rtinseconds'])
			charge = int(str(params['charge']).strip('+'))
			precursor = float(params['pepmass'][0])
			try:
				precursor_intensity = float(params['pepmass'][1])
			except:
				precursor_intensity = None
			yield Spectrum(n, rt, charge, precursor, precursor_intensity, spec['m/z array'], spec['intensity array'])

def get_transition(options, s):
	max_transition = None
	max_mz = None
	for n in range(len(s.mzs)):
		reference_ion = s.mzs[n]
		reference_ion_int = s.ints[n]

		target_ion = reference_ion + options.transition

		target_LL = target_ion - options.mzTol
		target_HL = target_ion + options.mzTol

		mask = np.where(
			(s.mzs > target_LL) & (s.mzs < target_HL)
		)

		sum_ints = np.sum(s.ints[mask])

		if sum_ints == 0:
			continue

		if not max_mz:
			max_mz = reference_ion
			max_transition = sum_ints + reference_ion_int
		if sum_ints > max_transition:
			max_transition = sum_ints + reference_ion_int
			max_mz = reference_ion

	if max_mz is None:
		max_mz = 0
		max_transition = 0
	return max_transition, max_mz

def get_MD(s):
	# get mass defect of precursor

	pt = s.precursor
	md = str(pt).split('.')[1][:3]
	nom = int(round(pt))
	md = '0.' + md
	return md

def MS2_EIC(options, s):

	target_LL = options.EIC - options.mzTol
	target_HL = options.EIC + options.mzTol

	mask = np.where(
		(s.mzs > target_LL) & (s.mzs < target_HL)
	)

	sum_ints = np.sum(s.ints[mask])

	return sum_ints

def get_NLS(options, s):
	# get intensity of charge-corrected NL

	neutral_loss = options.NLS
	if options.NLS:
		target = s.precursor - (neutral_loss / s.charge)
		target_LL = target - options.mzTol
		target_HL = target + options.mzTol

		mask = np.where (
			(s.mzs > target_LL) & (s.mzs < target_HL)
		)

		NLS_int = np.sum(s.ints[mask])

	return NLS_int, target, neutral_loss

def main(options):

	spectra = reader(options.i)

	try:
		assert options.i != options.o
	except AssertionError:
		print 'Input and output file names are the same. Aborting'

	of1 = open(options.o,'wt')
   
	for s in spectra:


		if s.index % 1000 == 0: print 'processing spectrum: ', s.index
		
		if options.NLS:
			NLS_int, target, neutral_loss = get_NLS(options, s)

		if options.transition:
			transition, transition_mz = get_transition(options, s)
		else:
			transition, transition_mz = None, None

		if options.EIC:
			EIC_val = MS2_EIC(options, s)
		else:
			EIC_val = None

		if options.getMD:
			md = get_MD(s)
		else:
			md = None

		of1.write( 11 * '%s, ' % (
						s.rt / 60, # 1
						NLS_int, # 2
						transition, # 3
						transition_mz, # 4
						s.index, # 5
						s.precursor, # 6
						s.charge, # 7
						target, # 8
						(neutral_loss / s.charge), # 9
						EIC_val, # 10
						md # 11
						)
					+ '\n'
		)

	of1.close()

	return

if __name__ == '__main__':
	options = parser.parse_args()
	sys.exit(main(options))
