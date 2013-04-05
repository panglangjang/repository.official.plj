import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import base64
import xbmc

def __init__(self):
    self.playlist=sys.modules["__main__"].playlist
def HOME():
        #addDir('Search','http://www.khmeravenue.com/',4,'http://yeuphim.net/images/logo.png')
        addDir('Recent Updates','http://azdrama.net/recently-updated/',2,'')
        #addDir('English Subtitles','http://azdrama.net/english/&sort=date',7,'')
        addDir('HK Dramas','http://azdrama.net/hk-drama/',2,'')
        addDir('HK Shows','http://azdrama.net/hk-show/',2,'')
        addDir('Korean Dramas','http://azdrama.net/korean-drama/',2,'')
        #addDir('Mainland Chinese Dramas','http://azdrama.net/chinese-drama/',2,'')
        #addDir('Taiwanese Dramas','http://azdrama.net/taiwanese-drama/',2,'')

def INDEX(url):
    #try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<div class="content">(.+?)<div id="r">').findall(newlink)
        match=re.compile('<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*></a><h1 class="normal"><a href="(.+?)" title="(.+?)">(.+?)</a><span class="download">').findall(listcontent[0])
        for (vimg,vurl,vname,vtmp) in match:
            #print vimg
            #print vurl
            #print vname
            #print vtmp
            vimg = vimg.encode('utf-8')
            vurl = vurl.encode('utf-8')        
            #vname = vname.encode('utf-8')
            #vtmp = vtmp.encode('utf-8')
            try:
                  addDir(vname,vurl+"list-episode/",5,vimg)
            except:
                  addDir(vname.decode("utf-8"),vurl+"list-episode/",5,vimg)
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
                    addDir(vname,vurl,2,"")
    #except: pass


def SEARCH():
    try:
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://yeuphim.net/movie-list.php?str='+ searchText
        INDEX(url)
    except: pass

def SearchResults(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<aclass="widget-title" href="(.+?)"><imgsrc="(.+?)" alt="(.+?)"').findall(newlink)
        if(len(match) >= 1):
                for vLink,vpic,vLinkName in match:
                    addDir(vLinkName,vLink,5,vpic)
        match=re.compile('<strong>&raquo;</strong>').findall(link)
        if(len(match) >= 1):
            startlen=re.compile("<strongclass='on'>(.+?)</strong>").findall(newlink)
            url=url.replace("/page/"+startlen[0]+"/","/page/"+ str(int(startlen[0])+1)+"/")
            addDir("Next >>",url,6,"")

def Mirrors(url,name):
    try:
        if(CheckRedirect(url)):
                MirrorsThe(name,url)
        else:
                link = GetContent(url)
                newlink = ''.join(link.splitlines()).replace('\t','')
                match=re.compile('<b>Episode list </b>(.+?)</table>').findall(newlink)
                mirrors=re.compile('<div style="margin: 10px 0px 5px 0px">(.+?)</div>').findall(match[0])
                if(len(mirrors) >= 1):
                        for vLinkName in mirrors:
                            addDir(vLinkName.encode("utf-8"),url,5,'')

    except: pass
	
def Parts(url,name):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        partlist=re.compile('<li>VIP #1:(.+?)by:').findall(link)
        partctr=0
        if(len(partlist)>0):
               partlink=re.compile('<a href="(.+?)">').findall(partlist[0])
               if(len(partlink) > 1):
                       for vlink in partlink:
                              partctr=partctr+1
                              addDir(name + " Part " + str(partctr),vlink,3,"")
        return partctr
		
def CheckParts(url,name):
	if(Parts(url,name) < 2):
		loadVideos(url,name)
def Episodes(url,name,newmode):
    #try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<ul class="listep">(.+?)</ul>').findall(newlink)
        if(newmode==5):
                vidmode=11
        else:
                vidmode=9
        match=re.compile('<li><a href="(.+?)" title="(.+?)">').findall(listcontent[0])
        for (vurl,vname) in match:
            try:
                  addDir(vname,vurl,vidmode,"")
            except:
                  addDir(vname.decode("utf-8"),vurl,vidmode,"")
        pagecontent=re.compile('<div class="wp-pagenavi" align=center>(.+?)</div>').findall(newlink)
        if(len(pagecontent)>0):
                match5=re.compile('<a href="(.+?)" class="(.+?)" title="(.+?)">(.+?)</a>').findall(pagecontent[0])
                for vurl,vtmp,vname,vtmp2 in match5:
                    addDir("page: " + vname,vurl,newmode,"")

    #except: pass

def GetEpisodeFromVideo(url,name):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<center><a href="(.+?)"><font style="(.+?)">(.+?)</font></a></center>').findall(newlink)
        Episodes(listcontent[0][0]+"list-episode/",name,5)

def Geturl(strToken):
        for i in range(20):
                try:
                        strToken=strToken.decode('base-64')
                except:
                        return strToken
                if strToken.find("http") != -1:
                        return strToken

	   
def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

def playVideo(videoType,videoId):
    url = ""
    print videoType + '=' + videoId
    if (videoType == "youtube"):
        url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)

def loadVideos(url,name):
           link=GetContent(url)
           newlink = ''.join(link.splitlines()).replace('\t','')
           match=re.compile('<div id="player" align="center"><iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newlink)
           if(len(match) > 0):
                   framecontent = GetContent(match[0])
                   qualityval = ["240","360p(MP4)","360p(FLV)","480p","720p","HTML5"]
                   qctr=0
                   embedlink=re.compile('<embed [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(framecontent)
                   for vname in embedlink:
                         vlink=re.compile('file=(.+?)\&').findall(vname)
                         if(len(vlink) > 0):
                             addLink(qualityval[qctr],urllib.unquote(vlink[0]),8,"","")
                         qctr=qctr+1
           else:
                   match=re.compile('<li>VIP #1: <a href="(.+?)">').findall(newlink)
                   if(len(match) > 0):
                           loadVideos(match[0],name)
                   else:  
                           d = xbmcgui.Dialog()
                           d.ok('Not Implemented','Sorry this video site is ',' not implemented yet')

def addLink(name,url,mode,iconimage,mirrorname):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))+"&mirrorname="+urllib.quote_plus(mirrorname)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addNext(formvar,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&formvar="+str(formvar)+"&name="+urllib.quote_plus('Next >')
        ok=True
        liz=xbmcgui.ListItem('Next >', iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))
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
formvar=None
mirrorname=None
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
try:
        mirrorname=urllib.unquote_plus(params["mirrorname"])
except:
        pass

sysarg=str(sys.argv[1])
print "mode is:" + str(mode)
if mode==None or url==None or len(url)<1:

        HOME()
elif mode==2:
        INDEX(url)
elif mode==3:
        loadVideos(url,mirrorname)
elif mode==4:
        SEARCH()
elif mode==5:
       Episodes(url,name,mode)
elif mode==6:
       SearchResults(url)
elif mode==7:
       Episodes(url,name,mode)
elif mode==8:
        playVideo("direct",url)
elif mode==9:
       GetEpisodeFromVideo(url,name)
elif mode==10:
       Episodes2(url,name)
elif mode==11:
       CheckParts(url,name)

xbmcplugin.endOfDirectory(int(sysarg))
