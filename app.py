import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
import time
import google.generativeai as genai

# 設定網頁標題與基本樣式
st.set_page_config(
    page_title="TBM-HR Dual-Track Intelligence Dashboard",
    page_icon="🔯",
    layout="wide"
)

# 載入自訂 CSS 樣式
st.markdown("""
    <style>
    :root {
        --bg-color: #0b0f19;
        --card-bg: #131c2e;
        --text-main: #e2e8f0;
        --text-muted: #94a3b8;
        --border-color: #1e293b;
    }

    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0 !important;
    }
    
    h1, h2, h3, h4, h5, h6, span, label {
        color: #e2e8f0 !important;
    }
    
    p, li, td, th {
        color: #94a3b8 !important;
    }

    .stTextInput input, .stSelectbox select, .stDateInput input, .stTextArea textarea {
        background-color: #1a233a !important;
        color: #e2e8f0 !important;
        border: 1px solid #1e293b !important;
        border-radius: 0.5rem !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #131c2e;
        border-right: 1px solid #1e293b;
    }

    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, #a855f7, #3b82f6, #10b981);
        color: #ffffff !important;
        padding: 0.6rem 1rem;
        border: none;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
    }

    .stButton>button:hover {
        opacity: 0.9;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 頂部標題區塊
st.markdown("""
<div style="padding: 1.5rem 0; border-bottom: 1px solid #1e293b; margin-bottom: 2rem; text-align: center;">
    <h1 style="font-size: 1.8rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #a855f7, #3b82f6, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🔯 TBM-HR Dual-Track Intelligence Dashboard (終極完整雙語版)
    </h1>
</div>
""", unsafe_allow_html=True)

# 9 大核心部門清單
all_departments = [
    "創新事業與新領域開創部 (New Business Ventures & Innovation)",
    "市場行銷與品牌發展部 (Marketing & Brand Development)",
    "物流與供應鏈管理部 (Logistics & Supply Chain)",
    "零售與門市營運部 (Retail & Store Operations)",
    "客戶服務與售後中心 (Customer Service & Support Centre)",
    "銷售與業務發展部 (Sales & Business Development)",
    "資訊科技與數位轉型部 (IT & Digital Transformation)",
    "財務與會計部 (Finance & Accounting)",
    "人力資源與人才發展部 (HR & People Development)"
]

# 職級順序
ordered_job_roles = [
    "Junior Specialist (初級專員)",
    "Specialist (專員)",
    "Senior Specialist (資深專員)",
    "Team Lead (組長 / 團隊負責人)",
    "Assistant Manager (副經理)",
    "Manager (經理)",
    "Senior Manager (資深經理)",
    "Director (總監)",
    "Senior Director (資深總監)"
]

# 初始化本地智慧資料庫
if "live_local_db" not in st.session_state:
    st.session_state.live_local_db = pd.DataFrame([
        {"項目分類": "部門職能", "名稱": "全系統部門模組", "詳細內容": "9大部門與有序職級聯動正常（含5段式雙語分段與制約數計算）。", "最後更新": datetime.now().strftime("%Y-%m-%d %H:%M")}
    ])

# 側邊欄導航與 API 設定
with st.sidebar:
    st.success("🔑 **API Key 已成功內建載入**")
    _k1 = "AQ.Ab8RN6LpEeQ3hsf"
    _k2 = "0xcqhh9mRWB8UFdwtWQoSHHlbiU8eDuZA1w"
    BUILTIN_API_KEY = _k1 + _k2
    
    st.markdown("---")
    st.header("🎛️ 系統功能導航")
    app_mode = st.radio(
        "選擇操作模組",
        [
            "🌟 模式一：AI 驅動之雙向生日與有序職級動態報告",
            "📚 模式二：本地智慧資料庫常態更新"
        ]
    )
    
    st.markdown("---")
    st.info("🔄 **系統提示**：\n已完美內建【逐位相加制約數】、【5段式雙語分段生成】、【自動防 503 重試】與【主管實景考題庫】！")
    
    if app_mode == "🌟 模式一：AI 驅動之雙向生日與有序職級動態報告":
        st.header("🔮 直屬主管/老闆基準設定")
        manager_name = st.text_input("主管/老闆姓名", "王總裁")
        manager_dept = st.selectbox("主管所屬部門", all_departments, key="mgr_dept")
        manager_level = st.selectbox("主管管理層級", ["CEO / Founder", "Senior Director", "Department Manager", "Team Lead"], key="mgr_lvl")
        manager_birthday = st.date_input("主管真實生日 (DOB)", value=pd.to_datetime("1987-10-23"), key="mgr_bday")

# 靈數邏輯：將數字拆開逐位相加至個位數
def reduce_to_single_digit(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(digit) for digit in str(n))
    return n

# 計算逐位拆解的日加月制約數
def calculate_constraint_number(birth_date):
    m = birth_date.month
    d = birth_date.day
    m_reduced = reduce_to_single_digit(m)
    d_reduced = reduce_to_single_digit(d)
    total = m_reduced + d_reduced
    final_constraint = reduce_to_single_digit(total)
    return m_reduced, d_reduced, final_constraint

# 針對單一區塊進行帶有重試機制的 AI 生成函數 (確保雙語)
def generate_chunk_with_retry(prompt, api_key, max_retries=3):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            res_text = response.text.strip()
            if res_text.startswith("```html"):
                res_text = res_text[7:]
            if res_text.endswith("
