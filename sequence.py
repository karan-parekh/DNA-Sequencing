from general import *


class Sequence:

    genome = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self):
        Sequence.queue_file = 'queue.csv'
        Sequence.crawled_file = 'crawled.txt'
        self.boot()

    @staticmethod
    def boot():
        with open('genomes/mac239.txt', 'r') as f:  # opens the genome file and purifies in-case of unwanted characters
            dope_genome = f.read()
            Sequence.genome = Sequence.purify(dope_genome)
        create_data_files()
        Sequence.queue = file_to_set(Sequence.queue_file)
        Sequence.crawled = file_to_set(Sequence.crawled_file)

    @staticmethod
    def crawl_genome(thread_name, primer):
        if primer not in Sequence.crawled:
            original_primer = primer
            primer = primer.split(",")
            primer = {'name': primer[0], 'seq': primer[1]}
            print(thread_name, "now crawling", primer['name'])
            print('Queue ', str(len(Sequence.queue)), '| Crawled ', str(len(Sequence.crawled)))
            print('--------------------\n')
            match_f = Sequence.try_all_matches(Sequence.genome, primer['seq'])
            rev_comp_primer = Sequence.reverse_complement(primer['seq'])
            match_r = Sequence.try_all_matches(Sequence.genome, rev_comp_primer)
            if match_f['score'] > match_r['score']:
                Sequence.print_match(primer['name'], match_f['score'], match_f['genome'], match_f['primer'],
                                     match_f['genome_index'], match_f['primer_index'], match_f['length'], 'F')
            else:
                Sequence.print_match(primer['name'], match_r['score'], match_r['genome'], match_r['primer'],
                                     match_r['genome_index'], match_r['primer_index'], match_r['length'], 'R')
            Sequence.queue.remove(original_primer)
            Sequence.crawled.add(original_primer)

    @staticmethod
    def try_all_matches(subject, query):
        """Crawls the primer through the entire genome for highest score"""
        subject, query = subject.upper(), query.upper()
        old_score = 0
        for subject_start in range(0, len(subject)):
            for query_start in range(0, len(query)):
                for length in range(0, len(query)):
                    if subject_start + length < len(subject) and query_start + length < len(query):
                        new_score = Sequence.score_match(subject, query, subject_start, query_start, length)
                        if new_score > old_score:
                            high_score = new_score
                            old_score = new_score
                            genome_index = subject_start
                            primer_index = query_start
        return {'score': high_score,
                'genome': subject,
                'primer': query,
                'genome_index': genome_index,
                'primer_index': primer_index,
                'length': length}

    @staticmethod
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

    @staticmethod
    def reverse_complement(rev_primer):
        rev_primer = rev_primer[::-1]
        comp_primer = []
        for p in rev_primer:
            if p == 'A':
                comp_primer.append('T')
            elif p == 'C':
                comp_primer.append('G')
            elif p == 'T':
                comp_primer.append('A')
            elif p == 'G':
                comp_primer.append('C')

        return "".join(comp_primer)

    @staticmethod
    def print_match(name, score, subject, query, subject_start, query_start, length, direction):
        """Prints in a proper format for console output"""
        print("Name: ", name)
        print("Direction: ", direction)
        print('Score : ' + str(score))
        print(str(subject_start) + (' ' * length) + str(subject_start + length))
        print('  ' + subject[subject_start:subject_start + length])
        print('  ' + query[query_start:query_start + length])
        print(str(query_start) + (' ' * length) + str(query_start + length))
        print('\n--------------------\n')

    @staticmethod
    def update_files():
        set_to_file(Sequence.queue, Sequence.queue_file)
        set_to_file(Sequence.crawled, Sequence.crawled_file)

    @staticmethod
    def purify(text):
        """Replaces all new lines and carriage returns in genome text file"""
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        if text.isalpha():
            return text
        else:
            print("Genome text file must only contain alphabets")




