#!/usr/bin/env python3
"""Streamlit Web Dashboard for K-Eye Forex Trading Bot.

Run with: streamlit run dashboard.py

This provides a real-time paper trading dashboard with:
- Live price charts with indicators
- Trade execution controls
- Performance analytics
- Equity curve visualization
"""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import numpy as np

from app.config import settings
from app.market_data import generate_sample_prices, PriceSeries
from app.simulator import run_simulation, generate_signal
from app.reporting import summarize_trades
from app.indicators import calculate_ema, calculate_rsi


# Page config
st.set_page_config(
    page_title="K-Eye Trading Bot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .header-style {
        font-size: 32px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .warning-banner {
        background-color: #fff2cc;
        border: 1px solid #ffc107;
        color: #856404;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def generate_prices_cached(length: int, seed: int = 42) -> PriceSeries:
    """Cache price generation to avoid regenerating on reruns."""
    np.random.seed(seed)
    return generate_sample_prices(length=length)


def create_price_chart(prices: list, ema_fast: list, ema_slow: list) -> go.Figure:
    """Create an interactive price chart with EMAs."""
    fig = go.Figure()

    # Price candlestick (simplified)
    fig.add_trace(go.Scatter(
        x=list(range(len(prices))),
        y=prices,
        mode='lines',
        name='Price',
        line=dict(color='#1f77b4', width=2),
    ))

    # Fast EMA
    fig.add_trace(go.Scatter(
        x=list(range(len(ema_fast))),
        y=ema_fast,
        mode='lines',
        name=f'EMA {settings.fast_ema}',
        line=dict(color='#ff7f0e', width=1, dash='dash'),
    ))

    # Slow EMA
    fig.add_trace(go.Scatter(
        x=list(range(len(ema_slow))),
        y=ema_slow,
        mode='lines',
        name=f'EMA {settings.slow_ema}',
        line=dict(color='#2ca02c', width=1, dash='dash'),
    ))

    fig.update_layout(
        title='EURUSD Price & EMA Crossovers',
        xaxis_title='Bar',
        yaxis_title='Price (USD)',
        hovermode='x unified',
        height=400,
        template='plotly_white',
    )

    return fig


def create_rsi_chart(rsi_values: list) -> go.Figure:
    """Create RSI indicator chart."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(range(len(rsi_values))),
        y=rsi_values,
        mode='lines',
        name='RSI',
        line=dict(color='#d62728', width=2),
        fill='tozeroy',
        fillcolor='rgba(214, 39, 40, 0.1)',
    ))

    # Overbought/Oversold zones
    fig.add_hline(y=70, line_dash='dash', line_color='red', annotation_text='Overbought (70)')
    fig.add_hline(y=30, line_dash='dash', line_color='green', annotation_text='Oversold (30)')

    fig.update_layout(
        title=f'RSI ({settings.rsi_period})',
        xaxis_title='Bar',
        yaxis_title='RSI',
        hovermode='x unified',
        height=300,
        template='plotly_white',
    )

    return fig


def create_equity_chart(equity_curve: list) -> go.Figure:
    """Create equity curve visualization."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(range(len(equity_curve))),
        y=equity_curve,
        mode='lines',
        name='Equity',
        line=dict(color='#17becf', width=2),
        fill='tozeroy',
        fillcolor='rgba(23, 190, 207, 0.1)',
    ))

    fig.update_layout(
        title='Account Equity Over Time',
        xaxis_title='Bar',
        yaxis_title='Balance (USD)',
        hovermode='x unified',
        height=300,
        template='plotly_white',
    )

    return fig


def create_trades_table(trades: list) -> pd.DataFrame:
    """Convert trades to a displayable DataFrame."""
    if not trades:
        return pd.DataFrame(columns=['Side', 'Entry Price', 'Quantity', 'Exit Price', 'P&L', 'Status'])

    data = []
    for trade in trades:
        data.append({
            'Side': trade.side,
            'Entry Price': f"${trade.entry_price:.5f}",
            'Quantity': f"{trade.quantity:.2f}",
            'Exit Price': f"${trade.exit_price:.5f}" if trade.exit_price else '--',
            'P&L': f"${trade.pnl:.4f}" if trade.pnl is not None else '--',
            'Status': trade.status,
        })

    return pd.DataFrame(data)


