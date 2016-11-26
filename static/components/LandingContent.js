import React from 'react';

import FormGroup from 'react-bootstrap/lib/FormGroup';
import InputGroup from 'react-bootstrap/lib/InputGroup';
import FormControl from 'react-bootstrap/lib/FormControl';
import Button from 'react-bootstrap/lib/Button';

var LandingContent = React.createClass({
	handleSearchChange: function(e) {
		this.props.onSearchChange(e.target.value);
	},
	handleSelectChange: function(e) {
		this.props.onSelectChange(e.target.value);
	},
	render: function() {
		return (
			<div className="landing-info">	
				<img src="static/logo.png" className="brand" />
				<div className="landing-content">
					<form className="landing-form" onSubmit={this.props.onSubmit}>
						<FormGroup>
							<InputGroup>
								<FormControl 
									type="text" 
									placeholder="Search..." 
									name="search" 
									onChange={this.handleSearchChange} />
								<InputGroup>
									<FormControl 
										componentClass="select" 
										name="method"
										onChange={this.handleSelectChange}>
										<option value="concert">Concert Name</option>
										<option value="artist">Artist</option>
										<option value="venue">Venue Name</option>
										<option value="location">Location</option>
									</FormControl>
								</InputGroup>
		        				<InputGroup.Button>
		        					<Button type="submit"><i className="fa fa-search"></i></Button>
		        				</InputGroup.Button>
	        				</InputGroup>
						</FormGroup>
					</form>
					<p>Sign in with Spotify.</p>
				</div>
			</div>
		);
	}
});

export default LandingContent;