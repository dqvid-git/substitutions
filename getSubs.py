import requests
import hashlib
import os
import tabula
from random import random
from datetime import datetime

URL = 'http://rgkript.ru/wp-content/uploads//'

def getFileName():
    return hashlib.sha512(str(random()).encode('utf-8')).hexdigest()[::10]

def getDate():
    """
    Returns substitutions date.
    """
    monthDayQntt = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    day = datetime.now().day if datetime.now().weekday() < 5 else datetime.now().day + (7 - datetime.now().weekday())
    month = datetime.now().month if day < monthDayQntt[datetime.now().month-1] else datetime.now().month+1
    if month > datetime.now().month: day -= monthDayQntt[month-2]
    month = f'0{month}' if month < 10 else str(month)
    day = f'0{day}' if day < 10 else str(day)
    year = str(datetime.now().year)
    return {'day': day, 'month': month, 'year': year}

def getURL(date):
    """
    Returns RGKRIPT url to download substitutions.
    """
    return f'{URL}{date["year"]}/{date["month"]}/ZAMENY-{date["day"]}.{date["month"]}.{date["year"]}-1.pdf'

def downloadSubs(url, fileName):
    """
    Downloads and saves a file with substitutions.
    """
    data = requests.get(url)
    with open(f'{fileName}.pdf', 'wb') as file:
        file.write(data.content)

def getSubstitutions(groupName):
    date = getDate()
    fileName = getFileName()
    downloadSubs(getURL(getDate()), fileName)
    # run(f'libreoffice --headless --convert-to pdf {fileName}.doc'.split())

    tables = tabula.read_pdf(f'{fileName}.pdf', multiple_tables=True, lattice=True, pages='all')

    if tables.__len__() == 0:
        os.remove(f'{fileName}.pdf')
        date = getDate()
        date['day'] = str(int(date['day'])+1)
        downloadSubs(getURL(date), fileName)
        tables = tabula.read_pdf(f'{fileName}.pdf', multiple_tables=True, lattice=True, pages='all')
        if tables.__len__() == 0:
            os.remove(f'{fileName}.pdf')
            date = getDate()
            date['day'] = str(int(date['day'])+2)
            downloadSubs(getURL(date), fileName)
            tables = tabula.read_pdf(f'{fileName}.pdf', multiple_tables=True, lattice=True, pages='all')

    subs = []

    for table in tables:
        for i in range(table.__len__()):
            sub = []
            if str(table.iloc[i,0]).lower() == groupName.lower():
                for j in range(4):
                    if str(table.iloc[i,j+1]) != 'nan':
                        sub.append(str(table.iloc[i,j+1]))
                subs.append(', '.join(sub))

    os.remove(f'{fileName}.pdf')
    if subs.__len__() == 0: return 'У вас нет замен'
    if subs.__len__() > 0: return f'Замены на {".".join(date.values())}:\n' + '\n\n'.join(subs)
