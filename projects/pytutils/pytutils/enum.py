from .props import lazyclassproperty


class LookupEnumMixin:
    @lazyclassproperty
    def lookup_by_name(cls):
        return cls.__members__

    @lazyclassproperty
    def lookup_by_value(cls):
        """
        This is primarily
        """
        lookup = {v.value: v for k, v in cls.__members__.items()}
        return lookup

    @lazyclassproperty
    def lookup_by_any(cls):
        lookup = dict(cls.lookup_by_name)
        lookup.update(cls.lookup_by_value)
        return lookup
