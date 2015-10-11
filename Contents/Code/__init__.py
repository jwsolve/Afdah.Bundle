######################################################################################
#
#	Afdah.tv - v0.01
#
######################################################################################

TITLE = "Afdah"
PREFIX = "/video/afdah"
ART = "art-default.jpg"
ICON = "icon-default.png"
ICON_LIST = "icon-list.png"
ICON_COVER = "icon-cover.png"
ICON_SEARCH = "icon-search.png"
ICON_NEXT = "icon-next.png"
ICON_MOVIES = "icon-movies.png"
ICON_SERIES = "icon-series.png"
ICON_QUEUE = "icon-queue.png"
BASE_URL = "http://www.afdah.ws"
MOVIES_URL = "http://www.afdah.ws"

import updater
updater.init(repo = '/jwsolve/afdah.bundle', branch = 'master')

######################################################################################
# Set global variables

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON_LIST)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_MOVIES)
	VideoClipObject.art = R(ART)
	
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
	HTTP.Headers['Cookie'] = 'path=/;'
	HTTP.Headers['Cookie'] = 'domain=.afdah.ws;'

####################################################################################################
def ValidatePrefs():

	try:
		test = HTTP.Request(Prefs['site_url'], cacheTime=0).content
	except:
		return ObjectContainer(header='Invalid URL', message='Please input a valid and existing URL, including http://')
	
######################################################################################
# Menu hierarchy

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():

	container = ObjectContainer()
	page_data = HTML.ElementFromURL(Prefs['site_url'])
	updater.add_button_to(container, PerformUpdate)
	container.add(PrefsObject(title='Preferences'))
	for each in page_data.xpath("//ul[contains(@class,'main-menu')]/li"):
		url = each.xpath("./a/@href")[0]
		title = each.xpath("./a/text()")[0]

		container.add(DirectoryObject(
			key = Callback(ShowCategory, title = title, category = title.lower(), page_count=1),
			title = title,
			thumb = R(ICON_MOVIES)
			)
		)
	return container

######################################################################################
@route(PREFIX + "/performupdate")
def PerformUpdate():
	return updater.PerformUpdate()

######################################################################################
@route(PREFIX + "/showcategory")	
def ShowCategory(title, category, page_count):

	oc = ObjectContainer(title1 = title)
	page_data = HTML.ElementFromURL(Prefs['site_url'] + '/movies/' + str(category) + '/page/' + str(page_count) + '/')
	
	for each in page_data.xpath("//div[@class='short-item']"):
		url = each.xpath("./a/@href")[0]
		title = each.xpath("./a/img/@alt")[0]
		thumb = each.xpath("./a/img/@src")[0]

		oc.add(DirectoryObject(
			key = Callback(EpisodeDetail, title = title, url = url),
			title = title,
			thumb = Prefs['site_url'] + thumb
			)
		)

	oc.add(NextPageObject(
		key = Callback(ShowCategory, title = category, category = category.lower(), page_count = int(page_count) + 1),
		title = "Next...",
		thumb = R(ICON_NEXT)
			)
		)
	
	return oc

######################################################################################
@route(PREFIX + "/episodedetail")
def EpisodeDetail(title, url):
	
	oc = ObjectContainer(title1 = title)
	page_data = HTML.ElementFromURL(url)
	title = page_data.xpath("//h2/text()")[0].replace('Watch ','',-1).replace(' Online HD','',-1)
	description = page_data.xpath("//meta[@name='description']/@content")[0].strip()
	thumb = page_data.xpath("//div[@class='poster']/img/@src")[0]
	
	oc.add(VideoClipObject(
		url = url,
		title = title,
		thumb = Resource.ContentsOfURLWithFallback(url = Prefs['site_url'] + thumb, fallback='icon-cover.png'),
		summary = description
		)
	)	

	return oc
