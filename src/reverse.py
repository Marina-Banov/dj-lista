import sys


def main(out_filename, in_filename="res/res.txt"):
    with open(in_filename) as f:
        res = f.readline().strip().split(',')
    with open(out_filename, "w+") as f:
        f.write(",".join(r for r in res[::-1]))


if __name__ == "__main__":
    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 2:
        main(sys.argv[1])
    else:
        print("Please provide output file name.")
