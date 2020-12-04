import requests
import json
import time
from bs4 import BeautifulSoup
import csv


# response = requests.get("https://www.zillow.com/charlotte-nc/", headers = headers, params = params)
# print(response)
def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def construct_unique_key(url,params={}):
    """
    constructs a key that is guaranteed to uniquely and repeatably
    identify an API request by its baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string 
    """
    param_string = []
    for k in params.keys():
        param_string.append(f"{k}={params[k]}")
    param_string.sort()
    unique_key = url+str(param_string)
    return unique_key

def make_request_with_cache(url, params={}):
    '''Check the cache for a saved result for this url+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    request_key = construct_unique_key(url,params=params)
    if request_key in CACHE_DICT.keys():
        print('Using Cache')
        return CACHE_DICT[request_key]
    else:
        print('Fetching')
        response = requests.get(url,params=params)
        CACHE_DICT[request_key]=response.text
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]

 

class ZillowScraper():
    results = []
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5',
    'cache-control': 'max-age=0',
    'cookie': 'zguid=23|%24adeca446-8fe9-4345-95d0-15c15df2820d; _ga=GA1.2.681585638.1605200876; _pxvid=9b9de636-2509-11eb-a299-0242ac12000d; zjs_anonymous_id=%22adeca446-8fe9-4345-95d0-15c15df2820d%22; _gcl_au=1.1.1108825719.1605200878; G_ENABLED_IDPS=google; zjs_user_id=%22X1-ZU14rncz71hdceh_4rddb%22; ajs_anonymous_id=%22a87d1213-d42f-4b4c-b78b-fafeeb05c712%22; zgcus_lbut=; zgcus_aeut=175617380; zgcus_ludi=f7ca2cfc-2522-11eb-9b0c-0e082db64ac5-17561; optimizelyDomainTestCookie=0.848780011179262; optimizelyEndUserId=oeu1605211770118r0.3628263585884004; FSsampler=136437144; _cs_c=1; _cs_id=815cbce8-f7ad-a7a3-8550-4d22844fa7e7.1605211773.1.1605211773.1605211773.1.1639375773593.Lax.0; __CT_Data=gpv=1&ckp=tld&dm=zillow.com&apv_82_www33=1&cpv_82_www33=1; ki_t=1605211774127%3B1605211774127%3B1605211774127%3B1%3B1; OptanonConsent=isIABGlobal=false&datestamp=Thu+Nov+12+2020+15%3A09%3A34+GMT-0500+(Eastern+Standard+Time)&version=5.11.0&landingPath=https%3A%2F%2Fwww.zillow.com%2Frental-manager%2F%3Fsource%3Dtopnav%26itc%3Dpostbutton_sitenav&groups=1%3A1%2C3%3A1%2C4%3A1; __stripe_mid=1f1299ac-d6b4-4fcf-9f2e-2252378997526b642f; _pin_unauth=dWlkPVpUZzFaams0T0RrdE16RTNOQzAwT0dKbExXSTROVEV0TTJWa00ySmhOalprT1dJMg; zgsession=1|a9df1fa9-8718-4725-a62d-7a82b9d058dd; _gid=GA1.2.486670207.1607107190; KruxPixel=true; DoubleClickSession=true; KruxAddition=true; loginmemento=1|00ba6f79593e9d98768eb07bd7e0eeee52457b3d6b563e179c3c84f923d39cb1; userid=X|3|114b246ad09aa0a7%7C9%7CqK2hLCcYewXV0dibNOGDIgnv8g7_-oxV; g_state={"i_l":1,"i_p":1607115417451}; JSESSIONID=BB39E9CDE2443E0F626759C99D426497; ZILLOW_SSID=1|; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEmnD24KL9BNnlo3WCCPaSV%2Faf2ybPt8TtUbLa%2F7JH7F3UrOuNnA7usgaRLqIAqLEQnY1Z6yUNy1K; _derived_epik=dj0yJnU9WW50VTVkdEdOdDJFM1V1Z1h5TmQtRUpHbk0zUV9rRnImbj1STDVkLXhqNW1VTVJPWEQxUFpXZjd3Jm09NyZ0PUFBQUFBRl9LbnBR; intercom-session-xby8p85u=RXpmamVKc3RXcko2L3J1OG9pYXhFU29tU2R6dy81ekwzYWg3UWgrUTk0R1IvaVNUQ2ZXc0s3OUJzbzFHODNaby0ta1Y4MG9KY1Vrd3QreWhVTE1ySXJldz09--36f380c92907ca9e6dd7eb2a7226a4c551cd7aa0; _px3=24fe966c8c140521ca822e13713252322f0b2b493ba51a6578fbd4913da57498:KQIDvxmbtfVaAyyleccGT6msXrImm006DISGKEvnZvz1B1AOikU6ArBzHlbIb7X5tEMC04TKHsiZTZZzdYypIQ==:1000:7usI7moibXVNqmSY65kPo9KRZcgzIPVVuy+OCf4P7ryYEexevsIhY9RNC5uWmJ1FJWPpt3OzC4ukdV846E/B8oKI9fjpuSUun1caBL7ZSiINlqd4x0N8qLDF28Pp82inbAuWgfVo0BBpgV1E2tOma4VlsEx3IDsuPBdkOfPxvvM=; _uetsid=1b5622a0366011ebbd8ea15c0932a180; _uetvid=1b56a920366011eb895aa9b79d1a7c92; AWSALB=B/OIj/Sm8jzy8iVaxNjSBajeySrZDb1aX5UW9B190+9p6OCKhL9FhMCtvZ4djWiGTet4ycAXdyJWxIkn8ioedUogrMd++g6BglNPMFmBt0+3OytR5VmyNSc7bIbA; AWSALBCORS=B/OIj/Sm8jzy8iVaxNjSBajeySrZDb1aX5UW9B190+9p6OCKhL9FhMCtvZ4djWiGTet4ycAXdyJWxIkn8ioedUogrMd++g6BglNPMFmBt0+3OytR5VmyNSc7bIbA; search=6|1609706682004%7Crect%3D35.314369497727974%252C-80.59740852734375%252C34.970678905935785%252C-80.99856209645348%26rid%3D24043%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%0924043%09%09%09%09%09%09; _gat=1',
    'dnt':'' '1',
    'referer': 'https://www.zillow.com/charlotte-nc/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Charlotte%2C%20NC%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.99856209645348%2C%22east%22%3A-80.59740852734375%2C%22south%22%3A34.970678905935785%2C%22north%22%3A35.314369497727974%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A24043%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

    def fetch(self, url, params):
        response = requests.get(url, headers = self.headers, params = params)
        print(response)
        return response

    def parse(self,response):
        content = BeautifulSoup(response, 'lxml')
        deck = content.find('ul',{'class':'photo-cards photo-cards_wow photo-cards_short'})
        for card in deck.contents:
            script = card.find('script',{'type':'application/ld+json'})
            if script:
                script_json = json.loads(script.contents[0])
                # print(script_json)
                self.results.append({
                    'address':script_json['name'],
                    'price': card.find('div',{'class':'list-card-price'}).text,
                    # 'size': card.find('div',{'class':'list-card-details'}).text,
                    'floorSize': script_json['floorSize']['value'],
                    'url':script_json['url']
                    })
       
        
    def to_csv(self):
        with open('zillow.csv','w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)


    def run(self):
        url = "https://www.zillow.com/charlotte-nc/"
        
        for page in range(1,21):
            params = {
                'searchQueryState': '{"pagination":{},"usersSearchTerm":"Charlotte, NC","mapBounds":{"west":-80.99856209645348,"east":-80.59740852734375,"south":34.970678905935785,"north":35.314369497727974},"regionSelection":[{"regionId":24043,"regionType":6}],"isMapVisible":false,"filterState":{"sort":{"value":"globalrelevanceex"},"ah":{"value":true}},"isListVisible":true,"mapZoom":11}'
                }

            res = self.fetch(url, params)
            self.parse(res.text)
            time.sleep(2)
        self.to_csv()

if __name__ == "__main__":
    scraper = ZillowScraper()
    scraper.run()
