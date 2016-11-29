from flask import Flask, render_template, request, jsonify
from secrets import spotify, jambase
import urllib2, json
import spotipy

app = Flask(__name__)

# API information
j_key = jambase['key']
j_key2 = jambase['key2']
jambase_url = 'http://api.jambase.com/'
s_key = spotify['id']
spotify = spotipy.Spotify()

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
		radius = 50
		# Gets the information based off of the location
		if term is not None:
			# Sets the query for the API search
			search = jambase_url + 'events?api_key=' + j_key + '&zipCode=' + term + '&radius=' + radius + '&page=0&o=json'
			res = urllib2.urlopen(search)
			try:
				events = json.load(res)['Events']
				total = len(res['Events'])
			except urllib2.HTTPError, e:
				print "The server couldn't fulfill the request"
				print "Error code: ", e.code
				total = 0
				events = "No events found. Please try again"
			except urllib2.URLError, e:
				print "We failed to reach a server"
				print "Reason: ", e.reason
				total = 0
				events = "No events found. Please try again"
			except:
				total = 0
				events = "No events found. Please try again"
		else:
			# Invalid parameters
			abort(400)

	elif method == 'venue':
		term = term.replace(' ', '+')
		# Gets the venue Id given the venue name
		if term is not None:
			search = jambase_url + 'venues?api_key=' + j_key + '&name=' + term + '&page=0' + '&o=json'
			res = urllib2.urlopen(search)
			try:
				venueId = str(json.load(res)['Venues'][0]['Id'])
				print str(venuId)
			except urllib2.HTTPError, e:
				print "The server couldn't fulfill the request"
				print "Error code: ", e.code
				venueId = None
			except urllib2.URLError, e:
				print "We failed to reach a server"
				print "Reason: ", e.reason
				venueId = None
			except:
				venueId = None
		else:
			# Invalid parameters
			abort(400)
		# Generates the list of events happening at the given venue Id
		if venueId is not None:
			search = jambase_url + 'events?api_key=' + j_key + '&venueId=' + venueId
			print search
			res = urllib2.urlopen(search)
			try:
				events = json.load(res)['Events']
				total = len(res['Events'])
			except urllib2.HTTPError, e:
				print "The server couldn't fulfill the request"
				print "Error code: ", e.code
				total = 0
				events = "No events found. Please try again"
			except urllib2.URLError, e:
				print "We failed to reach a server"
				print "Reason: ", e.reason
				total = 0
				events = "No events found. Please try again"
			except:
				total = 0
				events = "No events found. Please try again"
		else:
			total = 0
			events = "No events found. Please try again"

	elif method == 'artist':
		term = term.replace(' ', '%20')
		# Gets the artists Id given their name
		if term is not None:
			search = jambase_url + 'artists?api_key=' + j_key2 + '&name=' + term + "&o=json"
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
				artistId = str(json.load(res)['Artists'][0]['Id'])
		else:
			abort(400)
		# Gets a list of all the artists playing at the event the given artist is playing at based off of their Id
		if artistId is not None:
			search = jambase_url + 'events?api_key=' + j_key2 + '&artistId=' + artistId + "&o=json"
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
				events = json.load(res)['Events']
				total = len(events)
		else:
			total = 0
			events = "No events found. Please try again."
	else:
		events = "Invalid parameters."
		total = 0

	# Generates the JSON for the information
	return jsonify({'events': events, 'total': total})

# GEnerates the spotify playlist based on selected concert
@app.route('/api/gen_playlist', methods=['POST'])
def gen_playlist():
	artists = request.form['artists']
	for artist in artists:
		print artist
	playlist = artists
	return jsonify({'playlist': playlist})
