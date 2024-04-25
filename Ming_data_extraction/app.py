import io
import base64
from flask import Flask, request, render_template
import matplotlib.pyplot as plt
import pickle
import gzip
import os

import sys
sys.path.insert(0, './src')

from src.logo_plot import *
from src.pssm_scoring import *
from src.pssm_feature import *
from src.nuclear_protein_prediction import predict_nuclear_protein
from src.sequence_removal import *


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        protein_sequence = request.form['protein_sequence'].replace('\n', '').replace(' ','')

        try:
            result = predict_nuclear_protein(protein_sequence, classifier, nls_pssm)
            if result == "Nuclear":
                images = generate_logo(protein_sequence, calculate_scores(nls_pssm, protein_sequence))
                # plt.savefig(img, format='png', bbox_inches='tight')
                # plt.close()
                # img.seek(0)
                # plot_url = base64.b64encode(img.getvalue()).decode('utf8')
                return render_template('result.html',  prediction=result, images=images)
                # return app_logic(protein_sequence, nls_pssm)

            return render_template('result.html', prediction=result)
        
        except Exception as e:
            print(f"Error: {e}")
            return render_template('error.html', error=str(e))  # Create an error.html template for errors
                
    return render_template('index.html')


def calculate_scores(pssm, sequence):
    
    sequence_scores = pssm.calculate(sequence)
    return sequence_scores


def load_object_from_file(filename):
    """
    Utility function to load a Python object from a pickle file.
    """
    # print("Loading file from:", filename)

    with gzip.open(filename, 'rb') if filename.endswith('.gz') else open(filename, 'rb') as file:
        return pickle.load(file)
    
# # Function for handling calculation and result presentation in Flask app
# def app_logic(protein_sequence, nls_pssm):
#     img = io.BytesIO()
#     scores = calculate_scores(nls_pssm, protein_sequence)  # Ensure this function returns appropriate scores
#     images = generate_logo(protein_sequence, scores, buffer=img)

#     # plot_url = base64.b64encode(img.getvalue()).decode('utf8')
#     return render_template('result.html', prediction="Nuclear", images=images)
    
if __name__ == '__main__':
    print("Current working directory:", os.getcwd())

    # classifier = load_object_from_file('trained_classifiers/nls_random_forest_classifier.pkl.gz')
    # nls_pssm = load_object_from_file('data/nls_pssm.pkl')
    classifier = load_object_from_file('trained_classifiers/nls_random_forest_classifier.pkl.gz')
    nls_pssm = load_object_from_file('data/nls_pssm.pkl')
    app.run(debug=True)
