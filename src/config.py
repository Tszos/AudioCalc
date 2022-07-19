from six import u
import platform
from datetime import date

SYSTEM = platform.system()

JEDNOSTKI = [u(""), u("jeden"), u("dwa"), u("trzy"), u("cztery"), u("pięć"),
        u("sześć"), u("siedem"), u("osiem"), u("dziewięć")]
DZIESIATKI = [u(""), u("dziesięć"), u("dwadzieścia"), u("trzydzieści"),
        u("czterdzieści"), u("pięćdziesiąt"), u("sześćdziesiąt"),
        u("siedemdziesiąt"), u("osiemdziesiąt"), u("dziewięćdziesiąt")]
NASTKI = [u("dziesięć"), u("jedenaście"), u("dwanaście"), u("trzynaście"),
        u("czternaście"), u("piętnaście"), u("szesnaście"), u("siedemnaście"),
        u("osiemnaście"), u("dziewiętnaście")]
SETKI = [u(""), u("sto"), u("dwieście"), u("trzysta"), u("czterysta"),
        u("pięćset"), u("sześćset"), u("siedemset"), u("osiemset"),
        u("dziewięćset")]

WIELKIE = [
        [u("x"), u("x"), u("x")],
        [u("tysiąc"), u("tysiące"), u("tysięcy")],
        [u("milion"), u("miliony"), u("milionów")],
        [u("miliard"), u("miliardy"), u("miliardów")],
        [u("bilion"), u("biliony"), u("bilionów")],
    ]

ZLOTOWKI = [u("złoty"), u("złote"), u("złotych")]
GROSZE = [u("grosz"), u("grosze"), u("groszy")]

RATE = 2.47 / 60

TODAY = date.today()
DATE = TODAY.strftime("%d.%m.%Y")

INVOICE_TEMPLATE = "/Users/tszos/Desktop/1_06_2022.xlsx"
PRINCIPAL = input('Podaj zleceniodawcę: (WD/GH)').upper()
MP3_PATH = input('Podaj ścieżkę folderu z plikami')
INVOICE_DIR = input('Podaj ścieżkę w której zostanie zapisana faktura')
INVOICE_NUMBER = input('podaj numer faktury')

BOOK_TITLE_SCHEME = '[A-Z][^A-Z]*'
