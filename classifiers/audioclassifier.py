import numpy
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def getdatastats(data):
    col2 = data.iloc[:,-1]
    counts = col2.value_counts()
    return counts

def getdata(filename):
    data = pd.read_csv(filename, header=None)
    data.sample(frac=1)
    return data

def getdata_5050(filename):
    data = pd.read_csv(filename, header=None)
    data.sample(frac=1)
    # print(data)

    col2 = data.iloc[:, -1]
    counts = col2.value_counts().tolist()
    # print("cts:",counts)
    numqs = counts[1]

    data.sort_values(by=[13], inplace=True, ascending=False)

    qs = data[:numqs]
    nqs = data[numqs:2*numqs]

    fulldata = pd.concat([qs, nqs])
    return fulldata

def getsplitdata():
    # data = getdata("../audiodata/audios.csv")
    data = getdata_5050("../audiodata/audios.csv")
    print(getdatastats(data))

    data = data.values
    np.random.shuffle(data)

    X = data[:, 0:-2]
    X = X.astype('float')

    y = data[:, -1]
    y = y.astype('int')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def getclassifierstats(clf, X_train, X_test, y_train, y_test):
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    return score

def main():
    X_train, X_test, y_train, y_test = getsplitdata()

    print()

    # clf = linear_model.SGDClassifier(max_iter=1000, tol=1e-3)
    # print("SGDC:\t", getclassifierstats(clf, X_train, X_test, y_train, y_test))

    # clf = GaussianNB(priors=None, var_smoothing=1e-5)
    # print("GNB:\t", getclassifierstats(clf, X_train, X_test, y_train, y_test))

    # clf = linear_model.LinearRegression()
    # print("LinReg:\t", getclassifierstats(clf, X_train, X_test, y_train, y_test))

    # clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state = 0)
    # print("RFC:\t", getclassifierstats(clf, X_train, X_test, y_train, y_test))

    # scores_dtc = []
    # for i in range(50):
    #     scores_dtc.append(getclassifierstats(DecisionTreeClassifier(random_state=i), X_train, X_test, y_train, y_test))
    # maximum = max(scores_dtc)
    # print("DTC:\t", maximum, "\t i:", scores_dtc.index(maximum))

    # scores_rfc = []
    # for i in range(10, 110, 10):
    #     scores_rfc.append(getclassifierstats(RandomForestClassifier(n_estimators=i,max_depth=3,random_state=26), X_train, X_test, y_train, y_test))
    # maximum = max(scores_rfc)
    # max_n = (scores_rfc.index(maximum)*10)+10
    # print("RFC n_estimators:\t", maximum, "\t n:", max_n)
    #
    # scores_rfc = []
    # for i in range(1, 10):
    #     scores_rfc.append(getclassifierstats(RandomForestClassifier(n_estimators=max_n, max_depth=i, random_state=26), X_train, X_test, y_train, y_test))
    # maximum = max(scores_rfc)
    # max_d = (scores_rfc.index(maximum)) + 1
    # print("RFC max_depth:\t\t", maximum, "\t d:", max_d)
    #
    # scores_rfc = []
    # for i in range(1, 50):
    #     scores_rfc.append(getclassifierstats(RandomForestClassifier(n_estimators=max_n, max_depth=max_d, random_state=i), X_train,
    #                            X_test, y_train, y_test))
    # maximum = max(scores_rfc)
    # max_r = (scores_rfc.index(maximum)) + 1
    # print("RFC random_state:\t", maximum, "\t r:", max_r)

    scores_rfc = []
    maximum = -1
    pos = 0
    ct = 0
    for n in range(10, 90, 10):
        for d in range(2, 8):
            for r in range(1, 30):
                score = getclassifierstats(RandomForestClassifier(n_estimators=n, max_depth=d, random_state=r), X_train, X_test, y_train, y_test)
                vals = [score, n, d, r]
                scores_rfc.append(vals)

                print(vals)

                if score > maximum:
                    maximum = score
                    pos = ct
                ct += 1

    print("\nMAX: ", scores_rfc[pos])

    # maxval = scores_rfc[0][0]
    # pos = 0
    # for i in range(len(scores_rfc)):
    #     score = scores_rfc[i]
    #     if score[0] > maxval:
    #         maxval = score[0]
    #         pos = i
    #
    # print("max:", scores_rfc[pos])

if __name__=="__main__":
    main()