def main():
    """Main dashboard app."""
    # Header
    st.markdown(
        '<div class="header-style">📈 K-Eye Forex Trading Bot Dashboard</div>',
        unsafe_allow_html=True,
    )

    # Warning banner
    st.markdown(
        '<div class="warning-banner">'
        '⚠️ <strong>EXPERIMENTAL - PAPER TRADING ONLY</strong><br/>'
        'This is a demo simulator. NOT FOR LIVE TRADING. No real money is at risk.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Sidebar controls
    st.sidebar.header('⚙️ Configuration')
    
    starting_balance = st.sidebar.number_input(
        'Starting Balance ($)',
        min_value=1.0,
        max_value=10000.0,
        value=float(settings.starting_balance),
        step=0.5,
    )

    price_length = st.sidebar.slider(
        'Price Bars to Generate',
        min_value=20,
        max_value=200,
        value=60,
        step=10,
    )

    fast_ema = st.sidebar.slider(
        'Fast EMA Period',
        min_value=3,
        max_value=20,
        value=settings.fast_ema,
    )

    slow_ema = st.sidebar.slider(
        'Slow EMA Period',
        min_value=10,
        max_value=50,
        value=settings.slow_ema,
    )

    rsi_period = st.sidebar.slider(
        'RSI Period',
        min_value=7,
        max_value=21,
        value=settings.rsi_period,
    )

    risk_pct = st.sidebar.slider(
        'Risk per Trade (%)',
        min_value=0.1,
        max_value=5.0,
        value=settings.risk_per_trade * 100,
        step=0.1,
    )

    st.sidebar.markdown('---')
    run_button = st.sidebar.button('▶️ Run Simulation', use_container_width=True)

    # Main content
    if run_button:
        with st.spinner('Running simulation...'):
            # Generate prices
            prices = generate_prices_cached(price_length)
            prices_list = prices.prices

            # Calculate indicators
            ema_fast = calculate_ema(prices_list, fast_ema)
            ema_slow = calculate_ema(prices_list, slow_ema)
            rsi = calculate_rsi(prices_list, rsi_period)

            # Run simulation
            result = run_simulation(
                price_series=prices_list,
                starting_balance=starting_balance,
                symbol='EURUSD',
                fast_period=fast_ema,
                slow_period=slow_ema,
                rsi_period=rsi_period,
                risk_per_trade=risk_pct / 100.0,
                max_positions=1,
                stop_loss_pct=0.005,
            )

            # Generate report
            report = summarize_trades(result.trades, starting_balance)

        # Charts section
        st.subheader('📊 Market Analysis')
        col1 = st.columns(1)[0]
        with col1:
            fig_price = create_price_chart(prices_list, ema_fast, ema_slow)
            st.plotly_chart(fig_price, use_container_width=True)

        col2, col3 = st.columns(2)
        with col2:
            fig_rsi = create_rsi_chart(rsi)
            st.plotly_chart(fig_rsi, use_container_width=True)

        with col3:
            fig_equity = create_equity_chart(result.equity_curve)
            st.plotly_chart(fig_equity, use_container_width=True)

        # Performance metrics
        st.subheader('💰 Performance Summary')
        metric_cols = st.columns(5)

        with metric_cols[0]:
            st.metric(
                'Initial Balance',
                f'${starting_balance:.2f}',
            )

        with metric_cols[1]:
            st.metric(
                'Final Balance',
                f'${report.final_balance:.2f}',
                delta=f'${report.net_pnl:.2f}',
                delta_color='normal' if report.net_pnl >= 0 else 'off',
            )

        with metric_cols[2]:
            st.metric(
                'Net P&L',
                f'${report.net_pnl:.4f}',
                f'{(report.net_pnl/starting_balance)*100:.2f}%',
            )

        with metric_cols[3]:
            st.metric(
                'Total Trades',
                int(report.total_trades),
            )

        with metric_cols[4]:
            st.metric(
                'Win Rate',
                f'{report.win_rate:.1f}%',
            )

        # Trades table
        if result.trades:
            st.subheader('📋 Trade Log')
            trades_df = create_trades_table(result.trades)
            st.dataframe(trades_df, use_container_width=True, hide_index=True)
        else:
            st.info('No trades executed in this simulation.')

        # Strategy signals
        st.subheader('🎯 Latest Signals')
        latest_signal = generate_signal(
            prices_list,
            fast_period=fast_ema,
            slow_period=slow_ema,
            rsi_period=rsi_period,
        )
        col_signal = st.columns(1)[0]
        with col_signal:
            if latest_signal.action == 'BUY':
                st.success(f'Signal: {latest_signal.action} | {latest_signal.reason}')
            elif latest_signal.action == 'SELL':
                st.error(f'Signal: {latest_signal.action} | {latest_signal.reason}')
            else:
                st.warning(f'Signal: {latest_signal.action} | {latest_signal.reason}')

    else:
        # Initial state
        st.info(
            '👈 Use the **Configuration** panel on the left to set trading parameters, '
            'then click **Run Simulation** to start the paper trading demo.'
        )
        st.markdown(
            """
            ### About This Dashboard
            
            This is a **paper trading simulator** for learning algorithmic trading:
            
            - **Price Charts**: Visualize EURUSD with EMA crossovers
            - **RSI Indicator**: Monitor momentum and overbought/oversold conditions
            - **Equity Curve**: Track account balance over time
            - **Trade Log**: Review all executed trades and P&L
            - **Performance Metrics**: Win rate, total P&L, and more
            
            ### How It Works
            
            1. **Set Parameters**: Choose EMA periods, RSI settings, and risk per trade
            2. **Run Simulation**: Generate synthetic price data and execute trades automatically
            3. **Analyze Results**: Review charts, trades, and performance statistics
            4. **Experiment**: Adjust parameters and re-run to test different strategies
            
            ### Trading Rules
            
            - **BUY**: Fast EMA > Slow EMA AND RSI < 70
            - **SELL**: Fast EMA < Slow EMA AND RSI > 30
            - **STOP LOSS**: 0.5% below entry price
            - **POSITION LIMIT**: Maximum 1 open trade at a time
            
            ---
            
            ⚠️ **Remember**: This is paper trading only. No real money is involved.
            """
        )


if __name__ == '__main__':
    main()
