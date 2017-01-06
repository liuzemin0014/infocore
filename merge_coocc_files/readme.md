merge_coocc_files.py merges the cooccurrence files in the folder "to_merge" and writes the
merged output to the folder "results." Merged cooccurrence files contain all unique lines from the
files in "to_merge". Please replace the example files in to_merge with your own
files before running the program. The program expects the name of the output file to be passed in the program
call. Example:  
python merge_cooc_files.py mergedCooccFiles1234.txt

The files in to_merge are deleted after merging. They can be put in the "coocc_files" folder to keep
a copy.
