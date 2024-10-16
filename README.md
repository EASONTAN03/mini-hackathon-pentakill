# FakefaceDetect
# pentakill-cv-analysis
Project of cv analysis, Experaince GenAI 2.0 Hackathon 
"app" folder is the main folder

steps for running the app.
cd app
create .env for the following environment parameters
AZURE_OPENAI_GPT4_ENDPOINT=""
AZURE_OPENAI_GPT4o_ENDPOINT=""
AZURE_OPENAI_TEXT_EMBED_ENDPOINT=""
AZURE_OPENAI_API_KEY=""

then run the following code:
flask run

attached multiple resume.pdf files
attached one job description.pdf file
then click upload file

then write prompt
for example: " I will provide you with a list of candidates' information and a job description. Your goal is to match the candidates with the job description and rank the candidates accordingly, with the most suitable candidate ranked first."

then click "send"
