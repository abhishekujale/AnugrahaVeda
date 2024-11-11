from flask import Flask, request, render_template
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
import joblib

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('dataset.csv')

# Data Preprocessing
X = df[['disease']]
y_drug = df['drug']
y_procedure = df['description']

# Encode categorical variable 'disease' using one-hot encoding
encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(X)

# K-Nearest Neighbors Classifier for drug prediction
knn_clf_drug = KNeighborsClassifier(n_neighbors=5, weights='uniform')  # Initial parameters
knn_clf_drug.fit(X_encoded, y_drug)

# K-Nearest Neighbors Classifier for procedure prediction
knn_clf_procedure = KNeighborsClassifier(n_neighbors=5, weights='uniform')  # Initial parameters
knn_clf_procedure.fit(X_encoded, y_procedure)

# Save the trained models and encoder to disk
joblib.dump(knn_clf_drug, 'knn_model_drug.joblib')
joblib.dump(knn_clf_procedure, 'knn_model_procedure.joblib')
joblib.dump(encoder, 'encoder.joblib')

# Route for default message and prediction
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        input_example = request.form['input_example']
        input_encoded = encoder.transform([[input_example]])
        predicted_drug = knn_clf_drug.predict(input_encoded)
        predicted_procedure = knn_clf_procedure.predict(input_encoded)
        return render_template('index.html', predicted_drug=predicted_drug[0], predicted_procedure=predicted_procedure[0])

if __name__ == '__main__':
    app.run(debug=True,port=7000)
