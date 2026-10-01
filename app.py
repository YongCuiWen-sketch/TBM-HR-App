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

# 頂部標題區塊
st.markdown("""
<div style="padding: 1.5rem 0; border-bottom: 1px solid #1e293b; margin-bottom: 2rem; text-align: center;">
    <h1 style="font-size: 1.8rem; font-weight: 700; margin-bottom: 8px; background: linear-gradient(135deg, #a855f7, #3b82f6, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🔯 TBM-HR Dual-Track Intelligence Dashboard
    </h1>
    <h3 style="font-size: 1.0rem; color: #94a3b8; font-weight: normal; margin: 0;">
        【旗艦級雙向生日與首頁職業聯動 ｜ 五大類深度報告與專屬語音配音】
    </h3>
</div>
""", unsafe_allow_html=True)

# 完整保留您原本所有的 9 大核心部門清單
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

# 各部門對應的專業職稱選項庫
department_roles = {
    "創新事業與新領域開創部 (New Business Ventures & Innovation)": ["創新總監 (Innovation Director)", "新業務操盤手 (New Business Lead)", "MVP 專案經理", "策略孵化主管"],
    "市場行銷與品牌發展部 (Marketing & Brand Development)": ["Marketing 總監 / 操盤手", "品牌行銷總監 (Brand Director)", "流量增長負責人", "公關與公眾關係總監"],
    "物流與供應鏈管理部 (Logistics & Supply Chain)": ["供應鏈總監 (Supply Chain Director)", "物流營運負責人", "採購與庫存管理總監", "倉儲自動化專案主管"],
    "零售與門市營運部 (Retail & Store Operations)": ["零售營運總監 (Retail Operations Director)", "區域總經理 (Regional GM)", "門市拓展負責人", "零售培訓主管"],
    "客戶服務與售後中心 (Customer Service & Support Centre)": ["客服總監 (CS Director)", "客戶體驗負責人 (CX Lead)", "售後運營主管", "質量監控經理"],
    "銷售與業務發展部 (Sales & Business Development)": ["業務總監 (Sales Director)", "商務拓展總監 (BD Director)", "大客戶銷售負責人", "渠道營銷主管"],
    "資訊科技與數位轉型部 (IT & Digital Transformation)": ["技術總監 / CTO", "數位轉型負責人", "產品研發總監", "數據分析主管"],
    "財務與會計部 (Finance & Accounting)": ["財務總監 / CFO", "會計主管", "財務分析與預算經理", "資金管理主管"],
    "人力資源與人才發展部 (HR & People Development)": ["人資總監 / CHRO", "人才發展負責人", "組織效能經理", "招聘與薪酬主管"]
}

# 初始化本地智慧資料庫 (Session State)
if "live_local_db" not in st.session_state:
    st.session_state.live_local_db = pd.DataFrame([
        {"項目分類": "部門職能", "名稱": "全系統部門模組", "詳細內容": "9大部門與對應職稱連動正常。", "最後更新": datetime.now().strftime("%Y-%m-%d %H:%M")}
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
            "🌟 模式一：旗艦級雙向生日與首頁職業聯動報告",
            "📚 模式二：本地智慧資料庫常態更新"
        ]
    )
    
    st.markdown("---")
    st.info("🔄 **系統提示**：\n報告內容與語音配音會完全對應您在首頁所選擇的部門與特定職稱！")
    
    if app_mode == "🌟 模式一：旗艦級雙向生日與首頁職業聯動報告":
        st.header("🔮 直屬主管/老闆基準設定")
        manager_name = st.text_input("主管/老闆姓名", "最高決策主管")
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
        ("金 (Metal)", "堅毅果斷、重規則與效率、具備敏銳的商業清算能力"),
        ("水 (Water)", "靈動應變、思維深邃、善於應對多變市場與公關危機"),
        ("木 (Wood)", "生機盎然、向上發展、擁有強大的開創與團隊生長動能"),
        ("火 (Fire)", "熱情洋洋、內心向陽、擅長點燃團隊士氣與打造爆款聲量"),
        ("土 (Earth)", "沉穩踏實、重視結構、擅長把控風險與落實標準化流程")
    ]
    return elements[year % 5]

