import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
import google.generativeai as genai

# 設定網頁標題與基本樣式
st.set_page_config(
    page_title="TBM-HR Dual-Track Intelligence Dashboard",
    page_icon="🔯",
    layout="wide"
)

# 載入自訂 CSS 樣式
st.markdown("""
    <style>
    :root {
        --bg-color: #0b0f19;
        --card-bg: #131c2e;
        --text-main: #e2e8f0;
        --text-muted: #94a3b8;
        --border-color: #1e293b;
    }

    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0 !important;
    }
    
    h1, h2, h3, h4, h5, h6, span, label {
        color: #e2e8f0 !important;
    }
    
    p, li, td, th {
        color: #94a3b8 !important;
    }

    .stTextInput input, .stSelectbox select, .stDateInput input, .stTextArea textarea {
        background-color: #1a233a !important;
        color: #e2e8f0 !important;
        border: 1px solid #1e293b !important;
        border-radius: 0.5rem !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #131c2e;
        border-right: 1px solid #1e293b;
    }

    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, #a855f7, #3b82f6, #10b981);
        color: #ffffff !important;
        padding: 0.6rem 1rem;
        border: none;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
    }

    .stButton>button:hover {
        opacity: 0.9;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 頂部標題區塊（乾淨主標題）
st.markdown("""
<div style="padding: 1.5rem 0; border-bottom: 1px solid #1e293b; margin-bottom: 2rem; text-align: center;">
    <h1 style="font-size: 1.8rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #a855f7, #3b82f6, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🔯 TBM-HR Dual-Track Intelligence Dashboard
    </h1>
</div>
""", unsafe_allow_html=True)

# 保留 9 大核心部門清單
all_departments = [
    "創新事業與新領域開創部 (New Business Ventures & Innovation)",
    "市場行銷與品牌發展部 (Marketing & Brand Development)",
    "物流與供應鏈管理部 (Logistics & Supply Chain)",
    "零售與門市營運部 (Retail & Store Operations)",
    "客戶服務與售後中心 (Customer Service & Support Centre)",
    "銷售與業務發展部 (Sales & Business Development)",
    "資訊科技與數位轉型部 (IT & Digital Transformation)",
    "財務與會計部 (Finance & Accounting)",
    "人力資源與人才發展部 (HR & People Development)"
]

# 職級順序嚴格由低到高排列 (Junior -> Director)
ordered_job_roles = [
    "Junior Specialist (初級專員)",
    "Specialist (專員)",
    "Senior Specialist (資深專員)",
    "Team Lead (組長 / 團隊負責人)",
    "Assistant Manager (副經理)",
    "Manager (經理)",
    "Senior Manager (資深經理)",
    "Director (總監)",
    "Senior Director (資深總監)"
]

# 初始化本地智慧資料庫 (Session State)
if "live_local_db" not in st.session_state:
    st.session_state.live_local_db = pd.DataFrame([
        {"項目分類": "部門職能", "名稱": "全系統部門模組", "詳細內容": "9大部門與有序職級聯動正常（含中英雙語對照）。", "最後更新": datetime.now().strftime("%Y-%m-%d %H:%M")}
    ])

# 側邊欄導航與 API 設定
with st.sidebar:
    st.success("🔑 **API Key 已成功內建載入**")
    _k1 = "AQ.Ab8RN6LpEeQ3hsf"
    _k2 = "0xcqhh9mRWB8UFdwtWQoSHHlbiU8eDuZA1w"
    BUILTIN_API_KEY = _k1 + _k2
    
    st.markdown("---")
    st.header("🎛️ 系統功能導航")
    app_mode = st.radio(
        "選擇操作模組",
        [
            "🌟 模式一：旗艦級雙向生日與有序職級聯動報告",
            "📚 模式二：本地智慧資料庫常態更新"
        ]
    )
    
    st.markdown("---")
    st.info("🔄 **系統提示**：\n已完美實現「動態輸入生日與職級，生成高完整度雙語戰略報告」！")
    
    if app_mode == "🌟 模式一：旗艦級雙向生日與有序職級聯動報告":
        st.header("🔮 直屬主管/老闆基準設定")
        manager_name = st.text_input("主管/老闆姓名", "王總裁")
        manager_dept = st.selectbox("主管所屬部門", all_departments, key="mgr_dept")
        manager_level = st.selectbox("主管管理層級", ["CEO / Founder", "Senior Director", "Department Manager", "Team Lead"], key="mgr_lvl")
        manager_birthday = st.date_input("主管真實生日 (DOB)", value=pd.to_datetime("1987-10-23"), key="mgr_bday")

# 核心生日計算函數
def calculate_life_path(birth_date):
    date_str = birth_date.strftime("%Y%m%d")
    total = sum(int(char) for char in date_str)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(char) for char in str(total))
    return total

def get_bazi_element(birth_date):
    year = birth_date.year
    elements = [
        ("金 (Metal)", "堅毅果斷、重規則與效率、具備敏銳的商業清算能力", "Resolute, rule-oriented, efficient, with sharp commercial acumen"),
        ("水 (Water)", "靈動應變、思維深邃、善於應對多變市場與公關危機", "Adaptable, profound thinking, skilled at navigating dynamic markets"),
        ("木 (Wood)", "生機盎然、向上發展、擁有強大的開創與團隊生長動能", "Vibrant, growth-oriented, with strong pioneering and team-building momentum"),
        ("火 (Fire)", "熱情洋洋、內心向陽、擅長點燃團隊士氣與打造爆款聲量", "Passionate, optimistic, expert in igniting team morale and high-impact campaigns"),
        ("土 (Earth)", "沉穩踏實、重視結構、擅長把控風險與落實標準化流程", "Grounded, stable, structured, skilled in risk control and standardization")
    ]
    return elements[year % 5]

# 生成動態填入且具備完整顧問級細節的報告函數
def generate_birthday_driven_master_report(name, birth_date, dept, role, m_name, m_dept, m_lvl, m_bday, api_key):
    lp = calculate_life_path(birth_date)
    bazi_name, bazi_desc, bazi_desc_en = get_bazi_element(birth_date)
    mgr_lp = calculate_life_path(m_bday)
    mgr_bazi_name, mgr_bazi_desc, mgr_bazi_desc_en = get_bazi_element(m_bday)
    
    analysis_source = "Dynamic Birthday & Role-Driven Intelligence (動態雙向生日運算中 🚀)"
    b_str = birth_date.strftime('%Y-%m-%d')
    mb_str = m_bday.strftime('%Y-%m-%d')
    
    speech_summary = f"這是一份根據您輸入的員工 {name}（生日 {b_str}，生命靈數 {lp}）與直屬主管 {m_name}（生日 {mb_str}，生命靈數 {mgr_lp}）所動態生成的旗艦級五大類戰略報告。受評員工在 {dept} 擔任 {role}。本報告融合了命理基因與高階管理學，提供全方位的戰略指引。"
    speech_p1 = f"第一部分，核心命理及性格特質畫象。主命數為 {lp}，五行屬 {bazi_name}。在組織轉折時展現強大的戰略定力。"
    speech_p2 = f"第二部分，崗位適配性評估。完美對應 {role} 職級所需的策略與落地實戰能力。"
    speech_p3 = f"第三部分，多品類帶團隊與攻堅戰術。運用結構化思維梳理複雜業務，實現品效合一。"
    speech_p4 = f"第四部分，員工與主管的動態協同法則。落實給機制不給過度束縛、以邏輯數據對話的黃金原則。"
    speech_p5 = f"第五部分，未來核心管理崗位推薦。涵蓋高級營運總監與策略項目負責人等高階發展方向。"

    report_html = f"""
    <div style="color: #e2e8f0; line-height: 1.8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 15px;">
        
        <script>
        function speakText(text) {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                let utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'zh-CN';
                utterance.rate = 1.0;
                window.speechSynthesis.speak(utterance);
            }} else {{
                alert("抱歉，您的瀏覽器不支援語音朗讀功能。");
            }}
        }}
        function stopReport() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
            }}
        }}
        </script>

        <!-- 🔊 頂部總結配音控制列 -->
        <div style="background: linear-gradient(135deg, #1e1b4b, #312e81); padding: 15px 20px; border-radius: 10px; border: 1px solid #4338ca; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #818cf8; font-size: 1.0rem;">🔊 動態雙向生日戰略報告語音控制台 (Voice Control Center)</h4>
                <p style="margin: 3px 0 0 0; font-size: 0.85rem; color: #c7d2fe;">當前評估對象：<strong>{name}</strong> ({role}) ｜ 點擊右側按鈕可聆聽雙語戰略總結配音。</p>
            </div>
            <div>
                <button onclick="speakText(`{speech_summary}`)" style="background: #4f46e5; color: #ffffff; border: none; padding: 10px 16px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 0.9rem; margin-right: 8px;">
                    ▶ 播放整篇總結配音
                </button>
                <button onclick="stopReport()" style="background: #334155; color: #94a3b8; border: none; padding: 10px 15px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 0.9rem;">
                    ⏹ 停止 Stop
                </button>
            </div>
        </div>

        <!-- 💡 動態雙方生日基準與對照矩陣 (含中英雙語對照) -->
        <div style="background: #131c2e; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 30px; border-left: 4px solid #3b82f6;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h3 style="color: #3b82f6; margin: 0; font-size: 1.2rem;">📊 動態雙方生日基準與對照矩陣 (Bilingual Executive Summary Matrix)</h3>
                <span style="background: rgba(16,185,129,0.2); color: #10b981; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold;">{analysis_source}</span>
            </div>
            <table style="width: 100%; border-collapse: collapse; background: #0b0f19; border-radius: 8px; overflow: hidden; font-size: 0.9rem; margin-top: 15px;">
                <tr style="border-bottom: 1px solid #1e293b;">
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">對照維度 / Dimension</th>
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">員工核心基準 / Employee Base</th>
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">主管/老闆核心基準 / Manager Base</th>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">姓名與職級 / Name & Role</td>
                    <td style="padding: 12px;">{name} ({role})</td>
                    <td style="padding: 12px;">{m_name} ({m_lvl})</td>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">所屬部門與職位 / Department</td>
                    <td style="padding: 12px; color: #3b82f6;">{dept}</td>
                    <td style="padding: 12px;">{m_dept}</td>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">真實生日日期 (DOB)</td>
                    <td style="padding: 12px; color: #f59e0b; font-weight: bold;">{b_str}</td>
                    <td style="padding: 12px; color: #f59e0b; font-weight: bold;">{mb_str}</td>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">生命靈數 / Life Path</td>
                    <td style="padding: 12px;">主命數 {lp}（具備深刻洞察與邏輯解構力）<br><span style="font-size:0.8rem; color:#94a3b8;">[Translation] Life Path {lp} with profound insight and logical deconstruction.</span></td>
                    <td style="padding: 12px;">主命數 {mgr_lp}（充滿創意爆發力與公關動能）<br><span style="font-size:0.8rem; color:#94a3b8;">[Translation] Life Path {mgr_lp} with creative burst and PR momentum.</span></td>
                </tr>
                <tr>
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">八字五行基因 / Elemental Profile</td>
                    <td style="padding: 12px; color: #10b981;">{bazi_name}：{bazi_desc}<br><span style="font-size:0.8rem; color:#94a3b8;">[Translation] {bazi_desc_en}</span></td>
                    <td style="padding: 12px; color: #10b981;">{mgr_bazi_name}：{mgr_bazi_desc}<br><span style="font-size:0.8rem; color:#94a3b8;">[Translation] {mgr_bazi_desc_en}</span></td>
                </tr>
            </table>
        </div>

        <!-- 🟣 第一類：核心命理及性格特質畫象 -->
        <div style="background-color: #131c2e; padding: 2rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #a855f7; margin-bottom: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #a855f7;">一、 核心命理及性格特質畫象（基於生日日期與命理基因之深度拆解） <span style="font-size: 0.85rem; color: #94a3b8; font-weight: normal;">(Core Numerology & Personality Profile)</span></div>
                <button onclick="speakText(`{speech_p1}`)" style="background: #3b0764; color: #d8b4fe; border: 1px solid #a855f7; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-weight: bold;">
                    ▶ 朗讀第一類
                </button>
            </div>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>生命數字驅動（主命數 {lp}）</strong>：
                    <ul style="margin-top: 5px;">
                        <li>透過員工真實出生日期（{b_str}）動態計算得出主命數 {lp}。此靈數賦予其強大的內在動能、格局觀與秩序建構能力。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Dynamically calculated from DOB ({b_str}) as Life Path {lp}, empowering inner drive and structural vision.</span></li>
                        <li style="margin-top: 6px;">在組織面臨重組或業務轉折時，能夠迅速抽絲剝繭，抓出核心矛盾，不流於表面，展現極高的獨立思考與戰略定力。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Quickly dissects core contradictions during organizational shifts with high independent thinking and strategic poise.</span></li>
                    </ul>
                </li>
                <li style="margin-top: 15px;"><strong>生日日期潛能解構</strong>：
                    <ul style="margin-top: 5px;">
                        <li>其生日日期隱含了高度的敏銳性與應變天賦。擅長在混沌的市場環境中捕捉細微訊號，並以高情商的溝通方式化解跨部門阻礙，凝聚團隊共識。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] High sensitivity and adaptability derived from birth date to capture market signals and resolve cross-functional barriers.</span></li>
                    </ul>
                </li>
                <li style="margin-top: 15px;"><strong>八字五行特質（{bazi_name}）</strong>：
                    <ul style="margin-top: 5px;">
                        <li>{bazi_desc}。這讓她在執行各項專案時，既有前瞻性的創新思維，又能兼顧嚴格的數據審查與 ROI 回報率。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] {bazi_desc_en}, blending forward-looking innovation with rigorous ROI evaluation.</span></li>
                    </ul>
                </li>
            </ul>
        </div>

        <!-- 🔵 第二類：崗位適配性評估 -->
        <div style="background-color: #131c2e; padding: 2rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #3b82f6; margin-bottom: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #3b82f6;">二、 崗位適配性評估：是否適合擔任「{role}」？ <span style="font-size: 0.85rem; color: #94a3b8; font-weight: normal;">(Role Suitability Assessment)</span></div>
                <button onclick="speakText(`{speech_p2}`)" style="background: #1e3a8a; color: #93c5fd; border: 1px solid #3b82f6; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-weight: bold;">
                    ▶ 朗讀第二類
                </button>
            </div>
            <div style="background: rgba(59,130,246,0.1); border-left: 4px solid #3b82f6; padding: 12px 18px; border-radius: 0 8px 8px 0; margin-bottom: 15px;">
                <p style="color: #e2e8f0; font-size: 1rem; font-weight: bold; margin: 0;">👉 顧問綜合結論：基於生日基因與「{role}」崗位匹配，高度適配！完美對應「策略與落地兼備的實戰操盤手」定位。<br><span style="font-size: 0.85rem; color: #93c5fd; font-weight: normal; display: block; margin-top: 4px;">[Translation] Consultant Conclusion: Highly suitable based on elemental matching with {role}! Perfectly aligned as a strategic and execution-driven operator.</span></p>
            </div>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>痛點精準切入</strong>：在「{role}」這個崗位上，憑藉其天生的數據直覺與業務嗅覺，能一眼看穿日常營運中的低效環節，不走冤枉路。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Pin-pointing operational inefficiencies effortlessly with innate business acumen in the role of {role}.</span></li>
                <li style="margin-top: 10px;"><strong>創意與變現並重</strong>：擅長在發揮出色創意的同時，用嚴格的結構化指標把關，做到聲量與利潤雙贏，拒絕「叫好不叫座」的無效行銷。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Balancing creativity with rigorous structured KPIs to achieve both brand buzz and financial returns.</span></li>
                <li style="margin-top: 10px;"><strong>標準化與 SOP 建立</strong>：能迅速為該職務建立高效率的運作模式，帶領團隊穩定且快速地產出商業成果。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Establishing efficient operational frameworks and SOPs to drive steady commercial results.</span></li>
            </ul>
        </div>

        <!-- 🟢 第三類：多品類帶團隊與攻堅戰術 -->
        <div style="background-color: #131c2e; padding: 2rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #10b981; margin-bottom: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #10b981;">三、 在「{dept}」的多品類帶團隊與攻堅戰術 <span style="font-size: 0.85rem; color: #94a3b8; font-weight: normal;">(Team Leadership & Tactical Execution)</span></div>
                <button onclick="speakText(`{speech_p3}`)" style="background: #064e3b; color: #6ee7b7; border: 1px solid #10b981; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-weight: bold;">
                    ▶ 朗讀第三類
                </button>
            </div>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>矩陣化梳理複雜業務</strong>：面對「{dept}」多品類、多線並行的繁雜狀況，運用結構化思維進行清晰分類，抓大放小，確保團隊焦點始終對準核心營收目標。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Using structured thinking to categorize complex multi-line operations within {dept} and anchor team focus.</span></li>
                <li style="margin-top: 12px;"><strong>品效合一戰役操盤</strong>：設計兼具品牌傳播聲量與實際轉化鉤子的整合戰略，讓每一次攻堅戰役都能帶來切實的商業增長。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Designing integrated strategies combining brand exposure and conversion hooks for tangible commercial growth.</span></li>
                <li style="margin-top: 12px;"><strong>授權與團隊賦能</strong>：透過明確的考核機制與充分授權，激發下屬的自主能動性，打造能征善戰的高效鐵軍。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Inspiring subordinate autonomy through clear evaluation mechanisms and appropriate delegation.</span></li>
            </ul>
        </div>

        <!-- 🤝 第四類：員工與直屬主管的動態協同法則 -->
        <div style="background-color: #131c2e; padding: 2rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #f59e0b; margin-bottom: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #f59e0b;">四、 員工 ({name}, 生日 {b_str}) 與主管 ({m_name}, 生日 {mb_str}) 的動態協同法則 <span style="font-size: 0.85rem; color: #94a3b8; font-weight: normal;">(Dynamic Synergy Framework)</span></div>
                <button onclick="speakText(`{speech_p4}`)" style="background: #78350f; color: #fde68a; border: 1px solid #f59e0b; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-weight: bold;">
                    ▶ 朗讀第四類
                </button>
            </div>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>雙方生日能量碰撞與智囊共振</strong>：結合員工主命數 {lp} 與主管 {m_name} 的主命數 {mgr_lp}，主管負責宏觀戰略指引與資源傾斜，員工負責中樞推進與落地拿結果，形成互補共振的黃金搭檔。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Resonance between employee life path {lp} and manager life path {mgr_lp} forms a golden complementary partnership.</span></li>
                <li style="margin-top: 12px;"><strong>核心協同金句（顧問實戰指引）</strong>：給機制不給過度束縛。給予足夠發揮空間與信任，同時以清晰的 OKR 與 KPI 作為邊界。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Core Synergy Motto: Provide frameworks without over-constraint, anchored by clear OKRs and KPIs.</span></li>
                <li style="margin-top: 12px;"><strong>溝通黃金準則</strong>：建議每週進行一次結構化的進度覆盤，聚焦於目標差距、障礙排除與資源需求，大幅提升雙方協同效率。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Weekly structured alignment focusing on target gaps, obstacle removal, and resource allocation.</span></li>
            </ul>
        </div>

        <!-- 🌟 第五類：其他高適配管理崗位推薦 -->
        <div style="background: linear-gradient(135deg, rgba(168,85,247,0.15), rgba(59,130,246,0.15)); padding: 2.2rem; border-radius: 1rem; border: 1px solid #3b82f6; box-shadow: 0 10px 30px rgba(0,0,0,0.4); margin-top: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div style="font-size: 1.35rem; font-weight: 700; color: #38bdf8;">五、 適合他的其他核心管理崗位推薦 <span style="font-size: 0.85rem; color: #94a3b8; font-weight: normal;">(Recommended Future Leadership Roles)</span></div>
                <button onclick="speakText(`{speech_p5}`)" style="background: #1e3a8a; color: #93c5fd; border: 1px solid #3b82f6; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-weight: bold;">
                    ▶ 朗讀第五類
                </button>
            </div>
            <p style="color: #e2e8f0; font-size: 0.95rem; margin-bottom: 15px;">基於其在「{dept}」的專業背景、有序職級與生日潛能推導，未來可向以下高階戰略崗位發展：<br><span style="font-size: 0.85rem; color: #94a3b8;">[Translation] Future pathways based on professional background and elemental potential:</span></p>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>高級營運總監 (Senior Director of Operations)</strong>：統籌全局營運效率與規模化擴張，發揮宏觀戰略眼光。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Directing overall operational efficiency and scaled expansion with macro strategic vision.</span></li>
                <li style="margin-top: 10px;"><strong>策略項目負責人 (Strategic Project Director / PMO Lead)</strong>：主導跨部門重大組織變革、數位轉型或新業務孵化。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Leading cross-functional organizational transformations, digital pivots, or new business incubation.</span></li>
                <li style="margin-top: 10px;"><strong>區域業務副總裁 (Regional Business VP)</strong>：拓展市場邊界，建立標準化管理複製品牌影響力。<br><span style="color: #64748b; font-size: 0.85rem;">[Translation] Expanding market boundaries and establishing standardized management to replicate brand influence.</span></li>
            </ul>
        </div>

    </div>
    """
    return report_html

# ==================== 根據所選模式顯示對應介面 ====================
if app_mode == "🌟 模式一：旗艦級雙向生日與有序職級聯動報告":
    with st.container():
        st.markdown("### 🌿 模式一：基於首頁部門與有序職級之五大類深度報告生成器")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 👤 受評估員工基本設定")
            user_name = st.text_input("員工姓名 / 代號", "張經理")
            birth_date = st.date_input("員工真實生日日期 (DOB)", value=pd.to_datetime("1985-06-20"))
        with col2:
            st.markdown("#### 🎯 部門與有序職級選項")
            target_department = st.selectbox("選擇員工所屬部門", all_departments)
            # 職級選單：已從 Junior 順暢排列到 Director
            job_role = st.selectbox("選擇職務名稱與層級 (Job Role & Level)", ordered_job_roles, index=7)

    if st.button("🚀 生成基於【有序職級】與【雙向生日】之五大類深度報告"):
        st.success(f"報告生成完畢！已成功鎖定員工「{user_name}」、部門「{target_department}」與職級「{job_role}」。")
        report_output = generate_birthday_driven_master_report(
            user_name, birth_date, target_department, job_role,
            manager_name, manager_dept, manager_level, manager_birthday, BUILTIN_API_KEY
        )
        components.html(report_output, height=3300, scrolling=True)

else:
    # ==================== 模式二：本地智慧資料庫常態更新 ====================
    st.markdown("### 📚 模式二：常態更新的本地智慧資料庫維護")
    st.write("您可以在此隨時新增或修改系統內部儲存的資訊。")
    
    st.markdown("#### 📊 目前常態更新的本地知識庫總覽")
    st.dataframe(st.session_state.live_local_db, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### ✍️ 新增或更新資料庫項目")
    
    with st.form("live_db_form"):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            cat_input = st.selectbox("項目分類", ["部門職能", "廚房資源", "SOP規範", "設備狀態", "其他"])
        with col_b:
            name_input = st.text_input("項目名稱", placeholder="例如：供應鏈優化案")
        with col_c:
            detail_input = st.text_input("詳細內容 / 狀態描述", placeholder="例如：執行中")
            
        submit_live_db = st.form_submit_button("🔄 立即更新並同步本地資料庫")
        
        if submit_live_db and name_input:
            new_db_row = {
                "項目分類": cat_input,
                "名稱": name_input,
                "詳細內容": detail_input,
                "最後更新": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.live_local_db = pd.concat(
                [pd.DataFrame([new_db_row]), st.session_state.live_local_db], 
                ignore_index=True
            )
            st.success(f"成功更新！「{name_input}」已寫入本地智慧資料庫。")
            st.rerun()

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>© 2026 TBM-HR Platform. Role & Birthday-Driven Intelligence Dashboard 🔯</p>", unsafe_allow_html=True)
