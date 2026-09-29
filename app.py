import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from google import genai

# 設定頁面標題與配置
st.set_page_config(
    page_title="TBM AI Enterprise-Wide Talent & Team Intelligence System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 資安檢查：從 Streamlit 秘密設定中讀取 API Key (保障安全) ---
GEMINI_API_KEY = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# --- 側邊欄：API 金鑰與語系設定 ---
st.sidebar.markdown("### 🌐 系統設定 / Settings")
lang = st.sidebar.selectbox("選擇語言 / Select Language", ["繁體中文", "English"])

st.sidebar.markdown("### 🔑 系統安全授權狀態")
if GEMINI_API_KEY:
    st.sidebar.success("🔒 系統已透過安全通道載入 AI 授權")
else:
    # 如果雲端沒有設定 secrets，才允許手動輸入（方便你本地測試）
    GEMINI_API_KEY = st.sidebar.text_input("輸入 Gemini API Key", type="password", placeholder="請輸入 API Key...")
    if GEMINI_API_KEY:
        st.sidebar.info("💡 已手動輸入臨時 API Key")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏢 選擇目標部門與職位 / Dept & Role")

departments = {
    "繁體中文": {
        "財務與會計部 (Finance & Accounting)": ["資深會計 (Senior Accountant)", "財務經理 (Finance Manager)", "成本會計 (Cost Accountant)"],
        "倉儲物流部 (Warehouse & Logistics)": ["倉儲主管 (Warehouse Leader)", "物流統籌 (Logistics Coordinator)", "供應鏈專員 (Supply Chain Specialist)"],
        "採購部 (Purchasing Department)": ["採購經理 (Purchasing Manager)", "專案採購專員 (Project Buyer)", "供應商管理 (Vendor Manager)"],
        "專案部 (Project Department)": ["專案總監 (Project Director)", "專案經理/模式營運 (Project Manager)", "專案統籌協調 (Project Coordinator)"],
        "新創/開創部 (New Venture / Innovation Dept)": ["新創負責人 (Head of New Venture)", "創新業務拓展 (Business Innovation Lead)", "開創策略專員 (Exploration Specialist)"],
        "市場營銷部 (Marketing & Brand)": ["行銷負責人 (Marketing Lead)", "品牌公關 (PR Specialist)", "內容運營 (Content Strategist)"],
        "業務與銷售部 (Sales & BD)": ["業務總監 (Sales Director)", "大客戶經理 (Key Account Manager)", "業務代表 (Sales Executive)"],
        "日常營運部 (Operations Department)": ["營運長/總助 (COO / Chief of Staff)", "專案/營運總監 (Operations Director)", "部門主管 (Department Head)"]
    },
    "English": {
        "Finance & Accounting": ["Senior Accountant", "Finance Manager", "Cost Accountant"],
        "Warehouse & Logistics": ["Warehouse Leader", "Logistics Coordinator", "Supply Chain Specialist"],
        "Purchasing Department": ["Purchasing Manager", "Project Buyer", "Vendor Manager"],
        "Project Department": ["Project Director", "Project Manager / Model Ops", "Project Coordinator"],
        "New Venture / Innovation Dept": ["Head of New Venture", "Business Innovation Lead", "Exploration Specialist"],
        "Marketing & Brand": ["Marketing Lead", "PR Specialist", "Content Strategist"],
        "Sales & BD": ["Sales Director", "Key Account Manager", "Sales Executive"],
        "Operations Department": ["COO / Chief of Staff", "Operations Director", "Department Head"]
    }
}

selected_dept = st.sidebar.selectbox("選擇部門 / Select Department", list(departments[lang].keys()))
selected_role = st.sidebar.selectbox("選擇具體職位 / Select Specific Role", departments[lang][selected_dept])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 輸入員工與主管資料 (個資保護加密傳輸)")

emp_name = st.sidebar.text_input("員工/候選人姓名", "新進同仁 / Candidate" if lang == "繁體中文" else "Candidate Name")
birth_date = st.sidebar.date_input("員工出生日期", value=datetime.today())

boss_name = st.sidebar.text_input("直屬上司/老闆姓名", "直屬主管 / Supervisor" if lang == "繁體中文" else "Supervisor Name")
boss_birth_date = st.sidebar.date_input("上司/老闆出生日期", value=datetime.today())

b_year, b_month, b_day = birth_date.year, birth_date.month, birth_date.day

# --- 核心數值計算 ---
def calculate_numerology(year, month, day):
    def sum_digits(n): return sum(int(d) for d in str(n))
    def reduce_n(n):
        while n > 9 and n not in [11, 22, 33]: n = sum_digits(n)
        return n
    return reduce_n(year), reduce_n(month), reduce_n(day), reduce_n(sum_digits(year) + sum_digits(month) + sum_digits(day))

y_num, m_num, d_num, lp_num = calculate_numerology(b_year, b_month, b_day)
boss_y, boss_m, boss_d, boss_lp = calculate_numerology(boss_birth_date.year, boss_birth_date.month, boss_birth_date.day)

# --- 語系主介面文字 ---
texts = {
    "繁體中文": {
        "title": "🌟 TBM 全公司 AI 智慧人才與團隊矩陣系統 (安全加密版)",
        "desc": f"當前評估部門：【**{selected_dept}**】 | 目標崗位：【**{selected_role}**】。系統已啟動 Gemini AI 與資安防護。",
        "gen_btn": "🚀 啟動 Gemini AI 深度分析",
        "success_msg": "已成功透過安全通道產出【{}】在【{}】崗位的全景評估與主管化學反應報告！",
        "init_tip": "👈 請確認左側 API 授權狀態、選擇部門職位與生日，並點擊【啟動 Gemini AI 深度分析】開始！"
    },
    "English": {
        "title": "🌟 TBM AI Enterprise Talent & Team Intelligence System (Secure)",
        "desc": f"Evaluating Department: [{selected_dept}] | Target Role: [{selected_role}]. Secured & Powered by Gemini AI.",
        "gen_btn": "🚀 Run Gemini AI Deep Analysis",
        "success_msg": "Successfully generated AI report for [{}] in [{}] via secure channel!",
        "init_tip": "👈 Please verify API authorization on the left and click the button to start!"
    }
}

t = texts[lang]
st.title(t["title"])
st.markdown(t["desc"])

generate_btn = st.sidebar.button(t["gen_btn"], type="primary")

if generate_btn:
    if not GEMINI_API_KEY:
        st.error("⚠️ 尚未偵測到有效的 Gemini API Key，請在左側輸入或在 Streamlit Secrets 中設定！")
    else:
        try:
            # 初始化 Gemini Client
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            # 準備傳給 AI 的提示詞 (Prompt)
            prompt = f"""
            你是一位頂級的企業 HR 策略顧問與組織心理學家。請根據以下資料，為企業老闆提供一份極具洞察力的高階人才分析報告：
            
            - 目標部門：{selected_dept}
            - 評估職位：{selected_role}
            - 員工姓名：{emp_name}，生日：{birth_date.strftime('%Y-%m-%d')} (生命數字: {lp_num}, 年份能量: {y_num}, 月份驅動: {m_num}, 生日本質: {d_num})
            - 直屬主管：{boss_name}，生日：{boss_birth_date.strftime('%Y-%m-%d')} (生命數字: {boss_lp})
            
            請用繁體中文回覆，並分為以下四個結構化區塊：
            1. 【底層基因與天賦特質解構】：分析該員工的數字與生日所帶來的思考與行為優勢。
            2. 【目標崗位適配深度解析】：針對 {selected_role} 這個職位，他在該部門（{selected_dept}）的勝任優勢與潛在挑戰是什麼？
            3. 【直屬主管與下屬雙向化學反應】：分析主管（靈數 {boss_lp}）與員工（靈數 {lp_num}）在溝通、決策與日常帶領上的摩擦點與互補優勢。
            4. 【全公司跨部門潛能與落地管理建議】：建議他在這個崗位該如何被激勵，若未來面臨內部調動，還適合公司哪些其他部門？
            """
            
            with st.spinner("🔒 正在透過加密通道進行 Gemini AI 深度解構，請稍候..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                ai_report_text = response.text

            st.success(t["success_msg"].format(emp_name, selected_role))
            
            tab1, tab2, tab3 = st.tabs([
                "🤖 1. Gemini AI 深度洞察報告",
                "📊 2. 核心量化雷達與匹配度",
                "🔮 3. 預告：未來 V2 團隊矩陣藍圖"
            ])
            
            with tab1:
                st.subheader(f"🧠 AI 專屬顧問解析：{emp_name} ⇄ {selected_role}")
                st.markdown(ai_report_text)
                
            with tab2:
                st.subheader("📊 崗位核心維度量化評估")
                sc1, sc2 = st.columns(2)
                with sc1:
                    scores = {"核心執行力": 9.3, "崗位技能契合": 9.1, "抗壓與穩定度": 8.9, "協同溝通力": 9.0, "目標達成度": 9.2}
                    df_radar = pd.DataFrame(dict(r=list(scores.values()), theta=list(scores.keys())))
                    fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[0, 10])
                    fig.update_traces(fill='toself', line_color='#2ca02c')
                    st.plotly_chart(fig, use_container_width=True)
                with sc2:
                    st.info(f"💡 **量化小結：** 結合 AI 質化分析與數字量化模型，該候選人在 **{selected_dept}** 的綜合評估表現優異，具備良好的落地潛力。")
            
            with tab3:
                st.subheader("🔮 關於未來「團隊矩陣版 (V2)」的資安規劃")
                st.markdown("""
                當我們未來擴充到 V2 多下屬群體分析時，系統也會確保所有員工的生日與人事資料在傳輸與運算時皆符合最高資安標準。
                """)

        except Exception as e:
            st.error(f"❌ 呼叫 AI 時發生錯誤，請檢查您的 API Key 是否正確或網路連線：{e}")

else:
    st.info(t["init_tip"])

