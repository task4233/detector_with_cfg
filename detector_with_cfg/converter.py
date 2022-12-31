import json
import os
import traceback


class Covnerter():
    def __init__(
        self,
        all_apis_path: str,
        api_freqs_path: str,
        api_usages_path: str,
        api_frequencies_path: str,
    ) -> None:
        self.all_apis_path = all_apis_path
        self.api_freqs_path = api_freqs_path
        self.api_usages_path = api_usages_path
        self.api_frequencies_path = api_frequencies_path

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
        all_apis = list(self.all_apis.keys())
        all_apis.append('family')

        self.api_usages = [all_apis]
        self.api_frequencies = [all_apis]
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
        # load jsons
        with open(self.all_apis_path, 'r') as f:
            # all_apis:  Map<String, Integer> <=> Map<api_name, api_number>
            # api_number is 0-indexed
            self.all_apis = json.load(f)
        with open(self.api_freqs_path, 'r') as f:
            # api_freqs: List<Map<String, Integer>> <=> List<Map<api_name, occurrences>>
            self.api_freqs = json.load(f)

    def __save_jsons(self) -> None:
        with open(self.api_usages_path, 'w') as f:
            json.dump(self.api_usages, f)
        with open(self.api_frequencies_path, 'w') as f:
            json.dump(self.api_frequencies, f)


    def __validate_paths(self) -> None:
        if not os.path.exists(self.all_apis_path):
            mes = f"{self.all_apis_path} does not exist"
            raise FileNotFoundError(mes)
        if not os.path.exists(self.api_freqs_path):
            mes = f"{self.api_freqs_path} does not exist"
            raise FileNotFoundError(mes)
