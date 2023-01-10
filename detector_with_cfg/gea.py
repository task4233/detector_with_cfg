import random
import traceback
import copy


class GEA():
    def __init__(self) -> None:
        pass

    def generate_with_api_usages(self, api_usages: list) -> list:
        """
        - api_usages: list[list[0|1]]
          - one-hot vector which api is used or not
          - tail of the list indicates family(0: benign, 1: malicious)
        - pick 2 samples
            - 1 benign sample and 1 malicious sample
        - merge them
        - return
        """

        benigns = [api for api in api_usages if api[-1] == 0]
        maliciouses = [api for api in api_usages if api[-1] != 0]

        benign = copy.deepcopy(random.choice(benigns))
        malicious = random.choice(maliciouses)

        # print(f"benign: {len(benign)}")
        # print(f"malicious: {len(malicious)}")

        for i in range(len(malicious)):
            try:
                benign[i] |= malicious[i]
            except Exception as e:
                print(f'benign: {benign[i]}, malicious: {malicious[i]}')
                traceback.print_exc()

        return benign

    def generate_with_api_freqs(self, api_freqs: list) -> list:
        """
        - api_freqs: list[list[occurrences]]
          - number of occurrences for each apis
          - tail of the list indicates family(0: benign, 1: malicious)
        - pick 2 samples
            - 1 benign sample and 1 malicious sample
        - merge them
        - return
        """

        benigns = [api for api in api_freqs if api[-1] == 0]
        maliciouses = [api for api in api_freqs if api[-1] != 0]

        benign = copy.deepcopy(random.choice(benigns))
        malicious = random.choice(maliciouses)

        for i, v in enumerate(malicious):
            benign[i] += v
        return benign
