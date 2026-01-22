import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium
import os
import base64

# Page Configuration
st.set_page_config(page_title="NEW TERRA", layout="wide", initial_sidebar_state="collapsed")

# Helper to get base64 for background
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'
if 'theme' not in st.session_state:
    st.session_state['theme'] = '기본'

# Theme CSS definitions (GPT-5.2 Styled)
THEME_CSS = {
    '기본': "",
    '자연': """
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f1f8e9 0%, #a5d6a7 100%) !important;
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
        .stButton>button {
            background: rgba(76, 175, 80, 0.9) !important;
            color: white !important;
            border-radius: 20px !important;
            backdrop-filter: blur(5px);
        }
        h1, h2, h3 { 
            color: #2e7d32 !important; 
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
        }
        .vision-card { 
            background: rgba(255, 255, 255, 0.7) !important; 
            border-left: 8px solid #2e7d32 !important;
            backdrop-filter: blur(10px);
        }
        .hero-section { background: rgba(255,255,255,0.3) !important; border-radius: 30px; }
        </style>
    """,
    '하늘': """
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #e3f2fd 0%, #90caf9 100%) !important;
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
        .stButton>button {
            background: rgba(33, 150, 243, 0.8) !important;
            color: white !important;
            border-radius: 20px !important;
            backdrop-filter: blur(5px);
        }
        h1, h2, h3 { 
            color: #1565c0 !important; 
            text-shadow: 1px 1px 4px rgba(255,255,255,0.9);
        }
        .vision-card { 
            background: rgba(255, 255, 255, 0.7) !important; 
            border-left: 8px solid #2196f3 !important;
            backdrop-filter: blur(10px);
        }
        </style>
    """,
    '미세먼지': """
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #eceff1 0%, #cfd8dc 100%) !important;
            filter: grayscale(0.3) contrast(1.1);
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
        .stButton>button {
            background: rgba(120, 144, 156, 0.9) !important;
            color: white !important;
            border-radius: 5px !important;
        }
        h1, h2, h3 { 
            color: #37474f !important; 
        }
        .vision-card { 
            background: rgba(207, 216, 220, 0.8) !important; 
            border-left: 8px solid #546e7a !important;
        }
        .hero-section { filter: blur(0.5px); }
        </style>
    """
}

# Apply Theme CSS
st.markdown(THEME_CSS.get(st.session_state['theme'], ""), unsafe_allow_html=True)

