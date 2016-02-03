import sys
import urllib2
import re
from pprint import pprint
import subprocess

def reimu():
	if len( sys.argv ) > 1:
		for arg in sys.argv[1:]:
			get_embed_data( arg )
	else:
		print( "ugh" )

def get_embed_data( video_url ):
	video_id = re.search("v=([^&]*)", video_url)
	if video_id is None:
		return None
	video_id = video_id.groups()[0]

	youtube_embed_link = "https://www.youtube.com/embed/"
	youtube_video_link = "https://www.youtube.com/get_video_info?&video_id={id}&eurl=http%3A%2F%2Fwww%2Eyoutube%2Ecom%2F&sts={sts}"

	embed_data = urllib2.urlopen( urllib2.Request( youtube_embed_link + video_id ) ).read()

	sts_search = re.search( '"sts":(\d*)', embed_data )
	if sts_search is None:
		return None

	timestamp = sts_search.groups()[0]

	vars_url = youtube_video_link.format(id=video_id, sts=timestamp)
	formats = urllib2.unquote( urllib2.urlopen( urllib2.Request( vars_url ) ).read() ).decode('utf8').split(",")
	formats = [x for x in formats if x]
	streams = {}
	other_types = []
	types = {
		"5"   : "240p FLV",
		"18"  : "360p MP4",
		"22"  : "720p MP4",
		#"36"  : "240p 3GP",
		#"43"  : "360p WEBM",
		#"133" : "240p DASH",
		#"134" : "360p DASH",
		#"135" : "480p DASH",
		#"136" : "720p DASH",
	}
	for fmt in formats:
		parsed_format = dict( re.findall( "([^&=]*)=([^&]*)", fmt ) )
		if "itag" in parsed_format:
			if parsed_format["itag"] in types:
				streams[ types[ parsed_format["itag"] ] ] = urllib2.unquote(parsed_format["url"]).decode('utf8')
			else:
				other_types.append( parsed_format["itag"] )

	if "720p MP4" in streams:
		preferred = "720p MP4"
	elif "360p MP4" in streams:
		preferred = "360p MP4"
	else:
		print( "No valid video formats" )
		return None
	subprocess.call( "open -a QuickTime\ Player \"" + streams[ preferred ]+"\"", shell=True)

	#flash_vars = re.findall( "([^&=]*)=([^&]*)", unquoted )
	#return flash_vars