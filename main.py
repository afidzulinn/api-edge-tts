from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import edge_tts
import os
import uuid

from utils.tts import get_voice

app = FastAPI()

class TextToSpeechRequest(BaseModel):
    text: str = "halo, ini adalah api tts menggunakan edge tts"
    language: str = "id"
    gender: str = "female"
    output_format: str = ["mp3", "wav", "ogg"]


@app.get("/")
def read_root():
    return {"message": "edge tts API"}

@app.post("/text-to-speech/")
async def text_to_speech(request: TextToSpeechRequest):
    try:
        # Dapatkan suara yang sesuai berdasarkan bahasa dan gender
        voice = get_voice(request.language, request.gender)
        
        # Generate a unique file name
        file_name = f"output/{uuid.uuid4()}.{request.output_format}"

        # Instantiate the TTS engine
        communicate = edge_tts.Communicate(text=request.text, voice=voice)

        # Convert text to speech and save the audio file
        await communicate.save(file_name)

        # Check if file was created
        if not os.path.exists(file_name):
            raise HTTPException(status_code=500, detail="failed to generate audio file")

        return {"message": "audio generated successfully", "file_path": file_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9246)
