import streamlit as st
import google.genai as genai
import pandas as pd
import io

# 設定網頁標題與基本樣式（自然綠意與花草生活風）
st.set_page_config(
    page_title="TBM-HR 智慧人才與人格分析系統",
    page_icon="🌿",
    layout="wide"
)

# 載入自訂 CSS 樣式：清新綠意與大地米白調
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

# 頂部標題區塊（融入綠意花草意象）
st.markdown("""
<div style="padding: 1rem 0; border-bottom: 2px solid #D8E2D8; margin-bottom: 1.5rem;">
    <div style="display: flex; flex-direction: column; gap: 8px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="background-color: #FFFFFF; color: #2E7D32 !important; padding: 0.4rem 0.9rem; border-radius: 0.5rem; font-weight: 700; border: 1px solid #C8D6C8; font-size: 0.95rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
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
                結合東方八字命盤與西方生命靈數雙軌基準，如花草般適性綻放、陪伴團隊自然成長。
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 側邊欄：環境與全域設定
with st.sidebar:
    st.header("🌿 組織與模式設定")
    
    department = st.selectbox(
        "選擇評估部門",
        [
            "零售與門市營運部 (Retail & Store Operations)",
            "客戶服務與售後中心 (Customer Service & Support Centre)", 
            "銷售與業務發展部 (Sales & Business Development)",
            "資訊科技與數位轉型部 (IT & Digital Transformation)",
            "財務與會計部 (Finance & Accounting)", 
            "人力資源與人才發展部 (HR & People Development)"
        ]
    )

    manager_level = st.selectbox(
        "主管 / 領導層級 (由高至低)",
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


# ==================== 區塊一：單人精準人格分析與詳細計分 ====================
st.markdown('<div class="section-title">🌿 模式一：單人深度人格行為與詳細計分適配評估</div>', unsafe_allow_html=True)
st.write("以充滿自然綠意的視角，為個別同仁或候選人進行雙軌基準（八字 + 靈數）天賦與職位適配解析。")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    user_name = st.text_input("受評估員工姓名 / 代號", "張小明", key="single_name")
    birth_date = st.date_input("受評估員工出生年月日", value=pd.to_datetime("1990-01-01"), key="single_birth")
    candidate_position = st.selectbox(
        "應徵 / 擔任職位層級",
        [
            "高階主管 / 業務總監 (Director / Executive)",
            "資深經理 / 分店店長 (Senior Manager)",
            "資深會計 / 資深軟體工程師 / 資深技術員 (Senior Specialist)",
            "業務經理 / 門市企劃 (Manager / Specialist)",
            "會計專員 / IT 專員 / 客服專員 / HR 專員 (Staff / Specialist)",
            "基層人員 / 門市銷售新人 / 實習生 (Junior / Entry-Level / Intern)"
        ],
        key="single_pos"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
if st.button("開始執行單人綠意雙軌與 AI 深度解析", key="btn_single_run"):
    if not api_key:
        st.error("請先提供 Gemini API Key 才能執行 AI 分析！")
    else:
        try:
            mock_score = 92.5
            mock_comm = 88
            mock_stress = 85
            mock_service = 95

            st.markdown("#### ☘️ 個人核心特質儀表板")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("綜合適配指數", f"{mock_score}%", "+2.5%")
            m2.metric("溝通協調力", f"{mock_comm} 分", "和諧")
            m3.metric("抗壓應變力", f"{mock_stress} 分", "穩健")
            m4.metric("TBM 顧客導向度", f"{mock_service} 分", "卓越")

            client = genai.Client(api_key=api_key)
            prompt = f"""
            請擔任 TBM-HR (Tan Boon Ming) 資深 HR 顧問與自然生態心靈導師。
            運算 Baseline 必須嚴格基於「華人傳統八字命盤」與「西方生命靈數」之結合。
            請以充滿綠意、溫暖、鼓勵且具專業洞察的語調，針對以下個別員工進行適配度分析：
            - 評估部門：{department}
            - 受評估員工：{user_name}（生日：{birth_date}）
            - 主管生日：{manager_birthday}
            - 應徵/擔任職位：{candidate_position}
            - 領導層級：{manager_level}
            
            請以清晰優美的排版產出：
            1. 依據雙軌基準解析個人天賦特質與自然行為風格
            2. 與該 TBM 職位的適配優勢與成長潛能（如花草向陽般展現價值）
            3. 日常工作風格與溝通建議
            4. 與該層級領導者的互補與協作指南
            5. 主管關懷與面談引導建議
            """
            
            with st.spinner("正在為您進行充滿綠意的單人雙軌運算中..."):
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
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
st.markdown('<div class="section-title">🌻 模式二：群體團隊矩陣人格分析與 Excel 上傳運算</div>', unsafe_allow_html=True)
st.write("上傳包含團隊成員名單與生日的 Excel / CSV 檔案，系統將自動解構團隊的多元花草能量與互補默契。")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("上傳團隊名單 Excel / CSV 檔案", type=["csv", "xlsx"], key="team_file")
    
    with st.expander("點此查看建議的 Excel 檔案格式範例"):
        st.markdown("""
        您的 Excel 檔案建議包含以下欄位：
        - `姓名` (例如：張偉豪、林雅婷)
        - `生日` (例如：1988/05/12 —— 系統將自動換算雙軌 Baseline)
        - `職位` (例如：資深專員、店鋪經理)
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
    st.info("目前尚未上傳檔案，系統將預設使用綠意示範團隊矩陣資料進行運算。")
    df_preview = pd.DataFrame([
        {"姓名": "張偉豪", "生日": "1988/05/12", "職位": "店鋪經理", "適配評分": 94.5},
        {"姓名": "林雅婷", "生日": "1992/08/15", "職位": "客戶主任", "適配評分": 91.0},
        {"姓名": "陳冠宇", "生日": "1985/11/20", "職位": "資深專員", "適配評分": 88.5},
        {"姓名": "黃怡君", "生日": "1995/03/02", "職位": "行銷專員", "適配評分": 95.2}
    ])
    team_data_str = df_preview.to_string(index=False)

if st.button("開始執行群體矩陣與團隊協作綠意洞察", key="btn_team_run"):
    if not api_key:
        st.error("請先提供 Gemini API Key 才能執行 AI 分析！")
    else:
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"""
            請擔任 TBM-HR 資深 HR 顧問與團隊自然生態發展專家。
            以「生命靈數」與「華人傳統八字命盤」作為底層雙軌 Baseline。
            請以充滿綠意、包容且具建設性的語調，針對以下團隊成員與 Excel 數據進行群體人格矩陣分析：
            - 評估部門：{department}
            - 主管層級：{manager_level}
            - 主管生日：{manager_birthday}
            - 團隊成員與數據：
            {team_data_str}
            
            請以優雅結構化排版產出：
            1. 團隊成員整體雙軌天賦與綠意人格能量分佈概況
            2. 成員間如何發揮互補優勢、像花草生態系般創造和諧協作默契
            3. 團隊潛在溝通盲點與溫和化解建議
            4. 針對該層級領導者的凝聚力打造與激勵指南
            """
            
            with st.spinner("正在為您梳理團隊矩陣與自然協作能量中..."):
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt
                )
                
            st.success("群體團隊協作分析報告已產出！")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"發生錯誤：{e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #4CAF50 !important; font-size: 13px;'>© 2026 TBM-HR Platform. Bringing Everything Together ! 🌿 讓每位人才如花草般在崗位上欣欣向榮。</p>", unsafe_allow_html=True)
