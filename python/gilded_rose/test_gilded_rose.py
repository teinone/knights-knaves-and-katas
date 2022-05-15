# -*- coding: utf-8 -*-
""" """
import logging
import sys
import unittest
from python.gilded_rose.gilded_rose import GildedRose, Item, AgedItem, Sulfuras, BackstagePass, ConjuredItem, \
    validate_item_quality, LOGGING_LEVEL

logger = logging.getLogger("test_gilded_rose")
logger.addHandler(logging.StreamHandler(sys.stdout))  # TODO: change to log to external file
logger.setLevel(LOGGING_LEVEL)  # Set in gilded_rose.py

LINESEP1 = "\n=======================================================================\n"
LINESEP2 = "\n-----------------------------------------------------------------------"

MAXQ: int = GildedRose([]).normal_item_max_quality
MINQ: int = GildedRose([]).normal_item_min_quality

logger.info(f"Running tests, using Max Quality: {MAXQ}, Min Quality {MINQ}")


class GildedRoseTest(unittest.TestCase):

    def test_normal_item(self):
        logger.debug(f"{LINESEP1}TEST: Normal Item behaviour 1 day {LINESEP2}")
        items = [Item("Boring Boar", 10, 5)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Boring Boar, 9, 4",
                         msg="Normal decrementation not OK")
        logger.debug("PASS: Normal Item 1 day")

    def test_normal_item_expired(self):
        logger.debug(f"{LINESEP1}TEST: Expired Item behaviour 1 day {LINESEP2}")
        items = [Item("Expired Excuse", -2, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Expired Excuse, -3, 8",
                         msg="Normal item expiry decrementation not OK")
        logger.debug("PASS: Expired Item 1 day")

    def test_normal_item_zero(self):
        logger.debug(f"{LINESEP1}TEST: Item behaviour when value is 0 {LINESEP2}")
        items = [Item("Zero-value Zealot", 4, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Zero-value Zealot, 3, 0",
                         msg="Normal item decrementation doesn't stop at zero")
        logger.debug("PASS: Item behaviour when value is 0")

    def test_normal_item_zero_expired(self):
        logger.debug(f"{LINESEP1}TEST: Expired Item behaviour when value is 0 {LINESEP2}")
        items = [Item("Expired Zero-value Zealot", -2, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Expired Zero-value Zealot, -3, 0",
                         msg="Normal item decrementation doesn't stop at zero")
        logger.debug("PASS: Expired Item behaviour when value is 0")

    def test_normal_item_quality_too_high(self):
        logger.debug(f"{LINESEP1}TEST: Item Quality above maximum raises ValueError in validation {LINESEP2}")
        items = [Item("Overqualified Onager", 10, MAXQ+2)]
        gilded_rose = GildedRose(items)
        self.assertRaises(ValueError, validate_item_quality,
                          *(items[0], gilded_rose.normal_item_min_quality, gilded_rose.normal_item_max_quality))
        logger.debug("PASS: Item Quality above maximum raises ValueError")

    def test_normal_item_quality_too_low(self):
        logger.debug(f"{LINESEP1}TEST: Item Quality below minimum raises ValueError in validation {LINESEP2}")
        items = [Item("Negative Naga", 5, MINQ-5)]
        gilded_rose = GildedRose(items)
        self.assertRaises(ValueError, validate_item_quality,
                          *(items[0], gilded_rose.normal_item_min_quality, gilded_rose.normal_item_max_quality))
        logger.debug("PASS: Item Quality below minimum raises ValueError")

    def test_aged_item(self):
        """Aged items actually increases in Quality the older it gets."""
        logger.debug(f"{LINESEP1}TEST: AgedItem Quality increases with age, but doesn't exceed maximum {LINESEP2}")
        items = [AgedItem("Bombastic Brie", 10, 8),
                 AgedItem("Overripe Bombastic Brie", -2, MAXQ-2),
                 AgedItem("Ripe Bombastic Brie", 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Bombastic Brie, 9, 9",
                         msg="Aged item incrementation not OK")
        self.assertEqual(str(items[1]), f"Overripe Bombastic Brie, -3, {MAXQ-1}",
                         msg="Aged item incrementation not OK when expired")
        self.assertEqual(str(items[2]), "Ripe Bombastic Brie, 0, 11",
                         msg="Aged item incrementation not OK when near expiry")
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Bombastic Brie, 7, 11",
                         msg="Aged item incrementation not OK on third update")
        self.assertEqual(str(items[1]), f"Overripe Bombastic Brie, -5, {MAXQ}",
                         msg="Aged item incrementation not OK when expired and near maximum")
        self.assertEqual(str(items[2]), "Ripe Bombastic Brie, -2, 13",
                         msg="Aged item incrementation not OK when expired on third update")
        logger.debug("PASS: AgedItem Quality tests")

    def test_quality_too_high_for_multiple_classes(self):
        """Check that qualities over the defined maximum raise a ValueError in validate_item_quality.
        Sulfuras validates the quality in the Sulfuras constructor."""
        logger.debug(f"{LINESEP1}TEST: Special items fail validation when Quality over maximum {LINESEP2}")
        items = [
                 AgedItem("Overrated Romano", 10, MAXQ+40),
                 BackstagePass("Meet the Gremlins Weekend Pass", 10, MAXQ+15),
                 ConjuredItem("Conjured Coveted Compote", 10, MAXQ+2),
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
                         msg="Sulfuras not handled properly. Is the items list okay?")
        logger.debug("PASS: Special items fail validation when Quality over maximum")

    def test_quality_too_low_for_special_classes(self):
        """Check that qualities under the defined class-level minimum raise a ValueError
         in validate_item_quality. Sulfuras validates the quality in the Sulfuras constructor,
         so it should not be added here."""
        logger.debug(f"{LINESEP1}TEST: Special items fail validation when Quality below minimum {LINESEP2}")
        items = [
                 AgedItem("Aged Milk", 10, MINQ-5),
                 BackstagePass("Meet the Mother-In-Law", 10, MINQ-4),
                 ConjuredItem("Conjured Terrible Teriyaki", 10, MINQ-52),
                 # Add new item types here
                 ]
        # gilded_rose = GildedRose(items)
        for item in items:
            self.assertRaises(ValueError, validate_item_quality, *(item, item.min_quality, item.max_quality))
        logger.debug("PASS: Special items fail validation when Quality below minimum")

    def test_backstage_pass(self):
        """Backstage passes, increases in Quality as its SellIn value approaches;
        Quality increases by 2 when there are 10 days or less and by 3
        when there are 5 days or less but Quality drops to 0 after the concert """
        logger.debug(f"{LINESEP1}TEST: BackstagePass Items handle Quality as expected {LINESEP2}")
        items = [
            BackstagePass("CavalryCon on May 30", 18, 10),
            BackstagePass("CavalryCon on May 20", 8, 10),
            BackstagePass("CavalryCon on May 15", 3, 10),
            BackstagePass("CavalryCon on May 13", 1, 10),
            BackstagePass("CavalryCon on May 12", 0, 10),
            BackstagePass("CavalryCon in the past", -2, 10),
            BackstagePass("CavalryCon Scalper Special", 1, MAXQ),
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
        self.assertEqual(str(items[6]), f"CavalryCon Scalper Special, 0, {MAXQ}",
                         msg=f"Backstage Pass Quality not OK when {MAXQ}")
        logger.debug("PASS: BackstagePass Items handle Quality as expected")

    def test_conjured_item(self):
        """Conjured items should degrade twice as fast in quality as normal items"""
        logger.debug(f"{LINESEP1}TEST: Conjured Items handle Quality as expected {LINESEP2}")
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
        logger.debug("PASS: Conjured Items handle Quality as expected")

    def test_unregistered_product(self):
        """ New Item types should be registered in the GildedRose.catalog property,
        otherwise they should raise a TypeError"""
        logger.debug(f"{LINESEP1}TEST: Unregistered Item type raises TypeError (tests class validation) {LINESEP2}")

        class CursedCurd(Item):
            """Unregistered Item type"""
            def __init__(curd, name, sell_in, quality):
                super().__init__(name, sell_in, quality)

            def __repr__(curd):
                return "%s, %s, %s" % (curd.name, curd.sell_in, curd.quality)

        items = [
            Item("Billable Bill", 5, 20),
            ConjuredItem("Expired Conjured Confetti", -5, 20),
            CursedCurd("Cursed Curd", 5, 10)
        ]
        gilded_rose = GildedRose(items)
        self.assertRaises(TypeError, gilded_rose.update_quality)
        logger.debug("PASS: Unregistered Item type raises TypeError")

    def test_empty_item(self):
        logger.debug(f"{LINESEP1}TEST: Falsey object in items raises TypeError {LINESEP2}")
        items = [
            Item("Billable Bill", 5, 20),
            ConjuredItem("Expired Conjured Confetti", -5, 20),
            None
        ]
        gilded_rose = GildedRose(items)
        self.assertRaises(TypeError, gilded_rose.update_quality)
        logger.debug("PASS: Falsey object in items raises TypeError")

    def test_10_days(self):
        logger.debug(f"{LINESEP1}TEST: Items and Special Items have the right Quality after 10 days {LINESEP2}")
        items = [Item("Boring Boar", 8, 15),
                 AgedItem("Overripe Bombastic Brie", -2, MAXQ-9),
                 BackstagePass("Meet the Gremlins on May 24", 12, 10),
                 ConjuredItem("Conjured Capybara", 5, 40),
                 Sulfuras("Common Legendary Sulfuras", None, 80)
                 ]
        gilded_rose = GildedRose(items)
        # Run 10 days
        for _i in range(10):
            gilded_rose.update_quality()
        self.assertEqual(str(items[0]), "Boring Boar, -2, 4",
                         msg="Normal item decrementation not OK at 10 days")
        self.assertEqual(str(items[1]), f"Overripe Bombastic Brie, -12, {MAXQ}",
                         msg="Aged item incrementation not OK at 10 days")
        self.assertEqual(str(items[2]), "Meet the Gremlins on May 24, 2, 31",
                         msg="Backstage pass incrementation not OK at 10 days")
        self.assertEqual(str(items[3]), "Conjured Capybara, -5, 12",
                         msg="Conjured item decrementation not OK at 10 days")
        self.assertEqual(str(items[4]), "Common Legendary Sulfuras, None, 80",
                         msg="Sulfuras not OK at 10 days")
        logger.debug("PASS: Items and Special Item OK after 10 days")


if __name__ == '__main__':
    unittest.main()
