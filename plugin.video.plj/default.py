# -*- coding: utf-8 -*-
'''
    Official PLJ Addon
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Placeholder

    :copyright: (c) 2013 by panglangjang
    :license: GPLv3, see LICENSE.txt for more details.
'''

from xbmcswift2 import actions
import urllib,urllib2,re,xbmcplugin,xbmcgui

def CATEGORIES():
        categories = [
                ( 'International', [
                        ( '网络电视(PPS)', 'plugin://plugin.video.ppstream/' )
                ] ),

                ( 'Local', [
                        ( '香港看(HKKan)','plugin://plugin.video.hkkan/' ),
                        ( '迅雷看看(KanKan)', 'plugin//plugin.video.kankan/' ),
                        ( '音悦台(YingYueTai)','plugin://plugin.video.yingyuetai/' ),

                ] )

                ]
        for category,addons in categories:
                addDir('- '+category,'',0,'')
                for name, url in addons:
                        addDir(name,url,1,'')

def BRIDGE(url):
        actions.update_view(url)
                
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

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
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

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
        
elif mode==0:
        print "dummy"
       
elif mode==1:
        print ""+url
        BRIDGE(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
