from threading import Thread
import sys
import time
import statistics

stdout, sys.stdout = sys.stdout, None
import pygame
sys.stdout = stdout

def ab(name: str) -> None:  # audio breakpoint
    pygame.mixer.init()
    pygame.mixer.Sound('sounds/{}.ogg'.format(name)).play()
    while pygame.mixer.get_busy():
        time.sleep(0.001)

def nab(name: str) -> None:  # non-blocking audio breakpoint
    class NB(Thread):
        def run(self):
            ab(name)
    NB().start()

def benchmark(f, rounds=100):
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


if __name__ == '__main__':
    pass
