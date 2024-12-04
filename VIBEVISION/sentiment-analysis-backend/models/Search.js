const mongoose = require('mongoose');

// Define the Search schema
const SearchSchema = new mongoose.Schema({
    query: {
        type: String,
        required: true, // Ensure that query is required
    },
    sentiment: {
        type: String,
        required: true, // Ensure that sentiment result is required
    },
    createdAt: {
        type: Date,
        default: Date.now, // Automatically set the creation date
    },
});

module.exports = mongoose.model('Search', SearchSchema);
