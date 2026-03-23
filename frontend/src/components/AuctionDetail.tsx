import React, { useState, useEffect, FormEvent, ChangeEvent } from 'react';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import { auctionsAPI, bidsAPI } from '../services/api';
import { isAuthenticated } from '../services/auth';
import type { Auction, Bid } from '../types';

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

const AuctionCard = styled.div`
  background: white;
  padding: 30px;
  border-radius: 8px;
  margin-top: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h1`
  color: #2c3e50;
  margin-bottom: 10px;
`;

const Status = styled.span<{ status: string }>`
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  background-color: ${props => {
    switch (props.status) {
      case 'active': return '#4CAF50';
      case 'closed': return '#9e9e9e';
      case 'cancelled': return '#f44336';
      default: return '#9e9e9e';
    }
  }};
  color: white;
`;

const Details = styled.div`
  margin-top: 20px;

  p {
    margin-bottom: 10px;
    color: #666;

    strong {
      color: #2c3e50;
    }
  }
`;

const Price = styled.div`
  font-size: 32px;
  font-weight: bold;
  color: #4caf50;
  margin: 15px 0;
`;

const BidForm = styled.div`
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-top: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const FormTitle = styled.h3`
  color: #2c3e50;
  margin-bottom: 15px;
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

const SubmitButton = styled.button`
  background-color: #4caf50;
  color: white;
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

const ErrorMessage = styled.div`
  color: #f44336;
  font-size: 14px;
  margin-top: 10px;
`;

const SuccessMessage = styled.div`
  color: #4caf50;
  font-size: 14px;
  margin-top: 10px;
`;

const InfoBox = styled.div`
  margin-top: 20px;
  padding: 15px;
  background: #f0f0f0;
  border-radius: 4px;
  color: #666;
`;

const BidHistory = styled.div`
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-top: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const BidItem = styled.div`
  padding: 15px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;

  &:last-child {
    border-bottom: none;
  }
`;

const BidAmount = styled.strong`
  font-size: 18px;
  color: #2c3e50;
`;

const BidTime = styled.p`
  font-size: 14px;
  color: #666;
  margin: 5px 0 0 0;
`;

const Loading = styled.div`
  text-align: center;
  padding: 50px;
  font-size: 18px;
  color: #666;
`;

const AuctionDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [auction, setAuction] = useState<Auction | null>(null);
  const [bids, setBids] = useState<Bid[]>([]);
  const [bidAmount, setBidAmount] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  useEffect(() => {
    if (!id) return;
    
    fetchAuction();
    fetchBids();

    const interval = setInterval(() => {
      fetchAuction();
      fetchBids();
    }, 5000);

    return () => clearInterval(interval);
  }, [id]);

  const fetchAuction = async () => {
    if (!id) return;
    
    try {
      const response = await auctionsAPI.getAuction(id);
      setAuction(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load auction');
      setLoading(false);
    }
  };

  const fetchBids = async () => {
    if (!id) return;
    
    try {
      const response = await bidsAPI.getAuctionBids(id, { page: 1, limit: 10 });
      setBids(response.data.items);
    } catch (err) {
      console.error('Failed to load bids');
    }
  };

  const handlePlaceBid = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!isAuthenticated()) {
      setError('Please login to place a bid');
      return;
    }

    if (!id) return;

    try {
      await bidsAPI.placeBid(id, { amount: parseFloat(bidAmount) });
      setSuccess('Bid placed successfully!');
      setBidAmount('');
      fetchAuction();
      fetchBids();
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to place bid');
    }
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return <Loading>Loading auction...</Loading>;
  }

  if (!auction) {
    return <Container>Auction not found</Container>;
  }

  return (
    <Container>
      <AuctionCard>
        <Title>{auction.title}</Title>
        <Status status={auction.status}>{auction.status}</Status>

        <Details>
          <p><strong>Category:</strong> {auction.category}</p>
          <p><strong>Description:</strong> {auction.description}</p>
          <p><strong>Starting Price:</strong> ${auction.starting_price}</p>
          <Price>Current Price: ${auction.current_price}</Price>
          <p><strong>Start Date:</strong> {formatDate(auction.start_date)}</p>
          <p><strong>End Date:</strong> {formatDate(auction.end_date)}</p>
        </Details>

        {auction.status === 'active' && isAuthenticated() && (
          <BidForm>
            <FormTitle>Place a Bid</FormTitle>
            <Form onSubmit={handlePlaceBid}>
              <FormGroup>
                <Label>Bid Amount (must be higher than ${auction.current_price})</Label>
                <Input
                  type="number"
                  step="0.01"
                  value={bidAmount}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => setBidAmount(e.target.value)}
                  required
                  min={auction.current_price + 0.01}
                />
              </FormGroup>
              {error && <ErrorMessage>{error}</ErrorMessage>}
              {success && <SuccessMessage>{success}</SuccessMessage>}
              <SubmitButton type="submit">Place Bid</SubmitButton>
            </Form>
          </BidForm>
        )}

        {!isAuthenticated() && auction.status === 'active' && (
          <InfoBox>Please login to place a bid</InfoBox>
        )}
      </AuctionCard>

      <BidHistory>
        <FormTitle>Bid History</FormTitle>
        {bids.length === 0 ? (
          <p>No bids yet</p>
        ) : (
          bids.map((bid) => (
            <BidItem key={bid.id}>
              <div>
                <BidAmount>${bid.amount}</BidAmount>
                <BidTime>{formatDate(bid.timestamp)}</BidTime>
              </div>
            </BidItem>
          ))
        )}
      </BidHistory>
    </Container>
  );
};

export default AuctionDetail;
