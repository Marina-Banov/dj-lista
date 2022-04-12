import sys
import random
from song import Song


def generate_random_playlist(first, tempo_dict, key_dict):
    tempo_dict[first.tempo].remove(first)
    key_dict[first.key].remove(first)
    playlist = [first]
    last = first
    i = 0

    while True:
        added = False
        i += 1

        if i % 2:
            if len(tempo_dict[last.tempo]) > 0:
                last = random.choice(tempo_dict[last.tempo])
                tempo_dict[last.tempo].remove(last)
                key_dict[last.key].remove(last)
                playlist.append(last)
                added = True
        elif len(key_dict[last.key]) > 0:
            last = random.choice(key_dict[last.key])
            tempo_dict[last.tempo].remove(last)
            key_dict[last.key].remove(last)
            playlist.append(last)
            added = True

        if not added:
            break

    return playlist


def fitness_fun(playlist):
    return len(playlist)


def main(in_filename="data/data.txt", out_filename="res/res.txt"):
    db = []
    tempo_dict = dict()
    key_dict = dict()

    with open(in_filename) as f:
        f.readline()
        for line in f.readlines():
            s = Song(*line.strip().split(','))
            db.append(s)
            if tempo_dict.get(s.tempo) is None:
                tempo_dict[s.tempo] = [s]
            else:
                tempo_dict[s.tempo].append(s)
            if key_dict.get(s.key) is None:
                key_dict[s.key] = [s]
            else:
                key_dict[s.key].append(s)

    with open(out_filename, "r+") as f:
        _res = f.readline().strip().split(',')
        res = generate_random_playlist(random.choice(db), tempo_dict, key_dict)
        if fitness_fun(res) > fitness_fun(_res):
            f.seek(0)
            f.truncate()
            f.write(",".join(str(r) for r in res))
            print(len(res))


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        main()
