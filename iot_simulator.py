"""
GFIS IoT Simulator - Simulates real digester operations with realistic data
Useful for testing dashboards and ML models with continuous data stream
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
import random

class DigesterSimulator:
    """Simulates biogas digester operations with realistic parameters"""
    
    def __init__(self, 
                 initial_temp=39.0,
                 initial_ph=7.1,
                 initial_ch4=56.0,
                 feedstock_type='Cattle_Dung'):
        
        self.current_temp = initial_temp
        self.current_ph = initial_ph
        self.current_ch4 = initial_ch4
        self.feedstock_type = feedstock_type
        self.timestamp = datetime.now()
        
        # Parameter targets (optimal ranges)
        self.target_temp = 39.0  # Mesophilic range
        self.target_ph = 7.1
        self.target_ch4 = 57.0
        
        # Feedstock-specific characteristics
        self.feedstock_properties = {
            'Cattle_Dung': {'ch4_base': 56, 'cn_ratio': 28, 'feed_rate': 520},
            'Poultry_Litter': {'ch4_base': 55, 'cn_ratio': 18, 'feed_rate': 480},
            'Veg_Market_Waste': {'ch4_base': 58, 'cn_ratio': 25, 'feed_rate': 510},
            'Mixed_Bio_Waste': {'ch4_base': 54, 'cn_ratio': 22, 'feed_rate': 490}
        }
        
        # Historical data storage
        self.data_history = []
    
    def step(self, disturbance=None):
        """Simulate one hour of digester operation"""
        
        props = self.feedstock_properties[self.feedstock_type]
        
        # Natural drift towards targets with random fluctuation
        temp_delta = (self.target_temp - self.current_temp) * 0.05 + np.random.normal(0, 0.3)
        ph_delta = (self.target_ph - self.current_ph) * 0.02 + np.random.normal(0, 0.05)
        ch4_delta = (self.target_ch4 - self.current_ch4) * 0.03 + np.random.normal(0, 0.5)
        
        # Apply disturbances if provided
        if disturbance:
            if disturbance.get('high_feed'):
                temp_delta -= 0.5  # Temperature drop from increased feed
                ph_delta -= 0.1
                ch4_delta -= 1.0
            if disturbance.get('low_feed'):
                temp_delta += 0.2
                ph_delta += 0.05
                ch4_delta += 0.5
            if disturbance.get('temperature_shock'):
                temp_delta = disturbance['temperature_shock']
        
        # Update parameters
        self.current_temp = np.clip(self.current_temp + temp_delta, 35, 45)
        self.current_ph = np.clip(self.current_ph + ph_delta, 6.5, 7.5)
        self.current_ch4 = np.clip(self.current_ch4 + ch4_delta, 50, 62)
        
        # Calculate derived parameters
        feed_rate = props['feed_rate'] + np.random.normal(0, 30)
        cn_ratio = props['cn_ratio'] + np.random.normal(0, 1)
        gas_flow = (feed_rate / 12) + (self.current_ch4 - 50) * 0.2
        methane_m3_hr = gas_flow * (self.current_ch4 / 100)
        
        # Yield status determination
        if (self.current_temp > 35 and self.current_temp < 42 and 
            self.current_ph > 6.8 and self.current_ph < 7.3 and 
            self.current_ch4 > 55):
            status = 'Normal'
        elif (self.current_temp > 33 and self.current_temp < 44 and 
              self.current_ph > 6.5 and self.current_ph < 7.5):
            status = 'Warning'
        else:
            status = 'Critical'
        
        # CO2 equivalent reduction
        co2_reduction = methane_m3_hr * 12.77  # 1 m³ CH4 = 12.77 kg CO2e
        
        # Record data
        record = {
            'Timestamp': self.timestamp,
            'Ward': random.choice(['Rural Fringe', 'Solapur Market', 'MIDC Area']),
            'Human_Population': np.random.randint(100000, 200000),
            'Animal_Population': np.random.randint(5000, 60000),
            'Avg_Transport_Distance_km': np.random.uniform(2, 10),
            'Feedstock_Type': self.feedstock_type,
            'Feed_Rate_kg_hr': max(0, feed_rate),
            'Digester_Temp_C': self.current_temp,
            'pH': self.current_ph,
            'CH4_percent': self.current_ch4,
            'Gas_Flow_m3_hr': max(0, gas_flow),
            'C_N_Ratio': max(10, cn_ratio),
            'Methane_m3_hr': max(0, methane_m3_hr),
            'Methane_kg_hr': max(0, methane_m3_hr * 0.717),
            'CO2e_Reduction_kg_hr': max(0, co2_reduction),
            'Yield_Status': status
        }
        
        self.data_history.append(record)
        self.timestamp += timedelta(hours=1)
        
        return record
    
    def run_simulation(self, hours=24*7, output_file=None):
        """Run continuous simulation"""
        print(f"Starting {hours}-hour simulation for {self.feedstock_type}...")
        
        disturbance_schedule = {
            48: {'high_feed': True},  # Feed overload at 48 hours
            100: {'low_feed': True},  # Feed shortage at 100 hours
            150: {'temperature_shock': -2}  # Temperature drop at 150 hours
        }
        
        for hour in range(hours):
            disturbance = disturbance_schedule.get(hour)
            record = self.step(disturbance)
            
            if (hour + 1) % 24 == 0:
                print(f"✓ {hour + 1} hours simulated")
        
        # Convert to DataFrame
        df = pd.DataFrame(self.data_history)
        
        if output_file:
            df.to_csv(output_file, index=False)
            print(f"[+] Simulation data saved to {output_file}")
        
        return df


class MultiDigesterSimulation:
    """Simulate multiple digesters operating simultaneously"""
    
    def __init__(self, num_digesters=3):
        self.digesters = []
        self.feedstocks = ['Cattle_Dung', 'Poultry_Litter', 'Veg_Market_Waste', 'Mixed_Bio_Waste']
        
        for i in range(num_digesters):
            feedstock = self.feedstocks[i % len(self.feedstocks)]
            digester = DigesterSimulator(feedstock_type=feedstock)
            self.digesters.append(digester)
    
    def run_multi_simulation(self, hours=24*7):
        """Run simulation for multiple digesters"""
        print(f"Starting multi-digester simulation ({len(self.digesters)} digesters, {hours} hours)...")
        
        all_data = []
        
        for digester in self.digesters:
            df = digester.run_simulation(hours, output_file=None)
            all_data.append(df)
        
        # Combine data
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df.sort_values('Timestamp').reset_index(drop=True)
        
        return combined_df


class SystemOptimizer:
    """Provides optimization recommendations based on current state"""
    
    @staticmethod
    def analyze_condition(record):
        """Analyze digester condition and provide recommendations"""
        
        recommendations = {
            'critical_alerts': [],
            'warnings': [],
            'optimizations': [],
            'score': 100
        }
        
        # Temperature checks
        if record['Digester_Temp_C'] < 36:
            recommendations['critical_alerts'].append(
                f"Temperature too low ({record['Digester_Temp_C']:.1f}°C). Increase heating system."
            )
            recommendations['score'] -= 20
        elif record['Digester_Temp_C'] > 42:
            recommendations['critical_alerts'].append(
                f"Temperature too high ({record['Digester_Temp_C']:.1f}°C). Improve cooling."
            )
            recommendations['score'] -= 20
        
        # pH checks
        if record['pH'] < 6.5:
            recommendations['warnings'].append(
                f"pH too acidic ({record['pH']:.2f}). Add buffer or reduce feed rate."
            )
            recommendations['score'] -= 15
        elif record['pH'] > 7.5:
            recommendations['warnings'].append(
                f"pH too alkaline ({record['pH']:.2f}). Add organic matter."
            )
            recommendations['score'] -= 10
        
        # Methane checks
        if record['CH4_percent'] < 50:
            recommendations['warnings'].append(
                f"Low methane content ({record['CH4_percent']:.1f}%). Review feedstock quality."
            )
            recommendations['score'] -= 15
        elif record['CH4_percent'] < 55:
            recommendations['optimizations'].append(
                f"Methane slightly below optimal ({record['CH4_percent']:.1f}%). Consider adjusting C:N ratio."
            )
            recommendations['score'] -= 5
        
        # C:N ratio checks
        if record['C_N_Ratio'] < 20:
            recommendations['optimizations'].append(
                f"C:N ratio low ({record['C_N_Ratio']:.1f}). Add carbon source (wood chips, leaves)."
            )
            recommendations['score'] -= 5
        elif record['C_N_Ratio'] > 30:
            recommendations['optimizations'].append(
                f"C:N ratio high ({record['C_N_Ratio']:.1f}). Add nitrogen source (animal manure)."
            )
            recommendations['score'] -= 5
        
        recommendations['score'] = max(0, min(100, recommendations['score']))
        
        return recommendations


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("GFIS IoT DIGESTER SIMULATOR")
    print("="*70)
    
    # Single digester simulation
    print("\n[1] Running single-digester simulation...")
    simulator = DigesterSimulator(feedstock_type='Cattle_Dung')
    df_single = simulator.run_simulation(hours=24*14, output_file='simulated_iot_data_single.csv')
    
    print(f"[+] Generated {len(df_single)} records")
    print(f"[+] Date range: {df_single['Timestamp'].min()} to {df_single['Timestamp'].max()}")
    
    # Statistics
    print(f"\nStatistics from simulation:")
    print(f"  Temperature: {df_single['Digester_Temp_C'].mean():.2f}°C (±{df_single['Digester_Temp_C'].std():.2f})")
    print(f"  pH: {df_single['pH'].mean():.2f} (±{df_single['pH'].std():.2f})")
    print(f"  Methane %: {df_single['CH4_percent'].mean():.2f}% (±{df_single['CH4_percent'].std():.2f})")
    print(f"  Methane Production: {df_single['Methane_m3_hr'].mean():.2f} m³/hr")
    print(f"  Total Methane: {df_single['Methane_m3_hr'].sum():.0f} m³")
    
    # Multi-digester simulation
    print("\n[2] Running multi-digester simulation...")
    multi_sim = MultiDigesterSimulation(num_digesters=4)
    df_multi = multi_sim.run_multi_simulation(hours=24*7)
    df_multi.to_csv('simulated_iot_data_multi.csv', index=False)
    
    print(f"[+] Generated {len(df_multi)} total records")
    
    # Analysis
    print("\n[3] Optimization Analysis...")
    optimizer = SystemOptimizer()
    latest_record = df_single.iloc[-1].to_dict()
    
    recommendations = optimizer.analyze_condition(latest_record)
    print(f"\nSystem Health Score: {recommendations['score']}/100")
    
    if recommendations['critical_alerts']:
        print("\n🔴 Critical Alerts:")
        for alert in recommendations['critical_alerts']:
            print(f"  - {alert}")
    
    if recommendations['warnings']:
        print("\n🟡 Warnings:")
        for warning in recommendations['warnings']:
            print(f"  - {warning}")
    
    if recommendations['optimizations']:
        print("\n💡 Optimization Suggestions:")
        for opt in recommendations['optimizations']:
            print(f"  - {opt}")
    
    print("\n" + "="*70)
    print("Simulation complete! Data saved to:")
    print("  - simulated_iot_data_single.csv")
    print("  - simulated_iot_data_multi.csv")
    print("="*70)


if __name__ == "__main__":
    main()
