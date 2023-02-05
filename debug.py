from crawler import crawling, CarData

name = 'CLA 45 S'
url = '/usedcar/search.php?STID=CS210610&CARC=AM_S002&GRDKC=AM_S002_F002_K003&OPTCD=REP0'

if __name__ == '__main__':
    cars: list[dict[str, str]] = [{"name": name, "url": url}]

    data: list[CarData] = crawling(cars=cars)

    for d in data:
        print(d.name, d.price, d.model_year, d.mileage)
