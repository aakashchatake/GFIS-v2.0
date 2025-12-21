#!/usr/bin/env python3
"""
GFIS Requirements.txt Generator
Creates dependency list for deployment
"""

requirements = """# GFIS v2.0 - Green Fuel Intelligence System
# Core Dashboard & Visualization
streamlit==1.28.1
plotly==5.17.0
pandas==2.1.1
numpy==1.24.3

# Machine Learning & Data Science
scikit-learn==1.3.2
xgboost==2.0.1
scipy==1.11.3

# Data Processing
python-dateutil==2.8.2

# Web Framework (for API)
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.4.2

# Database (Optional)
# psycopg2-binary==2.9.9
# sqlalchemy==2.0.23

# Data Export
openpyxl==3.11.0
pyarrow==13.0.0

# Utilities
python-dotenv==1.0.0
requests==2.31.0
"""

if __name__ == "__main__":
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✓ requirements.txt created")
    print("\nTo install:")
    print("  pip install -r requirements.txt")
