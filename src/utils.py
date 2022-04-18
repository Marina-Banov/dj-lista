import os
from data_class import Song

DATA_FILE = "../data/data.txt"


def count(playlist=None):
    if playlist:
        return len(playlist)

    input_dir = input("Please provide file or folder you want to count: ")
    try:
        if len(os.listdir(input_dir)) > 1:
            exceptions = input("Any exceptions (separate multiple files "
                               "with space, press Enter if None)? ")
            exceptions = exceptions.split(" ")
        else:
            exceptions = []
    except NotADirectoryError:
        with open(input_dir) as f:
            return len(f.readline().strip().split(","))

    res = 0
    for filename in os.listdir(input_dir):
        if filename in exceptions:
            continue

        with open(os.path.join(input_dir, filename)) as f:
            len_f = len(f.readline().strip().split(','))
        res += len_f
        print(filename, len_f)

    return res


def get_db(db_file, db, **kwargs):
    with open(db_file) as f:
        f.readline()  # header
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


def is_valid(playlist=None, db=None):
    if not playlist:
        playlist_file = input("Which file would you like to test? ")
        with open(playlist_file) as f:
            playlist = list(map(int, f.readline().strip().split(',')))

    if len(playlist) != len(set(playlist)):
        return False

    if not db:
        db = []
        get_db(DATA_FILE, db)

    for i in range(len(playlist)-1):
        if i % 2 == 0:
            if db[playlist[i]].tempo != db[playlist[i+1]].tempo:
                print(i)
                return False
        elif db[playlist[i]].key != db[playlist[i+1]].key:
            print(i)
            return False

    return True


def reverse(playlist=None, to_file=True):
    if not playlist:
        in_file = input("Please provide the file you would like to reverse: ")
        with open(in_file) as f:
            playlist = f.readline().strip().split(",")
    if to_file:
        to_file = input("Please provide output file for reverse playlist: ")
        with open(to_file, "w+") as f:
            f.write(",".join(r for r in playlist[::-1]))
    else:
        return playlist[::-1]


def main():
    mode = 0
    input_string = """\n   1 - count
       2 - is_valid
       3 - reverse
       Choose the script you want to run: """

    fun = [count, is_valid, reverse]

    while mode not in list(range(1, len(fun) + 1)):
        try:
            mode = int(input(input_string.replace("\n    ", "\n")))
        except Exception:
            continue
    print()

    res = fun[mode-1]()
    if res:
        print(res)


if __name__ == "__main__":
    main()
