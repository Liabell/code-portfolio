import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import RecipeDetails from './components/RecipeDetails';
import history from './components/History'

ReactDOM.render(
    <React.StrictMode>
        <BrowserRouter history={history}>
            <Routes>
                <Route path="/" element={<App />} />
                <Route path="/recipe/:recipeID" element={<RecipeDetails />} />
            </Routes>
        </BrowserRouter>
    </React.StrictMode>,
    document.getElementById('root')
);
