from util import generateToken
from openai import OpenAI
import os
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

generateToken()
import json

# Get OpenAI Client from Util.
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
}
client = OpenAI(default_headers=headers)

class RatingEnum(str, Enum):
    Excellent = "Excellent"
    Good = "Good"
    Average = "Average"
    Poor = "Poor"

class ProductReview(BaseModel):
    product_summary: str = Field(..., description="A brief summary of the product being reviewed.")
    rating: float = Field(..., description="The rating given to the product, usually on a scale from 1 to 5.")
    rating_string: Optional[RatingEnum] = Field(..., description="The value should be either worst, average, good, best.")
    review_text: str = Field(..., description="The detailed review text provided by the reviewer.")
    reviewer: str = Field(..., description="The name or identifier of the reviewer.")
    rating_string: Optional[RatingEnum] = Field(..., description="The value should be either worst, average, good, best.")
    IsReview: bool = Field(..., description="Whether the input is a review or not.")

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    temperature=0.5,
    messages=[
        {"role": "system", "content": "Extract the review details. Please use NA for missing values."},
        {
            "role": "user",
            "content": """
                                    John rated mouse as excellent                                             
                                """,
        },
    ],
    response_format = ProductReview
)

# Extract the structured review information
review = completion.choices[0].message.parsed

print(review)