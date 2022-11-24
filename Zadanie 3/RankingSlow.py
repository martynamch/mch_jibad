def gen_tokens(filename):
    with open(filename, "r", encoding="utf-8") as infile:
        for line in infile:
            if line.strip():
                tokens = line.rstrip().split()
                yield tokens

def remove_key(d, key):
    r = dict(d)
    if key in r.keys():
        del r[key]
    return r


def clean_word(word):
    replacement_dict = {}
    characters_to_drop = '!.?<>";:-+=/"\'<>[]{}()'
    for c in characters_to_drop:
        replacement_dict[c] = ''

    for key, value in replacement_dict.items():
        word = word.replace(key, value)

    word = word.strip()
    word = word.lower()

    return word

def create_counting_dict(g):
    rank_dict = {}
    for i in g:
        for k in i:
            j = clean_word(k)
            if j not in rank_dict.keys():
                rank_dict[j] = 1
            else:
                prev_count = rank_dict[j]
                rank_dict[j] = prev_count + 1

    rank_dict = remove_key(rank_dict, '')

    return rank_dict

def get_top_n(g, n):

    rank_dict = create_counting_dict(g)

    r = sorted(set(rank_dict.values()), reverse=False)

    for i in range(0, n):
        top = r.pop()
        for k, v in rank_dict.items():
            if v == top:
                print(i+1, ". Słowo \"", k, "\" wystąpiło: ", v, " razy", sep="")


g = gen_tokens("C:\\Users\\marty\\Downloads\\potop.txt")
get_top_n(g, 5)
