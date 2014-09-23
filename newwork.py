__author__ = 'liyuhang'
#coding:utf-8
import urllib2,sys,json,time
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding('utf8')
lasthref=''
def newwork():
    f=open("works.text",'a')
    global lasthref
    url='http://www.lagou.com/jobs/list_?city=%E5%85%A8%E5%9B%BD&pn='
    beginbloon=True#是否第一次爬
    begin=None#存这次爬到的第一个
    for i in range(1,31):
        htmlhref=url+str(i)
        html=urllib2.urlopen(htmlhref)
        htmlu=unicode(html.read(),'utf-8')
        d=pq(htmlu)
        works=d('.clearfix')
        for work in works:
            workhref=pq(work).children('div').eq(0)
            href=workhref.find('a').attr('href')
            if(beginbloon):
                begin=href#抓的最近一次的href
                beginbloon=False
            elif(href==lasthref):
                lasthref=begin
                return
            span=workhref.find('span')
            time=span.eq(len(span)-1).text()
            worksinfo=json.dumps(workinfo(href),ensure_ascii=False,indent=4)
            f.write(worksinfo)
            # print worksinfo
            # print href
            # print time
        print htmlhref
    f.close()
#

def workinfo(url):#进url里面爬
    html=urllib2.urlopen(url)
    htmlu=unicode(html.read(),'utf-8')
    d=pq(htmlu)
    job=d('.job_detail h1').attr('title')
    print job
    p=d('.job_request span')
    salary=p.eq(0).text()
    didian=p.eq(1).text()
    jingyan=p.eq(2).text()
    xueli=p.eq(3).text()
    leixing=p.eq(4).text()
    # youhuo=d('.job_request').chiltren('span').remove()
    # print youhuo.html()
    youhuo=d('.job_request').text()
    job_bt=d('.job_bt')
    jobdescription=job_bt.text()#职位描述
    jobspace=d('.job_company').find("div").text()
    href=d('.c_feature').find('a').attr('href')
    workinfos={
        "job":job,
        "salary":salary,
        "jobspace":jobspace,
        "didian":didian,
        "jingyan":jingyan,
        'xueli':xueli,
        "leixing":leixing,
        "youhuo":youhuo,
        "jobdescription":jobdescription,
        'href':href,
    }
    return workinfos

while(True):
    print "咕叽咕叽~~~"
    newwork()
    print "巴拉巴拉~~~"
    time.sleep(30*60)





