import sys
import pickle

# Load the TF-IDF Vectorizer and Trained Model
with open('D:/SEM3/MINIPROJECT/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf_vectorizer = pickle.load(f)

with open('D:/SEM3/MINIPROJECT/trained_model .pkl', 'rb') as f:
    model = pickle.load(f)

# Get the review text from the command line argument
review_text = sys.argv[1]

# Transform the review text
X_test = tfidf_vectorizer.transform([review_text])

# Predict the sentiment
prediction = model.predict(X_test)[0]

# Print the prediction (this will be captured by the Node.js server)
print(prediction)

