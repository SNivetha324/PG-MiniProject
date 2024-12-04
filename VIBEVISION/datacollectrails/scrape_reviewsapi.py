#reviews
# import requests
# import http.client
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from tensorflow import keras
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import pickle
# import os
# from urllib.parse import quote
# import pandas as pd

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load the RNN model
# MODEL_PATH = os.path.join(os.getcwd(), 'mymodel.keras')  # Path to the saved model
# model = keras.models.load_model(MODEL_PATH)  # Loading the model

# # Load the tokenizer used during training
# TOKENIZER_PATH = os.path.join(os.getcwd(), 'tokenizerfile.pickle')  # Path to the tokenizer
# with open(TOKENIZER_PATH, 'rb') as handle:
#     tokenizer = pickle.load(handle)

# # Maximum length of the input sequence (same as used during training)
# max_length = 100

# # Load Excel data into a dictionary
# excel_path = 'D:/SEM3/MINIPROJECT/Asin.xlsx'  # Adjust path as necessary
# excel_data = pd.read_excel(excel_path)
# asin_dict = dict(zip(excel_data['Product Name'], excel_data['ASIN']))  # Assuming columns are named 'Product Name' and 'ASIN'

# # Helper function to preprocess text
# def preprocess_text(text):
#     sequence = tokenizer.texts_to_sequences([text])
#     padded_sequence = pad_sequences(sequence, maxlen=max_length, padding='post', truncating='post')
#     return padded_sequence

# # Fetch reviews using the ASIN
# def fetch_reviews_for_asin(api_key, asin):
#     url = "https://real-time-amazon-data.p.rapidapi.com/product-reviews"
#     querystring = {
#         "asin": asin,
#         "country": "US",
#         "sort_by": "TOP_REVIEWS",
#         "star_rating": "ALL",
#         "verified_purchases_only": "false",
#         "images_or_videos_only": "false",
#         "current_format_only": "false",
#         "page": "1"
#     }
#     headers = {
#         "x-rapidapi-key": api_key,
#         "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
#     }

#     try:
#         print(f"Fetching reviews for ASIN: {asin}")  # Debug: Print ASIN
#         response = requests.get(url, headers=headers, params=querystring)
        
#         # Log the full API request details
#         print(f"Request URL: {response.url}")  # Print the full URL with parameters
#         print(f"Status Code: {response.status_code}")  # Print status code
        
#         if response.status_code != 200:
#             print(f"Error: Received status code {response.status_code}")
#             print(f"Response Text: {response.text}")  # Log the full response text for debugging
#             return []

#         response_json = response.json()
#         print(f"API Response: {response_json}")  # Debug: Print the full API response

#         reviews = response_json.get('reviews', [])

#         # Extract and return the review texts
#         return [review.get('review_text', '') for review in reviews]

#     except Exception as e:
#         print(f"Error fetching reviews: {e}")  # Print error if fetching fails
#         return []
    
# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Print the raw data to debug the input
#         data = request.json
#         print("Received data:", data)  # Debugging

#         # Ensure data is not None
#         if data is None:
#             return jsonify({"error": "No data received, please send the product name in the request body as JSON."}), 400

#         # Check for product_name or brand_name key and adjust accordingly
#         product_name = data.get("product_name") or data.get("brand_name")  # Check both keys

#         # Ensure the client provides the product name
#         if not product_name:
#             return jsonify({"error": "Product name is required in the request body."}), 400

#         # Retrieve the ASIN for the product name from the dictionary
#         asin = asin_dict.get(product_name)

#         if not asin:
#             return jsonify({"error": f"No ASIN found for product: {product_name}"}), 404

#         api_key = "5ba1089567msh3547f02f2fea32ap18f045jsn7eebdaa0d611"  # Replace with your real API key

#         # Fetch reviews for the ASIN
#         reviews = fetch_reviews_for_asin(api_key, asin)
#         print("Fetched reviews:", reviews)  # Print the reviews to the terminal

#         # Preprocess reviews and predict sentiment
#         predictions = []
#         for review in reviews:
#             preprocessed_review = preprocess_text(review)
#             sentiment = model.predict(preprocessed_review)
#             sentiment_label = 'positive' if sentiment[0][0] >= 0.5 else 'negative'
#             predictions.append({
#                 'review': review,
#                 'sentiment': sentiment_label
#             })

#         return jsonify(predictions)

