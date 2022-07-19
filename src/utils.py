import os
import math
import re
import fnmatch


from openpyxl import load_workbook
from mutagen.mp3 import MP3
from int_to_words import kwotaslownie

from customers import Customer
from customers_data import CUSTOMERS
from config import RATE, INVOICE_TEMPLATE, PRINCIPAL, MP3_PATH, INVOICE_NUMBER, INVOICE_DIR, DATE, SYSTEM


def get_customer(princip=PRINCIPAL):
    while princip not in CUSTOMERS.keys():
        print('brak zleceniobiorcy w bazie')
        princip = input('Podaj zleceniodawcę: (WD/GH)')
    else:
        customer = Customer(**CUSTOMERS[princip])
        return customer

def mp3_data():
    book = 0
    book_name_raw = MP3_PATH.split('\\')[-1].capitalize() if SYSTEM == 'Windows' else MP3_PATH.split('/')[-1].capitalize()
    book_name = " ".join(re.findall('[A-Z][^A-Z]*', book_name_raw))
    os.chdir(MP3_PATH)
    obj = os.scandir()
    for entry in obj:
        if fnmatch.fnmatch(entry, '*mp3'):
            if entry.is_dir() or entry.is_file():
                audio = MP3(entry)
                lengh = audio.info.length
                book += lengh
    obj.close()
    return book, book_name


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def calculate_earnings():
    book_length = mp3_data()[0]
    return book_length * RATE


def post_to_invoice():
    customer = get_customer()
    name = f'{INVOICE_NUMBER.replace("/", "_")}.xlsx'
    inv = load_workbook(INVOICE_TEMPLATE)
    invoice = inv.active
    book_name = mp3_data()[1]
    charge = round_up(calculate_earnings())
    invoice['A8'] = INVOICE_NUMBER
    invoice['C14'] = customer.name
    invoice['C15'] = customer.address
    invoice['C16'] = customer.postal_code
    invoice['C17'] = customer.nip
    invoice['C23'] = f'Montaż dźwięku {book_name}'
    invoice['C32'] = f"Do zapłaty: {charge} zł"
    invoice['E26'] = f"Razem Do zapłaty: {charge} zł"
    invoice['F23'] = charge
    invoice['F2'] = f'Data wykonania usług: {DATE}'
    invoice['F4'] = f'Data wystawienia: {DATE}'
    invoice['C27'] = f'SŁOWNIE: {kwotaslownie(charge, 1).replace(".", ",")}'
    inv.save(f'{INVOICE_DIR}/{name}')
    print(f"{book_name} - {charge} zł")
