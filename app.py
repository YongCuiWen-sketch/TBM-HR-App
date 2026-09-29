import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 設定頁面標題與配置
st.set_page_config(
    page_title="TBM Team Synergy & Leadership Intelligence System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 側邊欄：雙語設定與分析模組 ---
st.sidebar.markdown("### 🌐 語言與介面設定 / Language & Settings")
lang = st.sidebar.selectbox("選擇語言 / Select Language", ["繁體中文", "English"])

analysis_mode = st.sidebar.selectbox(
    "選擇分析與管理模組 / Select Analysis Module", 
    [
        "1. 核心密碼與 Marketing 崗位適配", 
        "2. 高階領導者風格與帶兵策略", 
        "3. 上司與新員工個性配對與化學反應 (Boss-Employee Match)", 
        "4. 面試實戰情景題庫與考核指標",
        "5. 其他高價值管理崗位評估 (COO/產品總監)"
    ] if lang == "繁體中文" else [
        "1. Core Code & Marketing Fit", 
        "2. Leadership & Management Strategy", 
        "3. Boss & Employee Synergy Match", 
        "4. Interview Scenario & Evaluation",
        "5. Alternative Management Roles (COO/Product)"
    ]
)

# --- 語系文字字典 (全雙語對應) ---
texts = {
    "繁體中文": {
        "title": "🌟 TBM 團隊動態與高階領導力智慧系統",
        "desc": "本系統支援繁體中文與英文雙語切換。專為企業主與 HR 設計，完美結合個人命理能量、Marketing 實戰適配，以及最核心的「上司-員工雙向性格配對」，助您在團隊中精準定位、發揮最大戰力。",
        "sidebar_header": "📝 輸入團隊成員與主管資料",
        "name_input": "員工/候選人姓名",
        "role_input": "目標評估崗位",
        "birth_date": "員工出生日期",
        "boss_name": "直屬上司/老闆姓名",
        "boss_birth": "上司/老闆出生日期",
        "gen_btn": "🚀 生成雙語戰略配對報告",
        "success_msg": "已成功為【{}】與主管【{}】完成雙語化學反應解構！",
        "core_code": "📊 核心密碼與雙向配對總結",
        "basic_info": "**基本資料：** 員工: {} | 主管: {} | 崗位: {}",
        "radar_title": "🕸️ 團隊協同與能力綜合雷達圖",
        "content_title": "💡 專屬深度解構、配對法則與實戰策略",
        "init_tip": "👈 請在左側輸入資料，選擇對應的分析模組，並點擊【生成雙語戰略配對報告】開始體驗！"
    },
    "English": {
        "title": "🌟 TBM Team Synergy & Leadership Intelligence System",
        "desc": "Fully bilingual (Traditional Chinese / English). Designed for executives and HR to analyze individual potential, marketing fit, and crucial Boss-Employee synergy for optimal team placement.",
        "sidebar_header": "📝 Member & Leader Profile Info",
        "name_input": "Candidate / Employee Name",
        "role_input": "Target Role",
        "birth_date": "Employee Date of Birth",
        "boss_name": "Direct Supervisor / Boss Name",
        "boss_birth": "Boss Date of Birth",
        "gen_btn": "🚀 Generate Bilingual Synergy Report",
        "success_msg": "Successfully generated bilingual synergy report for [{}] & Boss [{}]!",
        "core_code": "📊 Core Codes & Synergy Summary",
        "basic_info": "**Profile:** Employee: {} | Boss: {} | Role: {}",
        "radar_title": "🕸️ Team Synergy & Competency Radar Chart",
        "content_title": "💡 Strategic Deep-Dive & Boss-Employee Synergy Guide",
        "init_tip": "👈 Please enter details on the left and click the button to start!"
    }
}

t = texts[lang]

st.title(t["title"])
st.markdown(t["desc"])

# --- 側邊欄輸入介面 ---
st.sidebar.header(t["sidebar_header"])
emp_name = st.sidebar.text_input(t["name_input"], "張小明 (Marketing Lead)" if lang == "繁體中文" else "Alex (Marketing Lead)")
emp_role = st.sidebar.text_input(t["role_input"], "行銷負責人 / Marketing Leader")
birth_date = st.sidebar.date_input(t["birth_date"], value=pd.to_datetime("1985-06-20"))

boss_name = st.sidebar.text_input(t["boss_name"], "老闆 / Founder" if lang == "繁體中文" else "Founder / Boss")
boss_birth_date = st.sidebar.date_input(t["boss_birth"], value=pd.to_datetime("1987-10-23"))

b_year, b_month, b_day = birth_date.year, birth_date.month, birth_date.day

# --- 核心數值計算 ---
def calculate_numerology(year, month, day):
    def sum_digits(n): return sum(int(d) for d in str(n))
    def reduce_n(n):
        while n > 9 and n not in [11, 22, 33]: n = sum_digits(n)
        return n
    y_num = reduce_n(year)
    m_num = reduce_n(month)
    d_num = reduce_n(day)
    lp_num = reduce_n(sum_digits(year) + sum_digits(month) + sum_digits(day))
    return y_num, m_num, d_num, lp_num

y_num, m_num, d_num, lp_num = calculate_numerology(b_year, b_month, b_day)
boss_y, boss_m, boss_d, boss_lp = calculate_numerology(boss_birth_date.year, boss_birth_date.month, boss_birth_date.day)

# --- 依據不同模組與雙語動態生成內容 ---
def get_system_content(mode, y, m, d, lp):
    if lang == "繁體中文":
        if "1." in mode: # Marketing 適配
            scores = {"策略規劃與落地": 9.0, "創意發想與傳播": 8.5, "抗壓穩健與執行": 8.8, "市場數據洞察": 9.2, "跨部門協作": 8.6}
            details = f"""
            ### 🎯 核心密碼與 Marketing 崗位適配分析
            * **員工生日：** `{birth_date.strftime('%Y-%m-%d')}` (主命數 `{lp}`，雙子巨蟹交界，食傷生財)
            * **生命數字 {lp} (實幹家與秩序維護者)：** 擁有極強的結構化思維與 SOP 建立能力，擅長把點子落實為商業結果。
            * **雙子巨蟹交界：** 兼具雙子靈動與巨蟹細膩，能精準洞察消費者痛點。
            * **總結評語：** 屬於「策略與落地兼備的實戰型 Marketing 操盤手」，能同時駕馭多品類產品與聲量銷售雙軌目標。
            """
        elif "2." in mode: # 領導與帶兵
            scores = {"願景與大局觀": 8.7, "團隊結構化管理": 9.3, "跨部門翻譯力": 9.0, "標準化 SOP 建立": 9.5, "包容與激勵": 8.2}
            details = f"""
            ### 🦅 高階領導者風格與帶兵策略
            * **仰望星空與腳踏實地兼具：** 能夠把 Campaign 的數據、排期與 KPI 抓得死死的。
            * **強大跨部門翻譯能力：** 能聽懂老闆和銷售要的「業績結果」，也能聽懂創意團隊要的「靈感自由」。
            * **帶兵建議：** 授權其全權負責方向，幫他配一個「創意瘋子」做副手，並給予團隊適度包容。
            """
        elif "3." in mode: # 上司與新員工配對 (你的核心亮點)
            scores = {"戰略思維同頻": 9.5, "優勢互補指數": 9.2, "溝通成本省省": 9.0, "火星撞地球(防範)": 7.5, "結果交付保障": 9.4}
            details = f"""
            ### 🤝 上司 ({boss_name}: {boss_birth_date.strftime('%Y-%m-%d')}, 靈數 {boss_lp}) 與 員工 ({emp_name}: {birth_date.strftime('%Y-%m-%d')}, 靈數 {lp}) 化學反應
            * **黃金同頻 (雙 4 號共鳴)：** 兩人的生命靈數都是 **4**，對於「承諾、效率、結果與規則」有高度共識，溝通成本極低，不需要過多解釋。
            * **完美角色互補：** 
              * **老闆 (靈數 {boss_lp} 帶1與7)：** 站在最前線定戰略、看大局、找資源。
              * **高管 (靈數 {lp} 帶雙子巨蟹與食傷)：** 作為內部總操盤手，把老闆的抽象構想轉化為嚴密的 SOP 與 ROI 數據閉環。
            * **需要防範的摩擦點：** 兩人都帶有強烈「食傷/主見」，自尊心強。遇到意見不合時切忌硬碰硬，應**「用數據和邏輯對話」**。
            * **給老闆的管理金句：** 給機制不給束縛（放權戰術）、做他堅實的靠山（當他因嚴格管理與其他部門產生摩擦時在頂層護法）。
            """
        elif "4." in mode: # 面試情景題
            scores = {"實戰鑑別度": 9.5, "動態應變力": 9.0, "團隊捏合力": 9.3, "資源爭取力": 8.8, "結果導向度": 9.2}
            details = f"""
            ### 🎙️ 面試實戰情景題庫與考核指標
            * **情景題考驗：** 團隊中一人創意散漫不交方案，另一人執行規矩但無亮點，如何捏合？
            * **高分特徵：** 揚長避短（創意人抓前端爆點，執行人抓後端排期），兼具同理心與規則底線。
            """
        else: # 其他崗位
            scores = {"營運 COO 適配度": 9.0, "產品總監適配度": 8.8, "商務 BD 總監": 8.7, "組織發展/HRD": 8.5, "專案統籌 PMO": 9.2}
            details = f"""
            ### 🏢 其他高價值管理崗位適配評估
            * **營運長 / 總經理辦公室 (COO / Chief of Staff)：** 適合公司擴張期，用 4 號結構化思維把亂局變規矩。
            * **產品總監 / 業務線負責人：** 擔任老闆與研發間的最強翻譯機。
            """
    else:
        # English Version
        if "1." in mode:
            scores = {"Strategy & Execution": 9.0, "Creativity & Comm": 8.5, "Stability": 8.8, "Market Insight": 9.2, "Collaboration": 8.6}
            details = f"""
            ### 🎯 Core Code & Marketing Fit Analysis
            * **Employee DOB:** `{birth_date.strftime('%Y-%m-%d')}` (Life Path `{lp}`, Gemini-Cancer Cusp)
            * **Life Path {lp} (The Builder & Realizer):** Exceptional structure and execution capabilities. Turns ideas into concrete business results.
            * **Gemini-Cancer Cusp:** Blends quick wit with deep empathy for target audiences.
            * **Summary:** An ideal strategic & hands-on Marketing leader capable of multi-category management.
            """
        elif "2." in mode:
            scores = {"Vision & Big Picture": 8.7, "Structured Management": 9.3, "Cross-Dept Translation": 9.0, "SOP Building": 9.5, "Empathy & Motivation": 8.2}
            details = f"""
            ### 🦅 Leadership & Management Strategy
            * **Best of Both Worlds:** Combines high-level vision with meticulous attention to KPIs, schedules, and data loops.
            * **Coaching Tip:** Give clear strategic direction and autonomy in execution; pair with a creative co-pilot.
            """
        elif "3." in mode:
            scores = {"Strategic Harmony": 9.5, "Synergy & Complement": 9.2, "Low Communication Cost": 9.0, "Friction Guardrail": 7.5, "Result Delivery": 9.4}
            details = f"""
            ### 🤝 Boss ({boss_name}: {boss_birth_date.strftime('%Y-%m-%d')}, LP {boss_lp}) & Employee ({emp_name}: {birth_date.strftime('%Y-%m-%d')}, LP {lp}) Synergy Match
            * **Shared Foundation (Double Life Path 4):** Both value commitment, efficiency, results, and structure. Extremely low communication friction.
            * **Role Complementarity:** 
              * **Boss (LP {boss_lp}):** Focuses on macro strategy, vision, and external resources.
              * **Executive (LP {lp}):** Acts as the internal commander, turning vision into strict SOPs and data-driven execution.
            * **Friction Warning:** Both possess strong intellectual independence. Avoid head-on clashes; always communicate using **data and logic**.
            * **Boss Management Tip:** Provide boundaries and autonomy; act as a solid backing shield during internal alignment.
            """
        elif "4." in mode:
            scores = {"Assessment Rigor": 9.5, "Adaptability": 9.0, "Team Blending": 9.3, "Resource Grasping": 8.8, "Result Orientation": 9.2}
            details = f"""
            ### 🎙️ Interview Scenario & Evaluation
            * **Test Question:** How to blend a chaotic creative staff with a rigid, uninspired executor?
            * **Ideal Answer:** Leverage their strengths respectively while maintaining empathy and performance standards.
            """
        else:
            scores = {"COO Fit": 9.0, "Product Director Fit": 8.8, "BD Director": 8.7, "HRD Fit": 8.5, "PMO Director": 9.2}
            details = f"""
            ### 🏢 Alternative Management Roles
            * **COO / Chief of Staff:** Perfect for scaling phases, turning operational chaos into structured efficiency.
            * **Product Director:** Acts as the strongest bridge between market demand and tech execution.
            """
            
    return scores, details

scores, analysis_content = get_system_content(analysis_mode, y_num, m_num, d_num, lp_num)

# --- 主畫面按鈕與呈現 ---
generate_btn = st.sidebar.button(t["gen_btn"], type="primary")

if generate_btn:
    st.success(t["success_msg"].format(emp_name, boss_name))
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader(t["core_code"])
        st.info(t["basic_info"].format(emp_name, boss_name, emp_role))
        
        st.write(f"- **Employee DOB (Year {y_num}/Month {m_num}/Day {d_num})** | **LP {lp_num}**")
        st.write(f"- **Boss DOB (LP {boss_lp})**")
        
        top_skill = max(scores, key=scores.get)
        low_skill = min(scores, key=scores.get)
        
        st.markdown(f"""
        * **Active Module:** `{analysis_mode}`
        * **Top Strength:** **{top_skill}**
        * **Focus Area:** **{low_skill}**
        """)
        
    with col2:
        st.subheader(t["radar_title"])
        df_radar = pd.DataFrame(dict(r=list(scores.values()), theta=list(scores.keys())))
        fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[0, 10])
        fig.update_traces(fill='toself', line_color='#2ca02c')
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])))
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown("---")
    st.subheader(t["content_title"])
    st.markdown(analysis_content)
    
else:
    st.info(t["init_tip"])
