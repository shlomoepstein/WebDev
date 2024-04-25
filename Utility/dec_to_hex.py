'''dec_to_hex.py
Apparently there's a built-in `hex()`, but I didn't have a connection
and wanted to convert some character codes for HTML, so I cooked this up
'''


import sys, math


def dec_to_hex(number):
    dec = number
    hex_places = 0
    hex = ''

    while math.pow(16, hex_places) <= number:
        hex_places += 1

    for i in range(hex_places - 1, -1, -1):
        place = 0
        while dec >= math.pow(16, i):
            dec -= math.pow(16, i)
            place += 1

        hex += hex_digit(place)

    return hex


def hex_digit(number):
    hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    return hex[number]


def main():
    number = int(sys.argv[1])
    print(f'{number} = 0x{dec_to_hex(number)}')


if __name__ == '__main__':
    main()
