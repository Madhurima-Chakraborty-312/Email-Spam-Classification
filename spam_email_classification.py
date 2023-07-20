# -*- coding: utf-8 -*-
"""Spam Email Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1015fzd0FEubPwzH1QhMqZKnwrPqjZsqR
"""

import numpy as np
import pandas as pd
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier

nltk.download('punkt')
nltk.download('stopwords')

# Step 1: Introduction and overview
print("Spam Email Classification Model")

# Step 2: Data set preparation
# Load the dataset
data = pd.read_csv('spam_dataset.csv')

data.head()

data.head().info

# Step 3: Text data preprocessing
# Remove stop words, perform stemming, or any other preprocessing steps
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Create a stemmer object
stemmer = PorterStemmer()

# Remove stop words and perform stemming
stopwords = set(stopwords.words('english'))
data['processed_content'] = data['Email No.'].apply(lambda x: ' '.join([stemmer.stem(word) for word in word_tokenize(x) if word.lower() not in stopwords]))

# Step 4: Exploratory Data Analysis (EDA)
# Conduct EDA to gain insights into the dataset
# Add your EDA code here
# For example, you can print the distribution of spam and non-spam emails
print("Distribution of labels:")
print(data['Prediction'].value_counts())

# Step 5: Feature extraction or selection
# Perform TF-IDF vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['processed_content'])
y = data['Prediction']

# Step 6: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 7: Implement a baseline classification model (Naive Bayes)

# Check for NaN values in y_train
if np.isnan(y_train).any():
    # Handle missing values in y_train
    X_train = X_train[~np.isnan(y_train)]
    y_train = y_train[~np.isnan(y_train)]

# Initialize the classifier
clf = MultinomialNB()

# Train the classifier
clf.fit(X_train, y_train)

# Step 8: Model evaluation
# Make predictions on the test set
y_pred = clf.predict(X_test)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='binary')
recall = recall_score(y_test, y_pred, average='binary')
f1 = f1_score(y_test, y_pred, average='binary')


# Print the evaluation metrics
print("Baseline Model Evaluation:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

# Step 9: Improve the model's performance
from sklearn.model_selection import GridSearchCV

# Define the parameter grid
param_grid = {
    'n_estimators': [100, 200, 500],
    'max_depth': [None, 5, 10],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}

# Initialize the Random Forest classifier
clf_rf = RandomForestClassifier()

# Perform grid search for hyperparameter tuning
grid_search = GridSearchCV(clf_rf, param_grid, cv=5)
grid_search.fit(X_train, y_train)

# Get the best parameters and score
best_params = grid_search.best_params_
best_score = grid_search.best_score_

# Initialize a new Random Forest classifier with the best parameters
clf_rf = RandomForestClassifier(**best_params)

# Train the Random Forest classifier with the updated parameters
clf_rf.fit(X_train, y_train)

# Step 10: Evaluate the model on the test set
# Make predictions on the test set using the improved model
y_pred_rf = clf_rf.predict(X_test)

# Calculate evaluation metrics for the Random Forest model
accuracy_rf = accuracy_score(y_test, y_pred_rf)
precision_rf = precision_score(y_test, y_pred_rf, average='binary')
recall_rf = recall_score(y_test, y_pred_rf, average='binary')
f1_rf = f1_score(y_test, y_pred_rf, average='binary')


# Print the evaluation metrics for the Random Forest model
print("Improved Model (Random Forest) Evaluation:")
print("Accuracy:", accuracy_rf)
print("Precision:", precision_rf)
print("Recall:", recall_rf)
print("F1 Score:", f1_rf)

# Step 11: Identify limitations and suggest enhancements
# Analyze the results and provide feedback
# Compare the performance of the baseline model and the improved model
if accuracy_rf > accuracy:
    print("The improved model (Random Forest) outperforms the baseline model (Naive Bayes).")
elif accuracy_rf < accuracy:
    print("The improved model (Random Forest) performs worse than the baseline model (Naive Bayes).")
else:
    print("The improved model (Random Forest) has the same performance as the baseline model (Naive Bayes).")

# Provide feedback and suggestions for further enhancements
# Add your analysis and suggestions here
# For example, you can discuss potential reasons for the performance differences, such as the ability of Random Forest to capture complex relationships in the data.

# Step 12: Prepare a presentation summarizing the findings and provide feedback
# Create a presentation summarizing the methodology, results, and insights gained
# Add your code for creating the presentation here
# For example, you can use libraries like Matplotlib or Plotly to create visualizations and present key findings.

# Create a bar plot to visualize the distribution of spam and non-spam emails
sns.set(style="darkgrid")
plt.figure(figsize=(6, 4))
sns.countplot(x='Prediction', data=data)
plt.title('Distribution of Spam and Non-Spam Emails')
plt.xlabel('Label')
plt.ylabel('Count')
plt.show()

# Print the evaluation metrics for both models in a table format
metrics_data = {
    'Model': ['Baseline (Naive Bayes)', 'Improved (Random Forest)'],
    'Accuracy': [accuracy, accuracy_rf],
    'Precision': [precision, precision_rf],
    'Recall': [recall, recall_rf],
    'F1 Score': [f1, f1_rf]
}
metrics_df = pd.DataFrame(metrics_data)
print("\nEvaluation Metrics:")
print(metrics_df)
