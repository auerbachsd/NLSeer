"""
Turn protein sequences into pssm feature vectors
"""
import pandas as pd
import numpy as np


from .pssm_scoring import *
from .sequence_removal import *


# Find the top n scores
def compute_top_n_scores(array, length=20):
    top_n = np.partition(array, -length)[-length:]
    top_n_sorted = np.sort(top_n)[::-1]  # Sort and reverse to show largest first
    return top_n_sorted


# Create a DataFrame from the list of top n scores and label
def create_feature_vectors(df, pssm, column_name, feature_vec_length, label ):
    top_n_scores_list = [compute_top_n_scores(pssm.calculate(protein_seq),feature_vec_length) for protein_seq in df[column_name]]
    scores_df = pd.DataFrame(top_n_scores_list, columns=[f'Score_{i+1}' for i in range(feature_vec_length)])
    scores_df['Label'] = label
    return scores_df

#
def compute_top_n_pssm_scores(sequence, pssm, feature_vec_length):
    feature_vec = compute_top_n_scores(pssm.calculate(sequence),feature_vec_length) 
    feature_df  = pd.DataFrame([feature_vec], columns=[f'Score_{i+1}' for i in range(feature_vec_length)])


    return feature_df
