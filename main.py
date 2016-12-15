from flask import Flask, render_template, request, jsonify, session, redirect
from secrets import spotify, seatgeek, secret
import urllib2, json, urllib

app = Flask(__name__)
# For session storage (in place of a database)
app.secret_key = secret['secret']

# API information
s_key = spotify['id']
s_secret = spotify['secret']
spotify_url = 'https://api.spotify.com/v1/'
spot_auth = 'https://accounts.spotify.com/authorize'

sg_id = seatgeek['id']
sg_secret = seatgeek['secret']
s_geek_url = 'https://api.seatgeek.com/2'

redirect_1 = 'http://localhost:8080/spotify/auth/handle'#'https:///concertearly.appspot.com/spotify/auth/handle'

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

@app.route('/get_user', methods=['GET'])
def get_user():
	if 'access' in session:
		url = '%sme'%(spotify_url)
		try:
			req = urllib2.Request(url)
			req.add_header('Authorization', 'Bearer ' + session['access'])
			res = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print "The server couldn't fulfill the request"
			print "Error code: ", e.code
		except urllib2.URLError, e:
			print "We failed to reach a server"
			print "Reason: ", e.reason
		else:
			res = json.load(res)
			session['spot_href'] = res['href']
			return jsonify(res)
	else:
		return jsonify({'user': ''})

# Deletes the users access token from the session
@app.route('/signout', methods=['GET'])
def signout():
	session.pop('access', None)
	session.pop('refresh', None)
	session.pop('spot_href', None)
	return redirect('/')

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
	return jsonify(details)

# Creates playlist
@app.route('/api/create_playlist', methods=['POST'])
def create_playlist():
	tracks = request.form.getlist('tracks[]')
	name = request.form['playlist_name']
	url = '%s/playlists'%(session['spot_href'])
	try:
		params = {'name': name}
		headers = {'Authorization': 'Bearer ' + session['access'], 'Content-Type': 'application/json'}
		req = urllib2.Request(url, json.dumps(params), headers)
		res = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "The server couldn't fulfill the request"
		print "Error code: ", e.code
	except urllib2.URLError, e:
		print "We failed to reach a server"
		print "Reason: ", e.reason
	else:
		href = json.load(res)['href'] + '/tracks'
		print href
		try:
			params = {'uris': tracks}
			headers = {'Authorization': 'Bearer ' + session['access'], 'Content-Type': 'application/json'}
			req = urllib2.Request(href, json.dumps(params), headers)
			res = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print "The server couldn't fulfill the request"
			print "Error code: ", e.code
		except urllib2.URLError, e:
			print "We failed to reach a server"
			print "Reason: ", e.reason
		else:
			return jsonify({'success': 1})
	return jsonify({'success': -1})

# Logs user into their spotify account
@app.route('/spotify/auth', methods=['GET'])
def spotify_auth():
	scopes = "playlist-modify playlist-modify-public streaming"
	cred = urllib.urlencode({'client_id': s_key, 'response_type': 'code', 'redirect_uri': redirect_1, 'scope': scopes})
	url = "%s?%s"%(spot_auth, cred)

	return redirect(url)

# Logs user into their spotify account
@app.route('/spotify/auth/handle', methods=['GET'])
def spotify_auth_handler():
	code = request.args.get('code', '')
	state = request.args.get('state', '')
	error = request.args.get('error', '')
	if code:
		params = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_1, 'client_id': s_key, 'client_secret': s_secret}
		params = urllib.urlencode(params)
		url = 'https://accounts.spotify.com/api/token'
		try:
			res = urllib2.urlopen(url, params)
		except urllib2.HTTPError, e:
			print "The server couldn't fulfill the request"
			print "Error code: ", e.code
		except urllib2.URLError, e:
			print "We failed to reach a server"
			print "Reason: ", e.reason
		else:
			res = json.load(res)
			session['access'] = res['access_token']
			session['refresh'] = res['refresh_token']
	elif error:
		print str(error)
	else:
		print "Invalid request"
	return redirect('/')
