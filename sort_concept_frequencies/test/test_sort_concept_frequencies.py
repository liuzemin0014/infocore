#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python version: 2.7.11

import logging
import time
import sys
import unittest
# Import patch to emulate command line arguments by replacing sys.argv.
from mock import patch
import os

sys.path.insert(1,'../app')
from sort_concept_frequencies import FreqCounter

class TestFreqCounter(unittest.TestCase):

    def test_FreqCounter_conSel2(self):
        testargs = ["prog", "filtered_td_15_639.txt", "conSel2.txt","textSel.txt"]
        with patch.object(sys, 'argv', testargs):
            freqCounter = FreqCounter()
        with open("results/gold_conSel2.txt") as gold, open (\
        "results/sortedFrequencies_filtered_td_15_639.txt_conSel2.txt_textSel.txt_.txt")\
        as output:
            self.assertEqual(gold.read(),output.read())

    def test_FreqCounter_without_concept_selection(self):
        testargs = ["prog", "filtered_td_15_639.txt", "conSel2.txt"]
        with patch.object(sys, 'argv', testargs):
            freqCounter = FreqCounter()
        with open("results/gold_conSel2.txt") as gold, open (\
        "results/sortedFrequencies_filtered_td_15_639.txt_conSel2.txt_.txt")\
        as output:
            self.assertEqual(gold.read(),output.read())

if __name__== '__main__':
    unittest.main()
