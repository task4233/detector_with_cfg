#!/bin/sh

# split
split -b 32M -d api_usages.json api_usages.json-
split -b 32M -d api_frequencies.json api_frequencies.json-
split -b 32M -d api_sequences.json api_sequences.json-