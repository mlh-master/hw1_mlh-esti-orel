# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:14:23 2019

@author: smorandv
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def rm_ext_and_nan(CTG_features, extra_feature):

    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A dictionary of clean CTG called c_ctg
    """
    c_ctg = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    CTG_features_nan = CTG_features.copy()
    del CTG_features_nan[extra_feature]

    for col in CTG_features_nan:
        CTG_features_nan[col] = pd.to_numeric(CTG_features_nan[col], errors='coerce')
        c_ctg[col]= CTG_features_nan[col].dropna()
    # --------------------------------------------------------------------------
    return c_ctg


def nan2num_samp(CTG_features, extra_feature):
    """
    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A pandas dataframe of the dictionary c_cdf containing the "clean" features
    """
    c_cdf = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    del CTG_features[extra_feature]

    for col in CTG_features:
        a = pd.to_numeric(CTG_features[col], errors='coerce')
        bank_for_col = a.dropna()
        bank_for_col = np.random.choice(bank_for_col, size=len(a))
        c_cdf[col] = a.fillna(pd.Series(bank_for_col))


    # -------------------------------------------------------------------------
    return pd.DataFrame(c_cdf)


def sum_stat(c_feat):
    """
    :param c_feat: Output of nan2num_cdf
    :return: Summary statistics as a dicionary of dictionaries (called d_summary) as explained in the notebook
    """
    d_summary ={}

    for col in c_feat.columns:
        dic = {}
       # dic['min','Q1','median','Q3','max']=c_feat[col].describe(include='min','Q1','median','Q3','max')
        dic['min'] = c_feat[col].describe()['min']
        dic['Q1'] = c_feat[col].describe()['25%']
        dic['median'] = c_feat[col].describe()['50%']
        dic['Q3'] = c_feat[col].describe()['75%']
        dic['max'] = c_feat[col].describe()['max']
        d_summary[col] = dic
    return d_summary


def rm_outlier(c_feat, d_summary):
    """

    :param c_feat: Output of nan2num_cdf
    :param d_summary: Output of sum_stat
    :return: Dataframe of the dictionary c_no_outlier containing the feature with the outliers removed
    """
    c_no_outlier = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    pd_c_feat = pd.DataFrame(c_feat)
    for col_names, col_dictionary in d_summary.items():
        q1 = col_dictionary['Q1']
        q3 = col_dictionary['Q3']
        step = 1.5 * (q3 - q1)
        LF = q1 - step
        UF = q3 + step
        # for column in pd_c_feat[col_names]
        values = pd_c_feat[col_names]
        for index, value in enumerate(values, 1):
            if value < LF or value > UF:
                values[index] = np.nan
        c_no_outlier[col_names] = values
    # -------------------------------------------------------------------------
    return pd.DataFrame(c_no_outlier)


def phys_prior(c_cdf, feature, thresh):
    """

    :param c_cdf: Output of nan2num_cdf
    :param feature: A string of your selected feature
    :param thresh: A numeric value of threshold
    :return: An array of the "filtered" feature called filt_feature
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:-----------------------------
    cols = [feature]
    filt_feature = c_cdf[c_cdf[cols] <= thresh][cols]
    filt_feature = filt_feature.dropna()

    # -------------------------------------------------------------------------
    return filt_feature


def norm_standard(CTG_features, selected_feat=('LB', 'ASTV'), mode='none', flag=False):
    """

    :param CTG_features: Pandas series of CTG features
    :param selected_feat: A two elements tuple of strings of the features for comparison
    :param mode: A string determining the mode according to the notebook
    :param flag: A boolean determining whether or not plot a histogram
    :return: Dataframe of the normalized/standardazied features called nsd_res
    """
    x, y = selected_feat
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------

    # -------------------------------------------------------------------------
    return pd.DataFrame(nsd_res)
