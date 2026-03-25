import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import date, timedelta
import base64
from io import StringIO, BytesIO
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
    .info-text {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 Stock Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar inputs
with st.sidebar:
    st.header("📌 Configuration")
    
    # Stock ticker input
    ticker = st.text_input("Stock Ticker Symbol", value="AAPL", help="Enter stock symbol (e.g., AAPL, GOOGL, MSFT)")
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", date.today() - timedelta(days=365))
    with col2:
        end_date = st.date_input("End Date", date.today())
    
    # Technical indicators
    st.subheader("📈 Technical Indicators")
    show_sma = st.checkbox("Show SMA", value=True)
    sma_period = st.slider("SMA Period", 5, 200, 20) if show_sma else None
    
    show_ema = st.checkbox("Show EMA", value=True)
    ema_period = st.slider("EMA Period", 5, 200, 50) if show_ema else None
    
    show_rsi = st.checkbox("Show RSI", value=True)
    rsi_period = st.slider("RSI Period", 7, 30, 14) if show_rsi else None
    
    # Chart preferences
    st.subheader("🎨 Chart Settings")
    chart_type = st.radio("Chart Type", ["Candlestick", "Line", "OHLC"])
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This dashboard provides comprehensive stock analysis including:
    - Historical price data
    - Technical indicators (SMA, EMA, RSI)
    - Performance metrics
    - CSV export capability
    """)

# Function to calculate RSI
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to create download link
def get_download_link(df, filename="stock_data.csv"):
    csv = df.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-link">📥 Download CSV File</a>'
    return href

# Main content
if ticker:
    try:
        # Fetch data
        with st.spinner(f"Fetching data for {ticker.upper()}..."):
            stock = yf.Ticker(ticker.upper())
            df = stock.history(start=start_date, end=end_date)
            
            if df.empty:
                st.error(f"No data found for ticker {ticker.upper()}. Please check the symbol and try again.")
                st.stop()
        
        # Calculate technical indicators
        df['SMA'] = df['Close'].rolling(window=sma_period).mean() if show_sma else None
        df['EMA'] = df['Close'].ewm(span=ema_period, adjust=False).mean() if show_ema else None
        
        if show_rsi:
            df['RSI'] = calculate_rsi(df['Close'], period=rsi_period)
        
        # Display stock info
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            current_price = df['Close'].iloc[-1]
            price_change = df['Close'].iloc[-1] - df['Close'].iloc[-2] if len(df) > 1 else 0
            price_change_pct = (price_change / df['Close'].iloc[-2]) * 100 if len(df) > 1 else 0
            st.metric(
                label="Current Price",
                value=f"${current_price:.2f}",
                delta=f"{price_change_pct:.2f}%"
            )
        
        with col2:
            st.metric(
                label="Volume",
                value=f"{df['Volume'].iloc[-1]:,.0f}",
                delta=f"{((df['Volume'].iloc[-1] - df['Volume'].iloc[-2]) / df['Volume'].iloc[-2] * 100):.1f}%" if len(df) > 1 else None
            )
        
        with col3:
            st.metric(
                label="52-Week Range",
                value=f"${df['Low'].min():.2f} - ${df['High'].max():.2f}"
            )
        
        with col4:
            st.metric(
                label="Avg Volume (20d)",
                value=f"{df['Volume'].rolling(20).mean().iloc[-1]:,.0f}"
            )
        
        st.markdown("---")
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📈 Price Chart", "📊 Technical Indicators", "📋 Data Table"])
        
        with tab1:
            # Create subplot for price and volume
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.7, 0.3]
            )
            
            # Add price chart
            if chart_type == "Candlestick":
                fig.add_trace(go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name="Price",
                    showlegend=True
                ), row=1, col=1)
            elif chart_type == "Line":
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df['Close'],
                    mode='lines',
                    name='Close Price',
                    line=dict(color='#1f77b4', width=2)
                ), row=1, col=1)
            else:  # OHLC
                fig.add_trace(go.Ohlc(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name="Price"
                ), row=1, col=1)
            
            # Add SMA
            if show_sma and df['SMA'].notna().any():
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df['SMA'],
                    mode='lines',
                    name=f'SMA {sma_period}',
                    line=dict(color='orange', width=1.5)
                ), row=1, col=1)
            
            # Add EMA
            if show_ema and df['EMA'].notna().any():
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df['EMA'],
                    mode='lines',
                    name=f'EMA {ema_period}',
                    line=dict(color='red', width=1.5)
                ), row=1, col=1)
            
            # Add volume bars
            colors = ['red' if df['Close'].iloc[i] < df['Open'].iloc[i] else 'green' for i in range(len(df))]
            fig.add_trace(go.Bar(
                x=df.index,
                y=df['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.5
            ), row=2, col=1)
            
            # Update layout
            fig.update_layout(
                title=f'{ticker.upper()} Stock Price Analysis',
                yaxis_title='Price (USD)',
                xaxis_title='Date',
                template='plotly_dark',
                height=600,
                hovermode='x unified'
            )
            
            fig.update_yaxis(title="Volume", row=2, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            if show_rsi:
                # RSI Chart
                fig_rsi = make_subplots(rows=1, cols=1)
                
                fig_rsi.add_trace(go.Scatter(
                    x=df.index,
                    y=df['RSI'],
                    mode='lines',
                    name='RSI',
                    line=dict(color='purple', width=2)
                ))
                
                # Add overbought/oversold lines
                fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
                fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
                fig_rsi.add_hline(y=50, line_dash="dot", line_color="gray")
                
                fig_rsi.update_layout(
                    title=f'{ticker.upper()} - Relative Strength Index (RSI)',
                    yaxis_title='RSI Value',
                    template='plotly_dark',
                    height=400
                )
                
                st.plotly_chart(fig_rsi, use_container_width=True)
                
                # RSI Interpretation
                current_rsi = df['RSI'].iloc[-1]
                st.info(f"**Current RSI:** {current_rsi:.2f}")
                if current_rsi > 70:
                    st.warning("⚠️ Stock is in overbought territory. Potential correction ahead.")
                elif current_rsi < 30:
                    st.success("✅ Stock is in oversold territory. Potential buying opportunity.")
                else:
                    st.info("📊 Stock is in neutral territory.")
            else:
                st.info("RSI is disabled. Enable it in the sidebar to view RSI analysis.")
        
        with tab3:
            # Display data table
            display_df = df.copy()
            display_df.index = display_df.index.strftime('%Y-%m-%d')
            st.dataframe(display_df, use_container_width=True, height=400)
            
            # CSV Export
            st.markdown("---")
            st.subheader("📥 Export Data")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Export to CSV", type="primary"):
                    csv_data = df.to_csv()
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"{ticker}_{start_date}_{end_date}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                # Additional export options
                export_format = st.selectbox("Export Format", ["Full Data", "Last 30 Days", "Last 90 Days"])
                if export_format == "Last 30 Days":
                    export_df = df.tail(30)
                elif export_format == "Last 90 Days":
                    export_df = df.tail(90)
                else:
                    export_df = df
                
                st.download_button(
                    label=f"Download {export_format}",
                    data=export_df.to_csv(),
                    file_name=f"{ticker}_{export_format.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
        
        # Performance Summary
        st.markdown("---")
        st.subheader("📊 Performance Summary")
        
        # Calculate returns
        daily_returns = df['Close'].pct_change()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "1-Week Return",
                f"{((df['Close'].iloc[-1] / df['Close'].iloc[-5]) - 1) * 100:.2f}%" if len(df) >= 5 else "N/A"
            )
        
        with col2:
            st.metric(
                "1-Month Return",
                f"{((df['Close'].iloc[-1] / df['Close'].iloc[-20]) - 1) * 100:.2f}%" if len(df) >= 20 else "N/A"
            )
        
        with col3:
            st.metric(
                "3-Month Return",
                f"{((df['Close'].iloc[-1] / df['Close'].iloc[-60]) - 1) * 100:.2f}%" if len(df) >= 60 else "N/A"
            )
        
        with col4:
            st.metric(
                "YTD Return",
                f"{((df['Close'].iloc[-1] / df[df.index.year == date.today().year]['Close'].iloc[0]) - 1) * 100:.2f}%" if len(df[df.index.year == date.today().year]) > 0 else "N/A"
            )
        
        # Additional statistics
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📈 Price Statistics")
            st.write(f"**Highest Price:** ${df['High'].max():.2f}")
            st.write(f"**Lowest Price:** ${df['Low'].min():.2f}")
            st.write(f"**Average Price:** ${df['Close'].mean():.2f}")
            st.write(f"**Volatility (Daily):** {daily_returns.std() * 100:.2f}%")
        
        with col2:
            st.markdown("### 📊 Volume Statistics")
            st.write(f"**Average Daily Volume:** {df['Volume'].mean():,.0f}")
            st.write(f"**Max Daily Volume:** {df['Volume'].max():,.0f}")
            st.write(f"**Min Daily Volume:** {df['Volume'].min():,.0f}")
            st.write(f"**Current/ Avg Ratio:** {df['Volume'].iloc[-1] / df['Volume'].mean():.2f}x")
        
        with col3:
            if show_rsi:
                st.markdown("### 🎯 RSI Analysis")
                st.write(f"**Current RSI:** {current_rsi:.2f}")
                st.write(f"**Max RSI:** {df['RSI'].max():.2f}")
                st.write(f"**Min RSI:** {df['RSI'].min():.2f}")
                st.write(f"**Avg RSI:** {df['RSI'].mean():.2f}")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check the stock ticker symbol and try again.")
else:
    st.info("Please enter a stock ticker symbol in the sidebar to begin analysis.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8rem;">
    <p>Data provided by Yahoo Finance | Dashboard created with Streamlit, Plotly, and yfinance</p>
    <p>This dashboard is for informational purposes only. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)