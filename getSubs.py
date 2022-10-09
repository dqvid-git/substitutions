import requests
import hashlib
import os
import tabula
from subprocess import run
from random import random
from datetime import datetime

URL = 'http://rgkript.ru/wp-content/uploads//'
FILENAME = hashlib.sha512(str(random()).encode('utf-8')).hexdigest()[::10]

def getURL():
    """
    Returns RGKRIPT url to download substitutions.
    """
    day = datetime.now().day
    day = f'0{day}'
    if datetime.now().weekday() == 5:
        day = f'0{int(day)+2}'
    elif datetime.now().weekday() == 6:
        day = f'0{int(day)+1}'
    elif (datetime.now().hour > 18) and (datetime.now().minute > 30):
        day = f'0{int(day)+1}'
    if day.__len__() == 3:
        day = day[1::]
    month = datetime.now().month
    if month < 10:
        month = f'0{month}'
    year = datetime.now().year
    print(f'{URL}{year}/{month}/ZAMENY-{day}.{month}.{year}.doc')
    return f'{URL}{year}/{month}/ZAMENY-{day}.{month}.{year}.doc'

def getSubstitutions(groupName):
    data = requests.get(getURL())
    with open(f'{FILENAME}.doc', 'wb') as file:
        file.write(data.content)

    run(f'libreoffice --headless --convert-to pdf {FILENAME}.doc'.split())

    tables = tabula.io.read_pdf(f'{FILENAME}.pdf', multiple_tables=True, lattice=True, pages='all')

    subs = []

    for table in tables:
        for i in range(table.__len__()):
            sub = []
            if table.iloc[i,0] == groupName:
                for j in range(4):
                    if str(table.iloc[i,j+1]) != 'nan':
                        sub.append(str(table.iloc[i,j+1]))
                subs.append(', '.join(sub))

    if subs.__len__() == 0: return 'У вас нет замен'
    if subs.__len__() > 0: return '\n'.join(subs)
