import sys
from is_valid import is_valid
from main import get_db


def find_order(a, b, a_range, b_range, id_dict, tempo_dict, key_dict):
    for i in range(*a_range):
        song_a = id_dict[a[i]]
        for j in range(*b_range):
            song_b = id_dict[b[j]]
            if song_b in tempo_dict[song_a.tempo]:
                return i, j, True
            if song_b in key_dict[song_a.key]:
                return i, j, False
    return -1, -1


def get_range(len_arr, direction, factor):
    if direction == 1:
        return 0, min(round(factor * len_arr), 200), 1
    return len_arr-1, max(round((1-factor) * len_arr), len_arr - 200), -1


def merge(a, b, tempo_dict, key_dict, id_dict, factor=.05):
    len_a = len(a)
    len_b = len(b)

    a_range = get_range(len_a, -1, factor)
    b_range = get_range(len_b, 1, factor)
    i, j, t = find_order(a, b, a_range, b_range, id_dict, tempo_dict, key_dict)
    diff = [[i, j, len_a-1-i + j if i >= 0 else float("inf"), t]]

    b_range = get_range(len_b, -1, factor)
    i, j, t = find_order(a, b, a_range, b_range, id_dict, tempo_dict, key_dict)
    diff.append([i, j, len_a-1-i + len_b-1-j if i >= 0 else float("inf"), t])

    a_range = get_range(len_a, 1, factor)
    i, j, t = find_order(a, b, a_range, b_range, id_dict, tempo_dict, key_dict)
    diff.append([i, j, i + len_b-1-j if i >= 0 else float("inf"), t])

    b_range = get_range(len_b, 1, factor)
    i, j, t = find_order(a, b, a_range, b_range, id_dict, tempo_dict, key_dict)
    diff.append([i, j, i + j if i >= 0 else float("inf"), t])

    res = []
    for d in range(4):
        if diff[d][2] == float("inf"):
            continue
        a_ = a[:]
        b_ = b[:]

        if d > 1:
            diff[d][0] = len_a - 1 - diff[d][0]
            if len_a % 2:
                a_.pop()
                # TODO sometimes len(res) varies when changing the order of
                #  input arrays and i think it's because of this
                diff[d][0] -= 1
            a_ = a_[::-1]
        elif not diff[d][3] and len(a_) % 2:
            diff[d][0] -= 1
        if 0 < d < 3:
            b_ = b_[::-1]
            diff[d][1] = len_b - 1 - diff[d][1]
            if not diff[d][3] and len(b_) % 2:
                diff[d][1] += 1

        r = a_[:diff[d][0]+1] + b_[diff[d][1]:]
        if len(r) > len(res) and is_valid(r, id_dict):
            res = r

    print(len(res))
    return res


def main(input_f1, input_f2, output_f, data_files=["data/data.txt"]):
    db = []
    bpm_dict = {}
    key_dict = {}
    id_dict = {}
    for f in data_files:
        get_db(f, db, tempo_dict=bpm_dict, key_dict=key_dict, id_dict=id_dict)

    f1 = list(map(int, open(input_f1).readline().strip().split(',')))
    f2 = list(map(int, open(input_f2).readline().strip().split(',')))
    res = merge(f1, f2, bpm_dict, key_dict, id_dict)
    if len(res) > 0:
        with open(output_f, "w+") as f:
            f.write(",".join(str(r) for r in res))


if __name__ == "__main__":
    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Not enough params. Define two input files and one output file.")
