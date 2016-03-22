from collections import OrderedDict, defaultdict


class OrderedDefaultDict(OrderedDict, defaultdict):
    def __init__(self, default_factory=None, **kwargs):
        super(OrderedDefaultDict, self).__init__(**kwargs)
        self.default_factory = default_factory

class DateRangeCache(list):
    def __init__(self, calculator):
        self.calculate = calculator

    def __getitem__(self, date):
        ret = []
        for start, end in self:
            if start <= date <= end:
                ret.append((start, end))
        if not ret:
            ret = self.calculate(date)
            self.extend(ret)
        return sorted(ret, reverse=True)

    get = __getitem__