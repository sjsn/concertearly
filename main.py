from flask import Flask, render_template, request, jsonify
from secrets import spotify, jambase
import urllib2, json
import spotipy

app = Flask(__name__)

j_key = jambase['key']
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
	print method
	if method == 'location':
		zipcode = str(request.args.get('zip', ''))
		radius = 50
		# Gets the information based off of the location
		if zipcode is not None:
			# Sets the query for the API search
			search = jambase_url + 'events?api_key=' + j_key + '&zipCode=' + zipcode + '&radius=' + radius + '&page=0' + + "&o=json"
			req = json.load(urllib2.urlopen(search))
			try:
				events = req['Events']
				total = len(req['Events'])
			except:
				total = 0
				events = "No events found. Please try again"
		else:
			# Invalid parameters
			abort(400)

	elif method == 'venue':
		venue_name = request.args.get('name', '')
		# Gets the venue Id given the venue name
		if venue_name is not None:
			search = jambase_url + 'venues?api_key=' + j_key + '&name=' + venue_name + + "&o=json"
			req = json.load(urllib2.urlopen(search))
			try:
				venueId = str(req['Venues'][0]['Id'])
			except:
				venueId = None
		else:
			# Invalid parameters
			abort(400)
		# Generates the list of events happening at the given venue Id
		if venueId is not None:
			search = jambase_url + 'events?api_key=' + j_key + '&venueId=' + venueId
			req = json.load(urllib2.urlopen(search))
			try:
				events = req['Events']
				total = len(req['Events'])
			except:
				total = 0
				events = "No events found. Please try again"
		else:
			total = 0
			events = "No events found. Please try again"

	elif method == 'artist':
		artist_name = request.form['search']
		artist_name = artist_name.replace(' ', '%20')
		# Gets the artists Id given their name
		if artist_name is not None:
			search = jambase_url + 'artists?api_key=' + j_key + '&name=' + artist_name + "&o=json"
			try:
				req = urllib2.Request(search)
				res = urllib2.urlopen(search)
			except urllib2.HTTPError, e:
				print "The server couldn't fulfill the request"
				print "Error code: ", e.code
				print "Other: ", e
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
			search = jambase_url + 'events?api_key=' + j_key + '&artistId=' + artistId + "&o=json"
			try:
				req = urllib2.Request(search)
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
