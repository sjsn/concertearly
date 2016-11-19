module.exports = {
	// List of entry points
	entry: [
		__dirname + '/static/app.js'
	],
	output: {
		filename: 'bundle.js',
		path: __dirname + '/static/dist'
	},
	module: {
		loaders: [
			{
				test: /\.jsx?$/,
				loader: "babel"
			}
		],
		query: {
			presets: ["react-hmre"]
		}
	}
};