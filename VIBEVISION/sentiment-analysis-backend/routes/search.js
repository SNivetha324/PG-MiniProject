const express = require('express');
const router = express.Router();
const Search = require('../models/Search'); // Import the Search model

// Route to handle search and save results to the database
router.post('/predict', async (req, res) => {
    const { text } = req.body;

    if (!text) {
        return res.status(400).json({ message: 'Text query is required' });
    }

    try {
        // Here you would use your sentiment analysis model to predict the sentiment
        // Replace this with your actual model prediction logic
        let sentiment;
        try {
            // Assume 'model' is a pre-loaded sentiment analysis model
            // sentiment = model.predict(text); // Example placeholder code
            sentiment = "positive"; // Replace this with actual prediction logic
        } catch (modelError) {
            console.error('Model prediction error:', modelError);
            return res.status(500).json({ message: 'Error predicting sentiment' });
        }

        // Save the search query and sentiment to the database
        const newSearch = new Search({ query: text, sentiment });
        await newSearch.save();

        // Send the sentiment result back to the client
        res.json({ sentiment });
    } catch (error) {
        console.error('Error saving search result:', error);
        res.status(500).json({ message: 'Error saving search result' });
    }
});

module.exports = router;
