from general import *


class Sequence:

    def __init__(self, genome_file='genomes/mac239.txt', primers_file='primers/primers.csv', custom_primers=False):
        self.genome_file = genome_file
        self.primers_file = primers_file
        self.custom_primers = custom_primers
        self.genome = None
        self.queue = set()
        self.crawled = set()
        self.queue_file = 'queue.csv'
        self.crawled_file = 'crawled.txt'
        # self.boot()

    def boot(self):
        if self.genome is None:
            with open(self.genome_file, 'r') as f:
                dope_genome = f.read()
                self.genome = self.purify(dope_genome)
        else:
            self.genome = self.purify(self.genome)
        delete_file_contents('results.csv')
        delete_file_contents('crawled.txt')
        delete_file_contents('primers/custom_primers.csv')
        create_data_files()
        self.populate_queue()
        self.queue = file_to_set(self.queue_file)
        self.crawled = file_to_set(self.crawled_file)

    def populate_queue(self):
        if self.custom_primers:
            self.primers_file = 'primers/custom_primers.csv'
        with open(self.primers_file, 'r') as p:
            primers = csv.DictReader(p)

            with open('queue.csv', 'w') as q:
                fieldnames = ['name', 'sequence']
                csv_writer = csv.DictWriter(q, fieldnames=fieldnames)
                for primer in primers:
                    d = {'name': primer['name'], 'sequence': primer['sequence']}
                    csv_writer.writerow(d)

    @measure_time
    def crawl_genome(self, thread_name, primer):
        if primer not in self.crawled:
            original_primer = primer
            primer = primer.split(",")
            primer = {'name': primer[0], 'seq': primer[1]}
            print(thread_name, "now crawling", primer['name'])
            print('Queue ', str(len(self.queue)), '| Crawled ', str(len(self.crawled)))
            print('--------------------\n')
            match_f = self.try_all_matches(self.genome, primer['seq'])
            rev_comp_primer = self.reverse_complement(primer['seq'])
            match_r = self.try_all_matches(self.genome, rev_comp_primer)
            if match_f['score'] > match_r['score']:
                self.print_match(primer['name'], match_f, 'Forward')
                append_to_results(primer['name'], match_f, 'Forward')
            else:
                self.print_match(primer['name'], match_r, 'Reverse')
                append_to_results(primer['name'], match_r, 'Reverse')
            self.queue.remove(original_primer)
            self.crawled.add(original_primer)
            self.update_files()

    def try_all_matches(self, subject, query):
        """Crawls the primer through the entire genome for highest score"""
        subject, query = subject.upper(), query.upper()
        old_score = 0
        for subject_start in range(0, len(subject)):
            for query_start in range(0, len(query)):
                for length in range(0, len(query)):
                    if subject_start + length < len(subject) and query_start + length < len(query):
                        new_score = self.score_match(subject, query, subject_start, query_start, length)
                        if new_score > old_score:
                            high_score = new_score
                            old_score = new_score
                            genome_index = subject_start
                            primer_index = query_start
        return {
            'score': high_score,
            'genome': subject,
            'primer': query,
            'genome_index': genome_index,
            'primer_index': primer_index,
            'length': length
        }

    @staticmethod
    def score_match(subject, query, subject_start, query_start, length):
        """Matches and returns the score for a primer with the genome at each base"""
        score = 0
        # for each base in the match
        for i in range(0, length):
            # first figure out the matching base from both sequences
            subject_base = subject[subject_start + i]
            query_base = query[query_start + i]
            if subject_base == query_base:
                score = score + 1
        return score

    @staticmethod
    def reverse_complement(rev_primer):
        """Returns the reverse complement of the primer"""
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
    def print_match(name, match, direction):
        score, subject, query, subject_start, query_start, length = match.values()
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
    def purify(text):
        """Replaces all new lines and carriage returns in genome text file"""
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        if text.isalpha():  # ToDo: Replace with regular expression for combination of 'ACTG'
            return text
        else:
            print("Genome text file must only contain alphabets")

    def update_files(self):
        set_to_file(self.queue, self.queue_file)
        set_to_file(self.crawled, self.crawled_file)
