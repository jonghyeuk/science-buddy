import streamlit as st
import requests
import json
import time
from utils.data import get_all_categories, search_topics
from utils.code_validator import validate_code

# 상수
API_URL = "http://localhost:8000"  # 로컬 테스트용

# 세션 상태 초기화
if 'access_code' not in st.session_state:
    st.session_state.access_code = ""
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = ""
if 'experiment_design' not in st.session_state:
    st.session_state.experiment_design = ""

# 스타일 적용
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# API 호출 함수
def api_chat(messages):
    """API를 통한 채팅"""
    try:
        response = requests.post(f"{API_URL}/api/chat", json={
            "code": st.session_state.access_code,
            "messages": messages
        })
        if response.status_code == 200:
            return response.json()["response"]
        else:
            st.error(f"API 오류: {response.status_code}")
            return "죄송합니다, 응답을 생성하는 중 오류가 발생했습니다."
    except Exception as e:
        st.error(f"API 연결 오류: {str(e)}")
        # 오프라인 모드에서는 유사한 응답 생성
        if "환경" in messages[-1]["content"]:
            return "환경과학에 관심이 있으시군요! 좀 더 구체적으로, 수질 오염, 대기 오염, 생태계 보존 중 어떤 주제에 관심이 있으신가요?"
        elif "수질" in messages[-1]["content"]:
            return "수질 오염에 대해 연구하고 싶으시군요. 몇 가지 흥미로운 주제를 제안해 드릴게요:\n\n1. 미세플라스틱이 수생 생물에 미치는 영향\n2. 지역 하천의 수질 오염도 측정 및 분석\n3. 천연 소재를 활용한 수질 정화 방법 연구"
        elif "미세플라스틱" in messages[-1]["content"]:
            return "미세플라스틱이 수생 생물에 미치는 영향을 연구하는 것은 매우 시의적절한 주제입니다! 이 주제로 실험을 설계해볼까요?"
        return "흥미로운 주제네요! 더 자세히 알려주시면 관련된 연구 주제를 추천해드릴 수 있어요."

def api_get_experiment(topic):
    """API를 통한 실험 설계 생성"""
    try:
        response = requests.post(f"{API_URL}/api/experiment", json={
            "code": st.session_state.access_code,
            "topic": topic
        })
        if response.status_code == 200:
            return response.json()["experiment_design"]
        else:
            st.error(f"API 오류: {response.status_code}")
            return "실험 설계를 생성할 수 없습니다. 다시 시도해주세요."
    except Exception as e:
        st.error(f"API 연결 오류: {str(e)}")
        # 오프라인 모드에서는 샘플 데이터 반환
        return """
        # 연구 목적
        미세플라스틱이 담수 생태계의 생물(물벼룩)에 미치는 영향을 관찰하고 분석하여 미세플라스틱 오염의 생태학적 영향을 이해한다.

        # 필요한 재료
        - 물벼룩 (Daphnia magna) - 생물 실험실에서 구입 가능
        - 미세플라스틱 비드 (5-100μm 크기)
        - 배양 용기 (최소 20개)
        - 현미경
        - 증류수
        - 물벼룩 먹이 (조류)
        - 온도계
        - pH 측정기

        # 실험 방법
        1. 5개의 실험군을 설정: 대조군(미세플라스틱 없음), 저농도(10μg/L), 중농도(100μg/L), 고농도(1000μg/L), 초고농도(10000μg/L)
        2. 각 실험군당 4개의 배양 용기에 각각 10마리의 물벼룩을 넣는다.
        3. 모든 배양 용기는 동일한 환경 조건(온도, 조명, 먹이)에서 유지한다.
        4. 7일 동안 다음 항목을 매일 관찰하고 기록:
           - 생존율
           - 행동 패턴 (움직임, 먹이 섭취 등)
           - 번식률 (새끼 수)
        5. 7일 후 현미경을 통해 물벼룩의 체내 미세플라스틱 축적을 관찰한다.

        # 데이터 분석 방법
        - 각 농도별 생존율을 그래프로 비교
        - 행동 패턴 변화를 점수화하여 통계 분석
        - 번식률과 미세플라스틱 농도 간의 상관관계 분석
        - 현미경 관찰 결과 정리 및 시각화
        - t-검정과 ANOVA를 이용한 실험군 간 유의미한 차이 분석

        # 예상되는 결과 및 의의
        이 실험을 통해 미세플라스틱 노출이 수생 생물의 생존, 행동, 번식에 미치는 영향을 정량적으로 측정할 수 있을 것이다. 다양한 농도에서의 영향을 비교함으로써 미세플라스틱 오염의 위험 수준을 평가하는 데 기여할 수 있다.

        이 연구는 수질 오염 정책 및 미세플라스틱 규제의 중요성을 뒷받침하는 과학적 증거를 제공할 수 있다.
        """

