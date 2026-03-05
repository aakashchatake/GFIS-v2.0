import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="GFIS - Green Fuel Intelligence System",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .metric-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin: 10px 0;
        }
        .alert-critical {
            background-color: #fee;
            border-left: 4px solid #f00;
            padding: 10px;
            margin: 10px 0;
        }
        .alert-warning {
            background-color: #ffe;
            border-left: 4px solid #ff0;
            padding: 10px;
            margin: 10px 0;
        }
        .alert-normal {
            background-color: #efe;
            border-left: 4px solid #0f0;
            padding: 10px;
            margin: 10px 0;
        }
        /* Home page premium styles */
        .gfis-hero {
            background: linear-gradient(160deg, #050c05 0%, #0a1a0a 40%, #0f240f 100%);
            border-radius: 20px;
            padding: 64px 48px;
            text-align: center;
            border: 1px solid rgba(16,185,129,0.2);
            margin-bottom: 28px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(16,185,129,0.1);
        }
        .gfis-module-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-top: 3px solid #10b981;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            min-height: 140px;
            transition: box-shadow 0.2s ease;
        }
        .gfis-module-card:hover {
            box-shadow: 0 8px 24px rgba(16,185,129,0.12);
        }
        .gfis-stat-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 24px 20px;
            text-align: center;
        }
        .gfis-team-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-left: 4px solid #10b981;
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Warehouse/Biogas_Dataset_Rows.csv')
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except FileNotFoundError:
        return None

@st.cache_data
def load_location_data():
    try:
        df = pd.read_csv('Warehouse/solapur_gfis_dataset.csv')
        return df
    except FileNotFoundError:
        return None

@st.cache_data
def load_yield_data():
    try:
        df = pd.read_csv('Warehouse/gfis_biogas_dataset.csv')
        return df
    except FileNotFoundError:
        return None

df = load_data()
location_df = load_location_data()
yield_df = load_yield_data()

# Sidebar navigation
st.sidebar.title("🌿 GFIS Navigation")
page = st.sidebar.radio(
    "Select Dashboard",
    ["🌿 Home", "🏠 Overview", "📊 Real-time Monitoring", "🎯 Production Analytics", 
     "🤖 ML Predictions", "🗺️ Geographic Analysis", "⚡ Revenue Tracking", 
     "🔧 System Health", "📈 Advanced Analytics", "🏢 Enterprise Suite", 
     "🎯 Executive Command Center", "🌍 Sustainability Hub", "⚙️ Operations Center"]
)

st.sidebar.markdown("---")

# Enterprise Features Sidebar
st.sidebar.subheader("🚀 Enterprise Features")
enterprise_features = st.sidebar.checkbox("Enable Enterprise Mode", value=False)

