# slide : https://www.canva.com/design/DAGoSCXEQc4/e-IcPqrmpWwPmSsQ14pC3g/edit?utm_content=DAGoSCXEQc4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
# Web : https://tni-ndr-2213110949-6jw8f9zolcagwgyaryuvuk.streamlit.app/
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import matplotlib
import seaborn as sns
import matplotlib.dates as mdates
import yfinance as yf
import plotly.graph_objects as go
# ---------------- Global Settings ----------------
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
sns.set(style="whitegrid")
st.set_page_config(page_title="หุ้น Realty Income (O)", layout="wide")

# ---------------- Custom CSS Styling ----------------
st.markdown("""
    <style>
        .main {
            background-color: #f9fafb;
            padding: 2rem 3rem;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        h1, h2, h3 {
            color: #222;
            font-weight: 700;
            margin-bottom: 0.6rem;
        }
        h4 {
            margin-bottom: 0.4rem;
            font-weight: 600;
        }
        .block-container {
            max-width: 1280px;  
            margin-left: auto;
            margin-right: auto;
        }
        .dataframe th, .dataframe td {
            text-align: center !important;
            font-size: 13px !important;
            padding: 6px 10px !important;
        }
        .stDataFrame {
            border: 1px solid #e1e4e8;
            border-radius: 10px;
            box-shadow: 0 1px 4px rgb(27 31 35 / 0.1);
        }
        .highlight-box {
            padding: 6px 10px;
            border-radius: 6px;
            margin-top: 6px;
            font-size: 20px;
        }
        .highlight-high {
            background-color: #e6f4ea;
            border-left: 5px solid #34a853;
            color: #0c5b32;
        }
        .highlight-low {
            background-color: #fce8e6;
            border-left: 5px solid #d93025;
            color: #a11a11;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.markdown("""
    <h1 style='text-align: center;'>📊 Realty Income Corp (O)</h1>
""", unsafe_allow_html=True)

# ---------------- Load and Clean Data ----------------
df = pd.read_excel("Book1.xlsx", skiprows=1)
df.columns = ["Date", "Price", "Open", "High", "Low", "Vol.", "Change%", "NYSE index"]
df = df[~df["Date"].isna() & ~df["Date"].astype(str).str.contains("Date")]
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce")
df = df.dropna(subset=["Date"])

st.sidebar.title("📅 เลือกช่วงเวลา")
st.sidebar.markdown("🛈 เลือกช่วงเวลาที่ต้องการดูแนวโน้มราคาย้อนหลัง")

# ตัวเลือกช่วงเวลา
period_option = st.sidebar.selectbox(
    "ดูข้อมูลย้อนหลัง:",
    ["7 วัน", "1 เดือน", "2 เดือน", "3 เดือน", "4 เดือน", "5 เดือน", "6 เดือน"]
)

# คำนวณวันที่เริ่มต้น
latest_date = df["Date"].max()
if "วัน" in period_option:
    days = int(period_option.split()[0])
    start_date = latest_date - pd.DateOffset(days=days)
    label = f"{days} วันล่าสุด"
else:
    months = int(period_option.split()[0])
    start_date = latest_date - pd.DateOffset(months=months)
    label = f"{months} เดือนล่าสุด"

# กรองข้อมูลตามช่วงเวลา
df_filtered = df[df["Date"] >= start_date].copy()
df_filtered["Date"] = df_filtered["Date"].dt.date

# แสดงผลใน Sidebar
st.sidebar.markdown(f"### ข้อมูลย้อนหลัง **{label}**")
st.sidebar.markdown(f"({start_date.date()} - {latest_date.date()})")
st.sidebar.markdown(f"📊 พบข้อมูลทั้งหมด: **{len(df_filtered)} แถว**")

# ---------------- สรุปราคาปิด ----------------
st.sidebar.markdown("## 💼 สรุปข้อมูลราคาปิดย้อนหลัง")

price_stats = df_filtered["Price"].describe()

st.sidebar.markdown(f"""
- 📅 ช่วงเวลา: **{label}**  
- 📝 ราคาเฉลี่ย: **${price_stats['mean']:.2f}**
- 📉 ราคาต่ำสุด: **${price_stats['min']:.2f}**
- 📈 ราคาสูงสุด: **${price_stats['max']:.2f}**
- 🧮 ส่วนเบี่ยงเบนมาตรฐาน: **${price_stats['std']:.2f}**
- 🔢 จำนวนข้อมูล: **{int(price_stats['count'])} วัน**
""")

# ---------------- Display Data and Summary ----------------
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 📄 ตัวอย่างข้อมูลล่าสุด")
    df_show = df_filtered.head(8).reset_index(drop=True)
    df_show.index += 1
    df_show.index.name = "ลำดับ"
    st.dataframe(df_show, use_container_width=True)

with col2:
    st.markdown("#### 📈 สถิติเบื้องต้นของราคาปิด")
    st.write(df_filtered["Price"].describe())

# ---------------- Highlight Max & Min Prices ----------------
st.markdown("### ⬆️⬇️ ราคาสูงสุดและต่ำสุดในช่วงนี้")

max_price = df_filtered["Price"].max()
max_date = df_filtered.loc[df_filtered["Price"] == max_price, "Date"].values[0]
min_price = df_filtered["Price"].min()
min_date = df_filtered.loc[df_filtered["Price"] == min_price, "Date"].values[0]
avg_price = df_filtered["Price"].mean()

max_change = ((max_price - avg_price) / avg_price) * 100
min_change = ((min_price - avg_price) / avg_price) * 100

col3, col4 = st.columns(2)
with col3:
    st.markdown(f"""
    <div class="highlight-box highlight-high">
        <h4>📈 ราคาสูงสุด</h4>
        <p style="font-size:30px;"><b>${max_price:.2f}</b></p>
        <p>ณ วันที่ {max_date}</p>
        <p>สูงกว่าค่าเฉลี่ย {max_change:.2f}%</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="highlight-box highlight-low">
        <h4>📉 ราคาต่ำสุด</h4>
        <p style="font-size:30px;"><b>${min_price:.2f}</b></p>
        <p>ณ วันที่ {min_date}</p>
        <p>ต่ำกว่าค่าเฉลี่ย {abs(min_change):.2f}%</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- Candlestick Chart ----------------
st.markdown("## 🔕️ กราฟ Candlestick ของราคาหุ้น")

with st.expander("📌 คลิกเพื่อดูกราฟ Candlestick"):
    # เตรียมข้อมูลสำหรับ Candlestick
    candle_df = df_filtered.copy()
    candle_df["Date"] = pd.to_datetime(candle_df["Date"])

    # ใช้ go.Figure บริสทาศ Candlestick chart เพียงส่วนเดียวบนี้
    fig_candle = go.Figure(data=[go.Candlestick(
        x=candle_df["Date"],
        open=candle_df["Open"],
        high=candle_df["High"],
        low=candle_df["Low"],
        close=candle_df["Price"],
        increasing_line_color='green',
        decreasing_line_color='red',
        name="O"
    )])

    fig_candle.update_layout(
        title="Candlestick Chart - Realty Income (O)",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        width=1000,
        height=500
    )

    st.plotly_chart(fig_candle, use_container_width=True)

# ---------------- Plot Price Trend with Linear Regression in Expander ----------------
st.markdown("## 📊 แนวโน้มราคาหุ้น")

df_sorted = df_filtered.sort_values("Date")
X = pd.to_datetime(df_sorted["Date"]).map(pd.Timestamp.toordinal).values.reshape(-1, 1)
y = df_sorted["Price"].values

model = LinearRegression()
model.fit(X, y)
trend = model.predict(X)

with st.expander("🔍 คลิกเพื่อดูกราฟแนวโน้มราคาหุ้น "):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=df_sorted["Date"], y=y, label="Actual Price", ax=ax, linewidth=1.5)
    sns.lineplot(x=df_sorted["Date"], y=trend, label="Trend (Linear Regression)", ax=ax, linestyle="--", color="red", linewidth=1.5)

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    ax.set_title("Realty Income Corp (O)", fontsize=10, weight='bold')
    ax.set_xlabel("Date", fontsize=8)
    ax.set_ylabel("Price (USD)", fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.legend(fontsize=8)
    ax.grid(True)

    st.pyplot(fig)

st.markdown("## 📉 ปริมาณการซื้อขายและราคาปิด")

with st.expander("🔍 คลิกเพื่อดูกราฟปริมาณการซื้อขาย"):
    fig_vol, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    # แปลงค่า Volume
    volume_values = df_sorted["Vol."].apply(lambda x: float(str(x).replace("M", ""))) * 1_000_000

    # Plot bar
    ax1.bar(df_sorted["Date"], volume_values, color="#c0d6e4", width=1.5, label="Volume", alpha=0.6)

    # แสดงค่าบน bar
    for x, v in zip(df_sorted["Date"], volume_values):
        ax1.text(x, v, f"{v / 1_000_000:.1f}M", fontsize=7, ha='center', va='bottom', rotation=90, color='black')

    # Plot line ราคาปิด
    sns.lineplot(x=df_sorted["Date"], y=df_sorted["Price"], ax=ax2, color="#1f77b4", label="Price", linewidth=2)

    ax1.set_ylabel("Volume", fontsize=9)
    ax2.set_ylabel("Price (USD)", fontsize=9)
    ax1.set_xlabel("Date", fontsize=9)

    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    ax1.tick_params(axis='y', labelsize=8)
    ax2.tick_params(axis='y', labelsize=8)
    ax1.tick_params(axis='x', labelsize=8)

    ax1.grid(True)
    fig_vol.tight_layout()

    fig_vol.legend(loc="upper left", fontsize=8)
    st.pyplot(fig_vol)

st.markdown("## 🌐 แนวโน้มราคาหุ้นล่าสุด (Real-time) จากตลาด")

ticker_symbol = "O"  # Realty Income Corp
df_yf = yf.download(ticker_symbol, period="6mo", interval="1d")
df_yf = df_yf.reset_index()
df_yf = df_yf[["Date", "Close"]].rename(columns={"Close": "Price"}).dropna()

# เตรียมข้อมูลสำหรับเทรนด์ไลน์
X_yf = pd.to_datetime(df_yf["Date"]).map(pd.Timestamp.toordinal).values.reshape(-1, 1)
y_yf = df_yf["Price"].values.flatten()   

model_yf = LinearRegression()
model_yf.fit(X_yf, y_yf)
trend_yf = model_yf.predict(X_yf).flatten()

# วาดกราฟใน expander
with st.expander("🔍 คลิกเพื่อดูกราฟราคาแบบ real time (ย้อนหลัง 6 เดือน)"):

    fig2, ax2 = plt.subplots(figsize=(12, 6))

    sns.lineplot(x=df_yf["Date"], y=df_yf["Price"].values.flatten(), label="Actual Price", ax=ax2, linewidth=1.5)  
    sns.lineplot(x=df_yf["Date"], y=trend_yf, label="Trend (Linear)", ax=ax2, linestyle="--", color="orange", linewidth=1.5)  

    ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    ax2.set_title("Realty Income Corp (O) - data from yfinance", fontsize=10, weight='bold')
    ax2.set_xlabel("Date", fontsize=8)
    ax2.set_ylabel("Price (USD)", fontsize=8)
    ax2.tick_params(axis='both', which='major', labelsize=8)
    ax2.legend(fontsize=8)
    ax2.grid(True)

    st.pyplot(fig2)

    


    
