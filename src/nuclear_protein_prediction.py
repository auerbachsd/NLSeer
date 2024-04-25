import pickle
import gzip

# Assuming sequence_removal and pssm_scoring modules contain necessary functions
from .sequence_removal import *
from .pssm_scoring import *
from .pssm_feature import *






def load_object_from_file(filename):
    """
    Utility function to load a Python object from a pickle file.
    """
    # print("Loading file from:", filename)

    with gzip.open(filename, 'rb') if filename.endswith('.gz') else open(filename, 'rb') as file:
        return pickle.load(file)

def predict_nuclear_protein(sequence, classifier, nls_pssm, feature_vec_length=20):
    """
    Predicts whether a given protein sequence is a nuclear protein.

    Parameters:
        sequence (str): The protein sequence to predict.
        classifier (object): Trained machine learning model.
        nls_pssm (dict): Position-Specific Scoring Matrix for nuclear localization sites.
        feature_vec_length (int): The length of feature vectors derived from the PSSM.

    Returns:
        str: "Nuclear" if the sequence is predicted as nuclear, otherwise "Non-nuclear".
    """
    length_cutoff = feature_vec_length + 20

    if len(sequence) <= length_cutoff:
        raise ValueError("The protein sequence is too short. Minimum required length is {}.".format(length_cutoff))


    feature_vector = compute_top_n_pssm_scores(sequence, nls_pssm, feature_vec_length)

    prediction = classifier.predict(feature_vector)

    return "Nuclear" if prediction[0] == 1 else "Non-nuclear"