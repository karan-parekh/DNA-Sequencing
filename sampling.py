import collections

with open('data_files/rod.txt', 'r') as f:
    genome = f.read()

primer = "ATGAATACTCCATGGAGAACCCCAGCAACA"

most_common_char = collections.Counter(primer).most_common(1)[0]
no_of_samples = len(genome) - len(primer) + 1


def get_slices():
    slices = []
    for i in range(no_of_samples):
        s = genome[i: i+len(primer)]
        slices.append(s)
    return slices


def get_tuple_list():
    tuple_list = []
    slices = get_slices()
    for s in slices:
        no = s.count(most_common_char[0])
        t = (s, no)
        tuple_list.append(t)
    return tuple_list


def sort_for_occurs():
    tuple_list = get_tuple_list()
    tuple_list.sort(key=lambda val: val[1], reverse=True)
    print(len(tuple_list))
    return tuple_list


def get_score(query, target):
    score = 0
    for i in range(len(query)):
        if query[i] == target[i]:
            score += 1
    return score


if __name__ == '__main__':
    sorted_list = sort_for_occurs()
    old_score = 0
    for e in sorted_list:
        new_score = get_score(e[0], primer)
        if new_score > old_score:
            high_score = new_score
            old_score = new_score
            match = e[0]
            co = sorted_list.index(e)
            if high_score == len(primer):
                print("Broke off")
                break
        else:
            high_score = old_score
    print(match)
    print(primer)
    print(co)
    print(high_score)










