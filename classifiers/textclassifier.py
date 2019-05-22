import pandas as pd
import nltk
import re
import string as STRING

removePunct = False

def formatsent(sent):
    exclude = set(STRING.punctuation)
    if removePunct:
        exclude.remove("'")
        s = ''.join(ch for ch in sent if ch not in exclude)
        return s.lower()
    else:
        pattern = re.compile('\W ')
        string = re.sub(pattern, '', sent)
        string = string.lower()
        # print(string)
        return string.lower()

def dialogue_act_features(sent):
    features = {}
    formattedsent = formatsent(sent)
    for word in nltk.word_tokenize(formattedsent):
        features['contains({})'.format(word.lower())] = True
    return features

def getsets(data):
    featuresets = []
    for i, row in data.iterrows():
        sent = row[0]
        senttype = row[4]
        featuresets.append((dialogue_act_features(sent), senttype))
    return featuresets

def getdata_5050(filename):
    data = pd.read_csv(filename, header=None, usecols=[0, 4])
    data.sample(frac=1)

    col2 = data.iloc[:, 1]
    counts = col2.value_counts().tolist()
    # print(counts)
    numqs = counts[1]

    data.sort_values(by=[4], inplace=True, ascending=False)

    qs = data[:numqs]
    nqs = data[numqs:]

    size = int(numqs * 0.8)

    train_set = pd.concat([qs[:size], nqs[:size]])
    test_set = pd.concat([qs[size:numqs], nqs[size:numqs]])

    return train_set.sample(frac=1), test_set.sample(frac=1)

def getdata(filename):
    data = pd.read_csv(filename, header=None, usecols=[0,4])
    data.sample(frac=1)

    size = int(data.shape[0] * 0.8)
    train_set = data[size:]
    test_set = data[:size]

    return train_set, test_set

def getdatastats(data):
    # totallen = data.shape[0]
    col2 = data.iloc[:,1]
    counts = col2.value_counts()
    return counts

# def train_maxent_classifier(train_set):
#     print ("training classifier")
#     classifier = nltk.MaxentClassifier.train(train_set, trace=0)
#     print ("done training")
#
#     return classifier

def train_classifier(train_set, classifier, name):
    print("training", name, "classifier")
    trained = classifier.train(train_set) #, trace=0)
    print("done training")

    return trained

def print5inset(test_set):
    i = 0
    for s in test_set:
        if i < 5:
            print(s)
        else:
            break
        i += 1

def testclassifier(classifier, test_set):
    # print5inset(test_set)

    acc = nltk.classify.accuracy(classifier, test_set)
    print ("ACCURACY:", acc)

    return acc

def reportacc(train_set, test_set, classifier, name):
    print("Remove Punct:", removePunct, "\n")

    classifier = train_classifier(train_set, classifier, name)
    testclassifier(classifier, test_set)

def main():
    global removePunct
    removePunct = True

    train_set, test_set = getdata_5050("../audiofiles/sentdata/sents.csv")

    # train_set, test_set = getdata("../audiofiles/sentdata/sents.csv")

    # print("\nDATA:")
    # print(train_set.head())
    # print("train size:", train_set.shape)
    # print(test_set.head())
    # print("test size:", test_set.shape)

    print("\nTRAIN SET INFO:")
    print(getdatastats(train_set))
    print("\nTEST SET INFO:")
    print(getdatastats(test_set))

    print()

    train_set = getsets(train_set)
    test_set = getsets(test_set)

    for sent in train_set[:2]:
        print(sent)
    print()

    reportacc(train_set, test_set, nltk.MaxentClassifier, "maxent")
    # reportacc(train_set, test_set, nltk.NaiveBayesClassifier, "naive bayes")
    # reportacc(train_set, test_set, nltk.DecisionTreeClassifier, "decision tree")

    # classifier = train_maxent_classifier(train_set)
    # classifier = train_classifier(train_set, nltk.MaxentClassifier, "maxent")
    # testclassifier(classifier, test_set)
    # print("\nMAXENT ACCURACY:",testclassifier(classifier, test_set))

    # classifier = train_classifier(train_set, nltk.NaiveBayesClassifier, "naive bayes")
    # testclassifier(classifier, test_set)
    # print("\nMAXENT ACCURACY:", testclassifier(classifier, test_set))

if __name__=="__main__":
    main()
