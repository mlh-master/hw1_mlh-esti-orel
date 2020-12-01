import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold as SKFold
from sklearn.metrics import log_loss
from sklearn.linear_model import LogisticRegression
import pandas as pd
import scipy.stats as stats
from clean_data import norm_standard as nsd


def pred_log(logreg, X_train, y_train, X_test, flag=False):
    """

    :param logreg: An object of the class LogisticRegression
    :param X_train: Training set samples
    :param y_train: Training set labels 
    :param X_test: Testing set samples
    :param flag: A boolean determining whether to return the predicted he probabilities of the classes (relevant after Q11)
    :return: A two elements tuple containing the predictions and the weightning matrix
    """


#X_train_nsd = nsd(X_train, ('LB', 'AC'), mode='standard')
 #   X_test_nsd = nsd(X_test, ('LB', 'AC'), mode='standard')
    logreg.fit(X_train, y_train)
    y_pred_log = logreg.predict(X_test)
   # y_pred_log += 1
    w_log = logreg.coef_
  #  w_log = pd.DataFrame(w_log, columns=X_train.columns)

# y_pred_test_lin = lin_reg.predict(X_test)

    # ---------------------------------------------------------------
    #gt_array = [y_train, y_test]  # ground truth
    #pred_array = [y_pred_train_lin, y_pred_test_lin]  # predictions
    #plot_gt_vs_pred(gt_array, pred_array)
    return y_pred_log, w_log


def w_no_p_table(w, features):
    x = np.arange(len(features))
    width = 0.5  # the width of the bars
    mode_name = ['Normal', 'Suspect', 'Pathology']
    fig, axs = plt.subplots(figsize=(20, 10), nrows=3)
    for idx, ax in enumerate(axs):
        ax.bar(x, w[idx, :], width)
        ax.set(xticks=x, xticklabels=features, ylabel='w', title=mode_name[idx])
    fig.tight_layout()
    plt.show()


def w_all_tbl(w2, w1, orig_feat):
    idx_l2 = np.argsort(-w2, axis=1)
    w2_sort = -np.sort(-w2, axis=1)
    w1_sort = np.zeros(w2_sort.shape)
    mode_name = ['Normal', 'Suspect', 'Pathology']
    lbl = ['L2', 'L1']
    col = ['orange', 'green']
    feature_dict = {}
    for i in range(w2_sort.shape[0]):
        w1_sort[i, :] = w1[i, idx_l2[i, :]]
        feature_dict[mode_name[i]] = [orig_feat[x] for x in idx_l2[i, :]]
    width = 0.4
    w_tot = [w2_sort, w1_sort]
    fig, axs = plt.subplots(figsize=(20, 10), nrows=3)
    x_orig = np.arange(len(orig_feat))
    x = np.arange(len(orig_feat)) - width/2
    for idx_w, w in enumerate(w_tot):
        for idx_ax, ax in enumerate(axs):
            ax.bar(x, w[idx_ax, :], width, label=lbl[idx_w], color=col[idx_w])
            ax.set(xticks=x_orig, xticklabels=feature_dict[mode_name[idx_ax]], ylabel='w', title=mode_name[idx_ax])
            ax.legend()
        x += width
    fig.tight_layout()
    plt.show()


def cv_kfold(X, y, C, penalty, K, mode):
    """
    
    :param X: Training set samples
    :param y: Training set labels 
    :param C: A list of regularization parameters
    :param penalty: A list of types of norm
    :param K: Number of folds
    :param mode: Mode of normalization (parameter of norm_standard function in clean_data module)
    :return: A dictionary as explained in the notebook
    """
    kf = SKFold(n_splits=K)
    validation_dict = []
    for c in C:
        for p in penalty:
            logreg = LogisticRegression(solver='saga', penalty=p, C=c, max_iter=10000, multi_class='ovr')
            loss_val_vec = np.zeros(K)
            k = 0
            for train_idx, val_idx in kf.split(X, y):
                x_train, x_val = X.iloc[train_idx], X.iloc[val_idx]
        # ------------------ IMPLEMENT YOUR CODE HERE:-----------------------------

        x_train_fold, x_val_fold = X_train[train_idx, :], X_train[val_idx, :]
        x_train_fold = (x_train_fold).fit
        x_val_fold = (x_val_fold).fit
        J_train_fold[h] = log_loss(y_train_fold, y_pred_train)
        y_pred_val = log_reg.predict_proba(x_val_fold)
        J_val_fold[h] = log_loss(y_val_fold, y_pred_val)

    return validation_dict


def odds_ratio(w, X, selected_feat='LB'):
    """

    :param w: the learned weights of the non normalized/standardized data
    :param x: the set of the relevant features-patients data
    :param selected_feat: the current feature
    :return: odds: median odds of all patients for the selected feature and label
             odds_ratio: the odds ratio of the selected feature and label
    """
   i = X.columns.get_loc(selected_feat)
   odds_ratio = np.exp(w[i])
   w_T=np.transpose(w)
   X_T=np.transpose(X)
   odds_pre= 1/(np.exp(-(w_T@ X_T)))
   odds=odds_pre.median

    return odds, odd_ratio