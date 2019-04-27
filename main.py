import warnings
warnings.filterwarnings("ignore") # might want to remove later

from tensorflow import keras
import joblib

import speechrec
import texttyping
from Else import lstm


def test_speech(classifier):
    speech1 = "is this a question"
    speech2 = "this is a statement"

    print(speech1, ":", speechrec.get_prediction(classifier, speech1))
    print(speech2, ":", speechrec.get_prediction(classifier, speech2))

def classify_speech(classifier, speech):
    return speechrec.get_prediction(classifier, speech)

def predictaudio(mic, classifier):
    sound, speech = speechrec.from_mic(mic)
    print(speech, ":", classify_speech(classifier, speech))

def eval_classifiers(maxentclass, lstmclass):
    train_set, test_set = texttyping.getdata5050()
    print ("maxent classifier:\t",texttyping.testclassifier(maxentclass, test_set))

    X_train, X_test, y_train, y_test = lstm.getdata5050()
    print ("lstm classifier:\t", lstm.eval_model(lstmclass, X_test, y_test))

if __name__ == "__main__":
    # from_mic()
    # speech, stats = from_file("audiofiles/mic-results.wav")
    # print(speech)
    # printparams(stats)

    # classifier = texttyping.trainclassifier()

    print("ORIGINAL CLASSIFIER ACCURACY:")

    filename = "classifiers/maxentclassifier.joblib"
    maxent_classifier = joblib.load(filename)

    filename = "classifiers/lstm.h5"
    lstm_classifier = keras.models.load_model(filename)

    eval_classifiers(maxent_classifier, lstm_classifier)

    print("EQUAL Q/NQ CLASSIFIER ACCURACY:")

    filename = "classifiers/maxentclassifier_eq.joblib"
    maxent_classifier = joblib.load(filename)

    filename = "classifiers/lstm_eq.h5"
    lstm_classifier = keras.models.load_model(filename)

    eval_classifiers(maxent_classifier, lstm_classifier)

    # test_speech(classifier)

    # r = sr.Recognizer()
    #
    # while (True):
    #     predictaudio(r, classifier)

    # speech1 = "is this also a longer question"
    # speech2 = "might this be a question"
    # speech3 = "this is another statement"
    # speech4 = "I don't care"

    # print(speech1, ":", classify_speech(classifier, speech1))
    # print(speech2, ":", classify_speech(classifier, speech2))
    # print(speech3, ":", classify_speech(classifier, speech3))
    # print(speech4, ":", classify_speech(classifier, speech4))
