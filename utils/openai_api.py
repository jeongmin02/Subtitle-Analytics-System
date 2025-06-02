import json
import base64
from pathlib import Path
from openai import OpenAI

client = OpenAI()

input_file = Path("result.json")
output_file = Path("analysis.json")

emotions = [
    "amusement", "awe", "contentment", "excitement",
    "anger", "disgust", "fear", "sadness"
]

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def query_gpt4o(image_path: str, subtitle: str):
    base64_image = encode_image_to_base64(image_path)

    prompt = f"""
다음 자막을 보고 대사 자막인지, 대사 외 자막인지 판단해 주세요. (대사 외 자막에는 출연자가 직접 하지 않은 말, 기호, 효과음 표현 등이 포함됩니다.) 자막의 디자인 요소(폰트, 색상, 크기, 강조 등)가 시청자의 감정에 어떤 영향을 미쳤는지 분석해 주세요. 디자인이 없는 기본 자막은 before_score로 간주하며, 느낌표, 물음표 등의 기호가 없으며, 아무 디자인이 없는 흰색 글씨로 표현됩니다. 이미지에서처럼 시각적으로 강조된 디자인 자막은 after_score로 간주됩니다. 각 감정(amusement, awe, contentment, excitement, anger, disgust, fear, sadness)에 대해 before_score와 after_score를 1~7 범위의 정수로 JSON 배열 형식으로 작성해 주세요. 그 외는 아래 형식을 따르되 간결하게 분석해주세요.

출력 형식:
### 1. 감정 점수 (JSON)
[
  {{"emotion": "amusement", "before_score": 2, "after_score": 5}},
  {{"emotion": "awe", "before_score": 1, "after_score": 3}}
]

### 2. 자막의 디자인이 감정에 미친 영향 & 근거 분석

대사 자막:
  "emotion": 설명

대사 외 자막:
  - 설명

### 감정 목록
emotions = [Amusement, Awe, Contentment, Excitement, Anger, Disgust, Fear, Sadness]

### 조건
- 모든 감정 점수는 1~7 범위 내 정수
- before_score < after_score
- 분석이 없는 항목은 생략 (내용 없음 등의 문장 금지)
- 설명은 모두 **한국어**, 감정명은 **영어**
- 방송명/로고/시간 정보 등은 분석 대상에서 제외
- 응답은 반드시 위 형식만 유지 (설명이나 인사말 등 추가 금지)

자막 내용: {subtitle}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "너는 TV 자막 디자인 분석가이며, 이미지에서 나타난 자막의 시각적 요소가 감정에 어떤 영향을 주는지 분석하는 전문가야. JSON 기반 감정 점수와 감정 표현 분석을 출력해줘."
                # "content": "너는 TV 자막 디자인 분석가이며, 이미지에서 나타난 자막의 시각적 요소가 감정에 어떤 영향을 주는지 분석하는 전문가야. 인물의 외모 분석은 필요하지 않아. JSON 기반 감정 점수와 감정 표현 분석을 출력해줘."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content

def parse_analysis_output(text):
    result = {
        "scores": [],
        "emotion_analysis": {},
        "gpt_raw_output": text
    }
    in_scores = False
    in_dsj = False
    in_non_dsj = False
    lines = text.splitlines()
    
    for line in lines:
        line = line.strip()
        if line.startswith("["):
            in_scores = True
            buffer = [line]
        elif in_scores:
            buffer.append(line)
            if line.endswith("]"):
                result["scores"] = json.loads("\n".join(buffer))
                in_scores = False
        elif line.startswith("대사 자막"):
            in_dsj = True
            result["emotion_analysis"]["대사 자막"] = {}
        elif line.startswith("대사 외 자막"):
            in_dsj = False
            in_non_dsj = True
            result["emotion_analysis"]["대사 외 자막"] = []
        elif in_dsj and ":" in line:
            k, v = line.split(":", 1)
            result["emotion_analysis"]["대사 자막"][k.strip()] = v.strip()
        elif in_non_dsj and line.startswith("- "):
            result["emotion_analysis"]["대사 외 자막"].append(line[2:].strip())

    return result

def generate_emotion_analysis(input_path: Path, output_path: Path):
    with open(input_path, "r") as f:
        items = json.load(f)

    results = []
    for item in items:
        subtitle = item["subtitle"]
        image_path = Path("./frames") / item["frame"]

        print(f"🔍 Processing ID {item['id']} : {subtitle}")
        try:
            gpt_response = query_gpt4o(str(image_path), subtitle)
            parsed = parse_analysis_output(gpt_response)
            item["emotion_scores"] = parsed["scores"]
            item["emotion_analysis"] = parsed["emotion_analysis"]
            item["gpt_raw_output"] = parsed["gpt_raw_output"]

        except Exception as e:
            print(f"[Error] ID {item['id']} 처리 중 오류 발생: {e}")
            item["emotion_scores"] = []
            item["emotion_analysis"] = {}

        results.append(item)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    generate_emotion_analysis(
        input_path=input_file,
        output_path=output_file
    )
