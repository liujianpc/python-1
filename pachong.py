__author__ = 'liyuhang'
#coding:utf-8
import urllib,urllib2,cookielib,sys,random,re
reload(sys)
sys.setdefaultencoding('utf8')

url="http://rs.xidian.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
value={"cookietime":"2592000","username":"柒染","password":"e2fa0937aa136df5818418d9a5c31fc4","quickforward":"yes","handlekey":"ls"}
data=urllib.urlencode(value)

headers={"Origin":"http://rs.xidian.edu.cn","Referer":"http://rs.xidian.edu.cn/forum.php","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"}
req=urllib2.Request(url=url,data=data,headers=headers)
cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

response=opener.open(req)#登陆成功
for lsl in cj:
    print lsl
#print response.read().encode("utf-8")验证登陆成功
def shuitie(opener,url,timelate,pagenumber,message):
    judege=True
    alltitle=[]
    while(judege):
        judege=False
        #number=random.randint(646,5000)
        number=2692
        url_open=url+"64"+str(number)
        response=opener.open(url_open).read().encode("utf-8")
        response=opener.open("http://rs.xidian.edu.cn/forum.php?mod=viewthread&tid=667320").read().encode('utf-8')
        #print response
        fid=re.findall("ptm\s*pnpost.*?fid=(\d*)",response,re.S)#获取当前页面的fid
        fid="72"
        formhash=re.findall('formhash=(.*?)">退出',response,re.S)[0]
        print formhash
        title=re.findall("<title>(.*?)</title>",response,re.S)#title
        print title[0]
        if(len(title)==1):
            alltitle.append(title[0])
        data={"message":message,"formhash":formhash,"usesig":"1","subject":"  "}
        data=urllib.urlencode(data)
        # if(len(fid)==1):
        #     fid=fid[0]
        # else:
        #     continue
        #tid="64"+str(number)
        tid="667320"
        #requestURL="http://rs.xidian.edu.cn/forum.php?mod=post&action=reply&fid="+fid+"&tid="+tid+"&extra=&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
        requestURL="http://rs.xidian.edu.cn/forum.php?mod=post&action=reply&fid=13&tid=667320&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
        print requestURL
        req=urllib2.Request(headers=headers,url=requestURL,data=data)
        response=opener.open(req).read().encode("utf-8")
    #print(alltitle[0])



shuitie(opener,"http://rs.xidian.edu.cn/forum.php?mod=viewthread&tid=",11,1,"MARK,下下来看看..")
the_page=response.read().decode("utf-8")

