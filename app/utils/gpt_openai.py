import re
import numpy as np
import pandas as pd
from openai import AzureOpenAI, OpenAIError
import os
import dotenv

dotenv.load_dotenv()   

def process_csv_files(cv_csv, jd_csv):
    df = pd.read_csv(cv_csv) 
    jd_df = pd.read_csv(jd_csv)
    pd.options.mode.chained_assignment = None 

    df['ocr']= df["ocr"].apply(lambda x : normalize_text(x))
    df['ada_v2'] = df["ocr"].apply(lambda x : get_text_embed (x)) # model should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model
    df=search_docs(df, jd_df, top_n=3)
    return df,jd_df


def get_model_and_api_version(url):
    # Split to get the path and query string
    base_url = url.split('/', 3)[0] + '//' + url.split('/', 3)[2] + '/'

    path = url.split('?')[0]
    query = url.split('?')[1]

    # Extract deployment model (5th segment in the path)
    path_segments = path.split('/')
    deployment_model = path_segments[5]  # Corrected index

    # Extract API version from the query string
    query_params = query.split('&')
    api_version = ""
    for param in query_params:
        if param.startswith('api-version='):
            api_version = param.split('=')[1]

    # Output results
    return base_url, deployment_model, api_version


def normalize_text(s, sep_token = " \n "):
    if isinstance(s, str):
        # Only apply normalization if it's a string
        s = re.sub(r'\s+',  ' ', s).strip()
        s = re.sub(r". ,","",s)
        # remove all instances of multiple spaces
        s = s.replace("..",".")
        s = s.replace(". .",".")
        s = s.replace("\n", "")
        s = s.strip()
        return s
    else:
        # Return an empty string or handle it as needed
        return ''
   
    
def cosine_similarity(a, b):
    a = np.array(a, dtype=np.float32)  # Ensure 'a' is a NumPy array of floats
    b = np.array(b, dtype=np.float32)  # Ensure 'b' is a NumPy array of floats
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_text_embed(text):
    full_endpoint = os.getenv("AZURE_OPENAI_TEXT_EMBED_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    base_url, deployment, api_version=get_model_and_api_version(full_endpoint)
    
    try:
        client = AzureOpenAI(
        azure_endpoint =base_url, 
        api_key=api_key,  
        api_version=api_version
        )

        embeddings = client.embeddings.create(input=[text], model=deployment).data[0].embedding
        return embeddings
    
    except OpenAIError as e:
        # Handle content filter violation
        return f"An error occurred: {str(e)}"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def search_docs(df, jd_df, top_n=1):
    # Normalize job descriptions and get embeddings
    jd_df['ocr'] = jd_df["ocr"].apply(lambda x: normalize_text(x))
    job_embeddings = jd_df["ocr"].apply(lambda x: np.array(get_text_embed(x), dtype=np.float32)).tolist()

    df["best_match_jd"] = None
    df["best_match_similarity"] = 0.0
    df['top_matches'] = None  # Initialize a new column for storing multiple best matches

    similarities = []  # Store similarity scores for each CV

    # Iterate over each CV embedding
    for idx, cv_embedding in df['ada_v2'].items():
        # If the embedding is None, skip this entry
        if cv_embedding is None:
            print(f"Skipping CV at index {idx} due to missing embedding.")
            similarities.append([])  # Add an empty list for skipped entries
            continue

        # Convert the CV embedding to a NumPy array of floats
        try:
            cv_embedding = np.array(cv_embedding, dtype=np.float32)
        except ValueError:
            print(f"Invalid embedding at index {idx}. Skipping.")
            similarities.append([])  # Add an empty list for invalid entries
            continue

        # Calculate similarities between the CV and all job embeddings
        cv_similarities = [cosine_similarity(cv_embedding, job_embedding) for job_embedding in job_embeddings]
        similarities.append(cv_similarities)

    # Ensure the number of similarity entries matches the number of rows in df
    if len(similarities) != len(df):
        print(f"Warning: Expected {len(df)} similarity entries but got {len(similarities)}")

    df['similarities'] = similarities  # Add the similarity scores to the dataframe

    # Now extract the top N matches based on similarity
    top_matches = []
    top_similarities = []

    for sim_list in df['similarities']:
        if sim_list:  # Ensure similarity list is not empty
            # Get the indices of the top N similar job descriptions
            top_indices = np.argsort(sim_list)[-top_n:][::-1]  # Get the top N indices in descending order

            # Retrieve the job description names and similarity scores
            matches = [jd_df.iloc[idx]['name'] for idx in top_indices]
            best_similarities = [sim_list[idx] for idx in top_indices]

            top_matches.append(matches)
            top_similarities.append(best_similarities)
        else:
            top_matches.append([])
            top_similarities.append([0])  # Add 0 if no valid similarity is found

    df['top_matches'] = top_matches
    df['best_match_similarity'] = [max(sim_list) if sim_list else 0 for sim_list in top_similarities]  # Highest similarity score or 0

    # Rank the rows based on the best match similarity
    df['rank'] = df['best_match_similarity'].rank(ascending=False, method='min')

    # Sort the dataframe by the rank
    df = df.sort_values(by='rank', ascending=True)

    return df[['name', 'ocr', 'top_matches', 'best_match_similarity', 'rank']]


def get_ai_response(text, ENDPOINT):
    full_endpoint = os.getenv(ENDPOINT)
    if ENDPOINT=="AZURE_OPENAI_GPT4_ENDPOINT":
        max_tokens = 1900
    else:
        max_tokens = 1500
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    base_url, deployment, api_version=get_model_and_api_version(full_endpoint)

    try:
        client = AzureOpenAI(
        azure_endpoint =base_url, 
        api_key=api_key,  
        api_version=api_version
        )

        print(base_url, deployment, api_version)
        chat_prompt=[
                {"role": "system", "content": "You are an AI assistant that helps with CV analysis."},
                {"role": "user", "content": text}
        ]

        response = client.chat.completions.create(
            model=deployment,
            messages=chat_prompt,
            temperature=0.7,
            max_tokens=1900,
        )
        return response.choices[0].message.content
    
    except OpenAIError as e:
        # Handle content filter violation
        return f"An error occurred: {str(e)}"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

def generate_prompts(df, job_description, user_input):
    df=df[:3]
    cv_ocr = [row['ocr'] for index, row in df.iterrows()]
    prompt = (
        f"Given the job description below, analyze the following CVs:\n\n"
        f"Job Description: {job_description}\n\n"
        f"CVs:\n{cv_ocr}\n\n"
        f"{user_input}"
    )
    return prompt

def generate_jd_kp_prompts(job_description):
    prompt = (
        f"Job Description: {job_description}\n\n"
        f"tell me key factors from the job description. I want qualifications, responsibility , job description, key skills and experience required by each role"
    )
    return prompt