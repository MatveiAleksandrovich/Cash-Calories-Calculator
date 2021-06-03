import datetime as dt


class Record:

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()
        else:
            self.date = dt.date.today()


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        now = dt.date.today()
        return sum(
            record.amount
            for record in self.records
            if record.date == now
        )

    def get_week_stats(self):
        now = dt.date.today()
        week = now - dt.timedelta(days=7)
        return sum(
            record.amount for record in self.records
            if week < record.date <= now
        )


class CashCalculator(Calculator):

    USD_RATE = 60.00
    EURO_RATE = 70.00
    CURRENCIES = {
        'rub': [1.00, 'руб'],
        'usd': [USD_RATE, 'USD'],
        'eur': [EURO_RATE, 'Euro']
    }
    NO_MONEY = 'Денег нет, держись'
    DEBT = 'Денег нет, держись: твой долг - {balance} {name}'
    MONEY_LEFT = 'На сегодня осталось {balance} {name}'

    def get_today_cash_remained(self, currency):
        status_today = self.get_today_stats()
        if status_today == self.limit:
            return self.NO_MONEY
        name = self.CURRENCIES[currency][1]
        cash_left = round(
            (self.limit - status_today) /
            self.CURRENCIES[currency][0],
            2
        )
        money = abs(cash_left)
        if cash_left < 0:
            return (
                self.DEBT.format(balance=money, name=name)
            )
        return (
                self.MONEY_LEFT.format(balance=money, name=name)
            )


class CaloriesCalculator(Calculator):

    CALORIES_ANSWER = (
        'Сегодня можно съесть что-нибудь ещё, но'
        ' с общей калорийностью не более {calories} кКал'
    )
    CALORIES_ANSWER_STOP_EATING = (
        'Хватит есть!'
    )

    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained > 0:
            return self.CALORIES_ANSWER.format(calories=calories_remained)
        return self.CALORIES_ANSWER_STOP_EATING


if __name__ == '__main__':
    r1 = Record(amount=145, comment="Безудержный шопинг", date="08.03.2020")
    r2 = Record(
        amount=1568, comment="Наполнение потребительской корзины",
        date="09.03.2020"
    )
    r3 = Record(amount=691, comment="Катание на такси", date="08.03.2020")
    r4 = Record(
        amount=1186, comment="Кусок тортика. И ещё один.",
        date="24.02.2020"
    )
    r5 = Record(amount=804, comment="Йогурт.", date="23.02.2020")
    r6 = Record(amount=1140, comment="Баночка чипсов.", date="24.02.2020")
    cash_calculator = CashCalculator(0)
    cash_calculator.add_record(Record(amount=145, comment="кофе"))
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    cash_calculator.add_record(Record(
        amount=3000, comment="бар в Танин др", date="08.11.2020"
    ))
    print(cash_calculator.get_today_cash_remained("rub"))
    calories_calculator = CaloriesCalculator(1100)
    calories_calculator.add_record(Record(amount=600, comment="кофе"))
    calories_calculator.add_record(Record(amount=200, comment="обед"))
    calories_calculator.add_record(Record(
        amount=350, comment="бар", date="18.11.2020"
    ))
    print(calories_calculator.get_calories_remained())
    cash_calculator = CashCalculator(50)
    cash_calculator.add_record(Record(amount=100, comment="еда"))
    cash_calculator.add_record(Record(amount=30, comment="Заправка"))
    print(cash_calculator.get_today_cash_remained("usd"))
