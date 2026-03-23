import React from 'react';
import styled from 'styled-components';

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

const InfoText = styled.p`
  color: #666;
  font-size: 16px;
`;

const UserProfile: React.FC = () => {
  return (
    <Container>
      <Card>
        <Title>User Profile</Title>
        <InfoText>Profile management coming soon...</InfoText>
      </Card>
    </Container>
  );
};

export default UserProfile;
