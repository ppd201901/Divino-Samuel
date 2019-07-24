from __future__ import print_function
import collections
import random
import time
import Pyro4

@Pyro4.expose
class DeckDist:

    def __init__(self, name):

        self._name = name

        Card = collections.namedtuple(name, ['rank', 'suit'])

        ranks = [ str(n) for n in range(2,11)] + list('JQKA')
        suits = 'spades diamonds clubs hearts'.split()

        self._cards = [Card(rank,suit)  for suit in suits
                                        for rank in ranks]
    def __len_(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):
        self._cards[position] = value


    def dist_cards(self):
        while True:
            random.shuffle(self._cards)
            yield random.choice(self._cards)
            time.sleep(random.random()/2.0)

    @property
    def name(self):
        return self._name

    @property
    def cards(self):
        return self._cards


if __name__ == "__main__":
    deckBlack = DeckDist("Black")
    deckRed  = DeckDist("Red")
    deckBlue = DeckDist("Blue")
    deckGreen = DeckDist("Green")

    with Pyro4.Daemon() as daemon:
        deckblack_uri = daemon.register(deckBlack)
        deckred_uri = daemon.register(deckRed)
        with Pyro4.locateNS() as ns:
            ns.register("projeto10.DeckDist.deckBlack", deckblack_uri)
            ns.register("projeto10.DeckDist.deckRed", deckred_uri)
        print("Baralho Distribuido.")
        daemon.requestLoop()