# 페이지 함수
def login_page():
    """로그인 페이지"""
    st.title("🧪 사이언스버디")
    st.subheader("고교생 과학 소논문 작성 도우미")
    
    with st.form("login_form"):
        access_code = st.text_input("액세스 코드를 입력하세요", type="password")
        submitted = st.form_submit_button("접속하기", use_container_width=True)
        
        if submitted:
            # 로컬에서 코드 검증 (API가 없을 경우)
            if validate_code(access_code):
                st.session_state.access_code = access_code
                st.session_state.current_page = "home"
                st.experimental_rerun()
            else:
                st.error("유효하지 않은 코드입니다.")
    
    st.markdown("---")
    st.markdown("### 사이언스버디란?")
    st.markdown("""
    사이언스버디는 고등학생들이 과학 소논문을 작성할 때 주제 선정부터 실험 설계까지 
    AI의 도움을 받을 수 있는 서비스입니다. AI와의 대화를 통해 자신만의 연구 주제를 
    발견하고, 실험 방법을 설계해보세요!
    """)

def home_page():
    """홈 화면"""
    st.title("🧪 사이언스버디")
    
    # 메뉴 카드
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 주제 탐색하기")
        st.markdown("AI와 대화하며 연구 주제 찾기")
        if st.button("시작하기", key="chat_start", use_container_width=True):
            st.session_state.current_page = "chat"
            st.experimental_rerun()
    
    with col2:
        st.markdown("### 관심분야 탐색")
        st.markdown("분야별 인기 연구 주제 살펴보기")
        if st.button("시작하기", key="topics_start", use_container_width=True):
            st.session_state.current_page = "topics"
            st.experimental_rerun()
    
    st.markdown("### 논문 작성 가이드")
    st.markdown("구조화된 논문 작성법 배우기")
    if st.button("시작하기", key="guide_start", use_container_width=True):
        st.session_state.current_page = "guide"
        st.experimental_rerun()
    
    # 선택된 주제가 있으면 실험 설계 버튼 활성화
    if st.session_state.selected_topic:
        st.markdown(f"### 실험 설계하기: {st.session_state.selected_topic}")
        st.markdown("선택한 주제에 대한 실험 방법 설계")
        if st.button("시작하기", key="experiment_start", use_container_width=True):
            st.session_state.current_page = "experiment"
            # 실험 설계가 아직 없으면 생성
            if not st.session_state.experiment_design:
                with st.spinner("실험 설계를 생성하는 중..."):
                    st.session_state.experiment_design = api_get_experiment(st.session_state.selected_topic)
            st.experimental_rerun()

def chat_page():
    """대화 페이지"""
    st.title("💬 주제 탐색하기")
    st.markdown("AI와 대화하며 연구 주제를 찾아보세요.")
    
    # 상단 네비게이션
    if st.button("← 홈으로 돌아가기", key="home_button"):
        st.session_state.current_page = "home"
        st.experimental_rerun()
    
    st.markdown("---")
    
    # 채팅 메시지 표시
    for i, msg in enumerate(st.session_state.chat_messages):
        if msg["role"] == "user":
            st.markdown(f"**You**: {msg['content']}")
        else:
            st.markdown(f"**AI**: {msg['content']}")
    
    # 사용자 입력
    with st.form("chat_form"):
        user_input = st.text_input("메시지를 입력하세요...", key="user_input")
        cols = st.columns([1, 1, 1])
        
        with cols[0]:
            if st.form_submit_button("환경과학에 관심 있어요", use_container_width=True):
                user_input = "환경과학에 관심이 있어요"
        
        with cols[1]:
            if st.form_submit_button("수질 오염 연구하고 싶어요", use_container_width=True):
                user_input = "수질 오염에 대해 연구하고 싶어요"
        
        with cols[2]:
            if st.form_submit_button("미세플라스틱 주제가 좋아요", use_container_width=True):
                user_input = "미세플라스틱 주제가 좋을 것 같아요"
        
        submitted = st.form_submit_button("전송", use_container_width=True)
        
        if submitted and user_input:
            # 사용자 메시지 추가
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            
            # AI 응답 생성
            with st.spinner("AI가 응답을 생성하는 중..."):
                response = api_chat(st.session_state.chat_messages)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
            
            # 미세플라스틱 주제 감지 및 저장
            if "미세플라스틱" in user_input.lower():
                st.session_state.selected_topic = "미세플라스틱이 수생 생물에 미치는 영향"
                st.info(f"'{st.session_state.selected_topic}' 주제가 선택되었습니다. 홈 화면에서 실험 설계를 시작할 수 있습니다.")
            
            st.experimental_rerun()

