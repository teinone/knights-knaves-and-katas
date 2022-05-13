# -*- coding: utf-8 -*-
import unittest

from gilded_rose import GildedRose, Item, AgedItem, Sulfuras, BackstagePass, ConjuredItem, validate_item_quality


class GildedRoseTest(unittest.TestCase):

    def test_normal_item(self):
        items = [Item("Boring Boar", 10, 5)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Boring Boar, 9, 4",
                         msg="Normal decrementation not OK")

    def test_normal_item_expired(self):
        items = [Item("Expired Excuse", -2, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Expired Excuse, -3, 8",
                         msg="Normal item expiry decrementation not OK")

    def test_normal_item_zero(self):
        items = [Item("Zero-value Zealot", 4, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Zero-value Zealot, 3, 0",
                         msg="Normal item decrementation doesn't stop at zero")

    def test_normal_item_zero_expired(self):
        items = [Item("Expired Zero-value Zealot", -2, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Expired Zero-value Zealot, -3, 0",
                         msg="Normal item decrementation doesn't stop at zero")

    def test_normal_item_quality_too_high(self):
        items = [Item("Overqualified Onager", 10, 52)]
        gilded_rose = GildedRose(items)
        self.assertRaises(ValueError, validate_item_quality,
                          *(items[0], gilded_rose.normal_item_min_quality, gilded_rose.normal_item_max_quality))

    def test_normal_item_quality_too_low(self):
        items = [Item("Negative Naga", 5, -5)]
        gilded_rose = GildedRose(items)
        self.assertRaises(ValueError, validate_item_quality,
                          *(items[0], gilded_rose.normal_item_min_quality, gilded_rose.normal_item_max_quality))

    def test_aged_item(self):
        """Aged items actually increases in Quality the older it gets."""
        items = [AgedItem("Bombastic Brie", 10, 8),
                 AgedItem("Overripe Bombastic Brie", -2, 48),
                 AgedItem("Ripe Bombastic Brie", 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Bombastic Brie, 9, 9",
                         msg="Aged item incrementation not OK")
        self.assertEqual(str(items[1]), "Overripe Bombastic Brie, -3, 49",
                         msg="Aged item incrementation not OK when expired")
        self.assertEqual(str(items[2]), "Ripe Bombastic Brie, 0, 11",
                         msg="Aged item incrementation not OK when near expiry")
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Bombastic Brie, 7, 11",
                         msg="Aged item incrementation not OK on third update")
        self.assertEqual(str(items[1]), "Overripe Bombastic Brie, -5, 50",
                         msg="Aged item incrementation not OK when expired and near 50")
        self.assertEqual(str(items[2]), "Ripe Bombastic Brie, -2, 13",
                         msg="Aged item incrementation not OK when expired on third update")

    def test_quality_too_high_for_multiple_classes(self):
        """Check that qualities over the defined maximum raise a ValueError in validate_item_quality.
        Sulfuras validates the quality in the Sulfuras constructor."""

        items = [
                 AgedItem("Overrated Romano", 10, 90),
                 BackstagePass("Meet the Gremlins Weekend Pass", 10, 65),
                 ConjuredItem("Conjured Coveted Compote", 10, 52),
                 Sulfuras("Common Legendary Sulfuras", None, 80),  # NOTE POSITION IN LIST
                 # Add new item types here
                 ]
        gilded_rose = GildedRose(items)
        # Check general max quality (from gilded_rose)
        for item in items:
            self.assertRaises(ValueError, validate_item_quality,
                              *(item, gilded_rose.normal_item_min_quality, gilded_rose.normal_item_max_quality))

        # Check products with product-specific min and max qualities, i.e. Sulfuras
        self.assertRaises(ValueError, Sulfuras, *("Excessively Legendary Sulfuras", None, 84))
        self.assertEqual(str(items[-1]), "Common Legendary Sulfuras, None, 80",
                         msg="Normal Sulfuras not handled properly. Is the items list okay?")

    def test_quality_too_low_for_special_classes(self):
        """Check that qualities under the defined class-level minimum raise a ValueError
         in validate_item_quality. Sulfuras validates the quality in the Sulfuras constructor,
         so it should not be added here."""

        items = [
                 AgedItem("Aged Milk", 10, -5),
                 BackstagePass("Meet the Mother-In-Law", 10, -4),
                 ConjuredItem("Conjured Terrible Teriyaki", 10, -52),
                 # Add new item types here
                 ]
        # gilded_rose = GildedRose(items)
        for item in items:
            self.assertRaises(ValueError, validate_item_quality, *(item, item.min_quality, item.max_quality))


    def test_backstage_pass(self):
        """Backstage passes, increases in Quality as its SellIn value approaches;
        Quality increases by 2 when there are 10 days or less and by 3
        when there are 5 days or less but Quality drops to 0 after the concert """
        items = [
            BackstagePass("CavalryCon on May 30", 18, 10),
            BackstagePass("CavalryCon on May 20", 8, 10),
            BackstagePass("CavalryCon on May 15", 3, 10),
            BackstagePass("CavalryCon on May 13", 1, 10),
            BackstagePass("CavalryCon on May 12", 0, 10),
            BackstagePass("CavalryCon in the past", -2, 10),
                  ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "CavalryCon on May 30, 17, 11",
                         msg="Normal backstage pass incrementation not OK")
        self.assertEqual(str(items[1]), "CavalryCon on May 20, 7, 12",
                         msg="<10 day backstage pass incrementation not OK")
        self.assertEqual(str(items[2]), "CavalryCon on May 15, 2, 13",
                         msg="<5 day backstage pass incrementation not OK")
        self.assertEqual(str(items[3]), "CavalryCon on May 13, 0, 13",
                         msg="Gig-day incrementation not okay")
        self.assertEqual(str(items[4]), "CavalryCon on May 12, -1, 0",
                         msg="Expiring backstage pass value not 0")
        self.assertEqual(str(items[5]), "CavalryCon in the past, -3, 0",
                         msg="Expired backstage pass value not 0")

    def test_conjured_item(self):
        """Conjured items should degrade twice as fast in quality as normal items"""
        items = [
            ConjuredItem("Conjured Confetti", 5, 20),
            ConjuredItem("Expired Conjured Confetti", -5, 20)
                  ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Conjured Confetti, 4, 18",
                         msg="Normal conjured item decrementation not OK")
        self.assertEqual(str(items[1]), "Expired Conjured Confetti, -6, 16",
                         msg="Expired conjured item decrementation not OK")

    def test_unregistered_product(self):
        class CursedCurd(Item):
            def __init__(curd, name, sell_in, quality):
                super().__init__(name, sell_in, quality)

            def __repr__(self):
                return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

        items = [
            Item("Billable Bill", 5, 20),
            ConjuredItem("Expired Conjured Confetti", -5, 20),
            CursedCurd("Cursed Curd", 5, 10)
        ]
        gilded_rose = GildedRose(items)
        self.assertRaises(TypeError, gilded_rose.update_quality)

    def test_empty_item(self):
        items = [
            Item("Billable Bill", 5, 20),
            ConjuredItem("Expired Conjured Confetti", -5, 20),
            None
        ]
        gilded_rose = GildedRose(items)
        self.assertRaises(TypeError, gilded_rose.update_quality)

    def test_10_days(self):
        items = [Item("Boring Boar", 8, 15),
                 AgedItem("Overripe Bombastic Brie", -2, 41),
                 BackstagePass("Meet the Gremlins on May 24", 12, 10),
                 ConjuredItem("Conjured Capybara", 5, 40),
                 Sulfuras("Common Legendary Sulfuras", None, 80)
                 ]
        gilded_rose = GildedRose(items)
        # Run 10 days
        for i in range(10):
            gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Boring Boar, -2, 4",
                         msg="Normal item decrementation not OK at 10 days")
        self.assertEqual(str(items[1]), "Overripe Bombastic Brie, -12, 50",
                         msg="Aged item incrementation not OK at 10 days")
        self.assertEqual(str(items[2]), "Meet the Gremlins on May 24, 2, 31",
                         msg="Backstage pass incrementation not OK at 10 days")
        self.assertEqual(str(items[3]), "Conjured Capybara, -5, 12",
                         msg="Conjured item decrementation not OK at 10 days")
        self.assertEqual(str(items[4]), "Common Legendary Sulfuras, None, 80",
                         msg="Sulfuras not OK at 10 days")

if __name__ == '__main__':
    unittest.main()
