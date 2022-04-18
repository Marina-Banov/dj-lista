import sys
import random
from utils import get_db, DATA_FILE, is_valid

RES_FILE = "../res/res.txt"
MERGING_KEY = "3B"


def get_new_element(last, by_tempo, tempo_dict, key_dict):
    last = random.choice(
        tempo_dict[last.tempo] if by_tempo else key_dict[last.key]
    )

    tempo_dict[last.tempo].remove(last)
    # TODO is this maybe necessary?
    # if len(tempo_dict[last.tempo]) == 1:
    #     s = tempo_dict[last.tempo][0]
    #     key_dict[s.key].remove(s)
    #     del tempo_dict[last.tempo]
    key_dict[last.key].remove(last)

    if len(key_dict[last.key]) == 1 and not by_tempo:
        s = key_dict[last.key][0]
        tempo_dict[s.tempo].remove(s)
        del key_dict[last.key]

    return last


def generate_random_playlist(first, tempo_dict, key_dict):
    playlist = [first]
    last = first
    i = 0

    while True:
        i += 1

        if i % 2:
            if tempo_dict.get(last.tempo):
                last = get_new_element(last, True, tempo_dict, key_dict)
                playlist.append(last)
            else:
                return playlist
        else:
            if key_dict.get(last.key):
                last = get_new_element(last, False, tempo_dict, key_dict)
                playlist.append(last)
            else:
                return playlist


def merge(list_pieces, db):
    res = []
    unmatched = []
    for i in list_pieces:
        if len(res) == 0 or db[i[0]].key == db[res[-1]].key:
            res.extend(i)
        else:
            unmatched.append(i)

    while True:
        changed = False
        for i in unmatched:
            if db[i[0]].key == db[res[-1]].key:
                res.extend(i)
                changed = True
            elif db[i[-1]].key == db[res[-1]].key:
                res.extend(i[::-1])
                changed = True
            elif db[i[0]].key == db[res[0]].key:
                res = i[::-1] + res
                changed = True
            elif db[i[-1]].key == db[res[0]].key:
                res = i + res
                changed = True
            if changed:
                unmatched.remove(i)
                break
        if not changed:
            break

    return res


def get_list_pieces(tempo_dict):
    tempo_dict_copy = tempo_dict.copy()
    list_pieces = []
    res_len = 0

    for key, value in tempo_dict_copy.items():
        if len(value) == 1:
            continue

        if len(tempo_dict[key]) == 2:
            list_pieces.append([value[0].id, value[1].id])
            res_len += 2
            continue

        # TODO why is this so uch slower than reading from files?
        # print(f"{len(list_pieces)}/{len(tempo_dict.keys())}")
        key_dict = {}
        for v in value:
            if key_dict.get(v.key) is None:
                key_dict[v.key] = [v]
            else:
                key_dict[v.key].append(v)

        for k in key_dict.copy():
            if len(key_dict[k]) == 1:
                tempo_dict_copy[key].remove(key_dict[k][0])
                del key_dict[k]

        if len(tempo_dict_copy[key]) == 0:
            with_key = [s for s in tempo_dict[key] if s.key == MERGING_KEY]
            if len(with_key) == 1:
                r = random.choice(tempo_dict[key])
                while r == with_key[0]:
                    r = random.choice(tempo_dict[key])
                list_pieces.append([with_key[0].id, r.id])
            else:
                try:
                    r = random.sample(tempo_dict[key], 2)
                    list_pieces.append([r[0].id, r[1].id])
                except ValueError:  # TODO
                    continue
            res_len += 2
            continue

        if len(tempo_dict_copy[key]) == 2:
            list_pieces.append([tempo_dict_copy[key][0].id,
                                tempo_dict_copy[key][1].id])
            res_len += 2
            continue

        if key_dict.get(MERGING_KEY) and len(key_dict[MERGING_KEY]) >= 1:
            first = random.choice(key_dict[MERGING_KEY])
        else:
            first = random.choice(tempo_dict[key])

        tempo_dict[first.tempo].remove(first)
        key_dict[first.key].remove(first)

        if key_dict.get(MERGING_KEY) and len(key_dict[MERGING_KEY]) >= 1:
            last = random.choice(key_dict[MERGING_KEY])
            tempo_dict[last.tempo].remove(last)
            key_dict[last.key].remove(last)
        else:
            last = None

        res = generate_random_playlist(first, tempo_dict, key_dict)

        if len(res) % 2:
            res.pop()
        if last:
            res = res[:-1] + [last]

        list_pieces.append([r.id for r in res])
        res_len += len(res)

    return list_pieces, res_len


def main(out_filename=RES_FILE):
    db = []
    tempo_dict = {}
    print("Reading database...")
    get_db(DATA_FILE, db, tempo_dict=tempo_dict)
    print("Getting list pieces...")
    list_pieces, res_len = get_list_pieces(tempo_dict)
    print("Merging...")
    res = merge(list_pieces, db)
    if not is_valid(res, db):
        print("Something went wrong!")
        return
    print(f"Successfully matched {len(res)}/{res_len} elements.")
    with open(out_filename, "w+") as f:
        f.write(",".join(str(r) for r in res))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
