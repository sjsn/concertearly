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

aid = '&aid=12402'

redirect_1 = 'http://localhost:8080/spotify/auth/handle'#'https://concertearly.appspot.com/spotify/auth/handle'

# Renders main page
@app.route('/', methods=['GET', 'POST'])
def main():
	return render_template('index.html')

# Returns a list of concerts by the artist
@app.route('/api/get_events', methods=['POST'])
def get_events():
	method = request.form['method']
	term = request.form['search']
	if method == 'zip':
		# Gets the events Id given its zipcode
		if term is not None:
			search = s_geek_url + '/venues?postal_code=' + term + '&client_id=' + sg_id + '&client_secret=' + sg_secret + aid
		try:
			res = urllib2.urlopen(search)
		except urllib2.HTTPError, e:
			print "The server couldn't fulfill the request"
			print "Error code: ", e.code
			venues = None
		except urllib2.URLError, e:
			print "We failed to reach a server"
			print "Reason: ", e.reason
			venues = None
		else:
			venues = json.load(res)['venues']
			print venues
			if len(venues) > 0:
				venueIds = [venue['id'] for venue in venues]
			else:
				venueIds = None
		if venueIds is not None:
			urls = [(s_geek_url + '/events?venue.id=' + str(venueId) + '&client_id=' + sg_id + '&client_secret=' + sg_secret + '&taxonomies.name=concert' + aid) for venueId in venueIds]
			final_events = []
			final_total = 0
			for url in urls:
				try:
					res = urllib2.urlopen(url)
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
					for event in events:
						final_events.append(event)
						final_total += total
			events = final_events
			total = final_total
		else:
			events = []
			total = 0
	elif method == 'city':
		term = term.replace(' ', '+')
		# Gets the events Id given its zipcode
		if term is not None:
			search = s_geek_url + '/venues?city=' + term + '&client_id=' + sg_id + '&client_secret=' + sg_secret + aid
		try:
			res = urllib2.urlopen(search)
		except urllib2.HTTPError, e:
			print "The server couldn't fulfill the request"
			print "Error code: ", e.code
			venues = None
		except urllib2.URLError, e:
			print "We failed to reach a server"
			print "Reason: ", e.reason
			venues = None
		else:
			venues = json.load(res)['venues']
			if len(venues) > 0:
				venueIds = [venue['id'] for venue in venues]
			else:
				venueIds = None
		if venueIds is not None:
			urls = [(s_geek_url + '/events?venue.id=' + str(venueId) + '&client_id=' + sg_id + '&client_secret=' + sg_secret + '&taxonomies.name=concert' + aid) for venueId in venueIds]
			final_events = []
			final_total = 0
			for url in urls:
				try:
					res = urllib2.urlopen(url)
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
					for event in events:
						final_events.append(event)
						final_total += total
			events = final_events
			total = final_total
		else:
			events = []
			total = 0
	elif method == 'venue':
		term = term.replace(' ', '+')
		# Gets the events Id given its name
		if term is not None:
			search = s_geek_url + '/venues?q=' + term + '&client_id=' + sg_id + '&client_secret=' + sg_secret + aid
		try:
			res = urllib2.urlopen(search)
		except urllib2.HTTPError, e:
			print "The server couldn't fulfill the request"
			print "Error code: ", e.code
			venueId = None
		except urllib2.URLError, e:
			print "We failed to reach a server"
			print "Reason: ", e.reason
			venueId = None
		else:
			venues = json.load(res)['venues']
			if len(venues) > 0:
				venueIds = [venue['id'] for venue in venues]
			else:
				venueIds = None
		if venueIds is not None:
			urls = [(s_geek_url + '/events?venue.id=' + str(venueId) + '&client_id=' + sg_id + '&client_secret=' + sg_secret + '&taxonomies.name=concert' + aid) for venueId in venueIds]
			final_events = []
			final_total = 0
			for url in urls:
				try:
					res = urllib2.urlopen(url)
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
					events = json.load(res)
					events = events['events']
					total = len(events)					
					for event in events:
						final_events.append(event)
						final_total += total
			events = final_events
			total = final_total
		else:
			events = []
			total = 0
	elif method == 'concert':
		term = term.replace(' ', '+')
		# Gets the concert Id given its name
		if term is not None:
			search = s_geek_url + '/events?q=' + term + '&client_id=' + sg_id + '&client_secret=' + sg_secret + aid
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
			events = []
			total = 0
	elif method == 'artist':
		term = term.replace(' ', '+')
		# Gets the artists Id given their name
		if term is not None:
			search = s_geek_url + '/performers?q=' + term + '&client_id=' + sg_id + '&client_secret=' + sg_secret + aid
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
			performers = json.load(res)['performers']
			if len(performers) > 0:
				artistId = str(performers[0]['id'])
			else:
				artistId = None
		if artistId is not None:
			search = s_geek_url + '/events?performers.id=' + artistId + '&client_id=' + sg_id + '&client_secret=' + sg_secret + '&taxonomies.name=concert' + aid
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
			events = []
			total = 0
	else:
		events = "Invalid parameters."
		total = 0
	# Generates the JSON for the information
	return jsonify({'events': events, 'total': total})

# Returns the user information if they're logged in
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

# Generates the potential spotify playlist based on the selected concert
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
			if res['artists']['total'] > 0:
				item['id'] = res['artists']['items'][0]['id']
				if len(res['artists']['items'][0]['images']) > 0:
					item['image'] = res['artists']['items'][0]['images'][0]['url']
				else:
					item['image'] = 'static/logo.png'
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
	if 'access' in session:
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
			res = json.load(res)
			href = res['href'] + '/tracks'
			playlist_uri = res['uri']
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
				return jsonify({'success': 1, 'uri': playlist_uri})
		return jsonify({'success': -1})
	else:
		return jsonify({'success': -1})

# Logs user into their spotify account part 1
@app.route('/spotify/auth', methods=['GET'])
def spotify_auth():
	scopes = "playlist-modify playlist-modify-public streaming"
	cred = urllib.urlencode({'client_id': s_key, 'response_type': 'code', 'redirect_uri': redirect_1, 'scope': scopes})
	url = "%s?%s"%(spot_auth, cred)
	return redirect(url)

# Logs user into their spotify account part 2
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
