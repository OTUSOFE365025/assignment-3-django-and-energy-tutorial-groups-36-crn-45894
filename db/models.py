import sys

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()

class Item(models.Model):
    """
    Represents an item with a UPC code, name, and price.
    """

    upc_code = models.IntegerField(default=0)
    name = models.CharField(max_length=50, default="Unknown Item Name")
    price = models.FloatField(default=0.0)

    def __str__(self):
        """
        Returns a human-readable string representation of the Item object.
        """
        return f"Product: (UPC: {self.upc_code}, Name: {self.name}, Price: ${float(self.price):.2f})"

    def get_price(self):
        """
        Returns price of an item.
        """
        return self.price
        