#     except Exception as e:
#         print(f"An error occurred: {e}")  # Print any unexpected errors
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)



#csv

# import requests
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from tensorflow import keras
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import pickle
# import os
# import pandas as pd
# import csv  # Import CSV module

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load the RNN model
# MODEL_PATH = os.path.join(os.getcwd(), 'mymodel.keras')  # Path to the saved model
# model = keras.models.load_model(MODEL_PATH)  # Loading the model

# # Load the tokenizer used during training
# TOKENIZER_PATH = os.path.join(os.getcwd(), 'tokenizerfile.pickle')  # Path to the tokenizer
# with open(TOKENIZER_PATH, 'rb') as handle:
#     tokenizer = pickle.load(handle)

# # Maximum length of the input sequence (same as used during training)
# max_length = 100

# # Load Excel data into a dictionary
# excel_path = 'D:/SEM3/MINIPROJECT/Asin.xlsx'  # Adjust path as necessary
# excel_data = pd.read_excel(excel_path)
# asin_dict = dict(zip(excel_data['Product Name'], excel_data['ASIN']))  # Assuming columns are named 'Product Name' and 'ASIN'

# # Helper function to preprocess text
# def preprocess_text(text):
#     sequence = tokenizer.texts_to_sequences([text])
#     padded_sequence = pad_sequences(sequence, maxlen=max_length, padding='post', truncating='post')
#     return padded_sequence

# # Fetch reviews using the ASIN
# def fetch_reviews_for_asin(api_key, asin):
#     url = "https://real-time-amazon-data.p.rapidapi.com/product-reviews"
#     querystring = {
#         "asin": asin,
#         "country": "US",
#         "sort_by": "TOP_REVIEWS",
#         "star_rating": "ALL",
#         "verified_purchases_only": "false",
#         "images_or_videos_only": "false",
#         "current_format_only": "false",
#         "page": "1"
#     }
#     headers = {
#         "x-rapidapi-key": api_key,
#         "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
#     }

#     try:
#         print(f"Fetching reviews for ASIN: {asin}")  # Debug: Print ASIN
#         response = requests.get(url, headers=headers, params=querystring)
        
#         # Log the full API request details
#         print(f"Request URL: {response.url}")  # Print the full URL with parameters
#         print(f"Status Code: {response.status_code}")  # Print status code
        
#         if response.status_code != 200:
#             print(f"Error: Received status code {response.status_code}")
#             print(f"Response Text: {response.text}")  # Log the full response text for debugging
#             return None

#         response_json = response.json()
#         print(f"API Response: {response_json}")  # Debug: Print the full API response

#         reviews = response_json.get('data', {}).get('reviews', [])
#         return reviews

#     except Exception as e:
#         print(f"Error fetching reviews: {e}")  # Print error if fetching fails
#         return None
    
# def save_reviews_to_csv(product_name, reviews):
#     # Create or append to a CSV file
#     csv_filename = f'{product_name}_reviews.csv'
#     with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         # Write the headers
#         writer.writerow(['Review ID', 'Review Title', 'Review Comment', 'Rating', 'Review Link', 'Review Author', 'Review Author Avatar', 'Review Date', 'Verified Purchase', 'Helpful Vote Statement', 'Reviewed Product ASIN'])
        
#         # Write review details
#         for review in reviews:
#             writer.writerow([
#                 review.get('review_id', ''),
#                 review.get('review_title', ''),
#                 review.get('review_comment', ''),
#                 review.get('review_star_rating', ''),
#                 review.get('review_link', ''),
#                 review.get('review_author', ''),
#                 review.get('review_author_avatar', ''),
#                 review.get('review_date', ''),
#                 review.get('is_verified_purchase', ''),
#                 review.get('helpful_vote_statement', ''),
#                 review.get('reviewed_product_asin', '')
#             ])
#     print(f"Reviews saved to {csv_filename}")

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Print the raw data to debug the input
#         data = request.json
#         print("Received data:", data)  # Debugging

#         # Ensure data is not None
#         if data is None:
#             return jsonify({"error": "No data received, please send the product name in the request body as JSON."}), 400

#         # Check for product_name or brand_name key and adjust accordingly
#         product_name = data.get("product_name") or data.get("brand_name")  # Check both keys

#         # Ensure the client provides the product name
#         if not product_name:
#             return jsonify({"error": "Product name is required in the request body."}), 400

#         # Retrieve the ASIN for the product name from the dictionary
#         asin = asin_dict.get(product_name)

