import sys
from main import get_db


def main(in_filename="data/data.txt", out_filename="res/res.txt"):
    with open(out_filename) as f:
        line = f.readline().strip().split(',')
        a, b = line[0], line[-1]
    id_dict = {}
    get_db(in_filename, [], id_dict=id_dict)
    print(id_dict[int(a)])
    print(id_dict[int(b)])


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        main()