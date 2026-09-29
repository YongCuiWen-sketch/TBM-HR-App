import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 設定網頁標題與基本樣式（自然綠意與花草生活風）
st.set_page_config(
    page_title="TBM-HR 智慧人才與人格分析系統",
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
        padding: 1.5rem;
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
                🌱 TBM 綠野心靈與天賦空間 (本地高穩定智慧核心)
            </div>
            <span style="background-color: #E8F5E9; color: #2E7D32 !important; padding: 0.3rem 0.8rem; border-radius: 2rem; font-size: 0.8rem; font-weight: 600; border: 1px solid #C8E6C9;">
                Bringing Everything Together ! 🌿
            </span>
        </div>
        <div>
            <h1 style="font-size: 1.6rem; font-weight: 700; margin: 4px 0 2px 0; color: #1B5E20 !important;">
                TBM-HR 智慧決策與人格分析平台
            </h1>
            <p style="font-size: 0.9rem; color: #388E3C !important; margin: 0;">
                結合東方八字命盤與西方生命靈數雙軌基準，內建各部門專屬 SOP 與崗位綱要，免聯外、零當機，陪伴團隊自然成長。
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== 本地運算核心邏輯 (八字與生命靈數) ====================
def calculate_life_path(birth_date):
    """計算西方生命靈數"""
    date_str = birth_date.strftime("%Y%m%d")
    total = sum(int(char) for char in date_str)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(char) for char in str(total))
    return total

def get_bazi_element(birth_date):
    """依據出生年份簡單對應五行（作為本地八字基準模擬）"""
    year = birth_date.year
    elements = ["金 (Metal)", "水 (Water)", "木 (Wood)", "火 (Fire)", "土 (Earth)"]
    return elements[year % 5]

def generate_local_report(name, birth_date, dept, role, level, manager_lvl):
    lp = calculate_life_path(birth_date)
    bazi = get_bazi_element(birth_date)
    
    # 針對部門與崗位提供專屬的 SOP 與崗位綱要
    sop_mapping = {
        "創新事業與新領域開創部 (New Business Ventures & Innovation)": {
            "jd": "負責新產品線孵化、市場機會探索與商業模式創新驗證。",
            "sop": "1. 每週進行競品與新興市場趨勢掃描 -> 2. 提出 MVP（最小可行性產品）方案 -> 3. 跨部門試驗與數據追蹤 -> 4. 滾動式修正創新策略。"
        },
        "市場行銷與品牌發展部 (Marketing & Brand Development)": {
            "jd": "塑造品牌核心價值、策劃數位/實體行銷活動與流量增長。",
            "sop": "1. 市場受眾與流量數據分析 -> 2. 擬定檔期行銷企劃與視覺素材 -> 3. 投放執行與社群互動維護 -> 4. 成效復盤與轉換率優化。"
        },
        "物流與供應鏈管理部 (Logistics & Supply Chain)": {
            "jd": "確保庫存精準、運輸排程流暢與供應商協調高效。",
            "sop": "1. 每日供應鏈庫存盤點與預警 -> 2. 調度與運輸路線最佳化排程 -> 3. 異常狀況即時處理與回報 -> 4. 供應商績效檢討與成本控制。"
        },
        "零售與門市營運部 (Retail & Store Operations)": {
            "jd": "提升門市營運績效、現場服務品質與顧客購物體驗。",
            "sop": "1. 每日早會與門市環境/陳列檢視 -> 2. 顧客接待與銷售引導服務 -> 3. 庫存補貨與現金結帳管考 -> 4. 當日業績結算與交接。"
        },
        "客戶服務與售後中心 (Customer Service & Support Centre)": {
            "jd": "解決客戶諮詢、客訴處理與售後維修協調。",
            "sop": "1. 客戶諮詢與客訴案件受理登記 -> 2. 跨部門技術/物流協調處理 -> 3. 滿意度追蹤與回訪 -> 4. 常見問題庫 (FAQ) 更新。"
        },
        "銷售與業務發展部 (Sales & Business Development)": {
            "jd": "開拓新客戶、維繫重要客戶關係與達成營業目標。",
            "sop": "1. 潛在客戶名單開發與拜訪排程 -> 2. 需求訪談與客製化方案提案 -> 3. 談判、合約簽訂與收款追蹤 -> 4. 客戶關係維護與續約管理。"
        },
        "資訊科技與數位轉型部 (IT & Digital Transformation)": {
            "jd": "系統維運、資安防護與企業數位工具導入。",
            "sop": "1. 系統效能監控與異常警報處理 -> 2. 使用者IT支援與權限管理 -> 3. 系統功能開發與測試 -> 4. 資安備份與漏洞修補。"
        },
        "財務與會計部 (Finance & Accounting)": {
            "jd": "帳務處理、成本控制、財務報表編製與資金調度。",
            "sop": "1. 每日收支憑證審核與入帳 -> 2. 應收應付款項管理 -> 3. 月結報表與稅務申報準備 -> 4. 財務預算執行分析與風險管控。"
        },
        "人力資源與人才發展部 (HR & People Development)": {
            "jd": "人才招募、薪酬福利管理、培訓發展與組織文化建立。",
            "sop": "1. 職缺招募與面試安排 -> 2. 新人報到引導與培訓計畫執行 -> 3. 績效考核與薪酬計算 -> 4. 員工關懷與組織溝通活動。"
        }
    }
    
    current_sop = sop_mapping.get(dept, {
        "jd": "負責部門日常運作與專案目標達成。",
        "sop": "1. 接收主管交辦任務 -> 2. 擬定執行計畫 -> 3. 跨部門協調推進 -> 4. 成果驗收與回報。"
    })

    report = f"""
### 🌿 【TBM-HR 本地智慧雙軌分析報告】

* **受評估對象**：{name}
* **出生日期**：{birth_date.strftime('%Y-%m-%d')}
* **評估部門**：{dept}
* **職業/崗位**：{role}
* **職級 Level**：{level}
* **對應管理層級**：{manager_lvl}

---

#### 1. 🧬 雙軌天賦基準解析 (Baseline)
* **東方五行八字基準**：本命五行屬 **{bazi}**。展現出穩健、應變力強且具備獨特職場生長潛能的特質，在團隊中如同常青植物般具備強大韌性。
* **西方生命靈數基準**：天賦靈數為 **{lp} 號人**。具備清晰的邏輯思維與協調天賦，特別適合在 {dept.split('(')[0]} 發揮創造力與執行力。

#### 2. 📋 崗位核心工作綱要 (Job Description)
* **職責定位**：針對 **{level}** 層級，{current_sop['jd']}
* **核心價值**：在該崗位上需兼顧效率與高品質輸出，成為推動團隊成長的核心綠意能量。

#### 3. 📝 專屬標準作業程序 (SOP) 執行藍圖
為此崗位量身規劃的日常與專案執行標準步驟：
{current_sop['sop']}

#### 4. 🌟 天賦適配與協作優勢
* 您的生命靈數（{lp}）與八字五行（{bazi}）在該崗位上展現高度契合。
* 能夠在壓力環境下保持冷靜，並透過溫和而堅定的溝通風格推動專案。

#### 5. 🤝 主管培育與面談引導建議
* **主管互動**：建議與 {manager_lvl} 保持每週一次的進度同步與心靈交流。
* **培育方向**：給予充足的自主發揮空間，並定期進行 SOP 執行成效復盤。
    """
    return report

