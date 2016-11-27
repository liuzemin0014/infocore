#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python version: 2.7.11

import sys
from os import listdir
from os.path import isfile, join
import os, shutil

class Merger(object):
    def __init__(self):
        try:
            self.outputPath = "results/"+sys.argv[1]
        except IndexError:
            print "Please pass an output filename like this:\n",\
             "python merge_coocc_files.py outputFilename.txt"

        self.toMerge = "to_merge"
        self.files = self.list_filenames_to_merge()
        if not self.files:
            print 'There are no files in the folder "to_merge"'
        self.allUniqueLines = set()

    def empty_to_merge_folder(self):
        for theFile in os.listdir(self.toMerge):
            filePath = os.path.join(self.toMerge, theFile)
            try:
                if os.path.isfile(filePath):
                    os.unlink(filePath)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    def list_filenames_to_merge(self):
        return [f for f in listdir(self.toMerge) if\
        isfile(join(self.toMerge, f))]

    def merge_files(self):
        for cooccFile in self.files:
            with open(self.toMerge+"/"+cooccFile) as coFile:
                for line in coFile:
                    self.allUniqueLines.add(line)

    def write_merged_file(self):
        with open(self.outputPath,"w") as output:
            for line in self.allUniqueLines:
                output.write(line)

if __name__ == '__main__':
    merger = Merger()
    merger.merge_files()
    merger.write_merged_file()
    merger.empty_to_merge_folder()
