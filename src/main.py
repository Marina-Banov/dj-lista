import sys
import random
from song import Song


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


def fitness_fun(playlist):
    return len(playlist)


def get_db(in_filename, db, **kwargs):
    with open(in_filename) as f:
        f.readline()
        for line in f.readlines():
            s = Song(*line.strip().split(','))
            db.append(s)
            if "id_dict" in kwargs:
                kwargs["id_dict"][s.id] = s
            if "tempo_dict" in kwargs:
                if kwargs["tempo_dict"].get(s.tempo) is None:
                    kwargs["tempo_dict"][s.tempo] = [s]
                else:
                    kwargs["tempo_dict"][s.tempo].append(s)
            if "key_dict" in kwargs:
                if kwargs["key_dict"].get(s.key) is None:
                    kwargs["key_dict"][s.key] = [s]
                else:
                    kwargs["key_dict"][s.key].append(s)


def main(in_filename="../data/data.txt",
         bpm_file="../data/bpm.txt",
         out_filename="../res/bpm2.txt"):
    with open(bpm_file) as f:
        tempos = [line.strip() for line in f.readlines()]

    db = []
    get_db(in_filename, db)
    tot_len = 0
    tot_res = 0

    for t in tempos:
        key, value = t.split(": ")
        key = float(key)
        value = list(map(int, value[1:len(value)-1].split(', ')))

        key_dict = {}
        for v in range(len(value)):
            s = db[value[v]]
            value[v] = s
            if key_dict.get(s.key) is None:
                key_dict[s.key] = [s]
            else:
                key_dict[s.key].append(s)

        tempo_dict = {key: value}
        len_ = len(tempo_dict[key])
        tot_len += len_
        if len_ == 2:
            tot_res += 2
            with open(out_filename, 'a') as f:
                f.write(f"{key}: {value}\n")
            continue

        for k in key_dict.copy():
            if len(key_dict[k]) == 1:
                tempo_dict[key].remove(key_dict[k][0])
                del key_dict[k]

        if len(tempo_dict[key]) == 0:
            continue

        if len(tempo_dict[key]) == 2:
            tot_res += 2
            with open(out_filename, 'a') as f:
                f.write(f"{key}: {tempo_dict[key]}\n")
            continue

        if key_dict.get("3B") and len(key_dict["3B"]) >= 1:
            first = random.choice(key_dict["3B"])
        else:
            first = random.choice(tempo_dict[key])

        tempo_dict[first.tempo].remove(first)
        key_dict[first.key].remove(first)

        if key_dict.get("3B") and len(key_dict["3B"]) >= 1:
            last = random.choice(key_dict["3B"])
            tempo_dict[last.tempo].remove(last)
            key_dict[last.key].remove(last)
        else:
            last = None

        res = generate_random_playlist(first, tempo_dict, key_dict)

        if len(res) % 2:
            res.pop()
        if last:
            res = res[:-1] + [last]

        tot_res += len(res)
        with open(out_filename, 'a') as f:
            f.write(f"{key}: {res}\n")

    print(f"{tot_res}/{tot_len}")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        main()
