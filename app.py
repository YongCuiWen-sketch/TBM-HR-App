import streamlit as st
from google import genai
import pandas as pd
import io

# 設定網頁標題與基本樣式（自然綠意與花草生活風）
st.set_page_config(
    page_title="TBM-HR 智慧人才與人格分析系統",
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
    p {
        color: #4A5568 !important;
    }
    .card {
        background-color: #FFFFFF;
        padding: 1.5rem;
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
                🌱 TBM 綠野心靈與天賦空間
            </div>
            <span style="background-color: #E8F5E9; color: #2E7D32 !important; padding: 0.3rem 0.8rem; border-radius: 2rem; font-size: 0.8rem; font-weight: 600; border: 1px solid #C8E6C9;">
                Bringing Everything Together ! 🌿
            </span>
        </div>
        <div>
            <h1 style="font-size: 1.6rem; font-weight: 700; margin: 4px 0 2px 0; color: #1B5E20 !important;">
                TBM-HR 智慧決策與人格分析平台
            </h1>
            <p style="font-size: 0.9rem; color: #388E3C !important; margin: 0;">
                結合東方八字命盤與西方生命靈數雙軌基準，自動生成各部門專屬 SOP 與崗位綱要，陪伴團隊自然成長。
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
            "CEO (最高執行長)",
            "TA (直屬營運主管 / Team Leader)",
            "高層 (Executive / C-Level Director)",
            "經理 (Branch / Department Manager)",
            "IT 資訊科技主管 (IT Manager / Head of IT)",
            "資深專員 / 專業技師 (Senior Specialist)",
            "基層服務人員 / 新人 (Junior / Frontline Staff)"
        ]
    )

    manager_birthday = st.sidebar.date_input("主管 / 領導者生日（雙基底對應）")
    
    st.markdown("---")
    
    api_key = ""
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.sidebar.success("已透過安全通道載入 AI 授權")
    else:
        api_key = st.sidebar.text_input("輸入 Gemini API Key", type="password")
        if not api_key:
            st.sidebar.warning("尚未偵測到 API Key！")


# ==================== 區塊一：單人精準人格分析與獨立分類設定 ====================
st.markdown('<div class="section-title">🌿 模式一：單人深度人格行為、崗位綱要與 SOP 智慧評估</div>', unsafe_allow_html=True)
st.write("精確選取員工所屬**部門**、**職業/職務類別**與**職級 Level**，系統將結合雙軌天賦，自動為該崗位量身打造專屬 SOP 與工作綱要。")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("受評估員工姓名 / 應徵者代號", "張小明", key="single_name")
        birth_date = st.date_input("受評估員工出生年月日", value=pd.to_datetime("1990-01-01"), key="single_birth")
    
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
    
if st.button("開始執行單人雙軌天賦與崗位 SOP 深度解析", key="btn_single_run"):
    if not api_key:
        st.error("請先提供 Gemini API Key 才能執行 AI 分析！")
    else:
        try:
            mock_score = 92.5
            mock_comm = 88
            mock_stress = 85
            mock_service = 95

            st.markdown("#### ☘️ 個人核心特質與崗位適配儀表板")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("綜合適配指數", f"{mock_score}%", "+2.5%")
            m2.metric("溝通協調力", f"{mock_comm} 分", "和諧")
            m3.metric("抗壓應變力", f"{mock_stress} 分", "穩健")
            m4.metric("TBM 顧客導向度", f"{mock_service} 分", "卓越")

            client = genai.Client(api_key=api_key)
            prompt = f"""
            請擔任 TBM-HR (Tan Boon Ming) 資深 HR 顧問與自然生態心靈導師。
            運算 Baseline 必須嚴格基於「華人傳統八字命盤」與「西方生命靈數」之結合。
            請針對以下獨立分類條件之候選人/員工進行深度適配與工作執行解析：
            - 評估部門：{target_department}
            - 職業/職務類別：{job_role}
            - 職級 Level：{candidate_level}
            - 受評估員工：{user_name}（生日：{birth_date}）
            - 主管生日：{manager_birthday}
            - 組織領導層級：{manager_level}
            
            請以充滿綠意、溫暖、專業且結構化的排版產出以下內容：
            1. **雙軌天賦與人格特質解析**：依據八字與靈數拆解其天生優勢與行為風格。
            2. **該崗位核心工作綱要 (Job Description)**：針對「{target_department}」部門之「{job_role}」與「{candidate_level}」層級，列出其核心職責。
            3. **該崗位專屬執行標準作業程序 (SOP)**：為此特定崗位量身規劃日常、周常與專案執行的關鍵步驟與標準化流程建議。
            4. **天賦與崗位適配優勢**：分析其人格特質如何完美對應該崗位的 SOP 要求。
            5. **領導協作與主管面談建議**：與直屬主管的互動指南及培育引導方針。
            """
            
            with st.spinner("正在為您結合雙軌天賦與崗位專屬 SOP 運算中..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
            st.success("分析報告已完成！")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"發生錯誤：{e}")


