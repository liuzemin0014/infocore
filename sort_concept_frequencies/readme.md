sort_concept_frequencies.py extracts frequencies of concepts or concept groups from a td file and sorts them in descending order. The program is stored in infocore_tools/sort_concept_frequencies/app along with the folders "concept_selection_files", "results", "td_files" and "text_selection_files". Those folders are necessary to run the program.
The program is written for python version 2 and can be called like this:
python sort_concept_frequencies.py textSel.txt concSel.txt td_file.txt
The file textSel.txt must be in the folder "text_selection_files", concSel.txt must be in the folder "concept_selection_files" and td_file.txt must be in the folder "td_files".

Formats of Selection Files

A text selection file contains one text ID per line:  
1709402  
1709404  
1709405  
1709406  
1709407  
1709409  

Concept selection files have two allowed formats:  

1.
One concept ID per line:  
10836  
11159  
10082  
30781  
30028  

When the program detects this format, the individual concepts are sorted by their frequency.

2.
Multiple concepts in groups:  
group 1  
10836  
11159  
10082  

group 2  
30781  
30028  
40485  

When a concept selection in this format is given to the program, the groups are sorted by the sum of the frequencies of the concepts contained in the groups.



Output Files


Output files are written to the "results" folder. The output filenames contain the names of all three files passed to the program and the prefix "sortedFrequencies". For example sortedFrequencies_textSel.txt_conSel2.txt_filtered_td_15_639.txt_.txt. Output files contain concept IDs and their frequencies or group names and their frequencies separated by comma. Examples:
40228,64  
30781,50  
11159,42  
30028,35  
10836,24  
10082,15  
40485,11  

group 2,96  
group 1,81  


Example Calls with Existing Selection Files

python sort_concept_frequencies.py textSel.txt conSel1.txt filtered_td_15_639.txt

python sort_concept_frequencies.py textSel.txt conSel2.txt filtered_td_15_639.txt


Calling the Program Easily with Tree

On unix systems the terminal program "tree" facilitates the use of sort_concept_frequencies by calling it on the app folder. Tree
views the content of all folder so the names of the selection files can easily be copied and pasted to the command prompt. Example
for calling tree in the app folder (. is the symbol for the current folder) :

~/infocore/infocore_tools/apps/sort_concept_frequencies/app $ tree .  
.  
├── concept_selection_files  
│   ├── conSel1.txt  
│   └── conSel2.txt  
├── __init__.py  
├── requirements_task_3.txt  
├── results  
│   ├── sortedFrequencies_textSel.txt_conSel1.txt_filtered_td_15_639.txt_.txt  
│   └── sortedFrequencies_textSel.txt_conSel2.txt_filtered_td_15_639.txt_.txt  
├── sort_concept_frequencies.py  
├── td_files  
│   └── filtered_td_15_639.txt  
└── text_selection_files  
    └── textSel.txt  