#         if not asin:
#             return jsonify({"error": f"No ASIN found for product: {product_name}"}), 404

#         api_key = "5ba1089567msh3547f02f2fea32ap18f045jsn7eebdaa0d611"  # Replace with your real API key

#         # Fetch reviews for the ASIN
#         reviews = fetch_reviews_for_asin(api_key, asin)
#         if reviews is None:
#             return jsonify({"error": "Failed to fetch reviews."}), 500

#         print("Fetched reviews:", reviews)  # Print the reviews to the terminal

#         # Save the reviews to a CSV file
#         save_reviews_to_csv(product_name, reviews)

#         # Preprocess reviews and predict sentiment
#         predictions = []
#         for review in reviews:
#             preprocessed_review = preprocess_text(review.get('review_comment', ''))
#             sentiment = model.predict(preprocessed_review)
#             sentiment_label = 'positive' if sentiment[0][0] >= 0.5 else 'negative'
#             predictions.append({
#                 'review': review.get('review_comment', ''),
#                 'sentiment': sentiment_label
#             })

#         return jsonify(predictions)

#     except Exception as e:
#         print(f"An error occurred: {e}")  # Print any unexpected errors
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)



# import requests
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import pickle
# import os
# import pandas as pd
# import csv

# import sklearn
# print(sklearn.__version__)


# # Load the uploaded files
# model_path = 'D:/SEM3/MINIPROJECT/14-09-2024/datacollectrails/tokenizerfile.pickle'  # Your uploaded trained model
# vectorizer_path = 'D:/SEM3/MINIPROJECT/14-09-2024/datacollectrails/tfidf_vectorizer.pkl'  # Your uploaded vectorizer

# # Load the model and vectorizer
# with open(model_path, 'rb') as model_file:
#     trained_model = pickle.load(model_file)

# with open(vectorizer_path, 'rb') as vectorizer_file:
#     vectorizer = pickle.load(vectorizer_file)

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Maximum length of the input sequence (for RNN if used)
# max_length = 100

# # Load Excel data into a dictionary
# excel_path = 'D:/SEM3/MINIPROJECT/Asin.xlsx'  # Adjust path as necessary
# excel_data = pd.read_excel(excel_path)
# asin_dict = dict(zip(excel_data['Product Name'], excel_data['ASIN']))  # Assuming columns are named 'Product Name' and 'ASIN'

# # Helper function to preprocess text
# def preprocess_text(text):
#     # Vectorizing using the loaded vectorizer (Assuming TF-IDF vectorizer was used during training)
#     return vectorizer.transform([text])

# # Fetch reviews using the ASIN
# def fetch_reviews_for_asin(api_key, asin):
#     url = "https://real-time-amazon-data.p.rapidapi.com/product-reviews"
#     querystring = {
#         "asin": asin,
#         "country": "US",
#         "sort_by": "TOP_REVIEWS",
#         "star_rating": "ALL",
#         "verified_purchases_only": "false",
#         "images_or_videos_only": "false",
#         "current_format_only": "false",
#         "page": "1"
#     }
#     headers = {
#         "x-rapidapi-key": api_key,
#         "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
#     }

#     try:
#         response = requests.get(url, headers=headers, params=querystring)
#         if response.status_code != 200:
#             return None
#         response_json = response.json()
#         reviews = response_json.get('data', {}).get('reviews', [])
#         return reviews
#     except Exception as e:
#         print(f"Error fetching reviews: {e}")
#         return None

# # Save reviews to a CSV file
# def save_reviews_to_csv(product_name, reviews):
#     csv_filename = f'{product_name}_reviews.csv'
#     with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Product Name', 'Review ID', 'Review Title', 'Review Comment', 'Rating', 'Review Link', 'Review Author', 'Review Author Avatar', 'Review Date', 'Verified Purchase', 'Helpful Vote Statement', 'Reviewed Product ASIN'])
#         for review in reviews:
#             writer.writerow([
#                 product_name,  # Save the product name
#                 review.get('review_id', ''),
#                 review.get('review_title', ''),
#                 review.get('review_comment', ''),
#                 review.get('review_star_rating', ''),
#                 review.get('review_link', ''),
#                 review.get('review_author', ''),
#                 review.get('review_author_avatar', ''),
#                 review.get('review_date', ''),
#                 review.get('is_verified_purchase', ''),
#                 review.get('helpful_vote_statement', ''),
#                 review.get('reviewed_product_asin', '')
#             ])
#     print(f"Reviews saved to {csv_filename}")