st.markdown("<br>", unsafe_allow_html=True)


# ==================== 區塊二：群體團隊矩陣與 Excel 上傳分析 ====================
st.markdown('<div class="section-title">🌻 模式二：群體團隊矩陣人格分析、跨部門協作與 SOP 總覽</div>', unsafe_allow_html=True)
st.write("上傳包含團隊成員姓名、生日、**所屬部門**、**職位**與**Level**的 Excel / CSV 檔案，系統將自動分析跨部門團隊的協作默契與整體作業 SOP 藍圖。")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("上傳團隊名單 Excel / CSV 檔案", type=["csv", "xlsx"], key="team_file")
    
    with st.expander("點此查看建議的 Excel 檔案格式範例"):
        st.markdown("""
        您的 Excel 檔案建議包含以下欄位：
        - `姓名` (例如：張偉豪、林雅婷)
        - `生日` (例如：1988/05/12 —— 系統將自動換算雙軌 Baseline)
        - `部門` (例如：創新事業與新領域開創部、市場行銷與品牌發展部、物流與供應鏈管理部)
        - `職位` (例如：新事業開發經理、品牌企劃、物流調度)
        - `Level` (例如：CEO、Senior Manager、Specialist、Junior)
        - `適配評分` (例如：92.5)
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
        st.markdown("#### 📋 上傳名單預覽")
        st.dataframe(df_preview.head(5), use_container_width=True)
        
        team_data_str = df_preview.to_string(index=False)
    except Exception as file_err:
        st.error(f"解析檔案時發生錯誤：{file_err}")
else:
    st.info("目前尚未上傳檔案，系統將預設使用跨部門綠意示範團隊矩陣資料進行運算。")
    df_preview = pd.DataFrame([
        {"姓名": "張偉豪", "生日": "1988/05/12", "部門": "創新事業與新領域開創部", "職位": "新事業開發經理", "Level": "Senior Manager", "適配評分": 95.0},
        {"姓名": "林雅婷", "生日": "1992/08/15", "部門": "物流與供應鏈管理部", "職位": "物流經理", "Level": "Manager", "適配評分": 91.0},
        {"姓名": "陳冠宇", "生日": "1985/11/20", "部門": "資訊科技與數位轉型部", "職位": "資深工程師", "Level": "Senior Specialist", "適配評分": 88.5},
        {"姓名": "黃怡君", "生日": "1995/03/02", "部門": "市場行銷與品牌發展部", "職位": "行銷新人", "Level": "Junior", "適配評分": 93.2}
    ])
    team_data_str = df_preview.to_string(index=False)

if st.button("開始執行群體矩陣、跨部門協作與 SOP 藍圖洞察", key="btn_team_run"):
    if not api_key:
        st.error("請先提供 Gemini API Key 才能執行 AI 分析！")
    else:
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"""
            請擔任 TBM-HR 資深 HR 顧問與團隊自然生態發展專家。
            以「生命靈數」與「華人傳統八字命盤」作為底層雙軌 Baseline。
            請以充滿綠意、包容且具建設性的語調，針對以下跨部門（包含創新事業、行銷、物流、IT等）、跨職級的團隊成員與 Excel 數據進行群體人格矩陣與工作 SOP 分析：
            - 管理層級基準：{manager_level}
            - 主管生日：{manager_birthday}
            - 團隊成員與獨立分類數據：
            {team_data_str}
            
            請以優雅結構化排版產出：
            1. **團隊整體雙軌天賦與綠意人格能量分佈**：分析跨部門成員的天賦組合。
            2. **跨部門與多層級協作藍圖**：從 CEO 到 Junior、各部門（創新開創、物流、行銷、IT等）之間的職責互補性與協作默契。
            3. **跨部門作業標準與交接 SOP 建議**：針對不同部門間的協作斷點，提出標準化作業程序（SOP）與溝通對接優化方案。
            4. **團隊潛在盲點與溫和化解指南**：團隊運作風險與主管應對策略。
            5. **領導者激勵與戰略佈署指南**：針對該領導層級的團隊凝聚力打造方案。
            """
            
            with st.spinner("正在為您梳理跨部門團隊矩陣、各部門 SOP 與協作藍圖中..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
            st.success("群體團隊協作與 SOP 分析報告已產出！")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"發生錯誤：{e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #4CAF50 !important; font-size: 13px;'>© 2026 TBM-HR Platform. Bringing Everything Together ! 🌿 讓每位人才與各部門 SOP 在崗位上欣欣向榮。</p>", unsafe_allow_html=True)
