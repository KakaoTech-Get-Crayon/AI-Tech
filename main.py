# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate-image/")
async def generate_image(prompt_request: PromptRequest):
    prompt = prompt_request.prompt
    
    # Fooocus API URL (Text to image with prompt 엔드포인트)
    fooocus_api_url = "http://127.0.0.1:8888/v2/generation/text-to-image-with-ip"
    payload = {
        "prompt": prompt
    }
    headers = {
        "accept": "image/png"
    }

    try:
        # Fooocus에 요청 보내기
        response = requests.post(fooocus_api_url, json=payload, headers=headers)
        response.raise_for_status()
        generated_image = response.content  # 이미지 바이트 데이터
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error in Fooocus model call: {str(e)}")

    # 이미지 저장 경로 설정
    image_path = f"./generated_images/{prompt.replace(' ', '_')}.png"
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(generated_image)

    return {"image_path": image_path}
