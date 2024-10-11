# FakefaceDetect
# pentakill-cv-analysis
Project of cv analysis, Experaince GenAI 2.0 Hackathon 

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>


## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Adding new CV 
│   ├── interim        <- Intermediate data with OCR (Text Extraction)
│   ├── processed      <- Final fetaures to be trained
│   └── raw            <- The raw cv (pdf) ;image(if possible)
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         fakefacedetect and configuration for tools like black
│
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
│
├── app        <- User interface (Tkinter)
│
└── src   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes fakefacedetect a Python module
    │
    ├── textract.py              <- extract text from cv [data/raw] to txt [data/interim]
    ├── prepare.py              <- extract keywords(features) from txt [data/interim] to csv/json [data/processed]
    ├── train.py            <- Using features[data/processed] to build a model. Output to models dir
    │
    └── evaluate              <- test model with specific cv
```

--------