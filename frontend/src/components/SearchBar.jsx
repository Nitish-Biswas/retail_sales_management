import { useState, useEffect, useRef } from 'react';
import '../styles/SearchBar.css';

export function SearchBar({ value, onChange }) {
  const [localValue, setLocalValue] = useState(value || '');
  const debounceTimer = useRef(null);

  const handleInputChange = (e) => {
    const newValue = e.target.value;
    setLocalValue(newValue);

  
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }

    
    debounceTimer.current = setTimeout(() => {
      onChange(newValue);
    }, 1200); 
  };

  // Handle Enter key 
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
      
      onChange(localValue);
      
      e.preventDefault(); 
    }
  };

  // Update local value when prop changes
  useEffect(() => {
    setLocalValue(value || '');
  }, [value]);

  // Cleanup timer on unmount
  useEffect(() => {
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, []);

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search by Customer Name or Phone Number (press enter for instant search) "
        value={localValue}
        onChange={handleInputChange}
        onKeyPress={handleKeyPress}
        className="search-input"
      />
      <svg
        className="search-icon"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
      >
        <circle cx="11" cy="11" r="8"></circle>
        <path d="m21 21-4.35-4.35"></path>
      </svg>
    </div>
  );
}
