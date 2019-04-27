import nltk
from random import shuffle
from joblib import dump, load
from sklearn.neural_network import MLPClassifier

# feature extractor to check what words text contains
def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

# get count of sentences of various types
def count_types(featuresets):
    senttypes = {}
    for f in featuresets:
        typ = f[1]
        if typ in senttypes.keys():
            senttypes[typ] += 1
        else:
            # print ("TYPES:",senttypes)
            senttypes[typ] = 1
    return senttypes

# set of (sentence words, sentence type)
# specifies binary sentence types - statement or question
def getsets(posts):
    # featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
    featuresets = []
    for post in posts:
        realtype = post.get("class")
        if realtype == "whQuestion" or realtype == "ynQuestion":
            senttype = "Question"
        else:
            senttype = "Statement"

        featuresets.append((dialogue_act_features(post.text), senttype))
    return featuresets

def getdata():
    # print ("gathering train/test data")
    posts = nltk.corpus.nps_chat.xml_posts() #[:100000]
    featuresets = getsets(posts)

    shuffle(featuresets)

    size = int(len(featuresets) * 0.2)
    train_set, test_set = featuresets[size:], featuresets[:size]

    # print("len train:",len(train_set))
    # print("len test:",len(test_set))

    return train_set, test_set

def getdata5050():
    # print ("gathering train/test data")
    posts = nltk.corpus.nps_chat.xml_posts() #[:100000]
    featuresets = getsets(posts)

    shuffle(featuresets)

    numqs, numnonqs = getdatastats(posts)

    qs = nqs = []
    for post in featuresets:
        realtype = post[1]
        if realtype == "whQuestion" or realtype == "ynQuestion":
            if len(qs) < numqs:
                qs.append(post)
        else:
            if len(nqs) < numqs:
                nqs.append(post)

    train_set = qs[:(numqs*3)//4] + nqs[:(numqs*3)//4]
    test_set = qs[(numqs*3)//4:] + nqs[(numqs*3)//4:]

    # print("len train:",len(train_set))
    # print("len test:",len(test_set))

    return train_set, test_set

def getdatastats(posts):
    # posts = nltk.corpus.nps_chat.xml_posts()
    totallen = len(posts)
    # print ("total posts:", totallen)

    numqs = 0
    for post in posts:
        realtype = post.get("class")
        if realtype == "whQuestion" or realtype == "ynQuestion":
            numqs += 1
    # print("numQs:", numqs)
    # print("num non-Qs:", totallen - numqs)

    return numqs, totallen-numqs

def train_maxent_classifier(train_set, test_set):
    print ("training classifier")
    classifier = nltk.MaxentClassifier.train(train_set, trace=0)
    print ("done training")

    return classifier

def testclassifier(classifier, test_set):
    acc = nltk.classify.accuracy(classifier, test_set)
    # print ("ACCURACY:", acc)
    return acc

def make_classifier():
    train_set, test_set = getdata()

    classifier = train_maxent_classifier(train_set, test_set)
    filename = "classifiers/maxentclassifier.joblib"
    dump(classifier, filename)

    train_seteq, test_seteq = getdata5050()

    classifiereq = train_maxent_classifier(train_set, test_set)
    filename = "classifiers/maxentclassifier_eq.joblib"
    dump(classifiereq, filename)

    return classifier, classifiereq, test_set, test_seteq

def main():
    # getdatastats()

    maxentclassifier, maxentclassifier_eq, test_set, test_seteq = make_classifier()

    print ("Original Accuracy:\t", testclassifier(maxentclassifier, test_seteq)) # 0.9375
    print ("Equal Parts Acc:\t", testclassifier(maxentclassifier_eq, test_seteq)) # 0.9887711672552748

if __name__ == "__main__":
    main()
