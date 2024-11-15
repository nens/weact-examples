import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_points(df):
    """
    Plots points on a map centered on Kyrgyzstan using Plotly,
    based on a DataFrame with a 'geometry' column.

    Parameters:
    df (pd.DataFrame): A DataFrame with a 'geometry' column where each entry is a dictionary
                       containing a point geometry with "type" and "coordinates" keys.
    """
    # Extract latitude and longitude from the 'geometry' column
    df['latitude'] = df['geometry'].apply(lambda geom: geom['coordinates'][1])
    df['longitude'] = df['geometry'].apply(lambda geom: geom['coordinates'][0])

    # Create a scatter plot on a map centered on Kyrgyzstan
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        mapbox_style="open-street-map",
        title="Points on Map - Kyrgyzstan"
    )
    
    # Update layout to focus on Kyrgyzstan
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=41.2044, lon=74.7661),  # Center on Kyrgyzstan
            zoom=5  # Adjust zoom level for an appropriate view
        ),
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    
    fig.show()

def plot_timeseries(df, value_format="Precipitation [mm/30min]"):
    """
    Plots a time series with Plotly based on a DataFrame with 'time', 'value', 'flag', and 'comment' columns.

    Parameters:
    df (pd.DataFrame): DataFrame with columns:
                       - 'time': timestamp in ISO format
                       - 'value': numerical values to plot
                       - 'flag': optional column, can be used for conditional formatting or markers
                       - 'comment': optional column, can add text annotations
    """
    # Convert 'time' column to datetime format
    df['time'] = pd.to_datetime(df['time'])

    # Create the line plot for the time series
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['time'],
        y=df['value'],
        name=value_format,
        marker_color='royalblue'
    ))

    # Customize layout
    fig.update_layout(
        title="Time Series Plot",
        xaxis_title="Time",
        yaxis_title=value_format,
        xaxis=dict(
            tickformat='%Y-%m-%d %H:%M:%S',
            title="Time",
            type="date"
        ),
        yaxis=dict(title=value_format),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    fig.show()
