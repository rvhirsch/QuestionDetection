import numpy
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

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
    # print(getdatastats(data))

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

def runmulti(clf, name):
    print(name, "\n")
    scores = []
    for i in range(30):
        X_train, X_test, y_train, y_test = getsplitdata() # grab new data for each iter

        score = getclassifierstats(clf, X_train, X_test, y_train, y_test)
        scores.append(score)
        print(score)
    print(name, "avg:\t", sum(scores)/len(scores), "\n")

def main():

    # clf = linear_model.SGDClassifier(loss='squared_hinge', max_iter=1000, tol=1e-3) # DONE
    # runmulti(clf, "SGD")

    # clf = GaussianNB(priors=None, var_smoothing=1e-9) # DONE
    # runmulti(clf, "GNB")

    # clf = linear_model.LinearRegression() # DONE
    # runmulti(clf, "LinReg")

    clf = linear_model.LogisticRegression(solver='liblinear', max_iter=1500) # DONE
    runmulti(clf, "LogReg")

    # clf = RandomForestClassifier(n_estimators=90, max_depth=5) #, random_state = 0) # DONE
    # runmulti(clf, "RFC")

    # clf = DecisionTreeClassifier(max_depth=5, splitter="random")  # DONE
    # runmulti(clf, "DTC")

    # clf = KNeighborsClassifier(n_neighbors=25) # DONE
    # runmulti(clf, "KNC")

    # X_train, X_test, y_train, y_test = getsplitdata()

    # scores_rfc = []
    # maximum = -1
    # pos = 0
    # ct = 0
    # for n in range(10, 90, 10):
    #     for d in range(2, 8):
    #         for r in range(1, 30):
    #             score = getclassifierstats(RandomForestClassifier(n_estimators=n, max_depth=d, random_state=r), X_train, X_test, y_train, y_test)
    #             vals = [score, n, d, r]
    #             scores_rfc.append(vals)
    #
    #             # print(vals)
    #
    #             if score > maximum:
    #                 maximum = score
    #                 pos = ct
    #             ct += 1

    # print("\nMAX: ", scores_rfc[pos], "\n")

    # vals = scores_rfc[pos]
    # clf = RandomForestClassifier(n_estimators=vals[1], max_depth=vals[2], random_state=vals[3])

if __name__=="__main__":
    main()
