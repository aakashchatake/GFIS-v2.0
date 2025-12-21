"""
GFIS ML Models - Biogas Yield Prediction & Analysis
Green Fuel Intelligence System
DIPEX 2026 Submission
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, accuracy_score, classification_report
import xgboost as xgb
import pickle
import json
from datetime import datetime

class BioGasYieldPredictor:
    """
    ML Model to predict biogas yield based on operational parameters
    Trained on Biogas_Dataset_Rows.csv time-series data
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
        self.performance_metrics = {}
    
    def prepare_data(self, df):
        """Prepare data for model training"""
        # Feature engineering
        df = df.copy()
        
        # Create additional features
        df['Temp_pH_Interaction'] = df['Digester_Temp_C'] * df['pH']
        df['Feed_Per_Hour'] = df['Feed_Rate_kg_hr']
        df['Hourly_Capacity'] = df['Feed_Rate_kg_hr'] / 100
        df['CH4_CO2_Ratio'] = df['CH4_percent'] / (100 - df['CH4_percent'] + 0.1)
        
        # Encode categorical variables
        le = LabelEncoder()
        df['Feedstock_Encoded'] = le.fit_transform(df['Feedstock_Type'])
        df['Ward_Encoded'] = le.fit_transform(df['Ward'])
        df['Status_Encoded'] = df['Yield_Status'].map({'Normal': 1, 'Warning': 0.5, 'Critical': 0})
        
        return df, le
    
    def train_yield_predictor(self, df):
        """Train XGBoost model for methane yield prediction"""
        print("[*] Preparing data for yield prediction...")
        df_prepared, le = self.prepare_data(df)
        
        # Features and target
        feature_cols = ['Digester_Temp_C', 'pH', 'Feed_Rate_kg_hr', 'C_N_Ratio', 
                       'Gas_Flow_m3_hr', 'CH4_percent', 'Feedstock_Encoded', 
                       'Temp_pH_Interaction', 'CH4_CO2_Ratio']
        
        X = df_prepared[feature_cols]
        y = df_prepared['Methane_m3_hr']  # Target: hourly methane production
        
        print(f"[+] Features shape: {X.shape}")
        print(f"[+] Target shape: {y.shape}")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train XGBoost model
        print("[*] Training XGBoost Regressor...")
        self.model = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            objective='reg:squarederror'
        )
        
        self.model.fit(X_train, y_train, 
                      eval_set=[(X_test, y_test)],
                      verbose=False)
        
        # Evaluation
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        self.performance_metrics = {
            'train_r2': r2_score(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'test_mae': mean_absolute_error(y_test, y_pred_test)
        }
        
        print("\n[+] Model Performance:")
        print(f"    Train R²: {self.performance_metrics['train_r2']:.4f}")
        print(f"    Test R²: {self.performance_metrics['test_r2']:.4f}")
        print(f"    Test RMSE: {self.performance_metrics['test_rmse']:.4f} m³/hr")
        print(f"    Test MAE: {self.performance_metrics['test_mae']:.4f} m³/hr")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'Feature': feature_cols,
            'Importance': self.model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        print("\n[+] Top Features:")
        for idx, row in feature_importance.head(5).iterrows():
            print(f"    {row['Feature']}: {row['Importance']:.4f}")
        
        self.feature_names = feature_cols
        return self.model, self.performance_metrics
    
    def predict(self, data_dict):
        """Make prediction for new data"""
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        # Prepare input
        features = np.array([data_dict[f] for f in self.feature_names]).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        return prediction


class FeedstockQualityClassifier:
    """
    ML Model to classify feedstock quality and digester conditions
    Binary classification: Optimal (A/B) vs Suboptimal (C)
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.performance_metrics = {}
    
    def create_quality_label(self, row):
        """Create quality grade based on conditions"""
        if (row['CH4_percent'] >= 57 and 
            37 <= row['Digester_Temp_C'] <= 41 and 
            6.9 <= row['pH'] <= 7.3):
            return 'A'  # Optimal
        elif (row['CH4_percent'] >= 54 and 
              35 <= row['Digester_Temp_C'] <= 42 and 
              6.7 <= row['pH'] <= 7.4):
            return 'B'  # Good
        else:
            return 'C'  # Suboptimal
    
    def train_quality_classifier(self, df):
        """Train Random Forest for quality classification"""
        print("\n[*] Training Feedstock Quality Classifier...")
        
        df = df.copy()
        
        # Create quality labels
        df['Quality_Grade'] = df.apply(self.create_quality_label, axis=1)
        
        # Binary classification: A/B vs C
        df['Quality_Binary'] = (df['Quality_Grade'] != 'C').astype(int)
        
        # Features
        feature_cols = ['Digester_Temp_C', 'pH', 'CH4_percent', 'Feed_Rate_kg_hr',
                       'C_N_Ratio', 'Gas_Flow_m3_hr', 'Methane_m3_hr']
        
        X = df[feature_cols]
        y = df['Quality_Binary']
        
        # Scale
        X_scaled = self.scaler.fit_transform(X)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        self.performance_metrics = {
            'train_accuracy': accuracy_score(y_train, y_pred_train),
            'test_accuracy': accuracy_score(y_test, y_pred_test)
        }
        
        print(f"[+] Train Accuracy: {self.performance_metrics['train_accuracy']:.4f}")
        print(f"[+] Test Accuracy: {self.performance_metrics['test_accuracy']:.4f}")
        
        return self.model, self.performance_metrics
    
    def classify(self, data_dict):
        """Classify quality for new data"""
        if self.model is None:
            raise ValueError("Model not trained!")
        
        feature_cols = ['Digester_Temp_C', 'pH', 'CH4_percent', 'Feed_Rate_kg_hr',
                       'C_N_Ratio', 'Gas_Flow_m3_hr', 'Methane_m3_hr']
        
        features = np.array([data_dict[f] for f in feature_cols]).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        
        pred_proba = self.model.predict_proba(features_scaled)[0]
        
        return {
            'optimal_prob': pred_proba[1],
            'suboptimal_prob': pred_proba[0],
            'recommendation': 'Continue current operations' if pred_proba[1] > 0.7 else 'Optimize parameters'
        }


class RevenueForecaster:
    """
    Time-series forecasting for revenue based on biogas production
    """
    
    def __init__(self):
        self.model = None
        self.daily_data = None
    
    def prepare_daily_data(self, df):
        """Convert hourly to daily data"""
        df = df.copy()
        df['Date'] = df['Timestamp'].dt.date
        
        daily = df.groupby('Date').agg({
            'Methane_m3_hr': 'sum',
            'Methane_kg_hr': 'sum',
            'CO2e_Reduction_kg_hr': 'sum',
            'CH4_percent': 'mean',
            'Digester_Temp_C': 'mean',
            'pH': 'mean'
        }).reset_index()
        
        # Assume: 1 m³ methane = 10 kWh electric energy
        # Assume: 1 kWh = ₹8 (average market rate)
        daily['Daily_KWh'] = daily['Methane_m3_hr'] * 10
        daily['Daily_Revenue_INR'] = daily['Daily_KWh'] * 8
        
        self.daily_data = daily
        return daily
    
    def forecast_revenue(self, days_ahead=30):
        """Simple moving average forecast"""
        if self.daily_data is None:
            raise ValueError("Daily data not prepared!")
        
        # Calculate trend
        recent_revenue = self.daily_data['Daily_Revenue_INR'].tail(30).mean()
        
        # Simple forecast
        forecast = {
            'daily_avg': recent_revenue,
            'monthly_forecast': recent_revenue * days_ahead,
            'yearly_forecast': recent_revenue * 365,
            'confidence_interval': recent_revenue * 0.15  # ±15%
        }
        
        print("\n[+] Revenue Forecast (Next 30 Days):")
        print(f"    Daily Average: ₹{forecast['daily_avg']:.2f}")
        print(f"    Monthly Projection: ₹{forecast['monthly_forecast']:.2f}")
        print(f"    Yearly Projection: ₹{forecast['yearly_forecast']:.2f}")
        print(f"    Confidence Interval: ±₹{forecast['confidence_interval']:.2f}")
        
        return forecast


class DataAnalyzer:
    """Comprehensive statistical analysis of biogas datasets"""
    
    @staticmethod
    def analyze_dataset(df):
        """Generate comprehensive dataset analysis"""
        print("\n" + "="*60)
        print("DATASET ANALYSIS REPORT")
        print("="*60)
        
        print(f"\n[+] Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"[+] Date Range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
        print(f"[+] Duration: {(df['Timestamp'].max() - df['Timestamp'].min()).days} days")
        
        print("\n[+] Key Statistics:")
        print(f"    Temperature: {df['Digester_Temp_C'].mean():.2f}°C (±{df['Digester_Temp_C'].std():.2f})")
        print(f"    pH: {df['pH'].mean():.2f} (±{df['pH'].std():.2f})")
        print(f"    Methane %: {df['CH4_percent'].mean():.2f}% (±{df['CH4_percent'].std():.2f})")
        print(f"    Methane Yield: {df['Methane_m3_hr'].mean():.2f} m³/hr (±{df['Methane_m3_hr'].std():.2f})")
        
        print("\n[+] Feedstock Distribution:")
        for feedstock, count in df['Feedstock_Type'].value_counts().items():
            pct = (count / len(df)) * 100
            print(f"    {feedstock}: {count} samples ({pct:.1f}%)")
        
        print("\n[+] Yield Status Distribution:")
        for status, count in df['Yield_Status'].value_counts().items():
            pct = (count / len(df)) * 100
            print(f"    {status}: {count} samples ({pct:.1f}%)")
        
        print("\n[+] Missing Values:")
        missing = df.isnull().sum()
        if missing.sum() > 0:
            print(missing[missing > 0])
        else:
            print("    None - Dataset is complete!")
        
        print("\n" + "="*60)
    
    @staticmethod
    def analyze_locations(df):
        """Analyze geographic data"""
        print("\n" + "="*60)
        print("GEOGRAPHIC ANALYSIS REPORT")
        print("="*60)
        
        print(f"\n[+] Total Wards: {len(df)}")
        print(f"[+] Total Population Covered: {df['population'].sum():,.0f}")
        print(f"[+] Total Households: {df['households'].sum():,.0f}")
        
        print(f"\n[+] Biogas Potential:")
        print(f"    Total Daily: {df['estimated_biogas_m3_day'].sum():,.0f} m³")
        print(f"    Average per Ward: {df['estimated_biogas_m3_day'].mean():,.0f} m³")
        print(f"    Peak Ward: {df['estimated_biogas_m3_day'].max():,.0f} m³")
        
        print(f"\n[+] Electricity Generation Potential:")
        print(f"    Total Daily: {df['electricity_potential_kwh_day'].sum():,.0f} kWh")
        print(f"    Average per Ward: {df['electricity_potential_kwh_day'].mean():,.0f} kWh")
        
        print(f"\n[+] CO2 Reduction Potential:")
        print(f"    Total Yearly: {df['co2_reduction_tonnes_year'].sum():,.0f} tonnes")
        
        print("\n" + "="*60)


def main():
    """Main execution pipeline"""
    print("\n" + "="*60)
    print("GFIS ML MODELS - TRAINING PIPELINE")
    print("Green Fuel Intelligence System v2.0")
    print("="*60)
    
    # Load data
    print("\n[*] Loading datasets...")
    df_timeseries = pd.read_csv('Biogas_Dataset_Rows.csv')
    df_locations = pd.read_csv('../../Warehouse/solapur_gfis_dataset.csv')
    df_yield = pd.read_csv('../../Warehouse/gfis_biogas_dataset.csv')
    
    df_timeseries['Timestamp'] = pd.to_datetime(df_timeseries['Timestamp'])
    
    print(f"[+] Loaded {len(df_timeseries)} hourly records")
    print(f"[+] Loaded {len(df_locations)} ward records")
    print(f"[+] Loaded {len(df_yield)} yield records")
    
    # Analyze datasets
    DataAnalyzer.analyze_dataset(df_timeseries)
    DataAnalyzer.analyze_locations(df_locations)
    
    # Train Yield Predictor
    print("\n[*] Training Biogas Yield Predictor...")
    yield_predictor = BioGasYieldPredictor()
    yield_predictor.train_yield_predictor(df_timeseries)
    
    # Train Quality Classifier
    quality_classifier = FeedstockQualityClassifier()
    quality_classifier.train_quality_classifier(df_timeseries)
    
    # Prepare Revenue Forecaster
    print("\n[*] Preparing Revenue Forecaster...")
    revenue_forecaster = RevenueForecaster()
    daily_data = revenue_forecaster.prepare_daily_data(df_timeseries)
    revenue_forecast = revenue_forecaster.forecast_revenue(30)
    
    # Save models
    print("\n[*] Saving models...")
    with open('models/yield_predictor.pkl', 'wb') as f:
        pickle.dump({
            'model': yield_predictor.model,
            'scaler': yield_predictor.scaler,
            'features': yield_predictor.feature_names,
            'metrics': yield_predictor.performance_metrics
        }, f)
    
    with open('models/quality_classifier.pkl', 'wb') as f:
        pickle.dump({
            'model': quality_classifier.model,
            'scaler': quality_classifier.scaler,
            'metrics': quality_classifier.performance_metrics
        }, f)
    
    # Save forecasts
    with open('models/revenue_forecast.json', 'w') as f:
        json.dump(revenue_forecast, f, indent=2)
    
    print("[+] Models saved to models/ directory")
    
    # Example predictions
    print("\n[*] Example Predictions:")
    print("="*60)
    
    test_sample = {
        'Digester_Temp_C': 39.5,
        'pH': 7.1,
        'Feed_Rate_kg_hr': 500,
        'C_N_Ratio': 25,
        'Gas_Flow_m3_hr': 45,
        'CH4_percent': 57,
        'Feedstock_Encoded': 0,
        'Temp_pH_Interaction': 39.5 * 7.1,
        'CH4_CO2_Ratio': 57 / 43
    }
    
    predicted_yield = yield_predictor.predict(test_sample)
    print(f"[+] Predicted Methane Yield: {predicted_yield:.2f} m³/hr")
    print(f"[+] Daily Projection: {predicted_yield * 24:.2f} m³/day")
    print(f"[+] Revenue Projection: ₹{predicted_yield * 24 * 80:.2f}/day")
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()
