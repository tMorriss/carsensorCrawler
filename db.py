
from datetime import date
from mysql import connector

DATE_FORMAT = '%Y-%m-%d'


class CarData:
    def __init__(self, date: date, name: str, price: int, model_year: int, mileage: int) -> None:
        self.date = date
        self.name = name
        self.price = price
        self.model_year = model_year
        self.mileage = mileage


class DBConnector:
    def __init__(self, host: str, user: str, pw: str, name: str) -> None:
        # sql接続
        self.con = connector.connect(
            host=host, port=3306, user=user, password=pw, database=name)

    def disconnect(self) -> None:
        self.con.close()

    def initialze(self) -> None:
        self.cur = self.con.cursor()
        self.con.autocommit = False

    def add(self, data: list[CarData]) -> None:
        values: list[CarData] = []
        for d in data:
            values.append('("{}", "{}", "{}", "{}", "{}")'.format(d.date.strftime(DATE_FORMAT), d.name, d.price, d.model_year, d.mileage))
        sql = 'INSERT INTO log (date, name, price, year, mileage) VALUES' + ','.join(values)
        self.cur.execute(sql)

    def delete(self, date: date) -> None:
        sql = 'DELETE FROM log WHERE date="{}"'.format(date.strftime(DATE_FORMAT))
        self.cur.execute(sql)

    def commit(self) -> None:
        self.cur.close()
        self.con.commit()

    def rollback(self) -> None:
        self.con.rollback()
