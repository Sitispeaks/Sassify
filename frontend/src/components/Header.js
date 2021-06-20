import React from "react";
import { Navbar, Nav, Container, Row, NavDropdown } from "react-bootstrap";
import { useDispatch, useSelector } from 'react-redux'
import { LinkContainer } from 'react-router-bootstrap'
import { logout } from '../actions/userActions'
import SearchBox from "./SearchBox";
function Header() {

  const userLogin = useSelector(state => state.userLogin)
  const { userInfo } = userLogin

  const dispatch = useDispatch()
  const logoutHandler = () => {
    dispatch(logout())
    console.log("logged out!!")
  }




  return (
    <header>
      <Navbar bg="dark" variant="dark" expand="lg" collapseOnSelect>
        <Container>
          <LinkContainer to="/">
            <Navbar.Brand >PIXELRENT</Navbar.Brand>
          </LinkContainer>


          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <SearchBox/>
            <Nav className="ml-auto">


              <LinkContainer to="/cart">
                <Nav.Link ><i className="fas fa-shopping-cart"></i>Cart</Nav.Link>
              </LinkContainer>


              {userInfo ? (
                <NavDropdown title={userInfo.name} id='username'>
                  <LinkContainer to='/profile'>
                    <NavDropdown.Item>Profile</NavDropdown.Item>
                  </LinkContainer>

                  <NavDropdown.Item onClick={logoutHandler}>Logout</NavDropdown.Item>

                </NavDropdown>
              ) : (
                <LinkContainer to='/login'>
                  <Nav.Link><i className="fas fa-user"></i>Login</Nav.Link>
                </LinkContainer>
              )}

              
              {userInfo && userInfo.isAdmin && (
                <NavDropdown title='Admin' id='adminmenue'>
                  <LinkContainer to='/admin1/userlist'>
                    <NavDropdown.Item>Users</NavDropdown.Item>
                  </LinkContainer>

                  <LinkContainer to='/admin1/productlist'>
                    <NavDropdown.Item>Products</NavDropdown.Item>
                  </LinkContainer>

                  <LinkContainer to='/admin1/orderlist'>
                    <NavDropdown.Item>Orders</NavDropdown.Item>
                  </LinkContainer>

                </NavDropdown>
              )}

            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
}

export default Header;