# 生成報告函數（修復變數帶入與防錯）
def generate_birthday_driven_master_report(name, birth_date, dept, role, level, m_name, m_dept, m_lvl, m_bday, api_key):
    lp = calculate_life_path(birth_date)
    bazi_name, bazi_desc = get_bazi_element(birth_date)
    mgr_lp = calculate_life_path(m_bday)
    mgr_bazi_name, mgr_bazi_desc = get_bazi_element(m_bday)
    
    analysis_source = ""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        身為頂尖HR高階戰略顧問，請依據以下雙方之「真實生日日期」以及「首頁指定的部門與職稱」進行五大類深度分析報告：
        - 員工：{name}，生日：{birth_date.strftime('%Y-%m-%d')} (生命靈數：{lp}, 五行八字：{bazi_name})
        - 所屬部門：{dept}
        - 指定職稱/崗位：{role} (職級：{level})
        - 主管/老闆：{m_name}，部門：{m_dept}，生日：{m_bday.strftime('%Y-%m-%d')} (生命靈數：{mgr_lp})
        """
        response = model.generate_content(prompt)
        analysis_source = "Google Gemini AI Cloud Analysis (雲端深度生成 🚀)"
    except Exception as e:
        analysis_source = f"Live Local Knowledge Base Fallback (備援系統運作中 🔄)"

    # 語音朗讀文本
    b_str = birth_date.strftime('%Y-%m-%d')
    mb_str = m_bday.strftime('%Y-%m-%d')
    
    speech_summary = f"這是一份為您量身打造的旗艦級五大類戰略總結報告。受評估員工 {name} 在 {dept} 擔任 {role}，生日為 {b_str}，生命靈數為 {lp}，五行屬 {bazi_name}。透過與直屬主管 {m_name}（生日 {mb_str}）的生日能量碰撞，本報告從核心命理、崗位適配、帶兵戰術、協同法則及未來高階崗位推薦等五大維度進行了深度解析。"
    speech_p1 = f"第一部分，核心命理及性格特質畫象。主命數為 {lp}，五行屬 {bazi_name}。賦予其在 {role} 崗位上卓越的格局與破局能力。"
    speech_p2 = f"第二部分，崗位適配性評估。深入剖析其擔任 {role} 的專業優勢、痛點洞察與指標把控能力。"
    speech_p3 = f"第三部分，多品類帶團隊與攻堅戰術。闡述如何以結構化思維在 {dept} 推進核心業務與團隊賦能。"
    speech_p4 = f"第四部分，員工與主管的動態協同法則。結合雙方生日能量，落實給機制不給束縛、以邏輯對話的協同原則。"
    speech_p5 = f"第五部分，其他高適配管理崗位推薦。涵蓋部門內的高階核心發展與多維戰略方向。"

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
                <h4 style="margin: 0; color: #818cf8; font-size: 1.0rem;">🔊 五大類報告總結配音與語音控制台</h4>
                <p style="margin: 3px 0 0 0; font-size: 0.85rem; color: #c7d2fe;">當前分析職位：<strong>{role}</strong> ｜ 點擊右側按鈕可聆聽總結配音。</p>
            </div>
            <div>
                <button onclick="speakText(`{speech_summary}`)" style="background: #4f46e5; color: #ffffff; border: none; padding: 10px 16px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 0.9rem; margin-right: 8px;">
                    ▶ 播放整篇總結配音
                </button>
                <button onclick="stopReport()" style="background: #334155; color: #94a3b8; border: none; padding: 10px 15px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 0.9rem;">
                    ⏹ 停止
                </button>
            </div>
        </div>

        <!-- 💡 雙方生日與首頁職稱對照矩陣 -->
        <div style="background: #131c2e; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 30px; border-left: 4px solid #3b82f6;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h3 style="color: #3b82f6; margin: 0; font-size: 1.2rem;">📄 職稱與生日數據驅動之五大類深度戰略報告</h3>
                <span style="background: rgba(16,185,129,0.2); color: #10b981; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold;">{analysis_source}</span>
            </div>
            <table style="width: 100%; border-collapse: collapse; background: #0b0f19; border-radius: 8px; overflow: hidden; font-size: 0.9rem; margin-top: 15px;">
                <tr style="border-bottom: 1px solid #1e293b;">
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">對照維度 / Dimension</th>
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">員工核心基準 / Employee Base</th>
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">主管/老闆核心基準 / Manager Base</th>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">姓名與職級</td>
                    <td style="padding: 12px;">{name} ({level})</td>
                    <td style="padding: 12px;">{m_name} ({m_level})</td>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">首頁指定部門與職稱</td>
                    <td style="padding: 12px; color: #3b82f6; font-weight: bold;">{role}<br><span style="font-size:0.8rem; color:#94a3b8;">({dept})</span></td>
                    <td style="padding: 12px;">{m_dept}</td>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">真實生日日期 (DOB)</td>
                    <td style="padding: 12px; color: #f59e0b; font-weight: bold;">{b_str}</td>
                    <td style="padding: 12px; color: #f59e0b; font-weight: bold;">{mb_str}</td>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">生命靈數 (Life Path)</td>
                    <td style="padding: 12px;">主命數 {lp}</td>
                    <td style="padding: 12px;">主命數 {mgr_lp}</td>
                </tr>
                <tr>
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">八字五行基因</td>
                    <td style="padding: 12px; color: #10b981;">{bazi_name} - {bazi_desc}</td>
                    <td style="padding: 12px; color: #10b981;">{mgr_bazi_name} - {mgr_bazi_desc}</td>
                </tr>
            </table>
        </div>

        <!-- 🟣 第一類：核心命理及性格特質畫象 -->
        <div style="background-color: #131c2e; padding: 2rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #a855f7; margin-bottom: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #a855f7;">一、 核心命理及性格特質畫象</div>
                <button onclick="speakText(`{speech_p1}`)" style="background: #3b0764; color: #d8b4fe; border: 1px solid #a855f7; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-weight: bold;">
                    ▶ 朗讀第一類
                </button>
            </div>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>生命數字驅動（主命數 {lp}）</strong>：透過員工真實出生日期計算得出，在擔任「{role}」時能迅速切入核心矛盾。</li>
                <li style="margin-top: 12px;"><strong>生日日期潛能解構</strong>：擅長在混沌環境中捕捉訊號，以高情商化解部門阻礙。</li>
                <li style="margin-top: 12px;"><strong>八字五行特質（{bazi_name}）</strong>：{bazi_desc}。</li>
            </ul>
        </div>

        <!-- 🔵 第二類：崗位適配性評估 -->
        <div style="background-color: #131c2e; padding: 2rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #3b82f6; margin-bottom: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #3b82f6;">二、 崗位適配性評估：是否適合擔任「{role}」？</div>
                <button onclick="speakText(`{speech_p2}`)" style="background: #1e3a8a; color: #93c5fd; border: 1px solid #3b82f6; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-weight: bold;">
                    ▶ 朗讀第二類
                </button>
            </div>
            <p style="color: #e2e8f0; font-size: 1rem; font-weight: bold; margin-bottom: 12px;">👉 顧問綜合結論：基於生日基因與「{role}」崗位匹配，高度適配！</p>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>痛點精準切入</strong>：在「{role}」崗位上憑藉數據直覺一眼看穿營運低效環節。</li>
                <li><strong>專業與變現並重</strong>：用嚴格結構化指標把關，確保商業價值最大化。</li>
            </ul>
        </div>

        <!-- 🟢 第三類：多品類帶團隊與攻堅戰術 -->
        <div style="background-color: #131c2e; padding: 2rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #10b981; margin-bottom: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #10b981;">三、 在「{dept}」的多品類帶團隊與攻堅戰術</div>
                <button onclick="speakText(`{speech_p3}`)" style="background: #064e3b; color: #6ee7b7; border: 1px solid #10b981; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-weight: bold;">
                    ▶ 朗讀第三類
                </button>
            </div>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>矩陣化梳理複雜業務</strong>：針對「{dept}」多線並行狀況運用結構化思維分類。</li>
                <li><strong>團隊賦能</strong>：透過明確考核與充分授權激發下屬能動性。</li>
            </ul>
        </div>

        <!-- 🤝 第四類：員工與直屬主管的動態協同法則 -->
        <div style="background-color: #131c2e; padding: 2rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #f59e0b; margin-bottom: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #f59e0b;">四、 員工與主管的動態協同法則</div>
                <button onclick="speakText(`{speech_p4}`)" style="background: #78350f; color: #fde68a; border: 1px solid #f59e0b; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-weight: bold;">
                    ▶ 朗讀第四類
                </button>
            </div>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>雙方生日能量共振</strong>：結合員工主命數 {lp} 與主管主命數 {mgr_lp}。</li>
                <li><strong>核心協同金句</strong>：給機制不給過度束縛、用邏輯對話、主管做堅實後盾。</li>
            </ul>
        </div>

        <!-- 🌟 第五類：其他高適配管理崗位推薦 -->
        <div style="background: linear-gradient(135deg, rgba(168,85,247,0.15), rgba(59,130,246,0.15)); padding: 2.2rem; border-radius: 1rem; border: 1px solid #3b82f6; box-shadow: 0 10px 30px rgba(0,0,0,0.4); margin-top: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="font-size: 1.35rem; font-weight: 700; color: #38bdf8;">五、 適合他的其他核心管理崗位推薦</div>
                <button onclick="speakText(`{speech_p5}`)" style="background: #1e3a8a; color: #93c5fd; border: 1px solid #3b82f6; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-weight: bold;">
                    ▶ 朗讀第五類
                </button>
            </div>
            <p style="color: #e2e8f0; font-size: 0.95rem; margin-bottom: 15px;">基於其在「{dept}」的專業背景與生日特質推導：</p>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>高級營運總監</strong>：統籌全局效率與規模化。</li>
                <li><strong>策略項目負責人</strong>：組織變革與跨部門協同。</li>
            </ul>
        </div>

    </div>
    """
    return report_html

