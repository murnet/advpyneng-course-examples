
class Property:
    def __init__(self, fget=None, fset=None, fdel=None):
        print(f"{fget=} {fset=}")
        self.fget = fget
        self.fset = fset
        self.fdel = fdel

    def __set_name__(self, owner, name):
        self.attr_name = name

    def __get__(self, instance, cls=None):
        print("__get__")
        if self.fget is None:
            raise AttributeError(f"property '{self.attr_name}' has no getter")
        return self.fget(instance)

    def __set__(self, instance, value):
        print("__set__")
        if self.fset is None:
            raise AttributeError(f"property '{self.attr_name}' has no setter")
        self.fset(instance, value)



class IPAddress:
    def __init__(self, ip, mask):
        self.ip = ip
        self.mask = mask

    def _get_mask(self):
        print("get_mask")
        return self._mask

    def _set_mask(self, new_mask):
        print("set_mask")
        if not isinstance(new_mask, int):
            raise TypeError("Маска должна быть числом")
        if new_mask not in range(0, 33):
            raise ValueError("Значение маски должно быть от 0 до 32")
        self._mask = new_mask

    mask = Property(fget=_get_mask, fset=_set_mask)
