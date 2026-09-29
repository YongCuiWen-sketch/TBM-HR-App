import streamlit as st
import google.genai as genai

# 設定網頁標題與基本樣式
st.set_page_config(
    page_title="TBM 全公司 AI 智慧人才與團隊矩陣系統 (安全加密版)",
    page_icon="⭐",
    layout="wide"
)

st.title("⭐ TBM 全公司 AI 智慧人才與團隊矩陣系統 (安全加密版)")
st.write("系統已啟動 Gemini AI 與資安防護，為您提供專業的人才與團隊矩陣深度評估。")

# 側邊欄：部門與職位設定
st.sidebar.header("🏢 評估設定")
department = st.sidebar.selectbox(
    "選擇評估部門",
    ["財務與會計部 (Finance & Accounting)", "研發部 (R&D)", "市場行銷部 (Marketing)", "人力資源部 (HR)"]
)
target_position = st.sidebar.text_input("目標崗位", "資深會計 (Senior Accountant)")
manager_birthday = st.sidebar.date_input("主管生日（用於團隊矩陣對應）")

# 側邊欄：API Key 安全授權
st.sidebar.markdown("---")
st.sidebar.header("🔑 系統安全授權")

api_key = ""
if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("已透過安全通道載入 AI 授權")
else:
    api_key = st.sidebar.text_input("請輸入您的 Gemini API Key", type="password")
    if not api_key:
        st.warning("⚠️ 尚未偵測到有效的 API Key！")

# 主畫面：受評估員工資料
st.markdown("---")
st.subheader("💡 員工潛能與靈數分析評估")

col1, col2 = st.columns(2)
with col1:
    user_name = st.text_input("受評估員工姓名 / 代號", "張小明")
with col2:
    birth_date = st.date_input("受評估員工出生年月日")

if st.button("🚀 開始執行 Gemini AI 深度分析"):
    if not api_key:
        st.error("❌ 請先提供 Gemini API Key 才能執行 AI 分析！")
    else:
        try:
            # 初始化 Google GenAI 用戶端
            client = genai.Client(api_key=api_key)
            
            # 建立詳細的 Prompt
            prompt = f"""
            請擔任專業的企業 HR 顧問與團隊矩陣分析師，針對以下資訊進行深度分析與評估：
            - 評估部門：{department}
            - 目標崗位：{target_position}
            - 受評估員工：{user_name}（出生日期：{birth_date}）
            - 主管生日：{manager_birthday}
            
            請產出詳細的潛能評估、團隊適應性與職涯發展建議報告。
            """
            
            with st.spinner("AI 顧問正在進行深度運算中，請稍候..."):
                # 使用穩定的 gemini-3.8-flash 模型
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt
                )
                
            st.success("✅ 分析完成！")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"❌ 呼叫 AI 時發生錯誤（可能是伺服器暫時繁忙，請稍後再試一次）：{e}")
