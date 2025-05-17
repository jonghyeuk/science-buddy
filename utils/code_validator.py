import os
import json
from dotenv import load_dotenv

load_dotenv()

# 환경 변수에서 접근 코드 목록 가져오기
VALID_ACCESS_CODES = json.loads(os.getenv("ACCESS_CODES", "[]"))

def validate_code(code):
    """접근 코드 유효성 검사"""
    return code in VALID_ACCESS_CODES
