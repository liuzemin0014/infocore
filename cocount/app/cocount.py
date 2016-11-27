#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python version: 2.7.10

import itertools
import logging
import time
import sys


class CooccCounter(object):
    """
    This Class takes a list of command line arguments and reads
    cooccurrence scores from a cooccurrence file according to the
    options passed in the arguments.
    """
    def __init__(self,argumentList):
        """ On intantiation, the command line arguments are assigned to
        variables. Lists of concepts and texts to work with are created
        and input and output filepaths are stored in variables."""
        self.argumentList = argumentList
        self.projectID = argumentList[1]
        self.setID = argumentList[2]
        self.textSelection = argumentList[3]
        self.countMethod = argumentList[4]
        self.IDsOrNot = argumentList[5]
        self.conceptSelection = argumentList[6:]
        self.cooccScoreDict = {}
        self.conceptSelectionList = []
        self.textSelectionDict = {}
        self.textSelectionList = []
        # If no suffix is passed, empty string is attached to input and
        # output filenames.
        self.suffix = ""
        self.cooccFilePath = ""
        self.outputFilePath = ""
        self.or_option = self.or_in_concept_selection()
        self.create_concept_selection_list()
        if not self.or_option:
            self.conceptSelectionList = set(self.conceptSelectionList)
            self.conceptSelectionList = list(self.conceptSelectionList)
        self.detect_type_of_text_selection()
        self.createFilePaths()
        self.lineCount = 0
        #logging.basicConfig(filename='test.log',level=logging.DEBUG)
        #logging.debug(self.conceptSelectionList)
        #logging.debug(self.textSelectionList)

    def or_in_concept_selection(self):
        """Creates a Boolean to check if the or option is activated. The Boolean
        is used later to call the functions readOrConceptSelection and or_count."""
        # The redundant code should be written in a new function.
        if "_" in self.conceptSelection[0]:
            try:
                with open("concept_selection_files/"+self.conceptSelection[1]) as conceptSelection:
                    if "+" in conceptSelection.read():
                        return True
                    else:
                        return False
            except IOError:
                return False

        else:
            try:
                with open("concept_selection_files/"+self.conceptSelection[0]) as conceptSelection:
                    if "+" in conceptSelection.read():
                        return True
                    else:
                        return False
            except IOError:
                return False

    def createFilePaths(self):
        """ If a suffix is passed, it is included in input and output
        filepaths. """
        self.cooccFilePath = "source_texts/cooccurrences_"+self.projectID+"_"\
        +self.setID+self.suffix+".txt"
        if self.suffix == "":
            self.outputFilePath = 'results/cocounts_'+'_'.join(\
            self.argumentList[1:])+".csv"
        else:
            self.outputFilePath = 'results/cocounts_'+'_'.join(\
            self.argumentList[1:3])+self.suffix+".csv"


    def remove_duplicates_in_simple_text_selection(self):
        self.textSelectionList = set(self.textSelectionList)
        self.textSelectionList = list(self.textSelectionList)

    def remove_duplicates_in_text_selection_groups(self):
        textSelectionList = []
        group = []
        for textSelection in self.textSelectionList:
            groupname = textSelection[0]
            textSelection = set(textSelection[1])
            textSelection = list(textSelection)
            textSelectionList.append([groupname,textSelection])
        self.textSelectionList = textSelectionList

    def or_count(self,textSelection,summationMethod):
        """Reads the cooccurrence file and passes concept pairs and cooccurrence
        scores of selected text to the function self.add_concept_pair_or."""
        groupName = ""
        # Test if the text selection is a group and remember the name of
        # the group.
        if textSelection[0][0].isalpha():
            groupName = textSelection[0]
            textSelection = textSelection[1]

        # Make a list with all pairs of concept groups.
        groupPairs = itertools.combinations(self.conceptSelectionList,2)
        for group in groupPairs:
            with open(self.cooccFilePath) as cooccFile:
                for line in cooccFile:
                    line = line.rstrip()
                    line = line.split(",")
                    if line[0] in textSelection:
                        self.add_concept_pair_or(line[1],line[2],line[3],group,summationMethod)
        self.write_to_file_or(groupName)

    def add_concept_pair_or(self,concept1,concept2,score,group,summationMethod):
        """Writes cooccurrence scores of concept pairs in the concept selections
        in a dictionary."""
        groupName = str(group)
        if (concept1 in group[0] and concept2 in group[1]) or (concept1\
        in group[1] and concept2 in group[0]):
            if groupName in self.cooccScoreDict:
                if summationMethod == "c":
                        self.cooccScoreDict[groupName] +=1
                elif summationMethod == "s":
                        self.cooccScoreDict[groupName] += score
            else:
                if summationMethod == "c":
                        self.cooccScoreDict[groupName] = 1
                elif summationMethod == "s":
                        self.cooccScoreDict[groupName] = score


    def detect_and_run_option(self):
        """ Checks the command line arguments for which option should be
        called. If the textSelectionList is a list of lists, the count
        method is called for each list in textSelectionList. That is the
        case if the grouping file contains groups of texts. If the
        textSelectionList is a list containing IDs, the count method is
        called only once. That is they case when the grouping file is a
        simple grouping file."""

        # The text selection contains groups.
        if self.textSelectionList[0][0].isalpha():
            for textSelection in self.textSelectionList:
                if self.argumentList[4].startswith("c"):
                    if self.argumentList[4] == "c":
                        if self.or_option:
                            self.or_count(textSelection,"c")
                        else:
                            self.count(textSelection,"c",True)
                    else:
                        self.count_lower_bound(textSelection,True)
                if self.argumentList[4] == "s":
                    if self.or_option:
                        self.or_count(textSelection,"s")
                    else:
                        self.count(textSelection,"s",True)
        # The text selection does not contain groups.
        else:
            if self.argumentList[4].startswith("c"):
                if self.argumentList[4] == "c":
                    if self.or_option:
                        self.or_count(self.textSelectionList,"c")
                    else:
                        self.count(self.textSelectionList,"c",True)
                else:
                    self.count_lower_bound(self.textSelectionList,True)
            if self.argumentList[4] == "s":
                if self.or_option:
                    self.or_count(self.textSelectionList,"s")
                else:
                    self.count(self.textSelectionList,"s",True)

    def detect_type_of_text_selection(self):
        """ Reads the grouping file and adds the selected texts to a
        list. If it contains groups, the method read_grouping_file is
        called.
        """
        groupingFilePath = "grouping_files/"+self.textSelection
        with open(groupingFilePath) as groupingFile:
            if groupingFile.read().startswith("id\n"):
                self.textSelectionList = self.read_IDs_from_File(\
                groupingFilePath,False)
                self.remove_duplicates_in_simple_text_selection()
            else:
                self.read_grouping_file(groupingFilePath)
                self.remove_duplicates_in_text_selection_groups()

    def read_IDs_from_File(self,string,conceptIDs):
        """Reads concept IDs or text IDs from a file and returns a list
        of concept IDs or text IDs. If the function is called to read
        conceptIDs, the value of the third parameter is True to convert
        the IDs to integers. This is necessary for the lookup in the
        count function."""
        idList = []
        with open(string) as inputFile:
            for line in inputFile:
                line = line.rstrip()
                if "id" not in line:
                    if conceptIDs == True:
                        idList.append(int(line))
                    else:
                        idList.append(line)
        return idList

    def read_grouping_file(self,string):
        """ If the grouping file contains group definitions, they are
        saved in a dictionary. The textSelectionList contains one list
        of texts for each group when groups are defined in the grouping
        file. The first element of these lists is the name of the group.
        """
        with open(string) as inputFile:
            iterLines = iter(inputFile)
            next(iterLines)
            for line in iterLines:
                line = line.rstrip().split(",")
                conceptID = line[0]
                for groupName in line[1:]:
                    if groupName != "":
                        if groupName in self.textSelectionDict:
                            self.textSelectionDict[groupName].append(\
                            conceptID)
                        else:
                            self.textSelectionDict[groupName] = [conceptID]
        for item in self.textSelectionDict.items():
            self.textSelectionList.append(list(item))

    def create_concept_selection_list(self):
        """Detects either a concept selection file, conceptIDs
        specified in the command line arguments or the special concept
        selections any or all.
        The selected concepts are stored in a list. If a suffix is
        passed, it is deleted from the concept selection and saved in a
        variable. """
        # A concept selection file, all or any and no suffix is passed.
        if len(self.conceptSelection) == 1:
            if self.conceptSelection[0] == "all":
                self.conceptSelectionList = range(10001,40717)
            elif self.conceptSelection[0] == "any":
                self.conceptSelectionList = range(10001,40717)
            else:
                # Change so that the concepts end up being integers.
                conceptSelectionPath = "concept_selection_files/"\
                +self.conceptSelection[0]
                if self.or_option:
                    self.readOrConceptSelection()
                else:
                    self.conceptSelectionList =\
                    self.read_IDs_from_File(conceptSelectionPath,True)
        if len(self.conceptSelection) == 2:
            # A suffix is passed.
            if "_" in self.conceptSelection[0]:
                # Save suffix and delete from conceptSelection.
                self.suffix = self.conceptSelection[0]
                del self.conceptSelection[0]
                # Concept selection is all or any.
                if self.conceptSelection[0] == "all":
                    self.conceptSelectionList = range(10001,40717)
                elif self.conceptSelection[0] == "any":
                    self.conceptSelectionList = range(10001,40717)
                else:
                    # A concept selection file is passed.
                    conceptSelectionPath = "concept_selection_files/"\
                    +self.conceptSelection[0]
                    if self.or_option:
                        self.readOrConceptSelection()
                    else:
                        self.conceptSelectionList =\
                        self.read_IDs_from_File(conceptSelectionPath,True)
            # Two concepts are passed.
            else:
                self.conceptSelectionList = [int(concept) for concept in\
                self.conceptSelection]
        # A suffix and multitple concepts are passed.
        if len(self.conceptSelection) >= 3:
            if "_" in self.conceptSelection[0]:
                self.suffix = self.conceptSelection[0]
                del self.conceptSelection[0]
                self.conceptSelectionList = [int(concept) for concept in\
                self.conceptSelection]

    def readOrConceptSelection(self):
        with open("concept_selection_files/"+self.conceptSelection[0]) as conceptSelection:
            for line in conceptSelection:
                conceptSet = []
                line = line.rstrip().split("+")
                for concept in line:
                    conceptSet.append(concept)
                self.conceptSelectionList.append(conceptSet)

    def count_lower_bound(self,textSelection,writeToFile):
        """ c<integer> = counting how many documents contain at
        least the specified number of references to this
        (group of) concept(s) """
        #logging.debug('count_lower_bound is called')

    def count(self,textSelection,summationMethod,writeToFile):
        """ Sums cooccurence scores for given sets of concepts and
        texts. Two summations methods are available:
        "c": If a concept pair has a cooccurrence score
        in one of the given texts, the count for the concept pair is
        incremented by one.
        "s": The cooccurrence scores of a concept pair in all selected
        texts are summed.
        If the fourth parameter writeToFile is True, the function
        write_to_file is called at the end of this function. The
        dictionary containing the cooccurrence scores is emptied at the
        end of write_to_file.
        """
        #logging.debug('count is called')
        groupName = ""
        # Test if the text selection is a group and remember the name of
        # the group.
        if textSelection[0][0].isalpha():
            groupName = textSelection[0]
            textSelection = textSelection[1]

        with open(self.cooccFilePath) as cooccFile:
            for line in cooccFile:
                line = line.rstrip()
                line = line.split(",")
                # Look for texts contained in the text selection.
                if line[0] in textSelection:
                    # Look for concept pairs contained in the concept
                    # selection.
                    if int(line[1]) in self.conceptSelectionList:
                        if int(line[2]) in self.conceptSelectionList:
                            conceptPair = (line[1],line[2])
                            if summationMethod == "c":
                                if conceptPair in self.cooccScoreDict:
                                    self.cooccScoreDict[conceptPair] +=1
                                else:
                                    self.cooccScoreDict[conceptPair] = 1
                            if summationMethod == "s":
                                cooccScore = line[3]
                                if conceptPair in self.cooccScoreDict:
                                    self.cooccScoreDict[conceptPair] +=\
                                    float(cooccScore)
                                else:
                                    self.cooccScoreDict[conceptPair] = \
                                    float(cooccScore)
        if writeToFile == True and self.conceptSelection[0] != "any":
            self.write_to_file(groupName)
        elif self.conceptSelection[0] == "any":
                self.write_to_file_any()

    def lookup_concept_pair(self,concept1,concept2):
        """Returns the cooccurence score of a concept pair. If there is
        no score for the concept pair, 0 is returned. """
        conceptPair = (concept1,concept2)
        conceptPairReversed = (concept2,concept1)
        if conceptPair in self.cooccScoreDict:
            return self.cooccScoreDict[conceptPair]
        if conceptPairReversed in self.cooccScoreDict:
            return self.cooccScoreDict[conceptPairReversed]
        else:
            return 0

    def get_output_file_path(self,groupName):
        if groupName != "":
            return self.outputFilePath.rstrip(".csv")+\
            "_"+groupName+".csv"
        else:
            return self.outputFilePath

    def lookup_or(self,group,group2):
        pair1 = (group,group2)
        pair = str(pair1)
        pair2 = (group2,group)
        reversedPair = str(pair2)
        if pair in self.cooccScoreDict:
            return str(self.cooccScoreDict[pair])
        elif reversedPair in self.cooccScoreDict:
            return str(self.cooccScoreDict[reversedPair])
        else:
            return "N.A."

    def write_to_file_or(self,groupName):
        outputPath = self.get_output_file_path(groupName)
        conceptGroups = ["+".join(group) for group in self.conceptSelectionList]
        with open(outputPath,"w") as output:
            if self.IDsOrNot == "y":
                for index,group in enumerate(conceptGroups):
                    if index < len(conceptGroups)-1:
                        output.write(str(group)+",")
                    else:
                        output.write(str(group)+"\n")
            for index,group in enumerate(self.conceptSelectionList):
                if self.IDsOrNot == "y":
                    output.write(str(conceptGroups[index])+",")
                for index2,group2 in enumerate(self.conceptSelectionList):
                        output.write(str(self.lookup_or(group,group2))+",")
                output.write("\n")

    def write_to_file_any(self):
        """ If the concept selection is any, the concept selection is
        newly defined after the count function has been called. Only
        concepts which are keys in the dictionary and therefore have
        non-zero counts are considered and written to the output file.
        """

        nonZeroScoreConcepts = [x[1] for x in self.cooccScoreDict.keys()] +\
        [x[0] for x in self.cooccScoreDict.keys()]

        nonZeroScoreConcepts = sorted(set(list(nonZeroScoreConcepts)))

        with open(self.outputFilePath, 'w') as outputFile:
            # Write the first line, which contains all selected concepts
            # and a the bar spacer XXXXX at the start.
            if self.IDsOrNot == "y":
                outputFile.write("XXXXX,")
                for concept in nonZeroScoreConcepts:
                    if concept != nonZeroScoreConcepts[-1]:
                        outputFile.write(str(concept)+",")
                    else:
                        outputFile.write(str(concept)+"\n")
            # Write all following lines, which contain a concept ID at
            # the start, followed by cooccurrence scores/counts of
            # concept pairs.
            for concept1 in nonZeroScoreConcepts:
                # Write down the first concept, which is than combined
                # with all other concepts to form concept pairs.
                if self.IDsOrNot == "y":
                    outputFile.write(str(concept1)+",")
                for concept2 in nonZeroScoreConcepts:
                    # Check if the concept is the last in the list, to
                    # determine if a comma is needed. Look up the score
                    # for the concept pair and write it down.
                    if concept2 != nonZeroScoreConcepts[-1]:
                        cooccScore = self.lookup_concept_pair(\
                        str(concept1),str(concept2))
                        outputFile.write(str(cooccScore)+",")
                    else:
                        # Write no comma at the end of the line.
                        cooccScore = self.lookup_concept_pair(\
                        str(concept1),str(concept2))
                        outputFile.write(str(cooccScore))
                outputFile.write("\n")

    def write_to_file(self,groupName):
        """Creates a cooccurence matrix for the selected concepts and
        texts. If the 5th command line parameter is y, concept IDs are
        visible in the file. If it is n, no IDs are printed. The
        dictionary containing the cooccurence scores is emptied at the
        end of the function. This is necessary to use the function to
        write multiple output files with dictionarys containing counts
        for different text selection. This is used for grouping files
        with groups."""

        tempOutoutputFilePath = self.get_output_file_path(groupName)

        with open(tempOutoutputFilePath, 'w') as outputFile:
            # Write the first line, which contains all selected concepts
            # and a the bar spacer XXXXX at the start.
            if self.IDsOrNot == "y":
                outputFile.write("XXXXX,")
                for concept in self.conceptSelectionList:
                    if concept != self.conceptSelectionList[-1]:
                        outputFile.write(str(concept)+",")
                    else:
                        outputFile.write(str(concept)+"\n")
            # Write all following lines, which contain a concept ID at
            # the start, followed by cooccurrence scores/counts of
            # concept pairs.
            for concept1 in self.conceptSelectionList:
                # Write down the first concept, which is than combined
                # with all other concepts to form concept pairs.
                if self.IDsOrNot == "y":
                    outputFile.write(str(concept1)+",")
                for concept2 in self.conceptSelectionList:
                    # Check if the concept is the last in the list, to
                    # determine if a comma is needed. Look up the score
                    # for the concept pair and write it down.
                    if concept2 != self.conceptSelectionList[-1]:
                        cooccScore = self.lookup_concept_pair(\
                        str(concept1),str(concept2))
                        outputFile.write(str(cooccScore)+",")
                    else:
                        # Write no comma at the end of the line.
                        cooccScore = self.lookup_concept_pair(\
                        str(concept1),str(concept2))
                        outputFile.write(str(cooccScore))
                outputFile.write("\n")
        #logging.debug(self.cooccScoreDict)
        self.cooccScoreDict = {}

if __name__== '__main__':
    counter = CooccCounter(sys.argv)
    counter.detect_and_run_option()
