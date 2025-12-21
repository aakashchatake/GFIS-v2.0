#!/bin/bash

# GFIS v2.0 Deployment Script
# Quick launch for the enhanced dashboard

echo "🚀 Starting GFIS v2.0 Enhanced Dashboard..."
echo "=========================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "
import sys
required = ['streamlit', 'pandas', 'numpy', 'plotly', 'xgboost']
missing = []
for pkg in required:
    try:
        __import__(pkg)
    except ImportError:
        missing.append(pkg)

if missing:
    print(f'❌ Missing packages: {missing}')
    print('Installing missing packages...')
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
    print('✅ Dependencies installed')
else:
    print('✅ All dependencies available')
"

# Check if data files exist
echo "📊 Checking data files..."
if [ ! -f "Warehouse/Biogas_Dataset_Rows.csv" ]; then
    echo "❌ Biogas_Dataset_Rows.csv not found in Warehouse/"
    exit 1
fi

if [ ! -f "Warehouse/solapur_gfis_dataset.csv" ]; then
    echo "❌ solapur_gfis_dataset.csv not found in Warehouse/"
    exit 1
fi

if [ ! -f "Warehouse/gfis_biogas_dataset.csv" ]; then
    echo "❌ gfis_biogas_dataset.csv not found in Warehouse/"
    exit 1
fi

echo "✅ All data files present"

# Launch the dashboard
echo ""
echo "🌟 Launching GFIS v2.0 Enhanced Dashboard..."
echo "=========================================="
echo "📊 Dashboard Features:"
echo "   • 11 comprehensive pages"
echo "   • Enterprise Suite with 5 modules"
echo "   • Executive Command Center"
echo "   • Sustainability & ESG Hub"
echo "   • Operations Management Center"
echo "   • Advanced analytics & AI predictions"
echo "   • Real-time monitoring & alerts"
echo ""
echo "🔗 Dashboard will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m streamlit run enhanced_dashboard.py --server.headless true --server.port 8501