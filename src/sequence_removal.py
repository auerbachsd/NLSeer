"""
This module removes certain protein sequences in a dataset
"""

standard_amino_acids = 'ACDEFGHIKLMNPQRSTVWY'  # 20 standard amino acids
# Remove protein sequences that contain non-standard amino acids
def remove_sequences(df, column_name):
    remove_index = []
    for i,seq in enumerate(df[column_name]):
        if any(aa not in standard_amino_acids for aa in seq):
            remove_index.append(i)

    return df.drop(df.index[remove_index])

# Remove protein sequences shorter than a length_cutoff
def remove_short_sequences(df, length_cutoff):
    return df[df['Length'] >= length_cutoff]