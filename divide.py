import os
import sys
import random


def main(in_filename="data/data.txt", factor=8):
    res = set()
    for filename in os.listdir("res/useful/"):
        f = open(os.path.join("res/useful/", filename))
        res.update(f.readline().strip().split(','))
    db = []
    with open(in_filename) as f:
        header = f.readline()
        for line in f.readlines():
            line = line.strip()
            if line.split(',')[0] in res:
                continue
            db.append(line)
        # db = [line.strip() for line in f.readlines()]
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
