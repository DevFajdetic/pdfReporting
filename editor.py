import subprocess
import os

bashCommand = os.path.join(
    os.getcwd(), 'env', 'Lib', 'site-packages', 'qt5_applications', 'Qt', 'bin', 'designer.exe')
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

