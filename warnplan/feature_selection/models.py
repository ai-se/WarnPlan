from __future__ import print_function, division

from pdb import set_trace

import numpy as np
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression


class Wrapper:
    def __init__(self): pass

    @classmethod
    def rfe_select(cls, tbl):
        """
        Sort features based on recursive feature elemintaion
        """
        clf = LogisticRegression()
        rfe = RFE(clf, n_features_to_select=15)
        numerical_columns = [col for col in tbl.columns if col not in ["F21", "F20", "F54", "Name"]]
        features = tbl[numerical_columns[:-1]]
        klass = tbl[tbl.columns[-1]]
        rfe = rfe.fit(features, klass)
        selected_features = [feat for selected, feat in zip(rfe.support_, numerical_columns) if selected]
        selected_features.insert(0, "Name")
        selected_features.append("category")
        new_tbl = tbl[selected_features]

        return new_tbl


class CBFS:
    """
    Fast Correlation-Based Filter (FCBF) algorithm as described in "Feature Selection for High-Dimensional Data: A Fast
    Correlation-Based Filter Solution". Yu & Liu (ICML 2003)
    """

    def __init__(self):
        pass

    @classmethod
    def _entropy(cls, vec, base=2):
        " Returns the empirical entropy H(X) in the input vector."
        _, vec = np.unique(vec, return_counts=True)
        prob_vec = np.array(vec / float(sum(vec)))
        if base == 2:
            logfn = np.log2
        elif base == 10:
            logfn = np.log10
        else:
            logfn = np.log
        return prob_vec.dot(-logfn(prob_vec))

    @classmethod
    def _conditional_entropy(cls, x, y):
        " Returns H(X|Y)."
        uy, uyc = np.unique(y, return_counts=True)
        prob_uyc = uyc / float(sum(uyc))
        cond_entropy_x = np.array([cls._entropy(x[y == v]) for v in uy])
        return prob_uyc.dot(cond_entropy_x)

    @classmethod
    def _mutual_information(cls, x, y):
        " Returns the information gain/mutual information [H(X)-H(X|Y)] between two random vars x & y."
        return cls._entropy(x) - cls._conditional_entropy(x, y)

    @classmethod
    def _symmetrical_uncertainty(cls, x, y):
        " Returns 'symmetrical uncertainty' (SU) - a symmetric mutual information measure."
        return 2.0 * cls._mutual_information(x, y) / (cls._entropy(x) + cls._entropy(y))

    @classmethod
    def _get_first_element(cls, d):
        """
        Returns tuple corresponding to first 'unconsidered' feature

        Parameters:
        ----------
        d : ndarray
            A 2-d array with SU, original feature index and flag as columns.

        Returns:
        -------
        a, b, c : tuple
            a - SU value, b - original feature index, c - index of next 'unconsidered' feature
        """

        t = np.where(d[:, 2] > 0)[0]
        if len(t):
            return d[t[0], 0], d[t[0], 1], t[0]
        return None, None, None

    @classmethod
    def _get_next_element(cls, d, idx):
        """
        Returns tuple corresponding to the next 'unconsidered' feature.

        Parameters:
        -----------
        d : ndarray
            A 2-d array with SU, original feature index and flag as columns.
        idx : int
            Represents original index of a feature whose next element is required.

        Returns:
        --------
        a, b, c : tuple
            a - SU value, b - original feature index, c - index of next 'unconsidered' feature
        """
        t = np.where(d[:, 2] > 0)[0]
        t = t[t > idx]
        if len(t):
            return d[t[0], 0], d[t[0], 1], t[0]
        return None, None, None

    @classmethod
    def _remove_element(cls, d, idx):
        """
        Returns data with requested feature removed.

        Parameters:
        -----------
        d : ndarray
            A 2-d array with SU, original feature index and flag as columns.
        idx : int
            Represents original index of a feature which needs to be removed.

        Returns:
        --------
        d : ndarray
            Same as input, except with specific feature removed.
        """
        d[idx, 2] = 0
        return d

    @classmethod
    def _c_correlation(cls, X, y):
        """
        Returns SU values between each feature and class.

        Parameters:
        -----------
        X : 2-D ndarray
            Feature matrix.
        y : ndarray
            Class label vector

        Returns:
        --------
        su : ndarray
            Symmetric Uncertainty (SU) values for each feature.
        """
        su = np.zeros(X.shape[1])
        for i in np.arange(X.shape[1]):
            su[i] = cls._symmetrical_uncertainty(X[:, i], y)
        return su

    @classmethod
    def feature_selection(cls, tbl, thresh=-1):
        """
        Perform Fast Correlation-Based Filter solution (FCBF).

        Parameters:
        -----------
        X : 2-D ndarray
        	Feature matrix
        y : ndarray
        	Class label vector
        thresh : float
        	A value in [0,1) used as threshold for selecting 'relevant' features.
        	A negative value suggest the use of minimum SU[i,c] value as threshold.

        Returns:
        --------
        sbest : 2-D ndarray
        	An array containing SU[i,c] values and feature index i.
        """

        numerical_columns = [col for col in tbl.columns if col not in ["F21", "F20", "F54", "Name"]]
        X = tbl[numerical_columns[:-1]].values
        y = tbl[numerical_columns[-1]].values

        n = X.shape[1]
        slist = np.zeros((n, 3))
        slist[:, -1] = 1

        # identify relevant features
        slist[:, 0] = cls._c_correlation(X, y)  # compute 'C-correlation'
        idx = slist[:, 0].argsort()[::-1]
        slist = slist[idx,]
        slist[:, 1] = idx
        if thresh < 0:
            thresh = np.median(slist[-1, 0])
            print("Using minimum SU value as default threshold: {0}".format(thresh))

        slist = slist[slist[:, 0] > thresh, :]  # desc. ordered per SU[i,c]

        "Identify redundant features among the relevant ones"
        cache = {}
        m = len(slist)
        p_su, p, p_idx = cls._get_first_element(slist)
        for i in xrange(m):
            q_su, q, q_idx = cls._get_next_element(slist, p_idx)
            if q:
                # p, q = int(p), int(q)
                while q:
                    if (p, q) in cache:
                        pq_su = cache[(p, q)]
                    else:
                        pq_su = cls._symmetrical_uncertainty(X[:, int(p)], X[:, int(q)])
                        cache[(p, q)] = pq_su

                    if pq_su >= q_su:
                        slist = cls._remove_element(slist, q_idx)
                    q_su, q, q_idx = cls._get_next_element(slist, q_idx)

            p_su, p, p_idx = cls._get_next_element(slist, p_idx)
            if not p_idx:
                break

        sbest = slist[slist[:, 2] > 0, :2]
        print("\n#Features selected: {0}".format(len(sbest)))
        print("Selected feature indices:\n{0}".format(sbest))
        set_trace()
        return sbest
