from openai import OpenAI
from openai import OpenAIError
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

potential_prompts = ["You are a code reviewer. Analyze the following Python snippet and return:\n",
                     "You are a code reviewer. Analyze the following Python function and return:\n",
                     "You are a code reviewer. Analyze the following Python class snippet and return:\n"]

llm_steps = """1. A brief quality summary.
2. Line-specific comments for any issues.
3. A quality rating: Good / Needs Improvement / Buggy"""

potential_prompts = [x + llm_steps for x in potential_prompts]

def pattern_match(snippet):

    #the main purpose of this function is to return an index that will allow us to index into a list that contains the correct prompt

    function_pattern = r'^\s*(?:@[\w.]+\s+)*def\s+\w+\s*\([^)]*\)\s*:'
    class_pattern = r'^\s*class\s+\w+\s*(?:\([^)]*\))?\s*:'

    if re.match(class_pattern, snippet):

        return 2
    
    elif re.match(function_pattern, snippet):

        return 1
    
    else:

        return 0

def get_rating(response):
    
    word_arr = []
    curr_word = ""
    
    for i in range(len(response)):
        
        if i == len(response) - 1:
            
            curr_word += response[i]
            word_arr += [curr_word.lower()]
        
        elif response[i] == "*":
            continue
            
        elif response[i] == " " or response[i] == "\n":
    
            word_arr += [curr_word.lower()]
            curr_word = ""
        
        else:
            
            curr_word += response[i]
        
    word_of_interest = str()
    
    for i in range(len(word_arr)):
        
        if word_arr[i] == "needs" and i != len(word_arr) - 1:
            
            if word_arr[i + 1] == "improvement":
                
                word_of_interest = "Needs Improvement"
        
        elif word_arr[i] == "good":
            
            word_of_interest = "Good"
        
        elif word_arr[i] == "buggy":
            
            word_of_interest = "Buggy"
    
    return word_of_interest

lst_reviewed = []

try:

    with open('python_snippets.json') as f:

        code_snippets = json.load(f)

        for i in range(len(code_snippets)):
        
            curr_id_code_pair = code_snippets[i]
            curr_code = curr_id_code_pair['code']
            curr_id = curr_id_code_pair['id']
        
            num_matched = pattern_match(curr_code)

            prompt = potential_prompts[num_matched] + "\n\n" + curr_code

            try:

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content":prompt}
                    ]
                )

                response_content = response.choices[0].message.content

                rating = get_rating(response_content)

                new_dict = {'id': curr_id, 'code': curr_code, 'GPT-4o Response': response_content, 'Quality Flag': rating}

                lst_reviewed.append(new_dict)
            
            except OpenAIError as e:
                print(f"OpenAI API Error when processing ID {curr_id}: {e}")
            
            except Exception as e:
                print(f"Unexpected error during LLM call for ID {curr_id}: {e}")

except FileNotFoundError:
    print("Error: python_snippets.json file not found. Please check the file path.")

except json.JSONDecodeError:
    print("Error: python_snippets.json is not a valid JSON file.")

except Exception as e:
    print(f"Unexpected error while loading or processing file: {e}")

with open('reviewed_snippets.json', 'w') as f:
    json.dump(lst_reviewed, f, indent=2)