import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Search from './Search';
import SearchResults from './SearchResults';
import './App.css';
import BannerImage from '../components/banner.jpg';

const App = () => {
  const [isDatabasePopulated, setDatabasePopulated] = useState(false);
  const [searchResults, setSearchResults] = useState([]);
  const [showSearch, setShowSearch] = useState(false); // State to control visibility of search

  useEffect(() => {
    // Show search bar and button when the component mounts
    setShowSearch(true);
  }, []); // Empty dependency array ensures this effect runs only once

  const handlePopulateDatabase = async () => {
    try {
      const response = await axios.post('http://localhost:5001/api/populate');
      console.log(response.data); // Log the response for confirmation
      setDatabasePopulated(true);
      setShowSearch(true); // Show search after DB is populated
    } catch (error) {
      console.error('Error populating database:', error);
    }
  };

  const handleSearch = async (query) => { // Sends search query to Database
    try {
      const response = await axios.get(`http://localhost:5001/api/recipes-3/search?q=${query}`);
      setSearchResults(response.data.recipes);
    } catch (error) {
      console.error('Error searching recipes:', error);
    }
  };

  return (
    <div className="App">
      {!isDatabasePopulated && <button class="dbButton"onClick={handlePopulateDatabase}>Populate DB</button>}
      <br></br>
      <img className="banner" src={BannerImage} alt="" />
      {showSearch && <Search onSearch={handleSearch} show={showSearch} />} {/* Show search when showSearch is true */}
      {isDatabasePopulated && <SearchResults results={searchResults} />} {/* Show search results if DB is populated and results are available */}
      <p>{isDatabasePopulated && '782 recipe(s) successfully added to the database'}</p>
    </div>
  );
};

export default App;
