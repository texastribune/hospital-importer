# Hospitals Importer

## Requirements

* You will need a `Hospital_Data_Merge_TX.csv` file with all the hospitals information on it.
You should have all the addresses and hospital's names edited before running the script.
* All the `csv` files should be in a folder like `data/12-18-2014`.
* If you have a missing file check the spelling and the case. You should update `manifest.json`.

## Generate JSON files

    python import.py data/2015

The output will be copied into `output/2015`.
