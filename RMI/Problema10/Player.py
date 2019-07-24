from __future__ import print_function
import Pyro4
from random import choice


class Player:
    def __init__(self):
        self.decks = set()

    def start(self):
        #print("Mostra Cartas :", self.cards)
        cards_get = {
            deck.name: deck.dist_cards() for deck in self.decks
        }
        while True:
            '''
            for deck, card_source in cards_get.items():
                card = next(card_source)
                print("{0}.{1}".format(deck, card))
            '''
            deck = choice(list(cards_get.keys()))
            card = next( cards_get[deck] )
            print("{0}.{1}".format(deck,card))

def find_decks():
    decks = []
    with Pyro4.locateNS() as ns:
        for deck, deck_uri in ns.list(prefix="projeto10.DeckDist.").items():
            print("found deck", deck)
            decks.append(Pyro4.Proxy(deck_uri))
    if not decks:
        raise ValueError("Buffer de baralho não encontrado, Inicio a DeckDist Primeiro")
    return decks


def main():
    player = Player()
    player.decks = find_decks()
    player.start()


if __name__ == "__main__":
    main()
