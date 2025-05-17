# 카테고리 및 주제 데이터

CATEGORIES = [
    {
        "id": "environment",
        "name": "환경과학",
        "icon": "🌍",
        "topics": [
            {
                "id": "pollution",
                "name": "환경오염",
                "subtopics": [
                    "미세플라스틱이 해양 생물에 미치는 영향",
                    "지역 하천의 수질 오염도 측정 및 분석",
                    "도시 대기오염과 식물 생장의 상관관계",
                    "생분해성 플라스틱의 분해 속도 비교 연구",
                    "토양 중금속 오염이 식물 생장에 미치는 영향"
                ]
            },
            {
                "id": "energy",
                "name": "신재생에너지",
                "subtopics": [
                    "가정용 소형 태양광 발전 효율성 연구",
                    "미세조류를 이용한 바이오연료 생산 최적화",
                    "풍력 발전기 날개 형태에 따른 효율성 비교",
                    "압전 소자를 이용한 보행 에너지 수확 장치 개발",
                    "지열 에너지의 계절별 효율성 분석"
                ]
            },
            {
                "id": "ecosystem",
                "name": "생태계 보존",
                "subtopics": [
                    "도시 생태계에서 야생 조류 다양성 연구",
                    "학교 옥상 정원의 생물다양성 증진 방안",
                    "곤충 호텔 설치에 따른 수분 매개체 증가 효과",
                    "지역 하천 생태계 복원 방안 연구",
                    "도시 열섬 현상 완화를 위한 녹지 배치 연구"
                ]
            }
        ]
    },
    {
        "id": "tech",
        "name": "기술과 공학",
        "icon": "⚙️",
        "topics": [
            {
                "id": "ai",
                "name": "인공지능(AI)",
                "subtopics": [
                    "감정 인식 AI를 활용한 학습 집중도 분석",
                    "머신러닝을 이용한 학교 급식 잔반량 예측",
                    "자연어 처리를 활용한 청소년 언어 사용 패턴 분석",
                    "컴퓨터 비전을 이용한 학교 내 쓰레기 분류 시스템",
                    "딥러닝을 활용한 학생 필기체 인식 개선 연구"
                ]
            },
            {
                "id": "robotics",
                "name": "로봇공학",
                "subtopics": [
                    "교내 배달을 위한 자율주행 로봇 설계",
                    "청소년 STEM 교육을 위한 로봇 키트 개발",
                    "식물 관리를 위한 자동화 시스템 제작",
                    "장애 학생을 위한 보조 로봇 설계",
                    "재난 대비 탐색 로봇 프로토타입 개발"
                ]
            }
        ]
    }
    # 추가 카테고리는 동일한 형식으로 계속...
]

def get_all_categories():
    """전체 카테고리 목록 반환"""
    return CATEGORIES

def get_category_by_id(category_id):
    """ID로 카테고리 찾기"""
    for category in CATEGORIES:
        if category["id"] == category_id:
            return category
    return None

def get_topic_by_id(category_id, topic_id):
    """특정 카테고리 내에서 ID로 주제 찾기"""
    category = get_category_by_id(category_id)
    if category:
        for topic in category["topics"]:
            if topic["id"] == topic_id:
                return topic
    return None

def search_topics(keyword):
    """키워드로 주제 검색"""
    results = []
    for category in CATEGORIES:
        for topic in category["topics"]:
            for subtopic in topic["subtopics"]:
                if keyword.lower() in subtopic.lower():
                    results.append({
                        "category": category["name"],
                        "topic": topic["name"],
                        "subtopic": subtopic
                    })
    return results
