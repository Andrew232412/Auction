import React, { useState, FormEvent, ChangeEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import styled from 'styled-components';
import { authAPI } from '../services/api';
import { setTokens } from '../services/auth';
import type { LoginRequest } from '../types';

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

const AuthContainer = styled.div`
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h2`
  margin-bottom: 20px;
  color: #2c3e50;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
`;

const FormGroup = styled.div`
  margin-bottom: 15px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 5px;
  color: #555;
  font-weight: 500;
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;

  &:focus {
    outline: none;
    border-color: #4caf50;
  }
`;

const ErrorMessage = styled.div`
  color: #f44336;
  font-size: 14px;
  margin-top: 10px;
`;

const SubmitButton = styled.button`
  background-color: #4caf50;
  color: white;
  width: 100%;
  padding: 12px;
  font-size: 16px;
  font-weight: 500;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: #45a049;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const LinkText = styled.p`
  margin-top: 15px;
  text-align: center;
  color: #666;

  a {
    color: #2196f3;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
`;

const Login: React.FC = () => {
  const [formData, setFormData] = useState<LoginRequest>({
    email: '',
    password: '',
  });
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(formData);
      const { access_token, refresh_token } = response.data;
      setTokens(access_token, refresh_token);
      navigate('/');
    } catch (err: any) {
      const data = err.response?.data;
      const status = err.response?.status;
      const fallback = status === 401
        ? 'Incorrect email or password'
        : 'Login failed. Please try again.';
      setError(data?.detail || data?.message || fallback);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <AuthContainer>
        <Title>Login</Title>
        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label>Email</Label>
            <Input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </FormGroup>
          <FormGroup>
            <Label>Password</Label>
            <Input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </FormGroup>
          {error && <ErrorMessage>{error}</ErrorMessage>}
          <SubmitButton type="submit" disabled={loading}>
            {loading ? 'Loading...' : 'Login'}
          </SubmitButton>
        </Form>
        <LinkText>
          Don't have an account? <Link to="/register">Register</Link>
        </LinkText>
      </AuthContainer>
    </Container>
  );
};

export default Login;
