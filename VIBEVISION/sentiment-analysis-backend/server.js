// const express = require('express');
// const mongoose = require('mongoose');
// const bodyParser = require('body-parser');
// const cors = require('cors');
// const xlsx = require('xlsx');
// const path = require('path');
// const { spawn } = require('child_process');
// const fs = require('fs');
// const spawn = require('cross-spawn');



// const app = express();

// // Middleware
// app.use(bodyParser.json());
// app.use(cors());

// // Connect to MongoDB
// mongoose.connect('mongodb://127.0.0.1:27017/mobileReviewsDB', {
//     useNewUrlParser: true,
//     useUnifiedTopology: true,
// }).then(() => {
//     console.log('Connected to MongoDB');
// }).catch((err) => console.log(err));

// // Define the schema
// const ReviewSchema = new mongoose.Schema({
//     Review: String,
//     Brand: String,
//     Feature: String,
//     Sentiment: String,
//     Score: Number,
// });

// // Create the model
// const Review = mongoose.model('Review', ReviewSchema);

// // Import and parse the Excel file
// const workbook = xlsx.readFile(path.join(__dirname, 'Amazon_Mobile_Data.csv'));
// const sheetName = workbook.SheetNames[0];
// const sheet = workbook.Sheets[sheetName];
// const xlData = xlsx.utils.sheet_to_json(sheet);

// // Python script path
// const pythonScriptPath = path.join(__dirname, 'predict_sentiment.py');

// // Process each review
// xlData.forEach((row) => {
//     const { Review: reviewText, Brand, Feature } = row;

//     // Spawn a new Python process for each prediction
//     const pythonProcess = spawn('C:/Users/pravi/AppData/Local/Programs/Python/Python312/python.exe', [pythonScriptPath, reviewText]);


//     pythonProcess.stdout.on('data', (data) => {
//         const prediction = data.toString().trim();
//         const sentimentLabel = prediction === '1' ? 'Positive' : prediction === '-1' ? 'Negative' : 'Neutral';

//         // Create a new review document
//         const review = new Review({
//             Review: reviewText,
//             Brand: Brand || 'Unknown',
//             Feature: Feature || 'General',
//             Sentiment: sentimentLabel,
//             Score: parseFloat(prediction),
//         });

//         // Save the review document
//         review.save()
//             .then(() => console.log('Review saved!'))
//             .catch((err) => console.log(err));
//     });
//     pythonProcess.stderr.on('data', (data) => {
//         console.error(`Python Error: ${data}`);
//     });
    
//     pythonProcess.on('close', (code) => {
//         console.log(`Python process exited with code ${code}`);
//     });
    
// });

// // Start the server
// const PORT = process.env.PORT || 3005;
// app.listen(PORT, () => {
//     console.log(`Server is running on port ${PORT}`);
// });


const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
const xlsx = require('xlsx');
const path = require('path');
const spawn = require('cross-spawn');  // Updated to cross-spawn

const app = express();

// Middleware
app.use(bodyParser.json());
app.use(cors());

// MongoDB connection
mongoose.connect('mongodb://127.0.0.1:27017/mobileReviewsDB', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
}).then(() => {
    console.log('Connected to MongoDB');
}).catch((err) => console.log(err));

// Review schema and model
const ReviewSchema = new mongoose.Schema({
    Review: String,
    Brand: String,
    Feature: String,
    Sentiment: String,
    Score: Number,
});
const Review = mongoose.model('Review', ReviewSchema);

// Import and parse Excel file
const workbook = xlsx.readFile(path.join(__dirname, 'Amazon_Mobile_Data.csv'));
const sheetName = workbook.SheetNames[0];
const sheet = workbook.Sheets[sheetName];
const xlData = xlsx.utils.sheet_to_json(sheet);

// Python script path
const pythonScriptPath = path.join(__dirname, 'predict_sentiment.py');

// Process each review
xlData.forEach((row) => {
    const { Review: reviewText, Brand, Feature } = row;

    // Spawn a new Python process for each prediction
    const pythonProcess = spawn('C:/Users/pravi/AppData/Local/Programs/Python/Python312/python.exe', [pythonScriptPath, reviewText]);

    pythonProcess.stdout.on('data', (data) => {
        const prediction = data.toString().trim();
        const sentimentLabel = prediction === '1' ? 'Positive' : prediction === '-1' ? 'Negative' : 'Neutral';

        const review = new Review({
            Review: reviewText,
            Brand: Brand || 'Unknown',
            Feature: Feature || 'General',
            Sentiment: sentimentLabel,
            Score: parseFloat(prediction),
        });

        review.save()
            .then(() => console.log('Review saved!'))
            .catch((err) => console.log(err));
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
    });
});

// Start the server
const PORT = process.env.PORT || 3005;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
