import '../styles/SortDropdown.css';

export function SortDropdown({ filters, onChange }) {
  const handleSortChange = (sortBy) => {
    onChange({
      ...filters,
      sort_by: sortBy,
      page: 1,
    });
  };

  const handleOrderChange = (order) => {
    onChange({
      ...filters,
      sort_order: order,
      page: 1,
    });
  };

  return (
    <div className="sort-dropdown">
      <select value={filters.sort_by || 'date'} onChange={(e) => handleSortChange(e.target.value)}>
        <option value="date">Sort by Date</option>
        <option value="quantity">Sort by Quantity</option>
        <option value="customer_name">Sort by Customer Name</option>
      </select>

      <select value={filters.sort_order || 'desc'} onChange={(e) => handleOrderChange(e.target.value)}>
        <option value="desc">Descending</option>
        <option value="asc">Ascending</option>
      </select>
    </div>
  );
}