# # Function to analyze reviews from a CSV file
# def analyze_reviews_from_csv(csv_filename):
#     # Read the CSV file
#     reviews_df = pd.read_csv(csv_filename)
    
#     # Preprocess and predict sentiment
#     sentiments = []
#     for index, row in reviews_df.iterrows():
#         review_text = row['Review Comment']
#         if pd.isna(review_text):
#             continue
        
#         preprocessed_review = preprocess_text(review_text)
#         sentiment = trained_model.predict(preprocessed_review)

#         # Determine sentiment label based on model prediction
#         if sentiment >= 0.6:
#             sentiment_label = 'positive'
#         elif sentiment <= 0.4:
#             sentiment_label = 'negative'
#         else:
#             sentiment_label = 'neutral'
        
#         # Print sentiment to terminal
#         print(f"Review: {review_text} | Sentiment: {sentiment_label}")
#         sentiments.append(sentiment_label)

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.json
#         if data is None:
#             return jsonify({"error": "No data received, please send the product name in the request body as JSON."}), 400

#         product_name = data.get("product_name") or data.get("brand_name")
#         if not product_name:
#             return jsonify({"error": "Product name is required in the request body."}), 400

#         asin = asin_dict.get(product_name)
#         if not asin:
#             return jsonify({"error": f"No ASIN found for product: {product_name}"}), 404

#         api_key = "5ba1089567msh3547f02f2fea32ap18f045jsn7eebdaa0d611"  # Replace with your real API key

#         # Fetch reviews for the ASIN
#         reviews = fetch_reviews_for_asin(api_key, asin)
#         if reviews is None:
#             return jsonify({"error": "Failed to fetch reviews."}), 500

#         # Save reviews to CSV
#         save_reviews_to_csv(product_name, reviews)

#         # Analyze reviews from CSV
#         csv_filename = f'{product_name}_reviews.csv'
#         analyze_reviews_from_csv(csv_filename)

#         return jsonify({"message": "Reviews saved and analyzed successfully. Check terminal for results."})

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


#predict

# import requests
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from tensorflow import keras
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import pickle
# import os
# import pandas as pd
# import csv

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load the RNN model
# MODEL_PATH = os.path.join(os.getcwd(), 'mymodel.keras')  # Path to the saved model
# model = keras.models.load_model(MODEL_PATH)  # Loading the model

# # Load the tokenizer used during training
# TOKENIZER_PATH = os.path.join(os.getcwd(), 'tokenizerfile.pickle')  # Path to the tokenizer
# with open(TOKENIZER_PATH, 'rb') as handle:
#     tokenizer = pickle.load(handle)

# # Maximum length of the input sequence (same as used during training)
# max_length = 100

# # Helper function to preprocess text
# def preprocess_text(text):
#     sequence = tokenizer.texts_to_sequences([text])
#     padded_sequence = pad_sequences(sequence, maxlen=max_length, padding='post', truncating='post')
#     return padded_sequence

# # Analyze the sentiment of reviews from a CSV file
# def analyze_reviews_from_csv(csv_file):
#     # Load reviews from the CSV file
#     df = pd.read_csv(csv_file)
    
#     predictions = []
#     for index, row in df.iterrows():
#         review_text = row.get('Review Comment', '')  # Adjust column name as needed
#         if review_text:
#             preprocessed_review = preprocess_text(review_text)
#             sentiment = model.predict(preprocessed_review)
            
#             if sentiment[0][0] >= 0.66:
#                 sentiment_label = 'positive'
#             elif sentiment[0][0] <= 0.33:
#                 sentiment_label = 'negative'
#             else:
#                 sentiment_label = 'neutral'
            
#             # Print sentiment result for each review
#             print(f"Review: {review_text}\nSentiment: {sentiment_label}\n")
            
#             predictions.append({
#                 'review': review_text,
#                 'sentiment': sentiment_label
#             })
#     return predictions

# # Endpoint to predict sentiment for reviews
# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Print the raw data to debug the input
#         data = request.json
#         print("Received data:", data)  # Debugging

#         # Ensure data is not None
#         if data is None:
#             return jsonify({"error": "No data received, please send the product name in the request body as JSON."}), 400

#         # Check for product_name or brand_name key and adjust accordingly
#         product_name = data.get("product_name") or data.get("brand_name")  # Check both keys

