# -*- coding: utf-8 -*-
'''
        HK Kan Beta
        by panglangjang

        Streaming Chinese Programming off azdrama.net
        
        GPLv3

'''
from t0mm0.common.net import Net
import urllib,urllib2,re,xbmcplugin,xbmcgui

__home__    =   None
__category__=   1
__show__    =   2

#def __init__(self):

def HOME():
        #addDir('Search','http://www.khmeravenue.com/',4,'http://yeuphim.net/images/logo.png')
        addDir('新的东西','http://azdrama.net/recently-updated',__category__,'')
        #addDir('English Subtitles','http://azdrama.net/english/&sort=date',7,'')
        addDir('电视剧','http://azdrama.net/hk-drama',__category__,'')
        addDir('综艺','http://azdrama.net/hk-show',__category__,'')
        addDir('韩国 电视剧','http://azdrama.net/korean-drama',__category__,'')
        #addDir('Mainland Chinese Dramas','http://azdrama.net/chinese-drama/',__category__,'')
        #addDir('Taiwanese Dramas','http://azdrama.net/taiwanese-drama/',2,'')

def INDEX(url):
    #try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<div class="content">(.+?)<div id="r">').findall(newlink)
        match=re.compile('<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*></a><h1 class="normal"><a href="(.+?)" title="(.+?)">(.+?)</a><span class="download">').findall(listcontent[0])
        for (vimg,vurl,vname,vtmp) in match:
            vurl = vurl +'list-episode/'
            print vurl
            try:
                  addDir(vname,vurl,__show__,vimg)
            except:
                  #if the addDir fails, its probably because some args need to be encoded to utf-8, because they contain chinese characters.
                  vimg = vimg.encode('utf-8')
                  vurl = vurl.encode('utf-8')
                  vname = vname.encode('utf-8')
                  addDir(vname,vurl,__show__,vimg)
        pagecontent=re.compile('<div class="wp-pagenavi" align=center>(.+?)</div>').findall(newlink)
        if(len(pagecontent)>0):
                match5=re.compile('<a href="(.+?)" class="(.+?)" title="(.+?)">(.+?)</a>').findall(pagecontent[0])

                #removing last element doesnt always handle the problem.
                #you get &laquo; if you are not on the first page
                #del match5[-1]
                for vurl,vtmp,vname,vtmp2 in match5:
                    #so far, this greedy replace call will have to suffice
                    #Note: the paginated pages do follow a pattern
                    #ex: http://azdrama.net/recently-updated/page-2.html
                    #in other words, this plugins menu can be written alot better.
                    vname = vname.replace('&laquo;','<<')
                    vname = vname.replace('&raquo;','>>')
                    addDir(vname,vurl,__category__,"")
    #except: pass


def GetContent(url):
    try:
       net = Net()
       response = net.http_GET(url)
       return response.content
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"不能得到的东西",'请再试一次')
	
def Episodes(url,name,newmode):
    link = GetContent(url)
    newlink = ''.join(link.splitlines()).replace('\t','')
    listcontent=re.compile('<ul class="listep">(.+?)</ul>').findall(newlink)

    match=re.compile('<li><a href="(.+?)" title="[^"]+ (?:Episode [0]*([\d]+)|([\d]{4}-[\d]{2}-[\d]{2}))">').findall(listcontent[0])

    is_mirror = len(match[0][1])==0 & len(match[0][2])==0
    #listlink = re.compile('<a href="([^\"]+?)">Watch all episodes</a>').findall(newlink)
    #listcontent=[]

    if(is_mirror): #must be mirrored parts
        print "Processing Mirrored Episodes:"
        #must be a mirrored link. eagerly load the parts:
        link = GetContent(match[0][0]) #href
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent = re.compile('<ul class="listew">(.+?)</ul>').findall(newlink)

        #rebuild match for next loop
        #default order is acsending
        match=re.compile('<a href="(.+?)"><font [^>]*><b>[^0-9]*([0-9]+?)[^<]*</b></font></a>').findall(listcontent[0])        

    else: #must be all hosted
        print "Processing Hosted Episodes: "
        #print listlink
        #request full episodes list:

        #scrap through all pages if paginated
        last_page= re.compile('<a href="'+url+'page-([\d]+)\.html" class="last"').findall(newlink)
        if(len(last_page)>0):
            last_page_num = int(last_page[0])
            print "Scraping through " + last_page[0] + " Pages!"

            #this will be a long operation!
            page_num = 2
            while(page_num <= last_page_num):
                print "Scraping Page: "+str(page_num)
                link = GetContent(url+'page-'+str(page_num)+'.html') #we're gonna go through each page to get the whole list!
                newlink = ''.join(link.splitlines()).replace('\t','')
                listcontent=re.compile('<ul class="listep">(.+?)</ul>').findall(newlink)

                #appending all new matchs to original list!
                match+=re.compile('<li><a href="(.+?)" title="[^"]+ (?:Episode [0]*([\d]+)|([\d]{4}-[\d]{2}-[\d]{2}))">').findall(listcontent[0])

                page_num+=1
        
        
        
        match.reverse() #default order is descending

    print "Listing Episodes"
    #print match    
    for (idx, data) in enumerate(match):
        #print data[0]
        #print data[1]
        #print data[2]
        order = data[1] if data[1] else data[2] #episode number or date
        
        episode_link=GetContent(data[0]) # data[0] is the href tag
        episode_newlink = ''.join(episode_link.splitlines()).replace('\t','')
        episode_match=re.compile('<div id="player" align="center"><iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(episode_newlink)

        if(len(episode_match) > 0):
            #print episode_match[0]
            framecontent = GetContent(episode_match[0])

            embedlink=re.compile('function player_(?:normal_mp4|best)\(\) {jQuery\("#videoplayer"\).html\("<embed [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(framecontent)
            #print embedlink
            if(len(embedlink) > 0):
                embedlink.reverse() #put "best" before "normal_mp4", if there is no best, there should just be normal_mp4    
                vname = embedlink[0] #select the first quality, should be "best" defaulting to "normal_mp4"
                #print vname
                vlink=re.compile('file=(.+?)\&').findall(vname)

                #finally, add the direct link to each episode
                print "Adding Link:" + name + str(order)
                #print "Caching link"
                #should append to array of all cached links, so it can be loaded later without so much scraping"
                addLink(name + " - 第" + str(order),urllib.unquote(vlink[0]),'')


def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param



params=get_params()
url=None
name=None
mode=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

sysarg=str(sys.argv[1])
print "mode is:" + str(mode)
if mode==__home__ or url==None or len(url)<1:
        HOME()
elif mode==__category__:
        INDEX(url)
elif mode==__show__:
        Episodes(url,name,mode)

xbmcplugin.endOfDirectory(int(sysarg))
