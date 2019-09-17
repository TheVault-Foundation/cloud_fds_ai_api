import pandas as pd 
from imblearn.under_sampling import RandomUnderSampler
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import itertools
import matplotlib.pyplot as plt
import numpy as np

from sklearn.linear_model import LogisticRegression

from nltk.probability import FreqDist

import random
 



class logisticRegression:
    
    def __init__(self, transaction):
        self.class_name = ['not_fraud', 'fraud']

    def Counter(self, array):
        fdist = FreqDist(array)

        return fdist.most_common(2)


    def plot_confusion_matrix(self, classes, pred, y_test, 
                            normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
        
        cm = confusion_matrix(y_test, pred)
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=0)
        plt.yticks(tick_marks, classes)
        
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, cm[i, j],
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black")

    
    def getScore(self):
        credit_data = pd.read_csv('../datafiles/creditcard.csv')
        X = credit_data.drop(['Class'], axis=1)
        y = credit_data['Class']
        print(self.Counter(y))	# {0: 284315, 1: 492}

        # Under Sampling
        # sampler = RandomUnderSampler(ratio=0.70, random_state=0)
        # X, y = sampler.fit_sample(X, y)
        # print('Class : ', self.Counter(y))	# {0: 702, 1: 492}

        model = LogisticRegression()
        model.fit(X, [1, -1])
        pred_outlier = model.predict(y)
        print(pred_outlier)

        # 평가
        print('confusion matrix\n', confusion_matrix(pred_outlier, y))
        print('Accuracy: ',accuracy_score(pred_outlier, y))
        print('classification_report\n', classification_report(pred_outlier, y))
        self.plot_confusion_matrix(self.class_name, pred_outlier, y, title='Logistic Regression')

        return random.randint(0, 100)



if __name__ == "__main__":
    fds = logisticRegression('')

    score = fds.getScore()

    print(score)