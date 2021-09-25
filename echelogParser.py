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

from bs4 import BeautifulSoup, SoupStrainer
import os,locale,argparse
from datetime import datetime
from alive_progress import alive_bar

parser = argparse.ArgumentParser(description='Simple utility to parse a directory of Echelog HTML IRC chat log files, extract the IRC chat logs and store them in a single file using a standard format. By default, ISO format is used for the timestamp (eg. "2011-02-13T01:55:34").')
parser.add_argument('directory', help='Path to directory containing Echelog HTML files')
parser.add_argument('-l', '--local', action='store_true', help='Use local locale based timestamp instead of ISO format')
parser.add_argument('-a', '--all', action='store_true', help='Include all IRC messages. By default, only chat message are included and not join/part etc. Note that Echelog used different formats for these over the years')
parser.add_argument('output', type=argparse.FileType('w'), help='File to write output into')
args = parser.parse_args()

if args.local:
    #Set locale to local locale
    locale.setlocale(locale.LC_ALL, '')
    dateTimeFormat = '%c'
else:
    dateTimeFormat = '%Y-%m-%dT%H:%M:%S'

files = os.listdir(args.directory)
#Filter out non html files and remove extension to allow easy sorting
pages = [fn[:-5] for fn in files if fn[-5:] == '.html']
#Sort logs into date order
pages.sort()

#Filter to parse only the <pre> tag, not the rest of the document - this improves performance
preFilter = SoupStrainer("pre")

with alive_bar(len(pages), title='Processing HTML files', spinner='classic') as bar:
    for webpage in pages:
        #Open file and parse HTML, use lxml to further improve performance
        with open(args.directory + '/' + webpage + '.html') as doc:
            soup = BeautifulSoup(doc, 'lxml', parse_only=preFilter)

        bar()
        bar.text('[File: '+ webpage + ']')
        ircText = soup#.body.pre
        ircLines = []

        for line in ircText.find_all('div'):
            time = str(line.contents[0])[1:9]
            msgType = line.contents[1]['class'][0]
            message = line.contents[1].get_text()
            #Skip blank messages
            if message != '':
                ircLines.append([time,msgType,message])

        for line in ircLines:
            if line[1] == 'd' or args.all:
                args.output.write(datetime.strptime(webpage[:10] + line[0],'%Y-%m-%d%H:%M:%S').strftime(dateTimeFormat) + ' ' + line[2] + '\n')

args.output.close()
