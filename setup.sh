#!/bin/bash
# GFIS v2.0 - Installation & Deployment Script
# Green Fuel Intelligence System - DIPEX 2026

echo "=========================================="
echo "  GFIS v2.0 Setup & Deployment Script"
echo "=========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Navigate to project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "✓ Project directory: $PROJECT_DIR"
cd "$PROJECT_DIR"

# Create virtual environment
echo ""
echo "Step 1: Creating virtual environment..."
python3 -m venv gfis_env
source gfis_env/bin/activate
echo "✓ Virtual environment created"

# Install dependencies
echo ""
echo "Step 2: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create models directory
echo ""
echo "Step 3: Setting up directories..."
mkdir -p models
mkdir -p data_exports
echo "✓ Directories created"

# Verify data files
echo ""
echo "Step 4: Verifying data files..."
if [ -f "../../Warehouse/solapur_gfis_dataset.csv" ]; then
    echo "✓ solapur_gfis_dataset.csv found"
else
    echo "✗ solapur_gfis_dataset.csv NOT found"
fi

if [ -f "../../Warehouse/gfis_biogas_dataset.csv" ]; then
    echo "✓ gfis_biogas_dataset.csv found"
else
    echo "✗ gfis_biogas_dataset.csv NOT found"
fi

if [ -f "Biogas_Dataset_Rows.csv" ]; then
    echo "✓ Biogas_Dataset_Rows.csv found"
else
    echo "✗ Biogas_Dataset_Rows.csv NOT found (will be in parent/current dir)"
fi

# Final instructions
echo ""
echo "=========================================="
echo "  Setup Complete! ✓"
echo "=========================================="
echo ""
echo "To start the dashboard:"
echo "  source gfis_env/bin/activate"
echo "  streamlit run enhanced_dashboard.py"
echo ""
echo "Dashboard will open at: http://localhost:8501"
echo ""
echo "Other commands:"
echo "  python data_analyzer.py        # Generate analysis report"
echo "  python ml_models.py            # Train ML models"
echo "  python iot_simulator.py        # Generate test data"
echo "  python integration_hub.py      # Run API demo"
echo ""
