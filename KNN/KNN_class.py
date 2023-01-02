import numpy as np
from sklearn.utils import shuffle
from collections import Counter
from sklearn import datasets


def metric_choice(choice):
    return choice   # ta funkcja nic nie wnosi

def menu(options):
    options = list(options.items())
    print("Wybierz odpowiedni numer.")
    while True:
        for ind, option in enumerate(options, start=1):
            print("{}. {}".format(ind, option[0]))
        try:
            choice = int(input("Podaj numer: "))
            return choice
        except ValueError:
            pass  # pusty except wymaga komentarza

def accuracy(predicted_list, actual_list):
    correct_predictions = 0
    for i in range(len(predicted_list)):  # nie dałoby się uniknąć tej pętli?
        if (predicted_list[i] == actual_list[i]):
            correct_predictions += 1
    return correct_predictions/len(predicted_list)

def euclides_metric(x, y):
    sum = 0  # przesłonięcie symbolu wbudowanego
    try:
        for i in range(len(x)):  # nie dałoby się uniknąć tej pętli?
            sum += pow((y[i] - x[i]), 2)
        return np.sqrt(sum)
    except:  # zamienił stryjek siekierkę na kijek - wyjątek jest lepszą sygnalizacją błędu niż print
        print("Not allowed")

def taxi_metric(x, y):
    sum = 0
    try:
        for i in range(len(x)):
            sum += np.abs((y[i] - x[i]))
        return sum
    except:
        print("Not allowed")

def max_metric(x, y):
    distance_list=[]
    try:
        for i in range(len(x)):
            distance_list.append(np.abs((y[i] - x[i])))
        return max(distance_list)
    except:
        print("Not allowed")

def cosine_metric(x, y):
    return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))  # 1-


class KNN:

    def __init__(self, k):
        self.k = k
        self.X_train=[]  # lista?
        self.Y_train = []


    def train(self, X, Y):
        self.X_train.extend(X)
        self.Y_train.extend(Y)


    def predict(self, X_test):

        predictions = []

        m = menu({"Euklidesowa": (metric_choice, 1, {}),
          "Taksówkowa": (metric_choice, (2), {}),
          "Maksimum": (metric_choice, (3), {}),
          "Cosinusowa": (metric_choice, (4), {})
          })

        for x_tst in X_test:
            distance_list = []
            for x_trn in self.X_train:
                if m==1:  # polecam słownik
                    distance = euclides_metric(x_tst, x_trn)
                elif m==2:
                    distance = taxi_metric(x_tst, x_trn)
                elif m==3:
                    distance = max_metric(x_tst, x_trn)
                elif m==4:
                    distance = cosine_metric(x_tst, x_trn)
                distance_list.extend([distance])

            index_dst = np.argsort(distance_list)
            distances_knn = index_dst[:self.k]
            knn = [self.Y_train[i] for i in distances_knn]
            predicted = Counter(knn).most_common()
            predictions.append(predicted[0][0])

        return predictions

if __name__=="__main__":

    iris = datasets.load_iris()
    index_list = [i for i in range(len(iris.data))]
    new_index_list = shuffle(index_list)

    X, y = [iris.data[i] for i in new_index_list], [iris.target[i] for i in new_index_list]

    X_train = X[0: 90]
    y_train = y[0: 90]
    X_predict = X[90:]
    y_predict = y[90:]

    knn3=KNN(3)
    knn5=KNN(5)
    knn8=KNN(8)

    knn3.train(X_train, y_train)
    knn5.train(X_train, y_train)
    knn8.train(X_train, y_train)

    knn3_results = knn3.predict(X_predict)
    knn5_results = knn5.predict(X_predict)
    knn8_results = knn8.predict(X_predict)


    print("Predicted for k=3: ", knn3_results)
    print("Predicted for k=5: ", knn5_results)
    print("Predicted for k=8: ", knn8_results)
    print("Actual: ", list(y_predict))

    print("Predicted for k=3: ", accuracy(knn3_results, y_predict))
    print("Predicted for k=5: ", accuracy(knn5_results, y_predict))
    print("Predicted for k=8: ", accuracy(knn8_results, y_predict))
