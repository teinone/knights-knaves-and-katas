# -*- coding: utf-8 -*-
""" """
from __future__ import print_function

from python.GildedRose.gilded_rose import *

if __name__ == "__main__":
    print ("OMGHAI!", flush=True)
    items = [
            Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
            AgedItem(name="Aged Brie", sell_in=2, quality=0),
            Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
            # Sulfuras(name="Sulfuras, Hand of Ragnaros", sell_in=None, quality=80),
            Sulfuras(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Sulfuras(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
            BackstagePass(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
            BackstagePass(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
            BackstagePass(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
            ConjuredItem(name="Conjured Mana Cake", sell_in=3, quality=6),  # <-- :O
            ]

    days = 30
    import sys
    if len(sys.argv) > 1:
        days = int(sys.argv[1]) + 1
    for day in range(days):
        print("-------- day %s --------" % day, flush=True)
        print("name, sellIn, quality", flush=True)
        for item in items:
            print(item, flush=True)
        print("", flush=True)
        GildedRose(items).update_quality()
