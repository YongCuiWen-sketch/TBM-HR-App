import streamlit as st
import google.genai as genai
import pandas as pd

# 設定網頁標題為 TBM-HR 與基本樣式（寬版佈局，乾淨白底）
st.set_page_config(
    page_title="TBM-HR 智慧人才與人格分析系統",
    page_icon="⭐",
    layout="wide"
)

# 載入自訂 CSS 樣式，精準復刻 TBM 官方網站的純白背景與紅藍標誌
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 頂部導覽列仿造 TBM 官網風格 */
    .tbm-nav-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 0;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 2rem;
    }

    /* 內容卡片與表單區塊 */
    .card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    
    /* 按鈕美化 */
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
        background-color: #C8102E; /* TBM 紅色按鈕 */
        color: white;
        padding: 0.6rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #A50D25;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- 穩定載入 TBM 官方 Logo 與導覽列 -----------------
st.markdown("""
<div class="tbm-nav-bar">
    <div style="display: flex; align-items: center; gap: 20px;">
        <!-- 使用穩定且保證可載入的 TBM 官方 Logo 圖片連結 -->
        <img src="https://shop.tbm.com.my/pub/static/version1713430635/frontend/Codilar/tbm/en_US/images/logo.svg" alt="TBM Logo" style="height: 42px;" onerror="this.onerror=null; this.src='https://www.tbm.com.my/media/logo/default/tbm-logo.png';">
        <span style="font-size: 1.1rem; font-weight: 700; color: #1E3A8A; border-left: 2px solid #CBD5E1; padding-left: 15px;">
            Bringing Everything Together ! &nbsp;|&nbsp; TBM-HR 智慧決策與人格分析平台
        </span>
    </div>
    <div>
        <span style="background-color: #FEF2F2; color: #C8102E; padding: 0.4rem 0.8rem; border-radius: 2rem; font-size: 0.85rem; font-weight: 600; border: 1px solid #FECACA;">
            ⭐ TBM-HR Portal
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# 側邊欄：環境與全域設定
with st.sidebar:
    st.image("https://img.icons8.com/color/96/manager.png", width=60)
    st.header("⚙️ TBM-HR 組織與模式設定")
    
    department = st.selectbox(
        "🏢 選擇評估部門",
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
        "👔 主管 / 領導層級 (由高至低)",
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

    manager_birthday = st.sidebar.date_input("📅 主管 / 領導者生日（人格靈數對應）")
    
    st.markdown("---")
    
    # API Key 安全授權
    api_key = ""
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.sidebar.success("🔒 已透過安全通道載入 AI 授權")
    else:
        api_key = st.sidebar.text_input("🔑 輸入 Gemini API Key", type="password")
        if not api_key:
            st.sidebar.warning("⚠️ 尚未偵測到 API Key！")

# 使用現代化的分頁籤 (Tabs) 切換單人與群體模式
tab1, tab2 = st.tabs(["👤 單人精準人格分析模式", "👥 群體 / 團隊矩陣人格分析模式（支援 Excel）"])

# ==================== 模式一：單人精準人格分析 ====================
with tab1:
    st.markdown("### 💡 TBM-HR 夥伴潛能、人格特質與適配度深度解析")
    st.write("針對應徵 TBM 各大部門的候選人或現職員工進行專業的人格行為風格分析。")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            user_name = st.text_input("👤 受評估員工姓名 / 代號", "張小明")
        with col2:
            birth_date = st.date_input("🎂 受評估員工出生年月日", value=pd.to_datetime("1990-01-01"))
        with col3:
            # 職位層級嚴格由高到低排列
            candidate_position = st.selectbox(
                "🎯 應徵 / 擔任職位層級 (由高至低)",
                [
                    "高階主管 / 業務總監 (Director / Executive)",
                    "資深經理 / 分店店長 (Senior Manager)",
                    "資深會計 / 資深軟體工程師 / 資深技術員 (Senior Specialist)",
                    "業務經理 / 門市企劃 (Manager / Specialist)",
                    "會計專員 / IT 專員 / 客服專員 / HR 專員 (Staff / Specialist)",
                    "基層人員 / 門市銷售新人 / 實習生 (Junior / Entry-Level / Intern)",
                    "其他自訂職位"
                ]
            )
        
        if candidate_position == "其他自訂職位":
            candidate_position = st.text_input("請輸入具體職位名稱", "資深零售專員")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("🚀 開始執行 TBM-HR 單人 AI 人格深度分析", key="btn_single"):
        if not api_key:
            st.error("❌ 請先提供 Gemini API Key 才能執行 AI 分析！")
        else:
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                請擔任 TBM-HR (Tan Boon Ming) 馬來西亞知名家電與一站式服務企業的資深 HR 顧問與人格分析專家。
                TBM 的企業使命是「Ensuring the right appliance for all」，願景是成為「One-stop solution center with best-in-class service」。
                
                請針對以下個別候選人/員工進行符合 TBM 企業文化的人格行為風格與適配度深度分析：
                - 評估部門：{department}
                - 受評估員工職位：{candidate_position}
                - 領導/主管層級：{manager_level}
                - 主管/領導者生日：{manager_birthday}
                - 受評估員工：{user_name}（出生日期：{birth_date}）
                
                請以清晰優美的結構化排版（包含標題與重點條列）產出：
                1. 個人人格特質與生命靈數行為風格解析（是否具備 TBM 重視的誠信、熱忱與服務精神）
                2. 與該 TBM 職位的適配度評估（人格優勢與潛在盲點）
                3. 部門工作行為風格建議（是否適合該零售/技術/後勤部門）
                4. 與該層級領導者（如 CEO 或 TA）的互動適應性與協作風格
                5. TBM-HR 面試時建議主考官詢問的關鍵人格與情境問題
                6. 長期在 TBM 體系下的人格成長與職涯發展建議報告
                """
                
                with st.spinner("✨ TBM-HR 顧問正在進行人格與潛能深度運算中，請稍候..."):
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt
                    )
                    
                st.success("🎉 TBM-HR 個人人格深度分析報告已完成！")
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ 呼叫 AI 時發生錯誤：{e}")

