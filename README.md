# NLSeer

# Nuclear Localization Signal (NLS) Prediction Project

The purpose of the project is to build a prediction tool that estimates the possibility of nuclear localization signals inside a protein's sequence based on the significance of each amino acid. Nuclear localization signals have been implicated in human diseases and play an important role in many biological pathways.

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

Nuclear localization signals are fragments of a protein sequence, ranging from anywhere between several amino acids to a couple dozen, that help direct a protein's movement to the nucleus. These signals have been implicated in human diseases and play a major role in many biological functions. However, despite all the advances made towards understanding the proteins that make up our body, advances in machine learning techniques present the possibility of more accurately identifying these signals.

In this project, we have implemented several techniques to construct a model specifically designed to predict NLS signals based on its sequence. These are the position-specific sorting matrix (PSSM), convolutional neural networks (CNN), and long short-term memory recurrent neural networks (LSTM-RNN). The objective is to be able to generate proababilities of having NLS for any given protein.

**Stakeholders** :

Medical researchers specializing in nuclear transport as a mode of disease progression as well as general molecular biologists who are trying to understand the mechanisms of their proteins of interest.

**KPIs for NLSeer**:

<ul>
    <li>AUC and ROC scores greater than or equal to 0.8</li>
    <li>Ability to predict nuclear localization signals using validation set from the Yamagishi Lab</li>
    <li>Data visualization will directly display the potential contribution of each amino acid to a NLS</li>
    <li>Superior performance in terms of accuracy and precision compared to other available NLS prediction tools</li>
</ul>

## Dataset

The main dataset is a compilation of nuclear localization signals organized by experimental verification that was extracted from the paper by Yamagishi et al in their 2016 paper (see citation below). The Yamagishi dataset has about 1,400 signal-containing proteins. For further enhancement of model capabilities, another dataset compiled by the Danish Department of Health Technology (cited below) including an approximately equal number of proteins containing signals for various organelles in addition to the nucleus were also screened in the model.

This dataset was modified in the following ways:

