import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { usersAPI } from '../services/api';
import type { User } from '../types';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
`;

const Card = styled.div`
  background: white;
  padding: 30px;
  border-radius: 8px;
  margin-top: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h1`
  color: #2c3e50;
  margin-bottom: 20px;
`;

const Row = styled.div`
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #eee;

  &:last-child {
    border-bottom: none;
  }
`;

const Field = styled.span`
  color: #555;
  font-weight: 500;
`;

const Value = styled.span`
  color: #2c3e50;
`;

const Message = styled.p`
  color: #666;
  font-size: 15px;
`;

const ErrorMessage = styled.div`
  color: #f44336;
  font-size: 14px;
  margin-top: 10px;
`;

// Decode a JWT payload without verifying its signature (purely for reading `sub`).
const decodeTokenSubject = (token: string): string | null => {
  try {
    const payload = token.split('.')[1];
    if (!payload) return null;
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/');
    const decoded = JSON.parse(atob(normalized));
    return typeof decoded?.sub === 'string' ? decoded.sub : null;
  } catch {
    return null;
  }
};

const formatDate = (value?: string): string =>
  value ? new Date(value).toLocaleString() : '—';

const UserProfile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('You are not logged in.');
      setLoading(false);
      return;
    }

    const userId = decodeTokenSubject(token);
    if (!userId) {
      setError('Unable to read session token.');
      setLoading(false);
      return;
    }

    usersAPI
      .getUser(userId)
      .then((response) => setUser(response.data))
      .catch(() => setError('Failed to load profile.'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Container>
      <Card>
        <Title>User Profile</Title>
        {loading && <Message>Loading profile...</Message>}
        {error && <ErrorMessage>{error}</ErrorMessage>}
        {user && (
          <>
            <Row>
              <Field>Username</Field>
              <Value>{user.username}</Value>
            </Row>
            <Row>
              <Field>Email</Field>
              <Value>{user.email}</Value>
            </Row>
            <Row>
              <Field>Member since</Field>
              <Value>{formatDate(user.created_at)}</Value>
            </Row>
            <Row>
              <Field>Last updated</Field>
              <Value>{formatDate(user.updated_at)}</Value>
            </Row>
          </>
        )}
      </Card>
    </Container>
  );
};

export default UserProfile;
