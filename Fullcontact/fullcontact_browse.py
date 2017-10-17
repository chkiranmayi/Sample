import requests
import json
import MySQLdb
from db_operations import *
from constants import *
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
import md5

class Fullcontact(BaseSpider):
    name = "fullcontact_browse"
    start_urls = ['https://portal.fullcontact.com/']
    handle_http_status_list = ['302']
    def __init__(self, *args, **kwargs):
        super(Fullcontact, self).__init__(*args, **kwargs)
        self.search_url = 'https://api.fullcontact.com/v2/person.json?email=%s'
        #self.listt = 'Full contact'
        #self.listt =  kwargs.get('check', self.listt)
        #self.listt = self.listt.split(',')
        self.con = MySQLdb.connect(db   = 'FULLCONTACTDB', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root')
        self.cur = self.con.cursor()
        get_query_param = "select sk, email, meta_data from fullcontact_crawl where crawl_status=0 and meta_data is not Null limit 1"
        self.cur.execute(get_query_param)
        self.mails = [i for i in self.cur.fetchall()]
        #for br in self.listt:
            #self.mails.append(br)

    def __del__(self):
        self.con.close()
        self.cur.close()

    def parse(self, response):
        sel = Selector(response)
        for i in self.mails:
            sk_ = i[0]
            meta_data = i[2]
            params = (
              ('email', i[1]),
            )
            headers_contact.update({'X-FullContact-APIKey':'a2f122ddaed0c1a6'})
            ty = requests.get(api_url, headers=headers_contact, params=params)
            data = json.loads(ty.text)
            sk = i[1].split('@')[0]
            social_profiles = data.get('socialProfiles')
            if social_profiles:
                self.parse_socialprofiles(sk, social_profiles)
            organizations = data.get('organizations', '')
            if organizations:
                self.parse_organizations(sk, organizations)
                ####contacts Info#####
            x = data.get('contactInfo', {})
            given_name = x.get('givenName', '')
            full_name = x.get('fullName', '')
            family_name = x.get('familyName', '')
            websites = x.get('websites', '')
            dg = data.get('demographics', {})
            dgg = dg.get('locationDeduced', {})
            city = dgg.get('city', {}).get('name', '')
            state = dgg.get('state', {}).get('name', '')
            country  = dgg.get('country', {}).get('name', '')
            continent = dgg.get('continent', {}).get('name', '')
            location = dgg.get('normalizedLocation', '')
            likelihood = data.get('likelihood', '')
            gender = dg.get('gender', '')
            age = dg.get('age', '')
            if websites:
                websites = '<>'.join([i.get('url') for i in websites])
            values = (sk, full_name, family_name, websites, 
            age, gender, state, city, country, location, continent, likelihood)
            self.cur.execute(profile_details_query, values)
            photos = data.get('photos')
            if photos:
                self.parse_photos(sk, photos)
            self.cur.execute(update_get_params%(1,sk_))

    def parse_photos(self, sk, photos):
        for ph in photos:
                ph_url, ph_type = ph.get('url'), ph.get('typeId')
                values3 = (md5.md5('{}{}'.format(ph_url, sk)).hexdigest(), sk, ph_type, ph_url)
                self.cur.execute(profile_richmedia_query, values3)

    def parse_organizations(self, sk, organizations):
        for org in organizations:
            org_name, org_start, org_end, org_title = org.get('name', ''), org.get('startDate', ''), org.get('endDate', ''),org.get('title', '')
            current = org.get('current', '')
            values2 = (md5.md5('{}{}{}'.format(org_title, sk,org_name)).hexdigest(), sk, org_name, org_title, current, org_start, org_end)
            self.cur.execute(organizations_query, values2)

    def parse_socialprofiles(self, sk, social_profiles):
        for i in social_profiles:
            type_name, user_name, p_url = i.get('typeName'), i.get('username', ''), i.get('url')
            type_id, followers = i.get('typeId'), i.get('followers', '')
            values1 = (md5.md5('{}{}{}'.format(type_id, p_url, sk)).hexdigest(), sk, user_name, '', type_name, followers, p_url)
            self.cur.execute(social_profiles_query, values1)

