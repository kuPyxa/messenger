import csv
import json
import yaml
import re


def get_data():
    files = ['info_1.txt', 'info_2.txt', 'info_3.txt']

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data = [headers]

    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []

    re_all = re.compile(r'(Название ОС|Код продукта|Изготовитель системы|Тип системы):\s+(.*?)\s*\n')

    for name in files:
        with open('data/lesson2/' + name) as file:
            data = file.read()
            match = re.findall(re_all, data)
            os_name_list.append(match[0][1])
            os_code_list.append(match[1][1])
            os_prod_list.append(match[2][1])
            os_type_list.append(match[3][1])

    main_data.extend([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]] for i in range(len(files)))

    return main_data


def write_to_csv(path):
    main_data = get_data()

    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        for row in main_data:
            writer.writerow(row)


def write_order_to_json(item, quantity, price, buyer, date):
    path = 'data/lesson2/orders.json'
    data = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date}

    with open(path) as file:
        temp = json.load(file)
        temp['orders'].append(data)

    with open(path, 'w') as file:
        json.dump(temp, file, indent=4)


def write_to_yaml():
    path = 'data/lesson2/write.yml'
    data = {
        'cities': ['Moscow', 'Berlin', 'London'],
        'count': 3,
        'currency': {'Moscow': '₽', 'Berlin': '€', 'London': '£'}
    }

    with open(path, 'w', encoding='utf_8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

    with open(path, encoding='utf8') as file:
        temp = yaml.load(file, Loader=yaml.Loader)

    return data == temp


def main():
    write_to_csv('data/lesson2/write.csv')
    write_order_to_json('Table', 1, 2000, 'Olesya', '2019-07-14')
    print(write_to_yaml())


if __name__ == '__main__':
    main()
