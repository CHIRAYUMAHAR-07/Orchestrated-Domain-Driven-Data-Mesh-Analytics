import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ----------------------------------------------------------
# App Setup
# ----------------------------------------------------------
st.set_page_config(page_title="NYC Taxi Data Analytics", layout="wide")
st.title("Orchestrated Domain-Driven Data Mesh Analytics Dashboard")
st.markdown("**By Chirayu Mahar | Orchestrated Domain-Driven Data Mesh Architecture**")

# ----------------------------------------------------------
# Flexible Data Loader (Excel or CSV)
# ----------------------------------------------------------
@st.cache_data
def load_dataset():
    """
    Automatically detects and loads Excel (.xlsx) or CSV files.
    Searches for 'main' and 'taxi' files in data/ folder or current directory.
    """
    # Updated file patterns to match your actual files
    file_options = [
        ("data/main.xlsx", "data/taxi.xlsx"),
        ("data/main.csv", "data/taxi.csv"),
        ("main.xlsx", "taxi.xlsx"),
        ("main.csv", "taxi.csv"),
        # Fallback to original names
        ("data/data.xlsx", "data/taxi_zone_lookup.xlsx"),
        ("data/data.csv", "data/taxi_zone_lookup.csv"),
    ]

    main_path, zone_path = None, None

    for m, z in file_options:
        if os.path.exists(m) and os.path.exists(z):
            main_path, zone_path = m, z
            break

    if not main_path or not zone_path:
        st.error("❌ Could not find your data files. Please ensure you have:\n"
                 "- `main.xlsx` (or main.csv) - your main taxi trip data\n"
                 "- `taxi.xlsx` (or taxi.csv) - your taxi zone lookup data\n\n"
                 "These files should be in a 'data' folder or in the same directory as app.py")
        
        # Show what files were found to help debug
        st.info("**Files found in current directory:**")
        if os.path.exists("data"):
            st.write(os.listdir("data"))
        else:
            st.write("No 'data' folder found")
        st.stop()

    # Load Excel or CSV depending on extension
    try:
        if main_path.endswith(".xlsx"):
            data = pd.read_excel(main_path)
        else:
            data = pd.read_csv(main_path)

        if zone_path.endswith(".xlsx"):
            zones = pd.read_excel(zone_path)
        else:
            zones = pd.read_csv(zone_path)
            
        return data, zones, main_path, zone_path
    
    except Exception as e:
        st.error(f"❌ Error loading files: {str(e)}")
        st.stop()

# Load data
try:
    data, zones, main_path, zone_path = load_dataset()
    st.success(f"✅ Data loaded successfully!\n\n**Main file:** `{main_path}` ({len(data):,} rows)\n\n**Zone file:** `{zone_path}` ({len(zones):,} rows)")
except Exception as e:
    st.error(f"Failed to load data: {str(e)}")
    st.stop()

# ----------------------------------------------------------
# Data Preview
# ----------------------------------------------------------
st.subheader("📋 Data Preview")
with st.expander("View Main Dataset Sample", expanded=True):
    st.write("**First 10 rows of main dataset:**")
    st.dataframe(data.head(10), use_container_width=True)

