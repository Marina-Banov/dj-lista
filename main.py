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


def main(in_filename="data/data.txt", out_filename="res/res.txt"):
    db = []
    tempo_dict = {}
    key_dict = {}
    get_db(in_filename, db, tempo_dict=tempo_dict, key_dict=key_dict)

    with open(out_filename, "r+") as f:
        _res = f.readline().strip().split(',')
        res = generate_random_playlist(random.choice(db), tempo_dict, key_dict)
        if fitness_fun(res) > fitness_fun(_res):
            f.seek(0)
            f.truncate()
            f.write(",".join(str(r.id) for r in res))
            print(len(res))


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        main()
