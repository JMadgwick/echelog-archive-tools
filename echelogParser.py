from bs4 import BeautifulSoup
import os
from datetime import datetime

import locale
locale.setlocale(locale.LC_ALL, '')   # use user's preferred locale


argPath = 'echelog/'
argHide = True

files = os.listdir(argPath)
#Filter out non html files and remove extension to allow easy sorting
pages = [fn[:-5] for fn in files if fn[-5:] == '.html']
pages.sort()

for webpage in pages:
    #Open file and parse HTML
    with open(argPath + '/' + webpage + '.html') as doc:
        soup = BeautifulSoup(doc, 'html.parser')

    ircText = soup.body.pre
    ircLines = []

    for line in ircText.find_all('div'):
        time = str(line.contents[0])[1:9]
        msgType = line.contents[1]['class'][0]
        message = line.contents[1].get_text()
        ircLines.append([time,msgType,message])
    
    for line in ircLines:
        if line[1] == 'd' or not argHide:
            print(datetime.strptime(webpage[:10] + line[0],'%Y-%m-%d%H:%M:%S').strftime('%c ') + line[2])

