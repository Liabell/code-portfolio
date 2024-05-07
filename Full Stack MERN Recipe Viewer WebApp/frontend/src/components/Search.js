import React, { useState } from 'react';
import axios from 'axios';

const Search = ({ onSearch, show }) => {
  const [query, setQuery] = useState('');

  const handleSearch = async () => { // Recieves response for search query
    try {
      const response = await axios.get(`http://localhost:5001/api/recipes-3/search?q=${query}`);
      onSearch(query);
    } catch (error) {
      console.error('Error searching recipes:', error);
    }
  };

  const handleKeyPress = async (e) => {
    if (e.key === 'Enter') {
      await handleSearch();
    }
  };

  return (
    <div className="Search">
      {show && (
        <>
          <input
            type="text"
            placeholder="Search Recipes"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button className="searchButton" onClick={handleSearch}>Search</button>
        </>
      )}
    </div>
  );
};

export default Search;
