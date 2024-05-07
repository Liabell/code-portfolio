import React, { useState } from 'react';
import silhouetteImage from '../components/silhouette_image.jpg'; // Import the silhouette image

const formatTime = (isoDuration) => {
    const matches = isoDuration.match(/PT(\d+)H?(\d+)M?/);
    if (!matches) return 'Time Invalid/Not Found';

    const hours = parseInt(matches[1], 10) || 0;
    const minutes = parseInt(matches[2], 10) || 0;
    const formattedHours = String(hours).padStart(2, '0');
    const formattedMinutes = String(minutes).padStart(2, '0');
    return `${formattedHours}:${formattedMinutes}`;
};

const RecipeCard = ({ recipe }) => {
    const [showIngredients, setShowIngredients] = useState(false);
    const [firstImageLoaded, setFirstImageLoaded] = useState(true);

    const handleFirstImageError = () => {
        setFirstImageLoaded(false);
    };

    const toggleIngredients = () => {
        setShowIngredients(!showIngredients);
    };

    return (
        <div className={`RecipeCard ${showIngredients ? 'showIngredients' : ''}`}>
            <img src={recipe.image} alt="" onError={handleFirstImageError}
                 style={{display: firstImageLoaded ? 'block' : 'none'}}/>
            {!firstImageLoaded && <img src={silhouetteImage} alt="Silhouette Image Broke"/>} {/* loads if recipe.image fails to display */}
            <h3>{recipe.name}</h3>
            <p><strong>Cook Time:</strong> {formatTime(recipe.cookTime)}</p>
            <p><strong>Prep Time:</strong> {formatTime(recipe.prepTime)}</p>
            <p><strong>Yield:</strong> {recipe.recipeYield}</p>
            <button onClick={toggleIngredients}>View Recipe</button>
            {showIngredients && (
                <div className="ingredients">
                    <h4>Ingredients</h4>
                    <ul>
                        {recipe.ingredients.map((ingredient, index) => (
                            <li key={index}>{ingredient}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default RecipeCard;
