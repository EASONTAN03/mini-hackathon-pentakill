from openai import AzureOpenAI, OpenAIError
import os
import dotenv

dotenv.load_dotenv()

def count_tokens(messages):
    # Assuming each message is a dictionary with 'role' and 'content'
    return sum(len(message['content'].split()) for message in messages)

def get_ai_response(text):
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = "2023-09-01-preview"
    deployment = "gpt-35-turbo"

    try:
        client = AzureOpenAI(
        azure_endpoint =endpoint, 
        api_key=api_key,  
        api_version=api_version
        )

        chat_prompt=[
                {"role": "system", "content": "You are an AI assistant that helps with CV analysis."},
                {"role": "user", "content": text}
        ]
        
        input_tokens = count_tokens(chat_prompt)
        max_response_tokens = 4096 - input_tokens  # Subtract input tokens from the max limit
        max_response_tokens = max(0, max_response_tokens)  # Ensure it's not negative
        

        response = client.chat.completions.create(
            model=deployment,
            messages=chat_prompt,
            temperature=0.7,
            max_tokens=max_response_tokens,
        )
        return response.choices[0].message.content
    
    except OpenAIError as e:
        # Handle content filter violation
        return f"An error occurred: {str(e)}"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"
