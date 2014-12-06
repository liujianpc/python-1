__author__ = 'liyuhang'
#coding:utf-8
import urllib2,sys,json,re,urllib,os,re
import time as timer
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding('utf8')
print("进程ID为:"+str(os.getpid())+'\n')
def newwork():
    f=open("log.text",'a')
    f.write("更新时间:"+str(timer.strftime('%Y-%m-%d %H:%M:%S', timer.localtime( timer.time() ) ))+"\n")
    f.close()
    url='http://www.neitui.me/neitui/type=all&page='
    for i in range(1,31):
        htmlhref=url+str(i)+'.html'
        #print(htmlhref)
        html=urllib2.urlopen(htmlhref)
        htmlu=unicode(html.read(),'utf-8')
        d=pq(htmlu)
        #print d.html()
        works=d('.jobinfo')
        #print works.html()
        for work in works:
            data={}
            #print pq(work).html()
            workhref="http://www.neitui.me"+pq(work).find('.jobnote-l a').attr('href')
            #print workhref
            #workinfo(workhref)
            companyhref="http://www.neitui.me"+pq(work).find('.jobnote-r a').attr('href')
            print companyhref
            companysdeep(companyhref)
def workinfo(url):
    html=urllib2.urlopen(url)
    htmlu=unicode(html.read(),'utf-8')
    d=pq(htmlu)
    workinfos={}
    info=d('.padding-r10')
    job=info.eq(0).text()
    workinfos['job']=job
    print ('job: '+job)
    salary=info.eq(1).text()[1:len(info.eq(1).text())-1]
    workinfos['salary']=salary
    print ('salary: '+salary)
    experience=info.eq(2).text()[1:len(info.eq(2).text())-1]
    workinfos['experience']=experience
    print ('experience: '+experience)
    location=d('.jobtitle-r').text()[3:]
    workinfos['location']=location
    print ('location: '+location)
    tags=d('.company_tag')
    print tags.length
    workinfos['tag']=[]
    for tag in tags:
    	workinfos['tag'].append(pq(tag).find('.content').text())
    	print ('tag: '+pq(tag).find('.content').text())
    description=d('.jobdetail').text()
    workinfos['description']=description
    print ('description: '+description)
    job_publisher_name=d('.jobnote .defaulta').text()
    print ('publisher: '+job_publisher_name)
    pattern=re.compile("(?:\((.*?)\))")#正则取出邮箱
    host=pattern.search(d('.jobnote').eq(0).text()).group(1).replace(" ",'')
    workinfos['host']=host
    print('host: '+host)
    return workinfos
def companysdeep(url):
    html=urllib2.urlopen(url)
    htmlu=unicode(html.read(),'utf-8')
    d=pq(htmlu)
    companyinfo={}
    name=d('.company_name h3 span').remove('a')text()
    companyinfo['name']=name
    print('name: '+name)
    href=d('.company_name h3 a').attr('href')
    companyinfo['href']=href
    print('href: '+href)
    logo=d('.img_inner img').attr('src')
    companyinfo['logo']=logo
    print('logo: '+logo)
    location=d('.company_des_item').eq(0).find('span').eq(1).text()
    companyinfo['location']=location
    print('location: '+location)
    position=d('.company_des_item').eq(1).find('span').eq(1).text()
    companyinfo['position']=position
    print('position: '+position)
    size=d('.company_des_item').eq(2).find('span').eq(1).text()
    companyinfo['size']=size
    print('size: '+size)
    finance=d('.company_des_item').eq(3).find('span').eq(1).text()
    companyinfo['finance']=finance
    print('finance: '+finance)
    tags=d('.company_tag')
    companyinfo['tag']=[]
    for tag in tags:
        companyinfo['tag'].append(pq(tag).find('.content').text())
        print('tag: '+pq(tag).find('.content').text())
    #description=d('.jobdetail').text()主要问题
   # print('description: '+description)
    #companyinfo['description']=description
    boss=d('.ceo').text()
    print("boss: "+boss)
    bosstitle=d('.ceo span').text()
    print('bosstitle: '+bosstitle)
    companyinfo['boss']=boss
    companyinfo['bosstitle']=bosstitle
    return companyinfo
newwork()


