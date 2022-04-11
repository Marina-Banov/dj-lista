import sys
from song import Song


def main(in_filename="data/data.txt"):
    db = []

    with open(in_filename) as f:
        f.readline()
        for line in f.readlines():
            db.append(Song(*line.strip().split(',')))

    print(len(db))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
