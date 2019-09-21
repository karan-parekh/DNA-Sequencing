# DNA-Sequencing

## Introduction: 
Biologists require to find similarities among hundreds of DNA strands which is a tedious manual task and prone to human error. This 
project aims at automating this task and eliminate human error

## Summary: 
The task is to search for a particular region in the target sequence (a 9kb DNA strand) where the query sequence (another DNA strand 
of less than 40b) matches with the highest score / max similarity. This has to be repeated multiple number of times for different 
query sequences on the same target sequence.

## Working:
1. Application accepts the target sequence in a text file and a table of query sequences in a csv file
2. The target sequence is filtered for any kind of unwanted character such as newline or carriage return
3. All the querries are put in a queue for further processing
4. It then searches for the region of highest score in the target for each query 
5. Results are yielded in the results.csv file, as soon as they're generated, in the project directory
6. To further speed up the process, it generates 8 threads for 8 different queries

## Usage:
1. Download and extract the project zip file
2. Run ```main.py``` for GUI
3. Select the text file for Genome (target sequence)
4. Select the csv file for Primers (query sequences)
5. Click Design
6. Resulst will be generated and stored in ```results.csv```

Note: Requires python 3 installed on your machine. 
	  You can install python from www.python.org
