import numpy as np
import scipy
from scipy import signal


def get_median(data, filter_len):

    if filter_len % 2 == 0:
        print(" filter length is not a odd number")

    elif filter_len % 2 == 1:
        y = []
        zeros = (filter_len - 1) // 2
        for i in range(len(data)):
            window = []
            j = i + 1
            if ((j + zeros) > len(data)):
                for a in range(i + zeros - (len(data) - 1)):
                    window.append(0)
                for b in range(int(i - zeros), len(data)):
                    window.append(data[b])

            elif j + zeros < filter_len:
                window = [0] * (zeros - j + 1)
                for j in range((filter_len - (zeros - j + 1))):
                    window.append(data[j])
            else:
                for c in range(filter_len):
                    window.append(data[i + c - zeros])

            print("window:", window)
            window.sort()
            print(" sorted window:", window)

            y.append(window[zeros])
        print("y:", y)
        return window, y

    else:
        print("filter length is not a odd number")


data = [2, 3, 9, 12, 6, 28, 20]
filter_len = 5
get_median(data, filter_len)

y2 = scipy.signal.medfilt(data, 5)
print("y2:", y2)
