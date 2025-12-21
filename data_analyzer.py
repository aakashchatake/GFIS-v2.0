#!/usr/bin/env python3
"""
GFIS Comprehensive Data Analysis Pipeline
Analyzes all biogas datasets and generates insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
from pathlib import Path

class GFISDataAnalyzer:
    """Comprehensive analysis of GFIS datasets"""
    
    def __init__(self):
        self.analysis_results = {}
        self.datasets = {}
    
    def load_all_datasets(self):
        """Load all available datasets"""
        print("Loading datasets...")
        
        try:
            self.datasets['timeseries'] = pd.read_csv('Biogas_Dataset_Rows.csv')
            self.datasets['timeseries']['Timestamp'] = pd.to_datetime(
                self.datasets['timeseries']['Timestamp']
            )
            print(f"✓ Loaded timeseries data: {self.datasets['timeseries'].shape}")
        except Exception as e:
            print(f"✗ Error loading timeseries: {e}")
        
        try:
            self.datasets['locations'] = pd.read_csv('../../Warehouse/solapur_gfis_dataset.csv')
            print(f"✓ Loaded location data: {self.datasets['locations'].shape}")
        except Exception as e:
            print(f"✗ Error loading locations: {e}")
        
        try:
            self.datasets['yield'] = pd.read_csv('../../Warehouse/gfis_biogas_dataset.csv')
            print(f"✓ Loaded yield data: {self.datasets['yield'].shape}")
        except Exception as e:
            print(f"✗ Error loading yield: {e}")
    
    def analyze_timeseries(self):
        """Detailed timeseries analysis"""
        df = self.datasets['timeseries']
        print("\n" + "="*70)
        print("TIMESERIES DATA ANALYSIS")
        print("="*70)
        
        analysis = {
            'shape': df.shape,
            'date_range': {
                'start': str(df['Timestamp'].min()),
                'end': str(df['Timestamp'].max()),
                'days': (df['Timestamp'].max() - df['Timestamp'].min()).days
            },
            'temperature': {
                'mean': float(df['Digester_Temp_C'].mean()),
                'std': float(df['Digester_Temp_C'].std()),
                'min': float(df['Digester_Temp_C'].min()),
                'max': float(df['Digester_Temp_C'].max()),
                'optimal_range': [35, 55],
                'pct_optimal': float((df['Digester_Temp_C'].between(35, 55)).sum() / len(df) * 100)
            },
            'pH': {
                'mean': float(df['pH'].mean()),
                'std': float(df['pH'].std()),
                'min': float(df['pH'].min()),
                'max': float(df['pH'].max()),
                'optimal_range': [6.5, 7.5],
                'pct_optimal': float((df['pH'].between(6.5, 7.5)).sum() / len(df) * 100)
            },
            'methane_content': {
                'mean': float(df['CH4_percent'].mean()),
                'std': float(df['CH4_percent'].std()),
                'min': float(df['CH4_percent'].min()),
                'max': float(df['CH4_percent'].max()),
                'optimal_threshold': 55,
                'pct_above_threshold': float((df['CH4_percent'] >= 55).sum() / len(df) * 100)
            },
            'methane_production': {
                'mean_m3_hr': float(df['Methane_m3_hr'].mean()),
                'total_m3': float(df['Methane_m3_hr'].sum()),
                'daily_avg_m3': float(df['Methane_m3_hr'].sum() / (df['Timestamp'].dt.day.nunique() or 1)),
                'peak_m3_hr': float(df['Methane_m3_hr'].max())
            },
            'feed_rate': {
                'mean': float(df['Feed_Rate_kg_hr'].mean()),
                'std': float(df['Feed_Rate_kg_hr'].std()),
                'min': float(df['Feed_Rate_kg_hr'].min()),
                'max': float(df['Feed_Rate_kg_hr'].max())
            },
            'c_n_ratio': {
                'mean': float(df['C_N_Ratio'].mean()),
                'std': float(df['C_N_Ratio'].std()),
                'optimal_range': [20, 30],
                'pct_optimal': float((df['C_N_Ratio'].between(20, 30)).sum() / len(df) * 100)
            },
            'feedstock_types': df['Feedstock_Type'].value_counts().to_dict(),
            'wards_coverage': df['Ward'].nunique(),
            'yield_status_distribution': df['Yield_Status'].value_counts().to_dict(),
            'co2_reduction_total': float(df['CO2e_Reduction_kg_hr'].sum())
        }
        
        self.analysis_results['timeseries'] = analysis
        
        # Print summary
        print(f"Records: {analysis['shape'][0]} samples | Duration: {analysis['date_range']['days']} days")
        print(f"\nTemperature: {analysis['temperature']['mean']:.2f}°C (±{analysis['temperature']['std']:.2f})")
        print(f"             {analysis['temperature']['pct_optimal']:.1f}% within optimal range (35-55°C)")
        print(f"\nPH Level: {analysis['pH']['mean']:.2f} (±{analysis['pH']['std']:.2f})")
        print(f"          {analysis['pH']['pct_optimal']:.1f}% within optimal range (6.5-7.5)")
        print(f"\nMethane Production: {analysis['methane_production']['mean_m3_hr']:.2f} m³/hr")
        print(f"                    {analysis['methane_production']['daily_avg_m3']:.0f} m³/day (avg)")
        print(f"                    {analysis['methane_production']['total_m3']:.0f} m³ (total)")
        print(f"\nMethane Content: {analysis['methane_content']['mean']:.2f}% (±{analysis['methane_content']['std']:.2f})")
        print(f"                 {analysis['methane_content']['pct_above_threshold']:.1f}% above threshold (55%)")
        print(f"\nCO2 Reduction: {analysis['co2_reduction_total']:.0f} kg CO2e")
        print(f"Feedstock Types: {len(analysis['feedstock_types'])} types")
        print(f"Wards Covered: {analysis['wards_coverage']}")
        
        return analysis
    
    def analyze_locations(self):
        """Geographic and ward-level analysis"""
        df = self.datasets['locations']
        print("\n" + "="*70)
        print("GEOGRAPHIC & WARD-LEVEL ANALYSIS")
        print("="*70)
        
        analysis = {
            'wards': len(df),
            'population_total': int(df['population'].sum()),
            'households_total': int(df['households'].sum()),
            'biogas_potential': {
                'total_m3_day': float(df['estimated_biogas_m3_day'].sum()),
                'mean_m3_day': float(df['estimated_biogas_m3_day'].mean()),
                'max_m3_day': float(df['estimated_biogas_m3_day'].max()),
                'std_dev': float(df['estimated_biogas_m3_day'].std())
            },
            'methane_percentage': {
                'mean': float(df['estimated_methane_pct'].mean()),
                'min': float(df['estimated_methane_pct'].min()),
                'max': float(df['estimated_methane_pct'].max())
            },
            'electricity_potential': {
                'total_kwh_day': float(df['electricity_potential_kwh_day'].sum()),
                'mean_kwh_day': float(df['electricity_potential_kwh_day'].mean()),
                'max_kwh_day': float(df['electricity_potential_kwh_day'].max())
            },
            'waste_analysis': {
                'organic_waste_tpd': float(df['organic_waste_tpd'].sum()),
                'animal_waste_tpd': float(df['animal_waste_tpd'].sum()),
                'total_waste_tpd': float(df['total_waste_tpd'].sum())
            },
            'collection_efficiency': {
                'mean': float(df['collection_efficiency_pct'].mean()),
                'min': float(df['collection_efficiency_pct'].min()),
                'max': float(df['collection_efficiency_pct'].max())
            },
            'co2_reduction_annual': {
                'total_tonnes': float(df['co2_reduction_tonnes_year'].sum()),
                'mean_per_ward': float(df['co2_reduction_tonnes_year'].mean())
            },
            'top_10_wards': df.nlargest(10, 'estimated_biogas_m3_day')[
                ['ward_id', 'estimated_biogas_m3_day', 'estimated_methane_pct', 
                 'electricity_potential_kwh_day']
            ].to_dict('records')
        }
        
        self.analysis_results['locations'] = analysis
        
        # Print summary
        print(f"Total Wards: {analysis['wards']}")
        print(f"Population Covered: {analysis['population_total']:,}")
        print(f"Households: {analysis['households_total']:,}")
        print(f"\nBiogas Potential: {analysis['biogas_potential']['total_m3_day']:.0f} m³/day")
        print(f"Electricity Potential: {analysis['electricity_potential']['total_kwh_day']:.0f} kWh/day")
        print(f"\nWaste Input: {analysis['waste_analysis']['total_waste_tpd']:.2f} TPD")
        print(f"  - Organic Waste: {analysis['waste_analysis']['organic_waste_tpd']:.2f} TPD")
        print(f"  - Animal Waste: {analysis['waste_analysis']['animal_waste_tpd']:.2f} TPD")
        print(f"\nCO2 Reduction Potential: {analysis['co2_reduction_annual']['total_tonnes']:.0f} tonnes/year")
        print(f"Collection Efficiency: {analysis['collection_efficiency']['mean']:.1f}% (avg)")
        
        return analysis
    
    def analyze_yield_data(self):
        """Yield dataset analysis"""
        df = self.datasets['yield']
        print("\n" + "="*70)
        print("YIELD DATASET ANALYSIS")
        print("="*70)
        
        analysis = {
            'records': len(df),
            'locations': df['location_id'].nunique(),
            'waste_types': df['waste_type'].unique().tolist(),
            'daily_waste': {
                'mean_kg': float(df['daily_waste_mass_kg'].mean()),
                'total_kg': float(df['daily_waste_mass_kg'].sum()),
                'max_kg': float(df['daily_waste_mass_kg'].max())
            },
            'methane_yield': {
                'mean_m3': float(df['methane_yield_m3'].mean()),
                'total_m3': float(df['methane_yield_m3'].sum()),
                'std_dev': float(df['methane_yield_m3'].std()),
                'min_m3': float(df['methane_yield_m3'].min()),
                'max_m3': float(df['methane_yield_m3'].max())
            },
            'population_density': {
                'mean': float(df['population_density'].mean()),
                'min': float(df['population_density'].min()),
                'max': float(df['population_density'].max())
            },
            'animal_population': {
                'mean': float(df['animal_population'].mean()),
                'total': int(df['animal_population'].sum())
            },
            'distance_stats': {
                'mean_km': float(df['distance_to_road_km'].mean()),
                'min_km': float(df['distance_to_road_km'].min()),
                'max_km': float(df['distance_to_road_km'].max())
            },
            'waste_type_analysis': df.groupby('waste_type').agg({
                'methane_yield_m3': ['mean', 'sum', 'count'],
                'daily_waste_mass_kg': 'mean'
            }).to_dict()
        }
        
        self.analysis_results['yield'] = analysis
        
        # Print summary
        print(f"Total Records: {analysis['records']}")
        print(f"Unique Locations: {analysis['locations']}")
        print(f"Waste Types: {', '.join(analysis['waste_types'])}")
        print(f"\nDaily Waste Input: {analysis['daily_waste']['mean_kg']:.2f} kg (avg)")
        print(f"Methane Yield: {analysis['methane_yield']['mean_m3']:.2f} m³ (avg)")
        print(f"              {analysis['methane_yield']['total_m3']:.0f} m³ (total)")
        print(f"Population Density: {analysis['population_density']['mean']:.0f} (avg)")
        print(f"Distance to Road: {analysis['distance_stats']['mean_km']:.2f} km (avg)")
        
        return analysis
    
    def correlation_analysis(self):
        """Analyze correlations between parameters"""
        print("\n" + "="*70)
        print("CORRELATION ANALYSIS")
        print("="*70)
        
        df = self.datasets['timeseries']
        numeric_cols = ['Digester_Temp_C', 'pH', 'CH4_percent', 'Feed_Rate_kg_hr',
                       'C_N_Ratio', 'Gas_Flow_m3_hr', 'Methane_m3_hr']
        
        corr_matrix = df[numeric_cols].corr()
        
        # Find strong correlations
        strong_corrs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:
                    strong_corrs.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': float(corr_val)
                    })
        
        strong_corrs.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        print("\nStrong Correlations (|r| > 0.5):")
        for corr in strong_corrs[:10]:
            print(f"  {corr['var1']} ↔ {corr['var2']}: {corr['correlation']:.3f}")
        
        self.analysis_results['correlations'] = strong_corrs
        return strong_corrs
    
    def save_analysis(self):
        """Save analysis results to JSON"""
        output_file = 'gfis_analysis_report.json'
        
        with open(output_file, 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
        
        print(f"\n[+] Analysis saved to {output_file}")
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        self.load_all_datasets()
        self.analyze_timeseries()
        self.analyze_locations()
        self.analyze_yield_data()
        self.correlation_analysis()
        self.save_analysis()
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)
        print(f"Results saved to: gfis_analysis_report.json")


class RevenueOptimization:
    """Calculate revenue potential and optimization recommendations"""
    
    def __init__(self, analysis_results):
        self.analysis = analysis_results
    
    def calculate_revenue(self):
        """Calculate potential revenue"""
        print("\n" + "="*70)
        print("REVENUE POTENTIAL ANALYSIS")
        print("="*70)
        
        # From timeseries data
        daily_methane_m3 = self.analysis['timeseries']['methane_production']['daily_avg_m3']
        
        # Energy conversion: 1 m³ CH4 = ~36 MJ = ~10 kWh
        daily_kwh = daily_methane_m3 * 10
        
        # Market rate: ₹8 per kWh (average in India)
        daily_revenue = daily_kwh * 8
        monthly_revenue = daily_revenue * 30
        yearly_revenue = daily_revenue * 365
        
        revenue_potential = {
            'daily_m3': daily_methane_m3,
            'daily_kwh': daily_kwh,
            'daily_revenue_inr': daily_revenue,
            'monthly_revenue_inr': monthly_revenue,
            'yearly_revenue_inr': yearly_revenue,
            'location_potential': self.analysis['locations']['biogas_potential']['total_m3_day'],
            'location_kwh': self.analysis['locations']['biogas_potential']['total_m3_day'] * 10,
            'location_daily_revenue': self.analysis['locations']['biogas_potential']['total_m3_day'] * 10 * 8
        }
        
        print(f"\nCurrent Operations (from timeseries):")
        print(f"  Daily Methane: {daily_methane_m3:.0f} m³")
        print(f"  Daily Energy: {daily_kwh:.0f} kWh")
        print(f"  Daily Revenue: ₹{daily_revenue:.0f}")
        print(f"  Monthly Revenue: ₹{monthly_revenue:.0f}")
        print(f"  Yearly Revenue: ₹{yearly_revenue:.0f}")
        
        print(f"\nFull Location Potential (all {self.analysis['locations']['wards']} wards):")
        print(f"  Daily Biogas: {revenue_potential['location_potential']:.0f} m³")
        print(f"  Daily Energy: {revenue_potential['location_kwh']:.0f} kWh")
        print(f"  Daily Revenue: ₹{revenue_potential['location_daily_revenue']:.0f}")
        print(f"  Monthly Revenue: ₹{revenue_potential['location_daily_revenue'] * 30:.0f}")
        print(f"  Yearly Revenue: ₹{revenue_potential['location_daily_revenue'] * 365:.0f}")
        
        print(f"\nCO2 Reduction & Environmental Impact:")
        print(f"  Annual CO2 Reduction: {self.analysis['locations']['co2_reduction_annual']['total_tonnes']:.0f} tonnes")
        print(f"  Economic Value (₹200/tonne): ₹{self.analysis['locations']['co2_reduction_annual']['total_tonnes'] * 200:.0f}")
        
        return revenue_potential


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("GFIS COMPREHENSIVE DATA ANALYSIS")
    print("Green Fuel Intelligence System v2.0")
    print("="*70)
    
    analyzer = GFISDataAnalyzer()
    analyzer.generate_report()
    
    revenue_optimizer = RevenueOptimization(analyzer.analysis_results)
    revenue_optimizer.calculate_revenue()
    
    print("\n" + "="*70)
    print("All analyses complete!")
    print("="*70)


if __name__ == "__main__":
    main()
