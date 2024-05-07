import React from 'react';
import { useParams } from 'react-router-dom';


const RecipeDetails = () => {
    const {recipeID} = useParams();
    console.log(recipeID);
    console.log('im here!')
    return (
        <div>
            <h4>Ingredients</h4>
            {/*<ul>*/}
            {/*    {recipeID.ingredients.map((ingredient, index) => (*/}
            {/*        <li key={index}>{ingredient}</li>*/}
            {/*    ))}*/}
            {/*</ul>*/}
        </div>
    );
}


export default RecipeDetails;
