import React from 'react';
import RecipeCard from './RecipeCard';

const SearchResults = ({ results }) => {
  // Check if results array exists and is not empty
  if (!results || results.length === 0) {
    return <div>No results found.</div>;
  } else {
    return ( // Passes data to Recipe Card
        <div className="SearchResults">
          {results.map((recipe, index) => (
              <RecipeCard key={index} recipe={recipe} />
          ))}
        </div>
    );
  }
};

export default SearchResults;
