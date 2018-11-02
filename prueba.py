import sys
import os

path = './Reconocimiento/data/'
for dirname, dirnames, filenames in os.walk(path):
    print dirname
    for subdir in dirnames:
        #print dirname
        #print subdir
        subject_path = os.path.join(dirname,subdir)
        #print subject_path

        for filename in os.listdir(subject_path):
            if filename == '.directory':
                continue
            #print filename