# Python Debugging Utils

## Audio Debugging

## Why audio debugging, directions and tips
* The trick is to place audio breakpoints in such way that you can understand
    and recognize the sound pattern while the program runs correctly and search
    for anomalies and unpredicted patterns
* Sounds should be characteristic, immediately recognizable, short
* Both blocking and nonblocking sounds are useful
* Some information about the execution is more readily absorbed through hearing (you
    can spot way more sound patterns than textual patterns in logs in a unit of time)
* With correct set up, abnormal events are easily noticeable
* You are listening all the time, without having to pay special attention, so there's
    possibility of spotting an anomaly even without consciously looking for it (impossible
    with textual logs)
* Good for developing holistic intuitions about control structure, algorithms, systems etc.
* Overlapping sounds can represent parallel events
* Representing both relative offsets and absolute duration of events
* Harder to remember sound sequence than to look at the screen
* Possibility of using two stereo channels for communicating additional information
* Assigning different timbers to different processors
* Assuring symmetry by starting some sound and ending it only when the symmetry is achieved
    (only effective for small time frames, hearing the same sound for too long is annoying)
* Treating noise as an error function to minimize (e.g. when optimizing multiprocessor
    use, make sounds on idle processors)
* Modifying volume to pass additional information
* Using sounds to inform about achieving certain line (just like "I'm here" logs)
* Choosing appropriate sounds and point at which they play is crucial. You try to optimize
    the ease of human understanding and the volume of data the programmer can
    effortlessly absorb. Some sounds are just noise, some give precious indications.

### Resources
Surprisingly not many
* [Debugging Parallel Programs Using Sound](https://dl.acm.org/citation.cfm?id=122765) paper
* Sounds taken from [Matthew Reagan's Xcode Breakpoint Sounds](https://github.com/matthewreagan/Xcode-Breakpoint-Sounds)
* [Sound Debugging](https://qnoid.com/2013/06/08/Sound-Debugging.html) blog post

## Index visualizations
Since they rely on unix-style color coding, they don't work on Windows (unless
 in PyCharm, cygwin and such).
 
## Example
```python3
from debug_utils import ab, ppl, header

def binomial_max_search(xs):
    assert len(xs) != 0
    l, r = 0, len(xs)  # [l r)
    while l < r - 1:  # at least 2 elements
        mid = (l + r - 1) // 2
        ppl(xs, (l, r, mid), 'l r mid')
        if xs[mid] < xs[mid + 1]:
            l = mid + 1
            ab('click')
        else:
            r = mid + 1
            ab('pop')
    ab('bird')
    return xs[l]  # only one element left

if __name__ == '__main__':
    a = [1,2,3,4,5,10,13,14,16,15,11,10,8,6,5,4,3,2,1,0]
    header('Searching for max')
    binomial_max_search(a)
```
Code in `example.py` produces sound and this output:

![](./example.png)

## Commands
|Command name  | Description |
|---|---|
|`enable(False)`| All commands do nothing.|
|`enable(True)`| All commands activated again.|
|`ab('bird')`| Blocking audible breakpoint `bird.ogg`.|
|`nab('bird')`| Non-blocking audible breakpoint `bird.ogg`.|
|`ppl(xs, (i, j, k), 'i j k')`| Pretty print list `xs` with marked indices `i`, `j`, `k`.|
|`header('hello', n=50)`| Print header with `Hello` inside, of with `n`.|
|`benchmark(f, rounds=100)`| Run `f()` `rounds` times, every 10th print mean time and standard deviation.|

### Current list of sounds
Only some of them sound good (like `bird`, `click`, `pop`, `zip`).

|Sound Name|
|---|
|bird|
|bzzt|
|chime|
|click|
|collect|
|error|
|knock|
|pop|
|punch|
|quack|
|swish|
|zip|

## TODO
* debug priority levels
* color printing
* easier logging to different files, maybe with timestamps?
* maybe Android-like log channels?
* external analyzer for these logs, allowing you to replay and rewind them
* visualizations
* audio breakpoints based on frequencies
* non-blocking image streams
* better image stream color specification (left-right)
* consequent image stream presentations update a single file, do not create many temporary files
* image stream documentation
* remove obsolete call to `toimage`
* progressive imports, that is only import things when you first need them
* timing utils
* colorful printing
* add `import Pillow` since without it, the image generation on Windows breaks
* there should be some global object with the history of interactions, so that even if the debugged script crashes
    you can inspect this object in REPL and potentially recover data that otherwise need to be recomputed
* this object should also store history of image feeds, so that you can generate the image post-mortem
