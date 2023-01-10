from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import plot_tree
from detector_with_cfg import converter, gea
from sklearn.tree import plot_tree
import re
import traceback
import matplotlib
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import metrics

import copy

import json
matplotlib.use('TkAgg')


class Classifier:
    def __init__(self, depth: int) -> None:
        self.all_apis_path = 'cfg_builder/output/allApis.json'
        self.api_freqs_path = 'cfg_builder/output/apiFrequencies.json'
        self.api_seqs_path = 'cfg_builder/output/apiSequences.json'
        self.api_usages_path = 'output/api_usages.json'
        self.api_frequencies_path = 'output/api_frequencies.json'
        self.api_sequences_path = 'output/api_sequences.json'

        self.depth = depth
        print(f"depth of decision tree is {self.depth}")

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
        # classify with API Usage
        self.__classify("API Usage", self.api_usages)
        self.__classify_with_gea("API Usage", self.api_usages)

        # classify with API Frequency
        self.__classify("API Frequency", self.api_freqs)
        self.__classify_with_gea("API Frequency", self.api_freqs)
        print("done classify")

    def __classify(self, name: str, data: list):
        print(f"start __classify for {name}")

        for column in data:
            for cell in column:
                cell = re.sub('[^A-Za-z0-9_]+', '_', str(cell))

        df = pd.DataFrame(data[1:], columns=data[0])
        df = df.replace([None, 'Nan', 'None', ''], 0)

        # 説明変数と目的変数に分ける
        # 説明変数: (API Usage, API Frequency, API Sequence)
        # 目的変数: (benign/malicious)
        df_x = df.iloc[:, :-1]
        df_y = df.iloc[:, -1]
        print(f"df: {df.shape}, df_x: {df_x.shape}, df_y: {df_y.shape}")

        # 学習とテスト用データセットに分割する
        train_x, test_x, train_y, test_y = train_test_split(
            df_x, df_y, random_state=1)

        # 決定木モデルの作成
        model = tree.DecisionTreeClassifier(
            max_depth=self.depth, random_state=1)
        # model = lightgbm.LGBMRegressor()
        model.fit(train_x, train_y)

        # 予測
        pred_y = model.predict(test_x)
        score = model.score(test_x, test_y)
        print(f"score({name}): {score}")

        plt.figure(figsize=(15, 10))
        plot_tree(model, feature_names=train_x.columns,
                  class_names=True, filled=True)
        plt.savefig(f"{name}_{self.depth}.pdf")

        self.__drawing_confusion_matrix(test_y, pred_y, name)
        self.__calculation_evaluations(test_y, pred_y)

        # check with gea
        # geaデータの用意
        # test_yと同じ数だけ用意する
        geas = []
        g = gea.GEA()
        for i in range(len(test_y)):
            gg = None
            if "API Usage" in name:
                gg = g.generate_with_api_usages(self.api_usages[1:])
            elif "API Frequency" in name:
                gg = g.generate_with_api_freqs(self.api_freqs[1:])
            else:
                print(f"invalid name: {name}")
                assert False
            geas.append(gg)

        df_gea = pd.DataFrame(geas, columns=data[0])
        df_gea = df_gea.replace([None, 'Nan', 'None', ''], 0)
        print(f"df_gea: {df_gea.shape}")
        df_gea_x = df_gea.iloc[:, :-1]
        df_gea_y = df_gea.iloc[:, -1]

        # 予測
        pred_y = model.predict(df_gea_x)

        plt.figure(figsize=(100, 100))
        plot_tree(model, feature_names=df_gea.columns,
                  class_names=True, filled=True)
        plt.savefig(f"{name}_gea_{self.depth}.pdf")

        self.__drawing_confusion_matrix(df_gea_y, pred_y, name)
        self.__calculation_evaluations(df_gea_y, pred_y)

    # TODO: adversarial training
    def __classify_with_gea(self, name: str, data: list, model=None):
        print(f"start __classify_with_gea for {name}")

        for column in data:
            for cell in column:
                cell = re.sub('[^A-Za-z0-9_]+', '_', str(cell))

        # check with gea
        geas = []
        changed_num = int(len(data) * 0.7)-1  # -1 is for column names
        g = gea.GEA()
        for i in range(changed_num):
            gg = None
            if "API Usage" in name:
                gg = g.generate_with_api_usages(self.api_usages[1:])
            elif "API Frequency" in name:
                gg = g.generate_with_api_freqs(self.api_freqs[1:])
            else:
                print(f"invalid name: {name}")
                assert False
            geas.append(gg)

        # column_names(index: 0) + data
        new_data = geas + data[changed_num:]
        try:
            df = pd.DataFrame(new_data, columns=data[0])
            df = df.replace([None, 'Nan', 'None', ''], 0)
        except Exception as e:
            traceback.print_exc()

        # 説明変数と目的変数に分ける
        # 説明変数: (API Usage, API Frequency, API Sequence)
        # 目的変数: (benign/malicious)
        df_x = df.iloc[:, :-1]
        df_y = df.iloc[:, -1]
        print(f"df: {df.shape}, df_x: {df_x.shape}, df_y: {df_y.shape}")

        # 学習とテスト用データセットに分割する
        train_x, test_x, train_y, test_y = train_test_split(
            df_x, df_y, random_state=1)

        # 決定木モデルの作成
        model = tree.DecisionTreeClassifier(
            max_depth=self.depth, random_state=1)
        # model = lightgbm.LGBMRegressor()
        model.fit(train_x, train_y)

        # 予測
        pred_y = model.predict(test_x)
        score = model.score(test_x, test_y)
        print(f"score({name}): {score}")

        plt.figure(figsize=(100, 100))
        plot_tree(model, feature_names=train_x.columns,
                  class_names=True, filled=True)
        plt.savefig(f"{name}_{self.depth}.pdf")

        self.__drawing_confusion_matrix(test_y, pred_y, name)
        self.__calculation_evaluations(test_y, pred_y)

        df_gea = pd.DataFrame(geas, columns=data[0])
        df_gea = df_gea.replace([None, 'Nan', 'None', ''], 0)
        print(f"df_gea: {df_gea.shape}")
        df_gea_x = df_gea.iloc[:, :-1]
        df_gea_y = df_gea.iloc[:, -1]

        # 予測
        pred_y = model.predict(df_gea_x)

        plt.figure(figsize=(15, 10))
        plot_tree(model, feature_names=df_gea.columns,
                  class_names=True, filled=True)
        plt.savefig(f"{name}_gea_{self.depth}.pdf")

        self.__drawing_confusion_matrix(df_gea_y, pred_y, name)
        self.__calculation_evaluations(df_gea_y, pred_y)

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
        plt.savefig(f"{name}_confusion_matrix_gea_{self.depth}.pdf")

    def __calculation_evaluations(self, y: pd.Series, pre: np.ndarray) -> None:
        print(f'Acc(GEA): {metrics.accuracy_score(y, pre)}')
        print(f'Pre(GEA): {metrics.precision_score(y, pre)}')
        print(f'Rec(GEA): {metrics.recall_score(y, pre)}')
