# Set the OPENAI_API_KEY environment variable in a different file
!export OPENAI_API_KEY='YOUR_API_KEY'

import openai

completion = client.chat.completions.create(
  model="gpt-3.5-turbo-16k",
   messages=[
    {"role": "system", "content": "You are a helpful assistant. Always anwser the question in Korean."},
    {"role": "user", "content": "Please provide a list of South Korea's presidents from the first to the present (up to present), including their index order, names, and periods in office."},
  ]
)

print(completion.choices[0].message)
