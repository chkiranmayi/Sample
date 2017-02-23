rom juicer.utils import *
from juicer.items import *
from scrapy.http import FormRequest

class Mouthshutbrowse(JuicerSpider):
    name = "mouthshut_browse"
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(Mouthshutbrowse, self).__init__(*args, **kwargs)
        self.browse_list = ['Apollo hospitals', 'apollo']
        self.search_url = "https://www.mouthshut.com/search/prodsrch.aspx?data=%s&type=&p=0"
        self.search = kwargs.get('search', 'Apollo Hospitals')
        self.domain = "https://www.mouthshut.com"
        for br in self.browse_list:
            self.start_urls.append(self.search_url%br)
        self.headers = { 
