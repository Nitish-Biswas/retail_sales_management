import '../styles/Pagination.css';

export function Pagination({ data, filters, onChange }) {
  if (!data) return null;

  const handlePrevious = () => {
    if (data.has_prev) {
      onChange({ ...filters, page: filters.page - 1 });
    }
  };

  const handleNext = () => {
    if (data.has_next) {
      onChange({ ...filters, page: filters.page + 1 });
    }
  };

  return (
    <div className="pagination">
      <button onClick={handlePrevious} disabled={!data.has_prev} className="pagination-btn">
        ← Previous
      </button>

      <div className="pagination-info">
        Page {data.current_page} of {data.total_pages} | Total: {data.total_records} records
      </div>

      <button onClick={handleNext} disabled={!data.has_next} className="pagination-btn">
        Next →
      </button>
    </div>
  );
}