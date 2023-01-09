import json
import glob
import os
import traceback


class Covnerter():
    def __init__(
        self,
        all_apis_path: str,
        api_freqs_path: str,
        api_seqs_path: str,
        api_usages_path: str,
        api_frequencies_path: str,
        api_sequences_path: str
    ) -> None:
        self.all_apis_path = all_apis_path
        self.api_freqs_path = api_freqs_path
        self.api_seqs_path = api_seqs_path
        self.api_usages_path = api_usages_path
        self.api_frequencies_path = api_frequencies_path
        self.api_sequences_path = api_sequences_path

        self.__family_key = "a05cba79-d480-44ad-8a41-1447d544d1b"
        pass

    def convert(
        self,
    ):
        try:
            self.__validate_paths()
            self.__load_jsons()
            self.__convert()
            self.__save_jsons()
            return self.api_usages, self.api_frequencies
        except Exception:
            traceback.print_exc()

    def __convert(self) -> None:
        """
        make one-hot vector from universal set of all apis in given APKs.
        """
        all_apis_list = list(self.all_apis.keys())
        all_apis_list.append('family')

        self.api_usages = [all_apis_list]
        self.api_frequencies = [all_apis_list]
        for api_freq in self.api_freqs:
            # 各APKのAPI_USAGE listを作る
            family = 0

            api_usage = [0] * len(self.all_apis)
            api_frequency = [0] * len(self.all_apis)
            for api_name, occurrences in api_freq.items():
                if api_name == self.__family_key:
                    family = occurrences
                    continue

                # api_usage_idx
                api_usage_idx = self.all_apis[api_name]
                api_usage[api_usage_idx] = 1
                api_frequency[api_usage_idx] = occurrences

            # 末尾に目的変数を付与
            api_usage.append(family)
            api_frequency.append(family)

            # 全体にappend
            self.api_usages.append(api_usage)
            self.api_frequencies.append(api_frequency)

    def __load_jsons(self) -> None:
        print("start load_json for all_apis")
        # all_apis:  Map<String, Integer> <=> Map<api_name, api_number>
        # api_number is 0-indexed
        self.all_apis = {}

        prefix = self.all_apis_path + "."
        files = sorted(glob.glob(prefix+"*"))

        max_idx = 0
        for file in files:
            with open(file, 'r') as f:
                print(f"loading {f.name}")
                dd = json.load(f)
            if dd.values() is None or len(dd.values()) == 0:
                continue
            for v in dd.values():
                v += max_idx
            max_idx = max(dd.values())
            self.all_apis.update(dd)
        print("done load_json for all_apis")

        print("start load_json for api_freqs")
        # api_freqs: List<Map<String, Integer>> <=> List<Map<api_name, occurrences>>
        prefix = self.api_freqs_path + "."
        files = sorted(glob.glob(prefix+"*"))

        self.api_freqs = []
        for file in files:
            with open(file, 'r') as f:
                dd_list = json.load(f)
            self.api_freqs += dd_list
        print("done load_json for api_freqs")

        print("start load_json for all_sequence")
        # api_seqs: List<List<String>> <=> List<List<api_name>>
        prefix = self.api_seqs_path + "."
        files = sorted(glob.glob(prefix+"*"))

        self.api_seqs = []
        for file in files:
            with open(file, 'r') as f:
                dd_list = json.load(f)
            ddd_list = []
            for api_seqs_with_api_name in dd_list:
                ddd_list += [self.all_apis[api_name]
                             for api_name in api_seqs_with_api_name if api_name != "0" and api_name != "1"]
            self.api_seqs += ddd_list
        print("done load_json for all_sequence")

    def __save_jsons(self) -> None:
        with open(self.api_usages_path, 'w') as f:
            json.dump(self.api_usages, f)
        with open(self.api_frequencies_path, 'w') as f:
            json.dump(self.api_frequencies, f)
        with open(self.api_sequences_path, 'w') as f:
            json.dump(self.api_seqs, f)

    def __validate_paths(self) -> None:
        if not os.path.exists(self.all_apis_path):
            mes = f"{self.all_apis_path} does not exist"
            raise FileNotFoundError(mes)
        if not os.path.exists(self.api_freqs_path):
            mes = f"{self.api_freqs_path} does not exist"
            raise FileNotFoundError(mes)
