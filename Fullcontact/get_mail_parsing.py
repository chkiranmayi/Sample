import MySQLdb
import datetime
import os
import openpyxl as px
import glob
import md5
import hashlib
import json
import re

def xcode(text, encoding='utf8', mode='strict'):
    return text.encode(encoding, mode) if isinstance(text, unicode) else text

def md5(x):
    return hashlib.md5(xcode(x)).hexdigest()

def replacefun(text):
    text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###').replace(u'\u2013','').strip()
    return text

def restore(text):
    text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',')
    return text

def clean(text):
    if not text: return text
    value = text
    value = re.sub("&amp;", "&", value)
    value = re.sub("&lt;", "<", value)
    value = re.sub("&gt;", ">", value)
    value = re.sub("&quot;", '"', value)
    value = re.sub("&apos;", "'", value)

    return value

def normalize(text):
    return clean(compact(xcode(text)))

def compact( text, level=0):
    if text is None: return ''
    if level == 0:
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
    compacted = re.sub("\s\s(?m)", " ", text)
    if compacted != text:
        compacted = compact(compacted, level+1)
    return compacted.strip()


class Linkedinparsing(object):

    def __init__(self):
        self.con = MySQLdb.connect(db='FULLCONTACTDB',
        user='root', passwd='',
        charset="utf8", host='localhost', use_unicode=True)
        self.cur = self.con.cursor()
        self.social_processing_path = '/home/kiranmayi/fb/fb/spiders/excelfiles'
        self.query = 'insert into fullcontact_crawl(sk, email, content_type ,crawl_status,created_at, modified_at) values("%s", "%s", "%s", "%s",now(), now()) on duplicate key update modified_at=now()'

    def __del__(self):
        self.cur.close()
        self.con.close()

    def rep_spl(self, var):
            """To remove unwanted characters"""
            var = str(var).replace('\r', '').replace('\n', '')\
            .replace('\t', '').replace(u'\xa0', '').replace(u'\xc2\xa0', '').replace(u'\xc3\u0192\xc2\xb1',' ').strip()
            if 'none' in var.lower():
                var = ''
            return var

    def main(self):
        sk_list = []
        files_list = glob.glob(self.social_processing_path+'/*.xlsx')
        if files_list:
            for _file in files_list:
                ws_ = px.load_workbook(_file, read_only=True)
                sheet_list = ws_.get_sheet_names()
                for xl_ in sheet_list:
                    sheet_ = ws_.get_sheet_by_name(name=xl_)
                    row_check = 0
                    email_address = linkedin_profile = ida = firstname = lastname = key_ = 0
                    for row in sheet_.iter_rows():
                        mls_list = []
                        for i in row:
                            if i.value:
                                mls_list.append(i.value.strip())
                        for mails in mls_list:
                            vals = (md5(mails), mails, "fulcontact", 0)
                            if md5(mails) in sk_list:
                                print mails
                            sk_list.append(md5(mails))
                            self.cur.execute(self.query%vals)
                            
                        #if len(mls_list)>1: print mls_list
                        
if __name__ == '__main__':
    Linkedinparsing().main()