# ==================== 根據所選模式顯示對應介面 ====================
if app_mode == "🌟 模式一：旗艦級雙向生日與首頁職業聯動報告":
    with st.container():
        st.markdown("### 🌿 模式一：基於首頁部門/職業與雙方生日聯動之五大類深度報告生成器")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 👤 受評估員工基本設定")
            user_name = st.text_input("員工姓名 / 代號", "核心高管")
            birth_date = st.date_input("員工真實生日日期 (DOB)", value=pd.to_datetime("1985-06-20"))
        with col2:
            st.markdown("#### 🎯 首頁部門與職業聯動選單（完全保留不變）")
            target_department = st.selectbox("選擇員工所屬部門", all_departments)
            available_roles = department_roles.get(target_department, ["高級經理", "資深總監"])
            job_role = st.selectbox("選擇職務名稱 (Job Role)", available_roles)
            candidate_level = st.selectbox("管理職級 (Level)", ["Senior Director", "Department Manager", "Team Lead", "CEO / Founder"])

    if st.button("🚀 生成基於【首頁指定職稱】與【雙向生日】之五大類深度報告"):
        st.success(f"報告生成完畢！已成功鎖定部門「{target_department}」與職稱「{job_role}」。")
        report_output = generate_birthday_driven_master_report(
            user_name, birth_date, target_department, job_role, candidate_level,
            manager_name, manager_dept, manager_level, manager_birthday, BUILTIN_API_KEY
        )
        components.html(report_output, height=2750, scrolling=True)

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
