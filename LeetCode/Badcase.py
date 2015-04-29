# -*- coding:utf8 -*-
from bs4 import BeautifulSoup
from math import radians, cos, sin, asin, sqrt
import urllib
import urllib2
import cookielib
import xlwt
import xlrd
import re

class Badcase:

    def __init__(self):
        self.page_links = set()
        self.p1_4_text = re.compile('定位数据有偏差，我们将在一周内对数据做更新，谢谢反馈！')
        self.p5_miss = re.compile('上报定位数据不完整，我们会关注您的问题，请今后注意正确操作步骤，准确报告您的问题，谢谢！')
        self.p5_single = re.compile('周边环境WiFi热点少，为了提高定位准确性，请使用GPS提高定位精度！')
        self.p5_100m = re.compile('定位在技术误差允许范围内，今后我们会努力进一步提高定位精度，谢谢反馈！')
        self.p5_disconnect = re.compile('定位请求未发送到服务器，请检查网络是否正确连接！')
        self.p5_text = [self.p5_miss, self.p5_single, self.p5_100m, self.p5_disconnect]
        self.fdbk_text = dict(zip(['P1', 'P2', 'P3', 'P4', 'P5'],
                                  [self.p1_4_text, self.p1_4_text, self.p1_4_text, self.p1_4_text, self.p5_text]))
        self.p_sum = dict(zip(['P1', 'P2', 'P3', 'P4', 'P5', 'Error'], [0, 0, 0, 0, 0, 0]))
        self.error_rea = dict()

    def adam_login(self):
        cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        postdata=urllib.urlencode({ 'username':'weisheng.tang','password':'o0lij3r@dk3poj'})
        req = urllib2.Request(
                url = 'http://adam.autonavi.com/login',
                data = postdata
                )
        result = urllib2.urlopen(req)

    # def page_loop(self):
    #     operator = "史银龙"
    #     self.adam_login()
    #     print 'Beginning detail page links collecting'
    #     for p in xrange(1, 641):
    #         url = 'http://adam.autonavi.com/J1/list/main?page_size=100&status=7&model_id=101,102&page_no=%s' % p
    #         content = urllib2.urlopen(url)
    #         soup = BeautifulSoup(content)
    #         result_rows = soup.find('table', class_='sort').tbody
    #         rowlist = result_rows.find_all('tr')
    #         listsize = len(rowlist)
    #         for r in xrange(listsize):
    #             row = rowlist[r]
    #             tag = row.find_all('td')
    #             if tag[4]['data-val-team'].encode('utf-8') == operator:
    #                 report_link = tag[2].a.get("href")
    #                 self.page_links.add(report_link)
    #     print 'Detail page links collecting finished'

    def page_parser(self):
        u_gps = re.compile(
            '\xe7\x94\xa8\xe6\x88\xb7\xe6\x89\x80\xe5\x9c\xa8\xe4\xbd\x8d\xe7\xbd\xae\xef\xbc\x9a(-?\d+\.\d+)\s+(-?\d+\.\d+)')
        gps_intel = re.compile('\xe5\x9d\x90\xe6\xa0\x87\xe4\xbf\xa1\xe6\x81\xaf\xef\xbc\x9a(-?\d+\.\d+),(-?\d+\.\d+)')
        u_gps_miss = re.compile(
            '\xe7\x94\xa8\xe6\x88\xb7\xe6\x89\x80\xe5\x9c\xa8\xe4\xbd\x8d\xe7\xbd\xae\xef\xbc\x9a\s+')
        gps_intel_miss = re.compile('\xe5\x9d\x90\xe6\xa0\x87\xe4\xbf\xa1\xe6\x81\xaf\xef\xbc\x9a\s+')
        badcase_auth = re.compile('定位问题自动处理系统')
        self.adam_login()
        print 'Beginning detail page parse'
        count = 0
        print len(self.page_links)
        for plink in self.page_links:
            p_level = ''
            miss_flag = False
            de_distance = 0
            try:
                p_cont = urllib2.urlopen(plink)
            except urllib2.URLError,e:
                print "Can't open %s" % plink
                continue
                print 'continue'
            gps_coord = ''
            p_soup = BeautifulSoup(p_cont)
            gps_sec = p_soup.find('div', class_='detail').find_all('section')
            de_desc = p_soup.get_text().encode('utf-8')
            de_stat = p_soup.find('ul', class_='info').find_all('li')[5].get_text().encode('utf-8')
            gps_text = gps_sec[1].p.get_text().encode('utf-8')
            if not re.search(badcase_auth,de_desc):
                continue
            if re.search(u_gps_miss, gps_text) or re.search(gps_intel_miss, gps_text):
                p_level = 'P5'
                miss_flag = True
            else:
                u_coord = re.search(u_gps, gps_text)
                g_coord = re.search(gps_intel, gps_text)
                de_distance = self.gps_distance(u_coord.group(1), u_coord.group(2), g_coord.group(1), g_coord.group(2))
                p_level = self.p_level_judge(de_distance)
            self.p_fdbk_judge(miss_flag,p_level,de_desc,de_stat,de_distance,plink,count)
            count += 1
            if count % 1000 == 0:
                break
        print 'Detail page parse finished'

    def gps_distance(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1 = float(lon1)
        lat1 = float(lat1)
        lon2 = float(lon2)
        lat2 = float(lat2)
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        m = 6367000 * c
        return m

    def p_level_judge(self, distance):
        if distance < 100:
            return 'P5'
        elif 100 <= distance < 500:
            return 'P4'
        elif 500 <= distance < 1000:
            return 'P3'
        elif 1000 <= distance < 5000:
            return 'P2'
        elif distance >= 5000:
            return 'P1'

    def p_fdbk_judge(self,miss_flag,p_level,desc,stat,distance,plink,count):
        error_reason = ''
        if re.search(p_level, stat):
            if p_level == 'P5':
                if miss_flag and not re.search(self.fdbk_text['P5'][0],desc):
                    error_reason = '%s//P5//描述有误//' % count
                    self.p_sum['Error'] += 1
                    self.error_rea[error_reason] = plink
                    return
                if distance >= 100 and not re.search(self.fdbk_text['P5'][2],desc):
                    error_reason = '%s//P5//描述有误' % count
                    self.p_sum['Error'] += 1
                    self.error_rea[error_reason] = plink
                    return
            elif not re.search(self.fdbk_text[p_level], desc):
                error_reason = '%s//%s//描述有误' % (count,p_level)
                self.p_sum['Error'] += 1
                self.error_rea[error_reason] = plink
                return
            self.p_sum[p_level] += 1
        else:
            err_stat = re.search('\s+P\d',stat).group(0)
            error_reason = '%s//%s//%s//定级有误' % (count,err_stat, p_level)
            self.p_sum['Error'] += 1
            self.error_rea[error_reason] = plink
            return

    def table_report(self):
        print 'Beginning write report'
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'SimSun'    # 指定“宋体”
        style.font = font
        try:
            wbk = xlwt.Workbook(encoding='utf-8')
            sum_sheet = wbk.add_sheet('总体统计')
            error_sheet = wbk.add_sheet('错误统计')
            level = ['P1','P2','P3','P4','P5','Error']
            error_sheet.write(0,0,'原因',style)
            error_sheet.write(0,1,'详情页链接',style)
            for i in range(6):
                sum_sheet.write(i,0,level[i],style)
                sum_sheet.write(i,1,self.p_sum[level[i]],style)
            row_order = 1
            for key in self.error_rea:
                error_sheet.write(row_order,0,key,style)
                error_sheet.write(row_order,1,self.error_rea[key],style)
                row_order += 1
            wbk.save('Badcase_report.xls')
        except StandardError, e:
            print e
        print 'Writing finished!'

    def tablelink_read(self):
        rpt = xlrd.open_workbook('Badcase_links.xls','utf-8')
        links = rpt.sheet_by_name('links').col_values(0)
        self.page_links = set(links)

if __name__=="__main__":
    spider = Badcase()
    spider.tablelink_read()
    spider.page_parser()
    spider.table_report()