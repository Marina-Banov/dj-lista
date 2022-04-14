import sys
from main import get_db


def main(out_filename, in_filename="data/data.txt"):
    db = []
    tempo_dict = {}
    get_db(in_filename, db, tempo_dict=tempo_dict)

    with open(out_filename, "w+") as f:
        for key, values in tempo_dict.items():
            if len(values) == 1:
                continue

            if len(values) < 200:
                f.write(f"{key}: {values}\n")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[0])
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Not enough params. Define an output file.")
