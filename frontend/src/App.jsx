import { useEffect, useState } from 'react';
import { SearchBar } from './components/SearchBar';
import { FilterPanel } from './components/FilterPanel';
import { SortDropdown } from './components/SortDropdown';
import { TransactionTable } from './components/TransactionTable';
import { Pagination } from './components/Pagination';
import { transactionService } from './services/api';
import './styles/App.css';

function App() {
  const [data, setData] = useState(null);
  const [filterOptions, setFilterOptions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [filters, setFilters] = useState({
    page: 1,
    page_size: 10,
  });
  
  // Fetch filter options on mount
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const options = await transactionService.getFilterOptions();
        setFilterOptions(options);
      } catch (err) {
        console.error('Failed to load filter options', err);
      }
    };

    fetchOptions();
  }, []);

  // Fetch transactions whenever filters change
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await transactionService.getTransactions(filters);
        setData(result);
      } catch (err) {
        setError('Failed to load transactions');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [filters]);

  

  const handleSearchChange = (search) => {
    setFilters({ ...filters, search, page: 1 });
  };

  const handleFiltersChange = (newFilters) => {
    setFilters(newFilters);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Sales Management System</h1>
        <p>TruEstate Retail Analytics Dashboard</p>
      </header>

      <div className="app-container">
        <aside className="sidebar">
          <FilterPanel 
            options={filterOptions}
            filters={filters}
            onChange={handleFiltersChange}
          />
        </aside>

        <main className="main-content">
          <div className="controls">
            <SearchBar value={filters.search || ''} onChange={handleSearchChange} />
            <SortDropdown filters={filters} onChange={handleFiltersChange} />
          </div>

          {error && <div className="error-message">{error}</div>}

          <TransactionTable transactions={data?.data || []} loading={loading} />

          <Pagination data={data} filters={filters} onChange={handleFiltersChange} />
        </main>
      </div>
    </div>
  );
}

export default App;