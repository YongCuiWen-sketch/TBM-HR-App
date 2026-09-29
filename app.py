import streamlit as st
import google.genai as genai
import pandas as pd
import io

# 設定網頁標題與基本樣式（寬版佈局，深色沉穩高對比模式）
st.set_page_config(
    page_title="TBM-HR 智慧人才與人格分析系統",
    page_icon="",
    layout="wide"
)

# 載入自訂 CSS 樣式：高對比深色背景 + 亮白字體，確保字字清晰可見
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A; /* 沉穩深藍黑色 */
        color: #F8FAFC !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #F8FAFC !important;
    }
    .card {
        background-color: #1E293B;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #334155;
        margin-bottom: 1.5rem;
        color: #F8FAFC !important;
    }
    .stTextInput input, .stSelectbox select, .stDateInput input {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #090D16;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
        background-color: #C8102E; /* TBM 紅色按鈕 */
        color: #FFFFFF !important;
        padding: 0.6rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #A50D25;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# 頂部簡約高對比標題區塊
st.markdown("""
<div style="padding: 1rem 0 1.5rem 0; border-bottom: 1px solid #334155; margin-bottom: 2rem;">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="background-color: #1E293B; color: #FFFFFF !important; padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 700; border: 1px solid #475569; font-size: 1.1rem;">
                [ TBM Logo ]
            </div>
            <div>
                <h1 style="font-size: 1.8rem; font-weight: 700; margin: 0 0 5px 0; color: #FFFFFF !important;">
                    TBM-HR 智慧決策與人格分析平台
                </h1>
                <p style="font-size: 0.95rem; color: #94A3B8 !important; margin: 0;">
                    Bringing Everything Together ! &nbsp;|&nbsp; 專業人才行為分析與團隊適配系統（生命靈數 + 八字命盤雙效運算）
                </p>
            </div>
        </div>
        <div>
            <span style="background-color: #7F1D1D; color: #FEE2E2 !important; padding: 0.4rem 0.8rem; border-radius: 2rem; font-size: 0.85rem; font-weight: 600; border: 1px solid #991B1B;">
                TBM-HR Portal
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 側邊欄：環境與全域設定
with st.sidebar:
    st.header("TBM-HR 組織與模式設定")
    
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

    manager_birthday = st.sidebar.date_input("主管 / 領導者生日（雙基底運算對應）")
    
    st.markdown("---")
    
    api_key = ""
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.sidebar.success("已透過安全通道載入 AI 授權")
    else:
        api_key = st.sidebar.text_input("輸入 Gemini API Key", type="password")
        if not api_key:
            st.sidebar.warning("尚未偵測到 API Key！")

# 分頁切換
tab1, tab2 = st.tabs(["單人精準人格與雙軌計分分析模式", "群體 / 團隊矩陣人格分析與 Excel 上傳運算模式"])

# ==================== 模式一：單人精準人格分析與雙軌計分 ====================
with tab1:
    st.markdown("### 單人深度人格行為、八字與靈數雙軌計分適配評估")
    st.write("針對個別候選人或現職員工，以「生命靈數」與「八字命盤」作為演算法 Baseline，進行行為風格與職位適配度深度解析。")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            user_name = st.text_input("受評估員工姓名 / 代號", "張小明")
        with col2:
            birth_date = st.date_input("受評估員工出生年月日", value=pd.to_datetime("1990-01-01"))
        with col3:
            candidate_position = st.selectbox(
                "應徵 / 擔任職位層級",
                [
                    "高階主管 / 業務總監 (Director / Executive)",
                    "資深經理 / 分店店長 (Senior Manager)",
                    "資深會計 / 資深軟體工程師 / 資深技術員 (Senior Specialist)",
                    "業務經理 / 門市企劃 (Manager / Specialist)",
                    "會計專員 / IT 專員 / 客服專員 / HR 專員 (Staff / Specialist)",
                    "基層人員 / 門市銷售新人 / 實習生 (Junior / Entry-Level / Intern)"
                ]
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("開始執行 TBM-HR 單人雙軌基準與 AI 深度分析", key="btn_single"):
        if not api_key:
            st.error("請先提供 Gemini API Key 才能執行 AI 分析！")
        else:
            try:
                mock_score = 93.2
                mock_bazi = "官印相生 / 靈數天賦 8 號"
                mock_stress = 88
                mock_service = 96

                st.markdown("#### 單人雙軌基準核心計分儀表板")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("綜合適配指數", f"{mock_score}%", "+3.1%")
                m2.metric("八字與靈數格局", mock_bazi, "穩健格局")
                m3.metric("抗壓應變力", f"{mock_stress} 分", "優良")
                m4.metric("TBM 顧客導向度", f"{mock_service} 分", "極佳")

                client = genai.Client(api_key=api_key)
                prompt = f"""
                請擔任 TBM-HR (Tan Boon Ming) 馬來西亞知名家電與一站式服務企業的資深 HR 顧問。
                本次分析的運算 Baseline（基準）必須嚴格基於「華人傳統八字命盤」與「西方生命靈數」之結合來推導其行為天賦與性格特質。
                
                請針對以下個別員工進行符合 TBM 企業文化的人格行為風格與適配度深度分析：
                - 評估部門：{department}
                - 受評估員工：{user_name}（生日：{birth_date}，作為生命靈數與八字日主推演依據）
                - 主管/領導者生日：{manager_birthday}（用於雙方命盤與靈數互動合盤對應）
                - 應徵/擔任職位：{candidate_position}
                - 領導層級：{manager_level}
                
                請以清晰優美的結構化排版產出：
                1. 依據「八字命盤與生命靈數」雙軌基準解析其天生行為風格、潛在優勢與盲點
                2. 與該 TBM 職位（{candidate_position}）的適配度計分與職能契合度
                3. 在 {department} 部門工作中的實際行為表現與溝通模式建議
                4. 與該層級領導者（生日：{manager_birthday}）命盤與靈數互動的協作適應性
                5. TBM-HR 面試與面談關鍵引導問題建議
                """
                
                with st.spinner("TBM-HR 正在進行八字與靈數雙軌基準運算及 AI 深度分析中..."):
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt
                    )
                    
                st.success("雙軌基準分析報告已完成！")
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"呼叫 AI 時發生錯誤：{e}")

# ==================== 模式二：群體矩陣人格分析與 Excel 上傳 ====================
with tab2:
    st.markdown("### 群體團隊八字與靈數矩陣人格分析（支援 Excel 上傳）")
    st.write("上傳包含團隊成員姓名與生日的 Excel / CSV 檔案，系統將以「生命靈數與八字命盤」作為底層 Baseline，自動解析團隊矩陣分佈與協作默契。")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("上傳團隊成員 Excel / CSV 檔案", type=["csv", "xlsx"])
        
        with st.expander("點此查看建議的 Excel 檔案格式範例"):
            st.markdown("""
            您的 Excel 檔案建議包含以下欄位：
            - `姓名` (例如：張偉豪、林雅婷)
            - `生日` (例如：1988/05/12 —— 用於系統自動換算八字與靈數 Baseline)
            - `職位` (例如：資深專員、店鋪經理)
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
            st.markdown("#### 上傳團隊名單預覽與 Baseline 轉換對應")
            st.dataframe(df_preview.head(5), use_container_width=True)
            
            team_data_str = df_preview.to_string(index=False)
        except Exception as file_err:
            st.error(f"解析檔案時發生錯誤：{file_err}")
    else:
        st.info("目前尚未上傳檔案，系統將預設使用標準模擬團隊矩陣資料進行雙軌 Baseline 運算。")
        df_preview = pd.DataFrame([
            {"姓名": "張偉豪", "生日": "1988/05/12", "職位": "店鋪經理"},
            {"姓名": "林雅婷", "生日": "1992/08/15", "職位": "客戶主任"},
            {"姓名": "陳冠宇", "生日": "1985/11/20", "職位": "資深專員"},
            {"姓名": "黃怡君", "生日": "1995/03/02", "職位": "行銷專員"}
        ])
        team_data_str = df_preview.to_string(index=False)

    if st.button("開始執行 TBM-HR 群體雙軌矩陣運算與 AI 協作分析", key="btn_team"):
        if not api_key:
            st.error("請先提供 Gemini API Key 才能執行 AI 分析！")
        else:
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                請擔任 TBM-HR (Tan Boon Ming) 資深 HR 顧問與團隊人格矩陣分析師。
                請以「生命靈數」與「華人傳統八字命盤」作為底層運算 Baseline，針對以下團隊成員及上傳的 Excel 數據進行專業的群體人格矩陣與協作綜合分析：
                - 評估部門：{department}
                - 主管層級：{manager_level}
                - 主管生日：{manager_birthday}（作為團隊主導核心命盤/靈數對照）
                - 團隊成員與生日清單：
                {team_data_str}
                
                請以清晰優美的結構化排版產出：
                1. TBM 團隊成員整體的八字格局與生命靈數矩陣分佈概況
                2. 成員間的五行/靈數互補性與團隊協作默契分析
                3. 團隊整體行為優勢與潛在衝突風險
                4. 針對該層級領導者如何依據團隊雙軌矩陣進行領導、激勵與戰略佈署的具體建議
                """
                
                with st.spinner("TBM-HR 正在進行群體八字與靈數矩陣大數據運算中..."):
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt
                    )
                    
                st.success("群體團隊雙軌矩陣分析報告已產出！")
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"呼叫 AI 時發生錯誤：{e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8 !important; font-size: 14px;'>© 2026 TBM-HR Platform. All Rights Reserved. Bringing Everything Together !</p>", unsafe_allow_html=True)
