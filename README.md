# Hospitals Importer

## Requirements

* `csv2json`
* You will need `hospitals-201X.json`. Old json data file.
* You will need a `Hospital_Data_Merge_TX.csv` file with all the hospitals information on it.
You should have all the addresses and hospital's names edited before running the script.
* All the `csv` files should be in a folder like `data/12-18-2014`.
* If you have a missing file check the spelling and the case. You should update `manifest.json`.

## Generate JSON files

    python import.py data/WHEREVER_YOU_HAVE_YOUR_CSV_FILES

The output will be copied into `output`. Once you have the `json` and `geojson` files you should copy them into `hospitals.texastribune.org/data`.
Keep in mind that you will need the old data files to show old info.