with st.expander("View Zone Lookup Data"):
    st.write("**Taxi Zone Lookup Data:**")
    st.dataframe(zones.head(10), use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------
# Dataset Overview
# ----------------------------------------------------------
st.subheader("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Trips", f"{len(data):,}")
col2.metric("Columns", f"{len(data.columns)}")
col3.metric("Missing Values", f"{data.isna().sum().sum():,}")
col4.metric("Zones", f"{len(zones):,}")

# Show column information
with st.expander("📝 Column Details"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Main Dataset Columns:**")
        st.write(list(data.columns))
    with col_b:
        st.write("**Zone Dataset Columns:**")
        st.write(list(zones.columns))

st.markdown("---")

# ----------------------------------------------------------
# Trips by Borough
# ----------------------------------------------------------
st.subheader("🗺️ Trips by Borough")

# Find column names with flexible matching
puloc_col = None
for col in data.columns:
    if "pulocation" in col.lower() or "pickup" in col.lower():
        puloc_col = col
        break

borough_col = None
for col in zones.columns:
    if "borough" in col.lower():
        borough_col = col
        break

locationid_col = None
for col in zones.columns:
    if "locationid" in col.lower():
        locationid_col = col
        break

if puloc_col and borough_col and locationid_col:
    try:
        merged = data.merge(zones, left_on=puloc_col, right_on=locationid_col, how="left")
        borough_counts = merged[borough_col].value_counts().reset_index()
        borough_counts.columns = ["Borough", "Trip Count"]
        
        # Remove any null/unknown values
        borough_counts = borough_counts[borough_counts["Borough"].notna()]

        fig = px.bar(
            borough_counts,
            x="Borough",
            y="Trip Count",
            title="Number of Trips per Borough",
            color="Trip Count",
            color_continuous_scale="Viridis",
            text="Trip Count"
        )
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show top zones
        if "zone" in merged.columns or any("zone" in col.lower() for col in merged.columns):
            zone_col = next((c for c in merged.columns if "zone" in c.lower()), None)
            if zone_col:
                st.subheader("📍 Top Pickup Zones")
                top_zones = merged[zone_col].value_counts().head(10).reset_index()
                top_zones.columns = ["Zone", "Trip Count"]
                st.dataframe(top_zones, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating borough visualization: {str(e)}")
        st.write("Debug info - Columns found:")
        st.write(f"- Pickup Location Column: {puloc_col}")
        st.write(f"- Borough Column: {borough_col}")
        st.write(f"- LocationID Column: {locationid_col}")
else:
    st.warning("⚠️ Could not automatically detect required columns for borough analysis.")
    st.write("**Looking for:**")
    st.write("- Pickup location column (containing 'PULocation' or 'pickup')")
    st.write("- Borough column in zone lookup")
    st.write("- LocationID column in zone lookup")
    st.write("\n**Available columns:**")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Main dataset:", list(data.columns))
    with col2:
        st.write("Zone lookup:", list(zones.columns))

st.markdown("---")

# ----------------------------------------------------------
# Time-based Analysis
# ----------------------------------------------------------
time_col = None
for col in data.columns:
    if any(keyword in col.lower() for keyword in ["time", "date", "datetime", "pickup"]):
        time_col = col
        break

if time_col:
    try:
        data_copy = data.copy()
        data_copy[time_col] = pd.to_datetime(data_copy[time_col], errors="coerce")
        
        # Remove rows where date parsing failed
        data_copy = data_copy[data_copy[time_col].notna()]
        
        if len(data_copy) > 0:
            data_copy["date_only"] = data_copy[time_col].dt.date
            data_copy["hour"] = data_copy[time_col].dt.hour
            
            # Daily trips
            st.subheader("📆 Trips Over Time")
            daily_trips = data_copy.groupby("date_only").size().reset_index(name="Trip Count")
            
            fig2 = px.line(
                daily_trips, 
                x="date_only", 
                y="Trip Count", 
                title="Daily Trip Volume",
                labels={"date_only": "Date", "Trip Count": "Number of Trips"}
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
            
            # Hourly distribution
            st.subheader("🕐 Trips by Hour of Day")
            hourly_trips = data_copy.groupby("hour").size().reset_index(name="Trip Count")
            
            fig3 = px.bar(
                hourly_trips,
                x="hour",
                y="Trip Count",
                title="Trip Distribution by Hour",
                labels={"hour": "Hour of Day", "Trip Count": "Number of Trips"},
                color="Trip Count",
                color_continuous_scale="Blues"
            )
            fig3.update_layout(height=400)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning(f"⚠️ Could not parse dates from column '{time_col}'")
    except Exception as e:
        st.warning(f"⚠️ Error processing time data: {str(e)}")
else:
    st.info("ℹ️ No date/time column detected in dataset for temporal analysis.")

st.markdown("---")

# ----------------------------------------------------------
# Interactive Data Explorer
# ----------------------------------------------------------
st.subheader("🔍 Interactive Data Explorer")

col1, col2 = st.columns([3, 1])
with col1:
    columns = st.multiselect(
        "Select columns to view:", 
        data.columns.tolist(), 
        default=list(data.columns[:min(5, len(data.columns))])
    )
with col2:
    num_rows = st.slider("Number of rows", 10, 100, 50)

if columns:
    st.dataframe(data[columns].head(num_rows), use_container_width=True)
else:
    st.info("Please select at least one column to display.")

# ----------------------------------------------------------
# Download Section
# ----------------------------------------------------------
st.markdown("---")
st.subheader("💾 Export Data")

col1, col2 = st.columns(2)
with col1:
    if st.button("Download Full Dataset as CSV"):
        csv = data.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="nyc_taxi_data_export.csv",
            mime="text/csv"
        )

with col2:
    if st.button("Download Zone Lookup as CSV"):
        csv_zones = zones.to_csv(index=False)
        st.download_button(
            label="📥 Download Zones CSV",
            data=csv_zones,
            file_name="taxi_zones_export.csv",
            mime="text/csv"
        )

st.markdown("---")
st.caption("✨ **Orchestrated Domain-Driven Data Mesh Architecture** | Built with Streamlit & Plotly")
st.caption("💡 Supports both Excel (.xlsx) and CSV files")