import xlwt
import MySQLdb
import json
import datetime
import md5
from itertools import chain
import re
import os
import optparse
import csv
import collections

class Lifilepde(object):

    def __init__(self, *args, **kwargs):
        self.db_name     = options.db_name
        self.con = MySQLdb.connect(db   = self.db_name, \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd ='')
        self.cur = self.con.cursor()
        self.query2 = "select email, meta_data, crawl_status from fullcontact_crawl"
        self.list_tables1 = ['RichMedia','organizations', 'social_profiles']
        self.excel_file_name = 'fullcontact_data_%s.csv'%str(datetime.datetime.now().date())
        self.header_params = []
        oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        self.main()


    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def md5(self, x):
        return hashlib.md5(self.xcode(x)).hexdigest()

    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###').replace(u'\u2013','').strip()
        return text

    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',')
        return text

    def clean(self, text):
        if not text: return text
        value = text
        value = re.sub("&amp;", "&", value)
        value = re.sub("&lt;", "<", value)
        value = re.sub("&gt;", ">", value)
        value = re.sub("&quot;", '"', value)
        value = re.sub("&apos;", "'", value)

        return value

    def normalize(self, text):
        return self.clean(self.compact(self.xcode(text)))

    def compact(self, text, level=0):
        if text is None: return ''
        if level == 0:
            text = text.replace("\n", " ")
            text = text.replace("\r", " ")
        compacted = re.sub("\s\s(?m)", " ", text)
        if compacted != text:
            compacted = self.compact(compacted, level+1)
        return compacted.strip()
    

    def querydesign(self, tble, email, email_split, meta_data, inde):
        q2 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%(self.db_name, tble)
        self.cur.execute(q2)
        fields = self.cur.fetchall()
        fileds_list = list(fields)
        fil_list = list(chain.from_iterable(fileds_list))[2:-3]
        self.header_params.extend([tble])
        q9 = 'select * from %s where profile_sk="%s"'%(tble, email)
        self.cur.execute(q9)
        values = self.cur.fetchall()
        if not values:
            if '200' in meta_data:
                q9 = 'select * from %s where profile_sk="%s"'%(tble, email_split)
                self.cur.execute(q9)
                values = self.cur.fetchall()
        #if meta_data == '200' and not values: import pdb;pdb.set_trace()        
        final_to_update = []
        for val in values:
                vals_ = list(val)[2:-3]
                valf = filter(None, map(lambda a,b: (a+':-'+b) if b else '', fil_list,vals_))
                final_to_update.append(', '.join(valf))
        return ' <> '.join(final_to_update)



    def metadesign(self, table, email, email_split, meta_data, inde):
        q0 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%(self.db_name, table)
        #if "kochinkomedians@gmail.com" in email: import pdb;pdb.set_trace()
        self.cur.execute(q0)
        fields = self.cur.fetchall()
        fileds_list = list(fields)
        fil_list = list(chain.from_iterable(fileds_list))[1:-3]
        if inde == 0: self.header_params.extend(fil_list)
        q8 = 'select * from %s where sk="%s"'%(table, email)
        self.cur.execute(q8)
        values = self.cur.fetchall()
        if not values:
            if '200' in meta_data:
                q8 = 'select * from %s where sk="%s"'%(table, email_split)
                self.cur.execute(q8)
                values = self.cur.fetchall()
        if meta_data == '200' and not values: import pdb;pdb.set_trace()
        cntf_ = []
        if values:
                vals_ = map(lambda x:(x[1:-3]), values)
                cntf_ = list(chain.from_iterable(vals_))
        if len(cntf_) != len(fil_list):
                lnewln = len(fil_list) - len(cntf_)
                cntf_.extend(['']*lnewln)
        return cntf_



    def send_xls(self):
        counter = 0
        self.cur.execute(self.query2)
        records = self.cur.fetchall()
        sk_s_list = []
        for inde, rec in enumerate(records):
                values_final = []
                email = rec[0]
                email_split = email.split('@')[0] 
                sk_s_list.append(email_split)
                json_meta = rec[1]
                crawl_status = rec[2]
                status_url, data_avai = ['']*2
                if '<' and '>' in email:
                    email = ''.join(re.findall('<(.*?)>', email))
                #if 'kochinkomedians@gmail.com' in email: import pdb;pdb.set_trace()
                if crawl_status == 1:
                        data_avai = 'Available'
                        status_url = '200'
                else:
                        data_avai = 'Not Available'
                        status_url = str(json_meta)
                if inde == 0: self.header_params.extend(['Email', 'Data Flag', 'Status'])
                values_final.extend([email, data_avai, status_url])
                callfun3 = self.metadesign('profile_details', email, email_split, status_url, inde)
                values_final.extend(callfun3)
                for tabl in self.list_tables1:
                        callfun = self.querydesign(tabl, email, email_split, status_url, inde)
                        values_final.extend([callfun])
                if status_url == '200' and values_final[3] == '':
                    self.cur.execute('update fullcontact_crawl set crawl_status=11 where email="%s"'%email)
                values_final =  [self.normalize(i) for i in values_final]
                if inde == 0:
                        self.todays_excel_file.writerow(self.header_params)
                self.todays_excel_file.writerow(values_final)
                #print values_final
        duplicates = [item for item, count in collections.Counter(sk_s_list).items() if count > 1]
        """for dp in duplicates:
            self.cur.execute('select crawl_status from fullcontact_crawl where email like "%s"'%(dp+'@%'))
            import pdb;pdb.set_trace()
            records = self.cur.fetchall()
            print records
        self.cur.execute('select sk from profile_details where sk not like "%@%"')
        records = self.cur.fetchall()
        for rc in records:
            #print rc
            if rc[0] in duplicates:
                print rc"""
        
        self.con.close()

    def main(self):
        self.send_xls()
if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option('-d', '--db-name', default='', help = 'db-name')
        (options, args) = parser.parse_args()
        Lifilepde(options)




    

