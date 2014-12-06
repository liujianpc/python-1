__author__ = 'liyuhang'
#coding:utf-8
import urllib2,sys,json,urllib
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding('utf8')
def company():#爬出有哪些公司
    html=urllib2.urlopen("http://www.lagou.com/sitemap")
    lagou=unicode(html.read(),"utf-8")
    d=pq(lagou)
    a=d('.companyListPage').find('dd a')
    pp=open('somework2.text','a')
    for i in a:
        companys={}
        href=pq(i).attr('href')
        print href
        if(href):
            infos=companysdeep(href)
        companys.update(infos)
        companys=json.dumps(companys,ensure_ascii=False,indent=4)
        postapi(companys)
        pp.write(companys)
    pp.close()
    #return companys

def companysdeep(url):#公司深度爬
    infos={}
    html=urllib2.urlopen(url)
    lagou=unicode(html.read(),'utf-8')
    d=pq(lagou)
    companyname=d('.fullname').attr('title')#公司名称
    infos["name"]=companyname
    companytagspan=d('#hasLabels li span')
    tags=[]
    for i in companytagspan:
        companytag=pq(i).html()#公司标签
        tags.append(companytag)
    #获取所有公司标签
    infos["tags"]=tags
    info=d('.oneword').text()#公司简介
    if (info):
        info=info.replace('\r\n','')
        info=info.replace('<br/>','')
        info=info.replace('\n','')
        info=info.replace('\t','')
    infos["introduce"]=info
    print info
    about=d('.c_tags tr')#地点领域 规模 主页
    guimo=[]
    for i in about:
        if (pq(i).find('a')):
            wheretime=pq(i).find('a').attr('href')
            infos["href"]=wheretime#主页地址
        elif(pq(i).find('td').eq(1).attr('title')):
            wheretime=pq(i).find('td').eq(1).attr('title')
            guimo.append(wheretime)
            print wheretime
        else:
            wheretime=pq(i).find('td').eq(1).text()
            if(wheretime==''):
                wheretime=None
            print wheretime
            guimo.append(wheretime)#时间 地点 领域 规模
    infos["about"]=guimo
    rongzi=d('.c_stages').text()#融资情况
    infos["finance"]=rongzi
    member=d('.c_member')
    m_name=[]
    m_name.append(member.find('.m_name').text())
    m_name.append(member.find('.m_position').text())
    m_name.append(member.find('.m_intro').text())
    infos["member"]=m_name
    chanpin={}
    if(d('.c_product')):#加入产品
        products=d('.c_product')
        for i in products:
            productname=pq(i).children('dd h3 a').text()#产品名称
            productinfo=pq(i).find('.scroll-pane div').text()#产品描述
            #product={productname:productinfo}
            chanpin[productname]=productinfo
    infos["product"]=chanpin
    #infos=json.dumps(infos,indent=4)
    return infos
def postapi(jsons):
    url="http://115.28.232.254:8080/api.php"
    value={"action":"auto_add_company_job","data":jsons}
    data=urllib.urlencode(value)
    print data
    req=urllib2.Request(url=url,data=data)
    html=urllib2.urlopen(req).read();
    print(html)
company()
#jsons='{"about": ["上海", "移动互联网,游戏", "150-500人"], "finance": "融资阶段 目前阶段： B轮", "tags": ["年底双薪", "节日礼物", "绩效奖金", "年度旅游", "定期体检", "通讯津贴", "五险一金", "弹性工作", "股票期权", "专项奖金", "免费班车", "带薪年假", "年终分红", "午餐补助"], "product": {}, "introduce": "手游里面的佼佼者", "member": [null, null, null], "href": "http://www.huodao.com", "name": "上海火道网络科技有限公司"}'
#postapi(jsons)