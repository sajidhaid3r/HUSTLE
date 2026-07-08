from google import genai

client = genai.Client(api_key="YOUR API KEY")
response=client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain to me how does a gemini api work in one sentence"
)
print(response.text)