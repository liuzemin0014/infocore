cocount.py is contained in the folder infocore_tools/app. It reads cooccurrence files created by the script cooc.py. Cooccurrence files contain a textID, two concepts IDs and a cooccurrence score separated by commas in every line. Ex.
1709402,10234,40648,2.993
cocount.py provides options to count cooccurrences scores of concept pairs for specific concepts and texts. The output of cocount.py is a cooccurrence matrix which depends on the parameters passed to the program. The cooccurrence scores in the output have three decimal places after the decimal mark.
Output files are named "cocounts_" followed by the full program call if no suffix is passed. If a suffix is passed output files start with "cocounts_" followed by the project ID, set ID and the suffix. Output files are written to the results folder. Example calls are at the end of this file. The program can be run in the infocore_tools/app folder. Results are than created in the folder infocore_tools/results.
Several example output files can be created by running the automated tests in the test folder. This can be done by running the test_cocount.py file in the folder infocore_tools/test. Ex. python test_cocount.py. Output files are than created in infocore_tools/test/results. The program is written for python version 2. 

There are seven parameters which control the behaviour of the program:

1. project ID
2. set ID
3. grouping file
4. add or count (s,c)
5. ids or no ids (y,n)
6. optional: suffix
7. selection of concepts

1. and 2:
The projectid and the setid define which cooccurrence file should be opened. The cooccurrence files should be placed in the source_texts folder.

3. The grouping file defines which texts should be considered. The two types of grouping files are simple grouping files and grouping files with groups. Grouping files should be placed in the grouping_files folder. A simple grouping files first line contains the word "id". All other lines contain one text ID. A grouping file with groups first line starts with id followed by a comma and a letter or word. The letter or word is arbitrary. It is only used to discern a grouping file with groups from a simple grouping file. If more than one group is assigned to one text, the letters or words in the first line are as many as groups to be assigned. The other lines in a grouping file with groups assign a text ID to one or multiple groups. The first entry in the line is the text ID followed by a comma and the name of the group. More commas and group names follow if more than one group is assigned. Group names are not allowed to start with numbers. One output file is created for each group. Examples of a grouping files are given below.

4. The fourth parameter defines the counting method. Add adds the cooccurrence scores of the selected concepts. It is called by passing "s" as the fourth parameter. Count counts how many texts contain at least one cooccurrence of one of the selected concept pairs. It is called by passing "c" as the fourth parameter.

5. The fifth parameter defines if concept IDs should be written to the output file. If y is passed, concept IDs are written to the output. If n is passed, no IDs are written to the output.

6. The sixth parameter is optional. With it a suffix containing an underscore can be passed. If a suffix is passed, the program expects a cooccurrence file with a suffix. Ex. cooccurrences_15_639_suffix.txt. The suffix is attached to the output file. Ex. cocounts_15_639_suffix.csv.

7. The concepts to be considered are selected in the seventh parameter. There are three ways of passing concepts. The first way is to directly pass them via the command line. See example call 1 below. The second option is to provide a concept selection file. A concept selection file contains one concept ID per line. Concept selection files should be placed in the concept_selection_files folder. Concept selection files must not contain underscores. The third way of passing concepts is via the keywords "all" and "any". All considers all concept pairs of concepts 10001 until 401716. Any considers all concept pairs which have none-zero cooccurrence counts in the cooccurrence file. An example call for any can be seen below. The selection all can take some time because many concepts are considered. This also depends on the size of the text selection. The cooccurrence scores are computed for every pair which can be formed from the selected concepts. Ex. If concepts 1 5 and 7 are selected, pairs 1;5, 1;7, 5;7 and 1,7 are considered. Reversed pairs like 5;1 are also shown in the output matrix. They have the same scores like their reverse pair. 


Example for a simple grouping file:

id
1709402
1709412
1709413

Example for a grouping file with groups:

id,a,b
1722473,Group 1,high
1709404,Group 2,low
1709418,,high
1709419,Group 1,

Example for a concept selection file:
10836
11159
10082

Example calls:

1.
Count cooccurrences of the concepts 10381 and 10620 in the texts contained in example_grouping_file.txt in the file cooccurrences_15_639.txt. Sum cooccurrence scores (s). Don't write concept IDs to the output file (n).

python cocount.py 15 639 example_grouping_file.txt s n 10381 10620

output file: infocore_tools/app/results/cocounts_15_639_example_grouping_file.txt_s_n_10381_10620.csv


2.
Count cooccurrences of the concepts contained in exampleConceptSelction.txt in the texts contained in example_grouping_file.txt in the file cooccurrences_15_639.txt. Add the number of texts, which contain a cooccurrence of one of the concepts pairs (c). Write concept IDs to the output file (y).

python cocount.py 15 639 example_grouping_file.txt c y exampleConceptSelection.txt

output file: infocore_tools/app/results/cocounts_15_639_example_grouping_file.txt_c_y_exampleConceptSelection.txt.csv

3. 

Count cooccurrences of the concepts contained in exampleConceptSelection.txt in the texts contained in grouping_file_withGroups.txt in the file cooccurrences_15_639.txt. Sum cooccurrence scores (s). Write concept IDs to the output file (y).

python cocount.py 15 639 grouping_file_withGroups.txt s y exampleConceptSelection.txt

output files:
infocore_tools/app/results/cocounts_15_639_grouping_file_withGroups.txt_s_y_exampleConceptSelection.txt_Group 1.csv
infocore_tools/app/results/cocounts_15_639_grouping_file_withGroups.txt_s_y_exampleConceptSelection.txt_Group 2.csv
infocore_tools/app/results/cocounts_15_639_grouping_file_withGroups.txt_s_y_exampleConceptSelection.txt_high.csv
infocore_tools/app/results/cocounts_15_639_grouping_file_withGroups.txt_s_y_exampleConceptSelection.txt_low.csv

4. Count cooccurrences of concept pairs which have none-zero counts in cooccurrences_15_639 and occurr in texts contained in example_grouping_file.txt. Add the number of texts which contain a cooccurence of one of the concept pairs (c). Write concept IDs to the output file (y).

python cocount.py 15 639 example_grouping_file.txt c y any

5. Same as 4 with a suffix. Note that a cooccurrence file named cooccurrences_15_639_suffix.txt is necessary to call the program like this. The cooccurrence file should be placed in the folder infocore_tools/app/source_texts

python cocount.py 15 639 example_grouping_file.txt c y _suffix any