# Custom CSS for modern design
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Noto+Sans+KR', sans-serif;
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    .main {{
        background-color: transparent;
    }}

    /* Remove all top margins and padding - More aggressive */
    [data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {{
        padding-top: 0 !important;
        margin-top: -100px !important; /* Force pull up if needed */
    }}

    .stAppViewBlockContainer, .block-container {{
        padding-top: 0 !important;
        margin-top: -50px !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}

    /* Target the very first element inside the main container */
    [data-testid="stVerticalBlock"] > div:first-child {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}

    header[data-testid="stHeader"], [data-testid="stDecoration"] {{
        display: none !important;
        height: 0 !important;
    }}

    /* Remove whitespace from top elements */
    #tabs-b-title {{
        display: none !important;
    }}

    /* Navigation Header */
    .header-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.95);
        padding: 10px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 1000;
        border-bottom: 1px solid #eee;
        backdrop-filter: blur(10px);
    }}
    
    .logo-box {{
        display: flex;
        align-items: center;
        cursor: pointer;
        gap: 10px;
    }}
    
    .logo-text {{
        font-size: 22px;
        font-weight: 700;
        color: #2E7D32;
        letter-spacing: -1px;
    }}
    
    /* Section containers */
    .section-box {{
        padding: 60px 0;
        margin-top: 20px;
    }}
    
    .hero-section {{
        text-align: center;
        padding: 20px 20px;
        background: transparent;
        margin-bottom: 0px;
    }}
    
    .vision-card {{
        background-color: #f9f9f9;
        padding: 40px;
        border-radius: 20px;
        border-left: 5px solid #2E7D32;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin: 20px 0;
    }}
    
    /* Vertical alignment for header */
    [data-testid="stHorizontalBlock"] {{
        align-items: center;
    }}

    /* Table-like Navigation UI - Borders Removed */
    #nav-anchor-home + div [data-testid="stHorizontalBlock"],
    #nav-anchor-other + div [data-testid="stHorizontalBlock"] {{
        background-color: transparent !important;
        padding: 0 !important;
        gap: 0 !important; /* Removed gap (grid lines) */
        border: none !important; /* Removed outer border */
        border-radius: 0;
        overflow: hidden;
        margin: -40px -10% 10px -10% !important;
        display: flex !important;
        align-items: stretch !important;
        box-shadow: none !important; /* Removed shadow for a cleaner look if borders are gone */
    }}

    /* Table Cell Style for Columns */
    #nav-anchor-home + div [data-testid="column"],
    #nav-anchor-other + div [data-testid="column"] {{
        background-color: #DCEDC8; /* Default cell color */
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: stretch !important;
        justify-content: center !important;
    }}

    /* Logo Cell specific */
    #nav-anchor-home + div [data-testid="column"]:first-child,
    #nav-anchor-other + div [data-testid="column"]:first-child {{
        background-color: white !important;
        min-width: 450px;
    }}

    /* Button Cell specific */
    #nav-anchor-home + div .stButton,
    #nav-anchor-other + div .stButton {{
        width: 100% !important;
        height: 100% !important;
    }}

    #nav-anchor-home + div .stButton>button,
    #nav-anchor-other + div .stButton>button {{
        border-radius: 0 !important;
        border: none !important;
        margin: 0 !important;
        width: 100% !important;
        height: 100% !important;
        min-height: 135px !important; /* 1.5배 크기 확대 */
        font-size: 39px !important; /* 1.5배 글씨 크기 확대 */
        font-weight: 800 !important;
        background-color: #DCEDC8 !important;
        color: black !important;
        transition: background-color 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    #nav-anchor-home + div .stButton>button:hover,
    #nav-anchor-other + div .stButton>button:hover {{
        background-color: #C5E1A5 !important;
        transform: none !important;
    }}
    
    .stButton>button:hover {{
        background-color: #C5E1A5;
        color: black !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    
    /* Hide Streamlit elements */
    #MainMenu {{display: none !important;}}
    header {{display: none !important;}}
    footer {{display: none !important;}}
    
    /* Scroll Spacer */
    .spacer {{ height: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# Helper to find files
def get_file_path(extension):
    for f in os.listdir('.'):
        if f.endswith(extension):
            return f
    return None

LOGO_FILE = "로고로고로고고고고고고고로롤고고고.png"
EXCEL_FILE = get_file_path('.xlsx')
PDF_FILE = get_file_path('.pdf')

# Data Loading
@st.cache_data
def load_data():
    if EXCEL_FILE:
        try:
            df = pd.read_excel(EXCEL_FILE)
            df.columns = ['Region', 'Year', 'MonthDate', 'Pb', 'Cd', 'As']
            df['Month'] = df['MonthDate'].apply(lambda x: int(str(x).split('.')[1]) if '.' in str(x) else 1)
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()

df = load_data()

# Region mapping
REGION_COORDS = {
    '서울': [37.5665, 126.9780], '부산': [35.1796, 129.0756], '대구': [35.8714, 128.6014],
    '인천': [37.4563, 126.7052], '광주': [35.1595, 126.8526], '대전': [36.3504, 127.3845],
    '울산': [35.5384, 129.3114], '세종': [36.4801, 127.2890], '경기': [37.4138, 127.5183],
    '강원': [37.8228, 128.1555], '충북': [36.6357, 127.4913], '충남': [36.6588, 126.6728],
    '전북': [35.8205, 127.1087], '전남': [34.8679, 126.9910], '경북': [36.5760, 128.5058],
    '경남': [35.2377, 128.6924], '제주': [33.4890, 126.4983]
}

def map_region(name):
    name = str(name)
    for k in REGION_COORDS.keys():
        if k in name:
            return k
    return None

if not df.empty:
    df['Mapped_Region'] = df['Region'].apply(map_region)

def create_pie_svg(pb, cd, as_val, size=50):
    total = pb + cd + as_val
    if total == 0:
        return ""
    p1 = (pb / total) * 100
    p2 = (cd / total) * 100
    p3 = (as_val / total) * 100
    svg = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 42 42" style="filter: drop-shadow(0 0 2px rgba(0,0,0,0.5));">
      <circle cx="21" cy="21" r="15.9" fill="transparent" stroke="#448AFF" stroke-width="10" stroke-dasharray="{p3} {100-p3}" stroke-dashoffset="0"></circle>
      <circle cx="21" cy="21" r="15.9" fill="transparent" stroke="#FFD740" stroke-width="10" stroke-dasharray="{p2} {100-p2}" stroke-dashoffset="{-p3}"></circle>
      <circle cx="21" cy="21" r="15.9" fill="transparent" stroke="#FF5252" stroke-width="10" stroke-dasharray="{p1} {100-p1}" stroke-dashoffset="{-p3-p2}"></circle>
      <circle cx="21" cy="21" r="10" fill="white" fill-opacity="0.8"></circle>
    </svg>
    """
    return svg

# --- NAVIGATION HEADER ---
if st.session_state['page'] == 'Home':
    st.markdown('<div id="nav-anchor-home"></div>', unsafe_allow_html=True)
else:
    st.markdown('<div id="nav-anchor-other"></div>', unsafe_allow_html=True)

header_cols = st.columns([2, 1, 1, 1, 1])

with header_cols[0]:
    logo_base64 = get_image_base64(LOGO_FILE)
    if logo_base64:
        st.markdown(f'''
            <div style="display: flex; align-items: center; height: 100%; justify-content: flex-start;">
                <a href="/" target="_self">
                    <img src="data:image/png;base64,{logo_base64}" width="1500" style="max-width: 100%;">
                </a>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='color: #2E7D32; margin: 0;'>NEW TERRA</h1>", unsafe_allow_html=True)

if header_cols[1].button("데이터 분석"): st.session_state['page'] = 'Analysis'
if header_cols[2].button("중금속 정보"): st.session_state['page'] = 'Info'
if header_cols[3].button("출처/팀"): st.session_state['page'] = 'Etc'
if header_cols[4].button("Q&A"): st.session_state['page'] = 'QnA'

# --- THEME SELECTION (Moved below Menu) ---
t_col1, t_col2 = st.columns([8, 2])
with t_col2:
    selected_theme = st.selectbox(
        "🎨 테마 선택",
        options=["기본", "자연", "하늘", "미세먼지"],
        index=["기본", "자연", "하늘", "미세먼지"].index(st.session_state['theme']),
        label_visibility="collapsed"
    )
    if selected_theme != st.session_state['theme']:
        st.session_state['theme'] = selected_theme
        st.rerun()

# --- PAGE ROUTING ---

if st.session_state['page'] == 'Home':
    # --- SECTION 1: MAIN (Image 1) ---
    st.markdown("<div class='hero-section'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #1B5E20; margin-bottom: 0px;'>대한민국 중금속 오염 현황 (2024)</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if not df.empty:
        # Filter for 2024 as requested
        df_24 = df[df['Year'] == 2024]
        # Adjusted location to center South Korea better [36.3, 127.8]
        m = folium.Map(location=[36.3, 127.8], zoom_start=7, tiles='cartodbpositron')
        
        for region, coords in REGION_COORDS.items():
            reg_data = df_24[df_24['Mapped_Region'] == region]
            if not reg_data.empty:
                avg_pb = reg_data['Pb'].mean()
                avg_cd = reg_data['Cd'].mean()
                avg_as = reg_data['As'].mean()
                
                # Create SVG Pie Chart as Marker Icon
                pie_svg = create_pie_svg(avg_pb, avg_cd, avg_as)
                
                popup_html = f"""
                    <div style="width:160px; font-family: sans-serif; text-align:center;">
                        <h4 style="margin-bottom:5px;">{region}</h4>
                        <div style="font-size: 11px;">
                            <span style="color:#FF5252">● 납(Pb): {avg_pb:.4f}</span><br>
                            <span style="color:#FFD740">● 카드뮴(Cd): {avg_cd:.4f}</span><br>
                            <span style="color:#448AFF">● 비소(As): {avg_as:.4f}</span>
                        </div>
                    </div>
                """
                
                folium.Marker(
                    location=coords,
                    icon=folium.DivIcon(
                        html=f'<div style="width:50px; height:50px; margin-left:-25px; margin-top:-25px;">{pie_svg}</div>'
                    ),
                    popup=folium.Popup(popup_html, max_width=200)
                ).add_to(m)
        
        # Center the map container on the homepage
        col_m1, col_m2, col_m3 = st.columns([1, 8, 1])
        with col_m2:
            folium_static(m, width=1000)
    
    # --- SECTION 2: VISION (Image 2) - CONNECTED TO SECTION 1 ---
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #1B5E20;'>Our Vision & Goal</h2>", unsafe_allow_html=True)
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown(f"""
        <div class='vision-card'>
            <h4 style='color: #2E7D32;'>목표</h4>
            <p style='font-size: 1.1em; font-weight: bold;'>
            "데이터 기반 시각화로 시민의 환경 이해를 돕고 안전한 생활 환경 조성을 실현하는 것"
            </p>
            <p>지역별 중금속 수치를 비교 가능한 형태로 가공하여 환경 문제에 대한 인식을 높입니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_v2:
        st.markdown(f"""
        <div class='vision-card'>
            <h4 style='color: #2E7D32;'>비전</h4>
            <p style='font-size: 1.1em; font-weight: bold;'>
            "데이터로 투명하게 그리는 깨끗한 토양, 새로운 땅 <b>NEW TERRA</b>"
            </p>
            <p>우리는 혁신적인 데이터 분석을 통해 더 나은 미래의 환경 가치를 창출합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align: right; color: gray; font-size: 0.8em; padding: 20px;'>연혁: 2026년 1월 22일</div>", unsafe_allow_html=True)

elif st.session_state['page'] == 'Analysis':
    # --- SECTION 3: ANALYSIS (Image 3) ---
    st.title("중금속 데이터 분석 센터")
    
    col_filter, col_chart = st.columns([1, 3])
    
    with col_filter:
        st.subheader("데이터 필터")
        years = sorted(df['Year'].unique().tolist(), reverse=True)
        selected_year = st.selectbox("연도 선택", ["전체 연도"] + years)
        places = sorted(df['Region'].unique().tolist())
        selected_place = st.selectbox("지역 선택", places)
        
        hm_options = st.multiselect("분석 항목", ["Pb", "Cd", "As"], default=["Pb", "Cd", "As"])
        
    with col_chart:
        if not df.empty and hm_options:
            filtered_df = df[df['Region'] == selected_place]
            if selected_year == "전체 연도":
                plot_df = filtered_df.groupby('Year')[hm_options].mean().reset_index()
                fig = px.line(plot_df, x='Year', y=hm_options, markers=True, 
                              title=f"{selected_place} 연도별 중금속 농도 추이",
                              color_discrete_sequence=['#FF5252', '#FFD740', '#448AFF'])
            else:
                plot_df = filtered_df[filtered_df['Year'] == selected_year].sort_values('Month')
                fig = px.line(plot_df, x='Month', y=hm_options, markers=True,
                              title=f"{selected_place} {selected_year}년 월별 중금속 농도 추이",
                              color_discrete_sequence=['#FF5252', '#FFD740', '#448AFF'])
                fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)
            
            fig.update_layout(hovermode="x unified", plot_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
            
            if st.button("AI 데이터 경향성 분석"):
                st.info("데이터 분석 중...")
                analysis_res = ""
                for hm in hm_options:
                    avg_val = plot_df[hm].mean()
                    status = "안정" if avg_val < 0.01 else "주의 필요"
                    analysis_res += f"- **{hm}**: 평균 수치 {avg_val:.4f}로 현재 **{status}** 상태입니다.\n"
                st.markdown(f"**AI 분석 리포트:**\n{analysis_res}\n\n**대안:** 지속적인 모니터링을 통해 특정 시점의 농도 상승을 예방해야 합니다.")

elif st.session_state['page'] == 'Info':
    # --- SECTION 4: INFO (Image 4) ---
    st.title("중금속 상세 가이드 (GPT-5.2 분석)")
    st.markdown("---")
    
    info_cols = st.columns(3)
    metals = {
        "납 (Pb)": {
            "기본정보": "배터리, 페인트, 노후 수도관 등 산업 전반에 널리 사용되는 청회색 금속입니다.",
            "관련 질병": "중추신경계 장애, 어린이의 지능 발달 저하 및 학습 장애, 고혈압을 유발할 수 있습니다.",
            "생활 속 안전 수치": "국내 토양 오염 우려 기준(1지역): 200mg/kg 이하 / 음용수 기준: 0.01mg/L 이하",
            "bg": "#FFEBEE"
        },
        "카드뮴 (Cd)": {
            "기본정보": "산업 공정의 부산물, 도금, 충전용 배터리 등에서 주로 발생하는 독성이 강한 금속입니다.",
            "관련 질병": "유명한 '이타이이타이병'의 원인으로, 신장 기능 장애와 뼈가 약해지는 골연화증을 초래합니다.",
            "생활 속 안전 수치": "국내 토양 오염 우려 기준(1지역): 4mg/kg 이하 / 음용수 기준: 0.005mg/L 이하",
            "bg": "#FFF8E1"
        },
        "비소 (As)": {
            "기본정보": "농약, 반도체 제조, 금속 제련 과정에서 방출되는 천연 및 산업적 오염 물질입니다.",
            "관련 질병": "만성 중독 시 색소 침착 등 피부 질환, 간·폐 등 장기 손상 및 암 발병률을 높입니다.",
            "생활 속 안전 수치": "국내 토양 오염 우려 기준(1지역): 25mg/kg 이하 / 음용수 기준: 0.01mg/L 이하",
            "bg": "#E3F2FD"
        }
    }
    
    for i, (name, details) in enumerate(metals.items()):
        with info_cols[i]:
            st.markdown(f"""
            <div style='background-color: {details["bg"]}; padding: 30px; border-radius: 20px; min-height: 400px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);'>
                <h3 style='color: #1B5E20; border-bottom: 2px solid #2E7D32; padding-bottom: 10px;'>{name}</h3>
                <p style='margin-top: 20px;'><b>기본 정보</b><br>{details["기본정보"]}</p>
                <p><b>관련 질병</b><br>{details["관련 질병"]}</p>
                <p><b>생활 속 안전 수치</b><br>{details["생활 속 안전 수치"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br><p style='color: gray; text-align: center;'>* 본 분석 정보는 GPT-5.2 데이터 모델을 활용하여 공신력 있는 환경 보건 자료를 바탕으로 재구성되었습니다.</p>", unsafe_allow_html=True)

elif st.session_state['page'] == 'Etc':
    # --- SECTION 5: ETC (Image 5) ---
    st.title("출처 및 팀 정보")
    st.markdown("---")
    
    st.info("""
    **안내 및 면책 조항**  
    본 웹사이트는 지역 단위의 환경 측정 데이터를 기반으로 한 정보 제공 목적의 서비스입니다.  
    개인의 건강 상태에 대한 진단이나 의학적 판단을 대체하지 않습니다.
    """)
    
    st.subheader("데이터 출처")
    st.markdown(f"""
    - **Dataset:** {EXCEL_FILE if EXCEL_FILE else '중금속 통합 18-24년 요약 데이터'}
    - **Source:** 환경부 토양지하수정보시스템 (SGIS)
    """)
    
    st.subheader("NEW TERRA Team")
    team_members = ["강정우", "김주혜", "유민아", "박소현", "이가연"]
    st.markdown(" | ".join([f"**{m}**" for m in team_members]))
    st.markdown("<br><p>우리는 데이터 분석을 통해 더 안전한 대한민국을 만들어가는 팀입니다.</p>", unsafe_allow_html=True)

elif st.session_state['page'] == 'QnA':
    # --- SECTION 6: Q&A (Image 6) ---
    st.title("Q&A 센터")
    st.markdown("---")
    
    with st.container():
        with st.form("qna_center"):
            st.markdown("#### 문의 사항을 남겨주시면 빠르게 답변해 드리겠습니다.")
            q_name = st.text_input("작성자 성함")
            q_title = st.text_input("문의 제목")
            q_content = st.text_area("문의 상세 내용", height=200)
            q_submit = st.form_submit_button("문의 제출하기")
            
            if q_submit:
                st.success("소중한 의견이 접수되었습니다. 감사합니다.")
                
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; padding: 40px; background-color: #f1f1f1; border-radius: 10px;'>
            <p style='color: #666;'>협업 및 대량 데이터 분석 문의</p>
            <h4 style='color: #2E7D32;'>trace.newterra@gmail.com</h4>
        </div>
    """, unsafe_allow_html=True)
