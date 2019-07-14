import csv
import json
import yaml
import re


def get_data():
    files = ['info_1.txt', 'info_2.txt', 'info_3.txt']

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data = [headers]

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    re_prod = re.compile(r'Изготовитель системы:\s+(?P<prod>.*?)\s*\n')
    re_name = re.compile(r'Название ОС:\s+(?P<name>.*?)\s*\n')
    re_code = re.compile(r'Код продукта:\s+(?P<code>.*?)\s*\n')
    re_type = re.compile(r'Тип системы:\s+(?P<type>.*?)\s*\n')

    for file in files:
        with open('data/lesson2/' + file) as f:
            for line in f:
                m = re.match(re_prod, line)
                if m:
                    prod = m.group('prod')
                    os_prod_list.append(prod)
                m = re.match(re_name, line)
                if m:
                    name = m.group('name')
                    os_name_list.append(name)
                m = re.match(re_code, line)
                if m:
                    code = m.group('code')
                    os_code_list.append(code)
                m = re.match(re_type, line)
                if m:
                    type = m.group('type')
                    os_type_list.append(type)

    for i in range(len(files)):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])

    return main_data


def write_to_csv(path):
    main_data = get_data()

    with open(path, 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for row in main_data:
            writer.writerow(row)


def write_order_to_json(item, quantity, price, buyer, date):
    path = 'data/lesson2/orders.json'
    data = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date}

    with open(path) as f:
        temp = json.load(f)

    temp['orders'].append(data)

    with open(path, 'w') as f:
        json.dump(temp, f, indent=4)


def write_to_yaml():
    path = 'data/lesson2/write.yml'
    data = {
        'cities': ['Moscow', 'Berlin', 'London'],
        'count': 3,
        'currency': {'Moscow': '₽', 'Berlin': '€', 'London': '£'}
    }

    with open(path, 'w', encoding='utf_8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    with open(path, encoding='utf8') as f:
        temp = yaml.load(f, Loader=yaml.Loader)

    return data == temp


def main():
    write_to_csv('data/lesson2/write.csv')
    write_order_to_json('Table', 1, 2000, 'Olesya', '2019-07-14')
    print(write_to_yaml())


if __name__ == '__main__':
    main()
