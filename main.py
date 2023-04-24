from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from gtts import gTTS
from datetime import datetime
import shutil
import speech_recognition as sr
from pydub import AudioSegment


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/texto")
async def texto(texto: Request):
    texto = await texto.json()
    fala = gTTS(text=str(texto['texto']),
                lang='pt-br',
                slow=True)

    epoch_time = datetime.now().timestamp()

    fala.save(f"./falas/texto{epoch_time}.wav")
    return FileResponse(f"./falas/texto{epoch_time}.wav")


@app.post("/audio/")
async def create_upload_file(file: UploadFile = File(...)):
    epoch_time = datetime.now().timestamp()
    with open(f"audios/conversa_up{epoch_time}.mp3", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    sound = AudioSegment.from_mp3(f"audios/conversa_up{epoch_time}.mp3")
    sound.export(f"audios/conversa_up{epoch_time}.wav", format="wav")

    # transcribe audio file
    AUDIO_FILE = f"audios/conversa_up{epoch_time}.wav"

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

        transcricao = r.recognize_google(audio, language="pt-BR")

    return {"transcricao": transcricao}
