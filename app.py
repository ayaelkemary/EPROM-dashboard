import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, time
import numpy as np
import os

# 1. PAGE SETUP
st.set_page_config(
    page_title="EPROM Building Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. PROFESSIONAL STYLING (Grey Background, EPROM Colors, & Black Text)
st.markdown("""
    <style>
    /* Force grey background for the whole app */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Ensure all general text is black */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li {
        color: #000000 !important;
    }

    [data-testid="stHeader"] {
        background-color: #f0f2f6;
    }
    .main {
        background-color: #f0f2f6;
    }
    
    /* Metric Card Styling - Transparent with separate black frames */
    div[data-testid="stMetric"] {
        background-color: transparent !important;
        border: 2px solid #000000 !important;
        padding: 10px !important;
        border-radius: 10px !important;
        margin-bottom: 10px !important;
        min-height: 150px !important; 
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    /* Remove default shadow and background from internal metric container */
    div[data-testid="metric-container"] {
        background-color: transparent !important;
        box-shadow: none !important;
        border: none !important;
        flex-grow: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    /* Ensure metric labels and values are black and fit the frame */
    div[data-testid="stMetricLabel"] > div {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    div[data-testid="stMetricValue"] > div {
        color: #000000 !important;
        font-size: 1.6rem !important; 
        white-space: nowrap !important;
    }

    /* Sidebar Styling - Smaller width and white text */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        min-width: 200px !important;
        max-width: 280px !important;
    }
    
    /* Sidebar Text Color */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, 
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .st-emotion-cache-17l6ba3,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
        color: white !important;
    }

    /* Status Boxes */
    .status-card {
        padding: 15px;
        border-radius: 10px;
        color: white !important;
        margin-bottom: 10px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 2px solid #000000; 
    }
    .status-green { background-color: #8cc63f; } /* EPROM Green */
    .status-blue { background-color: #00529b; }  /* EPROM Blue */
    .status-grey { background-color: #94a3b8; }
    
    /* Header Colors */
    h1, h2, h3 {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TOP CENTER LOGO
logo_path = "eprom_logo.png" 
_, col_center, _ = st.columns([0.8, 2, 0.8]) 
with col_center:
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #8cc63f; font-size: 100px; font-weight: bold; margin-bottom: 0;'>EPROM</h1>", unsafe_allow_html=True)

# 4. DATA ENGINE
def generate_demo_data():
    dates = pd.date_range(end=datetime.now(), periods=30)
    data = pd.DataFrame({
        'Date': dates,
        'Electricity_kWh': np.random.uniform(200, 500, 30),
        'Water_Liters': np.random.uniform(50, 150, 30),
        'Efficiency_Score': np.random.uniform(80, 99, 30)
    })
    return data

# 5. SIDEBAR NAVIGATION
with st.sidebar:
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("<h1 style='color: white; text-align: center; margin-bottom: 0;'>EPROM</h1>", unsafe_allow_html=True)
        
    st.markdown("<h2 style='color: white; text-align: center; margin-top: 0;'>Navigation</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Management Hub", ["Dashboard Overview", "Motion Sensor Analytics", "Split Unit AC Status", "Split Unit Logic", "Data Export"])
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload Excel/CSV Data", type=["xlsx", "csv"])
    st.divider()
    st.markdown("<p style='color: white; opacity: 0.8;'>EPROM BMS v5.4 | Integrated Systems</p>", unsafe_allow_html=True)

# Data Loading
if uploaded_file:
    try:
        if uploaded_file.name.endswith('xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        if 'Electricity_kWh' not in df.columns and len(df.columns) > 1:
            df.rename(columns={df.columns[1]: 'Electricity_kWh'}, inplace=True)
        if 'Water_Liters' not in df.columns and len(df.columns) > 2:
            df.rename(columns={df.columns[2]: 'Water_Liters'}, inplace=True)
        if 'Date' not in df.columns:
            df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    except Exception as e:
        st.sidebar.error(f"Data Error: {e}")
        df = generate_demo_data()
else:
    df = generate_demo_data()

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# 6. PAGE: DASHBOARD OVERVIEW
if page == "Dashboard Overview":
    st.title("📊 Building Performance Overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Power", f"{df['Electricity_kWh'].sum():,.0f} kWh", "+3.2%")
    m2.metric("Total Water", f"{df['Water_Liters'].sum():,.1f} L", "-1.5%")
    m3.metric("System Uptime", "99.9%", "Stable")
    ac_status = "Eco-Saving" if datetime.now().time() > time(15, 30) else "Active"
    m4.metric("AC Mode", ac_status)
    
    st.divider()
    
    # Graph 1: Utility Consumption Trend
    st.subheader("📈 Utility Consumption Trend (30 Days)")
    fig_line = px.line(df, x='Date', y=['Electricity_kWh', 'Water_Liters'],
                 color_discrete_sequence=['#8cc63f', '#00529b'],
                 labels={'value': 'Units', 'variable': 'Type'})
    
    fig_line.update_layout(
        template="simple_white", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color="black"), # Base font color
        xaxis=dict(
            tickfont=dict(color="black"), 
            title_font=dict(color="black")
        ),
        yaxis=dict(
            tickfont=dict(color="black"), 
            title_font=dict(color="black")
        ),
        legend=dict(font=dict(color="black")) 
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")

    # Graph 2: Power Allocation Breakdown
    st.subheader("🔋 Power Allocation Breakdown")
    pie_fig = px.pie(values=[55, 15, 20, 10], names=['Split AC Units', 'Lighting', 'Equipment', 'Auxiliary'],
                     color_discrete_sequence=['#0f172a', '#8cc63f', '#00529b', '#e2e8f0'], hole=0.5)
    
    pie_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="black"),
        legend=dict(font=dict(color="black"))
    )
    
    _, pie_col, _ = st.columns([1, 2, 1])
    with pie_col:
        st.plotly_chart(pie_fig, use_container_width=True)

# 7. PAGE: MOTION SENSOR ANALYTICS
elif page == "Motion Sensor Analytics":
    st.title("📡 Motion Sensor Activity")
    st.write("Real-time occupancy tracking for lighting and space management.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="status-card status-green">CORRIDOR NORTH<br>Motion: Detected<br>Status: 100% Light Intensity</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-card status-grey">SERVER ROOM<br>Motion: None<br>Status: Secure (Lights Off)</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="status-card status-blue">OFFICE ZONE B<br>Motion: Idle<br>Status: 30% Dimmed (Saving)</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-card status-green">MAIN RECEPTION<br>Motion: Detected<br>Status: Active</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="status-card status-grey">MEETING ROOM 4<br>Motion: None<br>Status: Power Off (Vacant)</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-card status-green">LAB ZONE 1<br>Motion: Detected<br>Status: Active</div>', unsafe_allow_html=True)

# 8. PAGE: SPLIT UNIT AC STATUS
elif page == "Split Unit AC Status":
    st.title("❄️ Split Unit AC Monitoring")
    st.write("Live telemetry and operating modes for individual air conditioning units.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="status-card status-green">AC-UNIT-ADMIN-01<br>Temp: 22°C<br>Mode: Cooling</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-card status-green">AC-UNIT-LAB-01<br>Temp: 20°C<br>Mode: Cooling</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="status-card status-blue">AC-UNIT-ADMIN-02<br>Temp: 25°C<br>Mode: Eco (Fan Only)</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-card status-blue">AC-UNIT-RECEPTION<br>Temp: 24°C<br>Mode: Eco</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="status-card status-grey">AC-UNIT-MEETING-01<br>Temp: --<br>Status: Power Off</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-card status-grey">AC-UNIT-STORAGE<br>Temp: --<br>Status: Power Off</div>', unsafe_allow_html=True)

# 9. PAGE: SPLIT UNIT LOGIC (Controls)
elif page == "Split Unit Logic":
    st.title("⚙️ Split Unit Automation Logic")
    st.info("At 15:30, the system triggers power-off commands for non-essential units.")
    
    now = datetime.now().time()
    cutoff = time(15, 30)
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Group Controls")
        st.button("Shutdown Admin Zone")
        st.button("Set Lab Zone to 22°C")
        if now > cutoff:
            st.error(f"AUTO-ECO MODE: ACTIVE (Time: {now.strftime('%H:%M')})")
        else:
            st.success("BUSINESS HOURS: Manual Control Enabled")

    with col_r:
        st.subheader("Scheduling")
        st.time_input("Shutdown Start Time", time(15, 30))
        st.multiselect("Active Days", ["Mon", "Tue", "Wed", "Thu", "Sun"], default=["Mon", "Tue", "Wed", "Thu", "Sun"])
        st.toggle("Emergency Master Shutdown")

# 10. PAGE: DATA EXPORT
elif page == "Data Export":
    st.title("📋 Reports & History")
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV Report", data=csv, file_name="EPROM_BMS_Report.csv")

# Footer
st.markdown("---")
st.caption(f"© {datetime.now().year} EPROM Building Systems | High Resolution Branding Enabled")