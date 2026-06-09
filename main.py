import streamlit as st
st.title('나의 첫 웹 앱!')
st.write('도전해보자!')
import streamlit as st
import time

# 1. 페이지 기본 설정 (가장 상단에 위치해야 합니다)
st.set_page_config(
    page_title="✨MBTI 진로 탐색 어드벤처✨",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. 화려한 커스텀 스타일(CSS) 적용
st.markdown("""
    <style>
    /* 메인 배경 및 폰트 스타일 */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    /* 타이틀 스타일 */
    .title-text {
        font-size: 45px !important;
        font-weight: 800;
        background: linear-gradient(90deg, #ff007f, #7f00ff, #00f0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    /* 결과 박스 스타일 */
    .result-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.1);
        border-left: 10px solid #7f00ff;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. MBTI별 진로 데이터 베이스 (예시)
mbti_jobs = {
    "ISTJ": {"name": "🧐 청렴결백한 논리주의자", "jobs": ["🔍 회계사/세무사", "⚖️ 법률 전문가", "🖥️ 데이터 분석가", "👮 공무원/경찰"], "desc": "철저하고 정직하며, 시스템과 규칙을 완벽하게 다루는 직업이 잘 어울려요!"},
    "ISFJ": {"name": "🛡️ 용감한 수호자", "jobs": ["🩺 간호사/의사", "🎒 초등·특수 교사", "🏨 호텔리어", "🎨 사회복지사"], "desc": "타인을 돕고 보호하며, 안정적이고 조화로운 환경에서 빛을 발해요!"},
    "INFJ": {"name": "🔮 선의의 옹호자", "jobs": ["🧠 심리상담사", "✍️ 소설가/작가", "🏫 교사/교육컨설턴트", "🌿 환경운동가"], "desc": "깊은 통찰력으로 사람들에게 영감을 주고, 더 나은 세상을 만드는 일에 끌려요!"},
    "INTJ": {"name": "🧠 용의주도한 전략가", "jobs": ["🚀 AI 연구원/과학자", "📊 경영 컨설턴트", "💻 시스템 아키텍트", "📈 투자분석가"], "desc": "복잡한 문제를 해결하고, 장기적인 전략을 기획하는 지적인 직업이 딱입니다!"},
    "ISTP": {"name": "🛠️ 만능 재주꾼", "jobs": ["🏎️ 엔지니어/정비사", "💻 백엔드 개발자", "📸 영상 편집자", "🕵️ 과학수사관"], "desc": "도구를 능숙하게 다루고, 직접 몸이나 기술을 써서 문제를 해결할 때 짜릿함을 느껴요!"},
    "ISFP": {"name": "🎨 호기심 많은 예술가", "jobs": ["🎨 웹툰 작가/디자이너", "🎵 작곡가/뮤지션", "🍰 파티시에", "🐾 수의테크니션"], "desc": "자신의 감각을 자유롭게 표현하고, 미적 감각을 발휘할 수 있는 환경이 완벽해요!"},
    "INFP": {"name": "🦄 열정적인 중재자", "jobs": ["🎨 크리에이터", "🎭 배우/예술가", "🧠 심리치료사", "📚 카피라이터"], "desc": "자신의 가치관과 신념을 지키며, 사람들의 마음을 치유하고 표현하는 일이 어울려요!"},
    "INTP": {"name": "💡 논리적인 사색가", "jobs": ["💻 소프트웨어 개발자", "🧪 물리학자/연구원", "🎮 게임 디자이너", "📊 빅데이터 전문가"], "desc": "끊임없이 탐구하고 새로운 이론이나 기술을 설계하는 분석적인 직업이 좋아요!"},
    "ESTP": {"name": "⚡ 수완 좋은 활동가", "jobs": ["💼 사업가/스타트업 CEO", "📈 마케팅 전문가", "🚒 소방관/스포츠 선수", "🎬 이벤트 기획자"], "desc": "변화무쌍하고 활동적이며, 당면한 문제를 즉각 해결하는 역동적인 직업이 어울려요!"},
    "ESFP": {"name": "🎉 자유로운 영혼의 연예인", "jobs": ["🎭 뮤지컬 배우/아이돌", "🎬 유튜버/스트리머", "✈️ 항공 승무원", "🛍️ 쇼호스트"], "desc": "사람들에게 즐거움을 주고, 자신이 주목받는 무대 위에서 최고의 에너지를 냅니다!"},
    "ENFP": {"name": "🌈 재기발랄한 활동가", "jobs": ["🎨 홍보·마케터", "🎤 아나운서/MC", "✈️ 여행 기획자", "🎒 청소년 지도사"], "desc": "아이디어가 샘솟고 사람들과 소통하며 긍정적인 에너지를 뿜어내는 직업이 제격이에요!"},
    "ENTP": {"name": "🔥 뜨거운 논쟁을 즐기는 변론가", "jobs": ["💼 벤처 투자자", "⚖️ 변호사/정치인", "🎮 기획자", "🚀 신사업 개발자"], "desc": "고정관념을 깨부수고, 매번 새로운 도전을 시도할 수 있는 모험적인 직업이 맞아요!"},
    "ESTJ": {"name": "👑 엄격한 관리자", "jobs": ["📈 대기업 임원/관리자", "⚖️ 판사/검사", "🏫 교장/장학사", "📊 프로젝트 매니저"], "desc": "조직을 체계적으로 이끌고, 명확한 목표를 달성해 내는 리더 역할이 완벽합니다!"},
    "ESFJ": {"name": "🤝 사교적인 외교관", "jobs": ["🎒 고등학교 교사", "🩺 상담간호사", " HR 인사담당자", "🎨 이벤트 코디네이터"], "desc": "사람들과 긴밀하게 협력하고, 타인을 따뜻하게 챙겨주는 커뮤니티 중심의 일이 좋아요!"},
    "ENFJ": {"name": "☀️ 정의로운 사회운동가", "jobs": ["🎤 전문 강사/정치인", "🏫 교사/교수", "🎨 시민단체 활동가", "💼 인사 컨설턴트"], "desc": "타인의 성장을 돕고 이끌어주며, 선한 영향력을 널리 전파하는 직업이 천직입니다!"},
    "ENTJ": {"name": "🦁 대담한 통솔자", "jobs": ["💼 CEO/창업가", "📊 경영 전략가", "💻 IT PM(프로젝트 리더)", "📈 자산운용가"], "desc": "강한 추진력과 카리스마로 팀을 리드하고, 큰 규모의 비전을 실현하는 직업이 어울려요!"}
}

# 4. 메인 화면 구성
st.markdown('<div class="title-text">🚀 MBTI 내 꿈을 찾아줘! 🌌</div>', unsafe_allow_html=True)
st.write("<h4 style='text-align: center; color: #555;'>나의 성향에 꼭 맞는 인생 직업 탐색 어드벤처 🧭</h4>", unsafe_allow_html=True)
st.markdown("---")

# 레이아웃 나누기
col1, col2 = st.columns([1, 2])

with col1:
    st.write("### 📌 Step 1")
    st.write("알파벳을 골라보세요! 👇")
    
    # 4개의 지표 선택 상자 생성
    e_i = st.selectbox("1️⃣ 에너지 방향", ["E (외향형 ☀️)", "I (내향형 🌙)"])
    s_n = st.selectbox("2️⃣ 인식 기능", ["S (감각형 🔍)", "N (직관형 🔮)"])
    t_f = st.selectbox("3️⃣ 판단 기능", ["T (사고형 📊)", "F (감정형 ❤️)"])
    j_p = st.selectbox("4️⃣ 생활 양식", ["J (판단형 📅)", "P (인식형 🍀)"])
    
    # 선택된 글자만 조합
    user_mbti = e_i[0] + s_n[0] + t_f[0] + j_p[0]

with col2:
    st.write("### 🔮 Step 2")
    st.write("당신의 성향 조합:")
    st.info(f"✨ 현재 선택된 조합: **{user_mbti}** ✨")
    
    # 분석 버튼
    btn_trigger = st.button("🌟 나의 천직 알아보기 (클릭!) 🌟", use_container_width=True)

# 5. 결과 출력 로직
if btn_trigger:
    # 로딩 애니메이션
    with st.spinner('🔮 우주에서 당신의 진로 신호를 분석 중... 📡'):
        time.sleep(1.5)
    
    # 대박 효과! 풍선 날리기 🎈
    st.balloons()
    
    # 데이터 매칭
    result = mbti_jobs[user_mbti]
    
    # 화려한 결과 상자 렌더링
    st.markdown(f"""
        <div class="result-box">
            <h2 style='color: #7f00ff; margin-top:0;'>🎉 분석 완료! 당신은 {user_mbti} 🎉</h2>
            <h3><b>{result['name']}</b></h3>
            <p style='font-size: 16px; color: #444; line-height: 1.6;'>"{result['desc']}"</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("### 🛠️ 추천하는 대표 직업군 list")
    
    # 이쁜 가로 카드 레이아웃으로 직업 노출
    job_cols = st.columns(4)
    for idx, job in enumerate(result['jobs']):
        with job_cols[idx % 4]:
            st.success(f"**{job}**")

    # 추가 감성 메시지
    st.warning("⚠️ **주의사항**: MBTI는 진로 탐색을 위한 재미있는 참고 자료일 뿐! 여러분의 무한한 가능성을 한계 짓지 마세요! 🔥")

# 6. 사이드바 꾸미기
with st.sidebar:
    st.write("# 🏫 진로 교육 센터")
    st.write("---")
    st.write("### 🧑‍🏫 선생님의 한마디")
    st.info("자신의 성향을 이해하는 것은 멋진 미래를 설계하는 첫걸음입니다. 친구들과 결과를 공유해보세요! 💬")
    st.write("---")
    st.write("🎈 **만든 이**: 생명과학&진로 교육 연구실 🧬")
