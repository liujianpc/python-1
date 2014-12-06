__author__ = 'liyuhang'
#coding:utf-8
import urllib2,sys,json,re,urllib,os,re
import time as timer
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding('utf8')
print("进程ID为:"+str(os.getpid())+'\n')
def newwork():#新增加工作的界面爬
    f=open("log.text",'a')
    f.write("哪上班更新时间:"+str(timer.strftime('%Y-%m-%d %H:%M:%S', timer.localtime( timer.time() ) ))+"\n")
    f.close()
    url='http://www.nashangban.com/job_list?page='
    for i in range(1,31):
    	htmlhref=url+str(i)
    	html=urllib2.urlopen(htmlhref)
        htmlu=unicode(html.read(),'utf-8')
        d=pq(htmlu)
        works=d('.job-item')#工作
        for work in works:
        	data={}        	
        	workhref="http://www.nashangban.com"+pq(work).find('.title').attr('href')
       		#print workhref
       		workinfos=workinfo(workhref)
        	data['workinfo']=workinfos
        	companyhref="http://www.nashangban.com"+pq(work).find('.name').attr('href')
        	companyinfo=companysdeep(companyhref)
        	companyinfo['email']=workinfos['email']
        	data['companyinfo']=companyinfo
        	info=json.dumps(data,ensure_ascii=False)
        	#print info
        	postapi(info)
        	timer.sleep(3)

        	#print companyhref

def workinfo(url):#进url里面爬 工作详情
    html=urllib2.urlopen(url)
    htmlu=unicode(html.read(),'utf-8')
    d=pq(htmlu)
    work=d('.job-info')#职位信息主体
    job=pq(work).find('h3').text()#职位名称
    #print job
    location=d('.location').find('b').text()
    #print("location "+location)
    kind=d('.type').find('b').text()
    #print("type "+kind)
    salary=d('.salary-start').find('b').text()
    #print salary
    jobdescription=d('.job-describe').text()
    #print('describe '+jobdescription)
    host=d('.company-domain').text()
    #print('host '+host)
    job_publisher_name=d('.job-publisher-name').text()
    #print("publisher "+job_publisher_name)
    workinfos={
        "job":job,#jobname
        "salary":salary,#salary
        "jobspace":location,#location
        "location":location,
        "experience":"",
        "education":"",
        "type":kind,#type
        "condition":"",
        "jobdescription":jobdescription,#description
        "email":host,#hostemail
        "lagouwork":url,#nashangban
        #"job-publisher":job_publisher_name#pulisher         
    }
    return workinfos

def companysdeep(url):
    html=urllib2.urlopen(url)
    htmlu=unicode(html.read(),'utf-8')
    d=pq(htmlu)
    companyinfo={}
    tags=d('.specialties ul li')
    companyinfo['tags']=[]
    for tag in tags:
    	companyinfo['tags'].append(pq(tag).text())   
    companyinfo['oneword']=""
    name=d('.company-head h2 .fullname').text()
    companyinfo['name']=name
    #print name
    href=d('.company-head .website a').attr('href')
    companyinfo['href']=href
    #print href
    logo=d('.company-head .logo img').attr('src')
    companyinfo['logo']=logo
    #print logo
    size=d('.company-head .size').text()
    #companyinfo['size']=size规模
    #print size
    location=d('.company-head .location').text()
    companyinfo['location']=location
    #print location
    foundtime=d('.company-head .found-time').text()
    #print foundtime
    pattern=re.compile(r'(\d*)')
    date=pattern.findall(foundtime)
    foundtime=""
    for i in range(0,len(date)):
    	foundtime=foundtime+str(date[i])
    	if i==3:
    		foundtime=foundtime+'-'
    	if i==len(date)-1:
    		foundtime=foundtime+'-01'
    #print foundtime
    companyinfo['foundtime']=foundtime
    #print foundtime
    positions=d('.specialties li')
    #print("length: "+str(positions.length))
    companyinfo['position']=[]
    for i in positions:
    	#print pq(i).text()
    	companyinfo['position'].append(pq(i).text())
    lingyu=','.join(companyinfo['position'])
    description=d('.intro article').text()
    companyinfo['introduce']=description
    #print description
    boss=d('.memver-content .name').text()
    #companyinfo['boss']=boss
    #print boss
    boss_title=d('.memver-content .title').text()
    #companyinfo['boss_title']=boss_title
    #print boss_title
    member=[{'name':boss,'position':boss_title,'intro':''}]
    finance=d('.finance li .time')
    remove=pq(finance).find('.time').remove()
    finance=pq(finance).text()
    companyinfo['finance']=finance
    #print finance
    companyinfo['lagoucompany']=url
    about=[location,lingyu,size]
    companyinfo['about']=about
    companyinfo['member']=member
    companyinfo['product']={}
    return companyinfo
def postapi(jsons):
    url="http://www.fengniaor.com/api.php"
    value={"action":"auto_add_company_job","data":jsons}
    data=urllib.urlencode(value)
    req=urllib2.Request(url=url,data=data)
    html=urllib2.urlopen(req).read()
    #print(html)



newwork()
