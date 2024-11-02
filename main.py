from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    # 추가 설정에 대한 선택적 파라미터를 추가
    initial: str = "initial"  # 초기 설정 기본값
    quality: str = "Quality"  # "Speed", "Quality", "Extreme Speed" 중 선택 가능
    guidance_scale: float = 30.0  # 가이던스 스케일 최대값
    styles: list[str] = ["MRE Sumi E Symbolic", "MK Color SketchNote", "Pencil Sketch Drawing"]

@app.post("/generate-image/")
async def generate_image(prompt_request: PromptRequest):
    # Fooocus API URL과 payload 설정 - v2옵션 선택 (v1은 guidance_scale 적용불가)
    fooocus_api_url = "http://127.0.0.1:8888/v2/generation/text-to-image-with-ip"
    payload = {
        "prompt": prompt_request.prompt,
        "performance_selection": prompt_request.quality,
        "guidance_scale": prompt_request.guidance_scale,
        "style_selections": prompt_request.styles
    }
    headers = {
        "accept": "image/png"
    }

    try:
        # Fooocus API에 요청 보내기
        response = requests.post(fooocus_api_url, json=payload, headers=headers)
        response.raise_for_status()
        generated_image = response.content  # 이미지 바이트 데이터
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Fooocus 모델 호출 오류: {str(e)}")

    # 생성된 이미지 저장 경로 설정
    image_path = f"./generated_images/{prompt_request.prompt.replace(' ', '_')}.png"
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(generated_image)

    return {"image_path": image_path}
