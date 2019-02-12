import matplotlib.pyplot as plt
import numpy as np
import sys, pymzml
from scipy.stats.stats import pearsonr

x = np.arange(1000)/100
y = np.ones(1000)

shape = [
    [-5.99675, 0.1756],
    [-3.99906, 0.0593],
    [-2.99841, 0.4044],
    [-2.00013, 0.3994],
    [-0.99877, 0.5407],
    [0, 1],
    [2.00108, 0.5902],
]

def readSpectra(mzml_file, msLevel = None):
    msrun = pymzml.run.Reader(str(mzml_file), obo_version = '3.71.0')
    for n, spectrum in enumerate(msrun):
        if msLevel:
            if spectrum['ms level'] != msLevel: continue
        lvl = spectrum['ms level']
        try:
            time = spectrum['scan time']
        except:
            try:
                time = spectrum['scan start time']
            except Exception, e:
                #print 'Warning, skipping spectrum %s' %n
                #print 'Stack trace:'
                #print str(e)
                continue
        try:
            mzs = np.array(spectrum.mz, dtype = "float32")
            ints = np.array(spectrum.i, dtype = 'float32')
            assert mzs.shape == ints.shape
            yield time, mzs, ints, lvl
        except Exception, e:
            #print 'Warning, skipping spectrum %s' %n
            #print 'Stack trace:'
            #print str(e)
            continue


def getShapeDimensions(shape):
    offsets = [float(s[0]) for s in shape]
    return min(offsets), max(offsets)

def makeModel(m, msubset, maxAmp, shape):
    wid = 0.08
    ymodel = 0
    for s in shape:
        cent = s[0] + m
        amp = s[1] * maxAmp
        ymodel += amp / (np.sqrt(2*np.pi*(wid)**2 )) * np.exp(-(msubset-cent)**2 / (2*(wid)**2))
    return ymodel

def fit(x, mzs, ints):
    i, m = ints[x], mzs[x]

    # git points in shape boundaries +/- tolerance
    mask = np.where(
        (mzs > mzs[x] + SHAPE_TARGET_LOWER_OFFSET - tolerance)
        &
        (mzs < mzs[x] + SHAPE_TARGET_UPPER_OFFSET + tolerance)
    )

    if mask[0].shape[0] < 50: return

    msubset = mzs[mask]
    isubset = ints[mask]
    ifit = makeModel(m, msubset, max(isubset), shape)

    pearsonC, p_val = pearsonr(ifit,isubset)
    # print (fit)
    # plt.plot(msubset, ifit)
    # plt.show()

    return pearsonC


MINIMUM_POINT_INTENSITY = 500
tolerance = 0.5
SHAPE_TARGET_LOWER_OFFSET, SHAPE_TARGET_UPPER_OFFSET = getShapeDimensions(shape)
spectra = readSpectra('MeOH_3_2.mzML')

for spectrum in spectra:
    time, mzs, ints, lvl = spectrum
    for x in range(len(mzs)):
        i = ints[x]
        if i < MINIMUM_POINT_INTENSITY: continue
        m = mzs[x]

        pearsonC = fit(x, mzs, ints)
        if pearsonC:
            print ('%s, %s, %s, %s'%(time, m,i,pearsonC))

