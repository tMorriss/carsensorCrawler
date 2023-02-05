from crawler import crawling, CarData

if __name__ == '__main__':
    cars: list[dict[str, str]] = [
        {'name': 'CLA 45 S', 'url': '/usedcar/search.php?STID=CS210610&CARC=AM_S002&GRDKC=AM_S002_F002_K003&OPTCD=REP0'},
        {'name': 'C63 セダン', 'url': '/usedcar/search.php?STID=CS210610&CARC=AM_S006&GRDKC=AM_S006_F001_K001&YMIN=2019&OPTCD=REP0'}
    ]

    data: list[CarData] = crawling(cars=cars)

    for d in data:
        print(d.name, d.price, d.model_year, d.mileage)
