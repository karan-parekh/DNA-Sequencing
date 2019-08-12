# DNA Sequencing to get score for a primer with a genome
# Ref: https://pythonforbiologists.com/sequence-similarity-search

import csv


def purify(text):
    """Replaces all new lines and carriage returns in genome text file"""
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    if text.isalpha():
        return text
    else:
        print("Genome text file must only contain alphabets")


def pretty_print_match(subject, query, subject_start, query_start, length):
    """Prints in a proper format for console output"""
    print(str(subject_start) + (' ' * length) + str(subject_start+length))
    print('  ' + subject[subject_start:subject_start+length])
    print('  ' + query[query_start:query_start+length])
    print(str(query_start) + (' ' * length) + str(query_start+length))
    print('\n--------------------\n')


def score_match(subject, query, subject_start, query_start, length, negative_score=False):
    """Matches and returns the score for a primer with the genome at each base"""
    score = 0
    # for each base in the match
    for i in range(0, length):
        # first figure out the matching base from both sequences
        subject_base = subject[subject_start + i]
        query_base = query[query_start + i]
        # then adjust the score up or down
        if subject_base == query_base:
            score = score + 1
        elif negative_score: 
            score = score - 1
    return score


def try_all_matches(subject, query):
    """Carries out all the possible matches for a primer through the entire genome
    and prints the highest score match"""
    old_score = 0
    for subject_start in range(0, len(subject)):
        for query_start in range(0, len(query)):
            for length in range(0, len(query)):
                if subject_start + length < len(subject) and query_start + length < len(query):
                    new_score = score_match(subject, query, subject_start, query_start, length)
                    if new_score > old_score:
                        high_score = new_score
                        old_score = new_score
                        ss = subject_start
                        qs = query_start
    print('Score : ' + str(high_score))
    pretty_print_match(subject, query, ss, qs, length)


if __name__ == "__main__":
    with open('genomes/mac239.txt', 'r') as f:  # opens the genome file and purifies incase of unwanted characters
        dope_genome = f.read()
        genome = purify(dope_genome)

    with open('primers/primers.csv', 'r') as f:  # opens the primer csv file for scoring
        primers = csv.reader(f)
        next(primers)
        for primer in primers:
            print("Name: ", primer[1])
            try_all_matches(genome.upper(), primer[2].upper())