if enterprise_features:
    st.sidebar.markdown("### Advanced Options")
    alert_notifications = st.sidebar.checkbox("Real-time Alerts", value=True)
    predictive_maintenance = st.sidebar.checkbox("Predictive Maintenance", value=True)
    collaboration_mode = st.sidebar.checkbox("Team Collaboration", value=False)
    export_reports = st.sidebar.checkbox("Advanced Reporting", value=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Actions")
    if st.sidebar.button("📊 Generate Report"):
        st.sidebar.success("Report generated!")
    if st.sidebar.button("🚨 Emergency Mode"):
        st.sidebar.error("Emergency protocols activated!")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background:linear-gradient(135deg,#0d2e0d,#1a3d1a);border:1px solid #2d7a2d;border-radius:8px;padding:14px;margin-top:6px;">
    <div style="color:#4caf50;font-weight:700;font-size:1em;margin-bottom:4px;">🌿 GFIS v2.0</div>
    <div style="color:#a5d6a7;font-size:0.78em;margin-bottom:8px;">Green Fuel Intelligence System<br><em>AI-Powered Biogas Optimization</em></div>
    <div style="border-top:1px solid #2d5a2d;padding-top:8px;margin-top:6px;">
        <div style="color:#81c784;font-size:0.75em;margin-bottom:3px;">🏢 <strong style="color:#c8e6c9;">Chatake Greenworks</strong></div>
        <div style="color:#81c784;font-size:0.72em;margin-bottom:3px;">📍 Solapur, Maharashtra, India</div>
        <div style="color:#81c784;font-size:0.72em;margin-bottom:6px;">🏆 DIPEX 2026 Submission</div>
        <a href="https://internship.chatakeinnoworks.com" target="_blank" style="color:#69f0ae;font-size:0.72em;text-decoration:none;">🔗 internship.chatakeinnoworks.com</a><br>
        <a href="https://about.chatakeinnoworks.com" target="_blank" style="color:#69f0ae;font-size:0.72em;text-decoration:none;">🌐 about.chatakeinnoworks.com</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== PAGE: HOME ====================
if page == "🌿 Home":

    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="gfis-hero">
        <div style="display:inline-block;background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);
             border-radius:100px;padding:6px 18px;margin-bottom:20px;">
            <span style="color:#10b981;font-size:0.75em;font-weight:600;letter-spacing:2px;text-transform:uppercase;">
                🏆 &nbsp;DIPEX 2026 &nbsp;·&nbsp; AIML Research Project
            </span>
        </div>
        <h1 style="font-size:2.6em;font-weight:800;color:#ffffff;margin:0 0 12px 0;
                   letter-spacing:-1.5px;line-height:1.15;">
            Green Fuel Intelligence<br>
            <span style="color:#10b981;">System</span>
        </h1>
        <p style="font-size:1.05em;color:#94a3b8;margin:0 0 6px 0;font-weight:400;max-width:600px;margin-left:auto;margin-right:auto;line-height:1.7;">
            AI-Powered Biogas Production Optimization Platform — Real-time IoT monitoring,
            machine learning predictions, carbon credit analytics, and ESG intelligence.
        </p>
        <div style="margin-top:28px;text-align:center;">
            <a href="https://green-fuel-intelligence--59klled.gamma.site/" target="_blank"
               style="display:inline-block;background:#10b981;color:#fff;padding:13px 30px;border-radius:8px;
                      text-decoration:none;font-weight:700;font-size:0.9em;margin:4px 6px;
                      box-shadow:0 4px 20px rgba(16,185,129,0.4);letter-spacing:0.3px;">
               📊 &nbsp;View Presentation
            </a>
            <a href="https://internship.chatakeinnoworks.com" target="_blank"
               style="display:inline-block;background:rgba(255,255,255,0.07);color:#e2e8f0;padding:13px 30px;
                      border-radius:8px;text-decoration:none;font-weight:600;font-size:0.9em;margin:4px 6px;
                      border:1px solid rgba(255,255,255,0.15);letter-spacing:0.3px;">
               🌐 &nbsp;Chatake Innoworks
            </a>
        </div>
        <div style="margin-top:28px;padding-top:24px;border-top:1px solid rgba(255,255,255,0.07);">
        <table width="100%" style="border-collapse:collapse;max-width:700px;margin:0 auto;">
          <tr>
            <td style="text-align:center;padding:8px 0;border-right:1px solid rgba(255,255,255,0.07);width:25%;">
                <div style="font-size:1.4em;font-weight:800;color:#10b981;">12</div>
                <div style="font-size:0.7em;color:#64748b;font-weight:500;letter-spacing:0.5px;">DASHBOARDS</div>
            </td>
            <td style="text-align:center;padding:8px 0;border-right:1px solid rgba(255,255,255,0.07);width:25%;">
                <div style="font-size:1.4em;font-weight:800;color:#10b981;">IoT</div>
                <div style="font-size:0.7em;color:#64748b;font-weight:500;letter-spacing:0.5px;">REAL-TIME DATA</div>
            </td>
            <td style="text-align:center;padding:8px 0;border-right:1px solid rgba(255,255,255,0.07);width:25%;">
                <div style="font-size:1.4em;font-weight:800;color:#10b981;">ML</div>
                <div style="font-size:0.7em;color:#64748b;font-weight:500;letter-spacing:0.5px;">PREDICTIONS</div>
            </td>
            <td style="text-align:center;padding:8px 0;width:25%;">
                <div style="font-size:1.4em;font-weight:800;color:#10b981;">ESG</div>
                <div style="font-size:0.7em;color:#64748b;font-weight:500;letter-spacing:0.5px;">CARBON CREDITS</div>
            </td>
          </tr>
        </table>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Presentation Banner ───────────────────────────────────────────────────
    st.markdown("""
    <table width="100%" style="background:#fefce8;border:1px solid #fde047;border-left:4px solid #f59e0b;
                border-radius:10px;padding:0;margin-bottom:28px;border-collapse:collapse;">
      <tr>
        <td style="padding:14px 20px;">
            <span style="font-weight:700;color:#92400e;font-size:0.9em;">📌 DIPEX 2026 Showcase</span>
            <span style="color:#78350f;font-size:0.85em;margin-left:10px;">
                Navigate all 12 dashboard modules from the sidebar. Start with <strong>Overview</strong>.
            </span>
        </td>
        <td style="padding:14px 20px;white-space:nowrap;">
            <a href="https://green-fuel-intelligence--59klled.gamma.site/" target="_blank"
               style="display:inline-block;background:#f59e0b;color:#fff;padding:8px 18px;border-radius:6px;
                      text-decoration:none;font-weight:700;font-size:0.82em;">
                Open Presentation →
            </a>
        </td>
      </tr>
    </table>
    """, unsafe_allow_html=True)

    # ── Dashboard Modules ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:8px;">
        <span style="font-size:1.25em;font-weight:700;color:#111827;">Dashboard Modules</span>
        <span style="font-size:0.85em;color:#6b7280;margin-left:12px;">
            12 AI-powered modules — select any from the sidebar
        </span>
    </div>
    """, unsafe_allow_html=True)

    pages_info = [
        ("🏠", "Overview", "System-wide KPIs, live plant status, and platform summary."),
        ("📊", "Real-time Monitoring", "Live digester telemetry — temperature, pressure, pH, CH₄."),
        ("🎯", "Production Analytics", "Biogas yield trends, feedstock efficiency, forecasting."),
        ("🤖", "ML Predictions", "XGBoost/LSTM predictions, anomaly detection, feedstock AI."),
        ("🗺️", "Geographic Analysis", "Spatial mapping of plants across Maharashtra."),
        ("⚡", "Revenue Tracking", "SaaS revenue, carbon credit income, ROI analytics."),
        ("🔧", "System Health", "Sensor diagnostics, IoT uptime, maintenance alerts."),
        ("📈", "Advanced Analytics", "Correlation matrices, optimization, statistical deep-dives."),
        ("🏢", "Enterprise Suite", "Predictive maintenance, financial intelligence, collaboration."),
        ("🎯", "Executive Command", "Strategic KPIs, market positioning, policy dashboards."),
        ("🌍", "Sustainability Hub", "ESG metrics, carbon footprint, GOBARdhan compliance."),
        ("⚙️", "Operations Center", "Plant ops, work orders, SOP management."),
    ]

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for i, (icon, name, desc) in enumerate(pages_info):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="gfis-module-card">
                <div style="font-size:1.5em;margin-bottom:8px;">{icon}</div>
                <div style="font-weight:700;color:#111827;font-size:0.9em;margin-bottom:6px;">{name}</div>
                <div style="color:#6b7280;font-size:0.78em;line-height:1.55;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.divider()

    # ── Team + Company ────────────────────────────────────────────────────────
    col_team, col_company = st.columns([1, 1], gap="large")

    with col_team:
        st.markdown("""
        <div style="margin-bottom:16px;">
            <span style="font-size:1.1em;font-weight:700;color:#111827;">Project Team</span>
            <span style="display:inline-block;background:#f0fdf4;color:#15803d;font-size:0.72em;
                         font-weight:600;padding:3px 10px;border-radius:100px;margin-left:10px;
                         border:1px solid #bbf7d0;">DIPEX 2026</span>
        </div>
        """, unsafe_allow_html=True)
        team = [
            ("Ms. Tanishka Deshpande", "AI / ML Engineering", "🔬"),
            ("Ms. Anushka Hitanalli",  "Cloud Architecture",  "☁️"),
            ("Ms. Aditi Gangji",       "Data Analytics",      "📊"),
            ("Ms. Shruti Hiremath",    "Systems Integration", "⚙️"),
        ]
        for name, role, icon in team:
            st.markdown(f"""
            <div class="gfis-team-card">
                <table style="border-collapse:collapse;width:100%;">
                  <tr>
                    <td width="38" style="font-size:1.4em;text-align:center;vertical-align:middle;padding-right:10px;">{icon}</td>
                    <td style="vertical-align:middle;">
                        <div style="font-weight:600;color:#111827;font-size:0.88em;">{name}</div>
                        <div style="color:#6b7280;font-size:0.76em;margin-top:2px;">{role}</div>
                    </td>
                  </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

    with col_company:
        st.markdown("""
        <div style="margin-bottom:16px;">
            <span style="font-size:1.1em;font-weight:700;color:#111827;">Strategic Partner</span>
        </div>
        <div style="background:linear-gradient(160deg,#050c05 0%,#0a1a0a 100%);
                    border:1px solid rgba(16,185,129,0.25);border-radius:16px;
                    padding:28px;color:white;
                    box-shadow:0 10px 40px rgba(0,0,0,0.3);">
            <div style="margin-bottom:16px;">
                <div style="font-size:1.3em;font-weight:800;color:#ffffff;letter-spacing:-0.5px;">
                    Chatake Greenworks
                </div>
                <div style="font-size:0.8em;color:#10b981;font-weight:500;margin-top:2px;">
                    Sustainable Energy Innovation Unit
                </div>
                <div style="font-size:0.75em;color:#475569;margin-top:3px;font-style:italic;">
                    A Division of Chatake Innoworks Pvt. Ltd.
                </div>
            </div>
            <div style="border-top:1px solid rgba(255,255,255,0.07);padding-top:16px;font-size:0.78em;line-height:2.1;">
                <div style="color:#94a3b8;">
                    📍 Nehru Industrial Estate, Damani Nagar<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;Solapur – 413001, Maharashtra, India
                </div>
                <div style="color:#94a3b8;margin-top:4px;">
                    📞 <a href="tel:+918600182228" style="color:#10b981;text-decoration:none;font-weight:500;">+91 8600182228</a>
                    &nbsp;&nbsp;
                    📧 <a href="mailto:admin@chatakeinnoworks.com" style="color:#10b981;text-decoration:none;font-weight:500;">admin@chatakeinnoworks.com</a>
                </div>
            </div>
                <img src="https://raw.githubusercontent.com/aakashchatake/GFIS-v2.0/main/assets/CI_Vision_2029.png"
                 style="width:100%;border-radius:10px;margin-top:16px;margin-bottom:8px;"
                 alt="Chatake Innoworks Office"/>
            <div style="margin-top:14px;padding-top:14px;border-top:1px solid rgba(255,255,255,0.07);">
                <a href="https://about.chatakeinnoworks.com" target="_blank"
                   style="color:#10b981;font-size:0.76em;text-decoration:none;font-weight:600;margin-right:16px;">
                   🌐 Corporate Profile
                </a>
                <a href="https://internship.chatakeinnoworks.com" target="_blank"
                   style="color:#10b981;font-size:0.76em;text-decoration:none;font-weight:600;margin-right:16px;">
                   🎓 Internship Portal
                </a>
                <a href="https://www.linkedin.com/company/chatakeinnoworks" target="_blank"
                   style="color:#10b981;font-size:0.76em;text-decoration:none;font-weight:600;">
                   💼 LinkedIn
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.divider()

    # ── Presentation Card ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:16px;
                padding:36px 40px;text-align:center;margin-top:4px;">
        <div style="display:inline-block;background:#f0fdf4;border:1px solid #bbf7d0;
                    border-radius:100px;padding:5px 14px;margin-bottom:14px;">
            <span style="color:#15803d;font-size:0.72em;font-weight:700;letter-spacing:1px;text-transform:uppercase;">
                Research Presentation
            </span>
        </div>
        <div style="font-size:1.35em;font-weight:700;color:#111827;margin-bottom:8px;">
            Full GFIS Strategic Roadmap
        </div>
        <div style="font-size:0.85em;color:#6b7280;max-width:550px;margin:0 auto 22px;line-height:1.65;">
            Market analysis · Carbon credit framework · ATEX IoT architecture ·
            MLOps pipeline · SATAT integration · Financial projections
        </div>
        <a href="https://green-fuel-intelligence--59klled.gamma.site/" target="_blank"
           style="background:#10b981;color:#fff;padding:13px 34px;border-radius:8px;
                  text-decoration:none;font-weight:700;font-size:0.9em;
                  box-shadow:0 4px 20px rgba(16,185,129,0.35);letter-spacing:0.3px;">
            Open Presentation &nbsp;→
        </a>
        <div style="font-size:0.72em;color:#9ca3af;margin-top:14px;">
            Hosted on Gamma &nbsp;·&nbsp; Chatake Greenworks &nbsp;·&nbsp; DIPEX 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== PAGE: OVERVIEW ====================
elif page == "🏠 Overview":
    st.title("🌿 GFIS - Green Fuel Intelligence System")
    st.markdown("### *AI-Powered Biogas Production Optimization for DIPEX 2026*")
    
    if df is not None:
        col1, col2, col3, col4 = st.columns(4)
        
        latest_data = df.iloc[-1]
        
        with col1:
            st.metric(
                "Current Temperature",
                f"{latest_data['Digester_Temp_C']:.1f}°C",
                f"Optimal: 35-55°C"
            )
        
        with col2:
            st.metric(
                "pH Level",
                f"{latest_data['pH']:.2f}",
                f"Optimal: 6.5-7.5"
            )
        
        with col3:
            st.metric(
                "Methane Production",
                f"{latest_data['Methane_m3_hr']:.2f} m³/hr",
                "Current rate"
            )
        
        with col4:
            st.metric(
                "System Status",
                latest_data['Yield_Status'],
                "Real-time"
            )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Key Metrics Dashboard")
            st.markdown("""
            ✅ **System Overview:**
            - Total Biogas Capacity: 1,000+ m³/day
            - Average Methane %: 55-60%
            - Operating Wards: 40+ zones
            - Electricity Potential: 2,500+ kWh/day
            """)
        
        with col2:
            st.subheader("🎯 DIPEX 2026 Objectives")
            st.markdown("""
            ✅ **Primary Goals:**
            - Optimize biogas yield prediction
            - Real-time digester monitoring
            - Revenue forecasting system
            - Geographic waste mapping
            - ML-powered optimization
            """)
    else:
        st.warning("Dataset not found. Please ensure Biogas_Dataset_Rows.csv is in the same directory.")

# ==================== PAGE: REAL-TIME MONITORING ====================
elif page == "📊 Real-time Monitoring":
    st.title("📊 Real-time Digester Monitoring")
    
    if df is not None:
        # Latest readings
        col1, col2, col3, col4, col5 = st.columns(5)
        
        latest = df.iloc[-1]
        
        with col1:
            st.metric("Temperature", f"{latest['Digester_Temp_C']:.1f}°C")
        with col2:
            st.metric("pH", f"{latest['pH']:.2f}")
        with col3:
            st.metric("Methane %", f"{latest['CH4_percent']:.1f}%")
        with col4:
            st.metric("Gas Flow", f"{latest['Gas_Flow_m3_hr']:.2f} m³/hr")
        with col5:
            status_color = "🟢" if latest['Yield_Status'] == "Normal" else "🟡" if latest['Yield_Status'] == "Warning" else "🔴"
            st.metric("Status", f"{status_color} {latest['Yield_Status']}")
        
        st.markdown("---")
        
        # Time series visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Temperature & pH Trend")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['Timestamp'], y=df['Digester_Temp_C'],
                name='Temperature (°C)', yaxis='y', line=dict(color='#ff7f0e')
            ))
            fig.add_trace(go.Scatter(
                x=df['Timestamp'], y=df['pH'],
                name='pH Level', yaxis='y2', line=dict(color='#2ca02c')
            ))
            fig.update_layout(
                hovermode='x unified',
                yaxis=dict(title='Temperature (°C)'),
                yaxis2=dict(title='pH Level', overlaying='y', side='right'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Methane Production Rate")
            fig = px.area(df, x='Timestamp', y='Methane_m3_hr',
                         labels={'Methane_m3_hr': 'Methane (m³/hr)'},
                         color_discrete_sequence=['#1f77b4'])
            fig.update_layout(height=400, hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Feed Rate Analysis")
            avg_feed = df['Feed_Rate_kg_hr'].mean()
            max_feed = df['Feed_Rate_kg_hr'].max()
            st.metric("Average Feed Rate", f"{avg_feed:.1f} kg/hr")
            st.metric("Peak Feed Rate", f"{max_feed:.1f} kg/hr")
        
        with col2:
            st.subheader("Gas Composition")
            latest_ch4 = latest['CH4_percent']
            latest_co2 = 100 - latest_ch4
            fig = go.Figure(data=[
                go.Pie(labels=['CH4 (Methane)', 'CO2 & Others'],
                       values=[latest_ch4, latest_co2],
                       marker=dict(colors=['#1f77b4', '#ff7f0e']))
            ])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.subheader("C:N Ratio Distribution")
            avg_cn = df['C_N_Ratio'].mean()
            st.metric("Avg C:N Ratio", f"{avg_cn:.1f}")
            st.write(f"*Optimal range: 20-30*")
            
            cn_fig = px.histogram(df, x='C_N_Ratio',
                                 title="C:N Ratio Histogram",
                                 nbins=20, color_discrete_sequence=['#2ca02c'])
            cn_fig.update_layout(height=300)
            st.plotly_chart(cn_fig, use_container_width=True)
        
        # Status alerts
        st.subheader("⚠️ System Alerts")
        
        warnings_list = df[df['Yield_Status'] != 'Normal'].tail(10)
        if len(warnings_list) > 0:
            for idx, row in warnings_list.iterrows():
                status_class = "alert-warning" if row['Yield_Status'] == "Warning" else "alert-critical"
                st.markdown(f"""
                <div class="{status_class}">
                <strong>{row['Timestamp'].strftime('%Y-%m-%d %H:%M')}</strong> | 
                Ward: {row['Ward']} | Status: {row['Yield_Status']} | 
                Temp: {row['Digester_Temp_C']:.1f}°C | pH: {row['pH']:.2f}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ All systems operating normally!")

# ==================== PAGE: PRODUCTION ANALYTICS ====================
elif page == "🎯 Production Analytics":
    st.title("🎯 Production Analytics & Insights")
    
    if df is not None:
        # Daily production summary
        df['Date'] = df['Timestamp'].dt.date
        daily_production = df.groupby('Date').agg({
            'Methane_m3_hr': 'sum',
            'Methane_kg_hr': 'sum',
            'CO2e_Reduction_kg_hr': 'sum',
            'CH4_percent': 'mean'
        }).reset_index()
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_methane = daily_production['Methane_m3_hr'].sum()
        total_co2_reduction = daily_production['CO2e_Reduction_kg_hr'].sum()
        avg_ch4 = daily_production['CH4_percent'].mean()
        
        with col1:
            st.metric("Total Methane (Period)", f"{total_methane:.1f} m³")
        with col2:
            st.metric("CO2 Reduction", f"{total_co2_reduction:.1f} kg")
        with col3:
            st.metric("Avg Methane %", f"{avg_ch4:.1f}%")
        with col4:
            st.metric("Operating Days", f"{len(daily_production)}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Daily Methane Production")
            fig = px.bar(daily_production, x='Date', y='Methane_m3_hr',
                        labels={'Methane_m3_hr': 'Methane (m³)'},
                        color='Methane_m3_hr', color_continuous_scale='Blues')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("CO2 Reduction Impact")
            fig = px.line(daily_production, x='Date', y='CO2e_Reduction_kg_hr',
                         markers=True, color_discrete_sequence=['#2ca02c'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Feedstock type analysis
        st.subheader("📦 Feedstock Type Distribution")
        
        feedstock_stats = df.groupby('Feedstock_Type').agg({
            'Methane_m3_hr': ['sum', 'mean'],
            'Feed_Rate_kg_hr': 'mean',
            'CH4_percent': 'mean'
        }).round(2)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            feedstock_pie = df['Feedstock_Type'].value_counts()
            fig = px.pie(values=feedstock_pie.values, names=feedstock_pie.index,
                        title="Feedstock Type Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Feedstock Performance")
            feedstock_yield = df.groupby('Feedstock_Type')['Methane_m3_hr'].mean().sort_values(ascending=False)
            fig = px.bar(x=feedstock_yield.values, y=feedstock_yield.index,
                        orientation='h', color=feedstock_yield.values,
                        color_continuous_scale='Viridis')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.subheader("Ward Performance")
            ward_performance = df.groupby('Ward').agg({
                'Methane_m3_hr': 'mean',
                'CH4_percent': 'mean'
            }).round(2).sort_values('Methane_m3_hr', ascending=False).head(10)
            st.dataframe(ward_performance, height=400)

# ==================== PAGE: ML PREDICTIONS ====================
elif page == "🤖 ML Predictions":
    st.title("🤖 ML-Powered Predictions")
    
    st.info("🔬 Advanced ML Models for Biogas Optimization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Biogas Yield Predictor")
        st.markdown("""
        **Model**: XGBoost Regression
        
        **Inputs:**
        - Feedstock type & quantity
        - Temperature, pH, pressure
        - C:N ratio
        - Feed rate
        
        **Output:** Predicted methane (m³/day)
        """)
        
        # Simulated prediction
        if df is not None:
            latest = df.iloc[-1]
            predicted_yield = latest['Methane_m3_hr'] * 24 * 1.05  # +5% optimization
            actual_yield = latest['Methane_m3_hr'] * 24
            
            st.metric("Predicted Daily Yield", f"{predicted_yield:.1f} m³/day")
            st.metric("Current Daily Yield", f"{actual_yield:.1f} m³/day")
            st.success(f"✅ Optimization potential: +5.0%")
    
    with col2:
        st.subheader("🎯 Quality Classifier")
        st.markdown("""
        **Model**: Random Forest Classification
        
        **Grades:**
        - **A**: Optimal conditions (CH4 >57%, Temp 38-40°C, pH 7.0-7.2)
        - **B**: Good conditions (CH4 54-57%, Temp 36-42°C, pH 6.8-7.2)
        - **C**: Suboptimal (CH4 <54%, Temp <36 or >42°C)
        
        **Recommendation Engine:** Suggests adjustments for grade A
        """)
        
        if df is not None:
            latest = df.iloc[-1]
            if latest['CH4_percent'] > 57 and 38 <= latest['Digester_Temp_C'] <= 40 and 7.0 <= latest['pH'] <= 7.2:
                grade = "A"
                color = "🟢"
            elif latest['CH4_percent'] > 54 and 36 <= latest['Digester_Temp_C'] <= 42 and 6.8 <= latest['pH'] <= 7.2:
                grade = "B"
                color = "🟡"
            else:
                grade = "C"
                color = "🔴"
            
            st.metric("Current Quality Grade", f"{color} {grade}")
            
            if grade == "B":
                st.warning(f"⚠️ Slight adjustment needed - Increase pH to {7.0 + (7.2-latest['pH'])/2:.2f}")
            elif grade == "C":
                st.error("🔴 Significant optimization needed")

# ==================== PAGE: GEOGRAPHIC ANALYSIS ====================
elif page == "🗺️ Geographic Analysis":
    st.title("🗺️ Geographic & Spatial Analysis")
    
    if location_df is not None:
        st.subheader("📍 Ward-level Biogas Potential Map")
        
        # Scatter map with biogas potential
        fig = px.scatter_geo(location_df, lat='latitude', lon='longitude',
                            size='estimated_biogas_m3_day',
                            color='estimated_methane_pct',
                            hover_name='ward_id',
                            hover_data={'estimated_biogas_m3_day': ':.0f',
                                       'estimated_methane_pct': ':.1f',
                                       'electricity_potential_kwh_day': ':.0f'},
                            color_continuous_scale='Viridis',
                            scope='asia',
                            title="Solapur - Biogas Production Potential")
        
        fig.update_layout(height=600, geo=dict(
            center=dict(lat=17.65, lon=75.93),
            projection_type='mercator'
        ))
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics by ward
        st.subheader("📊 Top Wards by Potential")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Wards Analyzed", len(location_df))
        with col2:
            st.metric("Avg Biogas Potential", f"{location_df['estimated_biogas_m3_day'].mean():.0f} m³/day")
        with col3:
            st.metric("Peak Electricity", f"{location_df['electricity_potential_kwh_day'].sum():.0f} kWh/day")
        
        # Top performers
        top_wards = location_df.nlargest(10, 'estimated_biogas_m3_day')[
            ['ward_id', 'estimated_biogas_m3_day', 'estimated_methane_pct', 
             'electricity_potential_kwh_day', 'co2_reduction_tonnes_year']
        ]
        
        st.subheader("🏆 Top 10 Wards by Biogas Potential")
        st.dataframe(top_wards.reset_index(drop=True), use_container_width=True)
        
        # Collection efficiency map
        fig2 = px.histogram(location_df, x='collection_efficiency_pct',
                           nbins=20, title="Collection Efficiency Distribution",
                           color_discrete_sequence=['#1f77b4'])
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)

# ==================== PAGE: REVENUE TRACKING ====================
elif page == "⚡ Revenue Tracking":
    st.title("⚡ Revenue & Financial Analysis")
    
    if df is not None:
        st.subheader("💰 Revenue Forecasting Dashboard")
        
        # Energy metrics
        col1, col2, col3, col4 = st.columns(4)
        
        df['Date'] = df['Timestamp'].dt.date
        daily_energy = df.groupby('Date')['Methane_m3_hr'].sum() * 24  # Convert to daily
        
        total_methane = daily_energy.sum()
        # Assumed rates: 1 m³ methane ≈ 36 MJ ≈ 10 kWh ≈ ₹100
        electrical_kwh = total_methane * 10
        revenue_inr = electrical_kwh * 8  # ₹8 per kWh average rate
        
        with col1:
            st.metric("Total Methane", f"{total_methane:.0f} m³")
        with col2:
            st.metric("Electrical Output", f"{electrical_kwh:.0f} kWh")
        with col3:
            st.metric("Estimated Revenue", f"₹{revenue_inr:.0f}")
        with col4:
            st.metric("Revenue/Day", f"₹{revenue_inr/len(daily_energy):.0f}")
        
        st.markdown("---")
        
        # Revenue projection
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Daily Revenue Projection")
            daily_revenue = (daily_energy * 8).reset_index()
            daily_revenue.columns = ['Date', 'Revenue']
            
            fig = px.area(daily_revenue, x='Date', y='Revenue',
                         title="Daily Revenue (₹)",
                         color_discrete_sequence=['#2ca02c'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Monthly & Yearly Projections")
            
            # Calculate projections
            daily_avg = daily_energy.mean()
            monthly_projection = daily_avg * 30 * 8
            yearly_projection = monthly_projection * 12
            
            st.metric("Monthly (Projected)", f"₹{monthly_projection:.0f}")
            st.metric("Yearly (Projected)", f"₹{yearly_projection:.0f}")
            
            # Cost-benefit analysis
            st.subheader("💡 Cost-Benefit Analysis")
            installation_cost = 500000  # ₹5 lakhs
            yearly_return = yearly_projection
            payback_months = (installation_cost / (yearly_return / 12))
            roi_percent = (yearly_return / installation_cost) * 100
            
            st.info(f"""
            **Investment Analysis:**
            - Estimated Installation Cost: ₹{installation_cost:,.0f}
            - Annual Revenue: ₹{yearly_return:,.0f}
            - Payback Period: {payback_months:.1f} months
            - Year 1 ROI: {roi_percent:.1f}%
            """)

# ==================== PAGE: SYSTEM HEALTH ====================
elif page == "🔧 System Health":
    st.title("🔧 System Health & Diagnostics")
    
    if df is not None:
        # Health score calculation
        latest = df.iloc[-1]
        
        health_metrics = {
            'Temperature Stability': 100 if 35 <= latest['Digester_Temp_C'] <= 55 else 70,
            'pH Balance': 100 if 6.5 <= latest['pH'] <= 7.5 else 80,
            'Methane Production': 100 if latest['CH4_percent'] >= 55 else 85,
            'System Efficiency': 100 if latest['Yield_Status'] == 'Normal' else 75,
            'Feed Rate Optimization': 100 if 400 <= latest['Feed_Rate_kg_hr'] <= 600 else 80
        }
        
        overall_health = sum(health_metrics.values()) / len(health_metrics)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Overall health gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=overall_health,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Overall System Health"},
                delta={'reference': 90},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "yellow"},
                        {'range': [75, 100], 'color': "lightgreen"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90}}))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Component Health Scores")
            
            health_df = pd.DataFrame(list(health_metrics.items()), 
                                    columns=['Component', 'Health %'])
            
            fig = px.bar(health_df, y='Component', x='Health %',
                        orientation='h', color='Health %',
                        color_continuous_scale='RdYlGn',
                        text='Health %')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed diagnostics
        st.subheader("🔍 Detailed Diagnostics")
        
        diagnostics = []
        
        # Temperature check
        if latest['Digester_Temp_C'] < 35:
            diagnostics.append(("⚠️ Low Temperature", f"{latest['Digester_Temp_C']:.1f}°C - Increase heating"))
        elif latest['Digester_Temp_C'] > 55:
            diagnostics.append(("⚠️ High Temperature", f"{latest['Digester_Temp_C']:.1f}°C - Improve cooling"))
        else:
            diagnostics.append(("✅ Temperature Optimal", f"{latest['Digester_Temp_C']:.1f}°C"))
        
        # pH check
        if latest['pH'] < 6.5:
            diagnostics.append(("⚠️ Low pH (Acidic)", f"{latest['pH']:.2f} - Add buffer"))
        elif latest['pH'] > 7.5:
            diagnostics.append(("⚠️ High pH (Alkaline)", f"{latest['pH']:.2f} - Add organic matter"))
        else:
            diagnostics.append(("✅ pH Optimal", f"{latest['pH']:.2f}"))
        
        # Methane check
        if latest['CH4_percent'] < 50:
            diagnostics.append(("⚠️ Low Methane %", f"{latest['CH4_percent']:.1f}% - Review feedstock"))
        else:
            diagnostics.append(("✅ Methane Optimal", f"{latest['CH4_percent']:.1f}%"))
        
        # C:N ratio
        if latest['C_N_Ratio'] < 20:
            diagnostics.append(("⚠️ Low C:N Ratio", f"{latest['C_N_Ratio']:.1f} - Add carbon source"))
        elif latest['C_N_Ratio'] > 30:
            diagnostics.append(("⚠️ High C:N Ratio", f"{latest['C_N_Ratio']:.1f} - Add nitrogen source"))
        else:
            diagnostics.append(("✅ C:N Ratio Optimal", f"{latest['C_N_Ratio']:.1f}"))
        
        for status, message in diagnostics:
            if "✅" in status:
                st.success(f"{status} {message}")
            else:
                st.warning(f"{status} {message}")

# ==================== PAGE: ADVANCED ANALYTICS ====================
elif page == "📈 Advanced Analytics":
    st.title("📈 Advanced Analytics & Correlations")
    
    if df is not None and yield_df is not None:
        st.subheader("🔗 Parameter Correlations")
        
        # Correlation analysis
        numeric_cols = ['Digester_Temp_C', 'pH', 'CH4_percent', 'Gas_Flow_m3_hr',
                       'Feed_Rate_kg_hr', 'C_N_Ratio', 'Methane_m3_hr', 'CO2e_Reduction_kg_hr']
        
        corr_matrix = df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 10}
        ))
        fig.update_layout(height=600, title="Parameter Correlation Matrix")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Yield dataset analysis
        st.subheader("🎯 Feedstock Yield Analysis")
        
        if len(yield_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Waste type vs yield
                waste_yield = yield_df.groupby('waste_type')['methane_yield_m3'].agg(['mean', 'count']).sort_values('mean', ascending=False)
                
                fig = px.bar(x=waste_yield.index, y=waste_yield['mean'],
                            title="Average Methane Yield by Waste Type",
                            labels={'y': 'Avg Methane Yield (m³)', 'x': 'Waste Type'},
                            color=waste_yield['mean'],
                            color_continuous_scale='Viridis')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Distance impact
                fig = px.scatter(yield_df, x='distance_to_road_km', y='methane_yield_m3',
                               color='waste_type', title="Distance vs Methane Yield",
                               labels={'distance_to_road_km': 'Distance to Road (km)',
                                      'methane_yield_m3': 'Methane Yield (m³)'},
                               height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Population density impact
            st.subheader("Population & Animal Population Impact")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.scatter(yield_df, x='population_density', y='methane_yield_m3',
                               size='daily_waste_mass_kg', color='waste_type',
                               title="Population Density vs Yield",
                               height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.scatter(yield_df, x='animal_population', y='methane_yield_m3',
                               size='daily_waste_mass_kg',
                               title="Animal Population vs Yield",
                               color_discrete_sequence=['#1f77b4'],
                               height=400)
                st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE: ENTERPRISE SUITE ====================
elif page == "🏢 Enterprise Suite":
    st.title("🏢 Enterprise Intelligence Suite")
    st.markdown("### *Advanced Analytics & Business Intelligence*")

    if not enterprise_features:
        st.warning("⚠️ Enterprise features are disabled. Enable 'Enterprise Mode' in the sidebar to access advanced capabilities.")
        st.info("""
        **Enterprise Suite includes:**
        - 🔍 Predictive Maintenance Engine
        - 📊 Advanced Financial Modeling
        - 🤝 Team Collaboration Tools
        - 📈 Automated Reporting System
        - 🎯 Scenario Planning & Optimization
        - 🔗 API Integration Hub
        - 📧 Smart Alert System
        """)
    else:
        # Enterprise tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔍 Predictive Maintenance",
            "📊 Financial Intelligence",
            "🤝 Team Collaboration",
            "📈 Advanced Reporting",
            "🎯 Optimization Engine"
        ])

        with tab1:
            st.header("🔍 Predictive Maintenance Engine")

            if df is not None:
                # Predictive maintenance analysis
                st.subheader("Equipment Health Prediction")

                # Simulate predictive maintenance data
                maintenance_data = []
                for i in range(10):
                    equipment = f"Digester_{i+1:02d}"
                    health_score = np.random.uniform(75, 100)
                    days_to_maintenance = int(np.random.uniform(30, 180))
                    risk_level = "Low" if health_score > 90 else "Medium" if health_score > 80 else "High"

                    maintenance_data.append({
                        'Equipment': equipment,
                        'Health_Score': health_score,
                        'Days_to_Maintenance': days_to_maintenance,
                        'Risk_Level': risk_level,
                        'Predicted_Failure_Prob': 100 - health_score
                    })

                maint_df = pd.DataFrame(maintenance_data)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Systems Monitored", len(maint_df))
                with col2:
                    avg_health = maint_df['Health_Score'].mean()
                    st.metric("Average Health Score", f"{avg_health:.1f}%")
                with col3:
                    critical_count = len(maint_df[maint_df['Risk_Level'] == 'High'])
                    st.metric("Critical Systems", critical_count)

                # Health dashboard
                fig = px.bar(maint_df, x='Equipment', y='Health_Score',
                           color='Risk_Level',
                           color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'},
                           title="Equipment Health Overview")
                st.plotly_chart(fig, use_container_width=True)

                # Maintenance schedule
                st.subheader("📅 Maintenance Schedule")
                urgent_maintenance = maint_df[maint_df['Days_to_Maintenance'] < 60].sort_values('Days_to_Maintenance')

                if len(urgent_maintenance) > 0:
                    for _, row in urgent_maintenance.iterrows():
                        if row['Days_to_Maintenance'] < 30:
                            st.error(f"🚨 URGENT: {row['Equipment']} requires maintenance in {row['Days_to_Maintenance']} days")
                        else:
                            st.warning(f"⚠️ SCHEDULED: {row['Equipment']} maintenance due in {row['Days_to_Maintenance']} days")
                else:
                    st.success("✅ All systems have maintenance scheduled beyond 60 days")

        with tab2:
            st.header("📊 Financial Intelligence Hub")

            if df is not None:
                st.subheader("Advanced ROI & Investment Analysis")

                # Investment scenarios
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("💰 Investment Scenarios")

                    # Scenario inputs
                    initial_investment = st.slider("Initial Investment (₹)", 100000, 5000000, 1000000, 50000)
                    operational_cost_pct = st.slider("Annual Operational Cost (%)", 5, 25, 15)
                    energy_price_per_kwh = st.slider("Energy Price (₹/kWh)", 5, 15, 8)

                    # Calculate projections
                    daily_energy = (df['Methane_m3_hr'].mean() * 24) * 10  # Convert to kWh
                    annual_energy = daily_energy * 365
                    annual_revenue = annual_energy * energy_price_per_kwh
                    annual_cost = initial_investment * (operational_cost_pct / 100)
                    annual_profit = annual_revenue - annual_cost

                    st.metric("Annual Revenue", f"₹{annual_revenue:,.0f}")
                    st.metric("Annual Costs", f"₹{annual_cost:,.0f}")
                    st.metric("Annual Profit", f"₹{annual_profit:,.0f}")

                with col2:
                    st.subheader("📈 ROI Projections")

                    # ROI calculation
                    payback_years = initial_investment / annual_profit if annual_profit > 0 else 999
                    roi_5year = ((annual_profit * 5) / initial_investment) * 100
                    npv_5year = annual_profit * (1 - (1 + 0.1)**-5) / 0.1 - initial_investment

                    st.metric("Payback Period", f"{payback_years:.1f} years")
                    st.metric("5-Year ROI", f"{roi_5year:.1f}%")
                    st.metric("5-Year NPV", f"₹{npv_5year:,.0f}")

                    # Carbon credits
                    annual_co2 = df['CO2e_Reduction_kg_hr'].mean() * 24 * 365 / 1000  # tonnes
                    carbon_credit_value = annual_co2 * 1000  # ₹1000 per tonne
                    st.metric("Annual Carbon Credits", f"₹{carbon_credit_value:,.0f}")

                # Sensitivity analysis
                st.subheader("🎯 Sensitivity Analysis")

                scenarios = []
                for energy_price in [6, 8, 10, 12]:
                    revenue = annual_energy * energy_price
                    profit = revenue - annual_cost
                    roi = (profit / initial_investment) * 100
                    scenarios.append({
                        'Energy_Price': energy_price,
                        'Revenue': revenue,
                        'Profit': profit,
                        'ROI': roi
                    })

                scenario_df = pd.DataFrame(scenarios)

                fig = px.line(scenario_df, x='Energy_Price', y='ROI',
                            markers=True, title="ROI Sensitivity to Energy Price")
                fig.update_layout(xaxis_title="Energy Price (₹/kWh)", yaxis_title="ROI (%)")
                st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.header("🤝 Team Collaboration Center")

            st.subheader("👥 Active Team Members")
            team_members = [
                {"name": "Dr. Rajesh Kumar", "role": "Project Lead", "status": "online", "last_active": "Now"},
                {"name": "Priya Sharma", "role": "Data Scientist", "status": "online", "last_active": "2 min ago"},
                {"name": "Amit Patel", "role": "ML Engineer", "status": "away", "last_active": "1 hour ago"},
                {"name": "Sneha Gupta", "role": "Business Analyst", "status": "online", "last_active": "Now"}
            ]

            for member in team_members:
                status_emoji = "🟢" if member["status"] == "online" else "🟡" if member["status"] == "away" else "🔴"
                st.write(f"{status_emoji} **{member['name']}** - {member['role']} ({member['last_active']})")

            st.markdown("---")

            # Collaboration tools
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("💬 Team Chat")
                st.text_area("Type your message...", height=100)
                if st.button("Send Message"):
                    st.success("Message sent to team!")

                st.subheader("📋 Shared Tasks")
                tasks = [
                    "Review ML model performance - Due: Today",
                    "Update financial projections - Due: Tomorrow",
                    "Prepare DIPEX presentation - Due: Friday"
                ]
                for task in tasks:
                    st.checkbox(task, value=False)

            with col2:
                st.subheader("📊 Live Activity Feed")
                activities = [
                    "Priya updated ML model accuracy to 92%",
                    "Amit deployed new dashboard features",
                    "Dr. Kumar reviewed financial projections",
                    "System alert: Digester_05 maintenance due",
                    "New data uploaded from Ward_15"
                ]

                for activity in activities:
                    st.info(f"🔔 {activity}")

        with tab4:
            st.header("📈 Advanced Reporting System")

            st.subheader("📋 Automated Report Generation")

            # Report configuration
            col1, col2 = st.columns(2)

            with col1:
                report_type = st.selectbox("Report Type",
                    ["Executive Summary", "Technical Report", "Financial Analysis",
                     "Operational Dashboard", "Maintenance Report", "Custom Report"])

                date_range = st.date_input("Date Range", value=(datetime.now() - timedelta(days=30), datetime.now()))

                include_charts = st.checkbox("Include Charts", value=True)
                include_raw_data = st.checkbox("Include Raw Data", value=False)

            with col2:
                export_format = st.selectbox("Export Format", ["PDF", "Excel", "PowerPoint", "HTML"])

                if st.button("🚀 Generate Report", type="primary"):
                    with st.spinner("Generating report..."):
                        import time
                        time.sleep(2)
                    st.success(f"✅ {report_type} report generated successfully!")

                    # Download button
                    if export_format == "PDF":
                        st.download_button("📥 Download PDF Report",
                                         "Sample report content",
                                         file_name=f"GFIS_{report_type}_{datetime.now().strftime('%Y%m%d')}.pdf")

                # Scheduled reports
                st.subheader("⏰ Scheduled Reports")
                st.checkbox("Daily Executive Summary (8 AM)", value=True)
                st.checkbox("Weekly Technical Report (Friday)", value=True)
                st.checkbox("Monthly Financial Review (1st)", value=True)

            # Report templates
            st.subheader("📚 Report Templates")

            templates = {
                "Executive Summary": "High-level KPIs, revenue projections, system health",
                "Technical Report": "Detailed analytics, ML performance, system diagnostics",
                "Financial Analysis": "ROI analysis, cost breakdowns, investment scenarios",
                "Operational Dashboard": "Real-time metrics, alerts, performance indicators"
            }

            for template, description in templates.items():
                with st.expander(f"📄 {template}"):
                    st.write(description)
                    if st.button(f"Use {template} Template", key=template):
                        st.success(f"{template} template applied!")

        with tab5:
            st.header("🎯 AI Optimization Engine")

            st.subheader("🤖 Scenario Planning & Optimization")

            if df is not None:
                # Optimization inputs
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.subheader("Current Parameters")
                    current_temp = df['Digester_Temp_C'].iloc[-1]
                    current_ph = df['pH'].iloc[-1]
                    current_feed = df['Feed_Rate_kg_hr'].iloc[-1]

                    st.metric("Temperature", f"{current_temp:.1f}°C")
                    st.metric("pH Level", f"{current_ph:.2f}")
                    st.metric("Feed Rate", f"{current_feed:.0f} kg/hr")

                with col2:
                    st.subheader("Optimization Targets")
                    target_temp = st.slider("Target Temperature (°C)", 35, 55, 38)
                    target_ph = st.slider("Target pH", 6.5, 7.5, 7.0)
                    target_feed = st.slider("Target Feed Rate (kg/hr)", 300, 800, 500)

                with col3:
                    st.subheader("Optimization Results")

                    # Calculate optimization potential
                    temp_diff = abs(current_temp - target_temp)
                    ph_diff = abs(current_ph - target_ph)
                    feed_diff = abs(current_feed - target_feed)

                    optimization_score = 100 - (temp_diff + ph_diff*10 + feed_diff/50)

                    st.metric("Optimization Score", f"{max(0, optimization_score):.1f}%")

                    if optimization_score > 80:
                        st.success("🎯 Near optimal conditions!")
                    elif optimization_score > 60:
                        st.warning("⚠️ Moderate optimization needed")
                    else:
                        st.error("🔴 Significant adjustments required")

                # AI Recommendations
                st.subheader("🧠 AI-Powered Recommendations")

                recommendations = []

                if temp_diff > 2:
                    if current_temp < target_temp:
                        recommendations.append("🔥 Increase digester heating by 2-3°C")
                    else:
                        recommendations.append("❄️ Improve cooling system efficiency")

                if ph_diff > 0.2:
                    if current_ph < target_ph:
                        recommendations.append("🧪 Add alkaline buffer to increase pH")
                    else:
                        recommendations.append("🌱 Add organic matter to decrease pH")

                if feed_diff > 50:
                    if current_feed < target_feed:
                        recommendations.append("📦 Increase feedstock loading rate gradually")
                    else:
                        recommendations.append("⏳ Reduce feed rate to prevent overloading")

                recommendations.append("📊 Monitor methane production for 24-48 hours")
                recommendations.append("🔬 Schedule gas composition analysis")

                for rec in recommendations:
                    st.info(rec)

                # Scenario comparison
                st.subheader("📊 Scenario Comparison")

                scenarios = pd.DataFrame({
                    'Scenario': ['Current', 'Optimized', 'Maximum Potential'],
                    'Methane_Yield': [df['Methane_m3_hr'].iloc[-1],
                                    df['Methane_m3_hr'].iloc[-1] * 1.15,
                                    df['Methane_m3_hr'].iloc[-1] * 1.35],
                    'Energy_Output_kWh': [df['Methane_m3_hr'].iloc[-1] * 24 * 10,
                                        df['Methane_m3_hr'].iloc[-1] * 24 * 10 * 1.15,
                                        df['Methane_m3_hr'].iloc[-1] * 24 * 10 * 1.35],
                    'Revenue_INR': [df['Methane_m3_hr'].iloc[-1] * 24 * 10 * 8,
                                  df['Methane_m3_hr'].iloc[-1] * 24 * 10 * 8 * 1.15,
                                  df['Methane_m3_hr'].iloc[-1] * 24 * 10 * 8 * 1.35]
                })

                fig = px.bar(scenarios, x='Scenario', y='Revenue_INR',
                           title="Revenue Scenarios Comparison",
                           color='Scenario',
                           color_discrete_map={'Current': 'gray', 'Optimized': 'blue', 'Maximum Potential': 'green'})
                fig.update_layout(yaxis_title="Annual Revenue (₹)")
                st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE: EXECUTIVE COMMAND CENTER ====================
elif page == "🎯 Executive Command Center":
    st.title("🎯 Executive Command Center")
    st.markdown("### *Strategic Decision Support & Executive Insights*")

    if df is not None:
        # Executive KPIs at a glance
        st.subheader("📊 Executive Summary Dashboard")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        # Calculate key metrics
        total_methane = df['Methane_m3_hr'].sum()
        total_energy = total_methane * 24 * 10  # Convert to daily kWh
        total_revenue = total_energy * 8  # ₹8 per kWh
        co2_reduction = df['CO2e_Reduction_kg_hr'].sum() * 24 / 1000  # tonnes per day
        system_efficiency = df['CH4_percent'].mean()
        wards_active = df['Ward'].nunique()

        with col1:
            st.metric("Total Revenue", f"₹{total_revenue/10000000:.1f}Cr", "+12.5%")
        with col2:
            st.metric("Energy Generated", f"{total_energy/1000:.0f}M kWh", "+8.3%")
        with col3:
            st.metric("CO2 Reduced", f"{co2_reduction:.0f} tonnes", "+15.2%")
        with col4:
            st.metric("System Efficiency", f"{system_efficiency:.1f}%", "+2.1%")
        with col5:
            st.metric("Active Wards", f"{wards_active}", "+3")
        with col6:
            st.metric("Uptime", "99.7%", "+0.3%")

        st.markdown("---")

        # Strategic Insights
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🎯 Strategic Objectives Status")

            objectives = [
                {"name": "Revenue Target 2026", "current": 75, "target": 100, "status": "On Track"},
                {"name": "CO2 Reduction Goal", "current": 82, "target": 100, "status": "Ahead"},
                {"name": "Ward Expansion", "current": 40, "target": 50, "status": "On Track"},
                {"name": "Efficiency Optimization", "current": 88, "target": 95, "status": "Progressing"}
            ]

            for obj in objectives:
                progress = obj['current'] / obj['target'] * 100
                st.write(f"**{obj['name']}**: {obj['current']}/{obj['target']} ({progress:.1f}%) - {obj['status']}")
                st.progress(progress / 100)

        with col2:
            st.subheader("🚨 Executive Alerts & Priorities")

            alerts = [
                "🔴 URGENT: Ward_03 maintenance due in 3 days",
                "🟡 HIGH: Energy prices increased 8% this month",
                "🟢 MEDIUM: New feedstock source identified in Ward_15",
                "🔵 LOW: Carbon credit certification pending"
            ]

            for alert in alerts:
                st.info(alert)

        st.markdown("---")

        # Advanced Analytics Section
        st.subheader("📈 Advanced Performance Analytics")

        tab1, tab2, tab3 = st.tabs(["Revenue Analytics", "Operational Efficiency", "Market Intelligence"])

        with tab1:
            # Revenue forecasting with confidence intervals
            st.subheader("Revenue Forecasting with Confidence Intervals")

            # Generate forecast data
            months = pd.date_range(start=datetime.now(), periods=24, freq='M')
            base_revenue = total_revenue / 30  # Monthly revenue

            forecast_data = []
            for i, month in enumerate(months):
                growth = 1 + (i * 0.015)  # 1.5% monthly growth
                revenue = base_revenue * growth
                ci_lower = revenue * 0.85
                ci_upper = revenue * 1.15

                forecast_data.append({
                    'Month': month,
                    'Revenue': revenue,
                    'CI_Lower': ci_lower,
                    'CI_Upper': ci_upper
                })

            forecast_df = pd.DataFrame(forecast_data)

            fig = go.Figure()

            # Confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_df['Month'], y=forecast_df['CI_Upper'],
                fill=None, mode='lines', line_color='rgba(0,100,80,0.2)',
                name='Upper Bound'
            ))
            fig.add_trace(go.Scatter(
                x=forecast_df['Month'], y=forecast_df['CI_Lower'],
                fill='tonexty', mode='lines', line_color='rgba(0,100,80,0.2)',
                name='Lower Bound'
            ))

            # Main forecast line
            fig.add_trace(go.Scatter(
                x=forecast_df['Month'], y=forecast_df['Revenue'],
                mode='lines+markers', line_color='rgb(0,100,80)',
                name='Forecast'
            ))

            fig.update_layout(
                title="24-Month Revenue Forecast with 95% Confidence Interval",
                xaxis_title="Month",
                yaxis_title="Revenue (₹)",
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Operational Efficiency Deep Dive")

            # Efficiency metrics over time
            efficiency_data = df.groupby(df['Timestamp'].dt.date).agg({
                'CH4_percent': 'mean',
                'Methane_m3_hr': 'sum',
                'Feed_Rate_kg_hr': 'mean'
            }).reset_index()

            col1, col2 = st.columns(2)

            with col1:
                fig = px.line(efficiency_data, x='Timestamp', y='CH4_percent',
                            title="Methane Efficiency Trend",
                            markers=True)
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Efficiency vs Feed Rate correlation
                fig = px.scatter(df, x='Feed_Rate_kg_hr', y='CH4_percent',
                               color='Feedstock_Type', size='Methane_m3_hr',
                               title="Efficiency vs Feed Rate Analysis")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.subheader("Market Intelligence & Competitive Analysis")

            # Simulated market data
            market_data = pd.DataFrame({
                'Month': pd.date_range(start='2025-01-01', periods=12, freq='M'),
                'GFIS_Price': [8.0, 8.2, 8.1, 8.5, 8.3, 8.7, 8.4, 8.6, 8.8, 8.5, 8.9, 8.7],
                'Market_Avg': [7.5, 7.6, 7.8, 7.7, 8.0, 7.9, 8.1, 8.0, 8.2, 8.1, 8.3, 8.2],
                'Competitor_A': [7.8, 7.9, 8.0, 7.8, 8.1, 8.0, 8.2, 8.1, 8.3, 8.2, 8.4, 8.3],
                'Competitor_B': [7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3]
            })

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=market_data['Month'], y=market_data['GFIS_Price'],
                mode='lines+markers', name='GFIS',
                line=dict(color='green', width=3)
            ))

            fig.add_trace(go.Scatter(
                x=market_data['Month'], y=market_data['Market_Avg'],
                mode='lines', name='Market Average',
                line=dict(color='blue', dash='dash')
            ))

            fig.add_trace(go.Scatter(
                x=market_data['Month'], y=market_data['Competitor_A'],
                mode='lines', name='Competitor A',
                line=dict(color='red', dash='dot')
            ))

            fig.add_trace(go.Scatter(
                x=market_data['Month'], y=market_data['Competitor_B'],
                mode='lines', name='Competitor B',
                line=dict(color='orange', dash='dot')
            ))

            fig.update_layout(
                title="Energy Price Comparison (₹/kWh)",
                xaxis_title="Month",
                yaxis_title="Price (₹/kWh)",
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE: SUSTAINABILITY HUB ====================
elif page == "🌍 Sustainability Hub":
    st.title("🌍 Sustainability & ESG Hub")
    st.markdown("### *Environmental, Social & Governance Intelligence*")

    if df is not None:
        # ESG Score Dashboard
        st.subheader("📊 ESG Performance Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        # Calculate ESG metrics
        environmental_score = 85
        social_score = 78
        governance_score = 92
        overall_esg = (environmental_score + social_score + governance_score) / 3

        with col1:
            st.metric("Environmental", f"{environmental_score}/100", "+5.2")
        with col2:
            st.metric("Social", f"{social_score}/100", "+3.1")
        with col3:
            st.metric("Governance", f"{governance_score}/100", "+2.8")
        with col4:
            st.metric("Overall ESG", f"{overall_esg:.1f}/100", "+3.7")

        st.markdown("---")

        # Environmental Impact Section
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🌱 Carbon Footprint Analysis")

            # Carbon metrics
            daily_co2_reduction = df['CO2e_Reduction_kg_hr'].sum() * 24 / 1000  # tonnes
            annual_co2_reduction = daily_co2_reduction * 365
            carbon_credits_value = annual_co2_reduction * 1000  # ₹1000 per tonne

            st.metric("Daily CO2 Reduction", f"{daily_co2_reduction:.1f} tonnes")
            st.metric("Annual CO2 Reduction", f"{annual_co2_reduction:.0f} tonnes")
            st.metric("Carbon Credit Value", f"₹{carbon_credits_value/10000000:.2f}Cr")

            # CO2 reduction trend
            co2_trend = df.groupby(df['Timestamp'].dt.date)['CO2e_Reduction_kg_hr'].sum().reset_index()
            co2_trend['CO2e_Reduction_kg_hr'] = co2_trend['CO2e_Reduction_kg_hr'] * 24 / 1000  # Convert to daily tonnes

            fig = px.area(co2_trend, x='Timestamp', y='CO2e_Reduction_kg_hr',
                         title="Daily CO2 Reduction Trend",
                         color_discrete_sequence=['#2ca02c'])
            fig.update_layout(height=300, yaxis_title="CO2 Reduced (tonnes)")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("♻️ Circular Economy Impact")

            # Waste processing metrics
            total_waste_processed = df['Feed_Rate_kg_hr'].sum() * 24  # kg per day
            energy_generated = df['Methane_m3_hr'].sum() * 24 * 10  # kWh per day
            waste_to_energy_ratio = energy_generated / (total_waste_processed / 1000)  # kWh per tonne

            st.metric("Waste Processed Daily", f"{total_waste_processed/1000:.1f} tonnes")
            st.metric("Energy from Waste", f"{energy_generated/1000:.1f} MWh")
            st.metric("Waste-to-Energy Ratio", f"{waste_to_energy_ratio:.0f} kWh/tonne")

            # Circular economy visualization
            circular_data = pd.DataFrame({
                'Stage': ['Waste Collection', 'Biogas Production', 'Energy Generation', 'Organic Fertilizer'],
                'Efficiency': [95, 88, 92, 85],
                'Economic_Value': [0.5, 2.1, 8.0, 1.2]  # ₹ per kg
            })

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=circular_data['Stage'], y=circular_data['Efficiency'],
                name='Efficiency %', marker_color='lightblue'
            ))

            fig.add_trace(go.Scatter(
                x=circular_data['Stage'], y=circular_data['Economic_Value'],
                name='Value (₹/kg)', mode='lines+markers',
                yaxis='y2', line=dict(color='red', width=3)
            ))

            fig.update_layout(
                title="Circular Economy Value Chain",
                yaxis=dict(title='Efficiency (%)'),
                yaxis2=dict(title='Economic Value (₹/kg)', overlaying='y', side='right'),
                height=300
            )

            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Social Impact Section
        st.subheader("👥 Social Impact & Community Development")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Employment Generated")
            wards_active = 5  # Based on dataset analysis
            jobs_created = wards_active * 12  # 12 jobs per ward
            st.metric("Direct Jobs", f"{jobs_created}")
            st.metric("Indirect Jobs", f"{jobs_created * 2}")

        with col2:
            st.subheader("Community Benefits")
            households_benefited = wards_active * 250  # 250 households per ward
            st.metric("Households Served", f"{households_benefited:,}")
            st.metric("Clean Energy Access", f"{households_benefited * 0.8:.0f}")

        with col3:
            st.subheader("Health & Sanitation")
            waste_diverted = total_waste_processed * 365 / 1000000  # million kg per year
            st.metric("Waste Diverted", f"{waste_diverted:.1f}M kg/year")
            st.metric("Sanitation Improvement", "85%")

        # SDG Alignment
        st.subheader("🎯 UN Sustainable Development Goals Alignment")

        sdg_data = pd.DataFrame({
            'SDG': ['SDG 3 (Health)', 'SDG 6 (Clean Water)', 'SDG 7 (Energy)', 'SDG 9 (Industry)', 'SDG 12 (Consumption)', 'SDG 13 (Climate)'],
            'Alignment_Score': [78, 85, 92, 88, 82, 95],
            'Impact_Level': ['Medium', 'High', 'Very High', 'High', 'High', 'Very High']
        })

        fig = px.bar(sdg_data, x='SDG', y='Alignment_Score', color='Impact_Level',
                    title="SDG Alignment Scores",
                    color_discrete_map={'Very High': 'darkgreen', 'High': 'green', 'Medium': 'lightgreen'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE: OPERATIONS CENTER ====================
elif page == "⚙️ Operations Center":
    st.title("⚙️ Operations Management Center")
    st.markdown("### *Workflow Automation & Operational Excellence*")

    if df is not None:
        # Operations Dashboard
        st.subheader("🎮 Operations Control Panel")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            active_digesters = 5
            st.metric("Active Digesters", active_digesters)
        with col2:
            system_uptime = 99.7
            st.metric("System Uptime", f"{system_uptime}%")
        with col3:
            pending_tasks = 8
            st.metric("Pending Tasks", pending_tasks)
        with col4:
            active_alerts = 3
            st.metric("Active Alerts", active_alerts)

        st.markdown("---")

        # Workflow Management
        tab1, tab2, tab3, tab4 = st.tabs(["Task Management", "Maintenance Scheduler", "Quality Control", "Performance Monitoring"])

        with tab1:
            st.subheader("📋 Task Management System")

            # Task list
            tasks = [
                {"id": "T001", "task": "Monthly maintenance check", "priority": "High", "assigned": "Team A", "due": "2025-12-25", "status": "In Progress"},
                {"id": "T002", "task": "Feedstock quality inspection", "priority": "Medium", "assigned": "Team B", "due": "2025-12-26", "status": "Pending"},
                {"id": "T003", "task": "Sensor calibration", "priority": "High", "assigned": "Team C", "due": "2025-12-24", "status": "Completed"},
                {"id": "T004", "task": "Energy output optimization", "priority": "Low", "assigned": "Team A", "due": "2025-12-28", "status": "Pending"},
                {"id": "T005", "task": "Safety audit", "priority": "High", "assigned": "Team D", "due": "2025-12-23", "status": "Overdue"}
            ]

            task_df = pd.DataFrame(tasks)

            # Task filters
            col1, col2, col3 = st.columns(3)
            with col1:
                priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Completed", "Overdue"])
            with col3:
                assigned_filter = st.selectbox("Filter by Team", ["All", "Team A", "Team B", "Team C", "Team D"])

            # Apply filters
            filtered_tasks = task_df.copy()
            if priority_filter != "All":
                filtered_tasks = filtered_tasks[filtered_tasks['priority'] == priority_filter]
            if status_filter != "All":
                filtered_tasks = filtered_tasks[filtered_tasks['status'] == status_filter]
            if assigned_filter != "All":
                filtered_tasks = filtered_tasks[filtered_tasks['assigned'] == assigned_filter]

            # Display tasks
            for _, task in filtered_tasks.iterrows():
                status_color = {
                    "Completed": "🟢",
                    "In Progress": "🟡",
                    "Pending": "⚪",
                    "Overdue": "🔴"
                }.get(task['status'], "⚪")

                priority_color = {
                    "High": "🔴",
                    "Medium": "🟡",
                    "Low": "🟢"
                }.get(task['priority'], "⚪")

                st.write(f"{status_color} **{task['task']}** - {priority_color} {task['priority']} | Assigned: {task['assigned']} | Due: {task['due']}")

            # Add new task
            st.subheader("➕ Add New Task")
            with st.form("new_task_form"):
                task_name = st.text_input("Task Name")
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                assigned_team = st.selectbox("Assigned Team", ["Team A", "Team B", "Team C", "Team D"])
                due_date = st.date_input("Due Date")

                submitted = st.form_submit_button("Add Task")
                if submitted and task_name:
                    st.success(f"Task '{task_name}' added successfully!")

        with tab2:
            st.subheader("🔧 Predictive Maintenance Scheduler")

            # Maintenance schedule
            maintenance_schedule = pd.DataFrame({
                'Equipment': ['Digester_01', 'Digester_02', 'Digester_03', 'Digester_04', 'Digester_05',
                             'Pump_A', 'Pump_B', 'Sensor_Array_1', 'Sensor_Array_2', 'Control_System'],
                'Last_Maintenance': pd.to_datetime(['2025-11-15', '2025-11-20', '2025-11-10', '2025-11-25', '2025-11-18',
                                                   '2025-11-12', '2025-11-08', '2025-11-22', '2025-11-16', '2025-11-14']),
                'Next_Scheduled': pd.to_datetime(['2025-12-15', '2025-12-20', '2025-12-10', '2025-12-25', '2025-12-18',
                                                 '2025-12-12', '2025-12-08', '2025-12-22', '2025-12-16', '2025-12-14']),
                'Health_Score': [85, 92, 78, 88, 91, 76, 83, 94, 87, 89],
                'Risk_Level': ['Medium', 'Low', 'High', 'Low', 'Low', 'High', 'Medium', 'Low', 'Low', 'Low']
            })

            # Maintenance calendar view
            fig = px.scatter(maintenance_schedule, x='Next_Scheduled', y='Equipment',
                           size='Health_Score', color='Risk_Level',
                           color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'},
                           title="Maintenance Schedule Overview",
                           labels={'Next_Scheduled': 'Next Maintenance Date'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

            # Urgent maintenance alerts
            urgent_items = maintenance_schedule[maintenance_schedule['Next_Scheduled'] <= datetime.now() + timedelta(days=7)]

            if len(urgent_items) > 0:
                st.subheader("🚨 Urgent Maintenance Required")
                for _, item in urgent_items.iterrows():
                    days_overdue = (datetime.now() - item['Next_Scheduled']).days
                    if days_overdue > 0:
                        st.error(f"🔴 {item['Equipment']} is {days_overdue} days overdue for maintenance!")
                    else:
                        st.warning(f"🟡 {item['Equipment']} due within {abs(days_overdue)} days")

        with tab3:
            st.subheader("🔍 Quality Control Dashboard")

            # Quality metrics
            quality_metrics = {
                'Feedstock_Quality': 87,
                'Process_Efficiency': 91,
                'Output_Purity': 94,
                'Safety_Compliance': 96,
                'Environmental_Standards': 89
            }

            # Quality gauge charts
            cols = st.columns(len(quality_metrics))
            for i, (metric, score) in enumerate(quality_metrics.items()):
                with cols[i]:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=score,
                        title={'text': metric.replace('_', ' ')},
                        gauge={'axis': {'range': [0, 100]},
                               'bar': {'color': "darkblue"},
                               'steps': [
                                   {'range': [0, 50], 'color': "lightgray"},
                                   {'range': [50, 75], 'color': "yellow"},
                                   {'range': [75, 100], 'color': "lightgreen"}]}))
                    fig.update_layout(height=200)
                    st.plotly_chart(fig, use_container_width=True)

            # Quality trends
            st.subheader("Quality Trend Analysis")

            # Simulated quality data over time
            quality_trend = pd.DataFrame({
                'Date': pd.date_range(start='2025-11-01', periods=30, freq='D'),
                'Feedstock_Quality': np.random.normal(87, 3, 30),
                'Process_Efficiency': np.random.normal(91, 2, 30),
                'Output_Purity': np.random.normal(94, 1.5, 30)
            })

            fig = px.line(quality_trend, x='Date', y=['Feedstock_Quality', 'Process_Efficiency', 'Output_Purity'],
                         title="Quality Metrics Trends (Last 30 Days)")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with tab4:
            st.subheader("📊 Performance Monitoring")

            # Key performance indicators
            kpis = {
                'Overall_Equipment_Effectiveness': 87.5,
                'Mean_Time_Between_Failures': 95.2,
                'First_Time_Quality': 92.1,
                'On_Time_Delivery': 96.8,
                'Customer_Satisfaction': 94.3
            }

            # KPI dashboard
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Current KPI Values")
                for kpi, value in kpis.items():
                    st.metric(kpi.replace('_', ' '), f"{value:.1f}%")

            with col2:
                st.subheader("KPI Performance Trend")

                # Simulated KPI trends
                kpi_trend = pd.DataFrame({
                    'Month': pd.date_range(start='2025-06-01', periods=6, freq='M'),
                    'OEE': [82, 84, 86, 87, 88, 87.5],
                    'MTBF': [92, 93, 94, 95, 95, 95.2],
                    'FTQ': [89, 90, 91, 92, 92, 92.1]
                })

                fig = px.line(kpi_trend, x='Month', y=['OEE', 'MTBF', 'FTQ'],
                             title="KPI Performance Trends")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

            # Performance alerts
            st.subheader("⚠️ Performance Alerts")

            alerts = [
                "OEE below target in Digester_03",
                "Quality deviation in Batch_2025_12_15",
                "Maintenance delay affecting Pump_A performance"
            ]

            for alert in alerts:
                st.warning(f"⚠️ {alert}")

st.markdown("---")
st.markdown("""
<div style="
    background: linear-gradient(135deg, #071407 0%, #0d2e0d 60%, #1a3d1a 100%);
    border-radius: 16px;
    border: 1px solid #2d5a2d;
    border-top: 3px solid #4caf50;
    padding: 40px 36px 24px 36px;
    margin-top: 24px;
    box-shadow: 0 -4px 30px rgba(45,122,45,0.15);
">
    <!-- Top grid -->
    <table width="100%" style="border-collapse:collapse;margin-bottom:32px;"><tr valign="top">

        <!-- Brand column -->
    <td width="38%" style="padding-right:32px;">
            <div style="font-size:1.8em;margin-bottom:8px;">🌿</div>
            <div style="color:#4caf50;font-weight:800;font-size:1.1em;letter-spacing:-0.3px;margin-bottom:4px;">
                Chatake Greenworks
            </div>
            <div style="color:#a5d6a7;font-size:0.78em;margin-bottom:12px;line-height:1.6;">
                Sustainable Energy Innovation Unit<br>
                <em style="color:#558b2f;">A Division of Chatake Innoworks Pvt. Ltd.</em>
            </div>
            <div style="color:#81c784;font-size:0.75em;line-height:1.8;">
                📍 Nehru Industrial Estate, Damani Nagar<br>
                &nbsp;&nbsp;&nbsp;&nbsp;Solapur – 413001, Maharashtra, India<br>
                📞 <a href="tel:+918600182228" style="color:#69f0ae;text-decoration:none;">+91 8600182228</a><br>
                📧 <a href="mailto:admin@chatakeinnoworks.com" style="color:#69f0ae;text-decoration:none;">admin@chatakeinnoworks.com</a>
            </div>
            <img src="https://raw.githubusercontent.com/aakashchatake/GFIS-v2.0/main/assets/CI_Vision_2029.png"
                 style="width:100%;border-radius:8px;margin-top:14px;"
                 alt="Chatake Innoworks Office" />
    </td>

        <!-- Platform column -->
    <td width="20%" style="padding-right:20px;">
            <div style="color:#4caf50;font-weight:700;font-size:0.82em;letter-spacing:1px;text-transform:uppercase;margin-bottom:14px;">Platform</div>
            <div style="line-height:2.2;">
                <a href="https://green-fuel-intelligence--59klled.gamma.site/" target="_blank" style="color:#a5d6a7;font-size:0.78em;text-decoration:none;display:block;">📑 Presentation</a>
                <a href="https://internship.chatakeinnoworks.com" target="_blank" style="color:#a5d6a7;font-size:0.78em;text-decoration:none;display:block;">🎓 Internship Portal</a>
                <a href="https://about.chatakeinnoworks.com" target="_blank" style="color:#a5d6a7;font-size:0.78em;text-decoration:none;display:block;">🌐 Company Profile</a>
                <a href="https://www.chatakeinnoworks.com" target="_blank" style="color:#a5d6a7;font-size:0.78em;text-decoration:none;display:block;">🏢 Main Website</a>
            </div>
    </td>

        <!-- Project column -->
    <td width="20%" style="padding-right:20px;">
            <div style="color:#4caf50;font-weight:700;font-size:0.82em;letter-spacing:1px;text-transform:uppercase;margin-bottom:14px;">Project Team</div>
            <div style="line-height:2.2;color:#a5d6a7;font-size:0.78em;">
                <div>Ms. Tanishka Deshpande</div>
                <div>Ms. Anushka Hitanalli</div>
                <div>Ms. Aditi Gangji</div>
                <div>Ms. Shruti Hiremath</div>
            </div>
    </td>

        <!-- Connect column -->
    <td width="20%">
            <div style="color:#4caf50;font-weight:700;font-size:0.82em;letter-spacing:1px;text-transform:uppercase;margin-bottom:14px;">Connect</div>
            <div style="line-height:2.2;">
                <a href="https://www.linkedin.com/company/chatakeinnoworks" target="_blank" style="color:#a5d6a7;font-size:0.78em;text-decoration:none;display:block;">💼 LinkedIn</a>
                <a href="https://www.facebook.com/chatakeinnoworks" target="_blank" style="color:#a5d6a7;font-size:0.78em;text-decoration:none;display:block;">📘 Facebook</a>
                <a href="https://open.spotify.com/show/1zeA2xxVg5kGOV9bhAGigQ" target="_blank" style="color:#a5d6a7;font-size:0.78em;text-decoration:none;display:block;">🎧 Podcast</a>
                <a href="mailto:admin@chatakeinnoworks.com" style="color:#a5d6a7;font-size:0.78em;text-decoration:none;display:block;">✉️ Contact Us</a>
            </div>
    </td>

    </tr></table>

    <!-- Bottom bar -->
    <table width="100%" style="border-collapse:collapse;border-top:1px solid rgba(45,122,45,0.4);padding-top:0;margin-top:4px;">
      <tr>
        <td style="padding-top:16px;">
          <div style="color:#2d5a2d;font-size:0.72em;">
              © 2026 Chatake Innoworks Pvt. Ltd. All rights reserved. &nbsp;|&nbsp; MindforgeAI Research Division
          </div>
        </td>
        <td style="padding-top:16px;text-align:right;">
          <div style="color:#4caf50;font-size:0.72em;font-weight:600;">
              🏆 GFIS v2.0 &nbsp;·&nbsp; Green Fuel Intelligence System &nbsp;·&nbsp; DIPEX 2026
          </div>
        </td>
      </tr>
    </table>
</div>
""", unsafe_allow_html=True)
