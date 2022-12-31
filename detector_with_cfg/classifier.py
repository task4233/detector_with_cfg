from sklearn import tree
from sklearn.model_selection import train_test_split
from detector_with_cfg import converter

import pandas as pd

class Classifier:
    def __init__(self) -> None:
        self.all_apis_path = 'cfg_builder/output/allApis.json'
        self.api_freqs_path = 'cfg_builder/output/apiFrequencies.json'
        self.api_usages_path = 'output/api_usages.json'
        self.api_frequencies_path = 'output/api_frequencies.json'

        self.api_usages, self.api_freqs = converter.Covnerter(
            self.all_apis_path,
            self.api_freqs_path,
            self.api_usages_path,
            self.api_frequencies_path,
        ).convert()

    def classify(self):
        self.__classify("API Usage", self.api_usages)
        self.__classify("API Frequency", self.api_freqs)
    
    def __classify(self, name: str, data: list):
        df = pd.DataFrame(data[1:], columns=data[0])

        # 説明変数と目的変数に分ける
        # 説明変数: (API Usage, API Frequency, API Sequence)
        # 目的変数: (benign/malicious)
        df_x = df[data[0][:-1]]
        df_y = df[data[0][-1]]

        # 学習とテスト用データセットに分割する
        train_x, test_x, train_y, test_y = train_test_split(df_x, df_y, random_state=1)
        
        # 決定木モデルの作成
        model = tree.DecisionTreeClassifier(max_depth=2, random_state=1)
        model.fit(train_x, train_y)

        # 予測
        model.predict(test_x)
        score = model.score(test_x, test_y)
        print(f"score({name}): {score}")