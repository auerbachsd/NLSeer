import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from Bio import SeqIO
import csv


# Function to generate the AnnonEncoded column
def generate_annotation(row):
    sequence = row['Sequence']
    begin = row['Begin']
    end = row['End']
    annotation = ['6' if begin <= i <= end else '0' for i in range(len(sequence))]
    return ''.join(annotation)

# Function to remove rows containing "B", "U", or "X" in the sequence
def remove_bux(df3):
    df3['Contains_BU_or_X'] = df3['Sequence'].apply(lambda x: bool(re.search(r'[BUXbux]', x)))
    df3 = df3[~df3['Contains_BU_or_X']]
    df3 = df3.drop(columns=['Contains_BU_or_X'])
    return df3


