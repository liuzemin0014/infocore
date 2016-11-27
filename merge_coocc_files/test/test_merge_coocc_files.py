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
from merge_coocc_files import Merger

class TestMerger(unittest.TestCase):

    def test_merge_coocc1234(self):
        """Compares the manually created file gold_coocc1234.txt with
        the file testMerge1234 created by merge_coocc_files.py"""
        testargs = ["prog", "testMerge1234.txt"]
        with patch.object(sys, 'argv', testargs):
            merger = Merger()
            merger.merge_files()
            merger.write_merged_file()
        with open("results/gold_coocc1234.txt") as gold, open("results/testMerge1234.txt") as output:
            self.assertEqual(gold.read(),output.read())
            os.remove("results/testMerge1234.txt")

if __name__== '__main__':
    unittest.main()
