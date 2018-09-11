from xml.etree.cElementTree import fromstring, ElementTree
import urllib2
import urllib as ul
import os, re
from datetime import datetime
from time import time
#ADD EXTERNAL MODUL
from nStreamModul_vkontakte import html_parser_vkontakte
from nStreamModul_vizor_tv import html_parser_vizor_tv

def debug(obj, text=''):
	print datetime.fromtimestamp(time()).strftime('[%H:%M:%S]')
	print '%s' % text +  ' %s\n' % obj

def mod_request(url, param = None):
	url = 'http://' + url
	html = ''
	try:
		debug(url, 'MODUL REQUEST URL')
		req = urllib2.Request(url, param, {'User-agent': 'Mozilla/5.0 WEBCENTER 3.0', 'Connection': 'Close'})
		html = urllib2.urlopen(req).read() 
		#print html
	except Exception, ex:
		print ex
		print 'REQUEST Exception'
	return html

      
class html_parser_moduls:
	
	def __init__(self):
		self.video_list = []
		self.next_page_url = ''
		self.next_page_text = ''
		self.prev_page_url = ''
		self.prev_page_text = ''
		self.search_text = ''
		self.search_on = ''
		self.active_site_url = ''
		self.playlistname = ''
		self.playlist_cat_name = ''
		self.kino_title = ''
		self.category_back_url = ''
		self.error = ''
		

	def reset_buttons(self):
		self.kino_title = ''
		self.next_page_url = None
		self.next_page_text = ''
		self.prev_page_url = None
		self.prev_page_text = ''
		self.search_text = ''
		self.search_on = None

	def get_list(self, url):
		debug(url, 'MODUL URL: ')
		self.reset_buttons() 

#EXTERNAL FILE WITH SWITCH AND PARSER  vkontakte search ################################################################################################################ 		
		if(url.find('vkontaktesearch')>-1):
			VKONTAKTESEARCH = html_parser_vkontakte() 
			VKONTAKTESEARCH.get_list(url)
			self.video_list = VKONTAKTESEARCH.video_list
			self.next_page_url = VKONTAKTESEARCH.next_page_url
			self.next_page_text = VKONTAKTESEARCH.next_page_text
			self.prev_page_url = VKONTAKTESEARCH.prev_page_url
			self.prev_page_text = VKONTAKTESEARCH.prev_page_text
			self.search_text = VKONTAKTESEARCH.search_text
			self.search_on = VKONTAKTESEARCH.search_on
			self.active_site_url = VKONTAKTESEARCH.active_site_url
			self.playlistname = VKONTAKTESEARCH.playlistname
			self.playlist_cat_name = VKONTAKTESEARCH.playlist_cat_name
			self.kino_title = VKONTAKTESEARCH.kino_title
			self.category_back_url = VKONTAKTESEARCH.category_back_url
			self.error = VKONTAKTESEARCH.error 		
#EXTERNAL FILE WITH SWITCH AND PARSER  vkontakte search ################################################################################################################ 
			  

#EXTERNAL FILE WITH SWITCH AND PARSER  vizor.tv ################################################################################################################ 		
		if(url.find('vizor.tv')>-1):
			VIZORTV = html_parser_vizor_tv() 
			VIZORTV.get_list(url)
			self.video_list = VIZORTV.video_list
			self.next_page_url = VIZORTV.next_page_url
			self.next_page_text = VIZORTV.next_page_text
			self.prev_page_url = VIZORTV.prev_page_url
			self.prev_page_text = VIZORTV.prev_page_text
			self.search_text = VIZORTV.search_text
			self.search_on = VIZORTV.search_on
			self.active_site_url = VIZORTV.active_site_url
			self.playlistname = VIZORTV.playlistname
			self.playlist_cat_name = VIZORTV.playlist_cat_name
			self.kino_title = VIZORTV.kino_title
			self.category_back_url = VIZORTV.category_back_url
			self.error = VIZORTV.error 		
#EXTERNAL FILE WITH SWITCH AND PARSER  vizor.tv ################################################################################################################

#SWITCH  m3u ########################################################################################

		if(url.find('m3u')>-1):
			parts = url.split('@') 
			filename = parts[0]
			name = parts[2].encode('utf-8')
			self.playlistname = name 
			ts = None
			if(url.find('TS')>-1):
				ts = 'True'
			try:               
				video_list_temp = [] 
				chan_counter = 0
				if filename.find('http')>-1:
					url = filename.replace('http://', '')
					myfile = mod_request(url) 
				else:
					myfile = open("/usr/lib/enigma2/python/Plugins/Extensions/WEBCENTER/%s" % filename, "r").read()
				#print myfile
				regex = re.findall(r'#EXTINF.*,(.*\s)\s*(.*)',myfile)
				if not len(regex)>0:
					regex = re.findall(r'((.*.+)(.*))',myfile)
				#print regex
		 
				for text in regex:
					title = text[0].strip()
					url = text[1].strip()
					chan_counter +=1 
					chan_tulpe = (
						chan_counter,
						title,
						'',
						'xxx.png',
						url,
						None,
						None,
						'',
						'',
						None,
						ts
					)
					video_list_temp.append(chan_tulpe) 

					if(len(video_list_temp)<1):
						print 'ERROR m3u CAT LIST_LEN = %s' %  len(video_list_temp)  
			except:
				print 'ERROR m3u'   									    	

			return video_list_temp	
			
