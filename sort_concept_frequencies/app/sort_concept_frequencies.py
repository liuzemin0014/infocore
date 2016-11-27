#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python version: 2.7.11


import sys
import operator

class FreqCounter(object):
    """ Takes a td file, a concept selection file and a text selection
    file as command line arguments. Adds frequencies from the
    td file for single concepts or groups of concepts depending on the concept
    selection file passed. To count frequencies
    for single concepts, the concept selection file contains one concept
    ID per line. To count frequencies of groups, the name of the group
    followed by one concept ID per line is contained in the file. Groups
    must be separated by a newline between the last concept of one group
    and the group name of the next group. See readme.txt for examples.
    Text selection files contain one text ID per line.
    Text selection files, concept selection files and td files must be
    placed in the corresponding folders in
    infocore_tools/apps/sort_concept_frequencies/app.
    Example call: """

    def __init__(self):
        self.conceptGroupsDefined = False
        self.tdFile = "td_files/"+sys.argv[1]
        # Check if text selection file is passed.
        if len(sys.argv) == 4:
            self.textIDs = self.readIDs("text_selection_files/"+sys.argv[3])
        if len(sys.argv) == 3:
            self.textIDs = self.readTextIDsFromTDfile()
        # Create data structures to extract frequencies.
        self.TDconceptList = self.createListofConceptsInTdFile(self.tdFile)
        self.textIDDict = self.createTextIDFreqListDict(self.tdFile)
        self.conceptIDs = self.readConceptIDs("concept_selection_files/"+sys.argv[2])
        self.conceptFreqDict={}
        self.conceptsSortedByFrequency=[]
        # Add, sort and print frequencies.
        if self.conceptGroupsDefined == True:
            self.count_group_frequencies()
        else:
            self.count_concept_frequencies()
        self.sort_dictionary()
        self.print_sorted_concepts()

    def readTextIDsFromTDfile(self):
        textIDs = []
        with open(self.tdFile) as tdFile:
            tdFileIterator = iter(tdFile)
            next(tdFileIterator)
            next(tdFileIterator)
            for line in tdFileIterator:
                line = line.split(",")
                textIDs.append(line[0])
        return textIDs

    def print_sorted_concepts(self):
        """Prints the concepts and their frequencies to a file. The file
        name contains the command line arguments used in the program
        call.
        """
        commandLineOptions = '_'.join(sys.argv[1:])
        outputFilePath = "results/sortedFrequencies_"+commandLineOptions+"_.txt"
        with open(outputFilePath,'w') as outputFile:
            for conceptFreqPair in self.conceptSortedByFrequency:
                conceptFrequencyPair = conceptFreqPair[0]+','+str(conceptFreqPair[1])+'\n'
                outputFile.write(conceptFrequencyPair)

    def sort_dictionary(self):
        """Sorts a dictionary by value in descending order."""
        self.conceptSortedByFrequency = sorted(self.conceptFreqDict.items(),
        key=operator.itemgetter(1), reverse=True)

    def count_concept_frequencies(self):
        """ Fills the dictionary with conceptIDs as keys and their
        frequencies as values.
        """
        for text in self.textIDs:
            for concept in self.conceptIDs:
                frequency = self.lookUpFrequency(text,concept)
                if concept in self.conceptFreqDict:
                    self.conceptFreqDict[concept] += frequency
                else:
                    self.conceptFreqDict[concept] = frequency

    def lookUpFrequency(self,textid,conceptid):
    	"""Takes a textID and a conceptID as arguments.
    	Finds the index of the given conceptID in the conceptList.
        Accesses the frequency list of the given textID via the
        dictionary and pick the concept frequency with the list index
        obtained before."""
    	# Find index for given conceptid.
    	conceptIndex = self.TDconceptList.index(conceptid)
    	# Return frequency for given textid,conceptid .
    	return self.textIDDict[textid][conceptIndex]

    def count_group_frequencies(self):
        """ Creates dictionary entries with groups as keys and the sum
        of frequencies of concepts contained in the group as values for
        each group.
        """
        for group in self.conceptIDs:
            groupName = group.pop(0)
            for text in self.textIDs:
                for concept in group:
                    frequency = self.lookUpFrequency(text,concept)
                    if groupName in self.conceptFreqDict:
                        self.conceptFreqDict[groupName] += frequency
                    else:
                        self.conceptFreqDict[groupName] = frequency

    def readConceptIDs(self,string):
        """Checks if a grouping file contains groups or not and calls
        the corresponding function to read the concept selection file.
        """
        with open(string) as conceptIDFile:
            if conceptIDFile.read()[0].isalpha():
                self.conceptGroupsDefined = True
                return self.read_concept_file_with_groups(string)
            else:
                return self.readIDs(string)

    def read_concept_file_with_groups(self,string):
        """Saves a concept selection with groups in a list of lists
        where the first element of the inner lists is the name of the
        group."""
        with open(string) as conceptIDFile:
            groupStrings = conceptIDFile.read().rstrip().split("\n\n")
            groups = [x.split("\n") for x in groupStrings]
        return groups

    def readIDs(self,string):
    	"""Expects the path to a file containing one ID per line. Reads
        concept IDs or text IDs from files."""
    	listOfIDs = []
    	inputFile = open(string)
    	for line in inputFile:
    		line = line.rstrip()
    		listOfIDs.append(line)
    	inputFile.close()
    	return listOfIDs

    def createListofConceptsInTdFile(self,string):
    	"""Make a concept accessible via a list index by creating a list
        of all concepts in filtered_td_11_651.txt.
    	Concept ID 10001 corresponds to index 1,
    	concept ID 10002 corresponds to index 2 ...
    	"""
    	inputFile = open(string)
    	for line in inputFile:
    		if line.startswith('id'):
    			line = line.rstrip()
    			listOfLine = line.split(',')
    			conceptList = listOfLine[2:]
    		if line.startswith(',,,'):
    			pass
    		else:
    			pass
    	inputFile.close()
    	return conceptList

    def createTextIDFreqListDict(self,string):
    	"""Create a dictionary which holds the data of the matrix in
    	filtered_td_11_651.txt . The keys of the dictionary are textIDs.
        The value of a textID is a list of concept frequencies occurring
        in that text. The order of frequencies corresponds to the order
        of concepts in the list created by createListofConcepts.
    	"""
    	textIDDict = {}
    	inputFile = open(string)
    	for line in inputFile:
    		if line.startswith('id'):
    			pass
    		if line.startswith(',,,'):
    			pass
    		else:
    			line = line.rstrip()
    			lineList = line.split(',')
    			FreqList = lineList[3:]
    			FreqListInt = [int(i) for i in FreqList]
    			# Add date as first item to have the first concept on index
    			# 1.
    			DateFreqListInt = [lineList[2]] + FreqListInt
    			textID = lineList[0]
    			textIDDict[textID] = DateFreqListInt
    	inputFile.close()
    	return textIDDict

    def add_frequencies_of_selected_concepts(self):
        """Loop over the lists of IDs to get the "coordinates" of the
        wanted frequency in the matrix/table. Add up Frequencies and
        count documents while looping. Writes the results to stdout.
        """
        DocCount = 0
        FreqCount = 0
        for text in self.textIDs:
        	for concept in self.conceptIDs:
        		Frequency = self.lookUpFrequency(text,concept)
        		if Frequency > 0:
        			FreqCount = FreqCount + self.lookUpFrequency(text,concept)
        			DocCount = DocCount + 1

        print 'Sum of frequencies for the specified documents and concepts:\
        ', FreqCount
        print 'Number of documents which contain one of the', \
        'specified concepts: ',DocCount
        print 'Number of specified concepts: ', \
        str(len(self.conceptIDs))
        print 'Number of specified documents: ',str(len(self.textIDs))

if __name__== '__main__':
    FreqCounter = FreqCounter()
