import React from 'react';
import LandingContent from './LandingContent';

var LandingPage = React.createClass({
	getInitialState: function() {
		return {background: "Pause"};
	},
	handleSearchChange: function(e) {
		this.props.onSearchChange(e);
	},
	handleSelectChange: function(e) {
		this.props.onSelectChange(e);
	},
	handleStopClick: function() {
		var video = document.querySelector('.bgVid');
		var body = document.querySelector('body');
		if (this.state.background == "Pause") {
			this.setState({background: "Resume"});
			video.style.display = "None";
			body.style.background = "url(static/background.png) center fixed no-repeat";
			body.style.backgroundColor = "black";
			body.style.zIndex = "-100";
		} else {
			this.setState({background: "Pause"});
			video.style.display = "Inherit";
		}
	},
	render: function() {
		return (
			<div className="landing">
				<video src="static/background.mp4" 
					type="video/mp4"
					muted
					autoPlay
					loop
					className="bgVid">
				</video>
				<LandingContent 
					onSubmit={this.props.onSubmit} 
					onSearchChange={this.handleSearchChange}
					onSelectChange={this.handleSelectChange}
					/>
				<div className="stop-btn">
					<button onClick={this.handleStopClick}>{this.state.background} Background</button>
				</div>
			</div>
		);
	}
});

export default LandingPage;
