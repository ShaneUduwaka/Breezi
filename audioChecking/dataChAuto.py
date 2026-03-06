import pandas as pd
from google import genai
from google.genai import types
import time

df = pd.read_csv("dataset3.tsv", sep="\t")

for i in range (3955,5230):
    tempPath = df.iloc[i,0]

    client = genai.Client(api_key="#")

    audio_file = client.files.upload(file=tempPath)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=['You are given an audio clip that needs to be transcribed and into Sinhala. Transcribe the audio fully in Sinhala without adding punctuation such as commas or full stops. Maintain a continuous flow of the text as spoken. Include any interjections or sounds like "ahh" or "meh" as they appear in the speech. Also type the numbers in sinahala dont put the numbers. Strictly follow these rules and im telling you again strictly folloe these rules.', audio_file]
    )

    print("\nRecord number :",i+1,"\n")
    print(response.text)

    time.sleep(2)

    df.iloc[i, 2] = response.text
    df.to_csv("dataset3.tsv", sep="\t", index=False)

 
