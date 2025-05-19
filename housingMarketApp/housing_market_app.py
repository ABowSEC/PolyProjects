import streamlit as sL
import pandas as pD
import matplotlib.pyplot as plotLib

#pD pparses static txt data

sL.set_page_config(page_title="Zillow Data Viewer", layout="centered")
sL.title ("Housing Market data Analysis")
sL.markdown("NOTE FOR ZILLOW DATA: Download CSV files from [Zillow Research data](https://www.zillow.com/research/data/) ") 

#Process Upload
uploadedFile = sL.file_uploader("Upload a Zillow CSV File",type=["csv"])

if uploadedFile:
    try:
        #Holds data from user 
        dFrame= pD.read_csv(uploadedFile) 
        sL.success("Upload Complete")

        #preview data
        if sL.checkbox("Show Raw Data"):
            sL.dataframe(dFrame)

        # Select a region for time series analysis
        if "RegionName" in dFrame.columns:
            region = sL.selectbox("Select a region to view trends:", dFrame["RegionName"].unique())
            row = dFrame[dFrame["RegionName"] == region].iloc[0]

            # Extract  date columns
            date_data = row.iloc[5:]  # of meta data colums
            date_data.index = pD.to_datetime(date_data.index, errors='coerce') #Invalid Date become 'NAT'
            date_data = date_data.dropna().astype(float)

            sL.line_chart(date_data)
            sL.markdown(f"**Current value:** ${date_data.iloc[-1]:,.2f} as of {date_data.index[-1].strftime('%B %Y')}")

        else:
            sL.warning("Couldn't find 'RegionName' column. Please upload a valid Zillow CSV file.")

    except Exception as e:
        sL.error(f"An error occurred while processing the file: {e}")

else:
    sL.info("Awaiting CSV file upload...")
        
            


