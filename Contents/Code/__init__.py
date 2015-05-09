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
BASE_URL = "http://afdah.tv"
MOVIES_URL = "http://afdah.tv"

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
	HTTP.Headers['Referer'] = 'afdah.tv'
	
######################################################################################
# Menu hierarchy

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	page_data = HTML.ElementFromURL(BASE_URL)
	
	for each in page_data.xpath("//ul[@class='genres']/li"):
		url = each.xpath("./a/@href")[0]
		title = each.xpath("./a/span/text()")[0]

		oc.add(DirectoryObject(
			key = Callback(ShowCategory, title = title, category = title, page_count=1),
			title = title,
			thumb = R(ICON_MOVIES)
			)
		)
	return oc

######################################################################################
@route(PREFIX + "/showcategory")	
def ShowCategory(title, category, page_count):

	oc = ObjectContainer(title1 = title)
	page_data = HTML.ElementFromURL(BASE_URL + '/genre/' + str(category) + '/page/' + str(page_count))
	
	for each in page_data.xpath("//div[contains(@class,'entry clearfix')]"):
		url = each.xpath("./h3/a/@href")[0]
		title = each.xpath("./h3/a/text()")[0]
		thumb = each.xpath("./div[@class='entry-thumbnails']/a/img/@src")[0]

		oc.add(DirectoryObject(
			key = Callback(EpisodeDetail, title = title, url = url),
			title = title,
			thumb = BASE_URL + thumb
			)
		)

	oc.add(NextPageObject(
		key = Callback(ShowCategory, title = category, category = category, page_count = int(page_count) + 1),
		title = "More...",
		thumb = R(ICON_NEXT)
			)
		)
	
	return oc

######################################################################################
@route(PREFIX + "/episodedetail")
def EpisodeDetail(title, url):
	
	oc = ObjectContainer(title1 = title)
	page_data = HTML.ElementFromURL(url)
	title = page_data.xpath("//h1[@class='entry-title']/a/text()")[0].replace('Watch ','',1).replace(' Online','',1)
	description = page_data.xpath("//div[contains(@style,'line-height:1.4')]/text()")[0]
	thumb = page_data.xpath("//img[@height='160']/@src")[0]
	
	oc.add(VideoClipObject(
		url = url,
		title = title,
		thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-cover.png'),
		summary = description
		)
	)	

	return oc
	