try:
    from onitama.connect.card import LI
except:
    from card import LI
from matplotlib import pyplot as plt
import matplotlib.image as img
import numpy
import os


try:
    os.mkdir(r'C:\Users\吕\Desktop\supergame\static\onitama\card')
except:
    pass

plt.rcParams['font.sans-serif'] = ['KaiTi']

for card in LI:
    print(card.name)
    fig = plt.figure(figsize=(5, 5))
    # plt.title(card.name)

    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=1, wspace=1)
    # # plt.margins(0, 0)

    plt.axis([0.3, 5.7, 0.3, 5.7])
    plt.axis('off')

    bgimg = img.imread(r'C:\Users\吕\Desktop\supergame\static\onitama\other\yangpi.jpg')
    plt.figimage(bgimg)

    tick = numpy.asarray((0, 1, 2, 3, 4, 5)) + 0.5
    plt.xticks(tick, [])
    plt.yticks(tick, [])
    for _ in tick:
        plt.plot(tick, numpy.ones_like(tick)*_, c='black')
        plt.plot(numpy.ones_like(tick)*_, tick, c='black')

    old = numpy.asarray((3, 3))
    new = numpy.asarray(card.method) + old
    plt.scatter(new[:, 0], new[:, 1], c='black', s=2400, marker='*')
    plt.scatter(old[0], old[1], c=card.seq, s=1800, marker='o')

    plt.text(3, 3, s=card.name, c=card.seq, size=150, alpha=0.3,
             va="center", ha="center")

    # plt.savefig(r'C:\Users\吕\Desktop\supergame\static\onitama\card\%s.jpg' % card.name)
    plt.show()
    break
