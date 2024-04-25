import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend (do this before importing plt)
import matplotlib.pyplot as plt
import numpy as np
import io
import logomaker
import base64





standard_amino_acids = 'ACDEFGHIKLMNPQRSTVWY'  # 20 standard amino acids
list_standard_amino_acids = list(standard_amino_acids)

# generate the logo for a protein sequence
def generate_logo(sequence, sequence_scores, segment_length=50):
    sequence_length = len(sequence)


    images = []

    # Loop through each segment of the sequence
    for start in range(0, sequence_length, segment_length):
        buffer = io.BytesIO()

        end = min(start + segment_length, sequence_length)  # Ensure we don't go out of bounds
        effective_segment_length = min(end-start, segment_length)


        # Extract the segment of the sequence and corresponding scores
        segment_sequence = sequence[start:end]
        segment_scores = sequence_scores[start:end]


        score_df = pd.DataFrame(index=range(effective_segment_length), columns=list_standard_amino_acids).fillna(0)

        # Map the pssm scores into the interval [0,1] using either logistic function, softmax, or minmax
        normalized_scores = logistic(np.array(segment_scores))
        # normalized_scores = softmax(sequence_scores)
        # normalized_scores = MinMax(sequence_scores)

        for i, (aa,score) in enumerate(zip(segment_sequence,normalized_scores)):
            score_df.at[i,aa] = score


        nn_logo = logomaker.Logo(score_df, color_scheme='skylign_protein')

        # style using Logo methods
        nn_logo.style_spines(visible=False)
        nn_logo.style_spines(spines=['left','bottom'], visible=True)
        xs = np.arange(0, effective_segment_length,10)
        xs_labels = np.arange(start, end,10)

        # style using Axes methods
        nn_logo.ax.set_xlim([0, effective_segment_length-1])
        nn_logo.ax.set_xticks(xs)
        nn_logo.ax.set_xticklabels(xs_labels.astype(str).tolist())
        nn_logo.ax.set_ylim([0, 1])
        nn_logo.ax.set_yticks([0, 0.25,.5,0.75 , 1])
        nn_logo.ax.set_yticklabels(['0', '0.25','0.5', '0.75', '1'])
        nn_logo.ax.set_ylabel('Sorting signal importance', labelpad=-1)

            # If a buffer is provided, save the plot to this buffer
        # if buffer is not None:
        plt.savefig(buffer, format='png', bbox_inches='tight')
        plt.close()
        buffer.seek(0)
        images.append(base64.b64encode(buffer.getvalue()).decode('utf8'))
        buffer.close()  # It's a good practice to close the buffer once done


    return images  

## Uncomment the following when running this code in python
# else:
#     plt.show()



def logistic(x):
    return 1/(1+np.exp(-x))


# def softmax(x):
#     e_x = np.exp(x-np.max(x))
#     return e_x / e_x.sum(axis=0)

# def MinMax(x):
#     x_min = np.min(x)
#     x_max = np.max(x)
#     return (x - x_min) / (x_max - x_min)


