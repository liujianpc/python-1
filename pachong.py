__author__ = 'liyuhang'
#coding:utf-8
import urllib,urllib2,cookielib,sys,random,re,time
reload(sys)
sys.setdefaultencoding('utf8')

url="http://rs.xidian.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
value={"cookietime":"2592000","username":"柒染","password":"e2fa0937aa136df5818418d9a5c31fc4","quickforward":"yes","handlekey":"ls"}
data=urllib.urlencode(value)

headers={"Origin":"http://rs.xidian.edu.cn","Referer":"http://rs.xidian.edu.cn/forum.php","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"}
req=urllib2.Request(url=url,data=data,headers=headers)
cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))#第一次登陆获得cookie
response=opener.open(req)#登陆成功
message=["路过帮顶，请叫我雷锋","mark,等下下下来看看","好资源，mark留着等会看","楼主不要管我，让我一个人静一静..."]
def shuitie(opener,url,timelate,pagenumber,message):#opener为第一次登陆获得cookie的对象 url为每个帖子相同的前面部分，temlate为每隔多久水一次帖子，pagenumber为水贴的数量，message为水贴的留言
    judege=0
    alltitle=[]
    allurl=[]
    while(judege<pagenumber):
        number=random.randint(646,5000)
        tid="64"+str(number)
        url_open=url+tid
        response=opener.open(url_open).read().encode("utf-8")#进入要水的帖子获取需要的参数
        fid=re.findall("ptm\s*pnpost.*?fid=(\d*)",response,re.S)[0]#获取当前页面的fid
        formhash=re.findall('formhash=(.*?)">退出',response,re.S)[0]#获取当前页面的formhash
        title=re.findall("<title>(.*?)</title>",response,re.S)[0]#title
        print title
        alltitle.append(title)
        allurl.append(url_open)
        print url_open
        try:
            f=open("log.text","a")
            f.write(title+'\n')
            f.write(url_open+'\n\n')
            f.close()
        finally:
            f.close()
        data={"message":message[judege%len(message)],"formhash":formhash,"usesig":"1","subject":"  "}
        data=urllib.urlencode(data)
        requestURL="http://rs.xidian.edu.cn/forum.php?mod=post&action=reply&fid="+fid+"&tid="+tid+"&extra=&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
        req=urllib2.Request(headers=headers,url=requestURL,data=data)
        response=opener.open(req).read().encode("utf-8")
        judege=judege+1
        time.sleep(timelate)#睡眠
    print "work over!"



shuitie(opener,"http://rs.xidian.edu.cn/forum.php?mod=viewthread&tid=",5,2,message)
the_page=response.read().decode("utf-8")

