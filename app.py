import streamlit as st
from google import genai
import pandas as pd
import io
import time

# 設定網頁標題與基本樣式（自然綠意與花草生活風）
st.set_page_config(
    page_title="TBM-HR 智慧人才與人格雙語分析系統",
    page_icon="🌿",
    layout="wide"
)

# 載入自訂 CSS 樣式
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F7F4;
        color: #2D3748 !important;
    }
    h1, h2, h3, h4, h5, h6, span, label {
        color: #1A3022 !important;
    }
    p, li {
        color: #4A5568 !important;
    }
    .card {
        background-color: #FFFFFF;
        padding: 1.8rem;
        border-radius: 1rem;
        border: 1px solid #D8E2D8;
        box-shadow: 0 4px 6px -1px rgba(46, 125, 50, 0.05), 0 2px 4px -1px rgba(46, 125, 50, 0.03);
        margin-bottom: 1.5rem;
    }
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #2E7D32 !important;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #4CAF50;
        padding-left: 12px;
    }
    .stTextInput input, .stSelectbox select, .stDateInput input {
        background-color: #FFFFFF !important;
        color: #2D3748 !important;
        border: 1px solid #C8D6C8 !important;
        border-radius: 0.5rem !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #E8F0E8;
        border-right: 1px solid #D8E2D8;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
        background-color: #2E7D32;
        color: #FFFFFF !important;
        padding: 0.6rem 1rem;
        border: none;
        box-shadow: 0 2px 4px rgba(46, 125, 50, 0.2);
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# 頂部標題區塊
st.markdown("""
<div style="padding: 1rem 0; border-bottom: 2px solid #D8E2D8; margin-bottom: 1.5rem;">
    <div style="display: flex; flex-direction: column; gap: 8px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="background-color: #FFFFFF; color: #2E7D32 !important; padding: 0.4rem 0.9rem; border-radius: 0.5rem; font-weight: 700; border: 1px solid #C8E6C9; font-size: 0.95rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                🌱 TBM 綠野心靈與天賦空間 (Essence & Talents Engine)
            </div>
            <span style="background-color: #E8F5E9; color: #2E7D32 !important; padding: 0.3rem 0.8rem; border-radius: 2rem; font-size: 0.8rem; font-weight: 600; border: 1px solid #C8E6C9;">
                Bringing Everything Together ! 🌿
            </span>
        </div>
        <div>
            <h1 style="font-size: 1.6rem; font-weight: 700; margin: 4px 0 2px 0; color: #1B5E20 !important;">
                TBM-HR 智慧決策與人格分析平台 (本質與才華深度雙語版)
            </h1>
            <p style="font-size: 0.9rem; color: #388E3C !important; margin: 0;">
                結合東方八字命盤與西方生命靈數雙軌基準，深度解構個人本質與天賦原型，不使用冰冷數字，提供具體清晰的中英雙語分析報告。
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 側邊欄：環境與全域設定
with st.sidebar:
    st.header("🌿 組織與模式設定")
    
    manager_level = st.selectbox(
        "管理層級設定 (Evaluation Manager Level)",
        [
            "CEO (最高執行長 / Chief Executive Officer)",
            "TA (直屬營運主管 / Team Leader)",
            "高層 (Executive / C-Level Director)",
            "經理 (Branch / Department Manager)",
            "IT 資訊科技主管 (IT Manager / Head of IT)",
            "資深專員 / 專業技師 (Senior Specialist)",
            "基層服務人員 / 新人 (Junior / Frontline Staff)"
        ]
    )

    manager_birthday = st.sidebar.date_input("主管 / 領導者生日（雙基底對應 / Manager Birthday）")
    
    st.markdown("---")
    
    api_key = ""
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.sidebar.success("已透過安全通道載入 AI 授權")
    else:
        api_key = st.sidebar.text_input("輸入 Gemini API Key", type="password")
        if not api_key:
            st.sidebar.warning("尚未偵測到 API Key！")


# 具備自動容錯與多模型備援的呼叫函式
def call_essence_gemini(api_key, prompt):
    client = genai.Client(api_key=api_key)
    models_to_try = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-2.0-flash']
    
    last_err = None
    for m in models_to_try:
        for _ in range(2):
            try:
                res = client.models.generate_content(
                    model=m,
                    contents=prompt
                )
                if res and res.text:
                    return res.text
            except Exception as e:
                last_err = e
                time.sleep(1)
                continue
    raise Exception(f"無法取得 AI 回應。詳細錯誤：{last_err}")


# ==================== 區塊一：單人精準人格分析與獨立分類設定 ====================
st.markdown('<div class="section-title">🌿 模式一：單人本質、核心才華、崗位綱要與中英雙語 SOP 深度評估</div>', unsafe_allow_html=True)
st.write("精確選取員工所屬**部門**、**職業/職務類別**與**職級 Level**，AI 將直接從靈魂本質、天賦原型與實際崗位需求出發，生成清晰易懂的中英雙語報告。")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("受評估員工姓名 / 應徵者代號 (Employee Name / ID)", "張小明", key="single_name")
        birth_date = st.date_input("受評估員工出生年月日 (Date of Birth)", value=pd.to_datetime("1990-01-01"), key="single_birth")
    
    with col2:
        target_department = st.selectbox(
            "1. 選擇所屬部門 (Department)",
            [
                "創新事業與新領域開創部 (New Business Ventures & Innovation)",
                "市場行銷與品牌發展部 (Marketing & Brand Development)",
                "物流與供應鏈管理部 (Logistics & Supply Chain)",
                "零售與門市營運部 (Retail & Store Operations)",
                "客戶服務與售後中心 (Customer Service & Support Centre)", 
                "銷售與業務發展部 (Sales & Business Development)",
                "資訊科技與數位轉型部 (IT & Digital Transformation)",
                "財務與會計部 (Finance & Accounting)", 
                "人力資源與人才發展部 (HR & People Development)"
            ],
            key="single_dept"
        )
        
        job_role = st.selectbox(
            "2. 選擇職業 / 職務類別 (Job Role)",
            [
                "新事業開發經理 / 創新策略專員 (New Business / Innovation Strategist)",
                "品牌企劃 / 行銷專員 (Brand / Marketing Specialist)",
                "物流調度 / 供應鏈管理專員 (Logistics / Supply Chain Specialist)",
                "倉儲管理 / 配送專員 (Warehouse / Distribution Staff)",
                "門市銷售 / 零售專員 (Retail Sales Representative)",
                "客服專員 / 售後技術支援 (Customer Service / Support)",
                "軟體工程師 / IT 技術專員 (Software Engineer / IT Specialist)",
                "會計 / 財務專員 (Accounting / Finance Specialist)",
                "HR 人資專員 / 招募專員 (HR / Talent Specialist)"
            ],
            key="single_role"
        )
        
        candidate_level = st.selectbox(
            "3. 選擇職級 Level (Rank & Level)",
            [
                "CEO / 最高執行長 (Chief Executive Officer)",
                "高層總監 / 核心合夥人 (Executive / C-Level Director)",
                "部門資深經理 / 資深主管 (Senior Manager / Department Head)",
                "資深專員 / 專業技師 (Senior Specialist)",
                "一般專員 / 區經理 / 專案經理 (Manager / Specialist / Staff)",
                "基層新人 / 第一線服務人員 (Junior / Frontline Staff)",
                "實習生 / 培訓生 (Intern / Trainee)"
            ],
            key="single_level"
        )
        
    st.markdown('</div>', unsafe_allow_html=True)
    
if st.button("開始生成本質才華解構與中英雙語 SOP 報告", key="btn_single_run"):
    if not api_key:
        st.error("請先提供 Gemini API Key 才能執行 AI 分析！")
    else:
        # 移除抽象的百分比數字，改用綠意心靈與職能導向的狀態提示
        st.markdown("#### ☘️ 個人天賦原型與本質特質定調 (Talent Archetype & Essence Overview)")
        st.info("💡 系統已略過抽象數字分數，直接進入深度本質、天賦才華與崗位 SOP 的中英雙語文字解析。")

        prompt = f"""
        請擔任 TBM-HR (Tan Boon Ming) 資深首席 HR 顧問與自然生態心靈導師。
        運算 Baseline 必須嚴格基於「華人傳統八字命盤」與「西方生命靈數」之結合。
        請針對以下候選人/員工產出一份**極度詳細、內容豐富、具備大部頭專業水準，且強制採用【中英雙語對照 (Bilingual Chinese & English)】**的深度評估報告：
        - 評估部門 / Department：{target_department}
        - 職業/職務類別 / Job Role：{job_role}
        - 職級 Level / Rank：{candidate_level}
        - 受評估員工 / Employee：{user_name}（生日 / DOB：{birth_date}）
        - 主管生日 / Manager DOB：{manager_birthday}
        - 組織領導層級 / Manager Level：{manager_level}
        
        【特別注意】：**絕對不要出現任何冰冷的百分比或分數（如 92.5% 或 88 分）**。請完全改以具體的「天賦原型（Talent Archetype）」與文字描述來呈現。
        
        【格式要求】：報告中的每一個章節標題與內文解說，皆須包含清晰的【中文】與對應的專業【英文翻譯說明】，確保雙語團隊皆能完全理解。
        
        請務必依照以下五大章節詳細論述：
        1. **【第一章 / Chapter 1】靈魂本質、核心才華與天賦原型深度解構 (Core Essence, Core Talents & Talent Archetype)**：
           - **本質與內在驅動力**：深入剖析其八字五行與生命靈數交織出的靈魂本質與內在渴望。
           - **核心才華與超能力**：精準點出其天生最卓越的才華、思考模式與職場優勢（附英文對照）。
        2. **【第二章】該崗位核心工作綱要 (Job Description & Core Responsibilities)**：針對該部門、職位與職級層級，列出全面且具體的日常、周常與季度核心職責（附英文對照）。
        3. **【第三章】該崗位專屬執行標準作業程序 (Standard Operating Procedure / SOP)**：提供步驟化、標準化的工作執行流程與實務操作守則（附英文對照）。
        4. **【第四章】本質才華與崗位 SOP 之適配性深度分析 (Essence & SOP Fit Analysis)**：詳述其個人本質與才華如何完美對應或補足該崗位 SOP 要求（附英文對照）。
        5. **【第五章】領導協作、主管面談與培育引導指南 (Leadership Collaboration & Interview Guide)**：與直屬主管的互動互補指南、績效考核重點以及面談引導話術（附英文對照）。
        """
        
        try:
            with st.spinner("正在為您進行靈魂本質與核心才華的深度 AI 運算與雙語報告生成中（請稍候）..."):
                report_content = call_essence_gemini(api_key, prompt)
                
            st.success("本質才華解構與中英雙語分析報告已產出！")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(report_content)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as err:
            st.error(f"發生錯誤：{err}")


st.markdown("<br>", unsafe_allow_html=True)


# ==================== 區塊二：群體團隊矩陣與 Excel 上傳分析 ====================
st.markdown('<div class="section-title">🌻 模式二：群體團隊矩陣、本質能量分佈與中英雙語 SOP 藍圖</div>', unsafe_allow_html=True)
st.write("上傳包含團隊成員姓名、生日、**所屬部門**、**職位**與**Level**的 Excel / CSV 檔案，AI 將為整個跨部門團隊進行本質能量分佈、協作藍圖與**中英雙語**解析。")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("上傳團隊名單 Excel / CSV 檔案 (Upload Team Excel/CSV)", type=["csv", "xlsx"], key="team_file")
    
    with st.expander("點此查看建議的 Excel 檔案格式範例 (View Excel Format Example)"):
        st.markdown("""
        您的 Excel 檔案建議包含以下欄位：
        - `姓名` (Name)
        - `生日` (BirthDate)
        - `部門` (Department)
        - `職位` (JobRole)
        - `Level` (Level)
        """)
    st.markdown('</div>', unsafe_allow_html=True)

team_data_str = ""
df_preview = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_preview = pd.read_csv(uploaded_file)
        else:
            df_preview = pd.read_excel(uploaded_file)
        
        st.success(f"成功讀取上傳檔案：{uploaded_file.name}（共 {len(df_preview)} 筆成員資料）")
        st.markdown("#### 📋 上傳名單預覽 (Team Preview)")
        st.dataframe(df_preview.head(5), use_container_width=True)
        
        team_data_str = df_preview.to_string(index=False)
    except Exception as file_err:
        st.error(f"解析檔案時發生錯誤：{file_err}")
else:
    st.info("目前尚未上傳檔案，系統將預設使用跨部門綠意示範團隊矩陣資料進行運算。")
    df_preview = pd.DataFrame([
        {"姓名": "張偉豪", "生日": "1988/05/12", "部門": "創新事業與新領域開創部", "職位": "新事業開發經理", "Level": "Senior Manager"},
        {"姓名": "林雅婷", "生日": "1992/08/15", "部門": "物流與供應鏈管理部", "職位": "物流經理", "Level": "Manager"},
        {"姓名": "陳冠宇", "生日": "1985/11/20", "部門": "資訊科技與數位轉型部", "職位": "資深工程師", "Level": "Senior Specialist"},
        {"姓名": "黃怡君", "生日": "1995/03/02", "部門": "市場行銷與品牌發展部", "職位": "行銷新人", "Level": "Junior"}
    ])
    team_data_str = df_preview.to_string(index=False)

if st.button("開始生成中英雙語團隊本質矩陣與協作 SOP 藍圖報告", key="btn_team_run"):
    if not api_key:
        st.error("請先提供 Gemini API Key 才能執行 AI 分析！")
    else:
        team_prompt = f"""
        請擔任 TBM-HR 資深首席 HR 顧問與團隊自然生態發展專家。
        以「生命靈數」與「華人傳統八字命盤」作為底層雙軌 Baseline。
        請以充滿綠意、包容且具建設性的語調，針對以下跨部門（包含創新事業、行銷、物流、IT等）、跨職級的團隊成員與 Excel 數據，產出一份**極度詳細、結構完整、且強制採用【中英雙語對照 (Bilingual Chinese & English)】的大部頭團隊本質與矩陣報告**：
        - 管理層級基準 / Manager Level：{manager_level}
        - 主管生日 / Manager DOB：{manager_birthday}
        - 團隊成員與獨立分類數據 / Team Data：
        {team_data_str}
        
        【特別注意】：**絕對不要出現任何冰冷的百分比或分數**。請改以團隊整體的「天賦生態原型（Team Talent Ecosystem Archetype）」來分析。
        
        【格式要求】：報告中的每一個章節標題與內文解說，皆須包含清晰的【中文】與對應的專業【英文翻譯說明】，確保雙語團隊皆能完全理解。
        
        請務必分章節詳細論述：
        1. **【第一章 / Chapter 1】團隊整體本質能量與雙軌天賦分佈藍圖 (Team Core Essence & Talent Distribution Blueprint)**：深度剖析跨部門成員的八字五行與生命靈數交織出的團隊整體本質與才華圖譜（附英文對照）。
        2. **【第二章】跨部門與多層級協作藍圖 (Cross-Functional Synergy & Collaboration Blueprint)**：從 CEO 到 Junior、各部門之間的職責互補性與協作默契（附英文對照）。
        3. **【第三章】跨部門標準作業程序 (SOP) 與無縫交接機制 (Cross-Departmental SOP & Handover Mechanism)**：針對部門間協作斷點提出的標準化作業程序與流程對接方案（附英文對照）。
        4. **【第四章】團隊潛在風險與溫和化解指南 (Team Potential Risks & Mitigation Guide)**：運作盲點、壓力點與主管應對策略（附英文對照）。
        5. **【第五章】領導者激勵與戰略佈署指南 (Leadership Motivation & Strategic Deployment Guide)**：針對該領導層級的團隊凝聚力打造方案與培育方針（附英文對照）。
        """
        
        try:
            with st.spinner("正在透過 AI 深度引擎梳理團隊本質矩陣與中英雙語 SOP 藍圖中..."):
                team_report_content = call_essence_gemini(api_key, team_prompt)
                
            st.success("中英雙語團隊本質矩陣與 SOP 分析報告已產出！")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(team_report_content)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as err:
            st.error(f"發生錯誤：{err}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #4CAF50 !important; font-size: 13px;'>© 2026 TBM-HR Platform. Bringing Everything Together ! 🌿 讓每位人才的本質才華與各部門 SOP 在崗位上欣欣向榮 (Empowering multicultural teams globally).</p>", unsafe_allow_html=True)
