from typing import List
import json
import os
import openai
from openai import OpenAI
from pydantic import BaseModel, Field
from datetime import datetime
import lean

# -*- coding: utf-8 -*-
def gpt(message, form):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    completion = client.beta.chat.completions.parse(
        model="gpt-4.1-2025-04-14",
        messages= message,
        response_format = form,
        max_tokens= 1024,
    )

    res_json = json.loads(completion.choices[0].message.content)

    return res_json


class LeanOutput(BaseModel):
    """Here if you need to modify output structure"""
    lean: str = Field(..., description="A list of possible methods and their instructions.")
   ## in case that you need sequence of form
   ## lean_sequence: List[str] = Field(..., description="A list of possible methods and their instructions.")


