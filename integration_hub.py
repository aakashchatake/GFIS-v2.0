"""
GFIS Integration Hub - API for Model Serving and Data Access
Provides unified interface for dashboards, models, and analytics
"""

import json
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path

class GFISIntegrationHub:
    """Unified integration point for all GFIS components"""
    
    def __init__(self, data_path='../../Warehouse'):
        self.data_path = Path(data_path)
        self.cache = {}
    
    def load_dataset(self, dataset_name, use_cache=True):
        """Load any dataset with optional caching"""
        
        if use_cache and dataset_name in self.cache:
            return self.cache[dataset_name]
        
        datasets = {
            'timeseries': 'Biogas_Dataset_Rows.csv',
            'locations': 'solapur_gfis_dataset.csv',
            'yield': 'gfis_biogas_dataset.csv'
        }
        
        if dataset_name not in datasets:
            raise ValueError(f"Unknown dataset: {dataset_name}")
        
        df = pd.read_csv(self.data_path / datasets[dataset_name])
        
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        if use_cache:
            self.cache[dataset_name] = df
        
        return df
    
    def get_realtime_metrics(self):
        """Get latest operational metrics"""
        df = self.load_dataset('timeseries')
        latest = df.iloc[-1].to_dict()
        
        return {
            'timestamp': str(latest['Timestamp']),
            'temperature_c': float(latest['Digester_Temp_C']),
            'ph_level': float(latest['pH']),
            'methane_percent': float(latest['CH4_percent']),
            'gas_flow_m3_hr': float(latest['Gas_Flow_m3_hr']),
            'methane_production_m3_hr': float(latest['Methane_m3_hr']),
            'feed_rate_kg_hr': float(latest['Feed_Rate_kg_hr']),
            'c_n_ratio': float(latest['C_N_Ratio']),
            'yield_status': latest['Yield_Status'],
            'co2_reduction_kg_hr': float(latest['CO2e_Reduction_kg_hr']),
            'feedstock_type': latest['Feedstock_Type'],
            'ward': latest['Ward']
        }
    
    def get_daily_summary(self):
        """Get today's operational summary"""
        df = self.load_dataset('timeseries')
        df['Date'] = df['Timestamp'].dt.date
        
        today = df['Date'].max()
        today_data = df[df['Date'] == today]
        
        if len(today_data) == 0:
            return None
        
        return {
            'date': str(today),
            'records': len(today_data),
            'temperature_avg_c': float(today_data['Digester_Temp_C'].mean()),
            'ph_avg': float(today_data['pH'].mean()),
            'methane_avg_percent': float(today_data['CH4_percent'].mean()),
            'methane_total_m3': float(today_data['Methane_m3_hr'].sum()),
            'co2_reduction_kg': float(today_data['CO2e_Reduction_kg_hr'].sum()),
            'feed_total_kg': float(today_data['Feed_Rate_kg_hr'].sum()),
            'normal_hours': int((today_data['Yield_Status'] == 'Normal').sum()),
            'warning_hours': int((today_data['Yield_Status'] == 'Warning').sum()),
            'critical_hours': int((today_data['Yield_Status'] == 'Critical').sum())
        }
    
    def get_geographic_potential(self, limit=10):
        """Get top wards by biogas potential"""
        df = self.load_dataset('locations')
        
        top_wards = df.nlargest(limit, 'estimated_biogas_m3_day')
        
        return [{
            'ward_id': int(row['ward_id']),
            'biogas_m3_day': float(row['estimated_biogas_m3_day']),
            'methane_percent': float(row['estimated_methane_pct']),
            'electricity_kwh_day': float(row['electricity_potential_kwh_day']),
            'co2_reduction_year': float(row['co2_reduction_tonnes_year']),
            'population': int(row['population']),
            'collection_efficiency': float(row['collection_efficiency_pct']),
            'latitude': float(row['latitude']),
            'longitude': float(row['longitude'])
        } for _, row in top_wards.iterrows()]
    
    def get_revenue_projection(self, days=30):
        """Project revenue for upcoming period"""
        df = self.load_dataset('timeseries')
        
        # Calculate average daily production
        df['Date'] = df['Timestamp'].dt.date
        daily_data = df.groupby('Date')['Methane_m3_hr'].sum()
        avg_daily_m3 = daily_data.mean()
        
        # Convert to revenue
        # 1 m³ CH4 = ~36 MJ = ~10 kWh
        daily_kwh = avg_daily_m3 * 10
        daily_revenue = daily_kwh * 8  # ₹8/kWh
        
        projections = {
            'period_days': days,
            'avg_daily_m3': float(avg_daily_m3),
            'avg_daily_kwh': float(daily_kwh),
            'avg_daily_revenue_inr': float(daily_revenue),
            'projected_revenue_inr': float(daily_revenue * days),
            'confidence_interval_pct': 15,
            'breakdowns': [
                {
                    'period': f'{i+1}-{i+1}',
                    'revenue_inr': float(daily_revenue)
                } for i in range(min(7, days))  # First week
            ]
        }
        
        return projections
    
    def get_feedstock_performance(self):
        """Compare performance across feedstock types"""
        df = self.load_dataset('timeseries')
        
        performance = []
        
        for feedstock in df['Feedstock_Type'].unique():
            subset = df[df['Feedstock_Type'] == feedstock]
            
            performance.append({
                'feedstock_type': feedstock,
                'count': len(subset),
                'avg_methane_m3_hr': float(subset['Methane_m3_hr'].mean()),
                'avg_ch4_percent': float(subset['CH4_percent'].mean()),
                'avg_temperature_c': float(subset['Digester_Temp_C'].mean()),
                'avg_ph': float(subset['pH'].mean()),
                'avg_feed_rate_kg_hr': float(subset['Feed_Rate_kg_hr'].mean()),
                'normal_percentage': float((subset['Yield_Status'] == 'Normal').sum() / len(subset) * 100)
            })
        
        return sorted(performance, key=lambda x: x['avg_methane_m3_hr'], reverse=True)
    
    def get_health_score(self):
        """Calculate overall system health score"""
        df = self.load_dataset('timeseries')
        latest = df.iloc[-1]
        
        score = 100
        issues = []
        
        # Temperature check
        if not (35 <= latest['Digester_Temp_C'] <= 55):
            score -= 20
            issues.append(f"Temperature {latest['Digester_Temp_C']:.1f}°C out of range")
        elif not (36 <= latest['Digester_Temp_C'] <= 42):
            score -= 10
            issues.append(f"Temperature {latest['Digester_Temp_C']:.1f}°C suboptimal")
        
        # pH check
        if not (6.5 <= latest['pH'] <= 7.5):
            score -= 20
            issues.append(f"pH {latest['pH']:.2f} out of range")
        elif not (6.8 <= latest['pH'] <= 7.3):
            score -= 10
            issues.append(f"pH {latest['pH']:.2f} suboptimal")
        
        # Methane check
        if latest['CH4_percent'] < 50:
            score -= 20
            issues.append(f"Methane {latest['CH4_percent']:.1f}% critically low")
        elif latest['CH4_percent'] < 55:
            score -= 10
            issues.append(f"Methane {latest['CH4_percent']:.1f}% below optimal")
        
        # C:N ratio check
        if not (20 <= latest['C_N_Ratio'] <= 30):
            score -= 10
            issues.append(f"C:N ratio {latest['C_N_Ratio']:.1f} out of range")
        
        # Status check
        if latest['Yield_Status'] == 'Critical':
            score -= 15
        elif latest['Yield_Status'] == 'Warning':
            score -= 5
        
        score = max(0, min(100, score))
        
        return {
            'score': score,
            'status': 'Excellent' if score >= 85 else 'Good' if score >= 70 else 'Fair' if score >= 50 else 'Poor',
            'issues': issues,
            'timestamp': str(latest['Timestamp'])
        }
    
    def export_data(self, dataset_name, format='csv', output_path=None):
        """Export dataset in specified format"""
        df = self.load_dataset(dataset_name)
        
        if format == 'csv':
            if output_path is None:
                output_path = f'export_{dataset_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            df.to_csv(output_path, index=False)
        elif format == 'json':
            if output_path is None:
                output_path = f'export_{dataset_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            df.to_json(output_path, orient='records', indent=2)
        
        return output_path
    
    def get_system_summary(self):
        """Get comprehensive system summary"""
        return {
            'realtime_metrics': self.get_realtime_metrics(),
            'daily_summary': self.get_daily_summary(),
            'health_score': self.get_health_score(),
            'top_wards': self.get_geographic_potential(5),
            'feedstock_performance': self.get_feedstock_performance(),
            'revenue_projection': self.get_revenue_projection(30)
        }


