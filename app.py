import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
import time
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
    <h1 style="font-size: 1.8rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #a855f7, #3b82f6, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🔯 TBM-HR Dual-Track Intelligence Dashboard (終極完整雙語版)
    </h1>
</div>
""", unsafe_allow_html=True)

# 9 大核心部門清單
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

# 職級順序
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

# 初始化本地智慧資料庫
if "live_local_db" not in st.session_state:
    st.session_state.live_local_db = pd.DataFrame([
        {"項目分類": "部門職能", "名稱": "全系統部門模組", "詳細內容": "9大部門與有序職級聯動正常（含5段式雙語分段與制約數計算）。", "最後更新": datetime.now().strftime("%Y-%m-%d %H:%M")}
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
            "🌟 模式一：AI 驅動之雙向生日與有序職級動態報告",
            "📚 模式二：本地智慧資料庫常態更新"
        ]
    )
    
    st.markdown("---")
    st.info("🔄 **系統提示**：\n已完美內建【逐位相加制約數】、【5段式雙語分段生成】、【自動防 503 重試】與【主管實景考題庫】！")
    
    if app_mode == "🌟 模式一：AI 驅動之雙向生日與有序職級動態報告":
        st.header("🔮 直屬主管/老闆基準設定")
        manager_name = st.text_input("主管/老闆姓名", "王總裁")
        manager_dept = st.selectbox("主管所屬部門", all_departments, key="mgr_dept")
        manager_level = st.selectbox("主管管理層級", ["CEO / Founder", "Senior Director", "Department Manager", "Team Lead"], key="mgr_lvl")
        manager_birthday = st.date_input("主管真實生日 (DOB)", value=pd.to_datetime("1987-10-23"), key="mgr_bday")

# 靈數邏輯：將數字拆開逐位相加至個位數
def reduce_to_single_digit(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(digit) for digit in str(n))
    return n

# 計算逐位拆解的日加月制約數
def calculate_constraint_number(birth_date):
    m = birth_date.month
    d = birth_date.day
    m_reduced = reduce_to_single_digit(m)
    d_reduced = reduce_to_single_digit(d)
    total = m_reduced + d_reduced
    final_constraint = reduce_to_single_digit(total)
    return m_reduced, d_reduced, final_constraint

# 針對單一區塊進行帶有重試機制的 AI 生成函數 (確保雙語)
def generate_chunk_with_retry(prompt, api_key, max_retries=3):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            res_text = response.text.strip()
            if res_text.startswith("```html"):
                res_text = res_text[7:]
            if res_text.endswith("```"):
                res_text = res_text[:-3]
            return res_text.strip()
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                return f"<div style='color: #ef4444; padding: 10px;'>此區塊生成暫時逾時，請重新點擊。({str(e)})</div>"

# 5段式分段組合主函數
def generate_ai_5_parts_report(name, birth_date, dept, role, m_name, m_dept, m_lvl, m_bday, api_key, progress_bar, status_text):
    b_str = birth_date.strftime('%Y-%m-%d')
    mb_str = m_bday.strftime('%Y-%m-%d')
    
    m_red, d_red, constraint_num = calculate_constraint_number(birth_date)
    
    base_context = f"""
    受評估員工：{name} (生日: {b_str}, 月份簡化: {m_red}, 日期簡化: {d_red}, 逐位拆解日加月制約數: {constraint_num}, 部門: {dept}, 職級: {role})
    直屬主管：{m_name} (生日: {mb_str}, 部門: {m_dept}, 層級: {m_lvl})
    要求：必須具備深度、清晰、結構嚴謹的高階顧問級分析，且每一個論述與段落都必須包含專業的中英文雙語對照。回傳乾淨的 HTML 片段。
    """

    # 1. 第一段：核心命理及性格特質畫象（含逐位拆解日加月制約數）
    status_text.text("⏳ [1/5] 正在生成：核心命理及性格特質畫象（含逐位拆解日加月制約數，中英文雙語對照）...")
    progress_bar.progress(20)
    p1 = f"""
    {base_context}
    請撰寫第一部分：「一、 核心命理及性格特質畫象（基於生日 {b_str} 與逐位拆解之日加月制約數 {constraint_num} 之 AI 深度拆解）」。
    內容須詳細解析其生命密碼、天賦優勢、思考邏輯，並特別納入並解構「日加月逐位相加簡化後之制約數 {constraint_num}（月份簡化 {m_red} + 日期簡化 {d_red}）」所賦予的潛在心理制約、行為盲點與突破契機。
    格式要求：使用外框為 #131c2e、上方邊框色 #a855f7 的美觀 HTML div 區塊，內含專業中英文雙語對照。
    """
    html_p1 = generate_chunk_with_retry(p1, api_key)

    # 2. 第二段：崗位適配性與跨部門流動評估
    status_text.text("⏳ [2/5] 正在生成：崗位適配性與跨部門流動評估（中英文雙語對照）...")
    progress_bar.progress(40)
    p2 = f"""
    {base_context}
    請撰寫第二部分：「二、 崗位適配性與跨部門流動評估 (Role Fit & Internal Mobility)」。
    內容須深度評估其在現職「{role}」與「{dept}」的強弱項與勝任度，同時分析其是否具備轉調至其他部門或高階職位的潛在流動選項。
    格式要求：使用外框為 #131c2e、上方邊框色 #3b82f6 的美觀 HTML div 區塊，內含專業中英文雙語對照。
    """
    html_p2 = generate_chunk_with_retry(p2, api_key)

    # 3. 第三段：職場人際協同與處事哲學
    status_text.text("⏳ [3/5] 正在生成：職場人際協同與處事哲學（中英文雙語對照）...")
    progress_bar.progress(60)
    p3 = f"""
    {base_context}
    請撰寫第三部分：「三、 職場人際協同與處事哲學 (Interpersonal Dynamics & Workplace Style)」。
    內容須適用於所有職級（不論新人或高管），深入剖析其日常溝通風格、人際互動模式以及面對職場挑戰時的處事哲學。
    格式要求：使用外框為 #131c2e、上方邊框色 #10b981 的美觀 HTML div 區塊，內含專業中英文雙語對照。
    """
    html_p3 = generate_chunk_with_retry(p3, api_key)

    # 4. 第四段：員工與主管的動態協同法則
    status_text.text("⏳ [4/5] 正在生成：員工與主管的動態協同法則（中英文雙語對照）...")
    progress_bar.progress(80)
    p4 = f"""
    {base_context}
    請撰寫第四部分：「四、 員工 ({name}, {b_str}) 與主管 ({m_name}, {mb_str}) 的動態協同法則 (Dynamic Synergy Law)」。
    內容須詳細剖析雙方生日能量碰撞、磁場互補與黃金共振管理模式。
    格式要求：使用外框為 #131c2e、上方邊框色 #f59e0b 的美觀 HTML div 區塊，內含專業中英文雙語對照。
    """
    html_p4 = generate_chunk_with_retry(p4, api_key)

    # 5. 第五段：主管識人盲點破解與實景情境考題
    status_text.text("⏳ [5/5] 正在生成：主管識人盲點破解與實景情境考題庫（中英文雙語對照）...")
    progress_bar.progress(100)
    p5 = f"""
    {base_context}
    請撰寫第五部分：「五、 主管識人盲點破解與實景情境考題庫 (Blind Spot Analysis & Situational Interview Questions)」。
    內容須針對主管在面試或帶兵時容易產生的「盲點」（例如只聽表面說詞、無法看清其實際解決方案能力），針對該員工 ({name}) 的生日與性格特質，量身設計 2-3 個具體的「實景情境考題」與解決方案評估標準，協助主管精準看出對方是否真正能幫到公司。
    格式要求：使用漸層背景 (rgba(168,85,247,0.15) 到 rgba(59,130,246,0.15)) 的精美 HTML div 區塊，內含專業中英文雙語對照。
    """
    html_p5 = generate_chunk_with_retry(p5, api_key)

    status_text.text("✨ 5段式雙語智能報告組裝完成！")

    # 組合完整 HTML 報告
    full_html_report = f"""
    <div style="color: #e2e8f0; line-height: 1.8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 15px;">
        
        <script>
        function speakText(text) {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                let utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'zh-CN';
                window.speechSynthesis.speak(utterance);
            }}
        }}
        function stopReport() {{
            if ('speechSynthesis' in window) {{ window.speechSynthesis.cancel(); }}
        }}
        </script>

        <!-- 🔊 頂部總結配音控制列 -->
        <div style="background: linear-gradient(135deg, #1e1b4b, #312e81); padding: 15px 20px; border-radius: 10px; border: 1px solid #4338ca; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #818cf8; font-size: 1.0rem;">🔊 5段式雙語 Gemini AI 智慧動態報告語音控制台</h4>
                <p style="margin: 3px 0 0 0; font-size: 0.85rem; color: #c7d2fe;">當前分析對象：<strong>{name} ({b_str}，制約數: {constraint_num})</strong> 搭配主管 <strong>{m_name} ({mb_str})</strong></p>
            </div>
            <div>
                <button onclick="speakText('這是為 {name} 量身打造的 AI 雙向生日雙語動態戰略報告與制約數分析。')" style="background: #4f46e5; color: #ffffff; border: none; padding: 10px 16px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 0.9rem; margin-right: 8px;">▶ 播放摘要</button>
                <button onclick="stopReport()" style="background: #334155; color: #94a3b8; border: none; padding: 10px 15px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 0.9rem;">⏹ 停止</button>
            </div>
        </div>

        <!-- 📊 雙方生日基準與對照矩陣 -->
        <div style="background: #131c2e; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 30px; border-left: 4px solid #3b82f6;">
            <h3 style="color: #3b82f6; margin: 0 0 15px 0; font-size: 1.2rem;">📊 AI 真實雙語生日基準與制約數矩陣 (Bilingual Birthday & Constraint Number Matrix)</h3>
            <table style="width: 100%; border-collapse: collapse; background: #0b0f19; border-radius: 8px; overflow: hidden; font-size: 0.9rem;">
                <tr style="border-bottom: 1px solid #1e293b;">
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">對照維度 / Dimension</th>
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">員工 ({name}) 基準</th>
                    <th style="padding: 12px; text-align: left; color: #e2e8f0;">主管 ({m_name}) 基準</th>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">生日、職級與逐位拆解制約數</td>
                    <td style="padding: 12px; color: #f59e0b; font-weight: bold;">{b_str} ({role})<br><span style="font-size:0.85rem; color:#38bdf8;">日加月制約數：({birth_date.month}拆解->{m_red}) + ({birth_date.day}拆解->{d_red}) = <strong>{constraint_num}</strong></span></td>
                    <td style="padding: 12px; color: #f59e0b; font-weight: bold;">{mb_str} ({m_lvl})</td>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 12px; color: #a855f7; font-weight: bold;">AI 雙語智慧解構 / Bilingual Analysis</td>
                    <td style="padding: 12px;">結合 {b_str} 與制約數 {constraint_num} 之核心天賦與盲點解析。<br><span style="font-size:0.8rem; color:#94a3b8;">[Translation] Core talent and constraint analysis for {name}.</span></td>
                    <td style="padding: 12px;">精確對應 {mb_str} 主管領導風格與決策基因。<br><span style="font-size:0.8rem; color:#94a3b8;">[Translation] Leadership and decision-making profile for {m_name}.</span></td>
                </tr>
            </table>
        </div>

        <!-- 5 大獨立生成區塊依序嵌載 -->
        <div style="margin-bottom: 30px;">{html_p1}</div>
        <div style="margin-bottom: 30px;">{html_p2}</div>
        <div style="margin-bottom: 30px;">{html_p3}</div>
        <div style="margin-bottom: 30px;">{html_p4}</div>
        <div style="margin-bottom: 30px;">{html_p5}</div>

    </div>
    """
    return full_html_report

# ==================== 介面操作模式 ====================
if app_mode == "🌟 模式一：AI 驅動之雙向生日與有序職級動態報告":
    with st.container():
        st.markdown("### 🌿 模式一：Gemini AI 雙語分段動態分析引擎（含制約數與實景考題）")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 👤 受評估員工基本設定")
            user_name = st.text_input("員工姓名 / 代號", "張經理")
            birth_date = st.date_input("員工真實生日日期 (DOB)", value=pd.to_datetime("1985-06-20"))
        with col2:
            st.markdown("#### 🎯 部門與有序職級選項")
            target_department = st.selectbox("選擇員工所屬部門", all_departments)
            job_role = st.selectbox("選擇職務名稱與層級 (Job Role & Level)", ordered_job_roles, index=7)

    if st.button("🚀 啟動 5段式雙語智能分段運算與匹配報告"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 執行 5 段式分段生成
        report_output = generate_ai_5_parts_report(
            user_name, birth_date, target_department, job_role,
            manager_name, manager_dept, manager_level, manager_birthday,
            BUILTIN_API_KEY, progress_bar, status_text
        )
        
        st.success(f"成功為「{user_name}」與主管「{manager_name}」生成 5段式雙語專屬 AI 動態匹配報告！")
        components.html(report_output, height=4200, scrolling=True)

else:
    # 模式二：本地智慧資料庫
    st.markdown("### 📚 模式二：常態更新的本地智慧資料庫維護")
    st.dataframe(st.session_state.live_local_db, use_container_width=True)
    
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
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>© 2026 TBM-HR Platform. AI-Powered Bilingual Dynamic Birthday Intelligence 🔯</p>", unsafe_allow_html=True)
