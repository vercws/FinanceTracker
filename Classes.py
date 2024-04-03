#Classes that are used in the main app window to store expenses and credits

class Expense:
    def __init__(self, amount, category):
        self.amount = amount
        self.category = category

    def to_dict(self):
        return {'amount': self.amount, 'category': self.category}

    @classmethod
    def from_dict(cls, data):
        return cls(data['amount'], data['category'])

    def __str__(self):
        return f'{self.amount:.2f} ({self.category})'


class Credit:
    def __init__(self, amount, category):
        self.amount = amount
        self.category = category

    def to_dict(self):
        return {'amount': self.amount, 'category': self.category}

    @classmethod
    def from_dict(cls, data):
        return cls(data['amount'], data['category'])

    def __str__(self):
        return f'{self.amount:.2f} ({self.category})'