def topics_page():
   """주제 탐색 페이지"""
   st.title("🔍 관심분야 탐색")
   
   # 상단 네비게이션
   if st.button("← 홈으로 돌아가기", key="home_button"):
       st.session_state.current_page = "home"
       st.experimental_rerun()
   
   # 검색 기능
   search_term = st.text_input("관심 키워드 검색...", placeholder="환경, AI, 미세플라스틱 등")
   
   if search_term:
       results = search_topics(search_term)
       if results:
           st.markdown(f"### '{search_term}' 검색 결과")
           for result in results:
               with st.expander(f"{result['subtopic']} ({result['category']} > {result['topic']})"):
                   st.markdown(f"**분야:** {result['category']}")
                   st.markdown(f"**주제:** {result['topic']}")
                   st.markdown(f"**연구 아이디어:** {result['subtopic']}")
                   if st.button(f"이 주제로 선택하기", key=f"select_{result['subtopic']}"):
                       st.session_state.selected_topic = result['subtopic']
                       st.success(f"'{result['subtopic']}' 주제가 선택되었습니다!")
                       st.session_state.experiment_design = ""  # 새 주제이므로 실험 설계 초기화
       else:
           st.info(f"'{search_term}'에 대한 검색 결과가 없습니다.")
   
   # 인기 연구 분야
   st.markdown("### 인기 연구 분야")
   col1, col2 = st.columns(2)
   
   popular_keywords = ["환경오염", "인공지능", "재생에너지", "미생물"]
   with col1:
       if st.button("환경오염", use_container_width=True):
           st.session_state.search_term = "환경오염"
           st.experimental_rerun()
       if st.button("재생에너지", use_container_width=True):
           st.session_state.search_term = "에너지"
           st.experimental_rerun()
   
   with col2:
       if st.button("인공지능", use_container_width=True):
           st.session_state.search_term = "인공지능"
           st.experimental_rerun()
       if st.button("미생물", use_container_width=True):
           st.session_state.search_term = "미생물"
           st.experimental_rerun()
   
   # 카테고리 목록
   st.markdown("### 주제 카테고리")
   categories = get_all_categories()
   
   for category in categories:
       with st.expander(f"{category['icon']} {category['name']}"):
           for topic in category['topics']:
               st.markdown(f"#### {topic['name']}")
               for i, subtopic in enumerate(topic['subtopics']):
                   col1, col2 = st.columns([4, 1])
                   with col1:
                       st.markdown(f"{i+1}. {subtopic}")
                   with col2:
                       if st.button("선택", key=f"btn_{category['id']}_{topic['id']}_{i}"):
                           st.session_state.selected_topic = subtopic
                           st.success(f"'{subtopic}' 주제가 선택되었습니다!")
                           st.session_state.experiment_design = ""  # 새 주제이므로 실험 설계 초기화

