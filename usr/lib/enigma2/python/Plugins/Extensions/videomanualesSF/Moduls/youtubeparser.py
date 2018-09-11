# -*- coding: utf-8 -*-
###################################################
# LOCAL import
###################################################
from youtube_dl import InfoExtractors
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, remove_html_markup
from Plugins.Extensions.IPTVPlayer.libs.youtube_dl.utils import clean_html, unescapeHTML
from Plugins.Extensions.IPTVPlayer.libs.pCommon import common, CParsingHelper
###################################################

###################################################
# FOREIGN import
###################################################
import re
###################################################

class YouTubeParser():
    HOST = 'Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/17.0'
    def __init__(self):
        self.cm = common()
        return

    def getDirectLinks(self, url, formats = 'flv, mp4'):
        printDBG('YouTubeParser.getDirectLinks')
        list = []
        try:
            list = InfoExtractors.YoutubeIE()._real_extract(url)
        except:
            printDBG('YouTubeParser.getDirectLinks Exception')
            return []

        retList = []
        for item in list:
            #printDBG("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            #printDBG( item )
            #printDBG("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            if -1 < formats.find( item['ext'] ):
                if 'yes' == item['m3u8']:
                    format = re.search('([0-9]+?)p$', item['format'])
                    if format != None:
                        item['format'] = format.group(1) + "x"
                        item['ext']  = item['ext'] + "_M3U8"
                        retList.append(item)
                else:
                    format = re.search('([0-9]+?x[0-9]+?$)', item['format'])
                    if format != None:
                        item['format'] = format.group(1)
                        retList.append(item)
                    
        # onverts all keys
        for idx  in range(len(retList)):
            for key in retList[idx].keys():
                retList[idx][key] = retList[idx][key].encode('utf-8')
                
        return retList
        
    ########################################################
    # List Base PARSER
    ########################################################
    def parseListBase(self, data, type='video'):
        printDBG("parseListBase----------------")
        urlPatterns = { 'video'    :    ['video'   , 'href="(/watch\?v=[^"]+?)"'            , ''], 
                        'channel'  :    ['category', 'href="(/[^"]+?)"'                     , ''],
                        'playlist' :    ['category', 'data-context-item-id="([^"]+?)"'      , '/playlist?list='],
                        'movie'    :    ['video'   , 'data-context-item-id="([^"]+?)"'      , '/watch?v='],
                        'live'     :    ['video'   , 'href="(/watch\?v=[^"]+?)"'            , ''] }
        currList = []
        for i in range(len(data)):
            # get requaired params
            url   = urlPatterns[type][2] + self.getAttributes(urlPatterns[type][1], data[i])            
            title = self.getAttributes('title="([^"]+?)"', data[i])
            if '' == title: title = self.getAttributes('data-context-item-title="([^"]+?)"', data[i])
            if '' == title: 
                sts,title = CParsingHelper.getDataBeetwenMarkers(data[i], '<h3 class="yt-lockup-title">', '</h3>', False)
                title = CParsingHelper.removeDoubles(remove_html_markup(title, ' '), ' ')
            img   = self.getAttributes('data-thumb="([^"]+?\.jpg)"', data[i])
            if '' == img:  img = self.getAttributes('src="([^"]+?\.jpg)"', data[i])
            time  = self.getAttributes('data-context-item-time="([^"]+?)"', data[i])
            if '' == time: time  = self.getAttributes('class="video-time">([^<]+?)</span>', data[i])
            # desc
            sts,desc  = CParsingHelper.getDataBeetwenReMarkers(data[i], re.compile('class="video-description[^>]+?>'), re.compile('</p>'), False)
            if '' == desc: sts,desc = CParsingHelper.getDataBeetwenReMarkers(data[i], re.compile('class="yt-lockup-description[^>]+?>'), re.compile('</div>'), False)
            desc = CParsingHelper.removeDoubles(remove_html_markup(desc, ' '), ' ')
            
            urlTmp = url.split(';')
            if len(urlTmp) > 0: url = urlTmp[0]
                
            if title != '' and url != '' and img != '':
                correctUrlTab = [url, img]
                for i in range(len(correctUrlTab)):
                    if not correctUrlTab[i].startswith('http:') and not correctUrlTab[i].startswith('https:'):
                        if correctUrlTab[i].startswith("//"):
                            correctUrlTab[i] = 'http:' + correctUrlTab[i]
                        else:
                            correctUrlTab[i] = 'http://www.youtube.com' + correctUrlTab[i]
                    else:
                        if correctUrlTab[i].startswith('https:'):
                            correctUrlTab[i] = "http:" + correctUrlTab[i][6:]

                title = clean_html(title.decode("utf-8")).encode("utf-8")
                desc  = clean_html(desc.decode("utf-8")).encode("utf-8")
                params = {'type': urlPatterns[type][0], 'category': type, 'title': title, 'url': correctUrlTab[0], 'icon': correctUrlTab[1], 'time': time, 'desc': desc}
                currList.append(params)

        return currList
    #end parseListBase
    
    ########################################################
    # Tray List PARSER
    ########################################################
    def getVideosFromTraylist(self, url):
        printDBG('YouTubeParser.getVideosFromTraylist')
        currList = []
        #try:
        if 1:
            sts,data =  self.cm.getPage(url, {'host': self.HOST})
            if sts:
                sts,data = CParsingHelper.getDataBeetwenMarkers(data, 'playlist-tray-container', 'playlist-tray-trim', False)
                data = data.split('video-list-item')
                return self.parseListBase(data)
        #except:
        else:
            printDBG('YouTubeParser.getVideosFromTraylist Exception')
            return []
            
        return currList
    # end getVideosFromPlaylist
       
    ########################################################
    # PLAYLIST PARSER
    ########################################################
    def getVideosFromPlaylist(self, url, category, page):
        printDBG('YouTubeParser.getVideosFromPlaylist')
        currList = []
        #try:
        if 1:
            sts,data =  self.cm.getPage(url, {'host': self.HOST})
            if sts:
                sts,data = CParsingHelper.getDataBeetwenMarkers(data, 'gh-activityfeed', 'footer-container', False)   
                itemsTab = data.split('playlist-video-item-base-content')
                return self.parseListBase(itemsTab)
        #except:
        else:
            printDBG('YouTubeParser.getVideosFromPlaylist Exception')
            return []
            
        return currList
    # end getVideosFromPlaylist

    ########################################################
    # CHANNEL LIST PARSER
    ########################################################
    def getAttributes(self, regx, data, num=1):
        match = re.search(regx, data)
        if not match: return ''
        else: return match.group(1)
        
    def getVideosFromChannelList(self, url, category, page):
        printDBG('YouTubeParser.getVideosFromChannelList page[%s]' % (page) )
        currList = []
        #try:
        if 1:
            sts,data =  self.cm.getPage(url, {'host': self.HOST})
            if sts:
                if '1' == page:
                    sts,data = CParsingHelper.getDataBeetwenMarkers(data, 'video-page-content', 'footer-container', False)
                else:
                    data = unescapeHTML(data.decode('unicode-escape')).encode('utf-8').replace('\/', '/')
                    
                # nextPage
                match = re.search('data-uix-load-more-href="([^"]+?)"', data)
                if not match: nextPage = ""
                else: nextPage = match.group(1).replace('&amp;', '&')
    
                data = data.split('context-data-item')
                currList = self.parseListBase(data)
                
                if '' != nextPage:
                    item = {'type': 'category', 'category': category, 'title': 'Następna strona', 'page': str(int(page) + 1), 'url': 'http://www.youtube.com' + nextPage}
                    currList.append(item)
        #except:
        else:
            printDBG('YouTubeParser.getVideosFromChannelList Exception')
            return []
        return currList
    # end getVideosFromChannel

    ########################################################
    # SEARCH PARSER
    ########################################################
    #def getVideosFromSearch(self, pattern, page='1'):
    def getSearchResult(self, pattern, searchType, page, nextPageCategory):
        printDBG('YouTubeParser.getSearchResult pattern[%s], searchType[%s], page[%s]' % (pattern, searchType, page))
        currList = []
        #try:
        if 1:
            url = 'http://www.youtube.com/results?search_query=%s&filters=%s&page=%s' % (pattern, searchType, page) 
            sts,data =  self.cm.getPage(url, {'host': self.HOST})
            if sts:
                if data.find('data-page="%d"' % (int(page) + 1)) > -1: nextPage = True
                else: nextPage = False
        
                sts,data = CParsingHelper.getDataBeetwenMarkers(data, '<ol id="search-results" class="result-list context-data-container">', '</ol>', False)
                data = data.split('result-item')
                del data[0]
                currList = self.parseListBase(data, searchType)
        
                if nextPage:
                    item = {'name': 'history', 'type': 'category', 'category': nextPageCategory, 'pattern':pattern, 'search_type':searchType, 'title': 'Następna strona', 'page': str(int(page) + 1)}
                    currList.append(item)
        #except:
        else:
            printDBG('YouTubeParser.getVideosFromSearch Exception')
            return []
        return currList
    # end getVideosFromSearch
