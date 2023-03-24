

class Book:
    def __init__(self, title, price, quantity):
        self.title = title
        self.price = price
        self.quantity = quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._is_number(value)
        self._price = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._is_number(value)
        self._quantity = value

    @staticmethod
    def _is_number(value):
        if not isinstance(value, (int, float)):
            raise TypeError("Значение должно быть числом")
        if value < 0:
            raise ValueError("Значение должно быть положительным")