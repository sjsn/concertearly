import React from 'react';
import ReactDOM from 'react-dom';

import Nav from './components/Nav'

var App = React.createClass({
	render: function() {
		return (
			<Nav />
			);
	}
});

ReactDOM.render(
	<App />,
	document.getElementById('content')
);