# ==================== 模式二：群體人格矩陣分析 ====================
with tab2:
    st.markdown("### 👥 TBM-HR 群體團隊人格矩陣與協作分析")
    st.write("透過上傳 Excel / CSV 檔案，一次性分析 TBM 團隊的人格結構分佈與團隊協作默契。")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("📂 上傳 TBM 員工名單檔案 (支援 .csv 或 .xlsx 格式，需包含姓名與生日欄位)", type=["csv", "xlsx"])
        
        with st.expander("📝 或者直接手動貼上 TBM 團隊名單（選填備用）"):
            team_members_input = st.text_area(
                "團隊成員名單與生日（每行一位，例如：張小明 1987/06/15）",
                value="張小明 1987/06/15\n王小美 1990/11/20\n李大華 1985/03/10"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("🚀 開始執行 TBM-HR 群體團隊人格矩陣分析", key="btn_team"):
        if not api_key:
            st.error("❌ 請先提供 Gemini API Key 才能執行 AI 分析！")
        else:
            team_data_str = ""
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    team_data_str = df.to_string(index=False)
                    st.success(f"✅ 成功讀取檔案：{uploaded_file.name}，共 {len(df)} 筆成員資料！")
                except Exception as file_err:
                    st.error(f"❌ 讀取檔案失敗：{file_err}")
            else:
                team_data_str = team_members_input
                st.info("ℹ️ 未上傳檔案，將使用上方手動輸入的名單進行分析。")
            
            if team_data_str:
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    請擔任 TBM-HR (Tan Boon Ming) 馬來西亞頂尖家電與一站式服務企業的資深 HR 顧問與團隊人格矩陣分析師。
                    TBM 致力於提供最佳的客戶服務與一站式解決方案（One-stop solution center）。
                    
                    請針對以下整個團隊進行專業的群體人格矩陣與協作綜合分析：
                    - 評估部門：{department}
                    - 領導/主管層級：{manager_level}
                    - 目標崗位/團隊方向：TBM 零售與售後服務卓越戰力配置
                    - 主管/領導者生日：{manager_birthday}
                    - 團隊成員與生日清單：
                    {team_data_str}
                    
                    請以清晰優美的結構化排版（包含標題與重點條列）產出：
                    1. TBM 團隊成員整體人格特質分佈與靈數矩陣概況
                    2. 成員間的人格互補性與協作默契分析
                    3. 團隊整體行為優勢與潛在盲點/風險
                    4. 針對該層級領導者（如 CEO 或 TA）如何依據團隊人格特質進行領導、激勵與佈署的具體戰略建議
                    """
                    
                    with st.spinner("✨ TBM-HR 顧問正在進行團隊人格矩陣大數據運算中，請稍候..."):
                        response = client.models.generate_content(
                            model='gemini-1.5-flash',
                            contents=prompt
                        )
                        
                    st.success("🎉 TBM-HR 群體團隊人格分析報告已完成！")
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ 呼叫 AI 時發生錯誤：{e}")
