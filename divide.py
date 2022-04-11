import sys
import random


def main(in_filename="data/data.txt", factor=10):
    with open(in_filename) as f:
        header = f.readline()
        db = [line.strip() for line in f.readlines()]
    random.shuffle(db)

    step = int(len(db) / factor)
    iteration = 0
    out_filename = in_filename.split(".txt")[0]
    for i in range(0, len(db), step):
        with open(f"{out_filename}{iteration}.txt", "w+") as f:
            f.write(header)
            f.write('\n'.join(line for line in db[i:i+step]))
        iteration += 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
