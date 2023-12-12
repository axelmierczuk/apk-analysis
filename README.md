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

This research presents a comprehensive approach to analyzing Android Package Kits (APKs) using both dynamic and static analysis methods. The primary objective is to identify and categorize APKs into various types, including adware, ransomware, scareware, and benign applications. The study utilizes a dataset derived from the CIC-AndMal2017 and CICMalDroid 2020 datasets, enriched with dynamic and static features. Dynamic analysis is performed based on system calls at runtime, while static analysis involves extracting features using Androguard. The paper discusses the process of dataset creation, challenges faced, and the reasons for selecting a subset of the available samples. Various machine learning models such as XGBoost, Decision Tree, and SVM Classifier have been trained and optimized to classify the APKs, and their performance is evaluated and compared. The research also outlines future directions for enhancing the dataset and refining the analysis methods.


## Dataset

The dataset, crucial to this research, was constructed due to challenges in finding comprehensive datasets encompassing both dynamic and static features of APKs. Raw APKs were sourced from “CIC-AndMal2017” [1] and “CICMalDroid 2020” [2]. The dynamic analysis dataset is based on system calls during runtime, gathered using “Automated APK Tracing” [3]. Conversely, the static dataset comprises various features extracted via Androguard [4]. The final dataset, a subset of all samples from the aforementioned sources, is available in the CSV format and encompasses 1,357 samples, with a focus on balancing between malicious (220 samples) and benign (1,137 samples) APKs.


_Note: Will not be uploading raw samples used for building CSVs in `dataset`. These can be found at the following locations:_

- _https://www.unb.ca/cic/datasets/maldroid-2020.html_
- _https://www.unb.ca/cic/datasets/andmal2017.html_


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

The study employs three machine learning models: XGBoost Classifier, Decision Tree Classifier augmented with Ada Boost, and Support Vector Classifier (SVC). Each model underwent a rigorous parameter optimization process using Grid Search, resulting in the identification of the most effective parameters for classification accuracy.


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
|                  | **Precision** | **Recall** | **F1-Score** |
|------------------|---------------|------------|--------------|
| **Benign**       | 0.978632      | 0.991341   | 0.984946     | 
| **Malicious**    | 0.947368      | 0.878048   | 0.911392     | 
| **Accuracy**     | 0.974264      | 0.974264   | 0.974264     | 
| **Macro Avg**    | 0.963000      | 0.934695   | 0.948169     | 
| **Weighted Avg** | 0.973919      | 0.974264   | 0.973859     |

![feature_importance_xgb.png](images%2Ffeature_importance_xgb.png)

### Decision Tree

|                  | **Precision** | **Recall** | **F1-Score** |
|------------------|---------------|------------|--------------|
| **Benign**       | 0.966386      | 0.995670   | 0.980810     |
| **Malicious**    | 0.970588      | 0.804878   | 0.880000     |
| **Accuracy**     | 0.966911      | 0.966911   | 0.966911     |
| **Macro Avg**    | 0.968487      | 0.900274   | 0.930405     |
| **Weighted Avg** | 0.967019      | 0.966911   | 0.965614     |


![feature_importance_dt.png](images%2Ffeature_importance_dt.png)

### SVM Classifier

|                  | **Precision** | **Recall** | **F1-Score** |
|------------------|---------------|------------|--------------|
| **Benign**       | 0.875000      | 1.000000   | 0.933333     |
| **Malicious**    | 1.000000      | 0.195121   | 0.326530     |
| **Accuracy**     | 0.878676      | 0.878676   | 0.878676     |
| **Macro Avg**    | 0.937500      | 0.597560   | 0.629931     |
| **Weighted Avg** | 0.893841      | 0.878676   | 0.841866     |


### Summary

![summary_benign.png](images%2Fsummary_benign.png)

![summary_malicious.png](images%2Fsummary_malicious.png)

## Future Work

- Capture network traffic and implement features.
- Review opportunities for unsupervised learning, which may lead to lineage inferencing.
- Improve dataset by using all 22,832 samples in order to reduce over-fitting.
- Improve dynamic analysis features extracted / collected for more balanced feature weights and potential model improvements.
- Improve static analysis features extracted / collected for potential model improvements.


## References

[1] CIC, "CICAndMal2017 Dataset," University of New Brunswick's Canadian Institute for Cybersecurity. [Online]. Available: https://www.unb.ca/cic/datasets/andmal2017.html.

[2] CIC, "CICMalDroid 2020 Dataset," University of New Brunswick's Canadian Institute for Cybersecurity. [Online]. Available: https://www.unb.ca/cic/datasets/maldroid-2020.html.

[3] R. Khoury, "Automated APK Tracing," GitHub Repository. [Online]. Available: https://github.com/RaphaelKhoury/automatedapk-tracing.

[4] Androguard, “Androguard/androguard: Reverse engineering and Pentesting for Android Applications,” GitHub, https://github.com/androguard/androguard

