import os
import math
import re

from datetime import date
from openpyxl import load_workbook
from mutagen.mp3 import MP3
from int_to_words import kwotaslownie

from customers import Customer
from customers_data import WD, GH

today = date.today()
date = today.strftime("%d.%m.%Y")

rate = 2.47 / 60
principals = ['WD', 'GH']

principal = input('Podaj zleceniodawcę: (WD/GH)')
mp3_path = input('Podaj ścieżkę folderu z plikami')
invoice_dir = input('Podaj ścieżkę w której zostanie zapisana faktura')
invoice_patch = '/Users/tszos/Documents/Faktury/WD_2022.xlsx'
invoice_number = input('podaj numer faktury')


def get_customer(princip=principal):
    while princip not in principals:
        print('brak zleceniobiorcy w bazie')
        princip = input('Podaj zleceniodawcę: (WD/GH)')
    else:
        if princip == 'WD':
            customer = Customer(**WD)
        elif princip == 'GH':
            customer = Customer(**GH)
    return customer


# mp3 data
def mp3_data(path=mp3_path):
    book = 0
    book_name_raw = path.split('/')[-1]
    book_name = " ".join(re.findall('[A-Z][^A-Z]*', book_name_raw))
    os.chdir(path)
    obj = os.scandir()
    for entry in obj:
        if entry.is_dir() or entry.is_file():
            audio = MP3(entry)
            length = audio.info.length
            book += length
    obj.close()
    return book, book_name


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def calculate_earnings():
    book_length = mp3_data()[0]
    return book_length * rate


def post_to_invoice(customer=get_customer(), inv_patch=invoice_patch,
                    inv_number=invoice_number, name=f'{invoice_number.replace("/", "_")}.xlsx'):
    inv = load_workbook(inv_patch)
    invoice = inv.active
    book_name = mp3_data()[1]
    charge = round_up(calculate_earnings())
    invoice['A8'] = inv_number
    invoice['C14'] = customer.name
    invoice['C15'] = customer.address
    invoice['C16'] = customer.postal_code
    invoice['C17'] = customer.nip
    invoice['C23'] = f'Montaż dźwięku {book_name}'
    invoice['C32'] = f"Do zapłaty: {charge} zł"
    invoice['E26'] = f"Razem Do zapłaty: {charge} zł"
    invoice['F23'] = charge
    invoice['F2'] = f'Data wykonania usług: {date}'
    invoice['F4'] = f'Data wystawienia: {date}'
    invoice['C27'] = f'SŁOWNIE: {kwotaslownie(charge, 1).replace(".", ",")}'
    inv.save(f'{invoice_dir}/{name}')
    print(f"{book_name} - {charge} zł")


# if __name__ == '__main__':
mp3_data()
post_to_invoice()
