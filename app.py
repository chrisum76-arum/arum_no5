import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="홈앤쇼핑 방송 현황",
    page_icon="📺",
    layout="wide",
)

# ── 브랜드 색상 커스텀 CSS ──────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #FAFAFA; }
    [data-testid="stSidebar"] { background-color: #FFF0E0; }
    h1, h2, h3 { color: #D95800; }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        border-top: 4px solid #FF6B00;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-label { font-size: 0.8rem; color: #666; font-weight: 600; text-transform: uppercase; }
    .metric-value { font-size: 2rem; font-weight: 700; color: #D95800; }
</style>
""", unsafe_allow_html=True)

CSV_PATH = Path(__file__).parent / "homeshoping_broadcast_sample_data.csv"

# ── 데이터 로드 ───────────────────────────────────────────────
def load_data():
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    df["날짜"] = pd.to_datetime(df["날짜"])
    df["난이도_수치"] = df["난이도"].map({"하": 1, "중": 2, "상": 3})
    # 론칭여부 컬럼 없으면 기본값 'O' 추가 (이전 버전 호환)
    if "론칭여부" not in df.columns:
        df.insert(5, "론칭여부", "O")
    return df

def save_data(df: pd.DataFrame):
    save_df = df.drop(columns=["난이도_수치"], errors="ignore")
    save_df["날짜"] = save_df["날짜"].dt.strftime("%Y-%m-%d")
    save_df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")

# ── 세션 상태로 데이터 관리 ───────────────────────────────────
if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# ── 헤더 ─────────────────────────────────────────────────────
st.title("📺 홈앤쇼핑 방송 현황 대시보드")
st.caption("CG 자막 제작팀 업무 데이터")
st.divider()

# ── 사이드바 필터 ─────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 필터")

    min_date = df["날짜"].min().date()
    max_date = df["날짜"].max().date()
    date_range = st.date_input(
        "날짜 범위",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    categories = ["전체"] + sorted(df["상품카테고리"].unique().tolist())
    sel_cat = st.selectbox("상품카테고리", categories)

    difficulties = ["전체", "하", "중", "상"]
    sel_diff = st.selectbox("난이도", difficulties)

    creators = ["전체"] + sorted(df["제작자"].unique().tolist())
    sel_creator = st.selectbox("제작자", creators)

    launch_opts = ["전체", "O (론칭)", "X (미론칭)"]
    sel_launch = st.selectbox("론칭 여부", launch_opts)

# ── 필터 적용 ─────────────────────────────────────────────────
filtered = df.copy()

if len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered = filtered[(filtered["날짜"] >= start) & (filtered["날짜"] <= end)]

if sel_cat != "전체":
    filtered = filtered[filtered["상품카테고리"] == sel_cat]

if sel_diff != "전체":
    filtered = filtered[filtered["난이도"] == sel_diff]

if sel_creator != "전체":
    filtered = filtered[filtered["제작자"] == sel_creator]

if sel_launch == "O (론칭)":
    filtered = filtered[filtered["론칭여부"] == "O"]
elif sel_launch == "X (미론칭)":
    filtered = filtered[filtered["론칭여부"] == "X"]

# ── KPI 요약 카드 ─────────────────────────────────────────────
total = len(filtered)
launched = (filtered["론칭여부"] == "O").sum()
not_launched = (filtered["론칭여부"] == "X").sum()
high_diff = (filtered["난이도"] == "상").sum()
days = filtered["날짜"].nunique()
avg_per_day = round(total / days, 1) if days > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">총 방송 건수</div>
        <div class="metric-value">{total:,}</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">✅ 론칭 완료</div>
        <div class="metric-value">{launched:,}</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">❌ 미론칭</div>
        <div class="metric-value">{not_launched:,}</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">고난도(상) 건수</div>
        <div class="metric-value">{high_diff:,}</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">일평균 방송수</div>
        <div class="metric-value">{avg_per_day}</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── 차트 행 1 ─────────────────────────────────────────────────
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📅 일별 방송 건수")
    daily = (
        filtered.groupby(filtered["날짜"].dt.date)
        .size()
        .reset_index(name="건수")
    )
    daily["날짜"] = daily["날짜"].astype(str)
    st.bar_chart(daily.set_index("날짜")["건수"], color="#FF6B00", height=280)

with col_right:
    st.subheader("🏷️ 카테고리별 비율")
    cat_count = filtered["상품카테고리"].value_counts().reset_index()
    cat_count.columns = ["카테고리", "건수"]
    st.dataframe(
        cat_count,
        use_container_width=True,
        hide_index=True,
        column_config={
            "건수": st.column_config.ProgressColumn(
                "건수",
                min_value=0,
                max_value=int(cat_count["건수"].max()) if len(cat_count) else 1,
                format="%d",
            )
        },
    )

st.divider()

# ── 차트 행 2 ─────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📊 난이도별 분포")
    diff_order = ["하", "중", "상"]
    diff_count = (
        filtered["난이도"]
        .value_counts()
        .reindex(diff_order, fill_value=0)
        .reset_index()
    )
    diff_count.columns = ["난이도", "건수"]
    st.bar_chart(diff_count.set_index("난이도")["건수"], color="#FF8C33", height=220)

with col_b:
    st.subheader("👤 제작자별 업무량")
    creator_diff = (
        filtered.groupby(["제작자", "난이도"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["하", "중", "상"], fill_value=0)
    )
    st.dataframe(
        creator_diff,
        use_container_width=True,
        column_config={
            "하": st.column_config.NumberColumn("하"),
            "중": st.column_config.NumberColumn("중"),
            "상": st.column_config.NumberColumn("상"),
        },
    )

st.divider()

# ── 데이터 편집 테이블 ────────────────────────────────────────
st.subheader("📋 방송 내역 편집")
st.caption("론칭여부 열에서 O / X 를 직접 수정한 뒤 **저장** 버튼을 누르세요.")

# 표시용 데이터 준비 (날짜는 문자열로)
edit_df = filtered.drop(columns=["난이도_수치"]).copy()
edit_df["날짜"] = edit_df["날짜"].dt.strftime("%Y-%m-%d")

# 난이도 아이콘
diff_label = {"하": "🟢 하", "중": "🟡 중", "상": "🔴 상"}
edit_df["난이도"] = edit_df["난이도"].map(diff_label)

# 론칭여부 아이콘
launch_label = {"O": "✅ O", "X": "❌ X"}
edit_df["론칭여부"] = edit_df["론칭여부"].map(launch_label).fillna("✅ O")

edited = st.data_editor(
    edit_df,
    use_container_width=True,
    hide_index=True,
    height=420,
    column_config={
        "날짜":     st.column_config.TextColumn("날짜", disabled=True),
        "방송시간": st.column_config.TextColumn("방송시간", disabled=True),
        "방송상품명": st.column_config.TextColumn("방송상품명", width="large", disabled=True),
        "상품카테고리": st.column_config.TextColumn("카테고리", disabled=True),
        "제작자":   st.column_config.TextColumn("제작자", disabled=True),
        "론칭여부": st.column_config.SelectboxColumn(
            "론칭여부",
            options=["✅ O", "❌ X"],
            required=True,
            width="small",
        ),
        "난이도":   st.column_config.TextColumn("난이도", disabled=True, width="small"),
    },
)

# ── 저장 버튼 ─────────────────────────────────────────────────
if st.button("💾 변경 내용 저장", type="primary"):
    # 아이콘 → 원래 값으로 역변환
    rev_launch = {"✅ O": "O", "❌ X": "X"}
    rev_diff   = {"🟢 하": "하", "🟡 중": "중", "🔴 상": "상"}

    edited["론칭여부"] = edited["론칭여부"].map(rev_launch)
    edited["난이도"]   = edited["난이도"].map(rev_diff)

    # 필터 결과의 인덱스를 원본 df에 반영
    for idx, row in zip(filtered.index, edited.itertuples(index=False)):
        st.session_state.df.at[idx, "론칭여부"] = row.론칭여부

    save_data(st.session_state.df)
    st.success(f"✅ {len(filtered)}건이 저장되었습니다.")
    st.rerun()

st.caption(f"총 {total:,}건 표시 중")
