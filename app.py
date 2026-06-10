import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(
    page_title="India e-Governance Portal",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLES ---
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .title-text {
        font-size: 40px;
        font-weight: bold;
        color: #1a1a1a;
    }
    .feature-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .success-box {
        padding: 15px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    </style>
""", unsafe_allow_html=True)

# --- MOCK DATA ---
STATES_DATA = {
    "Maharashtra": {"cases": 1250, "hospitals": 450, "active": "Metro Phase 3"},
    "Delhi": {"cases": 980, "hospitals": 320, "active": "Swachh Bharat"},
    "Karnataka": {"cases": 1100, "hospitals": 380, "active": "Digital Bangalore"},
    "Tamil Nadu": {"cases": 900, "hospitals": 410, "active": "Tamil Nadu Vision"},
    "Uttar Pradesh": {"cases": 1500, "hospitals": 600, "active": "One District One Product"},
}

GOVT_JOBS = [
    {"post": "UPSC CSE 2024", "last_date": "2024-03-15", "qualification": "Graduate", "vacancies": 1105},
    {"post": "SSC CHSL", "last_date": "2024-04-01", "qualification": "12th Pass", "vacancies": 4500},
    {"post": "Railway NTPC", "last_date": "2024-04-10", "qualification": "Graduate", "vacancies": 3500},
    {"post": "Bank PO", "last_date": "2024-02-28", "qualification": "Graduate", "vacancies": 5000},
]

SCHEMES = [
    {"name": "PM Kisan", "amount": "₹6000/yr", "category": "Agriculture"},
    {"name": "Ayushman Bharat", "amount": "₹5L", "category": "Health"},
    {"name": "PM Awas Yojana", "amount": "₹1.5L", "category": "Housing"},
    {"name": "Beti Bachao", "amount": "Variable", "category": "Education"},
]

UNIVERSITIES = [
    {"name": "University of Delhi", "result_status": "Declared", "exam": "Semester 4"},
    {"name": "JNU", "result_status": "Pending", "exam": "Entrance 2024"},
]

INDIA_GDP = pd.DataFrame({
    "State": ["Maharashtra", "Tamil Nadu", "Uttar Pradesh", "Karnataka", "Gujarat"],
    "GDP": [380000, 280000, 240000, 230000, 200000],
    "Literacy": [84.8, 80.1, 69.7, 75.4, 78.0]
})

# --- SESSION STATE ---
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = 'Home'

# --- FUNCTIONS ---
def show_home():
    st.markdown("""
    <div class="main-header">
        <div class="title-text">🇮🇳 Digital India e-Governance</div>
        <div>One Nation - One Platform - One Solution</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Aadhaar Cards", "1.35B +")
    col2.metric("DigiLocker Docs", "650Cr +")
    col3.metric("Govt Schemes", "1500+")
    col4.metric("Digital Payments", "₹8000B")
    
    st.markdown("---")
    st.markdown("### 🖥️ Select Service")
    
    # Feature Grid Row 1
    cols = st.columns(4)
    features = [
        ("💰 Schemes", "Find Government Benefits", "Schemes"),
        ("📄 Documents", "Verify GST, PAN, Aadhaar", "Utilities"),
        ("💼 Jobs", "Sarkari Naukri Portal", "Jobs"),
        ("🧮 Tax", "Income Tax Calculator", "Tax")
    ]
    
    for i, (icon, desc, key) in enumerate(features):
        with cols[i]:
            st.markdown(f"""
            <div class="feature-card" style="text-align:center">
                <h3>{icon}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Go to {key}", key=f"nav_{key}"):
                st.session_state['active_tab'] = key
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2
    cols2 = st.columns(4)
    features2 = [
        ("🏥 Healthcare", "Hospitals & Insurance", "Healthcare"),
        ("🗳️ Jan Sewa", "File Grievances", "Grievance"),
        ("🎓 Education", "Verify Degrees", "Education"),
        ("🚛 Transport", "DL & Vehicle RC", "Transport")
    ]
    
    for i, (icon, desc, key) in enumerate(features2):
        with cols2[i]:
            st.markdown(f"""
            <div class="feature-card" style="text-align:center">
                <h3>{icon}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Go to {key}", key=f"nav_{key}"):
                st.session_state['active_tab'] = key
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 3
    cols3 = st.columns(3)
    features3 = [
        ("🗺️ GIS Map", "State Data Visualization", "GIS"),
        ("📁 Locker", "Digital Document Sync", "Locker"),
        ("⚠️ Disaster", "Weather Alerts", "Disaster")
    ]
    
    for i, (icon, desc, key) in enumerate(features3):
        with cols3[i]:
            st.markdown(f"""
            <div class="feature-card" style="text-align:center">
                <h3>{icon}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Go to {key}", key=f"nav_{key}"):
                st.session_state['active_tab'] = key
                st.rerun()

def show_schemes():
    st.title("💰 Government Schemes & Subsidies")
    st.markdown("### Find Eligible Benefits")
    
    col1, col2, col3 = st.columns(3)
    income = col1.number_input("Annual Income (₹)", 0, 5000000, 100000, 5000)
    age = col2.number_input("Age", 18, 100, 30)
    occupation = col3.selectbox("Occupation", ["Farmer", "Student", "Business", "Employee", "Unemployed"])
    
    if st.button("Find Eligible Schemes", type="primary"):
        for scheme in SCHEMES:
            with st.expander(f"{scheme['name']} ({scheme['category']})"):
                st.markdown(f"**Benefit:** {scheme['amount']}")
                st.markdown(f"**Eligibility:** {occupation}, Income < ₹{income:,}")
                st.button("Apply Now", key=f"apply_{scheme['name']}")

def show_utilities():
    st.title("📄 Document Verification")
    
    tabs = st.tabs(["GSTIN", "PAN", "Aadhaar", "Voter ID"])
    
    with tabs[0]:
        st.subheader("Verify GST Registration")
        gstin = st.text_input("Enter GSTIN", placeholder="27AAAAA1234A1A1")
        if st.button("Verify GST"):
            if len(gstin) == 15:
                st.markdown("""<div class="success-box"><b>✅ Verified</b><br>Legal Name: SAMPLE PVT LTD<br>Status: Active</div>""", unsafe_allow_html=True)
            else:
                st.error("Invalid GSTIN")
    
    with tabs[1]:
        st.subheader("Verify PAN")
        pan = st.text_input("Enter PAN").upper()
        if st.button("Verify PAN"):
            st.success("✅ Valid PAN - Linked to Aadhaar")
    
    with tabs[2]:
        st.subheader("Verify Aadhaar")
        aadhaar = st.text_input("Enter Aadhaar", max_length=12)
        if st.button("Verify Aadhaar"):
            if len(aadhaar) == 12:
                st.success("✅ Aadhaar Validated")
            else:
                st.error("Invalid Aadhaar")
    
    with tabs[3]:
        st.subheader("Voter ID Status")
        voter = st.text_input("Enter EPIC No").upper()
        if st.button("Check Voter"):
            st.success("✅ Voter ID Active")

def show_jobs():
    st.title("💼 Sarkari Naukri Portal")
    st.markdown("### Latest Government Jobs")
    
    col1, col2 = st.columns(2)
    qual = col1.selectbox("Qualification", ["10th", "12th", "Graduate", "Post Graduate"])
    dept = col2.selectbox("Department", ["UPSC", "SSC", "Railway", "Banking"])
    
    for job in GOVT_JOBS:
        with st.expander(f"📌 {job['post']}"):
            st.markdown(f"**Qualification:** {job['qualification']}")
            st.markdown(f"**Vacancies:** {job['vacancies']}")
            st.markdown(f"**Last Date:** {job['last_date']}")
            st.button("Apply Now", key=f"job_{job['post']}")
    
    st.markdown("---")
    st.subheader("📊 Application Stats")
    fig = px.bar(INDIA_GDP, x='State', y='GDP', title="State-wise Job Statistics")
    st.plotly_chart(fig)

def show_tax():
    st.title("🧮 Income Tax Calculator")
    st.markdown("Calculate Your Tax Liability")
    
    col1, col2 = st.columns(2)
    income = col1.number_input("Annual Income (₹)", 0, 100000000, 500000, 10000)
    age = col2.number_input("Age", 18, 100, 30)
    
    reg = 25000 if age < 60 else 50000 if age < 80 else 100000
    
    taxable = max(0, income - reg)
    
    if taxable < 250000:
        tax = 0
    elif taxable < 500000:
        tax = (taxable - 250000) * 0.05
    elif taxable < 1000000:
        tax = 12500 + (taxable - 500000) * 0.20
    else:
        tax = 112500 + (taxable - 1000000) * 0.30
    
    if st.button("Calculate Tax"):
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Gross Income", f"₹{income:,}")
        col2.metric("Deductions", f"₹{reg:,}")
        col3.metric("Tax Payable", f"₹{int(tax):,}")
        
        if tax > 0:
            st.info("💡 Tip: Invest in NPS, PPF, or Health Insurance to claim deductions under 80C!")

def show_healthcare():
    st.title("🏥 Healthcare Services")
    
    st.markdown("### Find Hospital & Insurance")
    
    col1, col2, col3 = st.columns(3)
    state = col1.selectbox("State", list(STATES_DATA.keys()))
    pin = col2.text_input("PIN Code")
    service = col3.selectbox("Service", ["General", "ICU", "Cardiac", "Cancer"])
    
    if st.button("Search Hospitals"):
        num = STATES_DATA[state]["hospitals"]
        st.markdown(f"Found **{num}** hospitals in {state} for {service}")
        
    st.markdown("---")
    st.markdown("### Ayushman Bharat Claim Status")
    ack = st.text_input("Enter Acknowledge No")
    if st.button("Check Claim"):
        st.success("🟢 Claim Sanctioned - ₹2,50,000 approved")

def show_grievance():
    st.title("🗳️ Jan Sewa - File Grievance")
    
    st.markdown("### Submit Your Complaint")
    
    col1, col2 = st.columns(2)
    name = col1.text_input("Full Name")
    mobile = col2.text_input("Mobile Number", max_length=10)
    
    category = st.selectbox("Category", ["Land & Revenue", "Police", "Tax & Revenue", "Medical", "Education"])
    desc = st.text_area("Complaint Description")
    
    if st.button("Submit Grievance"):
        st.success("✅ Grievance Submitted - Reference ID: JAN/2024/" + str(random.randint(10000, 99999)))

def show_education():
    st.title("🎓 Education Services")
    
    tabs = st.tabs(["University Results", "Degree Verification", "Scholarships"])
    
    with tabs[0]:
        st.markdown("### Check University Results")
        uni = st.selectbox("University", [u["name"] for u in UNIVERSITIES])
        if st.button("Check Result"):
            for u in UNIVERSITIES:
                if u["name"] == uni:
                    st.markdown(f"**Status:** {u['result_status']}")
                    st.markdown(f"**Exam:** {u['exam']}")
    
    with tabs[1]:
        st.markdown("### Verify Degree")
        uni_name = st.text_input("University Name")
        roll = st.text_input("Roll Number")
        if st.button("Verify Degree"):
            st.success("✅ Degree Verified - Authentic")
    
    with tabs[2]:
        st.markdown("### Apply for Scholarships")
        st.info("National Scholarship Portal - Applications Open!")
        st.button("Apply Now")

def show_transport():
    st.title("🚛 Transport Services")
    st.markdown("### Driving License & Vehicle RC")
    
    tabs = st.tabs(["DL Status", "RC Status", "e-Challan"])
    
    with tabs[0]:
        st.subheader("Check DL Status")
        dl = st.text_input("Enter License No")
        dob = st.date_input("Date of Birth")
        if st.button("Check DL"):
            st.success("✅ License Valid - Non-Transport")
    
    with tabs[1]:
        st.subheader("Vehicle RC Status")
        reg = st.text_input("Vehicle Registration No")
        if st.button("Check RC"):
            st.success("✅ RC Valid - Tax Paid")
    
    with tabs[2]:
        st.subheader("Pay e-Challan")
        chic = st.text_input("Challan No")
        if st.button("Pay Challan"):
            st.success("✅ Payment Successful")

def show_gis():
    st.title("🗺️ GIS & Data Visualization")
    
    option = st.selectbox("Select Data", ["State GDP", "Literacy Rate", "Health Infrastructure"])
    
    if option == "State GDP":
        fig = px.bar(INDIA_GDP, x='State', y='GDP', title="State-wise GDP", color='GDP')
        st.plotly_chart(fig)
    elif option == "Literacy Rate":
        fig = px.scatter(INDIA_GDP, x='State', y='Literacy', size='Literacy', color='State', title="Literacy Rate")
        st.plotly_chart(fig)
    
    st.markdown("### 🗺️ Interactive Map")
    map_data = pd.DataFrame({
        "City": ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"],
        "Lat": [28.6, 19.0, 12.9, 13.0, 22.5],
        "Lon": [77.2, 72.8, 77.5, 80.2, 88.3]
    })
    st.map(map_data, latitude='Lat', longitude='Lon', zoom=3)

def show_locker():
    st.title("📁 Digital Locker")
    st.markdown("### Access Your Documents")
    
    col1, col2 = st.columns(2)
    col1.info("📄 Aadhaar Card - Synced")
    col2.info("📄 PAN Card - Synced")
    
    st.markdown("#### Upload New Document")
    uploaded = st.file_uploader("Choose File", type=['pdf',
