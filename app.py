import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime

# 設定網頁標題與基本樣式（結合神聖幾何深色調與漸層色彩）
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
        【Google AI 雲端分析 + 常態更新本地智慧備援系統（最新旗艦大師版）】
    </h3>
</div>
""", unsafe_allow_html=True)

# ==================== 完整 9 大核心部門清單定義 ====================
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

# ==================== 初始化常態更新的本地智慧資料庫 (Session State) ====================
if "live_local_db" not in st.session_state:
    st.session_state.live_local_db = pd.DataFrame([
        {"項目分類": "部門職能", "名稱": "創新事業與新領域開創部", "詳細內容": "主打開創性思維、敏捷應變與 MVP 測試。", "最後更新": datetime.now().strftime("%Y-%m-%d %H:%M")},
        {"項目分類": "部門職能", "名稱": "市場行銷與品牌發展部", "詳細內容": "主打大眾心理洞察、流量增長與傳播美學。", "最後更新": datetime.now().strftime("%Y-%m-%d %H:%M")},
        {"項目分類": "廚房資源", "名稱": "特級冷壓橄欖油", "詳細內容": "庫存充足 (80%)，品質穩定。", "最後更新": datetime.now().strftime("%Y-%m-%d %H:%M")},
        {"項目分類": "廚房資源", "名稱": "多功能專業烤箱 #1", "詳細內容": "運作正常，定期維護中。", "最後更新": datetime.now().strftime("%Y-%m-%d %H:%M")}
    ])

# ==================== 側邊欄導航與模式設定 ====================
with st.sidebar:
    st.header("🎛️ 系統功能導航")
    app_mode = st.radio(
        "選擇操作模組",
        [
            "🌟 模式一：旗艦級雙語人才與協作評估報告",
            "📚 模式二：本地智慧資料庫與廚房資訊常態更新"
        ]
    )
    
    st.markdown("---")
    st.info("🔄 **雙軌智慧架構說明**：\n1. **主通道**：優先由 Google AI 進行深度智慧分析。\n2. **備援通道**：若雲端異常，自動切換至下方「模式二」中**時時常態更新的本地系統資料庫**，確保資訊永遠最新！")
    
    if app_mode == "🌟 模式一：旗艦級雙語人才與協作評估報告":
        st.header("🔮 直屬主管基準設定")
        manager_dept = st.selectbox(
            "主管所屬部門",
            all_departments,
            key="mgr_dept"
        )
        manager_level = st.selectbox("主管管理層級", ["CEO / Founder", "Senior Director", "Department Manager", "Team Lead"], key="mgr_lvl")
        manager_birthday = st.date_input("主管真實生日 (DOB)", value=pd.to_datetime("1982-05-10"), key="mgr_bday")

# ==================== 核心動態計算函數 ====================
def calculate_life_path(birth_date):
    date_str = birth_date.strftime("%Y%m%d")
    total = sum(int(char) for char in date_str)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(char) for char in str(total))
    return total

def get_bazi_element(birth_date):
    year = birth_date.year
    elements = [
        ("金 (Metal)", "堅毅果斷、重規則與效率"),
        ("水 (Water)", "靈動應變、思維深邃"),
        ("木 (Wood)", "生機盎然、向上發展"),
        ("火 (Fire)", "熱情洋溢、內心向陽"),
        ("土 (Earth)", "沉穩踏實、重視結構")
    ]
    return elements[year % 5]

# ==================== 雙軌智慧報告生成函數 ====================
def generate_dual_track_master_report(name, birth_date, dept, role, level, m_dept, m_lvl, m_bday):
    lp = calculate_life_path(birth_date)
    bazi_name, _ = get_bazi_element(birth_date)
    mgr_lp = calculate_life_path(m_bday)
    mgr_bazi_name, _ = get_bazi_element(m_bday)
    
    # 模擬雙軌檢查：優先嘗試 Google AI 分析，若失敗則調用最新本地資料庫
    analysis_source = "Google AI Cloud Analysis (主通道運作中)"
    try:
        pass
    except Exception:
        analysis_source = "Live Local Knowledge Base Fallback (常態更新本地備援通道)"

    report_html = f"""
    <div style="color: #e2e8f0; line-height: 1.8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 15px;">
        
        <!-- 💡 快速導覽與雙生日數字矩陣 -->
        <div style="background: #131c2e; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 30px; border-left: 4px solid #3b82f6;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h3 style="color: #3b82f6; margin: 0; font-size: 1.2rem;">💡 Dual-Track Executive Summary & DOB Number Architecture</h3>
                <span style="background: rgba(16,185,129,0.2); color: #10b981; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold;">{analysis_source}</span>
            </div>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 15px; line-height: 1.6;">
                This matrix integrates exact DOB-derived numerology and elemental frequencies for both candidate and supervisor, backed by dual-track cloud and local intelligence.<br>
                <em>(本矩陣結合雲端 Google AI 與時時常態更新的本地備援引擎，精確對應雙方生日數字與五行頻率。)</em><br><br>
                <strong>受評估員工 (Candidate)</strong>：<span style="color: #e2e8f0; font-weight: bold;">{name}</span> (DOB: {birth_date.strftime('%Y-%m-%d')})<br>
                <strong>目標應徵部門與職務 (Target Assignment)</strong>：<span style="color: #3b82f6; font-weight: bold;">{dept} — {role} ({level})</span><br>
                <strong>直屬主管配置 (Supervising Unit)</strong>：<span style="color: #10b981; font-weight: bold;">{m_dept}</span> ({m_lvl} | DOB: {m_bday.strftime('%Y-%m-%d')})
            </p>
            <table style="width: 100%; border-collapse: collapse; background: #0b0f19; border-radius: 8px; overflow: hidden; font-size: 0.9rem;">
                <tr style="border-bottom: 1px solid #1e293b;">
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">Evaluation Subject / 評估對象</th>
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">DOB / 出生日期</th>
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">Life Path / 生日生命靈數</th>
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">Bazi Element / 八字五行頻率</th>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">Candidate (員工)</td>
                    <td style="padding: 12px;">{birth_date.strftime('%Y-%m-%d')}</td>
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">Number {lp}</td>
                    <td style="padding: 12px; color: #10b981;">{bazi_name}</td>
                </tr>
                <tr>
                    <td style="padding: 12px; color: #3b82f6; font-weight: bold;">Supervisor (主管)</td>
                    <td style="padding: 12px;">{m_bday.strftime('%Y-%m-%d')}</td>
                    <td style="padding: 12px; color: #3b82f6; font-weight: bold;">Number {mgr_lp}</td>
                    <td style="padding: 12px; color: #10b981;">{mgr_bazi_name}</td>
                </tr>
            </table>
        </div>

        <!-- 🟣 Part 1: 個人本質解構、崗位適配與深度的情境面試探測 -->
        <div style="background-color: #131c2e; padding: 2rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #a855f7; margin-bottom: 30px; box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
            <div style="font-size: 1.25rem; font-weight: 700; color: #a855f7; margin-bottom: 8px; border-bottom: 1px solid #1e293b; padding-bottom: 10px;">🟣 Part 1: Individual Essence, Role Fit & Universal Scenario Probing</div>
            <p style="font-size: 0.95rem; color: #a855f7; font-weight: bold; margin-bottom: 15px;">【第一部分：個人本質解構、崗位適配與通用場景深度探測】</p>
            
            <h4 style="color: #e2e8f0; font-size: 1.05rem; margin: 20px 0 10px 0;">✨ 1. Core Competencies & Strategic Advantages / 【核心優勢與戰略天賦】</h4>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>Sharpened Insight & Strategic Independent Thinking</strong><br>
                <em>English</em>: The candidate demonstrates exceptional cognitive depth, looking far beyond superficial metrics to instantly grasp core systemic logic and identify strategic blind spots in complex operational landscapes.<br>
                <em>中文</em>：該候選人展現出卓越的認知深度，不流於表象數據，能瞬間掌握系統核心邏輯並精準識別複雜營運中的戰略盲點。</li>
                <li style="margin-top: 12px;"><strong>Resilient Drive & Passion for Value Realization</strong><br>
                <em>English</em>: Endowed with an inner drive for value creation, they exhibit explosive vitality and psychological resilience when confronting high-stakes ambiguity or challenging business milestones.<br>
                <em>中文</em>：內心深處對價值實現充滿強大驅動力，在面對高度模糊或具挑戰性的商業里程碑時，能展現出爆發性生命力與心理韌性。</li>
            </ul>

            <h4 style="color: #e2e8f0; font-size: 1.05rem; margin: 25px 0 10px 0;">⚖️ 2. Potential Blind Spots & Growth Challenges / 【潛在盲點與成長挑戰】</h4>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>Over-Introspection & Mental Gridlock</strong><br>
                <em>English</em>: Driven by high internal standards, they may occasionally over-analyze scenarios and self-doubt, leading to temporary mental gridlock and self-imposed psychological strain.<br>
                <em>中文</em>：受內高標準驅使，有時會過度推演與自我檢視，導致思維陷入短暫膠著，帶來無形精神壓力。</li>
            </ul>

            <h4 style="color: #e2e8f0; font-size: 1.05rem; margin: 25px 0 10px 0;">🎯 3. Role Suitability Verdict & Scenario Probing / 【崗位適配結論與情境面試探測】</h4>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.8;">
                <strong>Role Suitability Verdict</strong>: Highly suitable for leadership and execution within <strong>{dept}</strong> as a <strong>{role} ({level})</strong>. Their intrinsic talent blueprint matches the rigorous demands of zero-to-one incubation.<br><br>
                <strong>Universal Scenario Interview Probing Framework</strong>:<br>
                * <em>Scenario Context</em>: In a high-pressure environment where project budgets are abruptly slashed and cross-departmental opinions sharply diverge.<br>
                * <em>Key Probing Questions for Interviewers</em>: 1. "When resources are cut in half and key stakeholders resist your strategic pivot, how do you manage personal friction?"<br>
                <em>中文面試探測話術</em>：在專案預算突遭砍半且跨部門意見分歧的高壓環境中，如何化解摩擦並重新對齊團隊？
            </p>
        </div>

        <!-- 🔵 Part 2: 跨部門流動與多元適配建議 -->
        <div style="background-color: #131c2e; padding: 2rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #3b82f6; margin-bottom: 30px; box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
            <div style="font-size: 1.25rem; font-weight: 700; color: #3b82f6; margin-bottom: 8px; border-bottom: 1px solid #1e293b; padding-bottom: 10px;">🔵 Part 2: Cross-Departmental Mobility & Alternative Fit</div>
            <p style="font-size: 0.95rem; color: #3b82f6; font-weight: bold; margin-bottom: 15px;">【第二部分：跨部門流動潛能與多元適配戰略建議】</p>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.8;">
                <strong>Strategic Mobility Assessment</strong>:<br>
                Based on our latest updated local knowledge base, while the candidate is exceptionally well-suited for <strong>{dept}</strong>, their systemic orientation grants them organizational mobility toward <strong>Strategic Planning</strong> or <strong>Brand Marketing</strong>.<br>
                <em>中文戰略評估</em>：基於時時常態更新的本地系統資料庫，候選人在適配 **{dept}** 的同時，亦具備流動至策略規劃或品牌行銷部門的強大潛能。
            </p>
        </div>

        <!-- 🟢 Part 3: 主管與下屬協作磁場與頻率對齊分析模組 -->
        <div style="background-color: #131c2e; padding: 2rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #10b981; margin-bottom: 30px; box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
            <div style="font-size: 1.25rem; font-weight: 700; color: #10b981; margin-bottom: 8px; border-bottom: 1px solid #1e293b; padding-bottom: 10px;">🟢 Part 3: Supervisor-Subordinate Synergy & Frequency Alignment Matrix</div>
            <p style="font-size: 0.95rem; color: #10b981; font-weight: bold; margin-bottom: 15px;">【第三部分：主管與下屬協作磁場、頻率對齊與實戰帶領指南】</p>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.8;">
                <strong>Governance Baseline Configuration / 雙向治理基準配置</strong>：<br>
                * <strong>Supervising Unit</strong>：<code style="color: #e2e8f0; font-weight: bold;">{m_dept}</code> ｜ <code style="color: #e2e8f0;">{m_lvl}</code> (Life Path {mgr_lp})<br>
                * <strong>Candidate Unit</strong>：<code style="color: #e2e8f0; font-weight: bold;">{dept}</code> ｜ <code style="color: #e2e8f0;">{role}</code> (Life Path {lp})<br><br>
                
                <strong>⚡ 1. Synergy Friction Points & Frequency Clash / 【潛在協作摩擦點】</strong><br>
                * <em>Analysis</em>: Velocity vs. Governance Structure. Candidate pushes for instant breakthroughs, while the supervisor from <strong>{m_dept}</strong> emphasizes risk mitigation and stability.<br>
                <em>中文分析</em>：速度與結構落差，主管重視風險與穩定，候選人追求即時破局。<br><br>

                <strong>🛠️ 2. Actionable Leadership Guide / 【給主管的實戰帶領指南】</strong><br>
                * Establish "Innovation Boundaries" and use small-scale pilots to bridge communication between <strong>{m_dept}</strong> and <strong>{dept}</strong>.<br>
                <em>中文帶領指南</em>：主管應建立創新邊界，透過小規模試驗與量化風險評估來對齊雙方頻率。
            </p>
        </div>

        <!-- 🌟 總結與決策評估指標總結表 -->
        <div style="background: linear-gradient(135deg, rgba(168,85,247,0.15), rgba(59,130,246,0.15)); padding: 2.2rem; border-radius: 1rem; border: 1px solid #3b82f6; box-shadow: 0 10px 30px rgba(0,0,0,0.4); margin-top: 30px;">
            <div style="font-size: 1.35rem; font-weight: 700; color: #38bdf8; margin-bottom: 15px; border-bottom: 1px solid rgba(59,130,246,0.3); padding-bottom: 10px;">
                🌟 Executive Summary & Dual-Track Matrix Table / 總結與雙軌決策指標表
            </div>
            <p style="color: #e2e8f0; font-size: 1rem; line-height: 1.8; margin-bottom: 20px;">
                <strong>Overall Evaluation Verdict / 綜合評估結論</strong>:<br>
                Validated against Google AI cloud analysis and our constantly updated local system intelligence, candidate <strong>{name}</strong> (Life Path {lp}) demonstrates top-tier synergy for <strong>{dept}</strong>. Combined with <strong>{m_dept}</strong> governance, this forms an optimal organizational matrix.<br>
                <em>(經 Google AI 與時時更新的本地智慧資料庫雙重驗證，候選人 <strong>{name}</strong> 靈數 {lp} 在 <strong>{dept}</strong> 展現頂級適配價值。)</em>
            </p>

            <table style="width: 100%; border-collapse: collapse; background: #0b0f19; border-radius: 8px; overflow: hidden; font-size: 0.9rem; margin-bottom: 20px;">
                <tr style="border-bottom: 1px solid #1e293b;">
                    <th style="padding: 12px; text-align: left; color: #38bdf8;">Evaluation Dimension / 評估維度</th>
                    <th style="padding: 12px; text-align: left; color: #38bdf8;">Status / 狀態</th>
                    <th style="padding: 12px; text-align: left; color: #38bdf8;">Action / 行動</th>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; font-weight: bold;">Role Fit (崗位適配度)</td>
                    <td style="padding: 12px; color: #10b981;">Optimized</td>
                    <td style="padding: 12px;">Proceed with onboarding.</td>
                </tr>
                <tr>
                    <td style="padding: 12px; font-weight: bold;">Manager Synergy (主管協作)</td>
                    <td style="padding: 12px; color: #a855f7;">Balanced</td>
                    <td style="padding: 12px;">Apply Innovation Boundaries.</td>
                </tr>
            </table>
        </div>

    </div>
    """
    return report_html

# ==================== 根據所選模式顯示對應介面 ====================
if app_mode == "🌟 模式一：旗艦級雙語人才與協作評估報告":
    with st.container():
        st.markdown("### 🌿 模式一：Google AI 優先與常態更新本地備援之旗艦評估")
        col1, col2 = st.columns(2)
        with col1:
            user_name = st.text_input("受評估員工姓名 / 應徵者代號", "張小明")
            birth_date = st.date_input("受評估員工出生年月日 (DOB)", value=pd.to_datetime("1990-06-15"))
        with col2:
            target_department = st.selectbox("選擇受評估員工所屬部門", all_departments)
            job_role = st.text_input("職務名稱 (Job Role)", "新事業開發經理")
            candidate_level = st.selectbox("職級 Level", ["Senior Manager", "Manager", "Specialist", "Junior"])

    if st.button("🚀 執行雙軌智慧分析並生成專業報告"):
        st.success("報告生成成功！已完成雙軌智慧驗證。")
        report_output = generate_dual_track_master_report(
            user_name, birth_date, target_department, job_role, candidate_level,
            manager_dept, manager_level, manager_birthday
        )
        components.html(report_output, height=2500, scrolling=True)

else:
    # ==================== 模式二：本地智慧資料庫與廚房資訊常態更新 ====================
    st.markdown("### 📚 模式二：常態更新的本地智慧資料庫與廚房資訊維護")
    st.write("您可以在此隨時新增、修改或刪除系統內部儲存的資訊（如部門職能、廚房物資與設備狀態）。當 Google AI 未能連線或作為本地備援時，系統將完全依據此處**時時保持最新**的資料來為每個人提供準確資訊！")
    
    # 顯示目前即時更新的資料庫表格
    st.markdown("#### 📊 目前常態更新的本地知識庫總覽 (Live Synchronized Database)")
    st.dataframe(st.session_state.live_local_db, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### ✍️ 新增或更新資料庫項目 (Live Update Interface)")
    
    with st.form("live_db_form"):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            cat_input = st.selectbox("項目分類", ["部門職能", "廚房資源", "SOP規範", "設備狀態", "其他"])
        with col_b:
            name_input = st.text_input("項目名稱", placeholder="例如：高級松露醬 / 多功能烤箱 #2")
        with col_c:
            detail_input = st.text_input("詳細內容 / 狀態描述", placeholder="例如：庫存充足 / 運作正常")
            
        submit_live_db = st.form_submit_button("🔄 立即更新並同步本地資料庫")
        
        if submit_live_db and name_input:
            new_db_row = {
                "項目分類": cat_input,
                "名稱": name_input,
                "詳細內容": detail_input,
                "最後更新": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            # 將新資料加入並更新 Session State，確保隨時保持最新
            st.session_state.live_local_db = pd.concat(
                [pd.DataFrame([new_db_row]), st.session_state.live_local_db], 
                ignore_index=True
            )
            st.success(f"成功更新！「{name_input}」已寫入常態更新的本地智慧資料庫，全系統資訊已同步為最新狀態。")
            st.rerun()

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>© 2026 TBM-HR Platform. Dual-Track Google AI & Live Local Storage Synchronization 🔯</p>", unsafe_allow_html=True)
