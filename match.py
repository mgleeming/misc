import numpy as np
import pymzml
import sys
import scipy.signal
import scipy.optimize as opt
import matplotlib.pyplot as plt

def gauss(x, amp, cent, wid, scale = 1):
    return(amp/ (np.sqrt(2*np.pi*(wid/scale)**2 )) * np.exp(-(x-(cent/scale))**2 / (2*(wid/scale)**2)))

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

spectra = readSpectra('/home/mleeming/Code/HiTIME-CPP/data/testing.mzML')

shape = [
    [-5.99675, 0.1756],
    [-3.99906, 0.0593],
    [-2.99841, 0.4044],
    [-2.00013, 0.3994],
    [-0.99877, 0.5407],
    [0, 1],
    [2.00108, 0.5902],
]

scale = 100000


def fitShape(mzs, ints, m, i, shape):
    values = []
    for s in shape:
        target = m + s[0]
        index = np.argmin(np.abs(mzs - target))

        targetmz = mzs[index]
        targetint = ints[index]

        if abs(targetmz - target) > 0.01: continue

        tol = 0.05
        mask = np.where(
            (mzs > targetmz - tol)
            &
            (mzs < targetmz + tol)
        )

        mzsubset = mzs[mask]
        intsubset = ints[mask]

        cen = int(targetmz * scale)
        wid = int((np.max(mzsubset) - np.min(mzsubset)) * scale)
        amp = int(np.max(mzsubset))
        p0 = [amp,cen,wid]
        try:

            MSpopt, MSpcov = opt.curve_fit(
                lambda x, amp, cen, wid: gauss(x, amp, cen, wid, scale = scale),
                mzsubset, intsubset, p0=p0, maxfev = 2000
            )
        except:
            return None
        yfit = gauss(mzsubset, MSpopt[0], MSpopt[1], MSpopt[2], scale = scale)

        y = intsubset
        y_fit = yfit
#        plt.plot(mzsubset, y)
#        plt.plot(mzsubset, yfit)
#        plt.show()
#        sys.exit()
        # residual sum of squares
        ss_res = np.sum((y - y_fit) ** 2)

        # total sum of squares
        ss_tot = np.sum((y - np.mean(y)) ** 2)

        # r-squared
        r2 = 1 - (ss_res / ss_tot)

        expectedint = float(i) * s[1]

        if targetint > expectedint:
            ratio = targetint / expectedint
        else:
            ratio = expectedint / targetint

        error =  r2 * ratio

        values.append(error)

    if len(values) > 1:
        return sum(values)
    else:
        return None

for s in spectra:
    time, mzs, ints, lvl = s
    for x in range(len(mzs)):
        i = ints[x]
        if i < 100: continue
        m = mzs[x]
        fit = fitShape(mzs, ints, m, i, shape)
        if fit:
           print time, m, i, fit