#         # Ensure the client provides the product name
#         if not product_name:
#             return jsonify({"error": "Product name is required in the request body."}), 400

#         # Load reviews from the CSV file
#         csv_filename = f'{product_name}_reviews.csv'  # Use the CSV file with product reviews
#         if not os.path.exists(csv_filename):
#             return jsonify({"error": f"No reviews CSV file found for product: {product_name}"}), 404

#         # Analyze reviews from the CSV file
#         predictions = analyze_reviews_from_csv(csv_filename)
        
#         return jsonify(predictions)

#     except Exception as e:
#         print(f"An error occurred: {e}")  # Print any unexpected errors
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

#prediction with reviews 
# import requests
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from tensorflow import keras
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import pickle
# import os
# import pandas as pd
# import csv

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load the RNN model
# MODEL_PATH = os.path.join(os.getcwd(), 'mymodel.keras')  # Path to the saved model
# model = keras.models.load_model(MODEL_PATH)  # Loading the model

# # Load the tokenizer used during training
# TOKENIZER_PATH = os.path.join(os.getcwd(), 'tokenizerfile.pickle')  # Path to the tokenizer
# with open(TOKENIZER_PATH, 'rb') as handle:
#     tokenizer = pickle.load(handle)

# # Maximum length of the input sequence (same as used during training)
# max_length = 100

# # Load Excel data into a dictionary
# excel_path = 'D:/SEM3/MINIPROJECT/Asin.xlsx'  # Adjust path as necessary
# excel_data = pd.read_excel(excel_path)
# asin_dict = dict(zip(excel_data['Product Name'], excel_data['ASIN']))  # Assuming columns are named 'Product Name' and 'ASIN'

# # Helper function to preprocess text
# def preprocess_text(text):
#     sequence = tokenizer.texts_to_sequences([text])
#     padded_sequence = pad_sequences(sequence, maxlen=max_length, padding='post', truncating='post')
#     return padded_sequence

# # Fetch reviews using the ASIN
# def fetch_reviews_for_asin(api_key, asin):
#     url = "https://real-time-amazon-data.p.rapidapi.com/product-reviews"
#     querystring = {
#         "asin": asin,
#         "country": "US",
#         "sort_by": "TOP_REVIEWS",
#         "star_rating": "ALL",
#         "verified_purchases_only": "false",
#         "images_or_videos_only": "false",
#         "current_format_only": "false",
#         "page": "1"
#     }
#     headers = {
#         "x-rapidapi-key": api_key,
#         "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
#     }

#     try:
#         print(f"Fetching reviews for ASIN: {asin}")  # Debug: Print ASIN
#         response = requests.get(url, headers=headers, params=querystring)
        
#         # Log the full API request details
#         print(f"Request URL: {response.url}")  # Print the full URL with parameters
#         print(f"Status Code: {response.status_code}")  # Print status code
        
#         if response.status_code != 200:
#             print(f"Error: Received status code {response.status_code}")
#             print(f"Response Text: {response.text}")  # Log the full response text for debugging
#             return None

#         response_json = response.json()
#         print(f"API Response: {response_json}")  # Debug: Print the full API response

#         reviews = response_json.get('data', {}).get('reviews', [])
#         return reviews

#     except Exception as e:
#         print(f"Error fetching reviews: {e}")  # Print error if fetching fails
#         return None
    
# def save_reviews_to_csv(product_name, reviews):
#     # Create or append to a CSV file
#     csv_filename = f'{product_name}_reviews.csv'
#     with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         # Write the headers
#         writer.writerow(['Review ID', 'Review Title', 'Review Comment', 'Rating', 'Review Link', 'Review Author', 'Review Author Avatar', 'Review Date', 'Verified Purchase', 'Helpful Vote Statement', 'Reviewed Product ASIN'])
        
#         # Write review details
#         for review in reviews:
#             writer.writerow([
#                 review.get('review_id', ''),
#                 review.get('review_title', ''),
#                 review.get('review_comment', ''),
#                 review.get('review_star_rating', ''),
#                 review.get('review_link', ''),
#                 review.get('review_author', ''),
#                 review.get('review_author_avatar', ''),
#                 review.get('review_date', ''),
#                 review.get('is_verified_purchase', ''),
#                 review.get('helpful_vote_statement', ''),
#                 review.get('reviewed_product_asin', '')
#             ])
#     print(f"Reviews saved to {csv_filename}")

