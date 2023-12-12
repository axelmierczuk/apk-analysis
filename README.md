# Dynamic and Static Analysis for APK Analysis

## Table of Contents
1. [Overview](#overview)
2. [Dataset](#dataset)
3. [Models](#models)
4. [Results](#results)
   * [XGBoost](#xgboost)
   * [Decision Tree](#decision-tree)
   * [SVM Classifier](#svm-classifier)
   * [Summary](#summary)
5. [Future Work](#future-work)
6. [References](#references)

## Overview

This project is about analyzing APK files for potential threats or malware. We make use of both static and dynamic analysis methods in order to get a thorough understanding of each APK sample. The datasets used in this project are collected from publicly available sources, preprocessed, and then utilized to train machine learning models. 

The models used include XGBoost Classifier, Decision Tree Classifier with Ada Boost, and Support Vector Classifier (SVC), all optimized using Grid Search to fine-tune the parameters. The performance of these models is outlined in great detail in the Results section.

In future work, we aim to improve the dataset by utilizing all available samples, while also enhancing the features extracted from both dynamic and static analysis for better model performance.

## Dataset

Note: Will not be uploading raw samples used for building CSVs in `dataset`. These can be found at the following locations:

- https://www.unb.ca/cic/datasets/maldroid-2020.html
- https://www.unb.ca/cic/datasets/andmal2017.html

Building a dataset was required due to challenges around finding an adequate dataset with both dynamic and static features.
Raw APKs were collected from “CIC-AndMal2017” [1] and “CICMalDroid 2020” [2] (as listed above).
The dynamic analysis dataset is based on syscalls at run-time, and gathered using the project “Automated APK Tracing” [3].
On the other hand, the static dataset based on a variety of features extracted using Androguard [4].

The full dataset used to train models can be found at `dataset/dataset-dynamic-static-joined.csv`. The dataset found in the CSV 
is actually a subset of all the samples from the “CIC-AndMal2017” and “CICMalDroid 2020” samples. The main reason for this is
due to the amount of time it takes to run dynamic analysis.

Below is a summary of the data in the dataset:

![data_distribution.png](images%2Fdata_distribution.png)

| Datapoint               | Result                                |
|-------------------------|---------------------------------------|
| APK Types               | Adware, Ransomware, Scareware, Benign |
| Dataset Size            | 1,357                                 |
| Malicious Samples       | 220 (16.2%)                           |
| Benign Samples          | 1,137 (83.8%)                         |
| Total Available Samples | 22,832                                |


## Models

The following models were trained:

- XGBoost Classifier
- Decision Tree Classifier boosted with Ada Boost
- Support Vector Classifier (SVC)

For each model, Grid Search was used to optimize parameters.


Best parameters for the `XGBoost Classifier` were:

- Column Sample By Tree - 0.6
- Gamma - 1 
- Max Depth - 5 
- Min Child Weight - 1 
- Sub-sample - 0.8

Best parameters for the `Decision Tree` were:

- Criterion - Gini
- Max Depth - 6
- Min Samples Leaf - 5
- Min Samples Split - 90

Best parameters for the `SVC` were:

- C - 10
- Gamma - 0.0001
- Kernel - Radial Basis Function



## Results

### XGBoost

|                  | **Precision**      | **Recall**         | **F1-Score**       |
|------------------|--------------------|--------------------|--------------------|
| **Benign**       | 0.9786324786324786 | 0.9913419913419913 | 0.9849462365591398 | 
| **Malicious**    | 0.9473684210526315 | 0.8780487804878049 | 0.9113924050632912 | 
| **Accuracy**     | 0.9742647058823529 | 0.9742647058823529 | 0.9742647058823529 | 
| **Macro Avg**    | 0.9630004498425551 | 0.9346953859148981 | 0.9481693208112155 | 
| **Weighted Avg** | 0.9739198817178694 | 0.9742647058823529 | 0.9738590781351332 |

![feature_importance_xgb.png](images%2Ffeature_importance_xgb.png)

### Decision Tree

|                  | **Precision**      | **Recall**         | **F1-Score**       |
|------------------|--------------------|--------------------|--------------------|
| **Benign**       | 0.9663865546218487 | 0.9956709956709957 | 0.9808102345415779 |
| **Malicious**    | 0.9705882352941176 | 0.8048780487804879 | 0.8800000000000001 |
| **Accuracy**     | 0.9669117647058824 | 0.9669117647058824 | 0.9669117647058824 |
| **Macro Avg**    | 0.9684873949579832 | 0.9002745222257418 | 0.930405117270789  |
| **Weighted Avg** | 0.9670198961937717 | 0.9669117647058824 | 0.9656145741878842 |


![feature_importance_dt.png](images%2Ffeature_importance_dt.png)

### SVM Classifier

|                  | **Precision**      | **Recall**         | **F1-Score**       |
|------------------|--------------------|--------------------|--------------------|
| **Benign**       | 0.875              | 1.0                | 0.9333333333333333 |
| **Malicious**    | 1.0                | 0.1951219512195122 | 0.326530612244898  |
| **Accuracy**     | 0.8786764705882353 | 0.8786764705882353 | 0.8786764705882353 |
| **Macro Avg**    | 0.9375             | 0.5975609756097561 | 0.6299319727891157 |
| **Weighted Avg** | 0.8938419117647058 | 0.8786764705882353 | 0.8418667466986794 |


### Summary

![summary_benign.png](images%2Fsummary_benign.png)

![summary_malicious.png](images%2Fsummary_malicious.png)

## Future Work

- Improve dataset by using all 22,832 samples in order to reduce over-fitting.
- Improve dynamic analysis features extracted / collected for more balanced feature weights and potential model improvements.
- Improve static analysis features extracted / collected for potential model improvements.

## References

[1] CIC, "CICAndMal2017 Dataset," University of New Brunswick's Canadian Institute for Cybersecurity. [Online]. Available: https://www.unb.ca/cic/datasets/andmal2017.html.

[2] CIC, "CICMalDroid 2020 Dataset," University of New Brunswick's Canadian Institute for Cybersecurity. [Online]. Available: https://www.unb.ca/cic/datasets/maldroid-2020.html.

[3] R. Khoury, "Automated APK Tracing," GitHub Repository. [Online]. Available: https://github.com/RaphaelKhoury/automatedapk-tracing.

[4] Androguard, “Androguard/androguard: Reverse engineering and Pentesting for Android Applications,” GitHub, https://github.com/androguard/androguard
