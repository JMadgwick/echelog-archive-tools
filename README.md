# echelog-archive-tools

Two simple utilities, one to scrape the [WayBackMachine](https://web.archive.org/) archived version of echelog and download HTML pages (containing IRC logs) from a specific channel, the other to parse these, extract the IRC chat logs and store them in a single file using a standard format.

_License: GNU AGPLv3_

#### Notes

The Echelog website hosted IRC logs for various different channels, most of these had archives going back for many years. In 2020 the owner of the website decided to close it down, see [the archived homepage for details](https://web.archive.org/web/20200601065804/https://echelog.com/).

Before the website finished shutting down and was taken offline, [a full archive of all content was taken](https://www.reddit.com/r/Archiveteam/comments/g30ipr/echelog_an_irc_log_archive_is_shutting_down_on/) by the Archive Team [ArchiveBot](https://wiki.archiveteam.org/index.php/ArchiveBot). This is now available in the Archive.org WayBackMachine.

And so it’s still possible to access all of the IRC logs previously hosted on Echelog.

The logs are available as HTML pages only, with one day of a channel on a single page. There’s no way to view more than a single day at a time and no way to search.

The purpose of the scraping tool is to easily download HTML log pages from the archived version of Echelog. These pages can then be parsed with the parsing tool to produce a single IRC log in the usual format.

The scraping tool works by downloading the initial page, finding the link to the previous page, downloading that page, and so on. To find the initial page (last date of IRC logs logged by Echelog), use the wildcard search on the WayBackMachine and get the archived URL for the page ending with the highest number (result URLs can be sorted). For postfix IRC logs, this would look like [`web.archive.org/web/*/http://echelog.com/logs/browse/postfix/*`](https://web.archive.org/web/*/http://echelog.com/logs/browse/postfix/*). The complete list of all IRC channels on Echelog was/is [on the homepage](https://web.archive.org/web/20200601065804/https://echelog.com/).

    
### echelogScraper.py
```
usage: echelogScraper.py [-h] [-p PAGES] [-na] initialURL outputPath

Utility to scrape the WayBackMachine archived version of echelog and download pages (containing IRC logs) from a specific
channel. The URL supplied must be to an IRC log page, pages/dates before this will then be fetched

positional arguments:
  initialURL            URL to start scraping from. Must be in the form
                        https://web.archive.org/web/{datetime}/https://echelog.com/logs/browse/{channel}/{id}
  outputPath            Path/directory to write files into. Must already exist, any conflicting files will be overwritten

optional arguments:
  -h, --help            show this help message and exit
  -p PAGES, --pages PAGES
                        Maximum number of pages (days) to download
  -na, --noabort        Don't abort when no logs are found for a one month period
```

### echelogParser.py
```
usage: echelogParser.py [-h] [-l] [-a] directory output

Simple utility to parse a directory of Echelog HTML IRC chat log files, extract the IRC chat logs and store them in a single
file using a standard format. By default, ISO format is used for the timestamp (eg. "2011-02-13T01:55:34").

positional arguments:
  directory    Path to directory containing Echelog HTML files
  output       File to write output into

optional arguments:
  -h, --help   show this help message and exit
  -l, --local  Use local locale based timestamp instead of ISO format
  -a, --all    Include all IRC messages. By default, only chat message are included and not join/part etc. Note that Echelog
               used different formats for these over the years
```
## Python Setup

1. Setup a Python virtual environment (optional): `virtualenv -p python3 pyenv`
1. Enter the Python virtual environment (optional): `source pyenv/bin/activate`
2. Install Requirements using pip: `pip install -r requirements.txt`
