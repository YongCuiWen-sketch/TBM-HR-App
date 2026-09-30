import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 設定網頁標題與基本樣式（結合神聖幾何深色調與 Part 1/2/3 漸層色彩）
st.set_page_config(
    page_title="TBM-HR Visual Talent & Synergy Dashboard",
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
        --color-part1: #a855f7; /* 靈性紫漸層 */
        --color-part2: #3b82f6; /* 天空藍漸層 */
        --color-part3: #10b981; /* 生機綠漸層 */
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

    .stTextInput input, .stSelectbox select, .stDateInput input {
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
        🔯 TBM-HR Visual Talent & Synergy Dashboard
    </h1>
    <h3 style="font-size: 1rem; color: #94a3b8; font-weight: normal; margin: 0;">
        【TBM-HR 智慧人才與協作視覺化摘要看板（雙生日動態匹配旗艦版）】
    </h3>
</div>
""", unsafe_allow_html=True)

# ==================== 主頁 / 側邊欄：主管動態基準設定 ====================
with st.sidebar:
    st.header("🔮 直屬主管動態基準設定 (Manager Baseline)")
    
    manager_dept = st.selectbox(
        "主管所屬部門 (Manager Department)",
        [
            "創新事業與新領域開創部 (New Business Ventures & Innovation)",
            "市場行銷與品牌發展部 (Marketing & Brand Development)",
            "物流與供應鏈管理部 (Logistics & Supply Chain)",
            "資訊科技與數位轉型部 (IT & Digital Transformation)",
            "最高管理層 (Executive / C-Level Management)"
        ],
        key="mgr_dept"
    )
    
    manager_level = st.selectbox(
        "主管管理層級 (Manager Level)",
        [
            "最高執行長 / 創辦人 (CEO / Founder)",
            "資深總監 / 核心合夥人 (Senior Director / Partner)",
            "部門主管 / 營運經理 (Department / Operations Manager)",
            "專案領隊 / 資深技術主管 (Team Lead / Tech Lead)"
        ],
        key="mgr_lvl"
    )

    manager_birthday = st.date_input("主管真實生日 (Manager DOB)", value=pd.to_datetime("1982-05-10"), key="mgr_bday")
    
    st.markdown("---")
    st.success("✨ 雙向生日動態匹配引擎運作中")

# ==================== 核心動態命理計算函數 ====================
def calculate_life_path(birth_date):
    date_str = birth_date.strftime("%Y%m%d")
    total = sum(int(char) for char in date_str)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(char) for char in str(total))
    return total

def get_bazi_element(birth_date):
    year = birth_date.year
    elements = [
        ("金 (Metal)", "堅毅果斷、重規則與效率，具有金屬般的銳利洞察力。"),
        ("水 (Water)", "靈動應變、思維深邃，擅長在動態與人際中流轉溝通。"),
        ("木 (Wood)", "生機盎然、向上發展，充滿成長動能與開拓新局的企圖心。"),
        ("火 (Fire)", "熱情洋溢、內心向陽，具備強大感染力與突破困境的爆發力。"),
        ("土 (Earth)", "沉穩踏實、重視結構，是團隊最安穩的基石與風險守門人。")
    ]
    return elements[year % 5]

# ==================== 依據雙方生日動態生成完整報告的函數 ====================
def generate_dynamic_matched_report(name, birth_date, dept, role, level, m_dept, m_lvl, m_bday):
    # 計算員工生日密碼
    lp = calculate_life_path(birth_date)
    bazi_name, bazi_desc = get_bazi_element(birth_date)
    
    # 計算主管生日密碼
    mgr_lp = calculate_life_path(m_bday)
    mgr_bazi_name, mgr_bazi_desc = get_bazi_element(m_bday)
    
    report_html = f"""
    <div style="color: #e2e8f0; line-height: 1.7; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 10px;">
        
        <!-- 💡 快速導覽與動態匹配摘要矩陣 -->
        <div style="background: #131c2e; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 25px; border-left: 4px solid #3b82f6;">
            <h3 style="color: #3b82f6; margin-top: 0; font-size: 1.1rem;">💡 Quick Visual Overview / 雙向生日動態匹配矩陣</h3>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 12px;">
                受評估員工：<strong>{name}</strong> (輸入生日 DOB: {birth_date.strftime('%Y-%m-%d')}) ｜ <strong>目標崗位</strong>：<span style="color: #e2e8f0; font-weight: bold;">{dept} — {role} ({level})</span><br>
                直屬主管配置：<strong>{m_dept}</strong> ｜ 管理層級：<span style="color: #e2e8f0;">{m_lvl}</span> (主管生日 DOB: {m_bday.strftime('%Y-%m-%d')})<br>
                <strong>【動態匹配計算結果】</strong>：員工靈數 <strong style="color: #a855f7;">{lp} 號</strong> / 五行 <strong style="color: #10b981;">{bazi_name}</strong> 
                VS 主管靈數 <strong style="color: #3b82f6;">{mgr_lp} 號</strong> / 五行 <strong style="color: #10b981;">{mgr_bazi_name}</strong>
            </p>
            <table style="width: 100%; border-collapse: collapse; background: #0b0f19; border-radius: 8px; overflow: hidden; font-size: 0.88rem;">
                <tr style="border-bottom: 1px solid #1e293b;">
                    <th style="padding: 10px; text-align: left; color: #e2e8f0;">Dimension / 維度</th>
                    <th style="padding: 10px; text-align: left; color: #e2e8f0;">Employee Profile (DOB: {birth_date.strftime('%Y-%m-%d')})</th>
                    <th style="padding: 10px; text-align: left; color: #e2e8f0;">Manager Profile (DOB: {m_bday.strftime('%Y-%m-%d')})</th>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 10px;"><strong>Life Path / 生命靈數</strong></td>
                    <td style="padding: 10px; color: #a855f7; font-weight: bold;">Number {lp} (Pioneering/Vibrant)</td>
                    <td style="padding: 10px; color: #3b82f6; font-weight: bold;">Number {mgr_lp} (Structural/Guiding)</td>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 10px;"><strong>Bazi Element / 八字五行</strong></td>
                    <td style="padding: 10px; color: #10b981;">{bazi_name}</td>
                    <td style="padding: 10px; color: #10b981;">{mgr_bazi_name}</td>
                </tr>
                <tr>
                    <td style="padding: 10px;"><strong>Synergy Index / 協同指數</strong></td>
                    <td colspan="2" style="padding: 10px; color: #e2e8f0;">Dynamic Match Active: High Potential with Rhythmic Alignment Required</td>
                </tr>
            </table>
        </div>

        <!-- 🟣 Part 1: 個人本質解構、崗位適配與通用場景探測 -->
        <div style="background-color: #131c2e; padding: 1.8rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #a855f7; margin-bottom: 25px; box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
            <div style="font-size: 1.2rem; font-weight: 700; color: #a855f7; margin-bottom: 8px; border-bottom: 1px solid #1e293b; padding-bottom: 8px;">🟣 Part 1: Individual Essence, Role Fit & Universal Scenario Probing</div>
            <p style="font-size: 0.9rem; color: #a855f7; font-weight: bold; margin-bottom: 12px;">【第一部分：依據員工生日動態解構之個人本質、崗位適配與情境探測】</p>
            
            <h4 style="color: #e2e8f0; font-size: 1rem; margin: 15px 0 8px 0;">✨ 1. Core Strengths & Unique Advantages / 【核心優點與特質】</h4>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.9rem;">
                <li><strong>Sharpened Insight & Strategic Independent Thinking (Life Path {lp})</strong><br>
                <em>English</em>: Grounded in birth date {birth_date.strftime('%Y-%m-%d')} (Life Path {lp} and {bazi_name}), the candidate naturally looks beyond the surface, instantly grasping core logic and spotting strategic blind spots.<br>
                <em>中文</em>：根據輸入的生日計算，結合靈數 {lp} 與五行 {bazi_name} 的本質，不流於表象，總能一眼看穿事情背後的本質與邏輯盲點。</li>
                <li style="margin-top: 10px;"><strong>Inner Passion & Resilient Drive</strong><br>
                <em>English</em>: Their inner core is filled with passion for value realization, exhibiting explosive vitality and resilience when committed to a goal.<br>
                <em>中文</em>：內心深處對價值實現充滿熱情，當認可一個目標時，會展現出強大的生命力與突破困境的爆發力。</li>
                <li style="margin-top: 10px;"><strong>Magnetic Presence & Empethetic Resonance</strong><br>
                <em>English</em>: Possessing a natural presence and communication potential, earning deep trust alongside their strategic mindset.<br>
                <em>中文</em>：天生帶有吸引人注意的磁場與優秀的溝通潛能，在理性與策略之外更能凝聚信任。</li>
            </ul>

            <h4 style="color: #e2e8f0; font-size: 1rem; margin: 20px 0 8px 0;">⚖️ 2. Potential Blind Spots & Growth Challenges / 【潛在盲點與成長挑戰】</h4>
            <ul style="color: #94a3b8; padding-left: 20px; font-size: 0.9rem;">
                <li><strong>Mental Overload & Over-Introspection</strong><br>
                <em>English</em>: Influenced by high-frequency analytical traits (Life Path {lp}), they may occasionally over-analyze and self-doubt, leading to mental gridlock.<br>
                <em>中文</em>：受靈數 {lp} 追求完美與深思熟慮的特質影響，有時會在心中進行過度深刻的推演，導致思維陷入膠著。</li>
                <li style="margin-top: 10px;"><strong>High Standards & Potential Burnout</strong><br>
                <em>English</em>: High visions can cause frustration when environments fall short. Without timely decompression, simmering anxiety may occur.<br>
                <em>中文</em>：內心對事物有高標準，當環境不如預期時容易感到悶燒或焦慮。</li>
            </ul>

            <h4 style="color: #e2e8f0; font-size: 1rem; margin: 20px 0 8px 0;">🎯 3. Current Role Suitability & Universal Interview Probing / 【崗位適配與面試深挖話術】</h4>
            <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6;">
                <strong>Role Suitability Verdict / 當前崗位適配結論</strong>:<br>
                針對 **{dept}** 之 **{role} ({level})** **高度適合**。其生日密碼展現出開創與專案孵化天賦。<br><br>
                <strong>Universal Scenario Interview Probing / 通用情境面試探測話術</strong>:<br>
                * <em>Scenario</em>: In a fast-paced environment where project resources are suddenly cut and team opinions diverge.<br>
                * <em>Probing Questions</em>: 1. "When resources are slashed and your team resists your new direction, how do you handle the pressure and align everyone?" 2. "Can you share an experience where your pursuit of high standards clashed with the team's pace?"<br>
                <em>中文話術設定</em>：在專案資源突然被砍半、團隊成員意見分歧的快節奏環境中。<br>
                1. 「當資源被砍半、團隊抗拒你的新方向時，你如何承受壓力並重新對齊大家？」<br>
                2. 「能否分享一個經驗，當你追求的高標準與團隊節奏衝突時，你是如何解決的？」
            </p>
        </div>

        <!-- 🔵 Part 2: 跨部門流動與多元適配建議 -->
        <div style="background-color: #131c2e; padding: 1.8rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #3b82f6; margin-bottom: 25px; box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
            <div style="font-size: 1.2rem; font-weight: 700; color: #3b82f6; margin-bottom: 8px; border-bottom: 1px solid #1e293b; padding-bottom: 8px;">🔵 Part 2: Cross-Departmental Mobility & Alternative Fit</div>
            <p style="font-size: 0.9rem; color: #3b82f6; font-weight: bold; margin-bottom: 12px;">【第二部分：基於生日動態匹配之跨部門流動與多元適配建議】</p>
            <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.7;">
                <strong>English Assessment</strong>:<br>
                While highly suitable for their primary applied role in <strong>{dept}</strong>, their birthday fingerprint (Life Path {lp}, {bazi_name}) grants them high organizational mobility across alternative business units.<br><br>
                <strong>Alternative Departmental Recommendations / 其他部門流動推薦</strong>:<br>
                1. <strong>Strategic Planning / Corporate Development</strong>: Their elemental essence allows them to see through complex logic and spot strategic opportunities, ideal for long-term planning.<br>
                2. <strong>Brand Marketing & Corporate Communications</strong>: Their natural resonant expression makes them exceptionally strong in driving brand messaging.<br><br>
                <em>中文評估</em>：基於該員工輸入的生日動態計算，其具備極高組織流動潛能。除原申請部門外，極適合流動至**策略規劃部**（參與組織破局）或**品牌行銷部**（發揮傳遞價值感染力）。
            </p>
        </div>

        <!-- 🟢 Part 3: 主管與下屬協作磁場與頻率對齊分析模組 -->
        <div style="background-color: #131c2e; padding: 1.8rem; border-radius: 1rem; border: 1px solid #1e293b; border-top: 5px solid #10b981; margin-bottom: 25px; box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
            <div style="font-size: 1.2rem; font-weight: 700; color: #10b981; margin-bottom: 8px; border-bottom: 1px solid #1e293b; padding-bottom: 8px;">🟢 Part 3: Supervisor-Subordinate Synergy & Frequency Alignment Matrix</div>
            <p style="font-size: 0.9rem; color: #10b981; font-weight: bold; margin-bottom: 12px;">【第三部分：主管與下屬雙生日頻率對齊與協作磁場分析模組】</p>
            <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.7;">
                <strong>Baselines / 雙向生日動態基準對照</strong>：<br>
                * <strong>直屬主管配置</strong>：<code style="color: #e2e8f0;">{m_dept}</code> ｜ 層級：<code style="color: #e2e8f0;">{m_lvl}</code> (動態生日靈數 {mgr_lp} / 五行 {mgr_bazi_name})<br>
                * <strong>下屬/候選人配置</strong>：<code style="color: #e2e8f0;">{name}</code> — <strong>{dept}</strong> / <strong>{role}</strong> (動態生日靈數 {lp} / 五行 {bazi_name})<br><br>
                
                <strong>⚡ 1. Synergy Friction Points & Frequency Clash / 【潛在磁場摩擦點與頻率衝突預警】</strong><br>
                * <em>English Analysis</em>: <strong>Speed vs. Structure</strong>. The candidate (Life Path {lp}) moves fast and pushes for instant breakthroughs, while the supervisor from <strong>{m_dept}</strong> (Life Path {mgr_lp}) focuses on risk control and structural stability. This can cause the supervisor to view them as "too impulsive," while the candidate feels the supervisor is "too conservative."<br>
                * <em>中文分析</em>：<strong>速度與結構的落差</strong>。靈數 {lp} 的候選人習慣快速衝刺、追求即時破局；而來自 **{m_dept}** 的主管（靈數 {mgr_lp}）重視風險控管與結構規劃。容易導致雙方在節奏上產生急躁與保守的衝突感。<br><br>

                <strong>🧩 2. Complementary Advantages & Synergy Value / 【互補優勢與協同價值】</strong><br>
                * <em>English Analysis</em>: <strong>"The Frontline Spear and the Rear Guard Shield"</strong>. A classic combination where the candidate provides market momentum and the supervisor from <strong>{m_dept}</strong> provides operational safety nets and execution discipline.<br>
                * <em>中文分析</em>：<strong>「前線長矛與後方防護盾」</strong>。由來自 **{m_dept}** 的主管提供營運安全網與執行紀律，結合候選人的前線開拓動能，形成絕佳攻守組合。<br><br>

                <strong>🛠️ 3. Actionable Leadership Guide for the Supervisor / 【給直屬主管的實戰帶領與溝通指南】</strong><br>
                * <strong>Establish "Innovation Boundaries"</strong>: Set clear milestones and safe zones for experimentation within <strong>{dept}</strong>.<br>
                * <strong>Bridge the Communication Gap</strong>: When proposing bold ideas, the supervisor from <strong>{m_dept}</strong> can ask: <em>"What is the potential risk, and how can we build a small-scale pilot to test it safely?"</em><br>
                * <em>中文帶領指南</em>：來自 **{m_dept}** 的主管應針對 **{role}** 建立「創新邊界」，設定清楚的階段性里程碑與安全試驗區。當提出前衛想法時，主管可反問：「這個想法的潛在風險是什麼？我們該如何用最小成本做小規模試驗？」完美對齊雙方生日頻率。
            </p>
        </div>

    </div>
    """
    return report_html

# ==================== 主頁面輸入表單 ====================
with st.container():
    st.markdown("### 🌿 模式一：單人本質、雙生日動態匹配與協作評估")
    st.write("請輸入受評估員工的真實姓名與出生年月日（DOB），系統將依據您輸入的生日與主管生日進行靈活匹配與深度模擬：")
    
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("受評估員工姓名 / 應徵者代號", "張小明")
        birth_date = st.date_input("受評估員工出生年月日 (Employee DOB)", value=pd.to_datetime("1990-06-15"))
    
    with col2:
        target_department = st.selectbox(
            "選擇受評估員工所屬部門 (Employee Department)",
            [
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
        )
        job_role = st.text_input("職務名稱 (Job Role)", "新事業開發經理")
        candidate_level = st.selectbox("職級 Level", ["Senior Manager", "Manager", "Specialist", "Junior"])

if st.button("🚀 根據雙方生日動態匹配並生成旗艦級雙語深度報告"):
    st.success("雙生日動態匹配運算完成！以下為完全依據您輸入的生日與主管基準所組織而成的旗艦級視覺化看板：")
    
    # 呼叫動態報告生成函數，帶入所有動態計算參數
    report_output = generate_dynamic_matched_report(
        user_name, birth_date, target_department, job_role, candidate_level,
        manager_dept, manager_level, manager_birthday
    )
    
    # 使用 components.html 確保完美渲染網頁看板，絕不發生原始碼外露
    components.html(report_output, height=1900, scrolling=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>© 2026 TBM-HR Platform. Dynamic DOB-Based Matching & Sacred Geometry Aesthetics 🔯</p>", unsafe_allow_html=True)