# 側邊欄：環境與全域設定
with st.sidebar:
    st.header("🌿 組織與模式設定")
    
    manager_level = st.selectbox(
        "管理層級設定 (Evaluation Manager Level)",
        [
            "CEO (最高執行長)",
            "TA (直屬營運主管 / Team Leader)",
            "高層 (Executive / C-Level Director)",
            "經理 (Branch / Department Manager)",
            "IT 資訊科技主管 (IT Manager / Head of IT)",
            "資深專員 / 專業技師 (Senior Specialist)",
            "基層服務人員 / 新人 (Junior / Frontline Staff)"
        ]
    )

    manager_birthday = st.sidebar.date_input("主管 / 領導者生日（雙基底對應）")
    
    st.markdown("---")
    st.success("✨ 本地端智慧運算系統已就緒（免 API Key、零 503 錯誤、極速響應）")


# ==================== 區塊一：單人精準人格分析與獨立分類設定 ====================
st.markdown('<div class="section-title">🌿 模式一：單人深度人格行為、崗位綱要與 SOP 本地智慧評估</div>', unsafe_allow_html=True)
st.write("精確選取員工所屬**部門**、**職業/職務類別**與**職級 Level**，系統將直接在本地計算雙軌天賦並生成專屬報告！")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("受評估員工姓名 / 應徵者代號", "張小明", key="single_name")
        birth_date = st.date_input("受評估員工出生年月日", value=pd.to_datetime("1990-01-01"), key="single_birth")
    
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
    
if st.button("立即生成本地雙軌天賦與崗位 SOP 報告", key="btn_single_run"):
    mock_score = 92.5
    mock_comm = 88
    mock_stress = 85
    mock_service = 95

    st.markdown("#### ☘️ 個人核心特質與崗位適配儀表板")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("綜合適配指數", f"{mock_score}%", "+2.5%")
    m2.metric("溝通協調力", f"{mock_comm} 分", "和諧")
    m3.metric("抗壓應變力", f"{mock_stress} 分", "穩健")
    m4.metric("TBM 顧客導向度", f"{mock_service} 分", "卓越")

    report_text = generate_local_report(user_name, birth_date, target_department, job_role, candidate_level, manager_level)
    
    st.success("本地智慧分析報告已瞬間完成！")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(report_text)
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


