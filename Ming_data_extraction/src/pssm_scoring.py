"""
This section of the code utilizes modified components of Position-Specific Scoring Matrices from Biopython.
Biopython is distributed under the Biopython License and BSD 3-Clause License.
More details can be found at: https://biopython.org
"""

import numpy as np
from collections import defaultdict
import math

standard_amino_acids = 'ACDEFGHIKLMNPQRSTVWY'  # 20 standard amino acids
""" Background amino acids frequencies """
background = {'A':0.0777,
              'C':0.0157,
              'D':0.053,
              'E':0.0656,
              'F':0.0405,
              'G':0.0691,
              'H':0.0227,
              'I':0.0591,
              'K':0.0595,
              'L':0.096,
              'M':0.0238,
              'N':0.0427,
              'P':0.0469,
              'Q':0.0393,
              'R':0.0526,
              'S':0.0694,
              'T':0.055,
              'V':0.0667,
              'W':0.0118,
              'Y':0.0311}
# The following frequence is computed via compute_background_frequencies.ipynb but does not work very well
# background = {'M': 0.02211207580407797,
#               'P': 0.07190226876090751,
#               'Y': 0.02350057717452554,
#               'K': 0.07186287865110758,
#               'L': 0.08816710159912904,
#               'E': 0.07915770815211147,
#               'V': 0.05594599178278543,
#               'A': 0.0684939300934968,
#               'C': 0.01752750469125266,
#               'T': 0.04976502705334625,
#               'S': 0.09052722567797492,
#               'G': 0.06453522405860374,
#               'D': 0.052761957907291,
#               'N': 0.035706040363920846,
#               'Q': 0.05032743028771193,
#               'R': 0.05507175017917029,
#               'I': 0.03830797595014963,
#               'F': 0.031072231613845622,
#               'H': 0.02474574231209003,
#               'W': 0.008509357886501775}



class GenericPositionMatrix:
    """Base class for position matrix operations on protein motifs."""
    

    def __init__(self, aligned_sequences):
        self.length = len(aligned_sequences[0])  
        self.standard_amino_acids = standard_amino_acids
        self._validate_sequences(aligned_sequences)  
        self.matrix = self._calculate_position_counts(aligned_sequences)
        self.num_sequences = len(aligned_sequences)
        self.effective_length = self.find_effective_length()  # Calculate effective length after all setups

    def _validate_sequences(self, aligned_sequences):
        if not all(len(seq) == self.length for seq in aligned_sequences):
            raise ValueError("Data has inconsistent lengths.")

    def _calculate_position_counts(self, aligned_sequences):
        aa_counts = defaultdict(lambda: [0] * self.length)
        for seq in aligned_sequences:
            for position, amino_acid in enumerate(seq):
                aa_counts[amino_acid][position] += 1
        return aa_counts

    def find_effective_length(self, threshold=0.9):
        """Dynamically determine the effective NLS length, excluding padding."""
        for position in range(self.length - 1, -1, -1):
            padding_ratio = self.matrix['-'][position] / self.num_sequences
            if padding_ratio < threshold:
                return position + 1  # Return length excluding padding
        return self.length  # Return full length if no padding detected

class PositionWeightMatrix(GenericPositionMatrix):
    """Supports frequency calculations for protein motifs."""

    def normalize(self, background_frequencies=background, pseudocount_factor=1):
        normalized_matrix = {aa: [0.0] * self.effective_length for aa in self.standard_amino_acids}
        total_counts = [0] * self.effective_length

        for aa in self.standard_amino_acids:
            for position in range(self.effective_length):
                pseudocount = background_frequencies[aa] * pseudocount_factor
                count = self.matrix.get(aa, [0] * self.effective_length)[position] + pseudocount
                normalized_matrix[aa][position] = count
                total_counts[position] += count

        for aa, counts in normalized_matrix.items():
            for position, count in enumerate(counts):
                normalized_matrix[aa][position] = count / total_counts[position] if total_counts[position] else 0

        self.matrix = normalized_matrix

    def log_odds(self, background_frequencies=background):
        background_frequencies = background
        # or {aa: 1.0 / len(self.standard_amino_acids) for aa in self.standard_amino_acids}
        log_odds_matrix = {aa: [0] * self.effective_length for aa in self.standard_amino_acids}

        for aa in self.standard_amino_acids:
            for position in range(self.effective_length):
                p = self.matrix[aa][position]
                b = background_frequencies.get(aa, 0)
                score = math.log(p / b, 2) if p > 0 else -math.inf
                log_odds_matrix[aa][position] = score

        return PositionSpecificScoringMatrix(log_odds_matrix, self.effective_length)

class PositionSpecificScoringMatrix:
    """Scores sequences against a Position Specific Scoring Matrix (PSSM)."""

    def __init__(self, matrix, length):
        self.matrix = matrix
        self.length = length
        self.standard_amino_acids = 'ACDEFGHIKLMNPQRSTVWY'

    def __str__(self):
        lines = ["   " + " ".join(f"{i:6d}" for i in range(self.length))]
        for amino_acid in self.standard_amino_acids:
            line = f"{amino_acid}: " + " ".join(f"{self.matrix[amino_acid][i]:6.2f}" for i in range(self.length))
            lines.append(line)
        return "\n".join(lines)

    def calculate(self, sequence):
        """Calculate the PSSM score for a given protein sequence."""
        # Initial checks and setup
        sequence = sequence.upper()
        if any(aa not in self.standard_amino_acids for aa in sequence):
            raise ValueError("Sequence contains invalid amino acids for this PSSM.")

        scores = np.empty(len(sequence) - self.length + 1, dtype=np.float32)
        for offset in range(len(scores)):
            score = sum(self.matrix[aa][position] for position, aa in enumerate(sequence[offset:offset + self.length]) if aa in self.matrix)
            scores[offset] = score
        return scores

    def search(self, sequence, threshold=0.0):
        """Find hits in the sequence with PSSM score above a given threshold."""
        sequence = sequence.upper()
        potential_hits = []
        scores = self.calculate(sequence)
        for i, score in enumerate(scores):
            if score >= threshold:
                potential_hits.append((i, score))

        potential_hits.sort(key=lambda x: x[1], reverse=True)
        return potential_hits