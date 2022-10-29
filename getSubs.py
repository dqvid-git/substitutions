import requests
import hashlib
import os
import tabula
from bs4 import BeautifulSoup as BS
from random import random

def getFileName():
    return hashlib.sha512(str(random()).encode('utf-8')).hexdigest()[:10]

def getDate():
    req = requests.get('http://rgkript.ru/raspisanie-zanyatiy/')
    return BS(req.content, 'html.parser').select('.page-content > h3 > a')[0].getText()[-10:]

def getURL():
    req = requests.get('http://rgkript.ru/raspisanie-zanyatiy/')
    return BS(req.content, 'html.parser').select('.page-content > h3 > a')[0]['href']

def downloadSubs(url, fileName):
    data = requests.get(url)
    with open(f'{fileName}.pdf', 'wb') as file:
        file.write(data.content)

def getSubstitutions(groupName):
    fileName = getFileName()
    downloadSubs(getURL(), fileName)

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
    if subs.__len__() > 0: return f'Замены на {getDate()}:\n' + '\n\n'.join(subs)
