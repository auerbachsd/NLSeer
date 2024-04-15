# NLSeer

# Nuclear Localization Signal (NLS) Prediction Project

The purpose of the project is to build a prediction tool that estimates the possibility of nuclear localization signals inside a protein's sequence while also taking into account its 3-D structure to help assess whether or not certain amino acids factor into forming one of these signals or not. In addition to the 3-D structure, the position of each amino acid inside the sequence is also taken into consideration.

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

In this project, we have implemented several techniques to construct a model specifically designed to predict NLS signals based on both the sequence and 3-D structure of a protein. These are the position-specific sorting matrix (PSSM), graph convolutional networks (GCN), and Bidirectional Encoder Representations from Transformers (BERT). For probability visualization, the Logomaker package was used to generate a graph showing probability of a NLS for each amino acid in the query sequence. The objective is to be able to generate proababilities of having NLS for any given protein.

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

The main dataset is a compilation of nuclear localization signals organized by experimental verification that was extracted from the paper by Yamagishi et al in their 2016 paper (see citation below). As a validation set, another NLS dataset was obtained from the Rost Lab at the Technical University of Munich. The Yamagishi dataset has about 1,300 signals while the Rost dataset has approximately 300 verified NLS signals. 

This dataset was modified in the following ways:

<ul>
    <li> Obtained UniProt IDs for each protein in the datasets to help obtain their 3-D structure using NLS sequences as a query, these IDs were added to the dataset (URL: https://www.uniprot.org/peptide-search) </li>
    <li> Through their UniProt IDs, full sequences were added to the dataset using the query system provided on the UniProt website. (URL for reference: https://www.uniprot.org/id-mapping) </li>
    <li> For the validation set, UniProt IDs and full sequences were obtained using the same methods. </li>
    <li> Some NLS sequences were updated accordingly during the search process as some of them were identified using antiquated technologies. Others which could not be found using the UniProt search tools or verified in scientific literature were removed from the list. However, only a few of the original sequences were lacking this verification </li>

## Approach
We used different approaches to estimate the contribution of each amino acid in a protein sequence to a potential NLS motif. 
To be completed.

### Position-specific scoring matrix (PSSM)
The PSSM approach lines up a series of proteins padded to the same length for simplicity and then assigns a score to each amino acid based on motifs found in the training data. Individual amino acids found in these motifs were identified with high accuracy. 
To be completed.

### Graph convolutional networks (GCNs) and bidirectional Encoder Representations from Transformers (BERT)

Two types of output were fed into these GCNs: the first was the embeddings of the protein sequence itself and the second was the corresponding 3-D structure node embeddings. For the first type of data, the sequences were pre-processed using the BERT embedder ProtBERT developed by the Rost Lab and optimized for analyzing proteins of varying lengths. 3-D structures were obtained from the AlphaFold database, which were then used to generate contact maps, or graphical representations of interactions between residues to check if this affected NLS likelihood. These contact maps were embedded further to generate node embeddings or a low-dimensional representation of the 3-D structure. 

## Citations
