#!/usr/bin/env python
""" trendlines command line tool

Usage:
    trendlines [-n NUMBER] [-s CRITERIA] [-d DATE] KEYWORD

Options:
    -h --help             show this screen
    -n --number=NUMBER    specify the number of results displayed
    -s --sortby=CRITERIA  specify the ranking criteria
    -d --date=DATE        specify the search date

"""
import docopt
import requests
from bcolors import BColors

wordlink_api = 'http://wordlink.com/search.php?'

def parse_arguments():
    return docopt.docopt(__doc__)

def formulate_request(url,arguments):
    number = arguments['--number'] if arguments['--number'] else ''
    sortby = arguments['--sortby'] if arguments['--sortby'] else ''
    date = arguments['--date'] if arguments['--date'] else ''
    keyword = arguments['KEYWORD']
    request = url + 'word='+keyword+'&date='+date \
            +'&sortby='+sortby
    return request

def main():
    arguments = parse_arguments()
    request = formulate_request(wordlink_api,arguments)
    response = requests.get(request)
    num_hits = response.json()['hits']['total']
    hits = response.json()['hits']['hits']

    num_display = int(arguments['--number'])
    for count,hit in enumerate(hits):
        if (count+1) > num_display:
            break
        else:
            title = hit['_source']['doc']['title'].encode('utf-8')
            url = hit['_source']['doc']['url'].encode('utf-8')
            print ('{count}     {title}').format(count=count+1,title=title)
            print BColors.OKBLUE+ '      {url}'.format(url=url) \
                  + BColors.ENDC



if __name__ == '__main__':
    main()