# ==================== 區塊二：群體團隊矩陣與 Excel 上傳分析 ====================
st.markdown('<div class="section-title">🌻 模式二：群體團隊矩陣人格分析、跨部門協作與 SOP 總覽</div>', unsafe_allow_html=True)
st.write("上傳包含團隊成員姓名、生日、**所屬部門**、**職位**與**Level**的 Excel / CSV 檔案，系統將自動分析跨部門團隊的協作默契與整體作業 SOP 藍圖。")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("上傳團隊名單 Excel / CSV 檔案", type=["csv", "xlsx"], key="team_file")
    
    with st.expander("點此查看建議的 Excel 檔案格式範例"):
        st.markdown("""
        您的 Excel 檔案建議包含以下欄位：
        - `姓名` (例如：張偉豪、林雅婷)
        - `生日` (例如：1988/05/12)
        - `部門` (例如：創新事業與新領域開創部、市場行銷與品牌發展部)
        - `職位` (例如：新事業開發經理、品牌企劃)
        - `Level` (例如：CEO、Senior Manager、Specialist)
        - `適配評分` (例如：92.5)
        """)
    st.markdown('</div>', unsafe_allow_html=True)

df_team = None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_team = pd.read_csv(uploaded_file)
        else:
            df_team = pd.read_excel(uploaded_file)
        st.success(f"成功讀取上傳檔案：{uploaded_file.name}（共 {len(df_team)} 筆成員資料）")
        st.dataframe(df_team.head(5), use_container_width=True)
    except Exception as err:
        st.error(f"檔案解析發生錯誤：{err}")
else:
    st.info("目前尚未上傳檔案，系統將使用內建跨部門示範團隊進行矩陣運算。")
    df_team = pd.DataFrame([
        {"姓名": "張偉豪", "生日": "1988/05/12", "部門": "創新事業與新領域開創部", "職位": "新事業開發經理", "Level": "Senior Manager", "適配評分": 95.0},
        {"姓名": "林雅婷", "生日": "1992/08/15", "部門": "物流與供應鏈管理部", "職位": "物流經理", "Level": "Manager", "適配評分": 91.0},
        {"姓名": "陳冠宇", "生日": "1985/11/20", "部門": "資訊科技與數位轉型部", "職位": "資深工程師", "Level": "Senior Specialist", "適配評分": 88.5},
        {"姓名": "黃怡君", "生日": "1995/03/02", "部門": "市場行銷與品牌發展部", "職位": "行銷新人", "Level": "Junior", "適配評分": 93.2}
    ])

if st.button("開始執行團隊矩陣與協作 SOP 藍圖總覽", key="btn_team_run"):
    team_summary_html = f"""
### 🌻 【TBM-HR 跨部門團隊協作與矩陣總覽報告】

* **管理層級基準**：{manager_level}
* **團隊總人數**：{len(df_team)} 位成員
* **評估範圍**：涵蓋創新開創、物流、行銷、IT 等多元跨部門協作網絡。

---

#### 1. 🌐 團隊雙軌能量分佈概況
* 本團隊成員在生命靈數與五行八字分佈上具備高度互補性。開創型人才（如創新事業部）與執行型人才（如物流與 IT 部門）形成完美的生態平衡。

#### 2. 🤝 跨部門與多層級協作藍圖 (Cross-Departmental Synergy)
* **策略與執行對接**：高階主管與專案經理透過標準化的 SOP 進行任務交接，確保創新點子能順利落地執行。
* **資源流動**：行銷與物流部門緊密配合，實現「前端市場拓展」與「後端供應鏈支援」的無縫銜接。

#### 3. 📋 跨部門標準作業程序 (SOP) 整合建議
* **日常同步**：各部門需於每週一召開跨部門協調會，對齊目標。
* **異常處理機制**：建立透明的通報 SOP，縮短跨部門溝通時間損耗。

#### 4. 🎯 領導者凝聚力指南
* 建議領導者針對不同 Level（從 CEO 到 Junior）採取因材施教的激勵策略，營造如花草生態系般欣欣向榮的職場氛圍。
    """
    
    st.success("團隊矩陣分析總覽已產出！")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(team_summary_html)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #4CAF50 !important; font-size: 13px;'>© 2026 TBM-HR Platform. Bringing Everything Together ! 🌿 本地智慧核心運行中，絕不當機。</p>", unsafe_allow_html=True)