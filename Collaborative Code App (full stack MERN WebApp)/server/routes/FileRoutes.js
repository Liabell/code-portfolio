const express = require('express');
const router = express.Router();
const File = require('../models/File');

// Route to retrieve all files
router.get('/', async (req, res) => {
  try {
    const files = await File.find();
    res.status(200).json(files);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Route to retrieve a specific file by ID
router.get('/:id', async (req, res) => {
  try {
    const file = await File.findById(req.params.id);
    if (!file) return res.status(404).json({ message: 'File not found' });
    res.status(200).json(file);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Route to create a new file
router.post('/', async (req, res) => {
  try {
    const { name, content, createdBy } = req.body;
    const newFile = new File({ name, content, createdBy });
    const savedFile = await newFile.save();
    res.status(201).json(savedFile);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Route to update a file
router.put('/:id', async (req, res) => {
  try {
    const { name, content } = req.body;
    const updatedFile = await File.findByIdAndUpdate(
      req.params.id,
      { name, content, lastModified: Date.now() },
      { new: true }
    );
    if (!updatedFile) return res.status(404).json({ message: 'File not found' });
    res.status(200).json(updatedFile);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Route to delete a file
router.delete('/:id', async (req, res) => {
  try {
    const deletedFile = await File.findByIdAndDelete(req.params.id);
    if (!deletedFile) return res.status(404).json({ message: 'File not found' });
    res.status(200).json({ message: 'File deleted successfully' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;