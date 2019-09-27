# DNA-Sequencing

## Introduction: 
Biologists require to find similarities among hundreds of DNA strands which is a tedious manual task and prone to human error. This project 
aims at automating this task and eliminate human error

## Summary: 
The task is to search for a particular region in the target sequence (a 9kb DNA strand) where the query sequence (another DNA strand of less than 40b) matches with the highest score/max similarity. This has to be repeated multiple number of times for different query
sequences on the same target sequence.

## Working:
1. The application accepts the target sequence in a text file and a table of query sequences in a csv file
2. The target sequence is filtered for any kind of unwanted characters such as newline or carriage return
3. All the queries are put in a queue for further processing
4. It then searches for the region of the highest score in the target for each query
5. Output for each query is a row of values with headers ```name```, ```sequence```, ```direction```, ```score```, ```start```, ```end``` 
5. Results are yielded in the results.csv file, as soon as they're generated, in the project directory
6. To further speed up the process, it generates 8 threads for 8 different queries

## Usage:
1. Download and extract the project zip file
2. Open terminal/command prompt in the project folder
3. Run ```python main_ui.py``` command
4. On the GUI, select the text file for Genome (target sequence)
5. Select the csv file for Primers (query sequences)
6. Click Design
7. Results will be generated and stored in ```results.csv```

### Note: 
1. Requires python 3 installed on your machine. You can install python from www.python.org
2. It may take several minutes to complete all the calculations, depending on size of your input files

### Areas of improvement:
1. Need to develop an efficient algorithm for faster processing
2. Need to implement Memoization