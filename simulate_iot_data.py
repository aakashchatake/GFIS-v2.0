import random
import pandas as pd

def simulate_sensor_data(num_samples=100):
    data = {
        'timestamp': pd.date_range(start='2025-01-01', periods=num_samples, freq='H'),
        'pH': [round(random.uniform(6.5, 8.0), 2) for _ in range(num_samples)],
        'temperature': [round(random.uniform(30, 40), 1) for _ in range(num_samples)],
        'ORP': [round(random.uniform(-300, -100), 1) for _ in range(num_samples)],
        'gas_composition': [round(random.uniform(50, 70), 1) for _ in range(num_samples)]
    }
    df = pd.DataFrame(data)
    df.to_csv('iot_sensor_data.csv', index=False)
    print('Simulated IoT sensor data saved to iot_sensor_data.csv')

if __name__ == '__main__':
    simulate_sensor_data()