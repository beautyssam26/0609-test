

import streamlit as st
import random
import time

# =====================================================================
# 1. 페이지 기본 설정 및 디자인 테마 정의 (글로벌 CSS)
# =====================================================================
st.set_page_config(
    page_title="🎨 고1 선택과목 마법 탐험대 🚀",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 화려함의 끝판왕! 네온 그라디언트와 커스텀 애니메이션 효과 추가
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dongle:wght@400;700&family=Nanum+Pen+Script&family=Pretendard:wght@400;600;800&display=swap');
    
    /* 기본 폰트 적용 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 배경 및 전반적인 그라디언트 효과 */
    .stApp {
        background: linear-gradient(135deg, #fef9e7 0%, #ebf5fb 50%, #f5eef8 100%);
    }
    
    /* 타이틀 스타일 */
    .main-title {
        font-size: 50px !important;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(45deg, #FF1493, #FF4500, #8A2BE2, #00FF7F, #00FFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: rainbow 8s ease infinite;
        background-size: 400% 400%;
        margin-bottom: 5px;
    }
    
    @keyframes rainbow {
        0%{background-position:0% 50%}
        50%{background-position:100% 50%}
        100%{background-position:0% 50%}
    }
    
    /* 카드 스타일 (계열 및 교과 정보용) */
    .glowing-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(138, 43, 226, 0.1);
        border: 2px solid rgba(138, 43, 226, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
    }
    .glowing-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(255, 20, 147, 0.2);
        border-color: #ff007f;
    }
    
    /* 미니 헤더 뱃지 스타일 */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        font-size: 14px;
        font-weight: 700;
        border-radius: 30px;
        color: white;
        margin-right: 8px;
        margin-bottom: 10px;
    }
    .badge-primary { background: linear-gradient(135deg, #8A2BE2, #4169E1); }
    .badge-secondary { background: linear-gradient(135deg, #FF1493, #FF69B4); }
    .badge-tertiary { background: linear-gradient(135deg, #00FF7F, #00b359); }
    
    /* 실시간 반응 버튼 스타일 */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #FF1493, #8A2BE2) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(255, 20, 147, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        height: 50px !important;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 8px 25px rgba(138, 43, 226, 0.6) !important;
    }
    
    /* 사이드바 스타일링 */
    section[data-testid="stSidebar"] {
        background-color: #1a0f30 !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #00FFFF !important;
    }
    
    /* 진행률 바 스타일 커스텀 */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #00FF7F, #00FFFF, #8A2BE2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. 계열별 교과목 정보 데이터베이스 구축 (2022 개정교육과정 반영)
# =====================================================================
career_database = {
    "IT/공학 계열 🤖💻": {
        "desc": "세상을 바꾸는 신기술, 기계, 그리고 알고리즘을 설계하는 창조자들의 놀이터!",
        "general": ["수학Ⅰ 🔢", "수학Ⅱ 📊", "미적분 📈", "물리학Ⅰ ⚡", "화학Ⅰ 🧪", "정보 💻"],
        "career": ["기하 📐", "인공지능 수학 🤖", "물리학Ⅱ 🌀", "화학Ⅱ ⚗️", "공학 일반 🛠️"],
        "convergence": ["융합과학탐구 🔬", "데이터 과학 📊", "수학과 문화 🏛️"],
        "keyword": "창의력 / 논리성 / 수리력 / 문제해결력",
        "jobs": ["AI 엔지니어 🧠", "화이트해커 🛡️", "로봇 공학자 🤖", "우주항공연구원 🚀", "게임 디자이너 🎮"]
    },
    "의학/생명과학 계열 🩺🧬": {
        "desc": "생명의 신비를 풀고 아픈 이들을 따뜻하게 보살피는 인류의 수호자!",
        "general": ["화학Ⅰ 🧪", "생명과학Ⅰ 🧬", "확률과 통계 🎲", "독서 📚"],
        "career": ["화학Ⅱ ⚗️", "생명과학Ⅱ 🔬", "보건 🩺", "생활과 과학 🌿"],
        "convergence": ["생명과학 실험 🧫", "융합과학탐구 🧪", "기후변화와 환경생태 🌍"],
        "keyword": "생명존중 / 분석력 / 인내심 / 실험정신",
        "jobs": ["의사/치과의사 🩺", "신약 개발자 💊", "유전공학자 🧬", "수의사 🐾", "바이오에너지 연구원 🌿"]
    },
    "자연과학 계열 🌌🔬": {
        "desc": "우주의 진리와 자연의 기초 물리 법칙을 끝없이 밝혀내는 탐험가!",
        "general": ["수학Ⅰ 🔢", "수학Ⅱ 📊", "미적분 📈", "물리학Ⅰ ⚡", "화학Ⅰ 🧪", "지구과학Ⅰ 🌍"],
        "career": ["물리학Ⅱ 🌀", "화학Ⅱ ⚗️", "지구과학Ⅱ 🌌", "기하 📐"],
        "convergence": ["과학사 🏛️", "융합과학 🧪", "창의융합과제 연구 💡"],
        "keyword": "호기심 / 탐구력 / 끈기 / 수학적 사고",
        "jobs": ["우주물리학자 🌌", "나노소재연구원 🔬", "기상예보관 ⛅", "고생물학자 🦖", "화학분석가 🧪"]
    },
    "경영/경제/금융 계열 📈💰": {
        "desc": "글로벌 시장의 흐름을 지배하고 새로운 가치를 발굴하는 비즈니스 리더!",
        "general": ["확률과 통계 🎲", "경제 📊", "사회·문화 👥", "영어 독해와 작문 ✍️"],
        "career": ["경제수학 📐", "실용 수학 ➕", "사회문제 탐구 🧐"],
        "convergence": ["금융과 경제 💳", "국제 경제 🌐", "창의경영 💡"],
        "keyword": "리더십 / 판단력 / 데이터분석력 / 친화력",
        "jobs": ["CEO/창업가 👑", "펀드매니저 💸", "마케터 📣", "회계사 📊", "M&A 컨설턴트 🤝"]
    },
    "인문/어문 계열 📚✍️": {
        "desc": "인간의 가치, 언어의 아름다움, 그리고 역사의 지혜를 탐닉하는 사색가!",
        "general": ["문학 📖", "세계사 🗺️", "동아시아사 ⛩️", "윤리와 사상 💭", "외국어Ⅰ 🗣️"],
        "career": ["고전 읽기 📜", "심화 국어 ✍️", "고전과 윤리 🕊️"],
        "convergence": ["문학과 영상 🎬", "비교 문화 🌐", "스토리텔링과 창작 📝"],
        "keyword": "공감능력 / 인문학적 소양 / 언어감각 / 성찰력",
        "jobs": ["외교관 🌐", "방송기자/PD 🎬", "소설가/웹소설 작가 📝", "동시통역사 🗣️", "역사학 연구원 🏛️"]
    },
    "사회과학/행정/법률 계열 ⚖️🏛️": {
        "desc": "우리 사회의 법과 정의를 지키고 더 공평하고 살기 좋은 세상을 그리는 정책가!",
        "general": ["정치와 법 ⚖️", "사회·문화 👥", "생활과 윤리 🕊️", "세계지리 🗺️"],
        "career": ["사회문제 탐구 🧐", "고전과 윤리 📜", "지리정보 서비스 📍"],
        "convergence": ["인권과 법률 🗽", "기후변화와 사회 🌍", "비교 사회문화 🧑‍🤝‍🧑"],
        "keyword": "정의감 / 논리적 변론 / 분석적 사고 / 의사소통",
        "jobs": ["판사/검사/변호사 ⚖️", "국회의원/행정공무원 🏛️", "프로파일러 🕵️", "도시계획가 🗺️", "인권 운동가 ✊"]
    },
    "교육 계열 🏫🏫": {
        "desc": "다음 세대의 가슴속에 희망과 호기심의 씨앗을 뿌리는 평생의 스승!",
        "general": ["독서 📖", "화법과 작문 🎤", "확률과 통계 🎲", "생활과 윤리 🕊️"],
        "career": ["교육학 🏫", "심리학 🧠", "사회문제 탐구 🧐"],
        "convergence": ["아동 복지와 교육 👶", "문화다양성 이해 🤝", "고전과 명저 읽기 📚"],
        "keyword": "인내심 / 공감과 사랑 / 교수학습 능력 / 리더십",
        "jobs": ["초등/중등/고등 교사 🧑‍🏫", "교육공학연구원 💻", "교과서 개발자 📘", "특수교육 전문가 🤝", "심리상담 교사 🧠"]
    },
    "예술/체육 계열 🎨⚽": {
        "desc": "온몸의 세포와 오감을 깨워 세상에 무한한 전율과 아름다움을 선물하는 예술인!",
        "general": ["미술 🎨", "음악 🎵", "체육 🏃", "생활과 윤리 🕊️", "독서 📖"],
        "career": ["미술 창작 🖌️", "음악 연주 🎹", "스포츠 생활 ⚽", "드로잉 ✏️"],
        "convergence": ["미디어 예술 📹", "스포츠 과학 🧬", "무대 연출 🎭", "작품 평론 📝"],
        "keyword": "예술적 감각 / 신체 조절력 / 독창성 / 표현력",
        "jobs": ["웹툰 작가 🎨", "뮤지컬 배우 🎭", "스포츠 트레이너 🏃", "영화감독 🎬", "전시기획자(큐레이터) 🖼️"]
    }
}

# Session State 초기화 (선택과목 가상 담기 바구니 및 진단 질문 트래킹용)
if "my_cart" not in st.session_state:
    st.session_state.my_cart = []
if "test_score" not in st.session_state:
    st.session_state.test_score = {"공학": 0, "생명": 0, "인문": 0, "경영": 0}

# =====================================================================
# 3. 사이드바 - 실시간 장바구니 🛒 & 1:1 상담 안내 💬
# =====================================================================
with st.sidebar:
    st.markdown("## 🏫 내 손안의 진학실 🔮")
    st.write("---")
    
    st.markdown("### 🛒 내가 찜한 선택과목")
    if len(st.session_state.my_cart) == 0:
        st.info("💡 아직 담은 과목이 없어요!\n오른쪽 화면에서 교과목 옆의 `담기 ➕`를 눌러 나만의 시간표를 만들어 보세요!")
    else:
        for item in st.session_state.my_cart:
            st.success(f"📌 {item}")
        
        if st.button("🧼 장바구니 비우기", use_container_width=True):
            st.session_state.my_cart = []
            st.rerun()
            
    st.write("---")
    st.markdown("### 🧑‍🏫 담임쌤의 잔소리(?) 한마디")
    st.warning("고1 시기는 나의 무한한 가능성을 실험하는 때입니다! 성적 유불리만 따지기보다는 나의 진짜 가슴이 뛰는 학문이 무엇인지 귀기울여 보세요! 👂💖")
    st.caption("🚀 배포처: 고등학교 1학년 진학지원팀 💫")

# =====================================================================
# 4. 메인 화면 - 화려한 인트로 레이아웃
# =====================================================================
st.markdown('<div class="main-title">🌟 고1을 위한 꿈의 선택과목 마법 탐험대 🌟</div>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #5B2C6F; font-weight: 600;'>내 관심 계열을 고르면 나에게 딱 어울리는 마법같은 교과목 목록을 배달해 드려요! 🧭🎁</h3>", unsafe_allow_html=True)
st.write("")

# 웰컴 애니메이션 데코레이션
st.snow() if random.random() > 0.5 else st.balloons()

# 탭을 나누어 두 가지 기능 제공 (1. 메인 추천 매치, 2. 미니 자가 진단 퀴즈)
tab1, tab2 = st.tabs(["🎯 바로 계열 탐색하기", "🔮 관심계열 미니 테스트"])

# =====================================================================
# Tab 1: 메인 계열 검색 및 과목 추천 매칭 시스템
# =====================================================================
with tab1:
    st.markdown("### 📌 Step 1. 관심이 가거나 설레는 계열을 터치해 보세요!")
    
    # 가로형 카드 형태로 계열 선택 셀렉트박스 꾸미기
    selected_name = st.selectbox(
        "✨ 현재 당신이 눈여겨보고 있는 계열은 무엇인가요?", 
        list(career_database.keys()),
        index=0
    )
    
    st.markdown("---")
    
    # 선택된 계열의 상세 데이터 로드
    data = career_database[selected_name]
    
    # 2열 레이아웃을 이용한 입체적 정보 시각화
    col1, col2 = st.columns([5, 4])
    
    with col1:
        st.markdown(f"""
            <div class="glowing-card">
                <span class="badge badge-primary">✨ 한줄 요약</span>
                <h3 style='color:#7D3C98; margin-top:5px; font-weight: 700;'>{selected_name}</h3>
                <p style='font-size:18px; color:#4a4a4a; line-height:1.6;'><b>{data['desc']}</b></p>
                <hr style='border:1px solid #eee;'>
                <p style='font-size:16px; color:#555;'>🎯 <b>핵심 필요 역량:</b> <span style='color:#FF1493; font-weight:bold;'>{data['keyword']}</span></p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🚀 Step 2. 고2, 고3 때 배울 추천 과목 확인하기!")
        st.info("💡 추천 교과목 옆의 `담기 ➕` 버튼을 누르면 실시간으로 내 시간표 장바구니에 쏙 들어갑니다!")
        
        # 교과목 추천 세부 카테고리 구성 (일반 / 진로 / 융합)
        col_sub1, col_sub2, col_sub3 = st.columns(3)
        
        with col_sub1:
            st.markdown('<span class="badge badge-primary">📕 일반 선택</span>', unsafe_allow_html=True)
            for sub in data['general']:
                sc_col1, sc_col2 = st.columns([3, 1])
                sc_col1.write(f"🔹 {sub}")
                if sc_col2.button("담기", key=f"g_{sub}"):
                    if sub not in st.session_state.my_cart:
                        st.session_state.my_cart.append(sub)
                        st.success(f"{sub} 담기 완료!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.warning("이미 담긴 과목입니다!")
                        
        with col_sub2:
            st.markdown('<span class="badge badge-secondary">📘 진로 선택</span>', unsafe_allow_html=True)
            for sub in data['career']:
                sc_col1, sc_col2 = st.columns([3, 1])
                sc_col1.write(f"🔸 {sub}")
                if sc_col2.button("담기", key=f"c_{sub}"):
                    if sub not in st.session_state.my_cart:
                        st.session_state.my_cart.append(sub)
                        st.success(f"{sub} 담기 완료!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.warning("이미 담긴 과목입니다!")
                        
        with col_sub3:
            st.markdown('<span class="badge badge-tertiary">🟢 융합 선택</span>', unsafe_allow_html=True)
            for sub in data['convergence']:
                sc_col1, sc_col2 = st.columns([3, 1])
                sc_col1.write(f"🌿 {sub}")
                if sc_col2.button("담기", key=f"v_{sub}"):
                    if sub not in st.session_state.my_cart:
                        st.session_state.my_cart.append(sub)
                        st.success(f"{sub} 담기 완료!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.warning("이미 담긴 과목입니다!")

    with col2:
        st.markdown(f"""
            <div class="glowing-card" style="background: linear-gradient(135deg, #FFF0F5, #FFE4E1);">
                <span class="badge badge-secondary">🔮 이런 학과&직업이 어울려요!</span>
                <h4 style="margin-top:10px; color:#C71585; font-weight:700;">꿈의 커리어 맵 🗺️</h4>
                <p style="font-size:15px; color:#555;">아래의 멋진 직업에 대해 흥미가 생긴다면 {selected_name} 과목들을 집중해서 이수하는 것이 대학 진학에도 강력한 스펙이 됩니다!</p>
                <ul style="list-style-type: none; padding-left: 0;">
        """, unsafe_allow_html=True)
        
        for job in data['jobs']:
            st.write(f"🔥 **{job}**")
            
        st.markdown(f"""
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # 선배들의 생생한 조언 카드 탑재
        st.markdown("""
            <div class="glowing-card" style="background: #E8F8F5;">
                <span class="badge badge-tertiary">🧑‍🎓 합격 선배들의 꿀팁 방출</span>
                <p style="font-size:15px; color:#0e6251; line-height:1.6; margin-top:5px;">
                "저는 고1 때 수학, 과학에 흥미가 덜했는데 추천 과목 장바구니에서 융합선택 과목을 우연히 보고 기후변화 쪽에 꽂혔어요. 덕분에 고2 탐구보고서 주제를 멋지게 잡았고 학종 합격까지 직행했답니다! 성적만 보고 선택하지 마세요!" <br>
                <b>- 서울권 대학 학종 합격생 정OO 선배 💖</b>
                </p>
            </div>
        """, unsafe_allow_html=True)

# =====================================================================
# Tab 2: 내 성향/계열 자가 진단 미니테스트 (3초 진단기)
# =====================================================================
with tab2:
    st.markdown("### 🕵️‍♂️ 3초 계열 매칭 스피드 테스트!")
    st.write("나의 성격이나 평소 관심사를 보고 아래 질문에 정직하게 응답해 보세요!")
    
    q1 = st.radio(
        "💡 Q1. 주말 자유 시간에 당신은 주로 무엇을 하는 것을 더 좋아하나요?",
        ["🔨 컴퓨터 프로그래밍이나 기계 만지기, 전자기기 분해 조립하기", "🩺 반려 동식물 돌보기 또는 내 몸의 건강과 영양성분 꼼꼼히 챙기기", "💬 사회적인 현상(시사 이슈, 뉴스, 인간 행동 등) 분석하거나 토론하기", "🎨 나만의 세계를 글, 그림, 음악으로 직접 참신하게 창조해보기"]
    )
    
    q2 = st.radio(
        "💡 Q2. 만약 수학 시간에 어려운 고난도 문제가 주어졌을 때 당신의 반응은?",
        ["🔥 오기 충만! 밤을 새워서라도 논리적으로 공식을 써서 풀어낸다.", "🌱 이 공식이 실생활에서 의약품 개발이나 암 치료 등에 어떻게 응용될지 상상한다.", "💵 이 공식이 금융 상품 설계나 환율 변동 추측 계산 등에 어떻게 쓰일지 궁금해진다.", "😭 머리가 복잡해져서 차라리 감수성 넘치는 문학책을 읽으며 마음을 달랜다."]
    )

    if st.button("🔮 나의 계열 진단 결과 매칭하기 🔮", key="trigger_test"):
        with st.spinner("⏳ 신중하게 당신의 잠재 능력 스펙트럼 분석 중..."):
            time.sleep(1.2)
        st.balloons()
        
        # 단순 가상 스코어 계산법으로 실감나는 결과 도출
        match_category = ""
        if "🔨" in q1 and "🔥" in q2:
            match_category = "IT/공학 계열 🤖💻"
        elif "🩺" in q1 or "🌱" in q2:
            match_category = "의학/생명과학 계열 🩺🧬"
        elif "💬" in q1 or "💵" in q2:
            match_category = "경영/경제/금융 계열 📈💰"
        else:
            match_category = "인문/어문 계열 📚✍️"
            
        st.markdown(f"""
            <div class="glowing-card" style="background: linear-gradient(135deg, #EAECEE, #D5F5E3); border:3px solid #2ECC71;">
                <h3 style="color:#1D8348; margin-top:0;">🎉 진단 완료! 당신의 최우선 매치 계열:</h3>
                <h2>🔮 {match_category} 🔮</h2>
                <p style="font-size:16px; color:#273746;">위 결과는 당신의 답변 특성을 기반으로 산출된 찰떡 매칭입니다. 상단에 마련된 <b>[🎯 바로 계열 탐색하기]</b> 탭에서 <b>{match_category}</b>을 선택하고 과목을 바로 구경해 보세요!</p>
            </div>
        """, unsafe_allow_html=True)

# =====================================================================
# 5. 푸터 & 하단 응원 메시지
# =====================================================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>✨ 이 진로 교육 어드벤처 앱은 고1 학생들이 주도적이고 재미있게 자신의 고등학교 교육과정을 직접 설계할 수 있도록 설계된 에듀테크 서비스입니다. ✨</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 13px; color: #bbb;'>© 2026 High School Career Design Platform. All rights reserved.</p>", unsafe_allow_html=True)
