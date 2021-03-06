# -*- coding: utf-8 -*-
""" """
import logging
import sys
from python.gilded_rose.item_classes import Item, AgedItem, Sulfuras, BackstagePass, ConjuredItem

# Set this to logging.INFO to prevent printing before/after inventory
LOGGING_LEVEL = logging.INFO

logger = logging.getLogger("gilded_rose")
logger.addHandler(logging.StreamHandler(sys.stdout))  # TODO: change to log to external file
logger.setLevel(LOGGING_LEVEL)


class GildedRose:
    """ """
    def __init__(self, items):
        self.items = items  # DO NOT TOUCH
        self.catalog = (
            Item,
            AgedItem,
            Sulfuras,
            BackstagePass,
            ConjuredItem
            # Register new product types here
        )
        # Additional properties used for sanity checks for normal Items.
        self.normal_item_min_quality = 0
        self.normal_item_max_quality = 50

    def update_quality(self) -> None:
        logger.debug(f"Items before: {self.items}")
        for item in self.items:
            try:
                # Check product type is registered in the catalog
                if item.__class__ not in self.catalog:
                    raise TypeError(f"Unknown product type for item: {item}, {item.__class__}")

                # Wrap legacy behaviour of normal Items
                if item.__class__ is Item:
                    # Sanity check Item Quality before updating
                    validate_item_quality(item, self.normal_item_min_quality, self.normal_item_max_quality)
                    update_normal_item_quality(item, self.normal_item_min_quality)

                # Use class-specific logic for all special item types
                else:
                    validate_item_quality(item, item.min_quality, item.max_quality)
                    item.update_item_quality()
            except Exception as e:
                logger.exception(f"Failed to update item at {item}. \n Exception: {e} \n")
                raise
        logger.debug(f"Items after : {self.items}")


def validate_item_quality(item: Item, min_quality: int, max_quality: int) -> None:
    """Check that item Quality is within min and max range."""
    try:
        if item.quality < min_quality:
            raise ValueError(f"Item Quality {item.quality} below minimum {min_quality},"
                             f" error in item {item}")
        if item.quality > max_quality:
            raise ValueError(f"Item Quality {item.quality} above maximum {max_quality},"
                             f" error in item {item}")
    except ValueError as e:
        logger.exception(f"Item Quality validation failed. \n Exception: {e} \n")
        raise


def update_normal_item_quality(item: Item, item_min_quality: int) -> None:
    """Handle normal item behaviour:
        - reduce Quality and SellIn days.
        - If SellIn < 0, reduce Quality twice as fast"""
    expired: bool = True if item.sell_in <= 0 else False
    new_quality: int = item.quality - 1
    if expired:
        new_quality -= 1
    # Ensure quality in never lower than minimum (default 0)
    item.quality = new_quality if not new_quality < item_min_quality else item_min_quality

    item.sell_in = item.sell_in - 1