class APIServer:
    """REST API server for GFIS Integration Hub"""
    
    def __init__(self):
        self.hub = GFISIntegrationHub()
    
    def setup_endpoints(self, app):
        """Setup Flask/FastAPI endpoints"""
        
        @app.get('/api/health')
        def health():
            return {'status': 'ok', 'timestamp': datetime.now().isoformat()}
        
        @app.get('/api/realtime')
        def get_realtime():
            return self.hub.get_realtime_metrics()
        
        @app.get('/api/daily-summary')
        def get_daily():
            return self.hub.get_daily_summary()
        
        @app.get('/api/geographic-potential')
        def get_geographic(limit: int = 10):
            return self.hub.get_geographic_potential(limit)
        
        @app.get('/api/revenue-projection')
        def get_revenue(days: int = 30):
            return self.hub.get_revenue_projection(days)
        
        @app.get('/api/feedstock-performance')
        def get_feedstock():
            return self.hub.get_feedstock_performance()
        
        @app.get('/api/health-score')
        def get_health():
            return self.hub.get_health_score()
        
        @app.get('/api/system-summary')
        def get_summary():
            return self.hub.get_system_summary()


def demo():
    """Demonstrate integration hub capabilities"""
    print("\n" + "="*70)
    print("GFIS INTEGRATION HUB DEMO")
    print("="*70)
    
    hub = GFISIntegrationHub()
    
    print("\n[1] Real-time Metrics:")
    metrics = hub.get_realtime_metrics()
    print(f"    Temperature: {metrics['temperature_c']:.1f}°C")
    print(f"    pH: {metrics['ph_level']:.2f}")
    print(f"    Methane: {metrics['methane_percent']:.1f}%")
    print(f"    Production: {metrics['methane_production_m3_hr']:.2f} m³/hr")
    print(f"    Status: {metrics['yield_status']}")
    
    print("\n[2] Daily Summary:")
    daily = hub.get_daily_summary()
    if daily:
        print(f"    Date: {daily['date']}")
        print(f"    Records: {daily['records']}")
        print(f"    Methane Total: {daily['methane_total_m3']:.0f} m³")
        print(f"    Normal Hours: {daily['normal_hours']}")
    
    print("\n[3] Top Geographic Potential:")
    wards = hub.get_geographic_potential(5)
    for i, ward in enumerate(wards, 1):
        print(f"    {i}. Ward {ward['ward_id']}: {ward['biogas_m3_day']:.0f} m³/day")
    
    print("\n[4] Revenue Projection (30 days):")
    revenue = hub.get_revenue_projection(30)
    print(f"    Daily Avg: ₹{revenue['avg_daily_revenue_inr']:.0f}")
    print(f"    30-Day Total: ₹{revenue['projected_revenue_inr']:.0f}")
    
    print("\n[5] Health Score:")
    health = hub.get_health_score()
    print(f"    Score: {health['score']}/100")
    print(f"    Status: {health['status']}")
    if health['issues']:
        for issue in health['issues']:
            print(f"    - {issue}")
    
    print("\n[6] Feedstock Performance:")
    feedstock = hub.get_feedstock_performance()
    for i, fs in enumerate(feedstock[:3], 1):
        print(f"    {i}. {fs['feedstock_type']}: {fs['avg_methane_m3_hr']:.2f} m³/hr ({fs['normal_percentage']:.0f}% normal)")
    
    print("\n" + "="*70)
    print("Demo complete!")
    print("="*70)


if __name__ == "__main__":
    demo()
