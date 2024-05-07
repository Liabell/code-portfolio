const mongoose = require('mongoose');

const recipeSchema = new mongoose.Schema({
  name: String,
  description: String,
  image: String,
  recipeYield: String,
  cookTime: String,
  prepTime: String,
  ingredients: [String],
});

const Recipe = mongoose.model('Recipe', recipeSchema);

module.exports = Recipe;
    