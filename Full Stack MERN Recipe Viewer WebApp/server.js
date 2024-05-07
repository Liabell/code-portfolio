const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const fs = require('fs');
const Recipe = require('./models/Recipe');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5001;
const MONGO_URI = 'mongodb://localhost:27017/recipes-3'; // MongoDB URI (change to recipes-3 eventually)

app.use(bodyParser.json());
app.use(cors()); // cors middleware to fix errors

app.use(express.static(path.join(__dirname, '../frontend')));

// Database Connection
mongoose.connect(MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

// Route to populate the database with recipes from recipes.json
app.post('/api/populate', async (req, res) => {
  try {
    const recipesData = fs.readFileSync('recipes.json', 'utf8');
    const recipes = JSON.parse(recipesData);

    // Slice the recipes array to include only the first 782 recipes, this is required by fitz
    const slicedRecipes = recipes.slice(0, 782);

    await Recipe.insertMany(slicedRecipes);
    res.status(201).json({ message: 'Database populated successfully!' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Route to search for recipes in the MongoDB database based on the generated query
app.get('/api/recipes-3/search', async (req, res) => {
  try {
    const query = req.query.q;
    const recipes = await Recipe.find({
      $or: [
        { name: { $regex: query, $options: 'i' } },
        { description: { $regex: query, $options: 'i' } },
        { ingredients: { $regex: query, $options: 'i' } },
      ],
    }).select('name cookTime prepTime ingredients recipeYield image');
    res.json({ success: true, recipes });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, error: 'Internal Server Error' });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
