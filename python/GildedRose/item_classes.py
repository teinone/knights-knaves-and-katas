""" """
import abc
from typing import Union


# Legacy superclass, do not touch under risk of mortal danger
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class AbstractItem(Item, abc.ABC):
    """
    Abstract Base Class for all special Items.
    Since each item type has its own quality evolution pattern, we create an abstract
    superclass for all items. This class provides the interface for all new subclasses
    without tampering with the Item class, while inheriting the properties of the legacy
    Item class. The default properties of this class can be overriden in any subclass.
    """

    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)
        self.max_quality: int = 50
        self.min_quality: int = 0

    @abc.abstractmethod
    def update_item_quality(self):
        """Note: this method should also implement the sell_by decrementation where applicable."""
        pass


class Sulfuras(AbstractItem):
    """Sulfuras is a legendary item and as such its Quality is 80 and it never
    alters and never has to be sold"""
    def __init__(self, name: str, sell_in: Union[None, int] = None, quality: int = 80):
        super().__init__(name, sell_in, quality)
        if quality != 80:
            raise ValueError(f"The Quality for Sulfuras should always be 80, got {quality}!")
        self.max_quality: int = 80
        self.min_quality: int = 80

    def update_item_quality(self):
        pass


class AgedItem(AbstractItem):
    """Aged Items actually increases in Quality the older they get"""
    def update_item_quality(self):
        if self.quality < self.max_quality:
            self.quality += 1

        self.sell_in -= 1


class BackstagePass(AbstractItem):
    """Backstage passes, increases in Quality as its SellIn value approaches;
        Quality increases by 2 when there are 10 days or less and by 3
        when there are 5 days or less but Quality drops to 0 after the concert """
    def update_item_quality(self):
        if self.sell_in <= 0:
            self.quality = 0
        else:
            new_quality: int = self.quality + 1
            if self.sell_in <= 10:
                new_quality += 1
            if self.sell_in <= 5:
                new_quality += 1
            # Ensure quality in never above maximum (default 50)
            self.quality = new_quality if not new_quality > self.max_quality else self.max_quality

        self.sell_in -= 1


class ConjuredItem(AbstractItem):
    """Conjured items degrade in Quality twice as fast as normal Items"""
    def update_item_quality(self):
        expired: bool = True if self.sell_in < 0 else False
        new_quality: int = self.quality - 2
        if expired:
            new_quality -= 2
        # Ensure quality in never lower than minimum (default 0)
        self.quality = new_quality if not new_quality < self.min_quality else self.min_quality

        self.sell_in = self.sell_in - 1
