#!/bin/sh

cat api_usages.json-* > api_usages.json
cat api_frequencies.json-* > api_frequencies.json
cat api_sequences.json-* > api_sequences.json

rm -rf api_usages.json-*
rm -rf api_frequences.json-*
rm -rf api_sequences.json-*
