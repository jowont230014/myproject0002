import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="주민등록 인구 및 세대 현황 시각화", layout="wide")

st.title("📊 주민등록 인구 및 세대 현황 시각화")

# --- 파일 업로드 or 기본 경로 ---
uploaded_file = st.sidebar.file_uploader("CSV 파일 업로드", type=["csv"])

def load_data(file):
    try:
        return pd.read_csv(file, encoding='utf-8')
    except Exception:
        return pd.read_csv(file, encoding='cp949')

# 기본 경로 (깃허브에 올릴 때 같은 폴더에 두면 자동 로드됨)
default_path = "202509_202509_주민등록인구및세대현황_월간.csv"

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.success("✅ 업로드된 파일을 불러왔습니다.")
elif os.path.exists(default_path):
    df = load_data(default_path)
    st.info(f"📂 로컬 파일을 불러왔습니다: {default_path}")
else:
    st.warning("CSV 파일을 업로드하거나 동일 폴더에 파일을 추가하세요.")
    st.stop()

# --- 데이터 미리보기 ---
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# --- 컬럼 선택 ---
columns = df.columns.tolist()

st.sidebar.header("⚙️ 시각화 설정")
x_col = st.sidebar.selectbox("X축 컬럼 선택", options=columns)
y_col = st.sidebar.selectbox("Y축 컬럼 선택", options=columns)
color_col = st.sidebar.selectbox("색상 그룹(선택)", options=[None] + columns)

# --- 시각화 유형 선택 ---
chart_type = st.sidebar.radio(
    "시각화 유형 선택",
    ["라인 차트", "막대 차트", "산점도", "히트맵"]
)

# --- Plotly 그래프 생성 ---
st.subheader("📈 시각화 결과")

if chart_type == "라인 차트":
    fig = px.line(df, x=x_col, y=y_col, color=color_col, markers=True,
                  title=f"{x_col}별 {y_col} 추이")

elif chart_type == "막대 차트":
    fig = px.bar(df, x=x_col, y=y_col, color=color_col, barmode='group',
                 title=f"{x_col}별 {y_col} 막대 차트")

elif chart_type == "산점도":
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, size=y_col,
                     title=f"{x_col} vs {y_col} 산점도")

elif chart_type == "히트맵":
    pivot_df = df.pivot_table(index=x_col, columns=color_col or x_col, values=y_col, aggfunc='mean')
    fig = px.imshow(pivot_df, aspect='auto', color_continuous_scale='Viridis',
                    title=f"{x_col} × {color_col or x_col} 히트맵")

else:
    st.error("지원되지 않는 시각화 유형입니다.")
    st.stop()

# --- 그래프 출력 ---
st.plotly_chart(fig, use_container_width=True)

# --- 데이터 요약 통계 ---
st.subheader("📋 요약 통계")
st.dataframe(df.describe(include='all'))

st.caption("💡 Plotly를 사용한 Streamlit 대시보드 — GitHub에서 바로 배포 가능")
