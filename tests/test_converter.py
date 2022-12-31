from detector_with_cfg import converter
import os

def test_converter():
    all_apis_path = 'cfg_builder/output/allApis.json'
    api_freqs_path = 'cfg_builder/output/apiFrequencies.json'
    api_seqs_path =  'cfg_builder/output/apiSequences.json'
    api_usages_path = 'output/api_usages.json'
    api_frequencies_path = 'output/api_frequencies.json'
    api_sequences_path =  'output/api_sequences.json'

    if os.path.exists(api_usages_path):
        os.remove(api_usages_path)
    if os.path.exists(api_frequencies_path):
        os.remove(api_frequencies_path)
    if os.path.exists(api_sequences_path):
        os.remove(api_sequences_path)

    converter.Covnerter(
        all_apis_path,
        api_freqs_path,
        api_seqs_path,
        api_usages_path,
        api_frequencies_path,
        api_sequences_path
    ).convert()

    assert os.path.exists(api_usages_path)
    assert os.path.getsize(api_usages_path) > 0
    assert os.path.exists(api_frequencies_path)
    assert os.path.getsize(api_frequencies_path) > 0
    assert os.path.exists(api_sequences_path)
    assert os.path.getsize(api_sequences_path) > 0
