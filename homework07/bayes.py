from collections import Counter
from math import log


class NaiveBayesClassifier:
    def __init__(self, alpha=1):
        self.alpha = alpha
        self.classes = []
        self.classes_p = {}
        self.counters = {}
        self.count_words = {}

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        self.classes = list(set(y))
        for c in self.classes:
            self.classes_p[c] = y.count(c) / len(y)

        self.counters = {c: Counter() for c in self.classes}

        for x, target in zip(X, y):
            words = x.split(" ")
            self.counters[target].update(words)

        self.count_words = {c: sum(counter.values()) for c, counter in self.counters.items()}

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        predicts = []
        for msg in X:
            keys_res = {}

            for key in self.classes:
                keys_res[key] = log(self.classes_p[key])

            for key in self.classes:
                words = msg.split(" ")
                for word in words:
                    keys_res[key] += log(
                        (self.counters[key][word] + self.alpha)
                        / (self.count_words[key] + len(self.count_words) * self.alpha)
                    )

            max_prob = max(keys_res.values())
            predict = [k for k, v in keys_res.items() if v == max_prob][0]
            predicts.append(predict)

        return predicts

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        predicts = self.predict(X_test)
        same_results = sum(1 for pred, true in zip(predicts, y_test) if pred == true)
        return same_results / len(X_test)
