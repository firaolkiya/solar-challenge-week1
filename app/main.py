import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 

# Set up the page title and layout
st.set_page_config(page_title="Data Insights Dashboard", layout="wide")

st.title("Solar Radiation Data Analysis Dashboard")

# --- Data Loading ---
@st.cache_data
def load_data():
    try:
        bdf = pd.read_csv('data/benin.csv')
        sdf = pd.read_csv('data/sierraleone.csv')
        tdf = pd.read_csv('data/togo.csv')

        bdf['country'] = 'Benin'
        sdf['country'] = 'Sierra Leone'
        tdf['country'] = 'Togo'

        df_combined = pd.concat([bdf, sdf, tdf], ignore_index=True)

        return df_combined

    except FileNotFoundError:
        st.error("Make sure you have the data files (benin_clean.csv, sierraleone_clean.csv, togo_clean.csv) in a 'data' subdirectory.")
        return pd.DataFrame() 

df_combined = load_data()

# Check if data was loaded successfully
if df_combined.empty:
    st.stop() 

# Define available metrics - make sure these columns exist in your loaded data
metrics = ['GHI', 'DNI', 'DHI']

available_metrics = [metric for metric in metrics if metric in df_combined.columns]

if not available_metrics:
    st.error("The required metric columns (GHI, DNI, DHI) were not found in the loaded data.")
    st.stop()

# --- Sidebar Widgets ---
st.sidebar.header("Filter Data and Select Options")

# Widget to select countries
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    df_combined['country'].unique(),
    df_combined['country'].unique() # Default to all countries
)

# Widget to select metric
selected_metric = st.sidebar.radio(
    "Select Metric",
    available_metrics # Use only available metrics
)

# Get the min and max of the selected metric for the slider
metric_min = float(df_combined[selected_metric].min()) if not df_combined[selected_metric].empty else 0.0
metric_max = float(df_combined[selected_metric].max()) if not df_combined[selected_metric].empty else 1000.0

# Widget for metric range slider
metric_range = st.sidebar.slider(
    f"Select {selected_metric} Range",
    metric_min,
    metric_max,
    (metric_min, metric_max) # Default range
)

# Filter data based on selected countries and metric range
filtered_df = df_combined[
    (df_combined['country'].isin(selected_countries)) &
    (df_combined[selected_metric] >= metric_range[0]) &
    (df_combined[selected_metric] <= metric_range[1])
]

# --- Main Content ---

st.header(f"Analysis of {selected_metric}")

# Boxplot of the selected metric
st.subheader(f"{selected_metric} Boxplot by Country")
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='country', y=selected_metric, data=filtered_df, palette='viridis', ax=ax)
    plt.title(f'Boxplot of {selected_metric}')
    plt.xlabel('Country')
    plt.ylabel(selected_metric)
    st.pyplot(fig)
else:
    st.warning("No data available for the selected filters.")

# More Plots (Histograms and Scatter Plots)
st.subheader("Additional Plots")
if not filtered_df.empty:
    # Histogram
    st.write(f"Histogram of {selected_metric}")
    fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
    sns.histplot(data=filtered_df, x=selected_metric, kde=True, hue='country', ax=ax_hist)
    plt.title(f'Histogram of {selected_metric}')
    plt.xlabel(selected_metric)
    plt.ylabel('Frequency')
    st.pyplot(fig_hist)

    # Scatter Plot (Example: GHI vs DNI - you'd need to adapt this based on your data)
    if 'GHI' in filtered_df.columns and 'DNI' in filtered_df.columns:
         st.write("Scatter Plot: GHI vs DNI (Example)")
         fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
         sns.scatterplot(data=filtered_df, x='GHI', y='DNI', hue='country', ax=ax_scatter)
         plt.title('Scatter Plot of GHI vs DNI')
         plt.xlabel('GHI')
         plt.ylabel('DNI')
         st.pyplot(fig_scatter)
    else:
         st.info("Cannot generate Scatter Plot: GHI or DNI columns not found in data.")

else:
    st.warning("No data available for the selected filters to generate additional plots.")


# Summary Statistics Table
st.header("Summary Statistics")
if not filtered_df.empty:
    st.write(f"Summary Statistics for {selected_metric} by Country")
    summary_table = filtered_df.groupby('country')[selected_metric].agg(['mean', 'median', 'std', 'min', 'max'])
    st.dataframe(summary_table)
else:
    st.warning("No data available for the selected filters to generate summary statistics.")

# Top Regions Table (Placeholder)
st.header("Top Regions (Placeholder)")
st.write("This section will show a table of top regions based on selected criteria.")

if not filtered_df.empty:
    st.subheader("Preview of Filtered Data")
    st.dataframe(filtered_df.head())
else:
    st.warning("No data available for the selected filters to show data preview.")


# Maps (Placeholder)
st.header("Geospatial Data Visualization (Placeholder)")
st.write("This section is for displaying data on a map.")

if not filtered_df.empty and 'latitude' in filtered_df.columns and 'longitude' in filtered_df.columns:
    st.map(filtered_df[['latitude', 'longitude']].dropna())
else:
    st.warning("Data is not available with latitude and longitude columns or no data after filtering to show on map.")


st.write("By Firaol Bulo")

