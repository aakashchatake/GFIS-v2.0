import streamlit as st
import pandas as pd

def main():
    st.title('GFIS Pilot Dashboard')
    df = pd.read_csv('iot_sensor_data.csv')
    st.line_chart(df[['pH', 'temperature', 'ORP', 'gas_composition']])
    st.write(df.head())
    st.info('This dashboard visualizes hypothetical IoT sensor data for biogas optimization.')

if __name__ == '__main__':
    main()