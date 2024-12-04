import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os
import pandas as pd
import csv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the RNN model
MODEL_PATH = os.path.join(os.getcwd(), 'mymodel.keras')  # Path to the saved model
model = keras.models.load_model(MODEL_PATH)  # Loading the model

# Load the tokenizer used during training
TOKENIZER_PATH = os.path.join(os.getcwd(), 'tokenizerfile.pickle')  # Path to the tokenizer
with open(TOKENIZER_PATH, 'rb') as handle:
    tokenizer = pickle.load(handle)

# Maximum length of the input sequence (same as used during training)
max_length = 100

# Load Excel data into a dictionary
excel_path = 'F:/miniprojectVV/VIBEVISION/vibevision/src/Asin.xlsx'  # Adjust path as necessary
excel_data = pd.read_excel(excel_path)
asin_dict = {str(product_name).strip().lower(): str(asin).strip() for product_name, asin in zip(excel_data['Product Name'], excel_data['ASIN'])}

# Helper function to preprocess text
def preprocess_text(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_length, padding='post', truncating='post')
    return padded_sequence

# Fetch reviews using the ASIN
def fetch_reviews_for_asin(api_key, asin):
    url = "https://real-time-amazon-data.p.rapidapi.com/product-reviews"
    querystring = {
        "asin": asin,
        "country": "US",
        "sort_by": "TOP_REVIEWS",
        "star_rating": "ALL",
        "verified_purchases_only": "false",
        "images_or_videos_only": "false",
        "current_format_only": "false",
        "page": "1"
    }
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
    }

    try:
        print(f"Fetching reviews for ASIN: {asin}")  # Debug: Print ASIN
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return None

        response_json = response.json()
        print(f"API Response: {response_json}")  # Debug: Print the full API response

        # Extract relevant information
        total_reviews = response_json.get('data', {}).get('total_reviews', 'N/A')
        total_ratings = response_json.get('data', {}).get('total_ratings', 'N/A')
        country = response_json.get('data', {}).get('country', 'N/A')
        reviews = response_json.get('data', {}).get('reviews', [])

        return reviews, total_reviews, total_ratings, country

    except Exception as e:
        print(f"Error fetching reviews: {e}")  # Print error if fetching fails
        return None, None, None, None

def save_reviews_to_csv(product_name, reviews, total_reviews, total_ratings, country):
    # Create or append to a CSV file
    csv_filename = f'{product_name}_reviews.csv'
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the headers including additional fields
        writer.writerow(['Total Reviews', 'Total Ratings', 'Country', 'Review ID', 'Review Title', 'Review Comment', 'Rating', 'Review Link', 'Review Author', 'Review Author Avatar', 'Review Date', 'Verified Purchase', 'Helpful Vote Statement', 'Reviewed Product ASIN'])
        
        # Write review details and the additional fields
        for review in reviews:
            writer.writerow([
                total_reviews,
                total_ratings,
                country,
                review.get('review_id', ''),
                review.get('review_title', ''),
                review.get('review_comment', ''),
                review.get('review_star_rating', ''),
                review.get('review_link', ''),
                review.get('review_author', ''),
                review.get('review_author_avatar', ''),
                review.get('review_date', ''),
                review.get('is_verified_purchase', ''),
                review.get('helpful_vote_statement', ''),
                review.get('reviewed_product_asin', '')
            ])
    print(f"Reviews saved to {csv_filename}")

# Updated function to predict sentiment with improved accuracy
def predict_sentiment(review_text):
    preprocessed_review = preprocess_text(review_text)
    sentiment = model.predict(preprocessed_review)
    
    # Using multiple thresholds for sentiment classification
    if sentiment[0][0] >= 0.6:
        sentiment_label = 'positive'
    elif sentiment[0][0] <= 0.4:
        sentiment_label = 'negative'
    else:
        sentiment_label = 'neutral'
    
    return sentiment_label

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("Received data:", data)  # Debugging

        if data is None:
            return jsonify({"error": "No data received, please send the product name in the request body as JSON."}), 400

        product_name = data.get("product_name") or data.get("brand_name")  # Check both keys

        if not product_name:
            return jsonify({"error": "Product name is required in the request body."}), 400

        product_name = product_name.strip().lower()
        asin = asin_dict.get(product_name)

        if not asin:
            return jsonify({"error": f"No ASIN found for product: {product_name}"}), 404

        api_key = "86843c83c3msh6c1c3425a51a554p106959jsn66c8dd77c252"  # Replace with your real API key

        # Fetch reviews for the ASIN and extract total reviews, total ratings, and country
        reviews, total_reviews, total_ratings, country = fetch_reviews_for_asin(api_key, asin)
        if reviews is None:
            return jsonify({"error": "Failed to fetch reviews."}), 500

        print("Fetched reviews:", reviews)  # Print the reviews to the terminal

        # Save the reviews to a CSV file with additional details
        save_reviews_to_csv(product_name, reviews, total_reviews, total_ratings, country)

        # Preprocess reviews and predict sentiment
        predictions = []
        for review in reviews:
            review_comment = review.get('review_comment', '')
            review_star_rating = review.get('review_star_rating', None)  # Get the star rating
            if review_comment:  # Skip if review comment is empty
                sentiment_label = predict_sentiment(review_comment)
                predictions.append({
                    'review': review_comment,
                    'sentiment': sentiment_label,
                    'review_star_rating': review_star_rating  # Include star rating in the response
                })

        return jsonify(predictions)

    except Exception as e:
        print(f"An error occurred: {e}")  # Print any unexpected errors
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)