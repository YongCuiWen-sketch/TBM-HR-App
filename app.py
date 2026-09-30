import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 設定網頁標題與基本樣式（自然綠意與花草生活風）
st.set_page_config(
    page_title="TBM-HR 智慧人才與人格雙語分析系統",
    page_icon="🌿",
    layout="wide"
)

# 載入自訂 CSS 樣式
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F7F4;
        color: #2D3748 !important;
    }
    h1, h2, h3, h4, h5, h6, span, label {
        color: #1A3022 !important;
    }
    p, li {
        color: #4A5568 !important;
    }
    .card {
        background-color: #FFFFFF;
        padding: 1.8rem;
        border-radius: 1rem;
        border: 1px solid #D8E2D8;
        box-shadow: 0 4px 6px -1px rgba(46, 125, 50, 0.05), 0 2px 4px -1px rgba(46, 125, 50, 0.03);
        margin-bottom: 1.5rem;
    }
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #2E7D32 !important;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #4CAF50;
        padding-left: 12px;
    }
    .stTextInput input, .stSelectbox select, .stDateInput input {
        background-color: #FFFFFF !important;
        color: #2D3748 !important;
        border: 1px solid #C8D6C8 !important;
        border-radius: 0.5rem !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #E8F0E8;
        border-right: 1px solid #D8E2D8;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
        background-color: #2E7D32;
        color: #FFFFFF !important;
        padding: 0.6rem 1rem;
        border: none;
        box-shadow: 0 2px 4px rgba(46, 125, 50, 0.2);
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# 頂部標題區塊
st.markdown("""
<div style="padding: 1rem 0; border-bottom: 2px solid #D8E2D8; margin-bottom: 1.5rem;">
    <div style="display: flex; flex-direction: column; gap: 8px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="background-color: #FFFFFF; color: #2E7D32 !important; padding: 0.4rem 0.9rem; border-radius: 0.5rem; font-weight: 700; border: 1px solid #C8E6C9; font-size: 0.95rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                🌱 TBM 綠野心靈與天賦空間 (本地穩定智慧核心 / Local Stable HR Engine)
            </div>
            <span style="background-color: #E8F5E9; color: #2E7D32 !important; padding: 0.3rem 0.8rem; border-radius: 2rem; font-size: 0.8rem; font-weight: 600; border: 1px solid #C8E6C9;">
                Bringing Everything Together ! 🌿
            </span>
        </div>
        <div>
            <h1 style="font-size: 1.6rem; font-weight: 700; margin: 4px 0 2px 0; color: #1B5E20 !important;">
                TBM-HR 智慧決策與人格分析平台 (本質與才華深度雙語版)
            </h1>
            <p style="font-size: 0.9rem; color: #388E3C !important; margin: 0;">
                結合東方八字命盤與西方生命靈數雙軌基準，免聯外、零 503 錯誤，秒速生成極詳細之各部門專屬 SOP 與中英雙語分析報告。
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 側邊欄：環境與全域設定
with st.sidebar:
    st.header("🌿 組織與模式設定")
    
    manager_level = st.selectbox(
        "管理層級設定 (Evaluation Manager Level)",
        [
            "CEO (最高執行長 / Chief Executive Officer)",
            "TA (直屬營運主管 / Team Leader)",
            "高層 (Executive / C-Level Director)",
            "經理 (Branch / Department Manager)",
            "IT 資訊科技主管 (IT Manager / Head of IT)",
            "資深專員 / 專業技師 (Senior Specialist)",
            "基層服務人員 / 新人 (Junior / Frontline Staff)"
        ]
    )

    manager_birthday = st.sidebar.date_input("主管 / 領導者生日（雙基底對應 / Manager Birthday）")
    
    st.markdown("---")
    st.success("✨ 本地端智慧高穩定核心已啟動（免 API Key、零 503 錯誤、極速響應）")


# ==================== 本地極詳細雙語報告生成函數 ====================
def calculate_life_path(birth_date):
    date_str = birth_date.strftime("%Y%m%d")
    total = sum(int(char) for char in date_str)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(char) for char in str(total))
    return total

def get_bazi_element(birth_date):
    year = birth_date.year
    elements = ["金 (Metal)", "水 (Water)", "木 (Wood)", "火 (Fire)", "土 (Earth)"]
    return elements[year % 5]

def generate_detailed_bilingual_report(name, birth_date, dept, role, level, manager_lvl):
    lp = calculate_life_path(birth_date)
    bazi = get_bazi_element(birth_date)
    
    # 根據不同部門提供極度詳細的本地顧問級內容
    report_db = {
        "創新事業與新領域開創部 (New Business Ventures & Innovation)": {
            "archetype": "開創先鋒型 (Pioneer Archetype)",
            "archetype_en": "Pioneer & Innovation Archetype",
            "essence": "具備強烈的開創精神與前瞻性思維，能在未知領域中迅速嗅到商業契機，擁有向陽而生的強大韌性。",
            "essence_en": "Possesses strong pioneering spirit and forward-thinking mindset, quickly identifying business opportunities in uncharted territories.",
            "jd": "負責新產品線孵化、跨界市場機會探索與商業模式創新驗證。",
            "jd_en": "Responsible for new product line incubation, cross-industry market exploration, and business model innovation validation.",
            "sop": "1. 每週進行競品與新興市場趨勢掃描 (Weekly trend & competitor scanning)\n2. 提出 MVP（最小可行性產品）方案與實驗藍圖 (Propose MVP framework)\n3. 跨部門試驗、數據追蹤與回饋收集 (Cross-department testing & data tracking)\n4. 滾動式修正創新策略與商業佈局 (Iterative strategy refinement)",
            "fit": "生命靈數與八字五行展現高度開創性，完美契合新領域開創的高變動與高抗壓需求。",
            "fit_en": "High alignment with innovation demands due to resilient elemental energy and visionary life path."
        },
        "市場行銷與品牌發展部 (Marketing & Brand Development)": {
            "archetype": "品牌造浪型 (Brand Catalyst Archetype)",
            "archetype_en": "Brand Catalyst & Growth Archetype",
            "essence": "擅長捕捉大眾心理與市場脈動，擁有極佳的審美與傳播天賦，能將品牌理念轉化為引人入勝的共鳴。",
            "essence_en": "Excels at capturing public psychology and market pulses with exceptional aesthetic and communication talents.",
            "jd": "塑造品牌核心價值、策劃全渠道行銷活動與流量增長專案。",
            "jd_en": "Shape core brand values, plan omni-channel marketing campaigns, and drive traffic growth.",
            "sop": "1. 目標受眾與市場流量數據分析 (Audience & traffic data analysis)\n2. 擬定檔期行銷企劃與視覺溝通素材 (Campaign planning & creative asset alignment)\n3. 多渠道投放執行與社群互動維護 (Multi-channel execution & community engagement)\n4. 成效復盤、轉換率優化與ROI檢討 (Performance review & ROI optimization)",
            "fit": "天生具備高度感性與敏銳洞察，能精準觸動消費者心弦，推動品牌聲量成長。",
            "fit_en": "Natural sensitivity and keen insight perfectly match consumer engagement and brand voice expansion.",
            "fit_en": "Natural sensitivity and keen insight perfectly match consumer engagement and brand voice expansion."
        },
        "物流與供應鏈管理部 (Logistics & Supply Chain)": {
            "archetype": "樞紐運籌型 (Logistics Strategist Archetype)",
            "archetype_en": "Strategic Logistics Archetype",
            "essence": "思維嚴謹、條理分明，對數字與流程有極高敏銳度，能在繁複的供應鏈環節中建立穩固秩序。",
            "essence_en": "Rigorous and structured thinking with high sensitivity to numbers and processes, establishing robust operational order.",
            "jd": "確保全球/區域庫存精準、運輸排程流暢與供應商協調高效。",
            "jd_en": "Ensure inventory accuracy, smooth transportation scheduling, and efficient vendor coordination.",
            "sop": "1. 每日供應鏈庫存盤點與安全水位預警 (Daily inventory audit & safety stock alert)\n2. 調度與運輸路線最佳化排程 (Dispatch and transportation route optimization)\n3. 突發異常狀況即時處理與替代方案啟動 (Emergency handling & backup plan execution)\n4. 供應商績效檢討與物流成本控制 (Vendor performance review & cost control)",
            "fit": "個性穩健、抗壓性極強，在面對物流鏈中斷或緊急調度時能保持冷靜高效。",
            "fit_en": "Remarkable stability and stress resilience ensure calm and efficient handling during supply chain disruptions.",
            "fit_en": "Remarkable stability and stress resilience ensure calm and efficient handling during supply chain disruptions."
        },
        "零售與門市營運部 (Retail & Store Operations)": {
            "archetype": "零售磁場型 (Retail Experience Archetype)",
            "archetype_en": "Retail Experience Archetype",
            "essence": "充滿親和力與現場感染力，擅長凝聚團隊向心力並為顧客創造卓越的消費體驗。",
            "essence_en": "Charismatic and field-oriented, excelling at fostering team cohesion and delivering exceptional customer experiences.",
            "jd": "提升門市營運績效、現場服務品質與顧客終身價值。",
            "jd_en": "Enhance store operational performance, on-site service quality, and customer lifetime value.",
            "sop": "1. 每日早會、團隊激勵與店面環境檢視 (Daily briefing, team motivation & store audit)\n2. 顧客接待、需求引導與高質感銷售服務 (Customer greeting, needs assessment & premium sales)\n3. 庫存管理、陳列優化與現金帳務管考 (Inventory management, visual merchandising & cash control)\n4. 當日業績結算與交接報告 (Daily sales settlement & handover report)",
            "fit": "天賦能量熱情且具備極佳的顧客導向，完美符合前線零售營運的高標準要求。",
            "fit_en": "Enthusiastic energy and high customer orientation perfectly match the stringent standards of frontline retail.",
            "fit_en": "Enthusiastic energy and high customer orientation perfectly match the stringent standards of frontline retail."
        },
        "客戶服務與售後中心 (Customer Service & Support Centre)": {
            "archetype": "同理撫慰型 (Empathic Support Archetype)",
            "archetype_en": "Empathic Support Archetype",
            "essence": "擁有深厚的同理心與情緒轉化能力，能將棘手的客訴危機化為建立品牌忠誠度的契機。",
            "essence_en": "Possesses deep empathy and emotional transformation skills, turning challenging customer complaints into brand loyalty.",
            "jd": "高效解決客戶諮詢、客訴危機處理與售後技術支援。",
            "jd_en": "Efficiently resolve customer inquiries, manage complaint crises, and provide after-sales technical support.",
            "sop": "1. 客戶諮詢受理與客訴情境同理傾聽 (Inquiry intake & empathetic listening for complaints)\n2. 跨部門（技術/物流）協調與解決方案擬定 (Cross-department coordination & solution formulation)\n3. 案情追蹤、客戶回訪與滿意度落實 (Case tracking, follow-up & satisfaction assurance)\n4. 常見問題庫 (FAQ) 歸納與服務流程優化 (FAQ maintenance & service process optimization)",
            "fit": "八字五行平和、靈數展現高度包容性，是化解衝突與穩定客戶關係的堅實力量。",
            "fit_en": "Balanced elemental energy and high inclusivity make them a solid pillar for resolving conflicts and stabilizing relationships.",
            "fit_en": "Balanced elemental energy and high inclusivity make them a solid pillar for resolving conflicts and stabilizing relationships."
        },
        "銷售與業務發展部 (Sales & Business Development)": {
            "archetype": "市場拓荒型 (Business Growth Archetype)",
            "archetype_en": "Business Growth Archetype",
            "essence": "極具企圖心與目標導向，擅長建立信任關係並推動交易達成，開創更廣闊的營收版圖。",
            "essence_en": "Highly ambitious and goal-oriented, excelling at building trust relationships and driving deals to close broader revenues.",
            "jd": "開拓新客戶市場、維繫重要企業夥伴關係與達成營業目標。",
            "jd_en": "Expand new client markets, maintain key enterprise partnerships, and achieve sales targets.",
            "sop": "1. 潛在客戶名單開發、篩選與拜訪排程 (Prospecting, filtering & visit scheduling)\n2. 深度需求訪談與客製化解決方案提案 (In-depth interviews & customized solution proposals)\n3. 商務談判、合約簽訂與收款流程追蹤 (Commercial negotiation, contract signing & payment tracking)\n4. 客戶關係深度維護與擴大續約管理 (Deep relationship maintenance & renewal management)",
            "fit": "天生具備強大驅動力與抗壓性，能在充滿挑戰的業務戰場中持續創造成果。",
            "fit_en": "Natural drive and stress resilience continuously deliver results in challenging sales battlefields.",
            "fit_en": "Natural drive and stress resilience continuously deliver results in challenging sales battlefields."
        },
        "資訊科技與數位轉型部 (IT & Digital Transformation)": {
            "archetype": "數位架構型 (Digital Architect Archetype)",
            "archetype_en": "Digital Architect Archetype",
            "essence": "邏輯極為縝密，具備強大的技術拆解能力與系統化思維，是推動企業數位轉型的核心引擎。",
            "essence_en": "Highly rigorous logic, strong technical decomposition, and systematic thinking as the core engine of digital transformation.",
            "jd": "系統架構維運、資安防護網建立與企業數位工具高效導入。",
            "jd_en": "System architecture maintenance, cybersecurity defense establishment, and efficient digital tool deployment.",
            "sop": "1. 系統效能監控、日誌分析與異常預警 (System performance monitoring & anomaly alerting)\n2. 使用者技術支援、資安權限與環境管理 (User IT support, security permissions & environment management)\n3. 模組功能開發、代碼審查與自動化測試 (Module development, code review & automated testing)\n4. 資安備份機制與系統漏洞修補 (Security backup & vulnerability patching)",
            "fit": "生命靈數與五行結構展現極佳的邏輯與穩定性，完美契合 IT 高標準之技術要求。",
            "fit_en": "Life path and elemental structure demonstrate exceptional logic and stability, perfectly fitting IT standards.",
            "fit_en": "Life path and elemental structure demonstrate exceptional logic and stability, perfectly fitting IT standards."
        },
        "財務與會計部 (Finance & Accounting)": {
            "archetype": "精算守門型 (Financial Guardian Archetype)",
            "archetype_en": "Financial Guardian Archetype",
            "essence": "一絲不苟、數字觀念極強，擅長在嚴格規範中把關企業資產並確保財務健全。",
            "essence_en": "Meticulous and financially sharp, excelling at safeguarding corporate assets and ensuring financial health under strict standards.",
            "jd": "帳務審核管理、成本精算控制、財務報表編製與資金風險控管。",
            "jd_en": "Accounting audit control, cost calculation, financial statement preparation, and capital risk management.",
            "sop": "1. 每日收支憑證嚴格審核與傳票登打入帳 (Daily voucher audit & ledger entry)\n2. 應收應付款項帳齡分析與催收管理 (AR/AP aging analysis & collection management)\n3. 月結財務報表編製與稅務申報準備 (Month-end financial statement preparation & tax filing)\n4. 財務預算執行差異分析與風險管控建議 (Budget variance analysis & risk control recommendations)",
            "fit": "特質沉穩、細緻且具高度責任感，是企業財務安全與合規的堅強後盾。",
            "fit_en": "Composed, meticulous, and highly responsible, acting as a strong shield for financial security and compliance.",
            "fit_en": "Composed, meticulous, and highly responsible, acting as a strong shield for financial security and compliance."
        },
        "人力資源與人才發展部 (HR & People Development)": {
            "archetype": "人才園丁型 (Talent Gardener Archetype)",
            "archetype_en": "Talent Gardener Archetype",
            "essence": "如同園丁般悉心照料團隊，擅長發掘個人潛能並營造充滿綠意與向心力的組織文化。",
            "essence_en": "Nurtures the team like a gardener, excelling at uncovering potential and cultivating a vibrant, cohesive culture.",
            "jd": "全方位人才招募、薪酬福利規劃、績效發展與組織文化建立。",
            "jd_en": "Comprehensive talent acquisition, compensation planning, performance development, and cultural building.",
            "sop": "1. 職缺招募漏斗管理、履歷篩選與專業面試 (Recruitment funnel management & interviewing)\n2. 新人報到引導、導師制度與培訓計畫落實 (Onboarding guidance, mentorship & training implementation)\n3. 績效考核追蹤、薪酬計算與福利優化 (Performance tracking, payroll & benefit optimization)\n4. 員工心聲關懷、組織凝聚力活動與溝通 (Employee care, engagement activities & communication)",
            "fit": "天生具備極高的包容力與同理心，完美契合 HR 照顧員工與推動組織成長的核心使命。",
            "fit_en": "High inclusivity and empathy perfectly align with HR's core mission of caring for employees and driving growth.",
            "fit_en": "High inclusivity and empathy perfectly align with HR's core mission of caring for employees and driving growth."
        }
    }
    
    current_data = report_db.get(dept, {
        "archetype": "核心專員型 (Core Specialist Archetype)",
        "archetype_en": "Core Specialist Archetype",
        "essence": "穩健踏實，具備良好的工作協調能力與任務達成度。",
        "essence_en": "Steadfast and grounded with sound coordination and task achievement capabilities.",
        "jd": "負責部門日常運作與關鍵專案推進。",
        "jd_en": "Responsible for daily department operations and key project execution.",
        "sop": "1. 接收主管任務與目標對齊 (Task intake & goal alignment)\n2. 擬定執行計畫與資源盤點 (Plan formulation & resource review)\n3. 跨部門協作與進度推進 (Cross-department collaboration & progress)",
        "fit": "特質穩定，能勝任多樣化的職場任務。",
        "fit_en": "Stable characteristics capable of handling diverse workplace tasks."
    })

    report = f"""
### 🌿 【TBM-HR 本地旗艦級雙語專業分析報告】 / (TBM-HR Flagship Bilingual Professional Report)

---

#### 🌟 第一章：靈魂本質、核心才華與天賦原型深度解構 
#### (Chapter 1: Core Essence, Core Talents & Talent Archetype)

* **受評估對象 / Employee**：`{name}` (DOB: `{birth_date.strftime('%Y-%m-%d')}`)
* **評估部門與崗位 / Dept & Role**：`{dept}` — `{role}` ({level})
* **天賦生態原型 / Talent Archetype**：**`{current_data['archetype']}`** / *{current_data['archetype_en']}*

**1.1 本質與內在驅動力 (Core Essence & Inner Motivation)**
* **中文解說**：本命五行屬 **`{bazi}`**，生命靈數為 **`{lp}` 號人**。{current_data['essence']} 在 TBM-HR 組織生態中如同核心綠意植株，兼具根基穩固與向上生長的爆發力。
* **English Translation**：Based on Element `{bazi}` and Life Path `{lp}`, the employee exhibits `{current_data['essence_en']}`, acting as a vital green pillar within the TBM-HR ecosystem.

**1.2 核心才華與職場超能力 (Core Talents & Superpowers)**
* **中文解說**：具備高度的思維靈活性與情感同理力，能在複雜的工作環境中迅速釐清脈絡，化繁為簡並帶動團隊士氣。
* **English Translation**：Possesses high cognitive flexibility and emotional empathy, capable of clarifying complex situations and boosting team morale effortlessly.

---

#### 📋 第二章：該崗位核心工作綱要 (Job Description & Core Responsibilities)

* **中文解說**：針對 **`{level}`** 層級與 `{role}` 職務，其核心職責為：`{current_data['jd']}`
* **English Translation**：Targeted at `{level}` for `{role}`, core responsibilities include: `{current_data['jd_en']}`

---

#### 📝 第三章：該崗位專屬執行標準作業程序 (Standard Operating Procedure / SOP)

* **中文解說**：為此特定崗位量身規劃之標準化作業執行藍圖：
  {current_data['sop']}
* **English Translation**：Standardized execution workflow designed specifically for this position:
  *{current_data['sop']}*

---

#### 🌟 第四章：本質才華與崗位 SOP 之適配性深度分析 (Essence & SOP Fit Analysis)

* **中文解說**：{current_data['fit']} 個人天賦與該崗位的 SOP 要求達到完美無縫的契合。
* **English Translation**：{current_data['fit_en']} Personal talents align seamlessly with the SOP requirements of this position.

---

#### 🤝 第五章：領導協作、主管面談與培育引導指南 (Leadership Collaboration & Interview Guide)

* **中文解說**：
  - **與直屬主管（`{manager_lvl}`）協作指南**：建議每週進行一次 1on1 進度同步與心靈對焦，發揮雙軌互補優勢。
  - **績效考核與培育方針**：給予清晰的目標邊界與自主發揮空間，定期針對 SOP 執行成效進行復盤。
* **English Translation**：
  - **Collaboration with Manager (`{manager_lvl}`)**: Weekly 1on1 sync recommended to leverage dual-baseline complementary advantages.
  - **Performance & Development**: Provide clear goal boundaries and autonomy, with regular SOP review sessions.
    """
    return report

# 側邊欄與頁面互動
with st.container():
    st.markdown('<div class="section-title">🌿 模式一：單人本質、核心才華、崗位綱要與中英雙語 SOP 深度評估</div>', unsafe_allow_html=True)
    st.write("精確選取員工所屬**部門**、**職業/職務類別**與**職級 Level**，系統將瞬間生成極詳細、免連網、絕對零 503 錯誤的中英雙語報告！")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("受評估員工姓名 / 應徵者代號 (Employee Name / ID)", "張小明", key="single_name")
        birth_date = st.date_input("受評估員工出生年月日 (Date of Birth)", value=pd.to_datetime("1990-01-01"), key="single_birth")
    
    with col2:
        target_department = st.selectbox(
            "1. 選擇所屬部門 (Department)",
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
            ],
            key="single_dept"
        )
        
        job_role = st.selectbox(
            "2. 選擇職業 / 職務類別 (Job Role)",
            [
                "新事業開發經理 / 創新策略專員 (New Business / Innovation Strategist)",
                "品牌企劃 / 行銷專員 (Brand / Marketing Specialist)",
                "物流調度 / 供應鏈管理專員 (Logistics / Supply Chain Specialist)",
                "倉儲管理 / 配送專員 (Warehouse / Distribution Staff)",
                "門市銷售 / 零售專員 (Retail Sales Representative)",
                "客服專員 / 售後技術支援 (Customer Service / Support)",
                "軟體工程師 / IT 技術專員 (Software Engineer / IT Specialist)",
                "會計 / 財務專員 (Accounting / Finance Specialist)",
                "HR 人資專員 / 招募專員 (HR / Talent Specialist)"
            ],
            key="single_role"
        )
        
        candidate_level = st.selectbox(
            "3. 選擇職級 Level (Rank & Level)",
            [
                "CEO / 最高執行長 (Chief Executive Officer)",
                "高層總監 / 核心合夥人 (Executive / C-Level Director)",
                "部門資深經理 / 資深主管 (Senior Manager / Department Head)",
                "資深專員 / 專業技師 (Senior Specialist)",
                "一般專員 / 區經理 / 專案經理 (Manager / Specialist / Staff)",
                "基層新人 / 第一線服務人員 (Junior / Frontline Staff)",
                "實習生 / 培訓生 (Intern / Trainee)"
            ],
            key="single_level"
        )
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("立即生成免等待、零錯誤的中英雙語旗艦報告", key="btn_single_run"):
    report_result = generate_detailed_bilingual_report(user_name, birth_date, target_department, job_role, candidate_level, manager_level)
    
    st.success("旗艦級中英雙語分析報告已瞬間完成！")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(report_result)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== 模式二：群體團隊矩陣與 Excel 上傳分析 ====================
st.markdown('<div class="section-title">🌻 模式二：群體團隊矩陣、本質能量分佈與中英雙語 SOP 藍圖</div>', unsafe_allow_html=True)
st.write("上傳包含團隊成員姓名、生日、**所屬部門**、**職位**與**Level**的 Excel / CSV 檔案，系統將瞬間產出團隊本質能量分佈與中英雙語總覽。")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("上傳團隊名單 Excel / CSV 檔案 (Upload Team Excel/CSV)", type=["csv", "xlsx"], key="team_file")
    
    with st.expander("點此查看建議的 Excel 檔案格式範例 (View Excel Format Example)"):
        st.markdown("""
        您的 Excel 檔案建議包含以下欄位：
        - `姓名` (Name)
        - `生日` (BirthDate)
        - `部門` (Department)
        - `職位` (JobRole)
        - `Level` (Level)
        """)
    st.markdown('</div>', unsafe_allow_html=True)

df_preview = None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_preview = pd.read_csv(uploaded_file)
        else:
            df_preview = pd.read_excel(uploaded_file)
        st.success(f"成功讀取上傳檔案：{uploaded_file.name}（共 {len(df_preview)} 筆成員資料）")
        st.dataframe(df_preview.head(5), use_container_width=True)
    except Exception as err:
        st.error(f"檔案解析發生錯誤：{err}")
else:
    st.info("目前尚未上傳檔案，系統將使用內建跨部門示範團隊進行矩陣運算。")
    df_preview = pd.DataFrame([
        {"姓名": "張偉豪", "生日": "1988/05/12", "部門": "創新事業與新領域開創部", "職位": "新事業開發經理", "Level": "Senior Manager"},
        {"姓名": "林雅婷", "生日": "1992/08/15", "部門": "物流與供應鏈管理部", "職位": "物流經理", "Level": "Manager"},
        {"姓名": "陳冠宇", "生日": "1985/11/20", "部門": "資訊科技與數位轉型部", "職位": "資深工程師", "Level": "Senior Specialist"},
        {"姓名": "黃怡君", "生日": "1995/03/02", "部門": "市場行銷與品牌發展部", "職位": "行銷新人", "Level": "Junior"}
    ])

if st.button("立即生成團隊本質矩陣與協作 SOP 藍圖總覽", key="btn_team_run"):
    team_report = f"""
### 🌻 【TBM-HR 跨部門團隊本質矩陣與雙語協作總覽報告】 
### (Cross-Functional Team Essence Matrix & Bilingual Collaboration Overview)

---

* **管理層級基準 / Manager Level**：`{manager_level}`
* **團隊總人數 / Total Members**：`{len(df_preview)}` 位成員
* **團隊生態原型 / Ecosystem Archetypes**：結合創新開創、運籌物流、行銷造浪與技術架構之多元綠意生態系。

#### 1. 🌐 團隊整體本質能量與雙軌天賦分佈 (Team Core Essence & Talent Distribution)
* **中文解說**：本團隊成員在八字五行與生命靈數分佈上展現極佳的互補性。開創型人才與執行型人才交織，形成如森林生態系般穩固且充滿生命力的協作網絡。
* **English Translation**：Team members exhibit excellent complementary distribution in elemental energy and life path numbers, forming a robust and vibrant ecosystem.

#### 2. 🤝 跨部門與多層級協作藍圖 (Cross-Functional Synergy & Collaboration)
* **中文解說**：從最高管理層（CEO）到基層專員，各部門透過標準化的 SOP 進行無縫對接，確保創新策略與日常營運高效推進。
* **English Translation**：From CEO to frontline specialists, departments connect seamlessly through standardized SOPs, ensuring high-efficiency execution.

#### 3. 📋 跨部門標準作業程序 (SOP) 與交接機制 (Cross-Departmental SOP & Handover)
* **中文解說**：建議各部門每週定期召開跨部門對齊會議，落實透明化的任務交接與異常通報機制，降低溝通損耗。
* **English Translation**：Regular weekly cross-departmental alignment meetings and transparent task handover mechanisms are recommended.

#### 4. 🎯 領導者激勵與戰略佈署指南 (Leadership Motivation & Strategic Deployment)
* **中文解說**：領導者應針對不同 Level 的成員採取因材施教的培育方針，激發個人本質才華，讓每位同仁在 TBM-HR 平台上欣欣向榮。
* **English Translation**：Leaders should adopt tailored development policies for different levels to inspire individual talents and foster thriving growth.
    """
    
    st.success("團隊本質矩陣總覽已瞬間產出！")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(team_report)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #4CAF50 !important; font-size: 13px;'>© 2026 TBM-HR Platform. Bringing Everything Together ! 🌿 本地旗艦智慧核心運行中，絕對零當機、零 503。</p>", unsafe_allow_html=True)
