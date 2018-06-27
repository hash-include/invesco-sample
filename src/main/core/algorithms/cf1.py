# http://blog.ethanrosenthal.com/2015/11/02/intro-to-collaborative-filtering/

from sklearn.metrics import mean_squared_error
import numpy as np

from src.main.core.algorithms import txnmat


class CF1(object):
    def __init__(self, month=None):
        self.iid2idx = dict()
        self.iid2idx = dict()
        self.idx2iid = dict()
        self.aid2idx = dict()
        self.idx2aid = dict()
        self.n_users = -1
        self.n_items = -1
        self.month = month
        self.__load()

    def __get_mse(self, pred, actual):
        # Ignore nonzero terms.
        pred = pred[actual.nonzero()].flatten()
        actual = actual[actual.nonzero()].flatten()
        return mean_squared_error(pred, actual)

    def __measure_sparsity(self, mat):
        sparsity = float(len(mat.nonzero()[0]))
        sparsity /= (mat.shape[0] * mat.shape[1])
        sparsity *= 100
        return 'Sparsity: {:4.2f}%'.format(sparsity)

    def __train_test_split(self, datamat, size=2):
        test = np.zeros(datamat.shape)
        train = datamat.copy()
        for user in range(datamat.shape[0]):
            non_zeros = datamat[user, :].nonzero()[0]
            if (len(non_zeros) > size):
                test_ratings = np.random.choice(datamat[user, :].nonzero()[0], size=size, replace=False)
                train[user, test_ratings] = 0.
                test[user, test_ratings] = datamat[user, test_ratings]

        # Test and training are truly disjoint
        assert (np.all((train * test) == 0))
        return train, test

    def __fast_similarity(self, datamat, kind='user', epsilon=1e-9):
        # epsilon -> small number for handling dived-by-zero errors
        if kind == 'user':
            sim = datamat.dot(datamat.T) + epsilon
        elif kind == 'item':
            sim = datamat.T.dot(datamat) + epsilon
        norms = np.array([np.sqrt(np.diagonal(sim))])
        return (sim / norms / norms.T)

    def __predict_slow_simple(self, datamat, similarity, kind='user'):
        pred = np.zeros(datamat.shape)
        if kind == 'user':
            for i in range(datamat.shape[0]):
                for j in range(datamat.shape[1]):
                    pred[i, j] = similarity[i, :].dot(datamat[:, j]) \
                                 / np.sum(np.abs(similarity[i, :]))
            return pred
        elif kind == 'item':
            for i in range(datamat.shape[0]):
                for j in range(datamat.shape[1]):
                    pred[i, j] = similarity[j, :].dot(datamat[i, :].T) \
                                 / np.sum(np.abs(similarity[j, :]))

            return pred

    def __predict_fast_simple(self, ratings, similarity, kind='user'):
        if kind == 'user':
            return similarity.dot(ratings) / np.array([np.abs(similarity).sum(axis=1)]).T
        elif kind == 'item':
            return ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])

    def __print_data(self, matrix, message):
        print("\n")
        print("Dataset: " + message)
        print("Shape: " + str(matrix.shape))
        print("Sparsity: " + str(self.__measure_sparsity(matrix)))
        print("First 5 rows: ")
        print(matrix[:5, ])
        print("\n")

    def __load_index_map(self, df):
        self.iids = list(df.columns[1:])
        for idx, iid in enumerate(self.iids):
            self.iid2idx[iid] = idx
            self.idx2iid[idx] = iid

        self.aids = list(df.index)
        for idx, aid in enumerate(self.aids):
            self.aid2idx[aid] = idx
            self.idx2aid[idx] = aid

        self.n_users = len(self.aids)
        self.n_items = len(self.iids)

    def __load(self):
        df = txnmat.compute_cfmat(month=self.month)
        self.__load_index_map(df)
        ratings = df.as_matrix(df.columns[1:])

        # print_data(ratings, "Ratings matrix")
        train, test = self.__train_test_split(ratings)
        # print_data(train, "Training Matrix")
        # print_data(test, "Testing Matrix")

        user_similarity = self.__fast_similarity(ratings)
        item_similarity = self.__fast_similarity(ratings, kind='item')

        # print_data(user_similarity, "User Similarity Matrix")
        # print_data(item_similarity, "Item Similarity Matrix")

        self.item_prediction = self.__predict_fast_simple(train, item_similarity, kind='item')
        self.user_prediction = self.__predict_fast_simple(train, user_similarity, kind='user')

        print('User-based CF MSE: ' + str(self.__get_mse(self.user_prediction, test)))
        print('Item-based CF MSE: ' + str(self.__get_mse(self.item_prediction, test)))
        # print_data(item_prediction, "Item Pred")
        # print_data(user_prediction, "User Pred")

    def get_value(self, aid, iid, algorithm='user'):
        if aid in self.aid2idx:
            aid_idx = self.aid2idx[aid]
        else:
            return -1

        if iid in self.iid2idx:
            iid_idx = self.iid2idx[iid]
        else:
            return -1

        value = -1
        if algorithm == 'user':
            value = self.user_prediction[aid_idx][iid_idx]
        elif algorithm == 'item':
            value = self.item_prediction[aid_idx][iid_idx]
        else:
            print("Invalid algorithm input provided.")
        return value


if __name__ == '__main__':
    pass
