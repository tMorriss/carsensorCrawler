import os
import yaml

from datetime import date

import db_secrets as secrets
from db import DBConnector
from crawler import crawling, CarData

car_list_file = os.path.dirname(__file__) + '/carList.yaml'

if __name__ == '__main__':
    today = date.today()

    with open(car_list_file, 'r') as yml:
        cars: list[dict[str, str]] = yaml.safe_load(yml)['list']

    try:
        data: list[CarData] = crawling(cars=cars)

        db = DBConnector(secrets.DB_HOST, secrets.DB_USER, secrets.DB_PASS, secrets.DB_NAME)
        db.initialze()
        db.delete(today)
        for d in data:
            db.add(date=today, name=d.name, price=d.price, model_year=d.model_year, mileage=d.mileage)

        db.commit()
    except Exception:
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.disconnect()
