const mongoose = require('mongoose');

const FileSchema = new mongoose.Schema({
  name: { type: String, required: true },
  content: { type: String, required: false, default: "" }, // Allow content to be empty by default
  lastModified: { type: Date, default: Date.now },
  createdBy: { type: String, required: true },
});

module.exports = mongoose.model('File', FileSchema);