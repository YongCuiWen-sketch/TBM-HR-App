import streamlit as st
import google.genai as genai
import pandas as pd

# 設定網頁標題與基本樣式
st.set_page_config(
    page_title="TBM 全公司 AI 智慧人才與團隊矩陣系統",
    page_icon="⭐",
    layout="wide"
)

st.title("⭐ TBM 全公司 AI 智慧人才與團隊矩陣系統")
st.write("歡迎使用 AI 智慧人才與團隊矩陣評估系統。請在側邊欄選擇評估模式與相關背景條件。")

# 側邊欄：部門與模式設定
st.sidebar.header("🏢 評估與模式設定")

# 模式選擇
analysis_mode = st.sidebar.radio(
    "選擇分析模式",
    ["👤 單人精準評估模式", "👥 群體 / 團隊矩陣分析模式（支援 Excel 上傳）"]
)

# 部門選項（已加入 IT 資訊科技部）
department = st.sidebar.selectbox(
    "選擇評估部門",
    [
        "財務與會計部 (Finance & Accounting)", 
        "研發部 (R&D)", 
        "市場行銷部 (Marketing)", 
        "銷售與業務部 (Sales & Business Development)",
        "資訊科技部 / IT Department (Information Technology)",
        "人力資源部 (HR)"
    ]
)

# 主管/領導層級選項（包含 CEO、TA 與 IT 部門相關）
manager_level = st.sidebar.selectbox(
    "主管 / 領導層級",
    [
        "CEO (最高執行長)",
        "TA (直屬主管 / Team Leader)",
        "高層 (Executive / C-Level)",
        "經理 (Manager)",
        "IT 資訊科技主管 (IT Manager / Head of IT)",
        "資深 / 專業人員 (Senior / Specialist)",
        "基層 / 新人 (Junior / Entry-Level)"
    ]
)

target_position = st.sidebar.text_input("目標崗位 / 職位", "資深軟體工程師 / IT 專員 (Senior IT Specialist)")
manager_birthday = st.sidebar.date_input("主管 / 領導者生日（用於團隊矩陣對應）")

# 側邊欄：API Key 安全授權
api_key = ""
if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("已透過安全通道載入 AI 授權")
else:
    api_key = st.sidebar.text_input("請輸入您的 Gemini API Key", type="password")
    if not api_key:
        st.sidebar.warning("⚠️ 尚未偵測到有效的 API Key！")

# 主畫面根據模式切換
st.markdown("---")

if analysis_mode == "👤 單人精準評估模式":
    st.subheader("💡 單人潛能與靈數分析評估")
    
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("受評估員工姓名 / 代號", "張小明")
    with col2:
        birth_date = st.date_input("受評估員工出生年月日")
        
    if st.button("🚀 開始執行單人 AI 深度分析"):
        if not api_key:
            st.error("❌ 請先提供 Gemini API Key 才能執行 AI 分析！")
        else:
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                請擔任專業的企業 HR 顧問與團隊矩陣分析師，針對以下個別員工進行深度分析與評估：
                - 評估部門：{department}
                - 領導/主管層級：{manager_level}
                - 目標崗位：{target_position}
                - 主管/領導者生日：{manager_birthday}
                - 受評估員工：{user_name}（出生日期：{birth_date}）
                
                請產出詳細的個人潛能評估、與該層級領導者（如 CEO 或 TA）的互動適應性、是否適合該部門或建議調往其他部門、面試時該問的關鍵問題、建議員工在面試中展現的優勢，以及職涯發展建議報告。
                """
                
                with st.spinner("AI 顧問正在進行個人深度運算中，請稍候..."):
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt
                    )
                    
                st.success("✅ 個人分析完成！")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"❌ 呼叫 AI 時發生錯誤：{e}")

else:
    st.subheader("👥 群體 / 團隊矩陣綜合分析（Excel 檔案上傳）")
    st.write("請上傳包含員工名單的 **CSV 或 Excel 檔案**（檔案內需包含「姓名」與「生日」欄位）。")
    
    uploaded_file = st.file_uploader("上傳員工名單檔案", type=["csv", "xlsx"])
    
    with st.expander("或者直接手動貼上名單（選填）"):
        team_members_input = st.text_area(
            "團隊成員名單與生日（每行一位）",
            value="張小明 1987/06/15\n王小美 1990/11/20\n李大華 1985/03/10"
        )
    
    if st.button("🚀 開始執行群體團隊矩陣分析"):
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
                    st.success(f"✅ 成功讀取檔案：{uploaded_file.name}，共 {len(df)} 筆資料！")
                except Exception as file_err:
                    st.error(f"❌ 讀取檔案失敗：{file_err}")
            else:
                team_data_str = team_members_input
                st.info("ℹ️ 未上傳檔案，將使用上方手動輸入的名單進行分析。")
            
            if team_data_str:
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    請擔任專業的企業 HR 顧問與團隊矩陣分析師，針對以下整個團隊進行群體矩陣與協作分析：
                    - 評估部門：{department}
                    - 領導/主管層級：{manager_level}
                    - 目標崗位/團隊方向：{target_position}
                    - 主管/領導者生日：{manager_birthday}
                    - 團隊成員與生日清單：
                    {team_data_str}
                    
                    請產出詳細的團隊成員互補性、群體靈數矩陣分佈、團隊優勢、潛在盲點，以及該層級領導者（如 CEO 或 TA）如何領導與佈署這個團隊的綜合建議報告。
                    """
                    
                    with st.spinner("AI 顧問正在進行團隊矩陣運算中，請稍候..."):
                        response = client.models.generate_content(
                            model='gemini-1.5-flash',
                            contents=prompt
                        )
                        
                    st.success("✅ 群體團隊分析完成！")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"❌ 呼叫 AI 時發生錯誤：{e}")
