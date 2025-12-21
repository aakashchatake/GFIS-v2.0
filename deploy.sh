#!/bin/bash

# GFIS v2.0 - Automated Deployment Script
# Supports multiple cloud platforms

echo "🚀 GFIS v2.0 Deployment Script"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if required files exist
check_files() {
    print_info "Checking deployment files..."

    files=("enhanced_dashboard.py" "requirements.txt" "Warehouse/Biogas_Dataset_Rows.csv" "Warehouse/solapur_gfis_dataset.csv" "Warehouse/gfis_biogas_dataset.csv")

    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            print_status "$file found"
        else
            print_error "$file missing"
            exit 1
        fi
    done
}

# Test local functionality
test_local() {
    print_info "Testing local functionality..."

    # Test Python imports
    python3 -c "
import sys
try:
    import streamlit, pandas, numpy, plotly, xgboost, sklearn
    print('✅ All Python dependencies available')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    sys.exit(1)
"

    # Test data loading
    python3 -c "
import pandas as pd
try:
    df = pd.read_csv('Warehouse/Biogas_Dataset_Rows.csv')
    location_df = pd.read_csv('Warehouse/solapur_gfis_dataset.csv')
    yield_df = pd.read_csv('Warehouse/gfis_biogas_dataset.csv')
    print(f'✅ Data loading successful: {len(df)} main + {len(location_df)} location + {len(yield_df)} yield records')
except Exception as e:
    print(f'❌ Data loading failed: {e}')
    import sys
    sys.exit(1)
"
}

# Deploy to Streamlit Cloud
deploy_streamlit() {
    print_info "Streamlit Cloud Deployment Guide:"
    echo ""
    echo "1. Go to https://share.streamlit.io"
    echo "2. Connect your GitHub account"
    echo "3. Select your GFIS repository"
    echo "4. Set main file path: enhanced_dashboard.py"
    echo "5. Click 'Deploy'"
    echo ""
    print_status "Repository ready for Streamlit Cloud deployment"
}

# Deploy to Heroku
deploy_heroku() {
    print_info "Heroku Deployment:"

    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        print_warning "Heroku CLI not found. Install from: https://devcenter.heroku.com/articles/heroku-cli"
        return
    fi

    # Create Procfile if it doesn't exist
    if [ ! -f "Procfile" ]; then
        echo "web: streamlit run enhanced_dashboard.py --server.port \$PORT --server.headless true" > Procfile
        print_status "Procfile created"
    fi

    echo "Run these commands:"
    echo "heroku create your-gfis-app-name"
    echo "git push heroku main"
    echo ""
    print_status "Ready for Heroku deployment"
}

# Deploy to Railway
deploy_railway() {
    print_info "Railway Deployment:"
    echo ""
    echo "1. Go to https://railway.app"
    echo "2. Connect your GitHub repository"
    echo "3. Set build command: pip install -r requirements.txt"
    echo "4. Set start command: streamlit run enhanced_dashboard.py --server.port \$PORT --server.headless true"
    echo ""
    print_status "Railway deployment configuration ready"
}

# Deploy to Render
deploy_render() {
    print_info "Render Deployment:"
    echo ""
    echo "1. Go to https://render.com"
    echo "2. Connect your GitHub repository"
    echo "3. Set build command: pip install -r requirements.txt"
    echo "4. Set start command: streamlit run enhanced_dashboard.py --server.port \$PORT --server.headless true"
    echo ""
    print_status "Render deployment configuration ready"
}

# Main menu
show_menu() {
    echo ""
    echo "Select deployment platform:"
    echo "1. Streamlit Cloud (Recommended)"
    echo "2. Heroku"
    echo "3. Railway"
    echo "4. Render"
    echo "5. Test Local Setup"
    echo "6. Exit"
    echo ""
    read -p "Enter choice (1-6): " choice

    case $choice in
        1)
            deploy_streamlit
            ;;
        2)
            deploy_heroku
            ;;
        3)
            deploy_railway
            ;;
        4)
            deploy_render
            ;;
        5)
            test_local
            ;;
        6)
            print_info "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid choice"
            show_menu
            ;;
    esac
}

# Main execution
main() {
    check_files
    print_status "All required files present"

    echo ""
    print_info "GFIS v2.0 - Enterprise Biogas Intelligence Dashboard"
    print_info "Ready for deployment to cloud platforms"
    echo ""

    show_menu
}

# Run main function
main