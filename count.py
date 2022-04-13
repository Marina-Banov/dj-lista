import os


def main():
    output_dir = "res/useful/"
    res = 0
    for filename in os.listdir(output_dir):
        # if len(filename) < len("res56.txt"):
        #    continue
        # if filename != "res1546_.txt":
        #    continue

        f = open(os.path.join(output_dir, filename))
        len_f = len(f.readline().strip().split(','))
        res += len_f
        print(filename, len_f)
    print(res)


if __name__ == "__main__":
    main()
