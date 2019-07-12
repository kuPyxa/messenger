import subprocess
from chardet.universaldetector import UniversalDetector


def task1():
    # Encoding
    w1 = 'разработка'
    w2 = 'сокет'
    w3 = 'декоратор'

    bw1 = w1.encode()
    bw2 = w2.encode()
    bw3 = w3.encode()

    print(bw1)
    print(bw2)
    print(bw3)


def task2():
    # Check type, content and length
    w1 = b'class'
    w2 = b'function'
    w3 = b'method'

    print(type(w1), w1, len(w1))
    print(type(w2), w2, len(w2))
    print(type(w3), w3, len(w3))


def task3():
    # Converting to byte type
    w1 = b'attribute'
    # w2 = b'класс'
    # w3 = b'функция'
    w4 = b'type'


def task4():
    # Encoding decoding
    w1 = 'разработка'
    w2 = 'администрирование'
    w3 = 'protocol'
    w4 = 'standard'

    wb1 = w1.encode().decode()
    wb2 = w2.encode().decode()
    wb3 = w3.encode().decode()
    wb4 = w4.encode().decode()

    print(wb1, wb2, wb3, wb4)


def task5():
    # Ping yandex.ru, youtube.com
    sites = ['yandex.ru', 'youtube.com']
    for site in sites:
        s = subprocess.run(["ping", site], capture_output=True)
        result = s.stdout.decode()
        print(result)


def task6():
    # Writing to file, check encoding, open with utf-8
    filename = 'temp.txt'
    strings = ['сетевое программирование', 'сокет', 'декоратор']
    with open(filename, 'w') as f:
        for string in strings:
            f.write(string + '\n')

    detector = UniversalDetector()
    detector.reset()
    with open(filename, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        print(detector.result)

    with open(filename, encoding='utf-8') as f:
        result = f.readline()
        print(result)


def main():
    # task1()
    # task2()
    # task3()
    # task4()
    # task5()
    task6()


if __name__ == '__main__':
    main()
