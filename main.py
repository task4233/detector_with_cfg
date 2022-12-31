from detector_with_cfg import converter


def main():
    all_apis_path = 'cfg_builder/output/allApis.json'
    api_freqs_path = 'cfg_builder/output/apiFrequencies.json'
    api_usages_path = 'output/api_usages.json'
    api_frequencies_path = 'output/api_frequencies.json'

    api_usages, api_frequences = converter.Covnerter(
        all_apis_path,
        api_freqs_path,
        api_usages_path,
        api_frequencies_path,
    ).convert()

    # 説明変数と目的変数に分ける
    # 説明変数: (API Usage, API Frequency, API Sequence)
    # 目的変数: (benign/malicious)
    # 学習とテスト用データセットに分割する
    # 決定木モデルの作成と予測

if __name__ == '__main__':
    main()