#SWITCH onlinefilmizle.tv ################################################################################################################				
# KRAL
		if(url.find('onlinefilmizle.tv')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.onlinefilmizle.tv'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_onlinefilmizle_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'onlinefilmizle.tv : ' + self.playlist_cat_name
				self.video_list = self.get_onlinefilmizle_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_onlinefilmizle_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_onlinefilmizle_film(url)
				
#SWITCH onlinefilmiizlet.com ################################################################################################################				
# KRAL
		if(url.find('onlinefilmiizlet.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.onlinefilmiizlet.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_onlinefilmiizlet_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'onlinefilmiizlet.com : ' + self.playlist_cat_name
				self.video_list = self.get_onlinefilmiizlet_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_onlinefilmiizlet_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_onlinefilmiizlet_film(url)

#SWITCH filmifullizle ################################################################################################################				
# KRAL
		if(url.find('filmifullizle.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'www.filmifullizle.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_filmifullizle_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'filmifullizle.com : ' + self.playlist_cat_name
				self.video_list = self.get_filmifullizle_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_filmifullizle_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_filmifullizle_film(url)

#SWITCH birfilmizle ################################################################################################################				
# KRAL
		if(url.find('birfilmizle.net')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.birfilmizle.net'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_birfilmizle_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'birfilmizle.net : ' + self.playlist_cat_name
				self.video_list = self.get_birfilmizle_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_birfilmizle_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_birfilmizle_film(url)
				
#SWITCH hdfilmsiten.com ################################################################################################################				
# KRAL
		if(url.find('hdfilmsiten.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.hdfilmsiten.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_hdfilmsiten_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'hdfilmsiten.com : ' + self.playlist_cat_name
				self.video_list = self.get_hdfilmsiten_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_hdfilmsiten_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_hdfilmsiten_film(url)
				
#SWITCH gunlukfilm.com ################################################################################################################				
# KRAL
		if(url.find('gunlukfilm.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'gunlukfilm.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_gunlukfilm_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'gunlukfilm.com : ' + self.playlist_cat_name
				self.video_list = self.get_gunlukfilm_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_gunlukfilm_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_gunlukfilm_film(url)
				
#SWITCH cizgidiyar.com ################################################################################################################				
# KRAL
		if(url.find('cizgidiyar.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.cizgidiyar.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_cizgidiyar_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'cizgidiyar.com : ' + self.playlist_cat_name
				self.video_list = self.get_cizgidiyar_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_cizgidiyar_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_cizgidiyar_film(url)
				
#SWITCH direkizle ################################################################################################################				
# KRAL
		if(url.find('direkizle.net')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'direkizle.net'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_direkizle_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'direkizle.net : ' + self.playlist_cat_name
				self.video_list = self.get_direkizle_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_direkizle_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_direkizle_film(url)

#SWITCH cinemaizle.org ################################################################################################################				
# KRAL
		if(url.find('cinemaizle.org')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.cinemaizle.org'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_cinemaizle_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'cinemaizle.org : ' + self.playlist_cat_name
				self.video_list = self.get_cinemaizle_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_cinemaizle_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_cinemaizle_film(url)

#SWITCH filmtekpart.com ################################################################################################################		
# KRAL
		if(url.find('filmtekpart.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.filmtekpart.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_filmtekpart_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'filmtekpart.com : ' + self.playlist_cat_name
				self.video_list = self.get_filmtekpart_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_filmtekpart_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_filmtekpart_film(url)
				
#SWITCH divxfilmizle.net ################################################################################################################		
# KRAL
		if(url.find('divxfilmizle.net')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.divxfilmizle.net'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_divxfilmizle_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'divxfilmizle.net : ' + self.playlist_cat_name
				self.video_list = self.get_divxfilmizle_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_divxfilmizle_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_divxfilmizle_film(url)

#SWITCH www.yenifilmler-izle.com ################################################################################################################		
# KRAL
		if(url.find('yenifilmler-izle.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.yenifilmler-izle.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_yenifilmlerizle_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'yenifilmler-izle.com : ' + self.playlist_cat_name
				self.video_list = self.get_yenifilmlerizle_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_yenifilmlerizle_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_yenifilmlerizle_film(url)

#SWITCH www.hdfilmtube.com ################################################################################################################		
# KRAL
		if(url.find('hdfilmtube.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.hdfilmtube.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_hdfilmtube_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'hdfilmtube.com : ' + self.playlist_cat_name
				self.video_list = self.get_hdfilmtube_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_hdfilmtube_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_hdfilmtube_film(url)
				
#SWITCH filmizlehep.com ################################################################################################################		
# KRAL
		if(url.find('filmizlehep.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'filmizlehep.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_filmizlehep_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'filmizlehep.com : ' + self.playlist_cat_name
				self.video_list = self.get_filmizlehep_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_filmizlehep_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_filmizlehep_film(url)
				
#SWITCH www.filmhani.com ################################################################################################################				
# KRAL
		if(url.find('filmhani.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.filmhani.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_filmhani_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = self.playlist_cat_name
				self.video_list = self.get_filmhani_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_filmhani_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_filmhani_film(url)

#SWITCH seyretogren.com ################################################################################################################		
# KRAL
		if(url.find('seyretogren.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.seyretogren.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_seyretogren_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'seyretogren.com : ' + self.playlist_cat_name
				self.video_list = self.get_seyretogren_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_seyretogren_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_seyretogren_film(url)
				
#SWITCH www.vkfilmizle.com ################################
# KRAL						
		if(url.find('vkfilmizle.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]
						
			self.active_site_url = 'www.vkfilmizle.com'
						
			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_vkfilmizle_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'vkfilmizle.com : ' + self.playlist_cat_name
				self.video_list = self.get_vkfilmizle_category_films(url)
				self.category_back_url = url
				self.category_title = name
						
			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_vkfilmizle_category_films(url)
				self.category_back_url = url 
						
			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_vkfilmizle_film(url)
				
#SWITCH www.movietr.org ################################
# KRAL						
		if(url.find('movietr.org')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]
						
			self.active_site_url = 'www.movietr.org'
						
			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_movietr_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'movietr.org : ' + self.playlist_cat_name
				self.video_list = self.get_movietr_category_films(url)
				self.category_back_url = url
				self.category_title = name
						
			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_movietr_category_films(url)
				self.category_back_url = url 
						
			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_movietr_film(url)

#SWITCH www.filmodam.com ################################
# KRAL						
		if(url.find('filmodam.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]
						
			self.active_site_url = 'www.filmodam.com'
						
			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_filmodam_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'filmodam.com : ' + self.playlist_cat_name
				self.video_list = self.get_filmodam_category_films(url)
				self.category_back_url = url
				self.category_title = name
						
			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_filmodam_category_films(url)
				self.category_back_url = url 
						
			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_filmodam_film(url)

#SWITCH www.gercekfilmler.com ################################
# KRAL						
		if(url.find('gercekfilmler.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]
						
			self.active_site_url = 'www.gercekfilmler.com'
						
			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_gercekfilmler_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'gercekfilmler.com : ' + self.playlist_cat_name
				self.video_list = self.get_gercekfilmler_category_films(url)
				self.category_back_url = url
				self.category_title = name
						
			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_gercekfilmler_category_films(url)
				self.category_back_url = url 
						
			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_gercekfilmler_film(url)

#SWITCH tamseyret.com ################################
# KRAL						
		if(url.find('tamseyret.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]
						
			self.active_site_url = 'www.tamseyret.com'
						
			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_tamseyret_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'tamseyret.com : ' + self.playlist_cat_name
				self.video_list = self.get_tamseyret_category_films(url)
				self.category_back_url = url
				self.category_title = name
						
			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_tamseyret_category_films(url)
				self.category_back_url = url 
						
			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_tamseyret_film(url)
				
#SWITCH fullhdfilmizlet.com ################################################################################################################		
		if(url.find('fullhdfilmizlet.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.fullhdfilmizlet.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_fullhdfilmizlet_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'fullhdfilmizlet.com : ' + self.playlist_cat_name
				self.video_list = self.get_fullhdfilmizlet_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_fullhdfilmizlet_category_films(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_fullhdfilmizlet_film(url)
				
#SWITCH dizihd.com ################################################################################################################				

		if(url.find('dizihd')>-1):
			parts = url.split('@')
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'dizihd.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_dizihd_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = self.playlist_cat_name
				self.video_list = self.get_dizihd_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==5 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==3 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_dizihd_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_dizihd_film(url)

#SWITCH www.pornetto.com ################################################################################################################				

		if(url.find('pornetto')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'www.pornetto.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_pornetto_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = self.playlist_cat_name
				self.video_list = self.get_pornetto_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==5 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==3 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_pornetto_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_pornetto_film(url)

#SWITCH  webteizle.com ################################################################################################################ 		
		if(url.find('webteizle')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')
			
			self.active_site_url = 'webteizle.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_webteizle_categories(url)
			
			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'webteizle.com: ' + self.playlist_cat_name
				self.video_list = self.get_webteizle_category_films(url)
				self.category_back_url = url
				self.category_title = name
			
			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_webteizle_category_films(url)
				self.category_back_url = url       				
			
			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_webteizle_film(url)		
		
#SWITCH  hdbelgeselizle.com ################################################################################################################ 		
		if(url.find('hdbelgeselizle.com')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')
			
			self.active_site_url = 'www.hdbelgeselizle.com'

			if(page=='start'): 
				url = 'www.hdbelgeselizle.com'
				self.playlistname = name
				self.video_list = self.get_hdbelgeselizle_categories(url)
			
			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'KATEGORILER: ' + self.playlist_cat_name
				self.video_list = self.get_hdbelgeselizle_category_films(url)
				self.category_back_url = url
				self.category_title = name
			
			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_hdbelgeselizle_category_films(url)
				self.category_back_url = url       				
			
			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_hdbelgeselizle_film(url)
				
#SWITCH  webtv.hurriyet.com.tr ################################################################################################################ 		
		if(url.find('hurriyet')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]
			
			self.active_site_url = 'webtv.hurriyet.com.tr'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_hurriyet_categories(url)
			
			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = self.playlist_cat_name
				self.video_list = self.get_hurriyet_category_films(url)
				self.category_back_url = url
				self.category_title = name
				
			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_hurriyet_category_films(url)
				self.category_back_url = url       				
			
			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_hurriyet_film(url)

#SWITCH www.trdizi.com ################################################################################################################				

		if(url.find('trdizi')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'www.trdizi.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_trdizi_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname =  self.playlist_cat_name
				self.video_list = self.get_trdizi_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==5 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==3 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_trdizi_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = name
				self.video_list = self.get_trdizi_film(url)				
									
		
#SWITCH filmsehri.com ################################################################################################################				

		if(url.find('filmsehri')>-1):
			debug('#SWITCH filmsehri.com #')
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'filmsehri.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_filmsehri_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'filmsehri CAT: ' + self.playlist_cat_name
				self.video_list = self.get_filmsehri_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==5 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==3 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_filmsehri_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_filmsehri_film(url)				

#SWITCH http://www.xvideos.com/################################################################################################################				

		if(url.find('xvideos.com')>-1):
			debug('#SWITCH xvideos.com #')
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'www.xvideos.com'
			video_list_temp = []
			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_xvideos_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'XVIDEOS CAT: ' + self.playlist_cat_name
				self.video_list = self.get_xvideos_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				print '++++++++++++'
				
				print page
				print len(page)
				if(int(len(page)-2)>0):
					page_nr= ' PAGE ' + page[len(page)-2]
				#if (len(page)==3 and page[1]=='page'):
				#	page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_xvideos_category_films(url)
				self.category_back_url = url
 # --> nStreamHTMLparser QUICKSTART PLAY FROM CATEGORY
			# if(page=='film'):
			# 	self.kino_title = name
			# 	self.playlistname = self.playlist_cat_name + '     ' + name
			# 	self.video_list = self.get_xvideos_film(url)      			       				

#SWITCH bicaps ################################################################################################################				

		if(url.find('bicaps.com')>-1):
			debug('#SWITCH filmsehri.com #')
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'bicaps.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_bicaps_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = 'bicaps.com : ' + self.playlist_cat_name
				self.video_list = self.get_bicaps_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_bicaps_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_bicaps_film(url)

#SWITCH video-klipleri.org ################################################################################################################				

		if(url.find('klipleri')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'video-klipleri.org'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_klipleri_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = self.playlist_cat_name
				self.video_list = self.get_klipleri_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_klipleri_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_klipleri_film(url)


#SWITCH eroguru.com ################################################################################################################				

		if(url.find('eroguru')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'eroguru.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_eroguru_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = self.playlist_cat_name
				self.video_list = self.get_eroguru_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_eroguru_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_eroguru_film(url)

#SWITCH www.evrenselfilm.com ################################################################################################################				

		if(url.find('evrenselfilm')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'www.evrenselfilm.com'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_evrenselfilm_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = self.playlist_cat_name
				self.video_list = self.get_evrenselfilm_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_evrenselfilm_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_evrenselfilm_film(url)

#SWITCH fragg.me ################################################################################################################				

		if(url.find('fragg')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'fragg.me'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_fragg_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = self.playlist_cat_name
				self.video_list = self.get_fragg_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_fragg_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_fragg_film(url)

#SWITCH www.filmizlese.net ################################################################################################################				

		if(url.find('filmizlese')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'www.filmizlese.net'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_filmizlese_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = self.playlist_cat_name
				self.video_list = self.get_filmizlese_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_filmizlese_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_filmizlese_film(url)
				    			   
#SWITCH www.myvideo.de ################################################################################################################				

		if(url.find('myvideo')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2].encode('utf-8')

			self.active_site_url = 'www.myvideo.de'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_myvideo_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname =  self.playlist_cat_name
				self.video_list = self.get_myvideo_category_films(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==5 and page[3]=='page'):
					page_nr= ' PAGE ' + page[4]
				if (len(page)==3 and page[1]=='page'):
					page_nr= ' PAGE ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_myvideo_category_films(url)
				self.category_back_url = url       				

			if(page=='film'):
				self.kino_title = name
				self.playlistname = name
				self.video_list = self.get_myvideo_film(url)
				
#SWITCH www.belgeseltv.net ################################################################################################################				
# KRAL
		if(url.find('lolabits.es')>-1):
			parts = url.split('@')
			#print parts
			url = parts[0]
			page = parts[1]
			name = parts[2]

			self.active_site_url = 'www.lolabits.es'

			if(page=='start'): 
				self.playlistname = name
				self.video_list = self.get_lolabits_categories(url)

			if(page=='category'):
				self.playlist_cat_name = name
				self.playlistname = self.playlist_cat_name
				self.video_list = self.get_lolabits_category_video(url)
				self.category_back_url = url
				self.category_title = name

			if(page=='category_page'):
				page_nr = ''
				page = url.split('/')
				if(len(page)==6 and page[3]=='page'):
					page_nr= ' SAYFA ' + page[4]
				if (len(page)==4 and page[1]=='page'):
					page_nr= ' SAYFA ' + page[2]
				self.playlistname = self.playlist_cat_name + page_nr
				self.video_list = self.get_lolabits_category_video(url)
				self.category_back_url = url 

			if(page=='film'):
				self.kino_title = name
				self.playlistname = self.playlist_cat_name + ' ' + name
				self.video_list = self.get_lolabits_video(url)
				
########################################################################
		return self.video_list  ########################################	
########################################################################

# FUNCTIONS onlinefilmizle.tv ###### site :ok / paging : ok / liste resim : / liste film : ok
# KRAL
	def get_onlinefilmizle_categories(self, url): 
		#print 'get_onlinefilmizle_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://onlinefilmizle.tv/wp-content/uploads/2012/06/online_film_izle.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://onlinefilmizle.tv/wp-content/uploads/2012/06/online_film_izle.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://onlinefilmizle.tv/wp-content/uploads/2012/06/online_film_izle.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://onlinefilmizle.tv/wp-content/uploads/2012/06/online_film_izle.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'  

		return video_list_temp  

	def get_onlinefilmizle_category_films(self, url):
		print 'get_onlinefilmizle_category_films'
		try:              
			page = mod_request(url)
			print page
			video_list_temp = [] 
			chan_counter = 0

 			regex = re.findall(r'<div class="moviefilm">\n<a.*?href="http:\/\/(.*?)">\n<img src="http:\/\/.*?" alt="(.*?)" height=".*?".*?width=".*?".*?\/>.*?<\/a>',page)
			print regex

			for text in regex:

				url = text[0]
				title = text[1]
				title = re.sub('#8211;', '', title)
				img_url =  text[1]
				#print img_url
				#descr = descr[0]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r"<span class='current'>\d+<\/span><a href='(http:\/\/.*?)' class='page larger'>", page)
			prev = re.findall(r"<a.*?href='(.*?)'.*?class='previouspostslink'>", page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@onlinefilmizle.tv@start@ONLINEFILMIZLE KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR sinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_sinemaizle_category_films'   									    	

		return video_list_temp
		
	def get_onlinefilmizle_film(self, url): 
		print 'get_sinemaizle_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		descr = re.findall(r'<div class="konuozet">\n.*?<p><p>(.*?)<\/p>',page) 
		img = re.findall(r'<img.*?src="(.*?)".*?alt=".*?".*?height=".*?" width=".*?".*?\/>',page)
		url2 = re.findall(r'Part.*?<\/span>.*?<a.*?href="http:\/\/(.*?)">.*?<span>',page)
		for link in url2:
			page2 = mod_request(link)
			vk2 = re.findall(r'<p><iframe.*?src="(.*?)".*?width=".*?".*?height=".*?".*?frameborder=".*?"><\/iframe><\/p>',page2)
			for ll in vk2:
				vk.append(ll)
		if len(descr):
			aciklama = descr[0]
		else:
			aciklama="Konu mevcut degil"
		#url4 =re.sub("#038;", "", vk[0])
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca : ' + str(chan_counter),
					aciklama,
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp  

# FUNCTIONS onlinefilmiizlet.com ###### site :ok / paging : ok / liste resim : / liste film :
# KRAL
	def get_onlinefilmiizlet_categories(self, url): 
		#print 'get_onlinefilmiizlet_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.onlinefilmiizlet.com/wp-content/themes/tahamata-v2/images/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.onlinefilmiizlet.com/wp-content/themes/tahamata-v2/images/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'  

		return video_list_temp  

	def get_onlinefilmiizlet_category_films(self, url):
		print 'get_onlinefilmiizlet_category_films'
		try:              
			page = mod_request(url)
			print page
			video_list_temp = [] 
			chan_counter = 0

			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)".*?height="\d+".*?width="\d+".*?alt=.*?\/><\/a>',page) 
			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)&w=\d+&h=\d+&zc=\d+"<\/a>',page)
 			regex = re.findall(r'<div class="imdb.*?".*?><\/div>\n.*?\n.*?<a.*?href="http:\/\/(.*?)" title="(.*?)">\n.*?\n<img src="(http:\/\/.*?)".*?<\/a>',page)
			#descr = re.findall(r'<div.*?class="filmdetayx_aciklama"><p>\s*(.*?)<\/p>',page)
			print regex

			for text in regex:

				url = text[0]
				title = text[1]
				title = re.sub('#8211;', '', title)
				img_url =  text[2]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					url,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r"<span class='page-numbers current'>\d+<\/span>\n<a class='page-numbers' href='(http:\/\/.*?)'>\d+<\/a>", page)
			prev = re.findall(r"<a class='page-numbers' href='(.*?\d+)'>\d+<\/a>\n<span class='page-numbers current'>\d+<\/span>", page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@onlinefilmiizlet.com@start@ONLINEFILMIIZLET KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR sinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_sinemaizle_category_films'   									    	

		return video_list_temp

	def get_onlinefilmiizlet_film(self, url): 
		print 'get_hdfilmsiten_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		descr = re.findall(r'<div class="filmdetayx_aciklama">.*?<\/div>\n<p>(.*?)<\/p>',page) 
		img = re.findall(r'<div class="filmdetayx_resimimg">\n<img src="(http:\/\/.*?)" class="img" alt="" \/><\/div>',page)
		#img2 = re.findall(r'<div class="filmdetayx_aciklama">.*?<img class=".*?" title=".*?" src="(.*)" alt=".*?".*?<\/div>',page)
		url2 = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		for link in url2:
			page2 = mod_request(link)
			vk2 = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page2)
			for jj in vk2:
				vk.append(jj)
		if len(descr):
			aciklama = descr[0]
		else:
			aciklama="Konu mevcut degil"
		#url4 =re.sub("#038;", "", vk[0])
		if(len(vk)>0):
			for text in vk:
				#text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca : ' + str(chan_counter),
					aciklama,
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp

# FUNCTIONS filmifullizle.com ###### site :ok / paging : ok / liste resim : / liste film :
# KRAL
	def get_filmifullizle_categories(self, url): 
		#print 'get_filmifullizle_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://resim.filmifullizle.com/resimler/logo.jpg',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://resim.filmifullizle.com/resimler/logo.jpg',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://resim.filmifullizle.com/resimler/logo.jpg',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://resim.filmifullizle.com/resimler/logo.jpg',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmifullizle CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmifullizle_category'  

		return video_list_temp  

	def get_filmifullizle_category_films(self, url):
		#print 'get_filmifullizle_category_films'
		try:              
			page = mod_request(url)
			#print page
			video_list_temp = [] 
			chan_counter = 0

			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)".*?height="\d+".*?width="\d+".*?alt=.*?\/><\/a>',page) 
			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)&w=\d+&h=\d+&zc=\d+"<\/a>',page)
 			regex = re.findall(r'<a href="http:\/\/(.*?)"><img.*?src="(.*?)".*?alt="(.*?)" class="captify".*?><\/a>',page)

			print regex

			for text in regex:
				url = text[0]
				title = text[2]
				title = re.sub('#8211;', '', title)
				title = re.sub('&#038;', '', title)
				img_url =  text[1]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<li class="active_page"><a href=".*?">.*?<\/a><\/li>\n<li><a href="(.*?)">.*?<\/a><\/li>', page)
			prev = re.findall(r'<li><a href="(.*?)">\d+<\/a><\/li>\n<li class="active_page">', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@filmifullizle.com@start@filmifullizle KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR filmifullizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_filmifullizle_category_films' 

		return video_list_temp

	def get_filmifullizle_film(self, url): 
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<div id="konumuz".*?<iframe.*?src="(.*?)" width=".*?" height=".*?" frameborder=".*?"><\/iframe>',page)
		descr = re.findall(r'<div class="solmeta"><b>A..klama<\/b><\/div>.*?\n(.*?)<br \/>',page) 
		#img = re.findall(r'<img.*?src="(.*?)".*?alt=".*?".*?height=".*?" width=".*?".*?\/>',page)
		#sitede resim bulunmuyor
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title,
					None,
					None,
					text,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp 
		
# FUNCTIONS hdfilmsiten.com ###### site :ok / paging : ok / liste resim : / liste film :
# KRAL
	def get_hdfilmsiten_categories(self, url): 
		print 'get_sinemaizle_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.hdfilmsiten.com/wp-content/themes/temahd/c/dizifilm/webtv/c/images/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.hdfilmsiten.com/wp-content/themes/temahd/c/dizifilm/webtv/c/images/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.hdfilmsiten.com/wp-content/themes/temahd/c/dizifilm/webtv/c/images/logo.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.hdfilmsiten.com/wp-content/themes/temahd/c/dizifilm/webtv/c/images/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR hdfilmsiten CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_hdfilmsiten_category'   									    	

		return video_list_temp  

	def get_hdfilmsiten_category_films(self, url):
		print 'get_sinemaizle_category_films'
		try:              
			page = mod_request(url)
			print page
			video_list_temp = [] 
			chan_counter = 0

			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)".*?height="\d+".*?width="\d+".*?alt=.*?\/><\/a>',page) 
			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)&w=\d+&h=\d+&zc=\d+"<\/a>',page)
 			regex = re.findall(r'<div class="filmresim">\n.*?\n.*?<a.*?href="http:\/\/(.*?)" title="(.*?)"><img src="http:\/\/(.*?)".*?<\/a>',page)
			#print regex

			for text in regex:

				url = text[0]
				title = text[1]
				title = re.sub('#8211;', '', title)
				img_url =  text[2]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					url,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'span class=.current.>\d+<\/span><a  href="(http:\/\/.*?)" class="page larger">', page)
			prev = re.findall(r'<\/a><a\s+href="(.*?\d+)" class="previouspostslink">', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@hdfilmsiten.com@start@hdfilmsiten KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR hdfilmsiten CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_hdfilmsiten_category_films'   									    	

		return video_list_temp

	def get_hdfilmsiten_film(self, url): 
		print 'get_hdfilmsiten_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<p><iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe><\/p>',page)
		descr = re.findall(r'<em>(.*?)<\/em>',page) 
		img = re.findall(r'<link rel="image_src" href="(http:\/\/.*?)"\/>',page)
		url2 = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		for link in url2:
			page2 = mod_request(link)
			vk2 = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page2)
			for jj in vk2:
				vk.append(jj)
		if len(descr):
			aciklama = descr[0]
		else:
			aciklama="Konu mevcut degil"
		#url4 =re.sub("#038;", "", vk[0])
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Part : ' + str(chan_counter),
					aciklama,
					None,
					text,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp

# FUNCTIONS gunlukfilm.com ###### site : ok / paging : / liste resim : / liste film :
# KRAL
	def get_gunlukfilm_categories(self, url): 
		print 'get_sinemaizle_categories'
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://gunlukfilm.com/wp-content/themes/gunluk/images/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://gunlukfilm.com/wp-content/themes/gunluk/images/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex1 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)

			for text in regex1:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://gunlukfilm.com/wp-content/themes/gunluk/images/logo.png',
					url,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://gunlukfilm.com/wp-content/themes/gunluk/images/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR gunlukfilm CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_gunlukfilm_category'   									    	

		return video_list_temp  

	def get_gunlukfilm_category_films(self, url):
		print 'get_gunlukfilm_category_films'
		try:              
			page = mod_request(url).encode('utf-8')
			print page
			video_list_temp = [] 
			chan_counter = 0

 			regex = re.findall(r'<div class="film-baslik"><a href="http:\/\/(.*?)" title="(.*?)">.*?<\/a><\/div>',page)
			#img_url = re.findall(r'<p><img.*?src="(http://.*?)".*? width="\d+" height="\d+" .*?/>',page)
			descr = re.findall(r'<p><img.*?src="http:\/\/.*?".*?" \/><\/p>\n<p>(.*?)<\/p>',page)
			print regex
			for text in regex:
				url = text[0]
				title = text[1].replace('&#8211;',' ')
				#title = re.sub('#8211;', '', title)
				#img_url =  text[1]
				#print img_url
				descr = descr[0].replace('&#8211;','')
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					descr,
					None,
					url,
					'nStreamModul@' + url + '@film@' + title,
					None,
					None,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<li class="active_page"><a href=".*?">.*?<\/a><\/li>\n<li><a href="(http:\/\/.*?)">.*?<\/a><\/li>', page)
			prev = re.findall(r'<li><a href="(http:\/\/.*?)">\d+<\/a><\/li>\n<li class="active_page">', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@gunlukfilm.com@start@GUNLUKFILM KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR gunlukfilm CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_gunlukfilm_category_films'   									    	

		return video_list_temp

	def get_gunlukfilm_film(self, url): 
		print 'get_gunlukfilm_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe.*?src="(http:\/\/vk.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe><\/p>',page)
		descr = re.findall(r'<div.*?class="konuozet">\s*<p><\/p>\s*(.*?)\s*<\/div>',page) 
		#img = re.findall(r'<img src="(.*?)" alt=".*?" title=".*?" width="\d+" height="\d+".*?\/>',page)
		url2 = re.findall(r'Part.*?<\/span>.*?<a.*?href="http:\/\/(.*?)">.*?<span>',page)
		for link in url2:
			page2 = mod_request(link)
			vk2 = re.findall(r'<p><iframe.*?src="(.*?)".*?width=".*?".*?height=".*?".*?frameborder=".*?"><\/iframe><\/p>',page2)
			for ll in vk2:
				vk.append(ll)
		if len(descr):
			aciklama = descr[0]
		else:
			aciklama="Konu mevcut degil"
		#url4 =re.sub("#038;", "", vk[0])
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca : ' + str(chan_counter),
					aciklama,
					None,
					text,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp
		
#FUNCTIONS cizgidiyar.com ###### site :ok?? utf8 codec (film listesi) #8211; cikiyor / paging : not ok / liste resim : / liste film :
# KRAL			
	def get_cizgidiyar_categories(self, url): 
		#print 'get_kinomaxpro_categories'
		try:              
			page = mod_request(url) 
			video_list_temp = [] 

			chan_counter = 1
			
			#new = (
				#chan_counter,
				#'YENI EKLENENLER',
				#None,
				#None,
				#None,
				#'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				#None,
				#'',
				#'',
				#None,
				#None
			#)
			#video_list_temp.append(new)
			
			regex = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)
			for text in regex:
				title = text[1].upper()
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 
	   
			if(len(video_list_temp)<1):
				print 'ERROR CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_kinomaxpro_category'   									    	
		
		return video_list_temp
		
	def get_cizgidiyar_category_films(self, url):
		#print 'get_kinomaxpro_category_films'
		#try:              
		page = mod_request(url) 
		video_list_temp = [] 
		chan_counter = 0
		regex = re.findall(r'<div class="latestthumb">\n\t+<a href="http:\/\/(.*?)" title="(.*?)"><img src="http:\/\/.*? " width="\d+" height="\d+" alt=".*?"',page) 
		#img = re.findall(r'<div class="latestthumb">\n.*?<a href=".*?" title=".*?"><img src="(.*?)" width="\d+" height="\d+" alt=".*?" \/><\/a>',page)
		for text in regex:
			chan_counter +=1
			url = text[0]
			#img_url = text[2]
			title = text[1].replace('&#8211;',':')
			#descr = regex_descr[chan_counter-1]
			chan_tulpe = (
				chan_counter,
				title,
				None,
				None,
				None,
				'nStreamModul@' + url + '@film@' + title,
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(chan_tulpe)

		next = re.findall(r'<strong class=.on.>\d+<\/strong>\s+<a href="(http:\/\/.*?)">', page)
		prev = re.findall(r'</a> ... <a href="(http://.*?)', page)
                                  
		if len(next):
			self.next_page_url = next[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
			self.next_page_text = 'SONRAKI' 
			
		if len(prev):
			self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
			self.prev_page_text = 'ONCEKI'
		else:	
			self.prev_page_url = 'nStreamModul@www.cizgidiyar.com@start@KATEGORILER'
			self.prev_page_text = 'KATEGORILER'                                                 
	
		if(len(video_list_temp)<1):
				print 'ERROR CAT_FIL LIST_LEN = %s' %  len(video_list_temp) 
		#except:
			#print 'ERROR get_kinomaxpro_category'   									    	

		return video_list_temp		

	def get_cizgidiyar_film(self, url): 
		page = mod_request(url)
		chan_counter = 0
		video_list_temp = []
			
		vk = re.findall(r'<p><iframe .*?src="http:\/\/vk(.*?)".*?frameborder="\d+".*?width="\d+".*?height="\d+"><\/iframe><\/p>',page)	
		#img = re.findall(r'<img.*?src="(.*?)".*?alt=".*?"\/>',page)
		isim = re.findall(r'<h1>(.*?)</h1>',page) 
		if(len(vk)>0): 
			url = 'http://vk' + vk[0].replace('&amp;', '&') 
			chan_counter = chan_counter + 1
			title = isim[0].replace('&#8211;','-')
			chan_tulpe = (
				chan_counter,
				title,
				tanim[0],
				None,
				url,
				None,
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(chan_tulpe)

		yt = re.findall(r'<iframe.*?src="http:\/\/www.youtube.com\/embed\/(\S{11}).*?frameborder="\d+".*?width="\d+".?height="\d+"><\/iframe>',page)
		isim = re.findall(r'<center><h2 class="pagetitle">(.*?)\<\/h2><\/center>',page)
		#tanim = re.findall(r'<p><font style="font-weight:bold;">Tan.m:</font> <p>(.*?)</p>',page)

		if(len(yt)>0):
			for film in yt:
				#title = film[0] 
				url = 'http://www.youtube.com/watch?v=' + film 
				chan_counter = chan_counter + 1
				title = isim[0].replace('&#8211;','-')
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					url,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name
		
		return video_list_temp

# FUNCTIONS direkizle.net ###### site : ok / paging : / liste resim : / liste film :
# KRAL
	def get_direkizle_categories(self, url): 
		#print 'get_direkizle_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://direkizle.net/wp-content/themes/sorunsuztema/images/direkizle-11.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://direkizle.net/wp-content/themes/sorunsuztema/images/direkizle-11.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://direkizle.net/wp-content/themes/sorunsuztema/images/direkizle-11.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://direkizle.net/wp-content/themes/sorunsuztema/images/direkizle-11.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'  

		return video_list_temp  

	def get_direkizle_category_films(self, url):
		print 'get_direkizle_category_films'
		try:              
			page = mod_request(url)
			print page
			video_list_temp = [] 
			chan_counter = 0

 			regex = re.findall(r'<div class="filmbaslik"><h2><a.*?href="http:\/\/(.*?)" rel=".*?" title="(.*?)">.*?<\/a><\/h2><\/div>',page)
 			img_url = re.findall(r'<p><img.*?src="(http://.*?)".*? width="\d+" height="\d+" .*?/>',page)
			
			print regex

			for text in regex:

				url = text[0]
				title = text[1]
				title = re.sub('#8211;', '', title)
				#img_url =  text[1]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url[0],
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url[0],
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<li class="active_page"><a href=".*?">.*?<\/a><\/li>\n<li><a href="(.*?)">.*?<\/a><\/li>', page)
			prev = re.findall(r'<\/li>\s?<li><a href="(http:\/\/.*?)">\d+<\/a><\/li>\n<li class="active_page">', page)
			
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@direkizle.net@start@DIREKIZLE KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR sinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_sinemaizle_category_films'   									    	

		return video_list_temp

	def get_direkizle_film(self, url): 
		print 'get_sinemaizle_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		descr = re.findall(r'<div.*?class="konuozet">\s*<p><\/p>\s*(.*?)\s*<\/div>',page) 
		img = re.findall(r'<p><img.*?src="(http://.*?)".*? width="\d+" height="\d+" .*?/>',page)
		url2 = re.findall(r'Part.*?<\/span>.*?<a.*?href="http:\/\/(.*?)">.*?<span>',page)
		for link in url2:
			page2 = mod_request(link)
			vk2 = re.findall(r'<p><iframe.*?src="(.*?)".*?width=".*?".*?height=".*?".*?frameborder=".*?"><\/iframe><\/p>',page2)
			for ll in vk2:
				vk.append(ll)
		if len(descr):
			aciklama = descr[0]
		else:
			aciklama="Konu mevcut degil"
		#url4 =re.sub("#038;", "", vk[0])
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca : ' + str(chan_counter),
					aciklama,
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp
		
# FUNCTIONS birfilmizle.net ###### site : ok / paging : / liste resim : / liste film :
# KRAL
	def get_birfilmizle_categories(self, url): 
		#print 'get_birfilmizle_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.birfilmizle.net/wp-content/themes/CineMovie/images/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.birfilmizle.net/wp-content/themes/CineMovie/images/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.birfilmizle.net/wp-content/themes/CineMovie/images/logo.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.birfilmizle.net/wp-content/themes/CineMovie/images/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'  

		return video_list_temp  

	def get_birfilmizle_category_films(self, url):
		print 'get_direkizle_category_films'
		try:              
			page = mod_request(url)
			print page
			video_list_temp = [] 
			chan_counter = 0

 			regex = re.findall(r'<div class="soneklenen-orta">\n<a href="http:\/\/(.*?)" title="(.*?)">\n*<img src=".*?\?src=(http:\/\/.*?)&.*?<\/a>',page)
			print regex

			for text in regex:

				url = text[0]
				title = text[1]
				title = re.sub('#8211;', '', title)
				img_url =  text[2]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r"<span class='current'>\d+<\/span><a href='(.*?)' class.*?>", page)
			prev = re.findall(r"<a href='(http://www.birfilmizle.net/page/\d+)' class='page smaller'>\d+</a><span class='current'>\d+</span>", page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@birfilmizle.net@start@BIRFILMIZLE KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR sinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_sinemaizle_category_films'   									    	

		return video_list_temp

	def get_birfilmizle_film(self, url): 
		print 'get_sinemaizle_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		descr = re.findall(r'<div class="detaylaricc">Konusu : <span><p>(.*?)</p>',page) 
		img = re.findall(r'<div class="vizyon-film-orta">\n<a href=".*?" title=".*?"><img src=".*?src=(.*?jpg)&.*?" alt=".*?"\/><\/a>',page)
		url2 = re.findall(r'Part.*?<\/span>.*?<a.*?href="http:\/\/(.*?)">.*?<span>',page)
		for link in url2:
			page2 = mod_request(link)
			vk2 = re.findall(r'<p><iframe.*?src="(.*?)".*?width=".*?".*?height=".*?".*?frameborder=".*?"><\/iframe><\/p>',page2)
			for ll in vk2:
				vk.append(ll)
		if len(descr):
			aciklama = descr[0]
		else:
			aciklama="Konu mevcut degil"
		#url4 =re.sub("#038;", "", vk[0])
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca : ' + str(chan_counter),
					aciklama,
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp

# FUNCTIONS cinemaizle.org ###### site : / paging :  / liste resim : / liste film : 
# KRAL
	def get_cinemaizle_categories(self, url): 
		#print 'get_cinemaizle_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://cinemaizle.org/wp-content//themes/zadev2/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://cinemaizle.org/wp-content//themes/zadev2/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			#regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)
			regex2 = re.findall(r'<li class="cat-item cat-item-\d+"><a href="http:\/\/(.*?)" title=".*?">(.*?)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://cinemaizle.org/wp-content//themes/zadev2/logo.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://cinemaizle.org/wp-content//themes/zadev2/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR cinemaizle CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_cinemaizle_category'  

		return video_list_temp  

	def get_cinemaizle_category_films(self, url):
		#print 'get_cinemaizle_category_films'
		try:              
			page = mod_request(url)
			#print page
			video_list_temp = [] 
			chan_counter = 0

 			regex = re.findall(r'<div class="ana-resim"><a href="http:\/\/(.*?)" ><img src=".*?src=(http:\/\/.*?)&.*? alt="(.*?)" \/><\/a>',page)

			print regex
			for text in regex:
				url = text[0]
				title = text[2]
				title = re.sub('#8211;', '', title)
				#title = re.sub('&#038;', '', title)
				img_url =  text[1]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<span class=.current.>\d+</span><a href=.(http:\/\/\b[^>]*). class=.page larger.>', page)
			prev = re.findall(r'<a href=.(http:\/\/\b[^>]*). class=.page smaller.>\d+<\/a><span class=.current.>', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@cinemaizle.org@start@cinemaizle KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR cinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_cinemaizle_category_films' 

		return video_list_temp

	def get_cinemaizle_film(self, url): 
		print 'get_cinemaizle_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		#mailru = re.findall(r'><embed src="\/filmplayer.swf\?file=(.*?)" quality', page)
		descr = re.findall(r'<h1>.*?</h1>\n<p>(.*?)<br \/>',page) 
		img = re.findall(r'<div class="aciklamaresim">\n<img src=".*?src=(http:\/\/.*?)&.*?<\/div>',page)
		
		url22 = re.findall(r'<a href="http:\/\/(.*?)">K.*?m \d+<\/a>', page)
		
		for link in url22:
			#page2 = mod_request(self.active_site_url + link)
			page2 = mod_request(link)
			vk2 = re.findall(r'<iframe\Wsrc="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>', page2)
			#mailru2 = re.findall(r'><embed src="\/filmplayer.swf\?file=(.*?)" quality', page2)

			for jj in vk2:
				vk.append(jj)
		if len(descr):
			aciklama = descr[0]
		else:
			aciklama="Konu mevcut degil"
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca : ' + str(chan_counter),
					aciklama,
					img,
					text,
					None,
					None,
					img,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
				
		yt = re.findall(r'<iframe width="\d+".?height="\d+" src="http:\/\/www.youtube.com\/embed\/(\S{11}).*?frameborder="\d+".*?><\/iframe>',page)
		isim = re.findall(r'<h2 class="baslik"><a href=".*?" rel="bookmark" title="(.*?)">.*?<\/a><\/h2>',page)
		if(len(yt)>0):
			for film in yt:
				#title = film[0] 
				url = 'http://www.youtube.com/watch?v=' + film 
				chan_counter = chan_counter + 1
				title = isim[0]
				chan_tulpe = (
					chan_counter,
					title  + ' Parca : ' + str(chan_counter),
					'',
					None,
					url,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)
				
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp  
		
# FUNCTIONS filmtekpart.com ###### site : / paging :  / liste resim : / liste film : 
# KRAL
	def get_filmtekpart_categories(self, url): 
		#print 'get_filmtekpart_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.filmtekpart.com/wp-content/themes/tahamata-V2/images/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.filmtekpart.com/wp-content/themes/tahamata-V2/images/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			#regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)
			regex2 = re.findall(r'<li\Wclass="cat-item cat-item-\d+"><a\nhref="http:\/\/(.*?)" title=".*?">(.*)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.filmtekpart.com/wp-content/themes/tahamata-V2/images/logo.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.filmtekpart.com/wp-content/themes/tahamata-V2/images/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmtekpart CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmtekpart_category'  

		return video_list_temp  

	def get_filmtekpart_category_films(self, url):
		#print 'get_filmtekpart_category_films'
		try:              
			page = mod_request(url)
			#print page
			video_list_temp = [] 
			chan_counter = 0

			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)".*?height="\d+".*?width="\d+".*?alt=.*?\/><\/a>',page) 
			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)&w=\d+&h=\d+&zc=\d+"<\/a>',page)
 			#regex = re.findall(r'<a href="http:\/\/(.*?)"><img.*?src="(.*?)".*?alt="(.*?)" class="captify".*?><\/a>',page)
 			regex = re.findall(r'<a\Whref="http:\/\/(.*?)" title="(.*?)"><img\Wsrc="(.*?)" class="img" alt="" \/><\/a>',page)
			print regex

			for text in regex:

				url = text[0]
				title = text[1]
				title = re.sub('&#8211;', '', title)
				title = re.sub('&#038;', '', title)
				img_url =  text[2]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r"<span class='current'>\d+</span><a href='(http://.*?)' class='page larger'>", page)
			prev = re.findall(r"class='page-numbers' href='(http://.*?)'>\d+<\/a> <span\nclass='page-numbers current'>\d+</span>", page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@filmtekpart.com@start@filmtekpart KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR filmtekpart CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_filmtekpart_category_films' 

		return video_list_temp

	def get_filmtekpart_film(self, url): 
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		#vk = re.findall(r'<p><iframe.*?src="(.*?)" width=".*?" height=".*?" frameborder=".*?"><\/iframe>',page)
		vk = re.findall(r'<iframe\Wsrc="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		descr = re.findall(r'class="filmdetayx_aciklama"><p>(.*)<a',page) 
		img = re.findall(r'<div\nclass="filmdetayx_resimimg"> <img\nsrc="(http:\/\/.*?)" class="img" alt="" /></div>',page)
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca :' + str(chan_counter),
					descr[0],
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp 

# FUNCTIONS divxfilmizle.net ###### site : / paging :  / liste resim : / liste film : 
# KRAL
	def get_divxfilmizle_categories(self, url): 
		#print 'get_divxfilmizle_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.divxfilmizle.net/wp-content/themes/inove/img/header.jpg',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.divxfilmizle.net/wp-content/themes/inove/img/header.jpg',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li class="cat-item cat-item-\d+"><a href="http:\/\/(.*?)" title=".*?">(.*?)<\/a>',page)
			#regex2 = re.findall(r'<li\Wclass="cat-item cat-item-\d+"><a\nhref="http:\/\/(.*?)" title=".*?">(.*)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.divxfilmizle.net/wp-content/themes/inove/img/header.jpg',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.divxfilmizle.net/wp-content/themes/inove/img/header.jpg',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR divxfilmizle CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_divxfilmizle_category'  

		return video_list_temp  

	def get_divxfilmizle_category_films(self, url):
		print 'get_divxfilmizle_category_films'
		try:              
			page = mod_request(url)
			#print page
			video_list_temp = [] 
			chan_counter = 0

			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)".*?height="\d+".*?width="\d+".*?alt=.*?\/><\/a>',page) 
			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)&w=\d+&h=\d+&zc=\d+"<\/a>',page)
 			regex = re.findall(r'<h2><a class="title" href="http:\/\/(.*?)" rel="bookmark">(.*?)<\/a><\/h2>',page)
 			##img_url = re.findall(r'<div class="content">\n.*?<p><img src="(http:\/\/.*?)"',page)
			##descr = re.findall(r'<strong>Film Konusu:<\/strong><\/span>(.*?)<br \/>',page)

			print regex

			for text in regex:

				url = text[0]
				title = text[1]
				title = re.sub('#8211;', '', title)
				#title = re.sub('&#038;', '', title)
				#img_url =  text[2]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					None,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<span class=.current.>\d+<\/span><a href=.(http:\/\/\b[^>]*). class=.page larger.>', page)
			prev = re.findall(r'<a href=.(http:\/\/\b[^>]*). class=.page smaller.>\d+<\/a><span class=.current.>', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@divxfilmizle.net@start@DIVXFILMIZLE KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR divxfilmizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_divxfilmizle_category_films' 

		return video_list_temp

	def get_divxfilmizle_film(self, url): 
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		#vk = re.findall(r'<p><iframe.*?src="(.*?)" width=".*?" height=".*?" frameborder=".*?"><\/iframe>',page)
		vk = re.findall(r'<iframe src="(http:\/\/.*)" frameborder="\d+" height="\d+" width="\d+"><\/iframe><\/p>',page)
		#descr = re.findall(r'<strong>Film Konusu:<\/strong><\/span>(.*?)<br \/>',page) 
		#img = re.findall(r'<p><img src="(http:\/\/.*?)" alt="" title=".*?" width="\d+" height="\d+".*? \/>',page)
		if(len(vk)>0):
			for text in vk:
				text=text.replace("amp;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca :' + str(chan_counter),
					None,
					None,
					text,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		

		yt = re.findall(r'<iframe width="\d+".?height="\d+" src="http:\/\/www.youtube.com\/embed\/(\S{11}).*?frameborder="\d+".*?><\/iframe>',page)
		isim = re.findall(r'<p><img class="alignleft size-full wp-image-\d+" title="(.*?)"',page)
		if(len(yt)>0):
			for film in yt:
				#title = film[0] 
				url = 'http://www.youtube.com/watch?v=' + film 
				chan_counter = chan_counter + 1
				title = isim[0]
				chan_tulpe = (
					chan_counter,
					title  + ' Parca : ' + str(chan_counter),
					'',
					None,
					url,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp 

# FUNCTIONS www.yenifilmler-izle.com ###### site : / paging :  / liste resim : / liste film : 
# KRAL
	def get_yenifilmlerizle_categories(self, url): 
		#print 'get_yenifilmlerizle_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.yenifilmler-izle.com/wp-content/themes/CineMovieV2-Blue/images/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.yenifilmler-izle.com/wp-content/themes/CineMovieV2-Blue/images/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)
			#regex2 = re.findall(r'<li\Wclass="cat-item cat-item-\d+"><a\nhref="http:\/\/(.*?)" title=".*?">(.*)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.yenifilmler-izle.com/wp-content/themes/CineMovieV2-Blue/images/logo.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.yenifilmler-izle.com/wp-content/themes/CineMovieV2-Blue/images/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR yenifilmlerizle CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_yenifilmlerizle_category'  

		return video_list_temp  

	def get_yenifilmlerizle_category_films(self, url):
		#print 'get_yenifilmlerizle_category_films'
		try:              
			page = mod_request(url)
			#print page
			video_list_temp = [] 
			chan_counter = 0

			regex = re.findall(r'<div class="soneklenen-orta">\n<a href="http:\/\/(.*?)" title="(.*?)"><img src="(http:\/\/.*?)".*?\/><\/a>',page) 
			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)&w=\d+&h=\d+&zc=\d+"<\/a>',page)
 			#regex = re.findall(r'<a href="http:\/\/(.*?)"><img.*?src="(.*?)".*?alt="(.*?)" class="captify".*?><\/a>',page)
 			#regex = re.findall(r'<a\Whref="http:\/\/(.*?)" title="(.*?)"><img\Wsrc="(.*?)" class="img" alt="" \/><\/a>',page)
			print regex

			for text in regex:

				url = text[0]
				title = text[1]
				title = re.sub('&#8211;', '', title)
				title = re.sub('&#038;', '', title)
				img_url =  text[2]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<span class=.current.>\d+<\/span><a href=.(http:\/\/\b[^>]*). class=.page larger.>', page)
			prev = re.findall(r'<a href=.(http:\/\/\b[^>]*). class=.page smaller.>\d+<\/a><span class=.current.>', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@yenifilmler-izle.com@start@yenifilmlerizle KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR yenifilmlerizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_yenifilmlerizle_category_films' 

		return video_list_temp

	def get_yenifilmlerizle_film(self, url): 
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		#vk = re.findall(r'<p><iframe.*?src="(.*?)" width=".*?" height=".*?" frameborder=".*?"><\/iframe>',page)
		vk = re.findall(r'<iframe\Wsrc="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		#descr = re.findall(r'<div class="detaylaricc">Filmin <span>.zeti</span><p>(.*?)</p>',page) 
		#img = re.findall(r'<div class="konu-iciresim"><img src="(.*?)" alt=".*?"/></div>',page)
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca :' + str(chan_counter),
					None,
					None,
					text,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp 
		
# FUNCTIONS www.hdfilmtube.com ###### site : / paging :  / liste resim : / liste film : 
# KRAL
	def get_hdfilmtube_categories(self, url): 
		#print 'get_hdfilmtube_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.hdfilmtube.com/wp-content/themes/blackman/images/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.hdfilmtube.com/wp-content/themes/blackman/images/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.hdfilmtube.com/wp-content/themes/blackman/images/logo.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.hdfilmtube.com/wp-content/themes/blackman/images/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR hdfilmtube CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_hdfilmtube_category'  

		return video_list_temp  

	def get_hdfilmtube_category_films(self, url):
		#print 'get_hdfilmtube_category_films'
		try:              
			page = mod_request(url)
			#print page
			video_list_temp = [] 
			chan_counter = 0

			regex = re.findall(r'<div class="baslik"><div class="bb"><a href="http:\/\/(.*)" title="(.*?)">',page) 
			img_url = re.findall(r'<div class="afis "><div id=".*?"><\/div><a href=".*?" title=".*?"><img src="(.*?)" \/><\/a><\/div>',page)
 			#regex = re.findall(r'<a href="http:\/\/(.*?)"><img.*?src="(.*?)".*?alt="(.*?)" class="captify".*?><\/a>',page)
 			#regex = re.findall(r'<a\Whref="http:\/\/(.*?)" title="(.*?)"><img\Wsrc="(.*?)" class="img" alt="" \/><\/a>',page)
			print regex

			for text in regex:

				url = text[0]
				title = text[1]
				title = re.sub('&#8211;', '', title)
				title = re.sub('&#038;', '', title)
				#img_url =  text[2]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url[0],
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url[0],
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<span class=.current.>\d+<\/span><a href=.(http:\/\/\b[^>]*). class=.page larger.>', page)
			prev = re.findall(r'<a href=.(http:\/\/\b[^>]*). class=.page smaller.>\d+<\/a><span class=.current.>', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@hdfilmtube.com@start@hdfilmtube KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR hdfilmtube CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_hdfilmtube_category_films' 

		return video_list_temp
		
	def get_hdfilmtube_film(self, url): 
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		#vk = re.findall(r'<p><iframe.*?src="(.*?)" width=".*?" height=".*?" frameborder=".*?"><\/iframe>',page)
		vk = re.findall(r'<iframe\Wsrc="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		#descr = re.findall(r'<div class="konu">\n<span class="pas">Konusu: <\/span> (.*?)\n</div>',page) 
		#img = re.findall(r'<a href="(.*?)" rel="lightbox"><img id="afisimdostumm" src="http:\/\/.*?" alt=".*?"\/><\/a>',page)
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca :' + str(chan_counter),
					None,
					None,
					text,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp 

# FUNCTIONS filmizlehep.com ###### site : ok / paging : ok  / liste resim : ok / liste film : 
# KRAL
	def get_filmizlehep_categories(self, url): 
		#print 'get_filmizlehep_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://filmizlehep.com/wp-content/themes/filmizlehep/images/header_zemin.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://filmizlehep.com/wp-content/themes/filmizlehep/images/header_zemin.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://filmizlehep.com/wp-content/themes/filmizlehep/images/header_zemin.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://filmizlehep.com/wp-content/themes/filmizlehep/images/header_zemin.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmizlehep CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmizlehep_category'  

		return video_list_temp  

	def get_filmizlehep_category_films(self, url):
		#print 'get_filmizlehep_category_films'
		try:              
			page = mod_request(url)
			#print page
			video_list_temp = [] 
			chan_counter = 0

			regex = re.findall(r'<div class="cover">\n\n<img src=".*?" \/>\n<a  href="http:\/\/(.*)" rel=".*?"><img src="(.*?)" height=".*?" width=".*?" alt="(.*?)" class="captify" \/><\/a>',page) 
			#img_url = re.findall(r'<div class="afis"><div id=".*?"><\/div><a href=".*?" title=".*?"><img src="(.*?)" \/><\/a><\/div>',page)
 			#regex = re.findall(r'<a href="http:\/\/(.*?)"><img.*?src="(.*?)".*?alt="(.*?)" class="captify".*?><\/a>',page)
 			#regex = re.findall(r'<a\Whref="http:\/\/(.*?)" title="(.*?)"><img\Wsrc="(.*?)" class="img" alt="" \/><\/a>',page)
			print regex

			for text in regex:

				url = text[0]
				title = text[2]
				title = re.sub('&#8211; ', '', title)
				title = re.sub('&#038;', '', title)
				img_url =  text[1]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<span class=.current.>\d+<\/span><a\s+href=.(http:\/\/\b[^>]*). class=.page larger.>', page)
			prev = re.findall(r'<a\s+href=.(http:\/\/\b[^>]*). class=.page smaller.>\d+<\/a><span class=.current.>', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@filmizlehep.net@start@filmizlehep KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR filmizlehep CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_filmizlehep_category_films' 

		return video_list_temp
		
	def get_filmizlehep_film(self, url): 
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		#vk = re.findall(r'<p><iframe.*?src="(.*?)" width=".*?" height=".*?" frameborder=".*?"><\/iframe>',page)
		vk = re.findall(r'<iframe\Wsrc="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		#descr = re.findall(r'<li><h4>Hakk.nda</h4><span>(.*?)<\/span><\/li>',page) 
		#img = re.findall(r'<a  href="http:\/\/.*?" rel="bookmark"><img src="(.*?)" alt=".*?" class="afis" \/><\/a>',page)
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca :' + str(chan_counter),
					None,
					None,
					text,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp 
		
# FUNCTIONS filmhani.com ###############################################################################################################
# KRAL
	def get_filmhani_categories(self, url): 
		print 'get_filmhani_categories'
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.filmhani.com/wp-content/uploads/2012/07/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.filmhani.com/wp-content/uploads/2012/07/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex1 = re.findall(r'<li><a href="http:\/\/(www.filmhani.com.*?)">(.*?)<\/a><\/li>',page)

			for text in regex1:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.filmhani.com/wp-content/uploads/2012/07/logo.png',
					url,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.filmhani.com/wp-content/uploads/2012/07/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmhani CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmhani_category'   									    	

		return video_list_temp  

	def get_filmhani_category_films(self, url):
		print 'get_filmhani_category_films'
		try:              
			page = mod_request(url).encode('utf-8')
			print page
			video_list_temp = [] 
			chan_counter = 0

 			regex = re.findall(r'div class="cover_kapsul"> <a href="http:\/\/(.*?)" title=""> <img width="\d+" height="\d+" src="(.*?)" class=".*?" alt="(.*?)" title=""[\b[^>]*.',page)

			print regex
			for text in regex:
				url = text[0]
				title = text[2]
				title = re.sub('#8211;', '', title)
				img_url =  text[1]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					url,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<span class=.current.>\d+</span><a href=.(http:\/\/\b[^>]*). class=.page larger.>', page)
			prev = re.findall(r'<a href=.(http:\/\/\b[^>]*). class=.page smaller.>\d+<\/a><span class=.current.>', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@filmhani.com@start@FILMHANI KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           



			if(len(video_list_temp)<1):
				print 'ERROR filmhani CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_filmhani_category_films'   									    	

		return video_list_temp

	def get_filmhani_film(self, url): 
		print 'get_filmhani_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		#mailru = re.findall(r'><embed src="\/filmplayer.swf\?file=(.*?)" quality', page)
		descr = re.findall(r'<h1>.*?</h1>\n<p>(.*?)<br \/>',page) 
		img = re.findall(r'<div class="aciklamaresim">\n<img src=".*?src=(http:\/\/.*?)&.*?<\/div>',page)
		
		url22 = re.findall(r'<a href="http:\/\/(.*?)">K.*?m \d+<\/a>', page)
		
		for link in url22:
			#page2 = mod_request(self.active_site_url + link)
			page2 = mod_request(link)
			vk2 = re.findall(r'<iframe\Wsrc="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>', page2)
			#mailru2 = re.findall(r'><embed src="\/filmplayer.swf\?file=(.*?)" quality', page2)

			for jj in vk2:
				vk.append(jj)
		if len(descr):
			aciklama = descr[0]
		else:
			aciklama="Konu mevcut degil"
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca : ' + str(chan_counter),
					aciklama,
					img,
					text,
					None,
					None,
					img,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
				
		yt = re.findall(r'<iframe width="\d+".?height="\d+" src="http:\/\/www.youtube.com\/embed\/(\S{11}).*?frameborder="\d+".*?><\/iframe>',page)
		isim = re.findall(r'<title>(.*?)</title><link rel="pingback"',page)
		if(len(yt)>0):
			for film in yt:
				#title = film[0] 
				url = 'http://www.youtube.com/watch?v=' + film 
				chan_counter = chan_counter + 1
				title = isim[0]
				chan_tulpe = (
					chan_counter,
					title  + ' Parca : ' + str(chan_counter),
					'',
					None,
					url,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)
				
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp  

# FUNCTIONS belgeseltv.net ###############################################################################################################
# KRAL
	def get_belgeseltvnet_categories(self, url): 
		print 'get_belgeseltvnet_categories'
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex1 = re.findall(r'<li id="menu-item-.*?" class=".*?"><a href="http:\/\/(www.belgeseltv.net/kategori.*?)">(.*?)<\/a><\/li>',page)

			for text in regex1:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'',
					url,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR belgeseltvnet CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_belgeseltvnet_category'   									    	

		return video_list_temp  

	def get_belgeseltvnet_category_films(self, url):
		print 'get_sinemaizle_category_films'
		try:              
			page = mod_request(url).encode('utf-8')
			print page
			video_list_temp = [] 
			chan_counter = 0

 			regex = re.findall(r'<div class="cover"><a href="http:\/\/(.*?)" rel="bookmark" title="(.*?)"><img src=".*?src=(http:\/\/.*?)&.*?width=".*?" height=".*?" alt=".*?" \/><\/a><\/div>',page)

			print regex
			for text in regex:
				url = text[0]
				title = text[1]
				title = re.sub('#8211;', '', title)
				img_url =  text[2]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					url,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<p><a href="http:\/\/(.*?)" >.*?nceki Sayfalar<\/a><a href=".*" >Sonraki Sayfalar &raquo;</a></p>', page)
			prev = re.findall(r'<p><a href="http:\/\/.*?" >.*?nceki Sayfalar<\/a><a href="(.*)" >Sonraki Sayfalar &raquo;</a></p>', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@belgeseltv.net@start@belgeseltvnet KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           



			if(len(video_list_temp)<1):
				print 'ERROR belgeseltvnet CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_belgeseltvnet_category_films'   									    	

		return video_list_temp

	def get_belgeseltvnet_film(self, url): 
		print 'get_belgeseltvnet_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe src="(.*?)" frameborder="\d+" width="\d+" height="\d+"><\/iframe><\/p>',page)
		descr = re.findall(r'<div.*?class="konuozet">\s*<p><\/p>\s*(.*?)\s*<\/div>',page) 
		img = re.findall(r'<img.*?src="(.*?)".*?alt=".*?".*?height=".*?" width=".*?".*?\/>',page)
		url2 = re.findall(r'Part.*?<\/span>.*?<a.*?href="http:\/\/(.*?)">.*?<span>',page)
		for link in url2:
			page2 = mod_request(link)
			vk2 = re.findall(r'<p><iframe.*?src="(.*?)".*?width=".*?".*?height=".*?".*?frameborder=".*?"><\/iframe><\/p>',page2)
			for ll in vk2:
				vk.append(ll)
		if len(descr):
			aciklama = descr[0]
		else:
			aciklama="Konu mevcut degil"
		#url4 =re.sub("#038;", "", vk[0])
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca : ' + str(chan_counter),
					aciklama,
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		

		yt = re.findall(r'<param name="movie" value="http:\/\/www.youtube.com\/v\/(\S{11}).*? \/><param name=".*?" value=".*?" \/>',page)
		isim = re.findall(r'<h1><a href="http:\/\/.*?" rel="bookmark" title=".*?">(.*?)<\/a><\/h1>',page)
		if(len(yt)>0):
			for film in yt:
				#title = film[0] 
				url = 'http://www.youtube.com/watch?v=' + film 
				chan_counter = chan_counter + 1
				title = isim[0]
				chan_tulpe = (
					chan_counter,
					title  + ' Parca : ' + str(chan_counter),
					'',
					None,
					url,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)
				
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp 
		
# FUNCTIONS seyretogren.com ###### site : / paging :  / liste resim : / liste film : 
# KRAL
	def get_seyretogren_categories(self, url): 
		print 'get_seyretogren_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			# new = (
				# chan_counter,
				# 'Yeni Eklenenler',
				# None,
				# 'http://www.seyretogren.com/templates/ja_lead/images/logo.png',
				# None,
				# 'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				# None,
				# 'http://www.seyretogren.com/templates/ja_lead/images/logo.png',
				# '',
				# None,
				# None
			# )
			# video_list_temp.append(new)

			regex2 = re.findall(r'<a href="(.*?)">.*?<\/a> \x7C',page)

			for text in regex2:
				title = text
				url = 'www.seyretogren.com/'+ text
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.seyretogren.com/templates/ja_lead/images/logo.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.seyretogren.com/templates/ja_lead/images/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR seyretogren CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_seyretogren_category'  

		return video_list_temp  

	def get_seyretogren_category_films(self, url):
		#print 'get_seyretogren_category_films'
		try:              
			page = mod_request(url)
			#print page
			video_list_temp = [] 
			chan_counter = 0

 			regex = re.findall(r'<h4><a href="\/(.*?)" title="(.*?)">.*?<\/a><\/h4>',page)
			#title = re.findall(r'<h4><a href="\/.*?" title="(.*?)">.*?<\/a><\/h4>',page)
			print regex

			for text in regex:

				url = text[0]
				#title = text[1].decode("utf-8")
				title = text[1]
				#title = re.sub('#8211;', '', title)
				#title = re.sub('&#038;', '', title)
				#img_url =  text[1]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + 'www.seyretogren.com/' + url + '@film@' + title,
					None,
					None,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<li class="active_page"><a href=".*?">.*?<\/a><\/li>\n<li><a href="(.*?)">.*?<\/a><\/li>', page)
			prev = re.findall(r'<li><a href="(.*?)">\d+<\/a><\/li>\n<li class="active_page">', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@seyretogren.com@start@seyretogren KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR seyretogren CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_seyretogren_category_films' 

		return video_list_temp

	def get_seyretogren_film(self, url): 
		print 'get_seyretogren_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<div class="videotitleinmodule" ><a href=http:\/\/(.*?)>.*?<\/a>',page)
		#descr = re.findall(r'<h1>.*?</h1>\n<p>(.*?)<br \/>',page) 
		#img = re.findall(r'<div class="aciklamaresim">\n<img src=".*?src=(http:\/\/.*?)&.*?<\/div>',page)
		url22 = re.findall(r'<div class="videotitleinmodule"><a href=http:\/\/(.*?)>.*?<\/a>', page)
		
		for link in url22:
			#page2 = mod_request(self.active_site_url + link)
			page2 = mod_request(link)
			vk2 = re.findall(r'<param name="flashvars" value="file=(.*?)&amp;autostart=true">', page2)

			for jj in vk2:
				vk.append(jj)

		if(len(vk)>0):
			for text in vk:
				#text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + str(chan_counter),
					None,
					None,
					text,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp  	
		
# FUNCTIONS vkfilmizle.com ###### site : / paging :  / liste resim : / liste film : 						
# KRAL
	def get_vkfilmizle_categories(self, url):
		#print 'get_vkfilmizle_categories'
		try:
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1

			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.vkfilmizle.com/wp-content/themes/tahamata/images/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.vkfilmizle.com/wp-content/themes/tahamata/images/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li\Wclass="cat-item cat-item-\d+"><a  href="http:\/\/(.*?)" title=".*?">(.*)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.vkfilmizle.com/wp-content/themes/tahamata/images/logo.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.vkfilmizle.com/wp-content/themes/tahamata/images/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR vkfilmizle CAT LIST_LEN = %s' %  len(video_list_temp)
		except:
			print 'ERROR get_vkfilmizle_category'

		return video_list_temp

	def get_vkfilmizle_category_films(self, url):
		#print 'get_vkfilmizle_category_films'
		try:
			page = mod_request(url)
			#print page
			video_list_temp = []
			chan_counter = 0

 			regex = re.findall(r'<a  href="http:\/\/(.*?)" title="(.*?)"><img src="(http:\/\/.*?)" alt=".*?" class="thumbnail" width="\d+" height="\d+"\/></a>',page)
			#print regex

			for text in regex:

				url = text[0]
				title = text[1]
				title = title.replace("&#8211;", "")
				#title = re.sub('#8211;', '', title)
				#title = re.sub('&#038;', '', title)
				img_url =  text[2]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<span class=.page-numbers current.>\d+<\/span>\n<a  class="page-numbers" href=.(http:\/\/\b[^>]*)', page)
			prev = re.findall(r'<a  class="page-numbers" href=.(http:\/\/\b[^>]*).>\d+<\/a>\n<span class=.page-numbers current.>', page)

			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 

			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:
				self.prev_page_url = 'nStreamModul@vkfilmizle.com@start@vkfilmizle KATEGORILER'
				self.prev_page_text = 'KATEGORILER'

			if(len(video_list_temp)<1):
				print 'ERROR vkfilmizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)
		except:
			print 'ERROR get_vkfilmizle_category_films'

		return video_list_temp

	def get_vkfilmizle_film(self, url):
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		#vk = re.findall(r'<p><iframe.*?src="(.*?)" width=".*?" height=".*?" frameborder=".*?"><\/iframe>',page)
		vk = re.findall(r'<iframe\Wsrc="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		descr = re.findall(r'<div class="filmdetayx_aciklama"><p>(.*?)<\/p>',page) 
		img = re.findall(r'<div class="filmdetayx_resim">\W+<img src="(.*?)" alt=".*?" class="resimboyut" \/>',page)
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + "parca :" + str(chan_counter),
					descr[0],
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name

		return video_list_temp 

# FUNCTIONS movietr.org ###### site : / paging :  / liste resim : / liste film : 						
# KRAL
	def get_movietr_categories(self, url):
		#print 'get_movietr_categories'
		try:
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1

			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://d1206.hizliresim.com/y/d/7tv7z.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://d1206.hizliresim.com/y/d/7tv7z.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li class="cat-item cat-item-\d+"><a href="http:\/\/(.*?)" title=".*?">(.*)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://d1206.hizliresim.com/y/d/7tv7z.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://d1206.hizliresim.com/y/d/7tv7z.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR movietr CAT LIST_LEN = %s' %  len(video_list_temp)
		except:
			print 'ERROR get_movietr_category'

		return video_list_temp

	def get_movietr_category_films(self, url):
		#print 'get_movietr_category_films'
		try:
			page = mod_request(url)
			#print page
			video_list_temp = []
			chan_counter = 0

 			regex = re.findall(r'<a href="http:\/\/(.*?)" rel="bookmark" title="(.*?)"><img src="(.*?)" height="\d+" width="\d+" alt="" \/><\/a>',page)
			print regex

			for text in regex:

				url = text[0]
				title = text[1]
				#title = re.sub('#8211;', '', title)
				#title = re.sub('&#038;', '', title)
				img_url =  text[2]
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<span class=.page-numbers current.>\d+<\/span>\n<a  class="page-numbers" href=.(http:\/\/\b[^>]*)', page)
			prev = re.findall(r'<a  class="page-numbers" href=.(http:\/\/\b[^>]*).>\d+<\/a>\n<span class=.page-numbers current.>', page)

			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 

			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:
				self.prev_page_url = 'nStreamModul@movietr.org@start@movietr KATEGORILER'
				self.prev_page_text = 'KATEGORILER'

			if(len(video_list_temp)<1):
				print 'ERROR movietr CAT_FIL LIST_LEN = %s' %  len(video_list_temp)
		except:
			print 'ERROR get_movietr_category_films'

		return video_list_temp

	def get_movietr_film(self, url):
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		#vk = re.findall(r'<p><iframe.*?src="(.*?)" width=".*?" height=".*?" frameborder=".*?"><\/iframe>',page)
		vk = re.findall(r'<iframe\Wsrc="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		#descr = re.findall(r'Konu:.*?<\/strong>(.*?)\s*<\w+',page) 
		#img = re.findall(r'<img.*?src="(.*?)".*?alt=".*?".*?height=".*?" width=".*?".*?\/>',page)
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + "parca :" + str(chan_counter),
					None,
					None,
					text,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name

		return video_list_temp 

# FUNCTIONS filmodam.com ###### site : / paging :  / liste resim : / liste film : 						
# KRAL
	def get_filmodam_categories(self, url):
		#print 'get_filmodam_categories'
		try:
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1

			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.filmodam.com/wp-content/uploads/2012/06/FILMODAM1.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.filmodam.com/wp-content/uploads/2012/06/FILMODAM1.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li class="cat-item cat-item-\d+"><a  href="http:\/\/(.*?)" title=".*?">(.*)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.filmodam.com/wp-content/uploads/2012/06/FILMODAM1.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.filmodam.com/wp-content/uploads/2012/06/FILMODAM1.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmodam CAT LIST_LEN = %s' %  len(video_list_temp)
		except:
			print 'ERROR get_filmodam_category'

		return video_list_temp

	def get_filmodam_category_films(self, url):
		#print 'get_filmodam_category_films'
		try:
			page = mod_request(url)
			#print page
			video_list_temp = []
			chan_counter = 0

 			regex = re.findall(r'<a  href="http:\/\/(.*?)" rel="bookmark" title="(.*?)"><img src="(.*?)" height="\d+" width="\d+" alt="" \/><\/a>',page)
			print regex

			for text in regex:

				url = text[0]
				title = text[1]
				#title = re.sub('#8211;', '', title)
				#title = re.sub('&#038;', '', title)
				img_url =  text[2]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<span class=.current.>\d+</span><a href=.(http:\/\/\b[^>]*). class=.page larger.>', page)
			prev = re.findall(r'<a  href=.(http:\/\/\b[^>]*). class=.page smaller.>\d+<\/a><span class=.current.>', page)

			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 

			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:
				self.prev_page_url = 'nStreamModul@filmodam.com@start@filmodam KATEGORILER'
				self.prev_page_text = 'KATEGORILER'

			if(len(video_list_temp)<1):
				print 'ERROR filmodam CAT_FIL LIST_LEN = %s' %  len(video_list_temp)
		except:
			print 'ERROR get_filmodam_category_films'

		return video_list_temp

	def get_filmodam_film(self, url):
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe\Wsrc="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		#descr = re.findall(r'Konu:.*?<\/strong>(.*?)\s*<\w+',page) 
		img = re.findall(r'<div class="filmaltiimg">\W+<img src="(http:\/\/.*?)" alt=".*?" height="\d+" width="\d+" \/>',page)
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + "parca :" + str(chan_counter),
					None,
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name

		return video_list_temp 

# FUNCTIONS gercekfilmler.com ###### site : / paging :  / liste resim : / liste film : 						
# KRAL
	def get_gercekfilmler_categories(self, url):
		#print 'get_gercekfilmler_categories'
		try:
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1

			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.gercekfilmler.com/wp-content/themes/filmizle/images/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.gercekfilmler.com/wp-content/themes/filmizle/images/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li class="cat-item cat-item-\d+"><a href="http:\/\/(.*?)" title=".*?">(.*)<\/a>',page)

			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.gercekfilmler.com/wp-content/themes/filmizle/images/logo.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.gercekfilmler.com/wp-content/themes/filmizle/images/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR gercekfilmler CAT LIST_LEN = %s' %  len(video_list_temp)
		except:
			print 'ERROR get_gercekfilmler_category'

		return video_list_temp

	def get_gercekfilmler_category_films(self, url):
		#print 'get_gercekfilmler_category_films'
		try:
			page = mod_request(url)
			#print page
			video_list_temp = []
			chan_counter = 0

 			regex = re.findall(r'<div class="entry">\W+<a href="http:\/\/(.*?)" rel="bookmark" title="(.*?)">',page)
 			img_url = re.findall(r'<img src="(http:\/\/.*?)" alt=".*?" class="post_thumbnail" \/>',page)
			
			print regex

			for text in regex:

				url = text[0]
				title = text[1]
				#title = re.sub('#8211;', '', title)
				#title = re.sub('&#038;', '', title)
				img_url =  img_url[0]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<span class=.page current.>\d+<\/span><\/li><li><a href=.(http:\/\/\b[^>]*). title=.\d+. class=.page.>', page)
			prev = re.findall(r'<a href=.(http:\/\/\b[^>]*). class=.page.>\d+<\/a><\/li><li><span class=.page current.>', page)

			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 

			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:
				self.prev_page_url = 'nStreamModul@gercekfilmler.com@start@gercekfilmler KATEGORILER'
				self.prev_page_text = 'KATEGORILER'

			if(len(video_list_temp)<1):
				print 'ERROR gercekfilmler CAT_FIL LIST_LEN = %s' %  len(video_list_temp)
		except:
			print 'ERROR get_gercekfilmler_category_films'

		return video_list_temp

	def get_gercekfilmler_film(self, url):
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe\Wsrc="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		#descr = re.findall(r'Konu:.*?<\/strong>(.*?)\s*<\w+',page) 
		img = re.findall(r'<p><img src="(.*?)" alt="" title=".*?" width="\d+" height="\d+" class=".*?" \/><\/p>',page)
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + "parca :" + str(chan_counter),
					None,
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name

		return video_list_temp 

# FUNCTIONS tamseyret.com ###### site : / paging :  / liste resim : / liste film : 						
# KRAL
	def get_tamseyret_categories(self, url):
		#print 'get_tamseyret_categories'
		try:
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1

			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.tamseyret.com/lib/images/background/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.tamseyret.com/lib/images/background/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<a href="(.*?)" title=".*?"><span>(.*?)<\/span><\/a>',page)

			for text in regex2:
				title = text[1]
				url = 'www.tamseyret.com/' + text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.tamseyret.com/lib/images/background/logo.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.tamseyret.com/lib/images/background/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR tamseyret CAT LIST_LEN = %s' %  len(video_list_temp)
		except:
			print 'ERROR get_tamseyret_category'

		return video_list_temp

	def get_tamseyret_category_films(self, url):
		#print 'get_tamseyret_category_films'
		try:
			page = mod_request(url)
			#print page
			video_list_temp = []
			chan_counter = 0

 			regex = re.findall(r'<a href="(Film-izle\/.*?)" title="(.*?)" class="listpan"><li>',page)
			img_url  = re.findall(r'<span class="afis left"><img src="(.*?)" alt=".*?" width="\d+" height="\d+"\/>',page)
			for text in regex:

				url = 'www.tamseyret.com/' + text[0]
				title = text[1]
				#title = re.sub('#8211;', '', title)
				#title = re.sub('&#038;', '', title)
				img_url = 'http://www.tamseyret.com/' + img_url[0]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)
			#nextprep1 = 'http://www.tamseyret.com/' 
			next = re.findall(r'<a href=".*?&page=\d+" class=.active.>\d+<\/a>\W+<a href="(.*?&page=\d+)" >\d+<\/a>', page)
			prev = re.findall(r'<a href="(.*?&page=\d+)" >\d+</a>\W+<a href=".*?&page=\d+" class=.active.>\d+<\/a>', page)
			#prev = nextprep1 + prevprep

			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 

			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:
				self.prev_page_url = 'nStreamModul@tamseyret.com@start@tamseyret KATEGORILER'
				self.prev_page_text = 'KATEGORILER'

			if(len(video_list_temp)<1):
				print 'ERROR tamseyret CAT_FIL LIST_LEN = %s' %  len(video_list_temp)
		except:
			print 'ERROR get_tamseyret_category_films'

		return video_list_temp

	def get_tamseyret_film(self, url):
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe\Wsrc="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		#descr = re.findall(r'Konu:.*?<\/strong>(.*?)\s*<\w+',page) 
		img = re.findall(r'<div class="left afis">\W+<img src="(.*?)" alt=".*?" width="\d+" \/>',page)
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + "parca :" + str(chan_counter),
					None,
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name

		return video_list_temp 
		
#FUNCTIONS hdbelgeselizle.com ################################################################################################################  
			
	def get_hdbelgeselizle_categories(self, url): 
		#print 'get_kinomaxpro_categories'
		try:              
			page = mod_request(url) 
			video_list_temp = [] 

			chan_counter = 1
			
			#new = (
				#chan_counter,
				#'YENI EKLENENLER',
				#None,
				#None,
				#None,
				#'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				#None,
				#'',
				#'',
				#None,
				#None
			#)
			#video_list_temp.append(new)
			
			regex = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)
			for text in regex:
				title = text[1].upper()
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 
	   
			if(len(video_list_temp)<1):
				print 'ERROR CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_kinomaxpro_category'   									    	
		
		return video_list_temp

	def get_hdbelgeselizle_category_films(self, url):
		#print 'get_kinomaxpro_category_films'
		#try:              
		page = mod_request(url) 
		video_list_temp = [] 
		chan_counter = 0
		regex = re.findall(r'<a href="http:\/\/(.*?)" title="(.*?)" class="play">izle<\/a>',page) 
		img = re.findall(r'<img src="(.*?)" alt=".*?" width="\d+" height="\d+" \/><br \/>',page)
		for text in regex:
			chan_counter +=1
			url = text[0]
			#img_url = img[0]
			title = text[1].replace('&#8211;',':').upper()
			#descr = regex_descr[chan_counter-1]
			chan_tulpe = (
				chan_counter,
				title,
				None,
				img[chan_counter-1],
				None,
				'nStreamModul@' + url + '@film@' + title,
				None,
				img[chan_counter-1],
				'',
				None,
				None
			)
			video_list_temp.append(chan_tulpe)

		next = re.findall(r"<\/a><a href='(.*?)'.*?class='nextpostslink'>", page)
		prev = re.findall(r"<\/span><a href='(.*?)'.*?class='previouspostslink'>", page)
                                  
		if len(next):
			self.next_page_url = next[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
			self.next_page_text = 'SONRAKI' 
			
		if len(prev):
			self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
			self.prev_page_text = 'ONCEKI'
		else:	
			self.prev_page_url = 'nStreamModul@www.hdbelgeselizle.com@start@KATEGORILER'
			self.prev_page_text = 'KATEGORILER'                                                 
	
		if(len(video_list_temp)<1):
				print 'ERROR CAT_FIL LIST_LEN = %s' %  len(video_list_temp) 
		#except:
			#print 'ERROR get_kinomaxpro_category'   									    	

		return video_list_temp		

	def get_hdbelgeselizle_film(self, url): 
		page = mod_request(url).encode('utf-8') 
		chan_counter = 0
		video_list_temp = []
			
		vk = re.findall(r'<p><iframe .*?src="http:\/\/vk(.*?)".*?frameborder="\d+".*?width="\d+".*?height="\d+"><\/iframe><\/p>',page)	
		vkresis = re.findall(r'<img.*?src="(.*?)".*?alt=".*?"\/>',page) #films resim isim .replace('&#8211;','-')
		isim = re.findall(r'<h1>(.*?)</h1>',page) 
		if(len(vk)>0): 
			url = 'http://vk' + vk[0].replace('&amp;', '&') 
			chan_counter = chan_counter + 1
			title = isim[0].replace('&#8211;','-').upper()
			chan_tulpe = (
				chan_counter,
				title + ' (turanemeksiz)',
				'',
				vkresis[0][0],
				url,
				None,
				None,
				vkresis[0][0],
				'',
				None,
				None
			)
			video_list_temp.append(chan_tulpe)

		yt = re.findall(r'<iframe.*?src="http:\/\/www.youtube.com\/embed\/(\S{11}).*?frameborder="\d+".*?width="\d+".?height="\d+"><\/iframe>',page)
		isim = re.findall(r'<h1>(.*?)</h1>',page)
		if(len(yt)>0):
			for film in yt:
				#title = film[0] 
				url = 'http://www.youtube.com/watch?v=' + film 
				chan_counter = chan_counter + 1
				title = isim[0].upper()
				chan_tulpe = (
					chan_counter,
					title + ' (turanemeksiz)',
					'',
					None,
					url,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name
		
		return video_list_temp

#FUNCTIONS trdizi.com###############################################################################################################

	def get_trdizi_categories(self, url): 
		#print 'get_filmsevenler_categories'
		try:              
			page = mod_request(url).encode('utf-8') 
			page = re.sub('\n','', page)
			video_list_temp = [] 

			chan_counter = 1

			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/@category@YENI EKLENENLER',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex = re.findall(r'<li class="item \d+"><a href="(.*?)" title="">(.*?)<\/a><\/li>',page)
			for text in regex:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + self.active_site_url + '/' + url + '/@category@' + title,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsevenler_category'   									    	

		return video_list_temp  
		
	def get_trdizi_category_films(self, url):
		#print 'get_filmsevenler_category_films'
		#try:              
		page = mod_request(url).encode('utf-8')
		page = re.sub('\n','', page) 
		video_list_temp = [] 
		chan_counter = 0
		
		regex_films = re.findall(r'<div class="thumb"><img src="(.*?)" alt="(.*?)" width="\d+" height="\d+" \/><\/div>\s*<h3><a href="http:\/\/(.*?)" title=".*?<\/a><\/h3>',page)               
		
		for text in regex_films:
			chan_counter +=1

			url = text[2]
			img_url = text[0]
			title = text[1]
			
			chan_tulpe = (
				chan_counter,
				title,
				None,
				img_url,
				None,
				'nStreamModul@' + url + '@film@' + title,
				None,
				img_url,
				'',
				None,
				None
			)  
			video_list_temp.append(chan_tulpe)

		next = re.findall(r"<span class='rightok'><a href=\"(.*?)\" class=\"nextpostslink\"><\/a><\/span><\/div>", page)
		prev = re.findall(r"<span class='leftok'><a href=\"(.*?)\" class=\"previouspostslink\"><\/a><\/span>", page)

		if len(next):
			self.next_page_url = next[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
			self.next_page_text = 'SONRAKI' 
			
		if len(prev):
			self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
			self.prev_page_text = 'ONCEKI'
		else:	
			self.prev_page_url = 'nStreamModul@www.trdizi.com@start@trdizi.com KATEGORILER'
			self.prev_page_text = 'KATEGORILER'                                                          
		
		
		
		if(len(video_list_temp)<1):
			print 'ERROR CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		#except:
		 #   print 'ERROR get_filmsevenler_category_films'   									    	

		return video_list_temp

	def get_trdizi_film(self, url): 
		#print 'get_filmsevenler_film'
		page = mod_request(url)
		page = re.sub('\n','', page) 
		ref_url_vimeo = url
		chan_counter = 0
		video_list_temp = []

		img = re.findall(r'<img src="(.*?)" alt=".*?" width="\d+" height="\d+"  class=".*?"/>',page)
		vk = re.findall(r'<iframe.*?src="(.*?)".*?width="\d+".*?height="\d+".*?frameborder="\d+"><\/iframe>',page)
		yt = re.findall(r'<object.*?width="\d+px".*?height="\d+px"><param.*?name="movie".*?value="(.*?)\?.*?"><\/param>',page)
		if len(vk): 
			url = vk[0].replace('&amp;', '&') 
			chan_counter = chan_counter + 1
			chan_tulpe = (
				chan_counter,
				self.kino_title + ' (TuranEmeksiz)',
				None,
				img[0],
				url,
				None,
				None,
				img[0],
				'',
				None,
				None
			)
			video_list_temp.append(chan_tulpe)
		if len(yt):
			url = yt[0].replace('v/', '/watch?v=')
			chan_counter = chan_counter + 1
			chan_tulpe = (
				chan_counter,
				self.kino_title + ' (TuranEmeksiz)',
				None,
				img[0],
				url,
				None,
				None,
				img[0],
				'',
				None,
				None
			)
			video_list_temp.append(chan_tulpe)
    	
		url2 = re.findall(r'<p>\d+\.Part<\/p>.*?<a.*?href="http:\/\/(.*?)">',page)
		sayi = 1
		for link in url2:
			page2 = mod_request(link)
			vk2 = re.findall(r'<iframe src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page2)
			descr = re.findall(r'<p><span>Konu<\/span>:(.*?)<\/p>.*?<p><span>Etiketler<\/span>',page)
			img = re.findall(r'<img.*?src="(.*?)".*?height="\d+".*?width="\d+".*?alt="".*?\/>',page)
			url3 =re.sub("#038;", "", vk2[0])
			if(len(vk2)>0):
				for text1 in vk2:
					sayi =sayi+1
					chan_counter = chan_counter + 1 
					chan_tulpe = (
						chan_counter,
						str(sayi) + '.Parca -' + self.kino_title,
						descr[0],
						img[0],
						url3,
						None,
						None,
						img[0],
						'',
						None,
						None
					)
					video_list_temp.append(chan_tulpe)

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		#print video_list_temp

		return video_list_temp

# FUNCTIONS filmsehri.com ###############################################################################################################

	def get_filmsehri_categories(self, url): 
		#print 'get_filmsehri_categories'
		try:              
			page = mod_request(url).encode('utf-8') 
			page = re.sub('\n','', page)
			video_list_temp = [] 

			chan_counter = 1

			new = (
				chan_counter,
				'NEW',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/@category@NEW',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex_url = re.findall(r'<li><a href=\"http:\/\/www.filmsehri.com\/(.*?)\" id=\"kategoriler\"',page)
			regex_title = re.findall(r'id=\"kategoriler\">(.*?)<\/a><\/li>',page)
		
			for text in regex_url:
				title = regex_title[chan_counter - 1]
				url = text
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + self.active_site_url + '/' + url + '/@category@' + title,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'   									    	

		return video_list_temp  

	def get_filmsehri_category_films(self, url):
		#print 'get_filmsevenler_category_films'
		try:              
			page = mod_request(url).encode('utf-8')
			page = re.sub('\n','', page) 
			video_list_temp = [] 
			chan_counter = 0
			#print page
		
			regex_helper = re.findall(r'<div id=\"orta-icerik\">(.*?)<\/div>', page)
			regex_link_title = re.findall(r'hidden\"><a href=\"http:\/\/(.*?)\">(.*?)<\/a', regex_helper[0])
			regex_img =  re.findall(r'<img src=\"(.*?)\" width=', regex_helper[0])
		
			for text in regex_link_title:
			
				url = text[0]
				img_url = regex_img[chan_counter]
				title = text[1]
				descr = ''
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					descr,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)
			
			next = re.findall(r"class=['\"]ileri['\"]><a href=['\"](.*?)['\"]>(.*?)<", page)
			prev = re.findall(r"class=['\"]geri['\"]><a href=['\"](.*?)['\"]>(.*?)<", page)
		
			if len(next):
				self.next_page_url = next[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = next[0][1] 

			if len(prev):
				self.prev_page_url = prev[0][0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = prev[0][1]
			else:	
				self.prev_page_url = 'nStreamModul@filmsehri.com@start@filmsehri ALL CATEGORIES'
				self.prev_page_text = 'Categories'			                                                           

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_filmsehri_category_films'   									    	

		return video_list_temp

	def get_filmsehri_film(self, url): 
		print 'get_filmsehri_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		parts = re.findall(r'\"1\">(.*?)<\/font>',page)
		
		if(len(parts)>0):
			for part in parts: 

				chan_counter = chan_counter + 1
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' (vkontakte)' + part,
					'',
					'',
					'http://' + url + str(chan_counter),
					None,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp 
		
# FUNCTIONS xvideos.com ###############################################################################################################

	def get_xvideos_categories(self, url):
		video_list_temp = []
		chan_counter = 0
		chan_counter = chan_counter + 1 
		new = (
			chan_counter,
			'LAST',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com@category@XVIDEOS LAST VIDEOS',
			None,
			'',
			'',
			None,
			None
		)
		video_list_temp.append(new)
		chan_counter = chan_counter + 1
		new = (
			chan_counter,
			'HITS',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com/hits@category@XVIDEOS HITS',
			None,
			'',
			'',
			None,
			None
		)		
		video_list_temp.append(new)
		chan_counter = chan_counter + 1		
		new = (
			chan_counter,
			'Best Of Today',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com/best/day/@category@XVIDEOS Best Of Today',
			None,
			'',
			'',
			None,
			None
		)
		video_list_temp.append(new)
		chan_counter = chan_counter + 1
		new = (
			chan_counter,
			'Best Of 7 Days',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com/best/week/@category@XVIDEOS Best Of 7 Days',
			None,
			'',
			'',
			None,
			None
		)
		video_list_temp.append(new)
		chan_counter = chan_counter + 1
		new = (
			chan_counter,
			'Best Of 30 Days',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com/best/month/@category@XVIDEOS Best Of 30 Days',
			None,
			'',
			'',
			None,
			None
		)
		video_list_temp.append(new)
		chan_counter = chan_counter + 1
		new = (
			chan_counter,
			'Best Of All Time',
			None,
			None,
			None,
			'nStreamModul@www.xvideos.com/best@category@XVIDEOS Best Of All Time',
			None,
			'',
			'',
			None,
			None
		)
		
		video_list_temp.append(new) 
		
		return video_list_temp

	def get_xvideos_category_films(self, url):
		#print 'get_xvideos_category_films'
		try:              
			page = mod_request(url).encode('utf-8')
			#page = re.sub('\n','', page) 
			video_list_temp = [] 
			chan_counter = 0
			print page
			#regex = re.findall (r'<a href="(.*?)".*?><img src="(.*?)" onMouseOver="startThumbSl', page)
			#regex_link = re.findall(r'<a href=\"(.*?)\" class=\"miniature\">', page)
			#regex_img = re.findall(r'\"miniature\"><img src=\"(.*?)\" onMouseOver=\"startThumbSl', page)
			regex = re.findall(r' <a href="(.*?)"><img src="(.*?)" id=".*?" \/><\/a>\s*<\/div>\s*<p><a href=".*?">(.*?)<\/a><\/p>',page)	                                                 
			for text in regex:
		
				url = 'http://www.xvideos.com' + text[0]
				img_url = text[1]
				#info = regex_title_ln_qa[chan_counter]
				title = text[2]
				chan_counter +=1
				#descr =  info[2] + ' ' + info[4]
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					url,
					None,#'nStreamModul@' + url + '@film@' + title, no extra pahe -> direct play from category
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)
		
			next = re.findall(r'nP" href="([^<"]*)">Next', page)
			prev = re.findall(r'<a href="([^<"]*)" class="nP">Prev', page)
				
			if next:
				slash = ''
				if next[0][0:1]!='/':
					slash = '/'
				self.next_page_url =  'nStreamModul@www.xvideos.com' + slash + next[0] + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'NEXT' 
			
			if prev:
				slash = ''
				if prev[0][0:1]!='/':
					slash = '/' 
				self.prev_page_url = 'nStreamModul@www.xvideos.com' + slash + prev[0] + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'PREV'
			else:	
				self.prev_page_url = 'nStreamModul@www.xvideos.com@start@XVIDEOS ALL CATEGORIES'
				self.prev_page_text = 'Categories'  		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR xvideos CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_xvideos_category_films'   									    	

		return video_list_temp 	

	# --> nStreamHTMLparser QUICKSTART PLAY FROM CATEGORY    
	# def get_xvideos_film(self, url): 
	# 	print 'get_xvideos_film'
	# 	page = mod_request(url)
	# 	video_list_temp = []
	# 	video = re.findall(r'3GP\|\|(.*?)\|\|',page)
	# 	if(len(video)>0): 
	# 		url = video 
	# 		chan_tulpe = (
	# 			1,
	# 			self.kino_title,
	# 			'',
	# 			'',
	# 			url[0],
	# 			None,
	# 			None,
	# 			'',
	# 			'',
	# 			None,
	# 			None
	# 		)
	# 		video_list_temp.append(chan_tulpe)
	# 
	# 
	# 	self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
	# 	self.prev_page_text = self.playlist_cat_name   	
	# 
	# 	return video_list_temp		
		
# FUNCTIONS bicaps.com ###############################################################################################################

	def get_bicaps_categories(self, url): 
		print 'get_sinemaizle_categories'
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://bicaps.com/bicapslogo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://bicaps.com/bicapslogo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex1 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*?title=".*?">(.*?)<\/a>',page)

			for text in regex1:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://bicaps.com/bicapslogo.png',
					url,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://bicaps.com/bicapslogo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'   									    	

		return video_list_temp  

	def get_bicaps_category_films(self, url):
		print 'get_sinemaizle_category_films'
		try:              
			page = mod_request(url).encode('utf-8')
			print page
			video_list_temp = [] 
			chan_counter = 0

			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)".*?height="\d+".*?width="\d+".*?alt=.*?\/><\/a>',page) 
			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)&w=\d+&h=\d+&zc=\d+"<\/a>',page)
 			regex = re.findall(r'<a.*?href="http:\/\/(.*?)">\s*<.*?img.*?src="(.*?)".*?alt="(.*?)\|.*?".*?height=".*?".*?width=".*?".*?\/>.*?<\/a>\s*<div.*?class="movie\w">',page)

			print regex
			for text in regex:
				url = text[0]
				title = text[2]
				title = re.sub('#8211;', '', title)
				img_url =  text[1]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					url,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r"\.\.\.<\/span><a.*?href='(.*?)'", page)
			prev = re.findall(r"<a.*?href='(.*?)'.*?class='previouspostslink'>", page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@bicaps.com@start@BICAPS KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           



			if(len(video_list_temp)<1):
				print 'ERROR sinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_sinemaizle_category_films'   									    	

		return video_list_temp

	def get_bicaps_film(self, url): 
		print 'get_sinemaizle_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe src="(.*?)" frameborder="\d+" width="\d+" height="\d+"><\/iframe><\/p>',page)
		descr = re.findall(r'<div.*?class="konuozet">\s*<p><\/p>\s*(.*?)\s*<\/div>',page) 
		img = re.findall(r'<img.*?src="(.*?)".*?alt=".*?".*?height=".*?" width=".*?".*?\/>',page)
		url2 = re.findall(r'Part.*?<\/span>.*?<a.*?href="http:\/\/(.*?)">.*?<span>',page)
		for link in url2:
			page2 = mod_request(link)
			vk2 = re.findall(r'<p><iframe.*?src="(.*?)".*?width=".*?".*?height=".*?".*?frameborder=".*?"><\/iframe><\/p>',page2)
			for ll in vk2:
				vk.append(ll)
		if len(descr):
			aciklama = descr[0]
		else:
			aciklama="Konu mevcut degil"
		#url4 =re.sub("#038;", "", vk[0])
		if(len(vk)>0):
			for text in vk:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca : ' + str(chan_counter),
					aciklama,
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp  	

# FUNCTIONS hurriyet.com ###############################################################################################################

	def get_hurriyet_categories(self, url): 
		print 'get_sinemaizle_categories'
		try:              
			page = mod_request(url).decode('iso-8859-9').encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 0

			regex1 = re.findall(r'<li.*?><a href="http:\/\/(.*?)".*?title="(.*?)".*?class=".*?CategoryHeader">',page)

			for text in regex1:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'   									    	

		return video_list_temp  

	def get_hurriyet_category_films(self, url):
		print 'get_sinemaizle_category_films'
		try:              
			page = mod_request(url).decode('iso-8859-9').encode('utf-8')
			print page
			video_list_temp = [] 
			chan_counter = 0

			#regex = re.findall(r"<span class=\"WebtvFavoriteContentLink\"><a href='(.*?)'>", page)
 			#regex = re.findall(r"<a href='(.*?)'>\s*<img width=\"\d+\" height=\"\d+\" border=\"\d+\" alt=\"(.*?)\"\s*src='(.*?)' \/><\/a>", page)
                	regex = re.findall(r"<a.*?href='(.*?)'>\s*?<img.*?class=\"hurLazyImage\".*?='(.*?)' width=\".*?\".*?height=\".*?\".*?border=\".*?\"\s*.*?alt=\"(.*?)\" \/><\/a><\/div>",page)

			for text in regex:

				url =  text[0]
				title = text[2]
				title = re.sub('&[^;]*.', '', title)
				img_url =  text[1]
				print img_url
				descr =  text[1]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					descr,
					img_url,
					url,
					None,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<div class="WebtvBackButton FL">\s*<a href="(.*?)">\s*<img src="', page)
			prev = re.findall(r'<div class="WebtvNextButton FL">\s*<a href="(.*?)">', page)
			if( not len(next)):
     				next = re.findall(r'<div class="PagerRightLogo FL">\s*<a href="(.*?)">',page) 
			if( not len(prev)):
     				prev = re.findall(r'<div class="PagerLeftLogo FL">\s*<a href="(.*?)">',page)

			if len(next):
				self.next_page_url = next[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@hurriyet.com.tr@start@KATEGORILER'
				self.prev_page_text = 'KATEGORILER'  		                                                           



			if(len(video_list_temp)<1):
				print 'ERROR sinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_sinemaizle_category_films'   									    	

		return video_list_temp   		

# FUNCTIONS webteizle.com ###############################################################################################################

	def get_webteizle_categories(self, url): 
		try:              
			page = mod_request(url).decode('windows-1254').encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://webteizle.com/images/WebteizleLogo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://webteizle.com/images/WebteizleLogo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex1 = re.findall(r'<li.*?><a\s*href="\/(.*?)"\s*title="(.*?)">',page)

			for text in regex1:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://webteizle.com/images/WebteizleLogo.png',
					None,
					'nStreamModul@' + self.active_site_url + '/' +  url + '@category@' + title,
					None,
					'http://webteizle.com/images/WebteizleLogo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'   									    	

		return video_list_temp  

	def get_webteizle_category_films(self, url):
		try:              
			page = mod_request(url).decode('windows-1254').encode('utf-8')
			if url!='webteizle.com':
				url_nav = url.split('/')
				url_navi= url_nav[0] + '/' + url_nav[1] + '/'
			else:
				url_nav = ''
				url_navi = ''
			print page
			video_list_temp = [] 
			chan_counter = 0

			regex = re.findall(r'<div.*?>.*?<a.*?href="(.*?)".*?class="red-link".*?title="(.*?)".*?><img.*?src="(.*?)".*?alt=".*?"' ,page)
			descrip = re.findall(r'Konu:<\/font>.*?<strong>(.*?)<\w', page)

			for text in regex:

				url = text[0]
				title = text[1]
				title = re.sub('#8211;', '', title)
				img_url =  text[2]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					descrip[chan_counter-1],
					img_url,
					None,
					'nStreamModul@' + 'webteizle.com' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			prev = re.findall(r'<a href="(.*?)">\d+</a>\s*\s*<b>\d+<\/b>', page)
			next = re.findall(r'<b>\d+<\/b>\s*\s*<a href="(.*?)">\d+</a>', page)
			if len(next):
				self.next_page_url = 'nStreamModul@' + url_navi + next[0] + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = 'nStreamModul@' + url_navi + prev[0] + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@webteizle.com@start@KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR sinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_sinemaizle_category_films'   									    	

		return video_list_temp

	def get_webteizle_film(self, url): 
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		descr = re.findall(r'Konu:.*?<\/strong>(.*?)\s*<\w+',page) 
		img = re.findall(r'<link.*?rel="image_src".*?href="(.*?)".*?\/>',page)
		if(len(vk)>0):
			for text in vk:
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title,
					descr[0],
					img[0],
					text,
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp  	

# FUNCTIONS pornetto.com ###############################################################################################################

	def get_pornetto_categories(self, url): 
		try:              
			page = mod_request('www.pornetto.com') 
			page1 = mod_request('www.pornetto.com/categories.php')
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex1 = re.findall(r'<a.*?href="http:\/\/(.*?)".*?title="(.*?)"><img width="\d+" height="\d+" class=".*?" src="(.*?)" alt=".*?"><\/a>',page1)
			for text in regex1:
				title = text[1]
				url = text[0]
				img = text[2]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img,
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					img,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'   									    	

		return video_list_temp  

	def get_pornetto_category_films(self, url):
		try:              
			page = mod_request(url)
			print page
			video_list_temp = [] 
			chan_counter = 0
			regex = re.findall(r'class=".*?".*?src="(.*?)".*?alt="(.*?)".*?\/><\/a><br.*?\/>\s*<.*?a.*?class=".*?".*?target=".*?".*?href="http:\/\/(.*?)".*?title=.*?<\/a>.*?<br.*?\/>\s*<span.*?class=".*?">(.*?)<\/span><br.*?\/>' ,page)
                     #regex = re.findall( r'class=".*?".*?src="(.*?)".*?alt="(.*?)".*?\/><\/a><br.*?\/>\s*<.*?a.*?class=".*?".*?target=".*?".*?href="http:\/\/(.*?)".*?title=.*?<\/a>.*?<br.*?\/>\s*<span.*?class=".*?">(.*?)<\/span><br.*?\/>' ,page)
			for text in regex:

				url = text[2]
				title = text[1]
				title = re.sub('#8211;', '', title)
				img_url =  text[0]
				descr = text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					descr,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)
 
			prev = re.findall(r'<a href="(.*?)" text="&lt;&lt;">', page)
			next = re.findall(r'<a href="(.*?)" text="&gt;&gt;"', page)
			if len(next):
				self.next_page_url = 'nStreamModul@' + url_navi + next[0] + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = 'nStreamModul@' + url_navi + prev[0] + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@pornetto.com@start@KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           



			if(len(video_list_temp)<1):
				print 'ERROR sinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_sinemaizle_category_films'   									    	

		return video_list_temp

	def get_pornetto_film(self, url): 
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		vk = re.findall(r's1.addVariable\("file","(.*?)"\);',page)
		#descr = re.findall(r'Konu:.*?<\/strong>(.*?)\s*<\w+',page) 
		img = re.findall(r's1.addVariable\("image","(.*?)"\)',page)
		if(len(vk)>0):
			for text in vk:
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title,
					None,
					img[0],
					text+'?start=0',
					None,
					None,
					img[0],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp  	

# FUNCTIONS dizihd.com ###############################################################################################################

	def get_dizihd_categories(self, url): 
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://dizihd.com/player/images/onezel.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://dizihd.com/player/images/onezel.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex1 = re.findall(r'"><a.*?href="http:\/\/(.*?)".*?title="(.*?)">.*?<\/a>',page)
			for text in regex1:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://dizihd.com/player/images/onezel.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://dizihd.com/player/images/onezel.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR dizihd CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_dizihd_category'   									    	

		return video_list_temp  

	def get_dizihd_category_films(self, url):
		try:              
			page = mod_request(url).encode('utf-8')
			print page
			video_list_temp = [] 
			chan_counter = 0

			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)".*?height="\d+".*?width="\d+".*?alt=.*?\/><\/a>',page) 
			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)&w=\d+&h=\d+&zc=\d+"<\/a>',page)
 			regex = re.findall(r'<a.*?href="http:\/\/.*?">.*?<img.*?src="(.*?)".*?><\/a>\s*<h2><a.*?href="http:\/\/(.*?)">(.*?)<\/a><\/h2>',page)

			for text in regex:

				url = text[1]
				title = text[2]
				title = re.sub('#8211;', '', title)
				img_url =  text[0]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r"\.\.\.<\/span><a.*?href=\"(.*?)\"", page)
			prev = re.findall(r"<a.*?href=\"(.*?)\".*?class=\"previouspostslink\">", page)
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@dizihd.com@start@BICAPS KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR dizihd CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_dizihd_category_films'   									    	

		return video_list_temp

	def get_dizihd_film(self, url): 
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		xmlpag= re.findall(r"var xmlAddress.*?'http:\/\/(.*?)'",page)
		xmlpage = mod_request(xmlpag[0])
		parts = re.findall(r'<videoPath value="(.*?)"\/>\s*<previewImage.*?\/>\s*<thumbImage value="(.*?)"/>',xmlpage)
			
		if(len(parts)>0):
			for text in parts:
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca : ' + str(chan_counter),
					None,
					text[1],
					text[0],
					None,
					None,
					text[1],
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		
		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp  

#FUNCTIONS myvideo.de###############################################################################################################

	def get_myvideo_categories(self, url): 
		#print 'get_filmsevenler_categories'
		try:              
			page = mod_request(url).encode('utf-8') 
			page = re.sub('\n','', page)
			video_list_temp = [] 

			chan_counter = 1

			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/@category@YENI EKLENENLER',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex = re.findall(r'<li class="item \d+"><a href="(.*?)" title="">(.*?)<\/a><\/li>',page)
			for text in regex:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + self.active_site_url + '/' + url + '/@category@' + title,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsevenler_category'   									    	

		return video_list_temp  
		
	def get_myvideo_category_films(self, url):
		#print 'get_myvideo_category_films'
		#try:              
		page = mod_request(url).encode('utf-8')
		page = re.sub('\n','', page) 
		video_list_temp = [] 
		chan_counter = 0
		
		regex_films = re.findall(r'<div class="thumb"><img src="(.*?)" alt="(.*?)" width="\d+" height="\d+" \/><\/div>\s*<h3><a href="http:\/\/(.*?)" title=".*?<\/a><\/h3>',page)               
		
		
		
		for text in regex_films:
			chan_counter +=1

			url = text[2]
			img_url = text[0]
			title = text[1]
			
			chan_tulpe = (
				chan_counter,
				title,
				None,
				img_url,
				None,
				'nStreamModul@' + url + '@film@' + title,
				None,
				img_url,
				'',
				None,
				None
			)  
			video_list_temp.append(chan_tulpe)

		next = re.findall(r"<span class='rightok'><a href=\"(.*?)\" class=\"nextpos\"><\/a><\/span><\/div>", page)
		prev = re.findall(r"<span class='leftok'><a href=\"(.*?)\" class=\"prev\"><\/a><\/span>", page)

		if len(next):
			self.next_page_url = next[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
			self.next_page_text = 'SONRAKI' 
			
		if len(prev):
			self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
			self.prev_page_text = 'ONCEKI'
		else:	
			self.prev_page_url = 'nStreamModul@www.myvideo.de@start@myvideo.de KATEGORILER'
			self.prev_page_text = 'KATEGORILER'                                                          
		
		
		
		if(len(video_list_temp)<1):
			print 'ERROR CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		#except:
		 #   print 'ERROR get_myvideo_category_films'   									    	

		return video_list_temp

	def get_myvideo_film(self, url): 
		#print 'get_myvideo_film'
		page = mod_request(url)
		page = re.sub('\n','', page) 
		ref_url_vimeo = url
		chan_counter = 0
		video_list_temp = []

		img = re.findall(r'<img src="(.*?)" alt=".*?" width="\d+" height="\d+"  class=".*?"/>',page)
		vk = re.findall(r'<iframe.*?src="(.*?)".*?width="\d+".*?height="\d+".*?frameborder="\d+"><\/iframe>',page)
		yt = re.findall(r'<object.*?width="\d+px".*?height="\d+px"><param.*?name="movie".*?value="(.*?)\?.*?"><\/param>',page)
		if len(vk): 
			url = vk[0].replace('&amp;', '&') 
			chan_counter = chan_counter + 1
			chan_tulpe = (
				chan_counter,
				self.kino_title + ' ',
				None,
				img[0],
				url,
				None,
				None,
				img[0],
				'',
				None,
				None
			)
			video_list_temp.append(chan_tulpe)
		if len(yt):
			url = yt[0].replace('v/', '/watch?v=')
			chan_counter = chan_counter + 1
			chan_tulpe = (
				chan_counter,
				self.kino_title + ' ',
				None,
				img[0],
				url,
				None,
				None,
				img[0],
				'',
				None,
				None
			)
			video_list_temp.append(chan_tulpe)
    	
		url2 = re.findall(r'<p>\d+\.Part<\/p>.*?<a.*?href="http:\/\/(.*?)">',page)
		sayi = 1
		for link in url2:
			page2 = mod_request(link)
			vk2 = re.findall(r'<iframe src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page2)
			descr = re.findall(r'<p><span>Beschreibung<\/span>:(.*?)<\/p>.*?<p><span>Stichw&ouml;rter<\/span>',page)
			img = re.findall(r'<img.*?src="(.*?)".*?height="\d+".*?width="\d+".*?alt="".*?\/>',page)
			url3 =re.sub("#038;", "", vk2[0])
			if(len(vk2)>0):
				for text1 in vk2:
					sayi =sayi+1
					chan_counter = chan_counter + 1 
					chan_tulpe = (
						chan_counter,
						str(sayi) + '.Parca -' + self.kino_title,
						descr[0],
						img[0],
						url3,
						None,
						None,
						img[0],
						'',
						None,
						None
					)
					video_list_temp.append(chan_tulpe)

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		#print video_list_temp


		return video_list_temp

		# FUNCTIONS filmizlese.net ###############################################################################################################

	def get_filmizlese_categories(self, url): 
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.filmizlese.net/logo.jpg',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.filmizlese.net/logo.jpg',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex1 = re.findall(r'<a class="filmkate" href="(.*?)" title=".*?">(.*?)</a>', page)


			for text in regex1:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.filmizlese.net/logo.jpg',
					None,
					'nStreamModul@' + self.active_site_url + url + '@category@' + title,
					None,
					'http://www.filmizlese.net/logo.jpg',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'   									    	

		return video_list_temp  


	def get_filmizlese_category_films(self, url):
		try:              
			page = mod_request(url).encode('utf-8') 
			print page
			video_list_temp = [] 
			chan_counter = 0

			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)".*?height="\d+".*?width="\d+".*?alt=.*?\/><\/a>',page) 
			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)&w=\d+&h=\d+&zc=\d+"<\/a>',page)
 			regex = re.findall(r'<div class="filml"><div style="float: left;"><a href="(.*?)" title="(.*?)"><img src="(.*?)" alt=".*?"', page)

			for text in regex:

				url =text[0]
				title = text[1]
				title = re.sub('#8211;', '', title)
				img_url =  'http://www.filmizlese.net'  + text[2]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					None,
					'nStreamModul@' + self.active_site_url +  url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)


			next = re.findall(r'class="selected">\d+<\/a><a href="(.*?)"', page)
						                    
			if len(next):
				self.next_page_url = 'nStreamModul@' + self.active_site_url + next[0] + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 

			
			else:	
				self.prev_page_url = 'nStreamModul@' + self.active_site_url + '@start@KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           



			if(len(video_list_temp)<1):
				print 'ERROR sinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_sinemaizle_category_films'   									    	

		return video_list_temp


	def get_filmizlese_film(self, url): 
		print 'get_sinemaizle_film'
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []
		#vk = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		mailru = re.findall(r'><embed src="\/filmplayer.swf\?file=(.*?)" quality', page)
		descr = re.findall(r'<div.*?class="konuozet">\s*<p><\/p>\s*(.*?)\s*<\/div>',page) 
		#img = re.findall(r'<img.*?src="(.*?)".*?alt=".*?".*?height=".*?" width=".*?".*?\/>',page)
		img = ""
		url22 = re.findall(r'm.*?<\/li><li><a href="(.*?)">.*?K', page)
		
		for link in url22:
			page2 = mod_request(self.active_site_url + link)
			#vk2 = re.findall(r'<p><iframe.*?src="(.*?)".*?width=".*?".*?height=".*?".*?frameborder=".*?"><\/iframe><\/p>',page2)
			mailru2 = re.findall(r'><embed src="\/filmplayer.swf\?file=(.*?)" quality', page2)

			for ll in mailru2:
				mailru.append(ll)
		if len(descr):
			aciklama = descr[0]
		else:
			aciklama="Konu mevcut degil"
		if(len(mailru)>0):
			for text in mailru:
				text=text.replace("#038;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca : ' + str(chan_counter),
					aciklama,
					None,
					text,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		
		

		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp  	

# FUNCTIONS fragg.me ###############################################################################################################

	def get_fragg_categories(self, url): 
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)
			
			chan_counter = chan_counter + 1
			new = (
				chan_counter,
				'En Cok Izlenenler',
				None,
				None,
				None,
				'nStreamModul@fragg.me/pop/@category@EN COK IZLENENLER',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)


			chan_counter = chan_counter + 1
			new = (
				chan_counter,
				'Reklamlar',
				None,
				None,
				None,
				'nStreamModul@fragg.me/ads/new/@category@REKLAMLAR',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)

			chan_counter = chan_counter + 1
			new = (
				chan_counter,
				'Arabalar',
				None,
				None,
				None,
				'nStreamModul@fragg.me/vehicles/new/@category@ARABALAR',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new) 

			chan_counter = chan_counter + 1
			new = (
				chan_counter,
				'Komedi ve Muzik',
				None,
				None,
				None,
				'nStreamModul@fragg.me/comedy/new/@category@KOMIK',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)

			chan_counter = chan_counter + 1
			new = (
				chan_counter,
				'Bilgisayar ve Oyunlar',
				None,
				None,
				None,
				'nStreamModul@fragg.me/computer/new/@category@BILGISAYAR',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)

			chan_counter = chan_counter + 1
			new = (
				chan_counter,
				'Aile ve Bebek',
				None,
				None,
				None,
				'nStreamModul@fragg.me/family/new/@category@AILE',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)

			chan_counter = chan_counter + 1
			new = (
				chan_counter,
				'Film ve Animasyon',
				None,
				None,
				None,
				'nStreamModul@fragg.me/film_animation/new/@category@ANIMASYON',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)

			chan_counter = chan_counter + 1
			new = (
				chan_counter,
				'Kategorisiz',
				None,
				None,
				None,
				'nStreamModul@fragg.me/others/new/@category@KATEGORISIZ',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)


			chan_counter = chan_counter + 1
			new = (
				chan_counter,
				'Insanlar',
				None,
				None,
				None,
				'nStreamModul@fragg.me/people/new/@category@INSANLAR',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)

			chan_counter = chan_counter + 1
			new = (
				chan_counter,
				'Hayvanlar Alemi',
				None,
				None,
				None,
				'nStreamModul@fragg.me/animals/new/@category@HAYVANLAR',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)

			chan_counter = chan_counter + 1
			new = (
				chan_counter,
				'Spor',
				None,
				None,
				None,
				'nStreamModul@fragg.me/sports/new/@category@SPOR',
				None,
				None,
				'',
				None,
				None
			)
			video_list_temp.append(new)

			if(len(video_list_temp)<1):
				print 'ERROR fragg CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_fragg_category'   									    	

		return video_list_temp  


	def get_fragg_category_films(self, url):
		try:              
			page = mod_request(url).encode('utf-8') 
			print page
			video_list_temp = [] 
			chan_counter = 0

			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)".*?height="\d+".*?width="\d+".*?alt=.*?\/><\/a>',page) 
			#regex = re.findall(r'<a.*?href="http:\/\/(.*?)".*?rel="bookmark".*?title="(.*?)\|.*?"><img.*?src="(.*?)&w=\d+&h=\d+&zc=\d+"<\/a>',page)
 			regex = re.findall(r'<a.*?href="(.*?)"><img.*?src="(.*?)" alt=".*?".*?title="(.*?)".*?width="\d+".*?height="\d+".*?\/><\/a><br.*?\/>', page)

			for text in regex:

				url =text[0]
				url2 = self.active_site_url +  url
				page2 = mod_request(url2)
				vid_url = re.findall(r'<meta.*?property="og:video".*?content="(.*?)">', page2)
				title = text[2]
				img_url = text[1]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					img_url,
					vid_url[0],
					None,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			prev = re.findall(r'Previous<\/a>.*?<a.*?href="(.*?)">', page)
			next = re.findall(r'<\/a>.*?<a.*?href="(.*?)".*?<\/a>.*?<span>', page)
						                    
			if len(next):
				self.next_page_url = 'nStreamModul@' + self.active_site_url + next[-1] + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 

			if len(prev):
				self.prev_page_url = 'nStreamModul@' +  self.active_site_url + prev[0] + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'

			else:	
				self.prev_page_url = 'nStreamModul@' + self.active_site_url + '@start@KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           



			if(len(video_list_temp)<1):
				print 'ERROR sinemaizle CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_sinemaizle_category_films'   									    	

		return video_list_temp

# FUNCTIONS www.evrenselfilm.com ###############################################################################################################

	def get_evrenselfilm_categories(self, url): 
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 

			chan_counter = 1

			new = (
				chan_counter,
				'Yeni EKlenenler',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/@category@YENI EKLENENLER',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)


			regex = re.findall(r'<li class="cat-item cat-item-\d*"><a href="http:\/\/(.*?)" title=".*?">(.*?)<\/a>',page)
		
			for text in regex:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + url + '/@category@' + title,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'   									    	

		return video_list_temp  


	def get_evrenselfilm_category_films(self, url):
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 0
		
			data = re.findall(r'<div class="solust"><a href="http:\/\/(.*?)" rel="bookmark" title=".*?">(.*?)<\/a>',page)
			data1 = re.findall(r'<p><img src="(.*?)" alt="" title=".*?\/><br.*?\/>\s*(.*?)<\/p>',page)

		
		
			for text in data:
			
				url = text[0]
				img_url = data1[chan_counter][0]
				title = text[1].replace("&#8211;" , "-")
				descr = data1[chan_counter][1]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					descr,
					img_url,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			
			next = re.findall(r'<\/a><a href="(.*?)" class="nextpostslink',page) 
			prev = re.findall(r'class="previouspostslink">.*?<\/a><a href=\'(.*?)\' class',page)
		
			if len(next):
				self.next_page_url = next[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 

			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@evrenselfilm.com@start@KATEGORILER'
				self.prev_page_text = 'KATEGORILER'			                                                           



			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_filmsehri_category_films'   									    	

		return video_list_temp


	def get_evrenselfilm_film(self, url): 
		page = mod_request(url)
		chan_counter = 0
		video_list_temp = []
		yt =  re.findall(r'<iframe.*?src="http:\/\/www.youtube.com\/embed\/(.*?)" frameborder="(.*?)"', page)
		resdec = re.findall(r'<p><img src="(.*?)" alt="" title=".*?\/><br.*?\/>\s*(.*?)<\/p>',page)
		if(len(yt)>0):
			for frag in yt: 
				img = resdec[0][0]
				desc = resdec[0][1]
				chan_counter = chan_counter + 1
				chan_tulpe = (
					chan_counter,
					self.kino_title + '**Fragman**',
					desc,
					img,
					'http://www.youtube.com/watch?v=' + frag[0],
					None,
					None,
					img,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)


		names =  re.findall(r'<p><span style="color: #ff0000;">Evrenselfilm.com (.*?)<\/span><br.*?\/>', page)
		parts = re.findall(r'<embed src=.*?file=(.*?)mp4',page)

		if(len(parts)>0):
			for part in parts: 
				chan_counter = chan_counter + 1
				chan_tulpe = (
					chan_counter,
					self.kino_title + '**'+names[chan_counter - 2]+'**',
					desc,
					img,
					part+'mp4',
					None,
					None,
					img,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)



		self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp 
		
		
# FUNCTIONS eroguru.com ###############################################################################################################

	def get_eroguru_categories(self, url): 
		try:              
			page = mod_request(url)
			video_list_temp = [] 


			new = (
				1,
				'Yeni Eklenenler',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/@category@YENI EKLENENLER',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			new = (
				2,
				'EROTIK - LESBIYEN',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/video-erotika/lesbi-vidyeo-hd/@category@EROTIK - LESBIYEN',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			new = (
				3,
				'WEBCAM',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/video-erotika/webcam/@category@WEBCAM',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			new = (
				4,
				'MASAJ',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/video-erotika/eroticheskiy-massazh/@category@MASAJ',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			new = (
				5,
				'SEXY VIDEO KLIP',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/video-erotika/music-video-sexy/@category@SEXY VIDEO KLIP',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)


			new = (
				6,
				'ANAL',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/porno-video-hd/analnyi-seks/@category@ANAL',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)


			new = (
				7,
				'GRUP SEX',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/porno-video-hd/gruppovoe-porno/@category@GRUP SEX',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)


			new = (
				8,
				'MASTURBASYON',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/porno-video-hd/masturbatsiya/@category@MASTURBASYON',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)


			new = (
				9,
				'BLOWJOB',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/porno-video-hd/minet-hd/@category@BLOWJOB',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'   									    	

		return video_list_temp  


	def get_eroguru_category_films(self, url):
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 0
		
			data = re.findall(r'<a href="http:\/\/(.*?)" ><div align="center"><.*?:(.*?)jpg',page)
			
				
			for text in data:
				url11 = text[0]
				page1 = mod_request(url11)
				preurl = re.findall(r'<iframe src="(.*?)" width="\d+" height="\d+"',page1)
				url = preurl[0].replace("&amp;","&")
				img_url =text[1] + 'jpg'
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					'Video'  + str(chan_counter),
					None,
					img_url,
					url,
					None,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			prev = re.findall(r'<a href="(.*?)"><span class="thide pprev">.*?<\/span><\/a>',page)
			next = re.findall(r'<a href="(.*?)"><span class="thide pnext">.*?<\/span><\/a>',page)

			if len(next):
				self.next_page_url = next[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 

			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@eroguru.com@start@KATEGORILER'
				self.prev_page_text = 'KATEGORILER'			                                                           



			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_filmsehri_category_films'   									    	

		return video_list_temp

# FUNCTIONS video-klipleri.org ###############################################################################################################

	def get_klipleri_categories(self, url): 
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 

			chan_counter = 1

			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				None,
				None,
				'nStreamModul@' + self.active_site_url + '/@category@YENI EKLENENLER',
				None,
				'',
				'',
				None,
				None
			)
			video_list_temp.append(new)


			regex = re.findall(r'<div class="i_cats"><a href="http:\/\/(.*?)" title="(.*?)">.*?</a><\/div>',page)
			sanatci = re.findall(r'<span class="i_cats"><a target="_top" href="http:\/\/(.*?)" title="(.*?)">.*?<\/a><\/span>',page)
			for ll in sanatci:
				regex.append(ll)

			for text in regex:
				title = text[1].replace("&amp;", "ve")
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_filmsehri_category'   									    	

		return video_list_temp  


	def get_klipleri_category_films(self, url):
		try:              
			page = mod_request(url).encode('utf-8') 
			video_list_temp = [] 
			chan_counter = 0
		
			data = re.findall(r'a href="http:\/\/(.*?)" class=".*?" title="(.*?)"><span.*?><span.*?><img src=.*?data-original="(.*?)"',page)
				
			for text in data:
				page1 =mod_request(text[0]).encode('utf-8')
				yt = re.findall(r'<iframe.*?src="http:\/\/www.youtube.com\/v\/(.*?)&ver.*?frameborder="\d+"><\/iframe>',page1)
				daily = re.findall(r'<iframe.*?src="http:\/\/www.dailymotion.com\/embed\/video\/(.*?)\?foreground.*?"><\/iframe>',page1)
					
				if len(yt):
					url = 'http://www.youtube.com/watch?v=' + yt[0]
				if len(daily):
					url = 'http://www.dailymotion.com/embed/video/' + daily[0]
				img_url = text[2]
				title = text[1]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					title,
					img_url,
					url,
					None,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)




			data = re.findall(r'<a href="http:\/\/(.*?)"><span class="imag"><img src=.*?data-original="(.*?)".*?alt="(.*?)".*?wid',page)
				
			for text in data:
				page2 =mod_request(text[0]).encode('utf-8')
				yt = re.findall(r'<iframe.*?src="http:\/\/www.youtube.com\/v\/(.*?)&ver.*?frameborder="\d+"><\/iframe>',page2)
				daily = re.findall(r'<iframe.*?src="http:\/\/www.dailymotion.com\/embed\/video\/(.*?)\?foreground.*?"><\/iframe>',page2)
					
				if len(yt):
					url = 'http://www.youtube.com/watch?v=' + yt[0]
				if len(daily):
					url = 'http://www.dailymotion.com/embed/video/' + daily[0]
				img_url = text[1]
				title = text[2]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					title,
					img_url,
					url,
					None,
					None,
					img_url,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			
			next = re.findall(r'<a href="\/turkpop-video-klipleri\/(.*?)\/">',page) 
			prev = re.findall(r'<div class=".*?"><div class="pagination"><a href="(.*?)">&laquo;',page)
		
			if len(next):
				self.next_page_url = 'nStreamModul@video-klipleri.org/turkpop-video-klipleri/' + next[0] + '/@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 

			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@video-klipleri.org@start@KATEGORILER'
				self.prev_page_text = 'KATEGORILER'			                                                           



			if(len(video_list_temp)<1):
				print 'ERROR filmsehri CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_filmsehri_category_films'   									    	

		return video_list_temp

# FUNCTIONS fullhdfilmizlet.com ###### 
	def get_fullhdfilmizlet_categories(self, url): 
		#print 'get_fullhdfilmizlet_categories'
		try:              
			page = mod_request(url)
			video_list_temp = [] 
			chan_counter = 1
			
			new = (
				chan_counter,
				'Yeni Eklenenler',
				None,
				'http://www.fullhdfilmizlet.com/wp-content/themes/basizlev1/images/logo.png',
				None,
				'nStreamModul@' + self.active_site_url + '@category@YENI EKLENENLER',
				None,
				'http://www.fullhdfilmizlet.com/wp-content/themes/basizlev1/images/logo.png',
				'',
				None,
				None
			)
			video_list_temp.append(new)

			regex2 = re.findall(r'<li.*?class="cat-item.*?cat-item-\d+"><a.*?href="http:\/\/(.*?)".*? title=".*?">(.*?)<\/a>',page)
	
			for text in regex2:
				title = text[1]
				url = text[0]
				chan_counter +=1 
				chan_tulpe = (
					chan_counter,
					title,
					None,
					'http://www.fullhdfilmizlet.com/wp-content/themes/basizlev1/images/logo.png',
					None,
					'nStreamModul@' + url + '@category@' + title,
					None,
					'http://www.fullhdfilmizlet.com/wp-content/themes/basizlev1/images/logo.png',
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe) 

			if(len(video_list_temp)<1):
				print 'ERROR fullhdfilmizlet CAT LIST_LEN = %s' %  len(video_list_temp) 
		except:
			print 'ERROR get_fullhdfilmizlet_category'  

		return video_list_temp  

	def get_fullhdfilmizlet_category_films(self, url):
		#print 'get_fullhdfilmizlet_category_films'
		try:              
			page = mod_request(url)
			#print page
			video_list_temp = [] 
			chan_counter = 0

 			regex = re.findall(r'<a href="http:\/\/(.*?)" .*?><img src=".*?" alt="(.*?)" class="captify" \/><\/a>',page)
 			##img_url = re.findall(r'<div class="content">\n.*?<p><img src="(http:\/\/.*?)"',page)
			##descr = re.findall(r'<strong>Film Konusu:<\/strong><\/span>(.*?)<br \/>',page)

			#print regex

			for text in regex:

				url = text[0]
				title = text[1]
				#title = re.sub('#8211;', '', title)
				#title = re.sub('&#038;', '', title)
				#img_url =  text[2]
				#print img_url
				#descr =  text[3]
				chan_counter +=1
				chan_tulpe = (
					chan_counter,
					title,
					None,
					None,
					None,
					'nStreamModul@' + url + '@film@' + title,
					None,
					None,
					'',
					None,
					None
				)  
				video_list_temp.append(chan_tulpe)

			next = re.findall(r'<span class=.current.>\d+<\/span><a href=.(http:\/\/\b[^>]*). class=.page larger.>', page)
			prev = re.findall(r'<a href=.(http:\/\/\b[^>]*). class=.page smaller.>\d+<\/a><span class=.current.>', page)
			                    
			if len(next):
				self.next_page_url = next[-1].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.next_page_text = 'SONRAKI' 
			
			if len(prev):
				self.prev_page_url = prev[0].replace('http://', 'nStreamModul@') + '@category_page@' + self.playlist_cat_name
				self.prev_page_text = 'ONCEKI'
			else:	
				self.prev_page_url = 'nStreamModul@fullhdfilmizlet.com@start@fullhdfilmizlet KATEGORILER'
				self.prev_page_text = 'KATEGORILER'   		                                                           

			if(len(video_list_temp)<1):
				print 'ERROR fullhdfilmizlet CAT_FIL LIST_LEN = %s' %  len(video_list_temp)    
		except:
			print 'ERROR get_fullhdfilmizlet_category_films' 

		return video_list_temp

	def get_fullhdfilmizlet_film(self, url): 
		page = mod_request(url)
		#page = re.sub('\n','', page) 
		chan_counter = 0
		video_list_temp = []

		vk = re.findall(r'<iframe.*?src="(.*?)" width="\d+" height="\d+" frameborder="\d+"><\/iframe>',page)
		#descr = re.findall(r'<strong>Film Konusu:<\/strong><\/span>(.*?)<br \/>',page) 
		#img = re.findall(r'<p><img src="(http:\/\/.*?)" alt="" title=".*?" width="\d+" height="\d+".*? \/>',page)
		if(len(vk)>0):
			for text in vk:
				text=text.replace("amp;", "")
				chan_counter = chan_counter + 1 
				chan_tulpe = (
					chan_counter,
					self.kino_title + ' Parca :' + str(chan_counter),
					None,
					None,
					text,
					None,
					None,
					None,
					'',
					None,
					None
				)
				video_list_temp.append(chan_tulpe)		

				self.prev_page_url = 'nStreamModul@' + self.category_back_url + '@category_page@' + self.playlist_cat_name
		self.prev_page_text = self.playlist_cat_name   	

		return video_list_temp 


                   
# chan_tulpe = (
# 	chan_counter,
# 	name,
# 	description,
# 	picon_url,
# 	stream_url,
# 	playlist_url,
# 	category_id,
# 	img_src,
# 	description4playlist_html,
# 	protected
#	ts_stream (IPTV quickzapping)
# )
# iptv_list_temp.append(chan_tulpe) 