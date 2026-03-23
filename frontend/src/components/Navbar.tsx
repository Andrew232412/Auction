import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { isAuthenticated, logout } from '../services/auth';

const Nav = styled.nav`
  background-color: #2c3e50;
  color: white;
  padding: 15px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const NavContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Brand = styled(Link)`
  font-size: 24px;
  font-weight: bold;
  color: white;
  text-decoration: none;

  &:hover {
    color: #ecf0f1;
  }
`;

const NavLinks = styled.div`
  display: flex;
  gap: 20px;
  align-items: center;
`;

const NavLink = styled(Link)`
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s;

  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
`;

const LogoutButton = styled.button`
  background-color: transparent;
  color: white;
  border: 1px solid white;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    background-color: white;
    color: #2c3e50;
  }
`;

const Navbar: React.FC = () => {
  return (
    <Nav>
      <NavContainer>
        <Brand to="/">Auction System</Brand>
        <NavLinks>
          <NavLink to="/">Auctions</NavLink>
          {isAuthenticated() ? (
            <>
              <NavLink to="/create-auction">Create Auction</NavLink>
              <NavLink to="/profile">Profile</NavLink>
              <LogoutButton onClick={logout}>Logout</LogoutButton>
            </>
          ) : (
            <>
              <NavLink to="/login">Login</NavLink>
              <NavLink to="/register">Register</NavLink>
            </>
          )}
        </NavLinks>
      </NavContainer>
    </Nav>
  );
};

export default Navbar;
