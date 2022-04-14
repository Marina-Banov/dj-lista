import sys
from main import get_db


def get_start_end(playlist, id_dict):
    return id_dict[int(playlist[0])], id_dict[int(playlist[-1])]


def main(out_filename="res/res.txt", in_filename="data/data.txt"):
    with open(out_filename) as f:
        line = f.readline().strip().split(',')
    id_dict = {}
    get_db(in_filename, [], id_dict=id_dict)
    start, end = get_start_end(line, id_dict)
    print(start)
    print(end)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
