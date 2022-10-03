import requests
import hashlib
from docx import Document
from random import random
from datetime import datetime

URL = 'http://rgkript.ru/wp-content/uploads//'
FILENAME = hashlib.sha512(str(random()).encode('utf-8')).hexdigest()

def getSubstitutionURL():
    """
    Returns RGKRIP url to download substitutions.
    """
    day = datetime.now().day
    if day < 10:
        day = '0' + str(day)
        if datetime.now().hour > 16:
            day = '0' + str(int(day)+1)
    month = datetime.now().month
    if month < 10:
        month = '0' + str(month)
    year = datetime.now().year
    return f'{URL}{year}/{month}/ZAMENY-{day}.{month}.{year}.doc'


data = requests.get(getSubstitutionURL())
with open(FILENAME[::10] + '.doc', 'wb') as file:
    file.write(data.content)

doc = Document(f'{FILENAME[::10]}.doc')
print(doc.tables)

print(URL + getSubstitutionURL())
