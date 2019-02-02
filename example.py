from debug_utils import ab, ppl, header, image_stream

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

    feed, show = image_stream()
    for i in range(1000):
        feed(i / 1000 if i % 3 else 0)
    show('strawberry')
