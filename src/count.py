import os


def main():
    output_dir = "res/"
    res = 0
    for filename in os.listdir(output_dir):
        if filename != "res.txt":
            continue

        with open(os.path.join(output_dir, filename)) as f:
            len_f = len(f.readline().strip().split(','))
        res += len_f
        print(filename, len_f)
    print(res)


if __name__ == "__main__":
    main()