# # Updated function to predict sentiment with improved accuracy
# def predict_sentiment(review_text):
#     preprocessed_review = preprocess_text(review_text)
#     sentiment = model.predict(preprocessed_review)
    
#     # Using multiple thresholds for sentiment classification
#     if sentiment[0][0] >= 0.66:
#         sentiment_label = 'positive'
#     elif sentiment[0][0] <= 0.33:
#         sentiment_label = 'negative'
#     else:
#         sentiment_label = 'neutral'
    
#     return sentiment_label

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Print the raw data to debug the input
#         data = request.json
#         print("Received data:", data)  # Debugging

#         # Ensure data is not None
#         if data is None:
#             return jsonify({"error": "No data received, please send the product name in the request body as JSON."}), 400

#         # Check for product_name or brand_name key and adjust accordingly
#         product_name = data.get("product_name") or data.get("brand_name")  # Check both keys

#         # Ensure the client provides the product name
#         if not product_name:
#             return jsonify({"error": "Product name is required in the request body."}), 400

#         # Retrieve the ASIN for the product name from the dictionary
#         asin = asin_dict.get(product_name)

#         if not asin:
#             return jsonify({"error": f"No ASIN found for product: {product_name}"}), 404

#         api_key = "5ba1089567msh3547f02f2fea32ap18f045jsn7eebdaa0d611"  # Replace with your real API key

#         # Fetch reviews for the ASIN
#         reviews = fetch_reviews_for_asin(api_key, asin)
#         if reviews is None:
#             return jsonify({"error": "Failed to fetch reviews."}), 500

#         print("Fetched reviews:", reviews)  # Print the reviews to the terminal

#         # Save the reviews to a CSV file
#         save_reviews_to_csv(product_name, reviews)

#         # Preprocess reviews and predict sentiment
#         predictions = []
#         for review in reviews:
#             review_comment = review.get('review_comment', '')
#             if review_comment:  # Skip if review comment is empty
#                 sentiment_label = predict_sentiment(review_comment)
#                 predictions.append({
#                     'review': review_comment,
#                     'sentiment': sentiment_label
#                 })

#         return jsonify(predictions)

#     except Exception as e:
#         print(f"An error occurred: {e}")  # Print any unexpected errors
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


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
excel_path = 'D:/SEM3/MINIPROJECT/Asin.xlsx'  # Adjust path as necessary
excel_data = pd.read_excel(excel_path)
#asin_dict = dict(zip(excel_data['Product Name'], excel_data['ASIN']))  # Assuming columns are named 'Product Name' and 'ASIN'


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
       
        # Log the full API request details
        print(f"Request URL: {response.url}")  # Print the full URL with parameters
        print(f"Status Code: {response.status_code}")  # Print status code
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response Text: {response.text}")  # Log the full response text for debugging
            return None

        response_json = response.json()
        print(f"API Response: {response_json}")  # Debug: Print the full API response

        # Extract relevant information: total reviews, total ratings, country
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
    if sentiment[0][0] >= 0.66:
        sentiment_label = 'positive'
    elif sentiment[0][0] <= 0.33:
        sentiment_label = 'negative'
    else:
        sentiment_label = 'neutral'
    
    return sentiment_label


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Print the raw data to debug the input
        data = request.json
        print("Received data:", data)  # Debugging

        # Ensure data is not None
        if data is None:
            return jsonify({"error": "No data received, please send the product name in the request body as JSON."}), 400

        # Check for product_name or brand_name key and adjust accordingly
        product_name = data.get("product_name") or data.get("brand_name")  # Check both keys

        # Ensure the client provides the product name
        if not product_name:
            return jsonify({"error": "Product name is required in the request body."}), 400

        # Normalize product_name to lower case for case-insensitive matching
        product_name = product_name.strip().lower()

        # Retrieve the ASIN for the product name from the dictionary
        asin = asin_dict.get(product_name)

        if not asin:
            return jsonify({"error": f"No ASIN found for product: {product_name}"}), 404

        api_key = "5ba1089567msh3547f02f2fea32ap18f045jsn7eebdaa0d611"  # Replace with your real API key

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
            if review_comment:  # Skip if review comment is empty
                sentiment_label = predict_sentiment(review_comment)
                predictions.append({
                    'review': review_comment,
                    'sentiment': sentiment_label
                })

        return jsonify(predictions)

    except Exception as e:
        print(f"An error occurred: {e}")  # Print any unexpected errors
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)