<ul>
    <li> Through their UniProt IDs, full sequences were added to the dataset using the query system provided on the UniProt website. (URL for reference: https://www.uniprot.org/id-mapping) </li>
    <li> For the DeepLoc set, UniProt IDs and full sequences were obtained using the same methods. </li>
    <li> Some NLS sequences were updated accordingly during the search process as some of them were identified using antiquated technologies. Others which could not be found using the UniProt search tools or verified in scientific literature were removed from the list. Fortunately, only a few of the original sequences were lacking this verification. </li>
</ul>


# Approach
We used several different approaches to estimate the possibility of a given protein containing a NLS: 


## Position-specific scoring matrix (PSSM)
The PSSM approach lines up a series of proteins padded to the same length for simplicity (1000 residues each) and then assigns a score to each amino acid based on motifs found in the training data. The logic of this approach is that over the course of evolution, groups of amino acids that perform a certain function are conserved over time. This means that proteins that have similar functions tend to have similar sequences, whether for the overall length of the protein or for select motifs in the sequence. Feature vectors were generated from full protein sequences and were set to 20 residues in length. 

Several types of binary classifiers were used to predict the likelihood of containing NLS motifs through PSSMs, with the NLS as the feature vector:

<ul>
    <li> Logistic regression </li>
    <li> SVC (Support Vector Machine Classifier) </li>
    <li> Decision tree </li>
    <li> Random forest </li>
    <li> Gaussian NB (Naive Bayes) </li>
    <li> MLP (Multi-layer perceptron) classifier </li>
    <li> Gradient boosting machine </li>
</ul>

## Convolutional neural networks (CNNs) and long short-term memory recurrent neural networks (LSTM-RNN)


The CNN model involved one-hot encoding - meaning that documented NLS sequences within our dataset were labelled as 1, and everything else was labelled 0 - this includes whole sequences of non-nuclear proteins once they were added to the dataset. Different kernel sizes were selected to further optimize the model. In addition to using the Tensorflow package to generate the CNN model, this was supplemented further by XGBoost, which prevented overfitting and minimized training loss. The CNN model utilized a batch size of 32 and ten epochs. Once the CNN model was trained on the data, XGBoost was used to extract features from the CNN model's predictions and supplement them with more refined data. This process was first done with the nuclear protein-only dataset obtained from the Yamagishi group, and then repeated with a more comprehensive dataset obtained from the DeepLoc team.

A long short-term memory (LSTM) model was then used to predict the presence of NLS using the combined dataset of Yamagishi and DeepLoc data. Similar to before, the maximum length of protein sequence was set to 1,000 and the final input size was set to 20,000 (20 columns for each type of amino acid times 1,000 positions). This model is "short-term" in that it only remembers some of the information as much as required, but this timeframe can be extended to cover the whole dataset. For this model, the retained information is the one-hot encoded NLS motif. 


# Results

## PSSM Construction and Evaluation

Using feature vectors extracted from NLS motifs, the following accuracy scores were obtained for the aforementioned classifiers:

<ul>
    <li> Logistic regression: 71% </li>
    <li> SVC (Support Vector Machine Classifier): 69% </li>
    <li> Decision tree: 72% </li>
    <li> Random forest: 73% </li>
    <li> Gaussian NB (Naive Bayes): 70% </li>
    <li> MLP (Multi-layer perceptron) classifier: 65% </li>
    <li> Gradient boosting machine: 69% </li>
</ul>

The random forest classifier was also tested with the dataframe that contained both the Deeploc dataset and the original Yamagishi nuclear protein dataset. The accuracy score for this test was 89%. 

## PSSM-CNN and PSSM-RNN Models

When coupled with PSSM data, the CNN and RNN models were able to parse out patterns from the NLS signals and fairly reliably predict them. However, their accuracy was lower than using the random forest classifier: 

<ul>
    <li> When only nuclear proteins were used as input, the average accuracy between five folds for cross-validation (ten epochs each) was 91.36%. </li>
    <li> However, we expanded the input data to include the more comprehensive DeepLoc dataset, which includes signals for both the nucleus and other organelles, the overall accuracy dropped to 73.62%. There may have been confirmation bias in the model stemming from the first dataset that may have skewed the accuracy results. On the other hand, when the CNN model was trained with the Deeploc data, the accuracy was 91%, but dropped to 74% when the Yamagishi dataset was used for validation. </li>
    <li> The LSTM model used the complete dataset with similar settings and obtained an accuracy score of 85.45%. </li>
</ul>

# Nuclear classification / NLS sequence parsing tool

We have also produced a simple NLS predictor based off of DeepLoc that uses the Logomaker package to generate a graph showing the likelihood of each amino acid contributing to a NLS if the queried protein is classified as "nuclear".  This tool can be found in the Python file "app.py". PSSM scores are generated for the queried protein and then the random forest classifier (see further details below) is used to determine whether or not the queried protein meets the requirements of being a nuclear protein. If determined to be nuclear, Logomaker is used to construct a graph showing the likelihood of each amino acid possibly contributing to a NLS motif based on its PSSM scores.

# Future Directions

<ul>
    <li> Use a graph convolutional network to incorporate node embeddings of graphs generated from contact maps (showing interactions between amino acids) from 3-D structures to see if this affects the likelihood of having a NLS sequence. These node embeddings of graphs would be used as a feature as well as PSSM data and one-hot encoded NLS motifs. </li>
    <li> Use the BERT (Bidirectional Encoded Representations from Transformers) natural language processing model, specifically tailored for amino acid sequences, to predict for presence of a NLS. This can either be a binary or multi-label classification. </li>
</ul>



# Citations
<ol>
    <li> DeepLoc 2.0: multi-label subcellular localization prediction using protein language models.
    Vineet Thumuluri, Jose Juan Almagro Armenteros, Alexander Rosenberg Johansen, Henrik Nielsen, Ole Winther.
    Nucleic Acids Research, Web server issue 2022. </li>
    <li> Kinjo AR, Nakamura H (2008) Nature of Protein Family Signatures: Insights from Singular Value Analysis of Position-Specific Scoring Matrices. PLoS ONE 3(4): e1963. https://doi.org/10.1371/journal.pone.0001963 </li>
    <li> Yamagishi R, Kaneko H. Data from comprehensive analysis of nuclear localization signals. Data Brief. 2015 Dec 12;6:200-3. doi: 10.1016/j.dib.2015.11.064. PMID: 26862559; PMCID: PMC4707185. </li>
    <li> Ismail, Md, and Md Nazrul Islam Mondal. "Extreme Gradient Boost with CNN: A Deep Learning-Based Approach for Predicting Protein Subcellular Localization." Proceedings of the International Conference on Big Data, IoT, and Machine Learning: BIM 2021. Singapore: Springer Singapore, 2021. </li>
    <li> Elnaggar A, Heinzinger M, Dallago C, Rehawi G, Wang Y, Jones L, Gibbs T, Feher T, Angerer C, Steinegger M, Bhowmik D, Rost B. ProtTrans: Toward Understanding the Language of Life Through Self-Supervised Learning. IEEE Trans Pattern Anal Mach Intell. 2022 Oct;44(10):7112-7127. doi: 10.1109/TPAMI.2021.3095381. Epub 2022 Sep 14. PMID: 34232869. </li>
</ol>