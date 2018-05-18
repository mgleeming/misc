import os

msconvertDirPath = r'"C:\Program Files\ProteoWizard\ProteoWizard 3.0.9216"'

thisPath = os.getcwd()

msconvertPath = os.path.join(msconvertDirPath, "msconvert.exe")
	
filePath = os.path.join(thisPath, "*.raw")

posDir = os.path.join(thisPath, 'pos')
negDir = os.path.join(thisPath, 'neg')

# neg ion export
filters = "--filter \"peakPicking true 1-\" "
filters += "--filter \"polarity negative\""
cmd = '"%s --mzML %s -o %s %s"' %(msconvertPath, filters, negDir, filePath) 
os.system(cmd)

# pos ion export
filters = "--filter \"peakPicking true 1-\" "
filters += "--filter \"polarity positive\""
cmd = '"%s --mzML %s -o %s %s"' %(msconvertPath, filters, posDir, filePath) 
os.system(cmd)