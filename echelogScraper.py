# Utility to fetch HTML IRC logs from the archived version of echelog.com
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
import requests
from datetime import datetime

startingURL = 'https://web.archive.org/web/20200531221309/https://echelog.com/logs/browse/????'
URL = startingURL

for i in range(1,10):
    print('Downloading page... ')
    result = requests.get(URL)
    resultURL = result.url
    print('Fetched: ' + resultURL)
    webpage = result.text

    soup = BeautifulSoup(webpage, 'html.parser')

    #To get next URL, find the previous page anchor - shown as '<' twice (at top and bottom of the page)
    #anchor = soup.body.contents[3].contents[5] #Hardcoded location will not work if Wayback toolbar is inserted
    anchor = soup.find_all(string="<")[0].parent #find_all gives up the string itself, we need the <a> which is the parent
    nextPage = anchor['href']
    print('Next page is: ' + nextPage)
    
    #Rewrite URL to fetch as last fetched (including redirects) but with page changed
    URL = resultURL[:resultURL.rindex('/') + 1] + nextPage
    
    #To get date, use anchor parent (menu <div>) and fixed location
    pageDate = anchor.parent.contents[2][3:-2] #Plus trim '&nbsp' chars and spaces from start and end of string
    outputFilename = datetime.strptime(pageDate,'%B %d, %Y').date().strftime('%Y-%m-%d') + '.html'
    
    open('echelog/' + outputFilename, 'wb').write(result.content)
    print('Saved file as: ' + outputFilename)
