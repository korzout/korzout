import math
import string
class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha
        self.wordsdict = {}
        self.labelsdict = {}
        self.wordset = set()
        self.labelset = set()

    def clean(self, s):
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator).lower()

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        
        for i in range(len(X)):
            print(X[i])
            title = self.clean(X[i])
            label = y[i]
            self.labelset.add(label)
            if label not in self.labelsdict.keys():
                self.labelsdict[label] = 1
            else:
                self.labelsdict[label] += 1
            for word in title:
                self.wordset.add(word)

                if word not in self.wordsdict.keys():
                    self.wordsdict[word] = dict()
                if label not in self.wordsdict[word].keys():
                    self.wordsdict[word][label] = 1
                else:
                    self.wordsdict[word][label] += 1


    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        prediction = []
        words_quanity = len(self.wordset)

        for title in X:
            max_probability = 0
            best_label  = None
            for label in self.labelset:
                current_probability = self.labelsdict[label] / sum(self.labelsdict.values())
                for word in title.split():
                    if word not in self.wordsdict.keys():
                        self.wordsdict[word] = dict()
                    current_probability = current_probability * (self.wordsdict[word].get(label,0) + self.alpha) / (sum(self.wordsdict[word].values()) + self.alpha * words_quanity)
                if current_probability > max_probability:
                    max_probability = current_probability
                    best_label = label
            prediction.append(best_label)
        return prediction
    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        prediction = self.predict(X_test)
        succeed = 0
        quanity = len(y_test)
        for i in range(len(prediction)):
            succeed += (prediction[i] == y_test[i])
        return succeed/quanity