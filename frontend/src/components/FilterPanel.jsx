import '../styles/FilterPanel.css';

export function FilterPanel({ options, filters, onChange }) {
  if (!options) return null;

  const updateFilter = (key, value) => {
    onChange({ ...filters, [key]: value, page: 1 });
  };

  const handleMultiSelect = (key, value, checked) => {
    const currentArray = filters[key] || [];
    const updated = checked
      ? [...currentArray, value]
      : currentArray.filter((v) => v !== value);
    updateFilter(key, updated);
  };

  return (
    <div className="filter-panel">
      <h3>Filters</h3>

      {/* Region Filter */}
      <div className="filter-group">
        <label className="filter-label">Customer Region</label>
        {options.regions.map((region) => (
          <div key={region} className="checkbox-item">
            <input
              type="checkbox"
              id={`region-${region}`}
              checked={(filters.customer_region || []).includes(region)}
              onChange={(e) => handleMultiSelect('customer_region', region, e.target.checked)}
            />
            <label htmlFor={`region-${region}`}>{region}</label>
          </div>
        ))}
      </div>

      {/* Gender Filter */}
      <div className="filter-group">
        <label className="filter-label">Gender</label>
        {options.genders.map((gender) => (
          <div key={gender} className="checkbox-item">
            <input
              type="checkbox"
              id={`gender-${gender}`}
              checked={(filters.gender || []).includes(gender)}
              onChange={(e) => handleMultiSelect('gender', gender, e.target.checked)}
            />
            <label htmlFor={`gender-${gender}`}>{gender}</label>
          </div>
        ))}
      </div>

      {/* Age Range Filter */}
      <div className="filter-group">
        <label className="filter-label">Age Range</label>
        <div className="age-inputs">
          <input
            type="number"
            placeholder="Min"
            value={filters.age_min || ''}
            onChange={(e) => updateFilter('age_min', e.target.value ? parseInt(e.target.value) : undefined)}
            min={options.age_range.min}
            max={options.age_range.max}
          />
          <span>-</span>
          <input
            type="number"
            placeholder="Max"
            value={filters.age_max || ''}
            onChange={(e) => updateFilter('age_max', e.target.value ? parseInt(e.target.value) : undefined)}
            min={options.age_range.min}
            max={options.age_range.max}
          />
        </div>
      </div>

      {/* Product Category Filter */}
      <div className="filter-group">
        <label className="filter-label">Product Category</label>
        {options.product_categories.map((category) => (
          <div key={category} className="checkbox-item">
            <input
              type="checkbox"
              id={`category-${category}`}
              checked={(filters.product_category || []).includes(category)}
              onChange={(e) => handleMultiSelect('product_category', category, e.target.checked)}
            />
            <label htmlFor={`category-${category}`}>{category}</label>
          </div>
        ))}
      </div>

      {/* Payment Method Filter */}
      <div className="filter-group">
        <label className="filter-label">Payment Method</label>
        {options.payment_methods.map((method) => (
          <div key={method} className="checkbox-item">
            <input
              type="checkbox"
              id={`payment-${method}`}
              checked={(filters.payment_method || []).includes(method)}
              onChange={(e) => handleMultiSelect('payment_method', method, e.target.checked)}
            />
            <label htmlFor={`payment-${method}`}>{method}</label>
          </div>
        ))}
      </div>

      {/* Date Range Filter */}
      <div className="filter-group">
        <label className="filter-label">Date Range</label>
        <div className="date-inputs">
          <input
            type="date"
            value={filters.date_from || ''}
            onChange={(e) => updateFilter('date_from', e.target.value || undefined)}
          />
          <input
            type="date"
            value={filters.date_to || ''}
            onChange={(e) => updateFilter('date_to', e.target.value || undefined)}
          />
        </div>
      </div>
    </div>
  );
}