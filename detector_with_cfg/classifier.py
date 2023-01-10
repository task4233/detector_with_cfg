from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import plot_tree
from detector_with_cfg import converter
from sklearn.tree import plot_tree
import re
import matplotlib
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import metrics

import json
matplotlib.use('TkAgg')

class Classifier:
    def __init__(self) -> None:
        self.all_apis_path = 'cfg_builder/output/allApis.json'
        self.api_freqs_path = 'cfg_builder/output/apiFrequencies.json'
        self.api_seqs_path = 'cfg_builder/output/apiSequences.json'
        self.api_usages_path = 'output/api_usages.json'
        self.api_frequencies_path = 'output/api_frequencies.json'
        self.api_sequences_path = 'output/api_sequences.json'

        self.depth = 4

        # self.api_usages, self.api_freqs = converter.Covnerter(
        #     self.all_apis_path,
        #     self.api_freqs_path,
        #     self.api_seqs_path,
        #     self.api_usages_path,
        #     self.api_frequencies_path,
        #     self.api_sequences_path
        # ).convert()

        with open(self.api_usages_path, 'r') as f:
          self.api_usages = json.load(f)
        
        with open(self.api_frequencies_path, 'r') as f:
          self.api_freqs = json.load(f)

    def classify(self):
        print("start classify")
        self.__classify("API Usage", self.api_usages)
        self.__classify("API Frequency", self.api_freqs)
        print("done classify")

    def __classify(self, name: str, data: list):
        print(f"start __classify for {name}")

        for column in data:
            for cell in column:
                cell = re.sub('[^A-Za-z0-9_]+', '_', str(cell))
        
        df = pd.DataFrame(data[1:], columns=data[0])

        # 説明変数と目的変数に分ける
        # 説明変数: (API Usage, API Frequency, API Sequence)
        # 目的変数: (benign/malicious)
        df_x = df[data[0][:-1]]
        df_y = df[data[0][-1]]

        # 学習とテスト用データセットに分割する
        train_x, test_x, train_y, test_y = train_test_split(
            df_x, df_y, random_state=1)

        # 決定木モデルの作成
        model = tree.DecisionTreeClassifier(max_depth=self.depth, random_state=1)
        # model = lightgbm.LGBMRegressor()
        model.fit(train_x, train_y)

        # 予測
        pred_y = model.predict(test_x)
        score = model.score(test_x, test_y)
        print(f"score({name}): {score}")

        plt.figure(figsize=(15, 10))
        plot_tree(model, feature_names=train_x.columns, class_names=True, filled=True)
        plt.savefig(f"{name}_{self.depth}.pdf")

        self.__drawing_confusion_matrix(test_y, pred_y, name)
        self.__calculation_evaluations(test_y, pred_y)


    # ref: https://qiita.com/satoichi/items/88e9034a01c206a478ea
    def __drawing_confusion_matrix(self, y: pd.Series, pre: np.ndarray, name: str) -> None: 
        confmat = confusion_matrix(y, pre)
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.matshow(confmat, cmap=plt.cm.Blues, alpha=0.3)
        for i in range(confmat.shape[0]):
            for j in range(confmat.shape[1]):
                ax.text(x=j, y=i, s=confmat[i, j], va='center', ha='center')
        plt.title('Predicted value')
        plt.ylabel('Measured value')
        plt.rcParams["font.size"] = 15
        plt.tight_layout() 
        plt.savefig(f"{name}_confusion_matrix_{self.depth}.pdf")

    def __calculation_evaluations(self, y: pd.Series, pre: np.ndarray) -> None:
        print('Acc: {:.3f}'.format(metrics.accuracy_score(y, pre)))
        print('Pre: {:.3f}'.format(metrics.precision_score(y, pre)))
        print('Rec: {:.3f}'.format(metrics.recall_score(y, pre)))