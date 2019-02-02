from threading import Thread
import sys
import time
import statistics
import numpy as np
import scipy.misc as smp

stdout, sys.stdout = sys.stdout, None
import pygame
pygame.mixer.init()
sys.stdout = stdout

__run = True

def enable(should_run: bool) -> None:
    global __run
    __run = should_run

def ab(name: str) -> None:  # audio breakpoint
    if not __run: return
    pygame.mixer.Sound('sounds/{}.ogg'.format(name)).play()
    while pygame.mixer.get_busy():
        time.sleep(0.001)

def nab(name: str) -> None:  # non-blocking audio breakpoint
    if not __run: return
    class NB(Thread):
        def run(self):
            ab(name)
    NB().start()

def benchmark(f, rounds=100):
    if not __run: return

    times = []
    stdout = sys.stdout
    for i in range(rounds):
        start_time = time.time()
        sys.stdout = None
        f()
        sys.stdout = stdout
        seconds = time.time() - start_time
        times.append(seconds)
        mean = statistics.mean(times)
        if (i + 1) % 10 == 0:
            print('{} {:3.2f} {:3.2f}'. format(i + 1, mean, statistics.stdev(times, mean)))

def ppl(xs, indices, str_labels):  # pretty print list
    if not __run: return

    labels = str_labels.split(' ')
    assert len(indices) == len(labels)
    assert len(set(labels)) == len(labels)

    def colorful(s, label=None):
        colors = list(range(31, 38)) + list(range(90, 97))
        if label is None:
            return (str(s),) * 2
        else:
            color = colors[labels.index(label)]
            return str(s), '\033[{}m{}\033[0m'.format(color, str(s))

    index_locations = {}

    middle_line = ''
    middle_line_color = ''
    for i in range(-1, len(xs) + 1):
        found = None
        for jj, j in enumerate(indices):
            if j == i:
                index_locations[i] = 0 if i == -1 else len(middle_line) + 1
                if not found: found = labels[jj]
        str_output = '(' if i == -1 else ' )' if i == len(xs) else (' ' + str(xs[i]))
        _, __ = colorful(str_output, found)
        middle_line += _
        middle_line_color += __

    top_line_chars = [' '] * len(middle_line)
    for k, v in index_locations.items():
        top_line_chars[v] = colorful('↓', labels[indices.index(k)])[1]
    top_line = ''.join(top_line_chars)

    labels_and_indices = []
    for k, v in index_locations.items():
        for ii, i in enumerate(indices):
            if i == k:
                labels_and_indices.append((labels[ii], k))
    labels_and_indices.sort(key=lambda p: p[1])
    processed_pairs = []
    for i in range(len(labels_and_indices)):
        if not processed_pairs or labels_and_indices[i][1] != processed_pairs[-1][1]:
            processed_pairs.append([labels_and_indices[i][0], labels_and_indices[i][1], labels_and_indices[i][0]])
        else:
            processed_pairs[-1][0] += '=' + labels_and_indices[i][0]
    bottom_line = ''
    for names, val, first_name in processed_pairs:
        if bottom_line != '':
            bottom_line += ' '
        first = True
        for name in names.split('='):
            if not first: bottom_line += '='
            bottom_line += colorful(name, first_name)[1]
            first = False
        bottom_line += '=' + str(val)

    print(top_line)
    print(middle_line_color)
    print(bottom_line)
    sys.stdout.flush()

def header(text, n=50):
    if not __run: return

    print('\n' + ('=' * n))
    print(str(text).center(n))
    print(('=' * n) + '\n')
    sys.stdout.flush()

def image_stream(channels=1):
    assert channels >= 1
    data = [None] * channels
    for i in range(len(data)):
        data[i] = []

    channel_size = 100

    def percent_to_pixel(p, theme):
        if theme == 'red':
            return int(255 * (1 - p)), int(255 * p), 30
        elif theme == 'strawberry':
            return int(248 * p), int(12 * p), int(58 * p)
        elif theme == 'gold' or True:
            return int(255 * p), int(191 * p), 0

    def feed(*percents):
        assert len(percents) == channels
        for i, p in enumerate(percents):
            data[i].append(p)

    def show(theme='gold'):
        img_data = np.zeros((channel_size * channels, len(data[0]), 3))
        for ch in range(channels):
            for j, p in enumerate(data[ch]):
                pixel = percent_to_pixel(p, theme)
                for i in range(ch * channel_size, (ch + 1) * channel_size):
                    img_data[i, j] = pixel
        img = smp.toimage(img_data)
        img.show()

    return feed, show
