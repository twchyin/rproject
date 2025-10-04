

import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(
    page_title="Insurance Claims Dashboard",
    layout="wide"
)

# --- 1. Load Data ---
@st.cache_data
def load_data():
    # Assuming the file is in the same directory as the script/notebook environment
    df = pd.read_csv("insurance_claims.csv")
    return df

df = load_data()

# --- 2. Sidebar Filter ---
st.sidebar.header("Filter Options")

# Get unique values for the gender filter
sex_options = df['insured_sex'].unique()
selected_sex = st.sidebar.selectbox(
    'Select Insured Sex:',
    options=sex_options,
    index=0 # Default to the first option
)

# Filter the DataFrame based on selection
filtered_df = df[df['insured_sex'] == selected_sex]

# --- 3. Main Dashboard Content ---
st.title("💸 Insurance Claims Analysis")
st.markdown("### Total Claims by Incident Severity")

# Calculate metrics for the chart
claim_summary = filtered_df.groupby('incident_severity')['total_claim_amount'].mean().reset_index()
claim_summary.columns = ['Incident Severity', 'Average Total Claim Amount']

# Create an interactive Plotly Bar Chart
fig = px.bar(
    claim_summary,
    x='Incident Severity',
    y='Average Total Claim Amount',
    title=f'Average Total Claim Amount by Severity for {selected_sex} Insureds',
    color='Incident Severity',
    template='plotly_white'
)

# Customize the layout
fig.update_layout(
    xaxis={'categoryorder':'total descending'}, # Sort bars
    yaxis_title='Average Claim Amount (USD)',
    hovermode='x unified'
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# --- 4. Data Preview ---
st.markdown("---")
st.subheader(f"Data Preview for {selected_sex} Insureds")
st.dataframe(filtered_df.head(10))

# Display a count metric
st.metric(
    label="Total Records Filtered",
    value=f"{len(filtered_df):,}"
)
