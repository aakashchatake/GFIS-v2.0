# Quick Start Guide - GFIS v2.0

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd /Users/akashchatake/Downloads/Chatake-Innoworks-Organization/Projects/AgriVerse/GFIS/Bio-Fuel/gfis-pilot

pip install streamlit pandas numpy plotly scikit-learn xgboost scipy
```

### Step 2: Run the Enhanced Dashboard
```bash
streamlit run enhanced_dashboard.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open http://localhost:8501 in your browser! 🎉

---

## 📊 Explore the Dashboard

### Navigation Sidebar
Click the menu (☰) at top-left to access:

1. **🏠 Overview** - System status and key metrics
2. **📊 Real-time Monitoring** - Live digester data with charts
3. **🎯 Production Analytics** - Daily/monthly trends
4. **🤖 ML Predictions** - AI-powered forecasts
5. **🗺️ Geographic Analysis** - Ward-level maps
6. **⚡ Revenue Tracking** - Financial projections
7. **🔧 System Health** - Diagnostics & scores
8. **📈 Advanced Analytics** - Correlations & deep analysis

---

## 🔬 Generate Analysis Reports

### Comprehensive Data Analysis
```bash
python data_analyzer.py
```

**Output:** `gfis_analysis_report.json`

Contains:
- Detailed timeseries statistics
- Geographic analysis of all wards
- Yield dataset insights
- Correlation matrices
- Revenue potential calculations

---

## 🤖 Train ML Models

### Train Prediction Models
```bash
mkdir -p models
python ml_models.py
```

**Generates:**
- `models/yield_predictor.pkl` - XGBoost model
- `models/quality_classifier.pkl` - Random Forest model
- `models/revenue_forecast.json` - Revenue projections

---

## 🎲 Simulate IoT Data

### Generate Realistic Sensor Data
```bash
python iot_simulator.py
```

**Creates:**
- `simulated_iot_data_single.csv` - Single digester (14 days)
- `simulated_iot_data_multi.csv` - Multi-digester data (7 days)

Use these for testing dashboards and models!

---

## 📡 Integration Hub Demo

### Access Unified API
```bash
python integration_hub.py
```

**Provides:**
- Real-time metrics endpoint
- Daily summaries
- Geographic potential analysis
- Revenue projections
- Feedstock performance
- System health scores
- REST API endpoints (with FastAPI/Flask)

---

## 📈 Key Metrics You'll See

| Metric | Sample Value | Range |
|--------|--------------|-------|
| Temperature | 39.5°C | 35-55°C (optimal) |
| pH Level | 7.1 | 6.5-7.5 (optimal) |
| Methane Content | 56.2% | 50-62% |
| Methane Production | 24.8 m³/hr | Varies |
| Daily Production | 595 m³/day | ~500-700 m³ |
| Daily Revenue | ₹47,600 | Based on production |
| CO2 Reduction | 12.77 kg/m³ | - |

---

## 🎯 What Each Script Does

| Script | Purpose | Output |
|--------|---------|--------|
| `enhanced_dashboard.py` | Interactive 8-page dashboard | Web interface |
| `ml_models.py` | Train prediction models | Pickle files + metrics |
| `data_analyzer.py` | Analyze all datasets | JSON report |
| `iot_simulator.py` | Generate test data | CSV files |
| `integration_hub.py` | Unified data access | API interface |

---

## 🔧 Troubleshooting

### "Module not found" Error
```bash
pip install --upgrade streamlit pandas numpy plotly scikit-learn xgboost
```

### Dashboard Won't Load
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache

# Restart dashboard
streamlit run enhanced_dashboard.py
```

### CSV Files Not Found
Ensure you're running from the correct directory:
```bash
pwd  # Should show: .../gfis-pilot
ls *.csv  # Should see data files
```

---

## 📚 Data Files Available

Located in `../../Warehouse/`:
- `solapur_gfis_dataset.csv` - 1,002 ward records
- `gfis_biogas_dataset.csv` - 302 yield records
- `Biogas_Dataset_Rows.csv` - 302 hourly timeseries

All automatically loaded by scripts!

---

## 🎓 Next Steps

1. ✅ Run the dashboard
2. ✅ Explore all 8 pages
3. ✅ Generate analysis reports
4. ✅ Train ML models
5. ✅ Simulate IoT data
6. ✅ Check revenue projections

---

## 🚀 Deploy to Internet

### Streamlit Cloud (Easiest)
1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Select repository & main file
4. Deploy!

### Local Server
```bash
streamlit run enhanced_dashboard.py --server.port 80 --server.address 0.0.0.0
```

---

## 📞 Quick Help

| Question | Answer |
|----------|--------|
| How to change metrics? | Edit `enhanced_dashboard.py` |
| How to add new pages? | Duplicate page section, modify sidebar |
| How to use own data? | Replace CSV files in Warehouse/ |
| How to integrate with database? | Modify `integration_hub.py` |

---

**Version:** GFIS v2.0  
**Status:** Ready for Production ✅  
**Last Updated:** December 21, 2025

Happy exploring! 🌿
