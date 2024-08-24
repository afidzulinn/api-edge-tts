from fastapi import HTTPException

def get_voice(language: str, gender: str) -> str:
    voices = {
        "id": {
            "male": "id-ID-ArdiNeural",
            "female": "id-ID-GadisNeural"
        },
        "en": {
            "male": "en-US-GuyNeural",
            "female": "en-US-JennyNeural"
        },
        "zh": {
            "male": "zh-CN-YunxiNeural",
            "female": "zh-CN-XiaoxiaoNeural"
        }
    }

    if language not in voices:
        raise HTTPException(status_code=400, detail="unsupported language")
    if gender not in voices[language]:
        raise HTTPException(status_code=400, detail="unsupported gender")

    return voices[language][gender]