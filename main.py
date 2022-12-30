from detector_with_cfg import converter


def main():
    all_apis_path = 'cfg_builder/output/allApis.json'
    api_freqs_path = 'cfg_builder/output/apiFrequencies.json'
    api_usages_path = 'output/api_usages.json'
    api_frequencies_path = 'output/api_frequencies.json'

    converter.Covnerter(
        all_apis_path,
        api_freqs_path,
        api_usages_path,
        api_frequencies_path,
    ).convert()

if __name__ == '__main__':
    main()
