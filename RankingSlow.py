def gen_tokens(filename):
    with open(filename, "r", encoding="utf-8") as infile:
        for line in infile:
            if line.strip():
                tokens = line.rstrip().split()
                yield tokens    # na pewno?

def remove_key(d, key):
    r = dict(d)
    if key in r.keys():
        del r[key]
    return r


def clean_word(word):
    replacement_dict = {}   # prosi się o dict comprehension
    characters_to_drop = '!.?<>";:-+=/"\'<>[]{}()'
    for c in characters_to_drop:
        replacement_dict[c] = ''

    for key, value in replacement_dict.items():
        word = word.replace(key, value)

    word = word.strip()
    word = word.lower()

    return word

def create_counting_dict(g):  # nieczytelna nazwa parametru
    rank_dict = {}    # polecam klasę collections.Counter
    for i in g: # nieczytelne nazwy
        for k in i:
            j = clean_word(k)  # jw.
            if j not in rank_dict.keys():
                rank_dict[j] = 1
            else:
                rank_dict[j] = rank_dict[j] + 1

    rank_dict = remove_key(rank_dict, '')   # a czemu nie użyć tutaj del?

    return rank_dict

def get_top_n(g, n):

    rank_dict = create_counting_dict(g)

    r = sorted(set(rank_dict.values()))

    for i in range(0, n):
        top = r.pop()
        for k, v in rank_dict.items():  # bardzo niewydajne
            if v == top:
                print(i+1, ". Słowo \"", k, "\" wystąpiło: ", v, " razy", sep="")
        # źle działa, jeśli remis wystąpi wcześniej niż na końcu


g = gen_tokens("C:\\Users\\marty\\Downloads\\potop.txt")    # proszę nie zaszywać ścieżek bezwzględnych w kodzie
get_top_n(g, 100)
