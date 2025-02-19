from util import generateToken
from openai import OpenAI
import os
generateToken()

# Make the API call
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
 }

client = OpenAI(default_headers=headers)

# Define the messages
messages = [
    {"role": "system", "content": "you are professor of AI, anwer all class 10th questions"},
    {"role": "user", "content": "What is OpenAI" }
    
]
completion = client.chat.completions.create(  
    model="gpt-4o-2024-05-13",
    messages=messages
)
# Print the response
print(completion.choices[0].message.content)
messages.append({"role":"assistant", "content":"completion.choices[0].message.content"})
messages.append({"role":"user", "content":"what are its benefits"})

completion = client.chat.completions.create(  
    model="gpt-4o-2024-05-13",
    messages=messages
)

print("="*50,"Benefits", "="*50)
print(completion.choices[0].message.content)
messages.append({"role":"assistant", "content":"completion.choices[0].message.content"})
messages.append({"role":"user", "content":"explain more in details about benefit one"})

completion = client.chat.completions.create(  
    model="gpt-4o-2024-05-13",
    messages=messages
)
print("="*50, "First Benefits Details", "="*50)
print(completion.choices[0].message.content)



