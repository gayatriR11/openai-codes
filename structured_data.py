from util import generateToken
from openai import OpenAI
import os
generateToken()
import json

# Get OpenAI Client from Util.
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
}
client = OpenAI(default_headers=headers)

# Define the JSON Schema for the response
review_schema = {
    "type": "object",
    "properties": {
        "product_summary": {
            "type": "string",
            "description": "A brief summary of the product being reviewed.",
        },
        "rating": {
            "type": "string",
            "description": "The rating given to the product, usually on a scale from 1 to 5.",
            "enum": ["wrost", "average", "good", "best"]
        },
        "review_text": {
            "type": "string",
            "description": "The detailed review text provided by the reviewer.",
        },
        "reviewer": {
            "type": "string",
            "description": "The name or identifier of the reviewer.",
        },
        "isReview": {
            "type": "string",
            "description": "The name or identifier of the reviewer.",
        },
    },
    "required": ["product_summary", "rating", "review_text", "reviewer", "isReview"],
    "additionalProperties": False,
}
# Use OpenAI's chat completion API with the JSON Schema
create_json_schema = {
            "name": "product_review",
            "strict": True,
            "schema": review_schema,
        }
completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    temperature=0.5,
    messages=[
        {"role": "system", "content": "Extract the review details.Please  use NA for missing values"},
        {
            "role": "user",
            "content": "John rated mouse a 4.5 out of 5.",
        },
    ],
    response_format={
        "type": "json_schema",
        "json_schema": create_json_schema
    },
)

# Extract the structured review information
rating = completion.choices[0].message.content
# Display the parsed review information
rating_json = json.loads(rating)
print(rating_json)