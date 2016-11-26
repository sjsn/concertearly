from flask import Flask, render_template, request
from secrets import spotify, jambase

app = Flask(__name__)

j_key = jambase['key']
s_key = spotify['id']

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'POST':
		term = request.form['search']
		method = request.form['method']
		results = None
	elif request.method == 'GET':
		results = None
	return render_template('index.html', results=results)

# Returns a list of concerts by the artist
# def get_events(term, method):
# 	if method == 'location':
# 		zipcode = str(request.args.get('zip', ''))
# 		radius = str(request.args.get('radius', ''))
# 		# Defaults search radius to 50 miles
# 		if radius is None or radius == '':
# 			radius = '50'
# 		# Gets the information based off of the location
# 		if zipcode is not None:
# 			# Sets the query for the API search
# 			search = jambase_url + 'events?api_key=' + j_key + '&zipCode=' + zipcode + '&radius=' + radius + '&page=0'
# 			req = requests.get(search)
# 			try:
# 				events = req.json()['Events']
# 				total = len(req.json()['Events'])
# 			except:
# 				total = 0
# 				events = "No events found. Please try again"
# 		else:
# 			# Invalid parameters
# 			abort(400)

# 	elif method == 'venue':
# 		venue_name = request.args.get('name', '')
# 		# Gets the venue Id given the venue name
# 		if venue_name is not None:
# 			search = jambase_url + 'venues?api_key=' + j_key + '&name=' + venue_name
# 			req = requests.get(search)
# 			try:
# 				venueId = str(req.json()['Venues'][0]['Id'])
# 			except:
# 				venueId = None
# 		else:
# 			# Invalid parameters
# 			abort(400)
# 		# Generates the list of events happening at the given venue Id
# 		if venueId is not None:
# 			search = jambase_url + 'events?api_key=' + j_key + '&venueId=' + venueId
# 			req = requests.get(search)
# 			try:
# 				events = req.json()['Events']
# 				total = len(req.json()['Events'])
# 			except:
# 				total = 0
# 				events = "No events found. Please try again"
# 		else:
# 			total = 0
# 			events = "No events found. Please try again"

# 	elif method == 'artist':
# 		artist_name = request.args.get('name', '')
# 		# Gets the artists Id given their name
# 		if artist_name is not None:
# 			search = jambase_url + 'artists?api_key=' + j_key + '&name=' + artist_name
# 			req = requests.get(search)
# 			try:
# 				artistId = str(req.json()['Artists'][0]['Id'])
# 			except:
# 				artistId = None
# 		else:
# 			abort(400)
# 		# Gets a list of all the artists playing at the event the given artist is playing at based off of their Id
# 		if artistId is not None:
# 			search = jambase_url + 'events?api_key=' + j_key + '&artistId=' + artistId
# 			req = requests.get(search)
# 			try:
# 				events = req.json()['Events']
# 				total = len(req.json()['Events'])
# 			except:
# 				total = 0
# 				events = "No events found. Please try again."
# 		else:
# 			total = 0
# 			events = "No events found. Please try again."
# 	else:
# 		events = "Invalid parameters."
# 		total = 0

# 	# Generates the JSON for the information
# 	return jsonify({'events': events, 'total': total})
