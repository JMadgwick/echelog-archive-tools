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
import requests,argparse,locale
from pathlib import Path
from datetime import datetime

def validatedURL(URL):
    archivePos = URL.index('https://web.archive.org/web/')
    echelogPos = URL.index('https://echelog.com/logs/browse/')
    if ((archivePos == 0) and (echelogPos == 43)):
        return URL
    else:
        raise ValueError()

#Set locale - used for output message date format
locale.setlocale(locale.LC_ALL, '')

parser = argparse.ArgumentParser(description='Utility to scrape the WayBackMachine archived version of echelog and download pages (containing IRC logs) from a specific channel. The URL supplied must be to an IRC log page, pages/dates before this will then be fetched')
parser.add_argument('initialURL', type=validatedURL, help='URL to start scraping from. Must be in the form https://web.archive.org/web/{datetime}/https://echelog.com/logs/browse/{channel}/{id}')
parser.add_argument('-p', '--pages', type=int, help='Maximum number of pages (days) to download')
parser.add_argument('-na', '--noabort', action='store_true', help="Don't abort when no logs are found for a one month period")
parser.add_argument('outputPath', type=Path, help='Path/directory to write files into. Must already exist, any conflicting files will be overwritten')
args = parser.parse_args()

if (Path.exists(args.outputPath)):
    print ("Writing to '" + str(Path.absolute(args.outputPath)) + "', any conflicting files will be overwritten")
    outputPath = str(args.outputPath)
else:
    print ("Path/directory '" + str(Path.absolute(args.outputPath)) + "' does not exist!")
    exit()

URL = args.initialURL
limit = args.pages or 6000
noLogCheck = 30

for i in range(1,limit):
    print('Downloading page...', end="\r")
    result = requests.get(URL)
    resultURL = result.url
    print('Fetched: ' + resultURL)
    webpage = result.text

    #Check for the final (earliest) page, which is blank and empty
    if (webpage == ''):
        print('Final page reached. Nothing more to fetch.')
        break

    soup = BeautifulSoup(webpage, 'lxml')

    #To get next URL, find the previous page anchor - shown as '<' twice (at top and bottom of the page)
    #anchor = soup.body.contents[3].contents[5] #Hardcoded location will not work if Wayback toolbar is inserted
    anchor = soup.find_all(string="<")[0].parent #find_all gives up the string itself, we need the <a> which is the parent
    nextPage = anchor['href']

    #Rewrite URL to insert web.archive.org URL from last fetched page (including redirects)
    URL = resultURL[:resultURL.rindex('/') + 1] + nextPage

    #To get date, use anchor parent (menu <div>) and fixed location
    pageDate = anchor.parent.contents[2].replace('\xa0','').strip() #Remove '&nbsp' chars and trim spaces from start and end of string
    pageDateParsed = datetime.strptime(pageDate,'%B %d, %Y').date()
    outputFilename = pageDateParsed.strftime('%Y-%m-%d') + '.html'

    #Check not an empty page, don't save these
    if soup.pre.get_text() == 'no log file for date':
        print('WARNING: Nothing logged on ' + pageDate + '. Not saving this page.')
        noLogCheck -= 1
        if ((noLogCheck == 0) and not args.noabort):
            print("No logs found for a one month period. Aborting. Use '-na' flag to disable this.")
            break
    else:
        open(outputPath + '/' + outputFilename, 'wb').write(result.content)
        print('Saved page for ' + pageDateParsed.strftime('%x') + ' as: ' + outputFilename)
        noLogCheck = 30

print('Complete')
