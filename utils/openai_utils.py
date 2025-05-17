import os
import openai
from dotenv import load_dotenv

load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chat_response(messages):
    """OpenAI API를 사용하여 채팅 응답 생성"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print(f"OpenAI API 오류: {str(e)}")
        return "죄송합니다, 응답을 생성하는 중 오류가 발생했습니다. 다시 시도해주세요."

def generate_experiment_design(topic):
    """주제에 대한 실험 설계 생성"""
    prompt = f"""
    다음 주제에 대한 고등학생 수준의 과학 소논문을 위한 실험 설계를 제공해주세요:
    
    주제: {topic}
    
    다음 형식으로 응답해주세요:
    1. 연구 목적
    2. 필요한 재료 목록
    3. 실험 방법 (단계별)
    4. 데이터 분석 방법
    5. 예상되는 결과 및 의의
    
    고등학생이 실제로 수행할 수 있는 현실적인 실험이어야 합니다.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 과학 교육 전문가로, 고등학생의 과학 소논문 작성을 돕습니다."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message["content"]
