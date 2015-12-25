#!/usr/bin/env python
""" trendlines command line tool

Usage:
    trendlines news KEYWORD [-n NUMBER] [-s CRITERIA] [-d DATE]
    trendlines weather CITY [-m METRICS]

Options:
    -h --help             show this screen
    -n --number=NUMBER    specify the number of results displayed
    -s --sortby=CRITERIA  specify the ranking criteria
    -d --date=DATE        specify the search date
    -m --metrics=METRICS  specify the unit for weather display

"""
import docopt
import requests
from bcolors import BColors

wordlink_api = 'http://wordlink.com/search.php?'
weather_api = 'http://api.openweathermap.org/data/2.5/weather?'

def parse_arguments():
    return docopt.docopt(__doc__)

def formulate_request_news(url,arguments):
    number = arguments['--number'] if arguments['--number'] else ''
    sortby = arguments['--sortby'] if arguments['--sortby'] else ''
    date = arguments['--date'] if arguments['--date'] else ''
    keyword = arguments['KEYWORD']
    request = url + 'word='+keyword+'&date='+date \
            +'&sortby='+sortby
    return request

def formulate_request_weather(url,city,metrics,api):
    request = url + 'q='+ city + '&units='+metrics+'&appid='+api
    return request

def main():
    arguments = parse_arguments()
    if arguments['news']:
        request = formulate_request_news(wordlink_api,arguments)
        response = requests.get(request)
        num_hits = response.json()['hits']['total']
        hits = response.json()['hits']['hits']

        num_display = int(arguments['--number']) if arguments['--number'] else 10
        for count,hit in enumerate(hits):
            if (count+1) > num_display:
                break
            else:
                title = hit['_source']['doc']['title'].encode('utf-8')
                url = hit['_source']['doc']['url'].encode('utf-8')
                print ('{count}     {title}').format(count=count+1,title=title)
                print BColors.OKBLUE+ '      {url}'.format(url=url) \
                      + BColors.ENDC

    elif arguments['weather']:
        api_id = '2de143494c0b295cca9337e1e96b00e0'
        city = arguments['CITY']
        metrics = arguments['--metrics'] if arguments['--metrics'] in ['metric','imperial'] else 'metric'
        request = formulate_request_weather(weather_api,city,metrics,api_id)
        response = requests.get(request).json()
        degree = response['main']['temp']
        print 'weather service in development', 'temp:', degree



if __name__ == '__main__':
    main()
