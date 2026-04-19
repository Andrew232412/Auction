import React, { useState, useEffect, ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { auctionsAPI } from '../services/api';
import type { Auction } from '../types';

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

const Title = styled.h1`
  color: #2c3e50;
  margin-bottom: 20px;
`;

const Filters = styled.div`
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const FiltersRow = styled.div`
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
`;

const FilterGroup = styled.div`
  flex: 1;
  min-width: 200px;
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

const Select = styled.select`
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

const AuctionGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
`;

const AuctionCard = styled.div`
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
`;

const AuctionTitle = styled.h3`
  color: #2c3e50;
  margin-bottom: 10px;
`;

const AuctionCategory = styled.p`
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
`;

const AuctionDescription = styled.p`
  color: #666;
  margin-bottom: 8px;
`;

const AuctionPrice = styled.div`
  font-size: 24px;
  font-weight: bold;
  color: #4caf50;
  margin: 10px 0;
`;

const StatusBadge = styled.span<{ status: string }>`
  display: inline-block;
  margin-top: 10px;
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

const EndsDate = styled.p`
  color: #666;
  font-size: 14px;
  margin: 4px 0 0 0;
`;

const Pagination = styled.div`
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 30px;
`;

const PageButton = styled.button`
  padding: 8px 16px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  &:hover:not(:disabled) {
    background-color: #34495e;
  }
`;

const PageInfo = styled.span`
  display: flex;
  align-items: center;
  color: #666;
`;

const Loading = styled.div`
  text-align: center;
  padding: 50px;
  font-size: 18px;
  color: #666;
`;

const ErrorMessage = styled.div`
  color: #f44336;
  font-size: 14px;
  margin: 10px 0;
`;

const EmptyMessage = styled.p`
  text-align: center;
  margin-top: 50px;
  color: #666;
`;

interface Filters {
  category: string;
  status: string;
  sort_by: string;
  page: number;
  limit: number;
}

const AuctionList: React.FC = () => {
  const [auctions, setAuctions] = useState<Auction[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [initialized, setInitialized] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [categoryInput, setCategoryInput] = useState<string>('');
  const [filters, setFilters] = useState<Filters>({
    category: '',
    status: '',
    sort_by: 'created_at',
    page: 1,
    limit: 12,
  });
  const [pagination, setPagination] = useState({
    total: 0,
    pages: 0,
  });
  const navigate = useNavigate();

  // Debounce category input so typing does not re-fetch on every keystroke.
  useEffect(() => {
    const handle = setTimeout(() => {
      setFilters((prev) =>
        prev.category === categoryInput ? prev : { ...prev, category: categoryInput, page: 1 }
      );
    }, 400);
    return () => clearTimeout(handle);
  }, [categoryInput]);

  useEffect(() => {
    fetchAuctions();
  }, [filters]);

  const fetchAuctions = async () => {
    setLoading(true);
    try {
      const params: Record<string, any> = {};
      if (filters.category) params.category = filters.category;
      if (filters.status) params.status = filters.status;
      params.sort_by = filters.sort_by;
      params.page = filters.page;
      params.limit = filters.limit;

      const response = await auctionsAPI.getAuctions(params);
      setAuctions(response.data.items);
      setPagination({
        total: response.data.total,
        pages: response.data.pages,
      });
    } catch (err) {
      setError('Failed to load auctions');
    } finally {
      setLoading(false);
      setInitialized(true);
    }
  };

  const handleSelectChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value,
      page: 1,
    });
  };

  const handleCategoryChange = (e: ChangeEvent<HTMLInputElement>) => {
    setCategoryInput(e.target.value);
  };

  const handlePageChange = (newPage: number) => {
    setFilters({
      ...filters,
      page: newPage,
    });
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString();
  };

  if (!initialized && loading) {
    return <Loading>Loading auctions...</Loading>;
  }

  return (
    <Container>
      <Title>Auctions</Title>

      <Filters>
        <FiltersRow>
          <FilterGroup>
            <Label>Category</Label>
            <Input
              type="text"
              name="category"
              placeholder="Filter by category"
              value={categoryInput}
              onChange={handleCategoryChange}
            />
          </FilterGroup>
          <FilterGroup>
            <Label>Status</Label>
            <Select name="status" value={filters.status} onChange={handleSelectChange}>
              <option value="">All</option>
              <option value="active">Active</option>
              <option value="closed">Closed</option>
              <option value="cancelled">Cancelled</option>
            </Select>
          </FilterGroup>
          <FilterGroup>
            <Label>Sort By</Label>
            <Select name="sort_by" value={filters.sort_by} onChange={handleSelectChange}>
              <option value="created_at">Newest</option>
              <option value="current_price">Price</option>
              <option value="end_date">Ending Soon</option>
              <option value="title">Title</option>
            </Select>
          </FilterGroup>
        </FiltersRow>
      </Filters>

      {error && <ErrorMessage>{error}</ErrorMessage>}

      <AuctionGrid>
        {auctions.map((auction) => (
          <AuctionCard
            key={auction.id}
            onClick={() => navigate(`/auctions/${auction.id}`)}
          >
            <AuctionTitle>{auction.title}</AuctionTitle>
            <AuctionCategory>{auction.category}</AuctionCategory>
            <AuctionDescription>
              {auction.description.substring(0, 100)}...
            </AuctionDescription>
            <AuctionPrice>${auction.current_price}</AuctionPrice>
            <EndsDate>Ends: {formatDate(auction.end_date)}</EndsDate>
            <StatusBadge status={auction.status}>
              {auction.status}
            </StatusBadge>
          </AuctionCard>
        ))}
      </AuctionGrid>

      {auctions.length === 0 && !loading && (
        <EmptyMessage>No auctions found</EmptyMessage>
      )}

      {pagination.pages > 1 && (
        <Pagination>
          <PageButton
            onClick={() => handlePageChange(filters.page - 1)}
            disabled={filters.page === 1}
          >
            Previous
          </PageButton>
          <PageInfo>
            Page {filters.page} of {pagination.pages}
          </PageInfo>
          <PageButton
            onClick={() => handlePageChange(filters.page + 1)}
            disabled={filters.page === pagination.pages}
          >
            Next
          </PageButton>
        </Pagination>
      )}
    </Container>
  );
};

export default AuctionList;
