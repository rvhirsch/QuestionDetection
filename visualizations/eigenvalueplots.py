import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

#     textfile = "../audiofiles/sentdata/sents.csv"

def getaudiodata(audiofile):
    # X = np.loadtxt(audiofile, delimiter=',', usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)) # 14 cols total
    X = np.loadtxt(audiofile, delimiter=',', usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)) # 14 cols total
    y = np.loadtxt(audiofile, delimiter=',', usecols=(13)) # 14 cols total
    return X, y

def splitposneg(X, y):
    xpos = []
    xneg = []
    ypos = []
    yneg = []
    for i in range(len(y)):
        if y[i] == 1:
            xpos.append(X[i])
            ypos.append(y[i])
        else:
            xneg.append(X[i])
            yneg.append(y[i])

    return xpos, ypos, xneg, yneg

def PCA2D(x, y):
    pca = PCA(n_components=3)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data=principalComponents, columns=['PC 1', 'PC 2', 'PC 3'])

    finalDf = pd.concat([principalDf, pd.DataFrame(data=y, columns=['target'])], axis=1)
    print(finalDf.head(20))

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title('2 Component PCA', fontsize=20)

    targets = [0.0, 1.0]
    colors = ['r', 'b']
    for target, color in zip(targets, colors):
        indicesToKeep = finalDf['target'] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'PC 1'],
                   finalDf.loc[indicesToKeep, 'PC 2'],
                   c=color, s=50)
    ax.legend(["Non-Question", "Question"])
    ax.grid()

    plt.xlim((-1000, 4000))
    plt.ylim((-1000, 4000))

    plt.show()

def PCA3D(x, y):
    pca = PCA(n_components=10)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data=principalComponents) #, columns=['PC 1', 'PC 2', 'PC 3'])
    principalDf.columns = ["PC " + str(x) for x in range(1, len(principalDf.columns)+1)]

    finalDf = pd.concat([principalDf, pd.DataFrame(data=y, columns=['target'])], axis=1)
    print(finalDf.head(20))

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_zlabel('Principal Component 6', fontsize=15)
    ax.set_title('3 Component PCA', fontsize=20)

    targets = [0.0, 1.0]
    colors = ['r', 'b']
    for target, color in zip(targets, colors):
        indicesToKeep = finalDf['target'] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'PC 1'],
                   finalDf.loc[indicesToKeep, 'PC 2'],
                   finalDf.loc[indicesToKeep, 'PC 3'],
                   c=color, s=50)
    ax.legend(["Non-Question", "Question"])
    ax.grid()

    # plt.xlim((-1000, 4000))
    # plt.ylim((-1000, 4000))
    # plt.z((-1000, 4000))

    plt.show()

def main():
    audiofile = "../audiodata/audios.csv"
    X, y = getaudiodata(audiofile)
    # xpos, ypos, xneg, yneg = splitposneg(X, y)

    # PCA2D(X, y)
    PCA3D(X, y)


if __name__=="__main__":
    main()