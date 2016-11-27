#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python version: 2.7.10

import logging
import time
import sys
import unittest
# Add the folder infocore/task1/infocore_tools/app/cocount_scripts
# to the sys.path to be able to import the scripts cocount1.py and cocount2.py.
sys.path.insert(1,'../app')
# Add the folder infocore/task1/infocore_tools/app/ to the sys.path to be able
# to impor the script cocount_main.py.
from cocount import CooccCounter

class TestCocount(unittest.TestCase):

    """
    Most tests run cocount.py with different parameter configurations
    and compares the output to reviewed correct output files. There are
    also tests for functions where no output file is needed.
    """

    def setUp(self):
        pass

    def test_noIDs(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_noIDs.txt", "s", "n", "10381", "10620"])
        cooccCounter.detect_and_run_option()
        with open("test_sources/gold_noIDs_new.txt") as gold, \
        open("results/cocounts_15_639_grouping_file_noIDs.txt_s_n_10381_10620.csv") as countIntOutput:
            goldString = gold.read()
            countIntOutputString = countIntOutput.read()
        self.failUnless(goldString == countIntOutputString)

    def test_conceptSelectionByFile(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_conceptSelByFile.txt","s",\
        "y", "conceptSelection.txt"])
        cooccCounter.detect_and_run_option()
        with open("test_sources/gold_conceptSelByFile.txt") as gold, \
        open("results/cocounts_15_639_grouping_file_conceptSelByFile.txt_s_y_conceptSelection.txt.csv") as output:
            goldString = gold.read()
            outputString = output.read()
        self.failUnless(goldString == outputString)

    def test_simple_grouping_file_add(self):
        counter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_simpleGF2.txt", "s", "y", "10384", "10545"])
        counter.detect_and_run_option()
        with open("test_sources/gold_simple_grouping_file_2_new.csv") as gold, \
        open("results/cocounts_15_639_grouping_file_simpleGF2.txt_s_y_10384_10545.csv") as simpleGFoutput:
            goldString = gold.read()
            simpleGFoutputString = simpleGFoutput.read()
        self.failUnless(goldString == simpleGFoutputString)

    def test_grouping_file_output_group_1(self):
        counter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_withGroups.txt", "s","y", "10024", "10445"])
        counter.detect_and_run_option()
        with open("test_sources/gold_ByGroup_Group1_new.csv") as gold, \
        open("results/cocounts_15_639_grouping_file_withGroups.txt_s_y_10024_10445_Group 1.csv")\
        as output:
            goldString = gold.read()
            outputString = output.read()
        self.failUnless(goldString == outputString)

    def test_grouping_file_output_group_2(self):
        counter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_withGroups.txt", "s","y", "10024", "10445"])
        counter.detect_and_run_option()
        with open("test_sources/gold_ByGroup_Group2_new.csv") as gold, \
        open("results/cocounts_15_639_grouping_file_withGroups.txt_s_y_10024_10445_Group 2.csv")\
        as output:
            goldString = gold.read()
            outputString = output.read()
        self.failUnless(goldString == outputString)

    def test_grouping_file_output_group_high(self):
        counter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_withGroups.txt", "s","y", "10024", "10445"])
        counter.detect_and_run_option()
        with open("test_sources/gold_ByLevel_high_new.csv") as gold, \
        open("results/cocounts_15_639_grouping_file_withGroups.txt_s_y_10024_10445_high.csv")\
        as output:
            goldString = gold.read()
            outputString = output.read()
        self.failUnless(goldString == outputString)

    def test_grouping_file_output_group_low(self):
        counter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_withGroups.txt", "s","y", "10024", "10445"])
        counter.detect_and_run_option()
        with open("test_sources/gold_ByLevel_low_new.csv") as gold, \
        open("results/cocounts_15_639_grouping_file_withGroups.txt_s_y_10024_10445_low.csv")\
        as output:
            goldString = gold.read()
            outputString = output.read()
        self.failUnless(goldString == outputString)

    def test_concept_selection_all_summation_s(self):
        counter = CooccCounter(["xy.py", "15", "639",\
        "all_texts.txt", "s","y", "all"])
        counter.count(counter.textSelectionList,"s",False)
        self.assertEqual(counter.cooccScoreDict[("10234","11067")],1.516)
        self.assertEqual(counter.cooccScoreDict[("10234","40648")],2.993)
        self.assertEqual(counter.cooccScoreDict[("10944","10945")],0.057)
        self.assertEqual(counter.cooccScoreDict[("10005","10837")],2.536)

    def test_concept_selection_all_summation_c(self):
        counter = CooccCounter(["xy.py", "15", "639",\
        "all_texts.txt", "c","y", "all"])
        counter.count(counter.textSelectionList,"c",False)
        self.assertEqual(counter.cooccScoreDict[("10234","11067")],1)
        self.assertEqual(counter.cooccScoreDict[("10234","40648")],1)
        self.assertEqual(counter.cooccScoreDict[("10944","10945")],1)
        self.assertEqual(counter.cooccScoreDict[("10005","10837")],2)

    def test_concept_selection_any_sum(self):
        counter = CooccCounter(["xy.py", "15", "639",\
        "all_texts.txt", "s","y", "any"])
        counter.count(counter.textSelectionList,"s",False)
        self.assertEqual(counter.cooccScoreDict[("10017","10035")],1.122)

    def test_concept_selection_any_count_with_suffix(self):
        counter = CooccCounter(["xy.py", "15", "639",\
        "all_texts.txt", "s","y", "_suffixAny","any"])
        counter.detect_and_run_option()
        self.assertEqual(counter.cooccScoreDict[("10017","10035")],1.122)

    def test_create_concept_selection_list_passing_string(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_count.txt", "c", "y","10836", "11159"])
        self.assertEqual(cooccCounter.conceptSelectionList,[10836,11159])

    def test_create_concept_selection_list_passing_file(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_count.txt", "c", "y","conceptSelectionDetectTest.txt"])
        self.assertEqual(cooccCounter.conceptSelectionList,[10836,11159])

    def test_read_grouping_file(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_count.txt", "c", "y","conceptSelectionDetectTest.txt"])
        self.assertEqual(cooccCounter.textSelectionList,["1709404","1709420","1709419"])

    def test_if_count_gives_the_right_counts_one(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_count.txt", "c", "y","10836", "11159"])
        cooccCounter.count(cooccCounter.textSelectionList,"c",False)
        self.assertEqual(cooccCounter.cooccScoreDict[("10836","11159")],3)

    def test_if_count_gives_the_right_counts_two(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "all_texts.txt", "c", "y","30763","30092"])
        cooccCounter.count(cooccCounter.textSelectionList,"c",False)
        self.assertEqual(cooccCounter.cooccScoreDict[("30092","30763")],17)

    def test_count_with_concept_selection_file_one(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "all_texts.txt", "c", "y",\
        "conceptSelectionCountTestWithFileOne.txt"])
        cooccCounter.detect_and_run_option()
        gold = open("test_sources/gold_count_test_with_file_one.csv")
        output = open("results/cocounts_15_639_all_texts.txt_c_y_conceptSelectionCountTestWithFileOne.txt.csv")
        goldString = gold.read()
        outputString = output.read()
        gold.close()
        output.close()
        self.assertEqual(goldString,outputString)

    def test_count_with_concept_selection_file_with_duplicates(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "all_texts.txt", "c", "y",\
        "conceptSelectionCountTestWithFileTwo.txt"])
        cooccCounter.detect_and_run_option()
        gold = open("test_sources/gold_count_test_with_file_two.csv")
        output = open("results/cocounts_15_639_all_texts.txt_c_y_conceptSelectionCountTestWithFileTwo.txt.csv")
        goldString = gold.read()
        outputString = output.read()
        gold.close()
        output.close()
        self.assertEqual(goldString,outputString)

    def test_detect_and_run_option_count(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_count.txt", "c", "y","10836", "11159"])
        cooccCounter.detect_and_run_option()
        gold = open("test_sources/gold_count_additional_options.txt")
        output = open("results/cocounts_15_639_grouping_file_count.txt_c_y_10836_11159.csv")
        goldString = gold.read()
        outputString = output.read()
        gold.close()
        output.close()
        self.assertEqual(goldString,outputString)

    def test_count(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_count.txt", "c", "y","10836", "11159"])
        cooccCounter.detect_and_run_option()
        with open("test_sources/gold_count.csv") as gold, \
        open("results/cocounts_15_639_grouping_file_count.txt_c_y_10836_11159.csv") as countOutput:
            goldString = gold.read()
            countOutputString = countOutput.read()
        self.failUnless(goldString == countOutputString)

    def test_count_with_suffix(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",\
        "grouping_file_count.txt", "c", "y","_suffix","10836", "11159"])
        cooccCounter.detect_and_run_option()
        with open("test_sources/gold_count.csv") as gold, \
        open("results/cocounts_15_639_suffix.csv") as countOutput:
            goldString = gold.read()
            countOutputString = countOutput.read()
        self.failUnless(goldString == countOutputString)

    def test_count_with_suffix_and_concept_selection_file(self):
        cooccCounter = CooccCounter(["cocount_main.py", "15", "639",
        "grouping_file_count.txt", "c", "y","_suffix2",
        "exampleConceptSelection.txt"])
        cooccCounter.detect_and_run_option()
        with open("test_sources/gold_count.csv") as gold, \
        open("results/cocounts_15_639_suffix2.csv") as countOutput:
            goldString = gold.read()
            countOutputString = countOutput.read()
        self.failUnless(goldString == countOutputString)

    def test_or(self):
        cooccCounter = CooccCounter(["program", "15", "639",
        "all_texts.txt", "s", "y",
        "or.txt"])
        cooccCounter.detect_and_run_option()
        with open("test_sources/gold_or_sum.txt") as gold, \
        open("results/cocounts_15_639_all_texts.txt_s_y_or.txt.csv") as output:
            goldString = gold.read()
            countOutputString = output.read()
        self.failUnless(goldString == countOutputString)

    def test_or2(self):
        cooccCounter = CooccCounter(["program", "15", "639",
        "all_texts.txt", "c", "y",
        "or2.txt"])
        cooccCounter.detect_and_run_option()
        with open("test_sources/gold_or_count.txt") as gold, \
        open("results/cocounts_15_639_all_texts.txt_c_y_or2.txt.csv") as output:
            goldString = gold.read()
            countOutputString = output.read()
        self.failUnless(goldString == countOutputString)

    def test_or_with_mutual_concept(self):
        cooccCounter = CooccCounter(["program", "15", "639",
        "all_texts.txt", "c", "y",
        "or3.txt"])
        cooccCounter.detect_and_run_option()
        with open("test_sources/gold_or_count2.txt") as gold, \
        open("results/cocounts_15_639_all_texts.txt_c_y_or3.txt.csv") as output:
            goldString = gold.read()
            countOutputString = output.read()
        self.failUnless(goldString == countOutputString)

    def test_or_with_identical_groups(self):
        cooccCounter = CooccCounter(["program", "15", "639",
        "all_texts.txt", "c", "y",
        "or4.txt"])
        cooccCounter.detect_and_run_option()
        with open("test_sources/gold_or_count3.txt") as gold, \
        open("results/cocounts_15_639_all_texts.txt_c_y_or4.txt.csv") as output:
            goldString = gold.read()
            countOutputString = output.read()
        self.failUnless(goldString == countOutputString)

    def test_or_with_three_groups(self):
        cooccCounter = CooccCounter(["program", "15", "639",
        "all_texts.txt", "c", "y",
        "or5.txt"])
        cooccCounter.detect_and_run_option()
        with open("test_sources/gold_or_count5.txt") as gold, \
        open("results/cocounts_15_639_all_texts.txt_c_y_or5.txt.csv") as output:
            goldString = gold.read()
            countOutputString = output.read()
        self.failUnless(goldString == countOutputString)






    # def test_concept_selection_all_with_suffix(self):
    #     counter = CooccCounter(["xy.py", "15", "639",\
    #     "all_texts.txt", "s","y", "_suffixAll","all"])
    #     counter.detect_and_run_option()

if __name__== '__main__':
    unittest.main()