def experiment_page():
    """실험 설계 페이지"""
    st.title("🧪 실험 설계하기")
    st.subheader(st.session_state.selected_topic)
    
    # 상단 네비게이션
    if st.button("← 홈으로 돌아가기", key="home_button"):
        st.session_state.current_page = "home"
        st.experimental_rerun()
    
    # 실험 설계가 없으면 생성
    if not st.session_state.experiment_design:
        with st.spinner("실험 설계를 생성하는 중..."):
            st.session_state.experiment_design = api_get_experiment(st.session_state.selected_topic)
    
    # 실험 설계 표시
    st.markdown(st.session_state.experiment_design)
    
    # 이메일 전송 기능
    st.markdown("---")
    st.subheader("실험 설계 공유하기")
    
    with st.form("email_form"):
        email = st.text_input("이메일 주소", placeholder="your@email.com")
        submitted = st.form_submit_button("이메일로 받기", use_container_width=True)
        
        if submitted:
            if "@" in email and "." in email:
                st.success("실험 설계가 이메일로 전송되었습니다! (테스트 모드)")
            else:
                st.error("유효한 이메일 주소를 입력해주세요.")
    
    # 클립보드 복사 버튼
    if st.button("클립보드에 복사", use_container_width=True):
        # JavaScript를 이용한 클립보드 복사는 Streamlit에서 직접 지원하지 않아
        # 브라우저에서 실행되는 JavaScript가 필요합니다.
        # 여기서는 사용자에게 텍스트를 선택하여 복사하도록 안내합니다.
        st.info("위 내용을 선택하고 Ctrl+C(Mac의 경우 Cmd+C)를 눌러 복사하세요.")

def guide_page():
    """논문 작성 가이드 페이지"""
    st.title("📝 논문 작성 가이드")
    
    # 상단 네비게이션
    if st.button("← 홈으로 돌아가기", key="home_button"):
        st.session_state.current_page = "home"
        st.experimental_rerun()
    
    st.markdown("""
    ### 소논문 구성 요소
    
    과학 소논문은 일반적으로 다음과 같은 구성 요소를 포함합니다:
    
    1. **제목 (Title)**
       - 연구 내용을 명확하고 간결하게 표현
       - 독자의 관심을 끌 수 있는 제목 선택
    
    2. **초록 (Abstract)**
       - 연구의 목적, 방법, 결과, 결론을 200-300자 내외로
       - 논문의 전체 내용을 압축적으로 표현
    
    3. **서론 (Introduction)**
       - 연구 배경 및 목적
       - 선행 연구 검토
       - 연구 질문 또는 가설 제시
    
    4. **연구 방법 (Methods)**
       - 실험 설계
       - 재료 및 장비
       - 데이터 수집 방법
       - 분석 방법
    
    5. **결과 (Results)**
       - 수집한 데이터 제시
       - 표와 그래프를 활용한 시각화
       - 통계 분석 결과
    
    6. **고찰 (Discussion)**
       - 결과 해석
       - 연구 질문/가설에 대한 답변
       - 연구의 한계점
       - 향후 연구 방향
    
    7. **결론 (Conclusion)**
       - 연구의 주요 발견
       - 연구의 의의
    
    8. **참고문헌 (References)**
       - 인용한 모든 자료의 출처
       - 학술지 형식에 맞춰 작성
    """)
    
    st.markdown("### 논문 작성 팁")
    
    tips = [
        "**객관적인 어조 유지하기**: 개인적인 의견보다는 데이터에 기반한 서술을 해야 합니다.",
        "**그래프와 표 활용하기**: 복잡한 데이터는 시각적으로 표현하면 더 이해하기 쉽습니다.",
        "**일관된 형식 사용하기**: 전체 논문에서 용어, 단위, 참고문헌 형식을 일관되게 사용합니다.",
        "**명확하고 간결하게 쓰기**: 불필요한 수식어를 피하고 핵심 내용을 명확하게 전달합니다.",
        "**여러 번 수정하기**: 초안 작성 후 여러 번 읽고 수정하여 완성도를 높입니다."
    ]
    
    for tip in tips:
        st.markdown(f"- {tip}")
    
    st.markdown("### 샘플 논문")
    
    st.info("사이언스버디로 주제를 선택하고 실험을 설계한 후, 이 가이드를 참고하여 논문을 작성해보세요!")

# 메인 앱 로직
def main():
    # 페이지 설정
    st.set_page_config(
        page_title="사이언스버디",
        page_icon="🧪",
        layout="centered"
    )
    
    # CSS 로드 시도
    try:
        load_css()
    except:
        pass
    
    # 현재 페이지에 따라 다른 함수 호출
    if st.session_state.current_page == "login":
        login_page()
    elif st.session_state.current_page == "home":
        home_page()
    elif st.session_state.current_page == "chat":
        chat_page()
    elif st.session_state.current_page == "topics":
        topics_page()
    elif st.session_state.current_page == "experiment":
        experiment_page()
    elif st.session_state.current_page == "guide":
        guide_page()

if __name__ == "__main__":
    main()
