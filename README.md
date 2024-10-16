# FakefaceDetect
# pentakill-cv-analysis
Project of cv analysis, Experaince GenAI 2.0 Hackathon 
"app" folder is the main folder


## Project Organization

```
├── data
│   ├── cv_pdf       <- input cv files
│   ├── jd_pdf        <- input job description files
│   └── ocr_text      <- extracted cv and jd .txt
│
├── app          <- Configuration file for flake8
│   ├── upload_cv        <- saved cv pdf files from file uploaded from html:js
│   ├── upload_jd        <- saved job description pdf files from file uploaded from html:js
│   ├── output       <- saved processed cv and jd in csv {name:ocr} files
│   ├── static       <- css and frontend media (img,png,mp4) 
│   ├── template        <- *.html 
│   ├── utils       <- functions called in routes.py
│   │   ├── files2csv.py        <- data processing from pdf to csv
│   │   └── gpt_openai.py      <- functions for retrieving and calling Azure openai 
│   ├── app,py       <- initialize flask app in local deployment (port:5000)
│   └── routes.py       <- receive HTTP methods from html:js and ex1cecute functions
│
├── requirements.txt   <- Dependencies (env:name:"cv-analysis")
│                         generated with `pip freeze > requirements.txt`
│
└── README.md          <- The top-level README for developers using this project.
```

--------
## cv-analysis with openai workflow
1. Processing multiple cv pdf and one job description pdf into csv files.
2. Text embedding cv_ocr and jd_ocr.
3. Using cosine similarity to calculate similarity score for CVs and one jd.
4. Ranking and filter out top 3 candidates respected to the jd.
5. Retrieve the ocr of the 3 candidates and 1 jd.
6. Combine [5.] and user input in to request prompt 
7. Calling openai with prompt and config, return the response
8. Can continue communicate with openai and getting desire solution.

## Step by step guidance:
steps for running the app.
Creating python environment
- cd pentakill-cv-analysis
- conda create --name cv-analysis python=3.10
- conda activate cv-analysis
- pip install requirements.txt

Set up env config
- cd app
- create .env for the following environment parameters
{
AZURE_OPENAI_GPT4_ENDPOINT=""
AZURE_OPENAI_GPT4o_ENDPOINT=""
AZURE_OPENAI_TEXT_EMBED_ENDPOINT=""
AZURE_OPENAI_API_KEY=""
}

Then run the following code:
- flask run

Interface operation
- attached multiple resume.pdf files
- attached one job description.pdf file
- then click upload file
- then input prompt into chatbox
+ for example: " I will provide you with a list of candidates' information and a job description. Your goal is to match the candidates with the job description and rank the candidates accordingly, with the most suitable candidate ranked first."
- then click "send"

Collaborators: Tan Beng Seh, Sui Wei En, Ng Rou Yan, Pah Onn Qi, Tan Yong Seng
