# Utility to Parse HTML IRC logs from echelog.com into plaintext
# Copyright (C) 2021 J. Madgwick

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from bs4 import BeautifulSoup
import os
from datetime import datetime

import locale
locale.setlocale(locale.LC_ALL, '')   # use user's preferred locale


argPath = 'echelog/'
argHide = True
outFile = open(argPath + 'output.log', 'w')
dateTimeFormat = '%Y-%m-%dT%H:%M:%S'

files = os.listdir(argPath)
#Filter out non html files and remove extension to allow easy sorting
pages = [fn[:-5] for fn in files if fn[-5:] == '.html']
pages.sort()

for webpage in pages:
    #Open file and parse HTML
    with open(argPath + '/' + webpage + '.html') as doc:
        soup = BeautifulSoup(doc, 'html.parser')

    print(webpage, end="\r")
    ircText = soup.body.pre
    ircLines = []

    for line in ircText.find_all('div'):
        time = str(line.contents[0])[1:9]
        msgType = line.contents[1]['class'][0]
        message = line.contents[1].get_text()
        #Skip blank messages
        if message != '':
            ircLines.append([time,msgType,message])
    
    for line in ircLines:
        if line[1] == 'd' or not argHide:
            outFile.write(datetime.strptime(webpage[:10] + line[0],'%Y-%m-%d%H:%M:%S').strftime(dateTimeFormat) + ' ' + line[2] + '\n')
outFile.close()

