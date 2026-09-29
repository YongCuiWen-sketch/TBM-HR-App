import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 設定頁面標題與配置
st.set_page_config(
    page_title="HR 命理與生命數字職場適性分析系統",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 頁面主標題
st.title("🌟 企業人才適性評估、面試攻略與日常輔導系統")
st.markdown("這是一套專為 HR 與企業主管設計的智慧分析工具。透過輸入員工或候選人的**年、月、日**生日數據，系統將自動解構其生命數字與五行特質，轉化為現代職場能力雷達圖、面試提問挖深攻略，以及入職後的日常輔導溝通話術。")

# --- 側邊欄：輸入介面 ---
st.sidebar.header("📝 輸入候選人/員工資料")
emp_name = st.sidebar.text_input("姓名 / 暱稱", "張小明")
emp_role = st.sidebar.text_input("目前崗位 / 應徵崗位", "行銷企劃")
birth_date = st.sidebar.date_input("出生日期", value=pd.to_datetime("1987-06-15"))

b_year = birth_date.year
b_month = birth_date.month
b_day = birth_date.day

# --- 核心邏輯：計算年、月、日的生命數字 ---
def calculate_numerology_details(year, month, day):
    def sum_digits(n):
        return sum(int(digit) for digit in str(n))
    
    def reduce_to_single(n):
        while n > 9 and n not in [11, 22, 33]:
            n = sum_digits(n)
        return n
    
    year_num = reduce_to_single(year)
    month_num = reduce_to_single(month)
    day_num = reduce_to_single(day)
    
    total_sum = sum_digits(year) + sum_digits(month) + sum_digits(day)
    life_path = reduce_to_single(total_sum)
    
    return year_num, month_num, day_num, life_path

y_num, m_num, d_num, lp_num = calculate_numerology_details(b_year, b_month, b_day)

# --- 評分演算法（基於年月日與靈數加權） ---
def generate_radar_scores(y, m, d, lp):
    creativity = min(10, max(4, (m * 1.5 + d * 0.8) % 10 + 2))
    communication = min(10, max(4, (d * 1.2 + lp * 1.0) % 10 + 2))
    resilience = min(10, max(4, (y * 0.5 + m * 1.3) % 10 + 3))
    logic = min(10, max(4, (y * 1.1 + d * 0.6) % 10 + 2))
    teamwork = min(10, max(4, (lp * 1.3 + m * 0.7) % 10 + 3))
    
    return {
        "開創與執行力": round(creativity, 1),
        "溝通與協調力": round(communication, 1),
        "抗壓與應變力": round(resilience, 1),
        "邏輯與分析力": round(logic, 1),
        "團隊協作力": round(teamwork, 1)
    }

scores = generate_radar_scores(y_num, m_num, d_num, lp_num)

# --- 面試提問攻略生成 ---
def generate_interview_questions(m, d, scores):
    questions = []
    if m % 2 == 1:
        questions.append("💡 **針對創新與變動的提問：** 「過去你在面對一個時間緊迫、且規則不明確的新專案時，你是如何跨出第一步的？能否分享一個你主動打破常規解決問題的經驗？」")
    else:
        questions.append("💡 **針對穩定與落地的提問：** 「當公司現有的制度或流程需要調整時，你通常習慣用什麼方式說服團隊？如果遇到同事抗拒配合，你會怎麼處理？」")
    
    low_skill = min(scores, key=scores.get)
    if low_skill == "邏輯與分析力":
        questions.append("🎯 **針對細節與邏輯的挖深提問：** 「在執行大型專案時，你通常用什麼工具或方法來確保數據正確、避免漏掉細節？如果最後發現數據有出入，你的檢查步驟是什麼？」")
    elif low_skill == "抗壓與應變力":
        questions.append("🎯 **針對抗壓與情緒管理的提問：** 「當多個專案同時到期，且老闆或客戶的需求臨時反覆更改時，你內心通常怎麼調適？能否舉一個你壓力最大、快撐不住時的應對例子？」")
    else:
        questions.append("🎯 **針對團隊協作的提問：** 「如果團隊成員在方向上跟你產生分歧，而主管交由你來主導，你會如何平衡大家的意見並推進進度？」")
        
    questions.append(f"🔍 **核心本質追問 (基於日數 {d} 的特質)：** 「你覺得自己在工作中最容易感到挫折的地方是什麼？主管或同事通常最常給你哪方面的反饋？」")
    return questions

# --- 內部日常輔導與溝通話術生成 ---
def generate_coaching_advice(m, d, scores):
    advice = []
    top_skill = max(scores, key=scores.get)
    low_skill = min(scores, key=scores.get)
    
    advice.append(f"💬 **日常激勵與稱讚切入點 (發揮其強項 {top_skill})：** 當需要給予動力或指派重要任務時，建議這樣開場：『這項專案非常需要你的{top_skill}，這剛好是你的優勢，交給你我很放心，你覺得我們可以怎麼切入？』給予舞台能激發最大熱情。")
    
    if low_skill == "抗壓與應變力":
        advice.append(f"⚠️ **當他遇到壓力或遇到瓶頸時的溝通話術：** 此類特質在面對突發高壓時容易悶在心裡。建議主管關心時這樣說：『我注意到最近專案變動比較快、辛苦了，我們一起把大目標拆成幾個小步驟，你目前覺得哪一個部分卡住了，我們一起來克服？』")
    elif low_skill == "邏輯與分析力":
        advice.append(f"⚠️ **當他的工作需要補足細節或數據時的溝通話術：** 避免直接指責其粗心，而是提供輔助工具。建議話術：『這份企劃的創意真的很棒！不過為了讓老闆或客戶一眼看懂，我們在數據和細節上加上這張檢核表（Checklist）再確認一次會更完美。』")
    else:
        advice.append(f"⚠️ **當他與團隊產生摩擦或溝通不良時的溝通話術：** 建議私下溫和引導：『我注意到你對這個流程有自己的堅持，不過團隊目前需要同步進度，我們來聊聊看怎麼把你的想法調整成大家都能順暢配合的方式好嗎？』")
        
    return advice

# --- 主畫面按鈕與呈現 ---
generate_btn = st.sidebar.button("🚀 生成全面分析與管理指南", type="primary")

if generate_btn:
    st.success(f"已成功為【{emp_name}】完成年、月、日能量解構與分析！")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("📊 核心密碼與白話文總結")
        st.info(f"**基本資料：** {emp_name} | 應徵/現任：{emp_role} | 生日：{birth_date.strftime('%Y-%m-%d')}")
        
        st.write(f"- **出生年份 (大環境/根基數)：** `{y_num}`")
        st.write(f"- **出生月份 (內心驅動/月數)：** `{m_num}`")
        st.write(f"- **出生日期 (核心本質/日數)：** `{d_num}`")
        st.write(f"- **綜合生命靈數 (Life Path)：** `{lp_num}`")
        
        top_skill = max(scores, key=scores.get)
        low_skill = min(scores, key=scores.get)
        
        st.markdown(f"""
        * **最強優勢維度：** **{top_skill}**（能量突出）
        * **需關注盲點維度：** **{low_skill}**（相對薄弱）
        * **整體適配評語：** 綜合其年、月、日的能量流轉，該員在 **{emp_role}** 崗位上具備良好潛力。建議招募時透過面試攻略挖深，入職後透過輔導話術精準帶領。
        """)
        
    with col2:
        st.subheader("🕸️ 人才能力雷達圖")
        df_radar = pd.DataFrame(dict(
            r=list(scores.values()),
            theta=list(scores.keys())
        ))
        fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[0, 10])
        fig.update_traces(fill='toself', line_color='#4E79A7')
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])))
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown("---")
    st.subheader("🎙️ 第一階段：面試提問攻略（招募時精準挖深）")
    interview_qs = generate_interview_questions(b_month, b_day, scores)
    for q in interview_qs:
        st.info(q)
        
    st.markdown("---")
    st.subheader("🤝 第二階段：內部日常輔導與對話指南（入職後留任管理）")
    coaching_advices = generate_coaching_advice(b_month, b_day, scores)
    for c in coaching_advices:
        st.warning(c)
else:
    st.info("👈 請在左側輸入員工姓名、崗位與出生日期，並點擊【生成全面分析與管理指南】按鈕開始體驗！")
