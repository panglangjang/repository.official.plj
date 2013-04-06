# -*- coding: utf-8 -*-
'''
    Official PLJ Addon
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Placeholder

    :copyright: (c) 2013 by panglangjang
    :license: GPLv3, see LICENSE.txt for more details.
'''

#from xbmcswift2 import actions
import urllib,urllib2,re,xbmcplugin,xbmcgui

def CATEGORIES():
        plugins = [
                        ( 95, '香港看(HKKan)','plugin.video.hkkan', 'hkk.png'),
                        ( 80, '迅雷看看(KanKan)','plugin.video.kankan', 'kk.png' ),
                        ( 70, '网络电视(PPS)', 'plugin.video.ppstream','pps.png' ),
                        ( 90, '音悦台(YinYueTai)','plugin.video.yinyuetai','yyt.png' )
                ]
        for rating, name, url, icon in plugins:
                addPlugin('可靠性: '+str(rating)+'% | '+ str(name), 'plugin://'+str(url),'special://home/addons/'+str(url)+'/icon.png')

def BRIDGE(url):
        #actions.update_view(url)
        xbmc.executebuiltin('Container.Update('+url+')')

def addPlugin(name,url,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=1"
        ok=True
        liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
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
