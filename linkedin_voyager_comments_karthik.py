import os
import scrapy
import re
import json
import csv
import datetime
import requests
import time
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from collections import OrderedDict
from generic_functions import * 

class Linkedinvoyagercomments(scrapy.Spider):
	name = "linkedinapivoyager_comments_karthik"
	allowed_domains = ["linkedin.com"]
	start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)

	def __init__(self, *args, **kwargs):
		super(Linkedinvoyagercomments, self).__init__(*args, **kwargs)
                self.login = kwargs.get('login', 'raja')
		self.logins_dict = {'raja':['rajaqx@gmail.com','']}
                self.profiles_list = ['https://www.linkedin.com/company/18073064/']
		self.url3 = 'https://www.linkedin.com/pulse-fe/api/v1/comments?urn='
		self.url4 = '&start=0&count='
		self.url5 = '&sort=REV_CHRON'
		self.filename = "LINKEDIN_COMPANY_COMMENTS.csv"
	        self.csv_file = self.is_path_file_name(self.filename)
		self.fields = ["post_id", "post_no_of_comments", "post_no_of_likes", "post_image_url", "post_description", "post_url", "post_company_name", "post_company_logo", "post_created_at_time", "comment_by", "comment_datetime", "commenter_by_image", "commenter_by_public_url", "comment_description", "commenter_headline", "comment_total_likes", "reply_by", "reply_datetime", "replier_by_image", "replier_by_public_url", "reply_text", "replier_headline", "reply_total_likes", "reply_count"]
		self.csv_file.writerow(self.fields)
		#self.profiles_list = ['https://www.linkedin.com/company/godigit/']
                dispatcher.connect(self.spider_closed, signals.spider_closed)
                self.domain = "https://www.linkedin.com"

	def parse(self, response):
                sel = Selector(response)
                logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
		csrf_token = ''.join(sel.xpath('//input[@id="csrfToken-login"]/@value').extract())
                source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())
		if self.profiles_list:
			login_account = self.logins_dict[self.login]
			account_mail, account_password = login_account
			return [FormRequest.from_response(response, formname = 'login_form',\
				formdata={'session_key':account_mail,'session_password':account_password,'isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next, meta={'csrf_token':csrf_token})]

	def is_path_file_name(self, excel_file_name):
		if os.path.isfile(excel_file_name):
    			os.system('rm %s' % excel_file_name)
		oupf = open(excel_file_name, 'ab+')
		todays_excel_file = csv.writer(oupf)
		return todays_excel_file

    	def spider_closed(self, spider):
		cv = requests.get('https://www.linkedin.com/logout/').text

	def parse_next(self, response):
                sel = Selector(response)
                cooki_list = response.request.headers.get('Cookie', [])
                li_at_cookie = ''.join(re.findall('li_at=(.*?); ', cooki_list))
                headers = {
                    'cookie': 'li_at=%s;JSESSIONID="%s"' % (li_at_cookie, response.meta['csrf_token']),
                    'x-requested-with': 'XMLHttpRequest',
                    'csrf-token': response.meta['csrf_token'],
                    'authority': 'www.linkedin.com',
                    'referer': 'https://www.linkedin.com/',
                }
                for li in self.profiles_list:
			api_compid_url = 'https://www.linkedin.com/voyager/api/feed/updates?companyId=%s&q=companyFeed' %(li.strip().strip('/').split('/')[-1])
                	yield Request(api_compid_url, callback = self.parse_correct, meta = {
                	    'csrf_token': response.meta['csrf_token'], 'headers':headers, 'api_url':api_compid_url
	                }, headers = headers)

	def parse_correct(self, response):
                data = json.loads(response.body)
		api_basic_url = response.meta.get('api_url', '')
		headers = response.meta.get('headers', {})
		data_elements = data.get('elements', [])
		for datae in data_elements:
			desci_list, descii_list = {}, []
			desc_list = datae.get('value', {}).get('com.linkedin.voyager.feed.ShareUpdate', {}).get('content', {})
			desc_kys = desc_list.keys()
			if desc_kys:
				desci_list = desc_list.get(desc_kys[0], {})
			descii_list = desci_list.get('text', {}).get('values', [])
			desc_fi = []
			for de in descii_list:
				desc_ = de.get('value', '')
				desc_fi.append(desc_)
			post_desc_fi = ' '.join(desc_fi)
			post_url = datae.get('permalink', '')
			post_id = datae.get('id', '')
			post_urn = datae.get('urn', '')
			if post_id:
				post_id = post_id.split(':')[1]
			post_social_at = datae.get('socialDetail', {}).get('totalSocialActivityCounts', {})
			post_nu_of_comments = post_social_at.get('numComments', '')
			post_nu_of_likes = post_social_at.get('numLikes', '')
			#post_image = desci_list.get('originalImage', {}).get('string', '')
			post_image = desci_list.get('image', {}).get('com.linkedin.voyager.common.MediaProxyImage',{}).get('url', '')
			post_info_share = datae.get('value', {}).get('com.linkedin.voyager.feed.ShareUpdate', {})
			post_by_info = post_info_share.get('actor', {}).get('com.linkedin.voyager.feed.CompanyActor', {}).get('miniCompany', {})
			post_company_name = post_by_info.get('name', '')
			post_company_logo = post_by_info.get('logo', {}).get('com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
			if post_company_logo:
				post_company_logo = post_image =  "%s%s" % ("https://media.licdn.com/media", post_company_logo)
			post_created_at_time = post_info_share.get("createdTime", '')
			if post_created_at_time:
				post_created_at_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(post_created_at_time)/1000))
			dict_ = [post_id, post_nu_of_comments, post_nu_of_likes, post_image, post_desc_fi, post_url, post_company_name, post_company_logo, post_created_at_time]
			if post_nu_of_comments != 0:
				comments_url = "%s%s%s%s%s"%(self.url3, post_urn, self.url4, '20', self.url5)
				comment_basic_url = "%s%s%s" % (self.url3, post_urn, self.url5)
				yield Request(comments_url, callback=self.parse_comments, meta= {"dict_":dict_, "comment_basic_url":comment_basic_url})
			else:
				fina = dict_+['' for i in range(15)]
				fina = [normalize(str(i)) for i in fina]
				self.csv_file.writerow(fina)
				
			
		url_paging  = data.get('paging',[])
		if url_paging:
			count_data = url_paging.get('count','')
			start_data = url_paging.get('start','')
			total_data = url_paging.get('total','')
			if total_data > count_data+start_data:
				cons_part = ''
				if '?' not in api_basic_url:
					cons_part = "?count=%s&start=%s"%(count_data, start_data+count_data)
				else:
					cons_part = "&count=%s&start=%s"%(count_data, start_data+count_data)
				retrun_url = "%s%s"%(api_basic_url,cons_part)
				yield Request(retrun_url, headers=headers, callback=self.parse_correct, meta={'api_url':api_basic_url, 'headers':headers})
	def parse_comments(self, response):
		dict_post_keys = response.meta.get('dict_', [])
		comment_basic_url = response.meta.get('comment_basic_url', '')
		sel = json.loads(response.body)
		elements = sel.get('elements', [])
		for element in elements:
		    created_date = str(element.get('createdDate',''))
		    if created_date:
			created_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(created_date)/1000))
		    urn = element.get('urn','')
		    all_likes = element.get('viewAllLikesUrl','')
		    total_likes = str(element.get('totalLikes',''))
		    message = element.get('message','')
		    commenter = element.get('commenter',{})
		    commenter_member_urn = commenter.get('urn','')
		    commenter_image = commenter.get('image',{}).get('url','')
		    commenter_public_profile_url = commenter.get('publicProfileUrl','')
		    commenter_name = commenter.get('name','')
		    commenter_headline = commenter.get('headline','')
		    commenter_member_token = commenter.get('memberToken','')
		    nested_comment_count = str(element.get('nestedCommentCount',''))
		    nested_nodes = element.get('nestedComments',{}).get('elements',[])
		    dict_comments = dict_post_keys + [commenter_name, created_date, commenter_image, commenter_public_profile_url, message,  commenter_headline,  total_likes]
		    if not nested_nodes:
			dict_comments.extend(['' for i in range(8)])
			dict_comments = [normalize(str(i)) for i in dict_comments]
			self.csv_file.writerow(dict_comments)
		    for nest in nested_nodes:
			reply_urn = nest.get('urn','')
			reply_all_likes = nest.get('viewAllLikesUrl','')
			reply_created_date = str(nest.get('createdDate',''))
			if reply_created_date:
			    reply_created_date = created_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(reply_created_date)/1000))
			reply_message = nest.get('message','')
			rcn = nest.get('commenter',{})
			reply_commenter_urn = rcn.get('urn','')
			reply_commnter_image = rcn.get('image',{}).get('url','')
			reply_public_profile = rcn.get('publicProfileUrl','')
			reply_name = rcn.get('name','')
			reply_headline = rcn.get('headline','')
			reply_member_token = rcn.get('memberToken','')
			reply_like_count = str(nest.get('totalLikes',''))
			reply_totla_comment = str(nest.get('nestedCommentCount',''))
			list_replies = [reply_name, reply_created_date, reply_commnter_image, reply_public_profile, reply_message,reply_headline,  reply_like_count, reply_totla_comment]
			dict_comments.extend(list_replies)
			dict_comments = [normalize(str(i)) for i in dict_comments]
			self.csv_file.writerow(dict_comments)
			del dict_comments[-8:]

                url_paging  = sel.get('paging',[])
                if url_paging:
                        count_data = url_paging.get('count','')
                        start_data = url_paging.get('start','')
                        total_data = url_paging.get('total','')
                        if total_data > count_data+start_data:
                                cons_part = ''
                                if '?' not in comment_basic_url:
                                        cons_part = "?count=%s&start=%s"%(count_data, start_data+count_data)
                                else:
                                        cons_part = "&count=%s&start=%s"%(count_data, start_data+count_data)
                                retrun_url = "%s%s"%(comment_basic_url,cons_part)
                                yield Request(retrun_url, callback=self.parse_comments,meta= {"dict_":dict_post_keys, "comment_basic_url":comment_basic_url} )

