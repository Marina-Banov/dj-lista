import sys
from main import get_db


def is_valid(playlist, id_dict):
    for i in range(len(playlist)-1):
        if i % 2 == 0:
            if id_dict[playlist[i]].tempo != id_dict[playlist[i+1]].tempo:
                print(i)
                return False
        elif id_dict[playlist[i]].key != id_dict[playlist[i+1]].key:
            print(i)
            return False

    return True


def main(res_file="res/res.txt", input_files=["data/data.txt"]):
    res = list(map(int, open(res_file).readline().strip().split(',')))
    id_dict = {}
    for f in input_files:
        get_db(f, [], id_dict=id_dict)
    print(is_valid(res, id_dict))


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2:])
    else:
        main()
