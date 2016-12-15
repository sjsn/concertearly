import React from 'react';

import Search from './Search';

import Navbar from 'react-bootstrap/lib/Navbar';
import Nav from 'react-bootstrap/lib/Nav';
import NavItem from 'react-bootstrap/lib/NavItem';
import NavDropdown from 'react-bootstrap/lib/NavDropdown';
import MenuItem from 'react-bootstrap/lib/MenuItem';

var Navigation = React.createClass({
	handleSearchChange: function(e) {
		this.props.onSearchChange(e);
	},
	handleSelectChange: function(e) {
		this.props.onSelectChange(e);
	},
	render: function() {
		return (
			<Navbar className='navigation' fixedTop>
				<Navbar.Header>
					<Navbar.Brand>
						<a href="/"> 
							Concert Early	
						</a>
					</Navbar.Brand>
				</Navbar.Header>
				<Nav>
					<Navbar.Form pullLeft>
						<Search 
							onSubmit={this.props.onSubmit} 
							onSearchChange={this.handleSearchChange}
							onSelectChange={this.handleSelectChange}
							className='nav-form'
							/>
					</Navbar.Form>
				</Nav>
			</Navbar>
		);
	}
});

export default Navigation;
