def build(l0):
    l = tuple(set(l0))
    d = {}
    nodes = [0]

    acc_st = {}

    for z in l[0]:
        d_l = {}
        n = nodes[-1]
        d_l[z] = n + 1
        d[n] = d_l
        nodes.append(n + 1)
    acc_st[nodes[-1]] = l[0]

    for el in l[1:]:

        n = 0
        i = 0

        while el[i] in d[n].keys():
            n = d[n][el[i]]
            i += 1

        d_n = {}
        n_ = nodes[-1] + 1
        d_n[el[i]] = n_
        d[n][el[i]] = n_
        nodes.append(n_)
        i += 1

        for z in el[i:]:
            d_l = {}
            n = nodes[-1]
            d_l[z] = n + 1
            d[n] = d_l
            nodes.append(n + 1)
        acc_st[nodes[-1]] = el

    fail_link_dict = {}
    ver_val = []
    for k in d[0].keys():
        fail_link_dict.update({d[0][k]: 0})
        ver_val.append(d[0][k])

    dict_temp = d.copy()
    dict_temp.pop(0)

    while len(dict_temp) != 0:
        vx = []
        for k in ver_val:

            for f in d[k].values():
                for key, value in d[k].items():
                    if value == f:
                        label = key

                new_start = fail_link_dict[k]

                if label in d[new_start].keys():
                    fail_link_dict.update({f: d[new_start][label]})
                else:
                    fail_link_dict.update({f: new_start})

                if f in d.keys():
                    vx.append(f)

            dict_temp.pop(k)

        ver_val = []
        for v in vx:
            ver_val.append(v)

    keys = []

    for k in d.keys():
        keys.append(k)

    acc = []

    for nd in nodes:
        if nd not in keys:
            acc.append(nd)

    return d, fail_link_dict, acc, acc_st


def search(automaton, text):
    trie = automaton[0]
    fail_links = automaton[1]
    acc_state = automaton[3]

    i = 0
    n = 0
    sailed = []
    result = []

    while n < len(text):
        t = text[n]

        if i in acc_state.keys():
            sailed.append(i)
            i = fail_links[i]
        elif t in trie[i].keys():
            i = trie[i][t]
            n += 1
        else:
            if i == 0:
                n += 1
            else:
                i = fail_links[i]
    if i in acc_state:
        sailed.append(i)

    for s in sailed:
        result.append(text.index(acc_state[s]))

    return result

