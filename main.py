import os
import re
import requests
import yaml
from bs4 import BeautifulSoup
from datetime import date

import db_secrets as secrets
from db import DBConnector, CarData


domain = 'https://www.carsensor.net'
car_list_file = os.path.dirname(__file__) + '/carList.yaml'


def crawling(cars: list[dict[str, str]], db: DBConnector):
    today = date.today()
    car_data: list[CarData] = []
    for car in cars:
        url = domain + car['url']
        while (True):
            res = requests.get(url.replace('index.html', url))
            if (res.status_code != 200):
                break

            soup = BeautifulSoup(res.text, 'html.parser')
            res.close()

            car_list = soup.find('div', id='carList')
            for cassette_wrap in car_list.find_all('div', class_='cassetteWrap'):
                price_context = cassette_wrap.find('p', class_='basePrice__content')
                price_big_text = price_context.find('span', class_='basePrice__mainPriceNum')
                price_small_text = price_context.find('span', class_='basePrice__subPriceNum')
                price: int = -1
                if (price_big_text is not None and price_small_text is not None):
                    price = int(price_big_text.text) * 10000 + int(price_small_text.text.replace('.', '')) * 1000

                detail_data = cassette_wrap.find_all('dd', class_='specList__data')

                model_year_text = detail_data[0].find('span', class_='specList__emphasisData').text
                mileage_text = detail_data[1].find('span', class_='specList__emphasisData').text
                mileage = int(float(mileage_text) * 10000)

                car_data.append(CarData(date=today, name=car['name'], price=price,
                                        model_year=int(model_year_text), mileage=mileage))

            next_button = soup.find('button', class_='pager__btn__next')
            if ('is-disabled' in next_button.attrs['class']):
                break
            url = domain + re.findall(r'location.href=\'([^\'].*)\'', next_button.attrs['onclick'])[0]

    try:
        db.initialze()
        db.delete(today)
        db.add(car_data)
        db.commit()
    except:
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.disconnect()


if __name__ == '__main__':
    with open(car_list_file, 'r') as yml:
        cars: list[dict[str, str]] = yaml.safe_load(yml)['list']

    db = DBConnector(secrets.DB_HOST, secrets.DB_USER, secrets.DB_PASS, secrets.DB_NAME)
    crawling(cars=cars, db=db)
