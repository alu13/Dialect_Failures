# GCP_Exploration

This is an accompanying code repository to the Computational Social Science course project. Our report covering key findings is available in this repository, under `/doc` folder.

## Directory structure
```
├── LICENSE
├── README.md
├── data -> all collected data
│   ├── csvs -> all raw Reddit utterance files
│   └── jsons -> all data on BLEU/SS scores
└── src
    ├── data_preprocessing.ipynb -> data pre-processing notebook
    ├── data_visualization -> visualization functions
    ├── DialoGPT.py -> file for getting DialoGPT outputs
    ├── Double_Pipline.ipynb -> notebook for getting DialoGPT and Blenderbot scores
    └── GCP_exploration.py -> pulling data files from GCP bucket
```

## Reproducing our work

All preprocessing can be found in data_preprocessing.ipynb
All scores can be resampled in Double_Pipeline.ipynb 
All visualization steps can be found in data_visualization

### Environment setup

To reproduce steps associated with topic analysis, make sure to use the `environment.yml` file to recreate the conda environment.