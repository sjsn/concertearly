from flask import Flask, render_template, request, jsonify
from secrets import spotify, seatgeek
import urllib2, json

app = Flask(__name__)

# API information
jambase_url = 'http://api.jambase.com/'
s_key = spotify['id']
spotify_url = 'https://api.spotify.com/v1/'
sg_id = seatgeek['id']
sg_secret = seatgeek['secret']
s_geek_url = 'https://api.seatgeek.com/2'

# Renders main page
@app.route('/', methods=['GET', 'POST'])
def main():
	return render_template('index.html')

# Returns a list of concerts by the artist
@app.route('/api/get_events', methods=['POST'])
def get_events():
	method = request.form['method']
	term = request.form['search']
	if method == 'location':
		return None
	# 	radius = 50
	# 	# Gets the information based off of the location
	# 	if term is not None:
	# 		# Sets the query for the API search
	# 		search = jambase_url + 'events?api_key=' + j_key + '&zipCode=' + term + '&radius=' + radius + '&page=0&o=json'
	# 		res = urllib2.urlopen(search)
	# 		try:
	# 			events = json.load(res)['Events']
	# 			total = len(res['Events'])
	# 		except urllib2.HTTPError, e:
	# 			print "The server couldn't fulfill the request"
	# 			print "Error code: ", e.code
	# 			total = 0
	# 			events = "No events found. Please try again"
	# 		except urllib2.URLError, e:
	# 			print "We failed to reach a server"
	# 			print "Reason: ", e.reason
	# 			total = 0
	# 			events = "No events found. Please try again"
	# 		except:
	# 			total = 0
	# 			events = "No events found. Please try again"
	# 	else:
	# 		# Invalid parameters
	# 		abort(400)

	# elif method == 'venue':
	# 	term = term.replace(' ', '+')
	# 	# Gets the venue Id given the venue name
	# 	if term is not None:
	# 		search = jambase_url + 'venues?api_key=' + j_key + '&name=' + term + '&page=0' + '&o=json'
	# 		res = urllib2.urlopen(search)
	# 		try:
	# 			venueId = str(json.load(res)['Venues'][0]['Id'])
	# 			print str(venuId)
	# 		except urllib2.HTTPError, e:
	# 			print "The server couldn't fulfill the request"
	# 			print "Error code: ", e.code
	# 			venueId = None
	# 		except urllib2.URLError, e:
	# 			print "We failed to reach a server"
	# 			print "Reason: ", e.reason
	# 			venueId = None
	# 		except:
	# 			venueId = None
	# 	else:
	# 		# Invalid parameters
	# 		abort(400)
	# 	# Generates the list of events happening at the given venue Id
	# 	if venueId is not None:
	# 		search = jambase_url + 'events?api_key=' + j_key + '&venueId=' + venueId
	# 		print search
	# 		res = urllib2.urlopen(search)
	# 		try:
	# 			events = json.load(res)['Events']
	# 			total = len(res['Events'])
	# 		except urllib2.HTTPError, e:
	# 			print "The server couldn't fulfill the request"
	# 			print "Error code: ", e.code
	# 			total = 0
	# 			events = "No events found. Please try again"
	# 		except urllib2.URLError, e:
	# 			print "We failed to reach a server"
	# 			print "Reason: ", e.reason
	# 			total = 0
	# 			events = "No events found. Please try again"
	# 		except:
	# 			total = 0
	# 			events = "No events found. Please try again"
	# 	else:
	# 		total = 0
	# 		events = "No events found. Please try again"

	elif method == 'artist':
		term = term.replace(' ', '+')
		# Gets the artists Id given their name
		if term is not None:
			search = s_geek_url + '/performers?q=' + term + '&client_id=' + sg_id + '&client_secret=' + sg_secret
		try:
			res = urllib2.urlopen(search)
		except urllib2.HTTPError, e:
			print "The server couldn't fulfill the request"
			print "Error code: ", e.code
			artistId = None
		except urllib2.URLError, e:
			print "We failed to reach a server"
			print "Reason: ", e.reason
			artistId = None
		else:
			artistId = str(json.load(res)['performers'][0]['id'])
		if artistId is not None:
			search = s_geek_url + '/events?performers.id=' + artistId + '&client_id=' + sg_id + '&client_secret=' + sg_secret
			try:
				res = urllib2.urlopen(search)
			except urllib2.HTTPError, e:
				print "The server couldn't fulfill the request"
				print "Error code: ", e.code
				total = 0
				events = "No events found. Please try again."
			except urllib2.URLError, e:
				print "We failed to reach a server"
				print "Reason: ", e.reason
				total = 0
				events = "No events found. Please try again."
			else:
				events = json.load(res)['events']
				total = len(events)
	else:
		events = "Invalid parameters."
		total = 0

	# Generates the JSON for the information
	return jsonify({'events': events, 'total': total})

# Generates the spotify playlist based on the selected concert
@app.route('/api/gen_playlist', methods=['POST'])
def gen_playlist():
	artists = request.form.getlist('artists[]')
	numTracks = int(30 / len(artists))
	details = []
	for artist in artists:
		item = {}
		url_artist = artist.replace(' ', '%20')
		url = '%ssearch?type=artist&limit=1&q=artist:%s'%(spotify_url, url_artist)
		try:
			res = json.load(urllib2.urlopen(url))
		except urllib2.HTTPError, e:
			print "The server couldn't fulfill the request"
			print "Error code: ", e.code
		except urllib2.URLError, e:
			print "We failed to reach a server"
			print "Reason: ", e.reason
		else:
			item['name'] = artist
			if len(res['artists']['items']) > 0:
				item['id'] = res['artists']['items'][0]['id']
				item['image'] = res['artists']['items'][0]['images'][0]['url']
				track_url = '%sartists/%s/top-tracks?country=US'%(spotify_url, item['id'])
				try:
					res = json.load(urllib2.urlopen(track_url))['tracks']
				except urllib2.HTTPError, e:
					print "The server couldn't fulfill the request"
					print "Error code: ", e.code
				except urllib2.URLError, e:
					print "We failed to reach a server"
					print "Reason: ", e.reason
				else:
					item['tracks'] = [{}]
					for track in res[:numTracks]:
						song = {}
						song['name'] = track['name']
						song['sample'] = track['preview_url']
						song['uri'] = track['uri']
						song['id'] = track['id']
						song['album'] = track['album']['name']
						item['tracks'].append(song)
					details.append(item)
	# print jsonify({'details': details})
	return jsonify(details)

@app.route('/api/create_playlist', methods=['POST'])
def create_playlist():
	artists = request.form['artists']
	return None
