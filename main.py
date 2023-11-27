import requests
import csv
from operator import itemgetter


def parse_it():
    each_page = 1
    get_data = requests.get(
        url=f'https://4lapy.ru/api/goods_list_cached/?category_id=165&count=10&page={each_page}&sort=popular'
    )
    page_number = get_data.json()['data']['total_pages']
    with open('data.csv', mode='w', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow(
            [
                'id',
                'Наименование',
                'Ссылка на товар',
                'Регулярная цена',
                'Промо цена',
                'Бренд',
            ]
        )
        for each_page in range(1, page_number + 1):
            lentgh = get_data.json()['data']['goods']
            data = [
                get_data.json()['data']['goods'][i]['packingVariants']
                for i in range(len(lentgh))
            ]
            d = [
                itemgetter(
                    'id',
                    'title',
                    'webpage',
                    'price',
                    'brand_name',
                    'availability',
                )(each_product)
                for each_variants in data
                for each_product in each_variants
            ]
            for product in d:
                if product[5] == 'В наличии':
                    file_writer.writerow(
                        [
                            product[0],
                            product[1],
                            product[2],
                            product[3].get('actual'),
                            (
                                product[3].get('singleItemPackDiscountPrice')
                                if product[3].get(
                                    'singleItemPackDiscountPrice'
                                )
                                != 0
                                else 'Скидки нет'
                            ),
                            product[4],
                        ]
                    )


if __name__ == '__main__':
    parse_it()
