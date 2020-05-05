import sys
import math
import numpy as np

rgb_entropy = []
r_entropy = []
g_entropy = []
b_entropy = []


def main():
    global rgb_entropy
    global r_entropy
    global g_entropy
    global b_entropy

    my_data = read_tga()
    for i in range(8):
        calc_entropy(my_data[0], my_data[1], my_data[2], i+1)

    print("Best rgb entropy: ",     print_type(rgb_entropy.index(min(rgb_entropy)) + 1))
    print("Best blue entropy: ",    print_type(b_entropy.index(min(b_entropy)) + 1))
    print("Best green entropy: ",   print_type(g_entropy.index(min(g_entropy)) + 1))
    print("Best red entropy: ",     print_type(r_entropy.index(min(r_entropy)) + 1))


def calc_entropy(data, x, y, param):
    encoded = np.zeros((y, x, 3))

    for i in range(1, y + 1):
        for j in range(1, x + 1):
            for k in range(3):
                if param == 1:
                    encoded[i - 1, j - 1, k] = (data[i][j][k] - data[i][j - 1][k]) % 256
                elif param == 2:
                    encoded[i - 1, j - 1, k] = (data[i][j][k] - data[i - 1][j][k]) % 256
                elif param == 3:
                    encoded[i - 1, j - 1, k] = (data[i][j][k] - data[i - 1][j - 1][k]) % 256
                elif param == 4:
                    encoded[i - 1, j - 1, k] = (data[i][j][k] - (
                            data[i][j - 1][k] + data[i - 1][j][k] - data[i - 1][j - 1][k])) % 256
                elif param == 5:
                    encoded[i - 1, j - 1, k] = (data[i][j][k] - (
                            data[i - 1][j][k] + (data[i][j - 1][k] - data[i - 1][j - 1][k]) // 2)) % 256
                elif param == 6:
                    encoded[i - 1, j - 1, k] = (data[i][j][k] - (
                            data[i][j - 1][k] + (data[i - 1][j][k] - data[i - 1][j - 1][k]) // 2)) % 256
                elif param == 7:
                    encoded[i - 1, j - 1, k] = (data[i][j][k] - (
                            data[i][j - 1][k] + data[i - 1][j][k]) // 2) % 256
                elif param == 8:
                    if data[i - 1][j - 1][k] >= max(data[i][j - 1][k], data[i - 1][j][k]):
                        encoded[i - 1, j - 1, k] = (data[i][j][k] - max(data[i][j - 1][k],
                                                                        data[i - 1][j][k])) % 256
                    elif data[i - 1][j - 1][k] <= min(data[i][j - 1][k], data[i - 1][j][k]):
                        encoded[i - 1, j - 1, k] = (data[i][j][k] - min(data[i][j - 1][k],
                                                                        data[i - 1][j][k])) % 256
                    else:
                        encoded[i - 1, j - 1, k] = (data[i][j][k] - (
                                data[i][j - 1][k] + data[i - 1][j][k] - data[i - 1][j - 1][k])) % 256

    print_entropy(encoded, param)


def print_entropy(image, param):
    r_used_bytes = []
    r_occurrences = []
    r_probability = []

    g_used_bytes = []
    g_occurrences = []
    g_probability = []

    b_used_bytes = []
    b_occurrences = []
    b_probability = []

    all_used_bytes = []
    all_occurrences = []
    all_probability = []

    print(print_type(param))

    for i in range(len(image)):
        for j in range(len(image[0])):
            for k in range(3):
                if k == 0:
                    actualize(b_used_bytes, b_occurrences, image, i, j, k)
                elif k == 1:
                    actualize(g_used_bytes, g_occurrences, image, i, j, k)
                else:
                    actualize(r_used_bytes, r_occurrences, image, i, j, k)

                actualize(all_used_bytes, all_occurrences, image, i, j, k)

    how_many = sum(b_occurrences)

    print_stats(all_occurrences, all_probability, 3 * how_many, 0, param)
    print_stats(r_occurrences, r_probability, how_many, 1, param)
    print_stats(g_occurrences, g_probability, how_many, 2, param)
    print_stats(b_occurrences, b_probability, how_many, 3, param)


def print_stats(occurrences, probability, x, what, switch):
    global rgb_entropy
    global r_entropy
    global g_entropy
    global b_entropy

    entropy = 0
    for i in occurrences:
        probability.append(i / x)
    for num in probability:
        entropy += num * (-math.log(num, 2))
    if switch != 0:
        if what == 0:
            rgb_entropy.append(entropy)
        elif what == 1:
            r_entropy.append(entropy)
        elif what == 2:
            g_entropy.append(entropy)
        elif what == 3:
            b_entropy.append(entropy)

    if what == 0:
        print("Rgb entropy: ", entropy)
    elif what == 1:
        print("Red entropy: ", entropy)
    elif what == 2:
        print("Green entropy: ", entropy)
    elif what == 3:
        print("Blue entropy: ", entropy)


def actualize(used_bytes, occurrences, base_image, a, b, c):
    try:
        index = used_bytes.index(base_image[a][b][c])
        occurrences[index] += 1
    except ValueError:
        used_bytes.append(base_image[a][b][c])
        occurrences.append(0)
        index = used_bytes.index(base_image[a][b][c])
        occurrences[index] += 1


def read_tga():
    data = []

    file = open(sys.argv[1], "rb")
    file.read(12)

    x = int.from_bytes(file.read(2), byteorder='little')
    y = int.from_bytes(file.read(2), byteorder='little')
    file.read(2)

    for i in range(y + 1):
        row = []
        for j in range(x + 1):
            if i == 256:
                row.append([0, 0, 0])
            else:
                if j == 0:
                    row.append([0, 0, 0])
                else:
                    row.append(
                        [int.from_bytes(file.read(1), byteorder='little'),
                         int.from_bytes(file.read(1), byteorder='little'),
                         int.from_bytes(file.read(1), byteorder='little')])

        data.append(row)
    data.reverse()

    base_image = []
    for i in range(y):
        base_image.append(data[i + 1][1:])

    print_entropy(base_image, 0)
    return [data, x, y]


def print_type(param):
    if param == 0:
        return "Base image"
    elif param == 1:
        return "Predictor = W"
    elif param == 2:
        return "Predictor = N"
    elif param == 3:
        return "Predictor = NW"
    elif param == 4:
        return "Predictor = N + W − NW"
    elif param == 5:
        return "Predictor =  N + (W − NW)/2"
    elif param == 6:
        return "Predictor = W + (N − NW)/2"
    elif param == 7:
        return "Predictor = (N + W)/2"
    elif param == 8:
        return "Predictor = New Standard"


main()
