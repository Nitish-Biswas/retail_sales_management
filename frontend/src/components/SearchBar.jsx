import '../styles/SearchBar.css';

export function SearchBar({ value, onChange }) {
  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search by Customer Name or Phone Number"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="search-input"
      />
      <svg className="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <circle cx="11" cy="11" r="8" />
        <path d="m21 21-4.35-4.35" />
      </svg>
    </div>
  );
}