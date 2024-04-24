# NLSeer

# Nuclear Localization Signal (NLS) Prediction Project

The purpose of the project is to build a prediction tool that estimates the possibility of nuclear localization signals inside a protein's sequence based on the significance of each amino acid. 

# Authors

<ol>
    <li> Scott Auerbach </li>
    <li> Ukamaka Nnyaba </li>
    <li> Ming Zhang </li>
    <li> Yingyi Guo </li>
    <li> Hemaa Selvakumar </li>
    <li> Cisil Karaguzel </li>
</ol>

# Description

## Overview

Nuclear localization signals are fragments of a protein sequence, ranging from anywhere between several amino acids to a couple dozen, that help direct a protein's movement to the nucleus. These signals have been implicated in human diseases and play a major role in many biological functions. However, despite all the advances made towards understanding the proteins that make up our body, our ability to predict (and thus understand) where these signals are remains elusive. Advances in machine learning techniques present the possibility of identifying these signals.

In this project, we have implemented several techniques to construct a model specifically designed to predict NLS signals based on its sequence. These are the position-specific sorting matrix (PSSM), convolutional neural networks (CNN), and Bidirectional Encoder Representations from Transformers (BERT). For probability visualization, the Logomaker package was used to generate a graph showing probability of contributing to a NLS for each amino acid in the query sequence. The objective is to be able to generate proababilities of having NLS for any given protein.

**Stakeholders** :

Medical researchers specializing in nuclear transport as a mode of disease progression as well as general molecular biologists who are trying to understand the mechanisms of their proteins of interest.

**KPIs for NLSeer**:

<ul>
    <li>AUC and ROC scores greater than or equal to 0.8</li>
    <li>Ability to predict nuclear localization signals using validation set from the Rost Lab</li>
    <li>Data visualization will directly display the potential contribution of each amino acid to a NLS</li>
    <li>Successfully integrate factoring in 3-D structure of a protein to assess potential of being part of a NLS</li>
    <li>Superior performance in terms of accuracy and precision compared to other available NLS prediction tools</li>
</ul>

## Dataset

The main dataset is a compilation of nuclear localization signals organized by experimental verification that was extracted from the paper by Yamagishi et al in their 2016 paper (see citation below). The Yamagishi dataset has about 1,300 signals while the Rost dataset has approximately 300 verified NLS signals. For further enhancement of model capabilities, another dataset compiled by the Danish Department of Health Technology (cited below) including proteins containing signals for various organelles in addition to the nucleus were also screened in the model.

This dataset was modified in the following ways:

<ul>
    <li> Through their UniProt IDs, full sequences were added to the dataset using the query system provided on the UniProt website. (URL for reference: https://www.uniprot.org/id-mapping) </li>
    <li> For the DeepLoc set, UniProt IDs and full sequences were obtained using the same methods. </li>
    <li> Some NLS sequences were updated accordingly during the search process as some of them were identified using antiquated technologies. Others which could not be found using the UniProt search tools or verified in scientific literature were removed from the list. However, only a few of the original sequences were lacking this verification </li>

## Approach
We used different approaches to estimate the contribution of each amino acid in a protein sequence to a potential NLS motif. 


### Position-specific scoring matrix (PSSM)
The PSSM approach lines up a series of proteins padded to the same length for simplicity (1000 residues each) and then assigns a score to each amino acid based on motifs found in the training data. The logic of this approach is that over the course of evolution, groups of amino acids that perform a certain function are conserved over time. This means that proteins that have similar functions tend to have similar sequences, whether for the overall length of the protein or for select motifs in the sequence. Individual amino acids found in these motifs were identified with ~70% accuracy. 


### Convolutional neural networks (CNNs) and bidirectional Encoder Representations from Transformers (BERT)

First, the BERT model was used to process the amino acid sequences by truncating their length past the maximum of 512 and padding anything shorter than that to that number. This model utilized an Adam optimizer and a cross-entropy loss function. Due to computational constraints, we ran a very basic version of the model where only two epochs were used and the batch size was two. Even with bare-bones settings, the model was too taxing to run on our computers, so we pivoted towards the CNN model. 

The CNN model involved one-hot encoding - meaning that documented NLS sequences within our dataset were labelled as 1, and everything else was labelled 0 - this includes whole sequences of non-nuclear proteins once they were added to the dataset. Different kernel sizes were selected to further optimize the model. In addition to using the Tensorflow package to generate the CNN model, this was supplemented further by XGBoost, which prevented overfitting and minimized training loss. The CNN model utilized a greater batch size (32) and more epochs (10). Once the CNN model was trained on the data, XGBoost was used to extract features from the CNN model's predictions and supplement them with more refined data. This process was first done with the nuclear protein-only dataset obtained from the Yamagishi group, and then repeated with a more comprehensive dataset obtained from the DeepLoc team.


## Results

### PSSM Construction and Evaluation


### BERT Model
For the initial BERT model without any PSSM input, the overall accuracy was very low: roughly 1%. No further attempts to optimize this model were taken due to lack of capacity on our computers.

### PSSM-CNN Model

When coupled with PSSM data, the CNN model was able to parse out patterns from the NLS signals and fairly reliably predict them: 

<ul>
    <li> When only nuclear proteins were used as input, the average accuracy between five folds (ten epochs each) was 91.36%. </li>
    <li> When using the more comprehensive DeepLoc dataset, which includes signals for both the nucleus and other organelles, the overall accuracy dropped to 73.62%. There may have been confirmation bias in the first dataset that may have skewed the accuracy results.




## Citations
DeepLoc 2.0: multi-label subcellular localization prediction using protein language models.
Vineet Thumuluri, Jose Juan Almagro Armenteros, Alexander Rosenberg Johansen, Henrik Nielsen, Ole Winther.
Nucleic Acids Research, Web server issue 2022.