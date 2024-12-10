from openai import OpenAI

def openaiGenerate(prompt):
    model = OpenAI(api_key="sk-1234567890")
    response = model.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}])
    return response.choices[0].message.content