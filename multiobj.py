from util import generateToken
from openai import OpenAI
import os
generateToken()
import json
from pydantic import BaseModel, Field

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
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "A brief summary of the product being reviewed.",
        },
        "rating": {
            "type": "number",
            "description": "The rating given to the product, usually on a scale from 1 to 5.",
        },
        "rating_string": {
            "type": "string",
            "description": "The value should be either worst, average, good, best.",
            "enum": ["worst", "average", "good", "best"]
        },
        "review_text": {
            "type": "string",
            "description": "The detailed review text provided by the reviewer.",
        },
        "reviewer": {
            "type": "string",
            "description": "The name or identifier of the reviewer.",
        },
        "IsReview": {
            "type": "boolean",
            "description": "Whether the input is a review or not."
        }
    },
    "required": ["product_summary", "rating", "review_text", "reviewer", "IsReview", "rating_string"],
    "additionalProperties": False,
}


# Use OpenAI's chat completion API with the JSON Schema
reviews_schema = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": review_schema
        }
    },
    "required": ["items"],
    "additionalProperties": False,
}

create_json_schema = {
            "name": "product_review",
            "strict": True,
            "schema": reviews_schema,
        }

completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    temperature=0.5,
    messages=[
        {"role": "system", "content": "Extract the review details. Please use NA for missing values."},
        {
            "role": "user",
            "content": """
                                    John rated mouse, keyboard and speaker as 1/5
                                    Ravi rated keyboard as 5/5            
                                """,
        },
    ],
    response_format={
        "type": "json_schema",
        "json_schema": create_json_schema
    },
)

# Extract the structured review information
ratings = completion.choices[0].message.content
# Display the parsed review information
ratings_json = json.loads(ratings)
for review in ratings_json["items"]:
    print("Product Summary:", review["product_summary"])
    print("Rating:", review["rating"])
    print("Rating String:", review["rating_string"])
    print("Review Text:", review["review_text"])
    print("Reviewer:", review["reviewer"])
    print("Is Review:", review["IsReview"])
    print("\n")