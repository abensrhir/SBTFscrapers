import requests as req
from lxml import html

## The url you want to scrape , please just replace 
## &pl=freetown&t=c&i=SL&searchcity=Freetown%20Sierra%20Leone&search=hospital"
## with the appropriate string and leave ?p=**page** intouched , it will be used to go through the pages

__url__ = "http://yellowpages.cybo.com/search/?p=**page**&pl=freetown&t=c&i=SL&searchcity=Freetown%20Sierra%20Leone&search=hospital"


## Please replace this with the number of pages you want to scrape , if the page is empty it will be handled accordignly

__number_of_pages__ = 3

def requestpage(url,pagenumber):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    _url = url.replace("**page**",str(pagenumber))
    _content = req.get(_url,headers=headers).content
    return _content

def parsepage(_htmlcontent_):
    finalresults = []
    content_tree = html.fromstring(_htmlcontent_)
    #print content_tree
    results = content_tree.xpath('//*[@id="results"]/tr/td')
    #print _htmlcontent
    if len(results) < 1:
        return
    else:

        for result in results:
            #print result
            _location_name = result.xpath('.//a/div/table[1]/tr[1]/td[1]/strong/a/span/text()')
            _address = result.xpath('.//a/div/table[2]/tr/td[1]/span/i/span/text()')
            _city = result.xpath('.//a/div/table[2]/tr/td[1]/span/span[1]/text()')
            _administrative_region = result.xpath('.//a/div/table[2]/tr/td[1]/span/span[2]/text()')
            _country = result.xpath('.//a/div/table[2]/tr/td[1]/span/span[3]/text()')
            _phone = result.xpath('.//a/div/table[2]/tr/td[2]/a/span/text()')
            if len(_location_name)>0:
                location_name = _location_name[0] if 0 < len(_location_name) else None
                address = _address[0] if 0 < len(_address) else None
                city = _city[0] if 0 < len(_city) else None
                administrative_region = _administrative_region[0] if 0 < len(_administrative_region) else None
                country = _country[0] if 0 < len(_country) else None
                phone = _phone[0] if 0 < len(_phone) else None
                output = {"locationname":location_name,"address":address,"city":city,"region":administrative_region,"phone":phone,"country":country}
                finalresults.append(output)
            else:
                continue
        return finalresults

pageresults = []
for page in range(1,__number_of_pages__+1):
    data = requestpage(__url__,page)
    output = parsepage(data)
    if output:
        pageresults.extend(output)

print pageresults