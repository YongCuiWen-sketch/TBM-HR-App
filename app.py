import streamlit as st
import google.genai as genai

# 設定網頁標題與基本樣式
st.set_page_config(
    page_title="TBM 全公司 AI 智慧人才與團隊矩陣系統 (安全加密版)",
    page_icon="⭐",
    layout="wide"
)

st.title("⭐ TBM 全公司 AI 智慧人才與團隊矩陣系統 (安全加密版)")
st.write("當前評估部門：【財務與會計部 (Finance & Accounting)】 | 目標崗位：【資深會計 (Senior Accountant)】。系統已啟動 Gemini AI 與資安防護。")

# 側邊欄：API Key 設定
st.sidebar.header("🔑 系統安全授權")

# 優先檢查 Streamlit Secrets，若無則讓使用者手動輸入
api_key = ""
if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("已透過安全通道載入 AI 授權")
else:
    api_key = st.sidebar.text_input("請輸入您的 Gemini API Key", type="password")
    if not api_key:
        st.warning("⚠️ 尚未偵測到有效的 Gemini API Key，請在左側輸入或在 Streamlit Secrets 中設定！")

# 接收使用者輸入或顯示評估介面
st.markdown("---")
st.subheader("💡 員工潛能與靈數分析評估")

user_name = st.text_input("受評估員工姓名 / 代號", "張小明")
birth_date = st.date_input("出生年月日")

if st.button("🚀 開始執行 Gemini AI 深度分析"):
    if not api_key:
        st.error("❌ 請先提供 Gemini API Key 才能執行 AI 分析！")
    else:
        try:
            # 初始化 Google GenAI 用戶端
            client = genai.Client(api_key=api_key)
            
            # 建立 Prompt
            prompt = f"請針對員工 {user_name}（出生日期：{birth_date}），為其在財務與會計部資深會計崗位進行 AI 智慧人才與團隊矩陣的深度分析與職涯建議。"
            
            with st.spinner("AI 顧問正在進行深度運算中..."):
                # 使用最新的 gemini-3.8-flash 模型
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt
                )
                
            st.success("✅ 分析完成！")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"❌ 呼叫 AI 時發生錯誤，請檢查您的 API Key 是否正確或網路連線：{e}")
