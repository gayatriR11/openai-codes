from util import generateToken
from openai import OpenAI
import os
import numpy as np
generateToken()
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
}
client = OpenAI(default_headers=headers)

response = client.embeddings.create(
  input=["Hi, how are you?", "Hello, what's up?", "where are you from?"],
  model="text-embedding-3-small",
  #dimensions=5
)

print(response.data[0].embedding)
print(response.data[1].embedding)
print(response.data[2].embedding)
