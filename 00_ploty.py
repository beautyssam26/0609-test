
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(page_title="글로벌 시가총액 Top 10 주식 대시보드", layout="wide")

st.title("🌐 글로벌 시가총액 Top 10 주식 대시보드 (최근 1년)")
st.markdown("야후 파이낸스(`yfinance`) 데이터를 실시간으로 가져와 글로벌 시가총액 상위 기업들의 주가 흐름을 비교합니다.")

# 2026년 기준 글로벌 시가총액 상위 10개 기업 (데이터 수집이 용이한 미국 증시 상장사 중심 구성)
TOP_10_COMPANIES = {
    'NVIDIA': 'NVDA',
    'Apple': 'AAPL',
    'Alphabet (Google)': 'GOOGL',
    'Microsoft': 'MSFT',
    'Amazon': 'AMZN',
    'TSMC': 'TSM',
    'Broadcom': 'AVGO',
    'Tesla': 'TSLA',
    'Meta Platforms': 'META',
    'Berkshire Hathaway': 'BRK-B'
}

# 2. 사이드바 제어 흐름 설정
st.sidebar.header("⚙️ 대시보드 옵션")

# 기업 선택 멀티셀렉트 (기본값: 전체 선택)
selected_companies = st.sidebar.multiselect(
    "시각화할 기업을 선택하세요:",
    options=list(TOP_10_COMPANIES.keys()),
    default=list(TOP_10_COMPANIES.keys())
)

# 차트 표시 방식 라디오 버튼
chart_type = st.sidebar.radio(
    "데이터 표시 방식 선택:",
    ("누적 수익률 (%)", "실제 주가 (USD)")
)

# 3. 데이터 수집 함수 (st.cache_data를 통한 캐싱으로 로딩 속도 최적화)
@st.cache_data(ttl=3600)  # 1시간 동안 데이터 캐싱 유지
def load_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        if not hist.empty:
            # 타임존 제거 및 날짜 형식 포맷 통일 (Streamlit Arrow 직렬화 에러 방지)
            hist.index = hist.index.date
            return hist['Close']
    except Exception as e:
        return None
    return None

# 4. 메인 대시보드 로직
if not selected_companies:
    st.warning("⚠️ 최소 한 개 이상의 기업을 선택해주세요.")
else:
    with st.spinner("야후 파이낸스에서 실시간 데이터를 가져오는 중입니다..."):
        df = pd.DataFrame()
        for name in selected_companies:
            ticker = TOP_10_COMPANIES[name]
            close_series = load_stock_data(ticker)
            if close_series is not None:
                df[name] = close_series
                
    if df.empty:
        st.error("데이터를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.")
    else:
        # 매칭되는 거래일 기준 결측치 제거
        df = df.dropna()
        
        # 데이터 변환 (실제 주가 vs 누적 수익률)
        if chart_type == "누적 수익률 (%)":
            # (현재 가격 / 최초 시작 가격 - 1) * 100
            df_display = ((df / df.iloc[0]) - 1) * 100
            y_label = "수익률 (%)"
            title_suffix = "누적 수익률 비교 (%)"
        else:
            df_display = df
            y_label = "주가 ($)"
            title_suffix = "주가 변화 (USD)"
            
        # Plotly Express 시각화를 위해 Wide형태를 Long 형태로 변환 (Melt)
        df_melted = df_display.reset_index().melt(id_vars=['index'], var_name='Company', value_name='Value')
        df_melted.rename(columns={'index': 'Date'}, inplace=True)
        
        # 5. 상호작용형 선형 차트 그리기
        fig = px.line(
            df_melted, 
            x='Date', 
            y='Value', 
            color='Company',
            title=f"📊 글로벌 주요 기업 최근 1년 {title_suffix}",
            labels={'Value': y_label, 'Date': '날짜', 'Company': '기업'},
            template='plotly_white'
        )
        
        # 마우스 오버 시 툴팁 서식 지정
        fig.update_traces(mode="lines", hovertemplate="<b>%{hovertext}</b><br>날짜: %{x}<br>값: %{y:.2f}")
        
        # Streamlit 화면에 차트 출력
        st.plotly_chart(fig, use_container_width=True)
        
        # 6. 하단 데이터 요약 테이블 제공
        st.markdown("---")
        st.subheader("📋 기업별 주요 주가 통계")
        
        summary_list = []
        for name in selected_companies:
            if name in df.columns:
                current_val = df[name].iloc[-1]
                initial_val = df[name].iloc[0]
                total_return = ((current_val / initial_val) - 1) * 100
                
                summary_list.append({
                    "기업명": name,
                    "티커(Ticker)": TOP_10_COMPANIES[name],
                    "현재 주가": f"${current_val:,.2f}",
                    "1년 전 주가": f"${initial_val:,.2f}",
                    "최근 1년 수익률": f"{total_return:+.2f}%"
                })
                
        st.dataframe(pd.DataFrame(summary_list), use_container_width=True, hide_index=True)
