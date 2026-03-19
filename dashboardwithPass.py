import streamlit as st

password = st.text_input("Kashish1404912", type="password")

if password != "1234":
    st.stop()

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import yfinance as yf
import pandas as pd
import ta
import winsound
from datetime import datetime

# =========================
# EXACT 5-MIN CANDLE REFRESH
# =========================
now = datetime.now()
next_minute = (now.minute // 5 + 1) * 5
if next_minute == 60:
    next_run = now.replace(hour=now.hour+1, minute=0, second=2, microsecond=0)
else:
    next_run = now.replace(minute=next_minute, second=2, microsecond=0)

wait_ms = int((next_run - now).total_seconds() * 1000)
st_autorefresh(interval=wait_ms, key="refresh")

st.set_page_config(page_title="PRO Intraday Scanner", layout="wide")

# =========================
# STYLE
# =========================
st.markdown("""
<style>
body {background-color:#0f172a; color:white;}
.stButton>button {background-color:#00ffcc;color:black;font-weight:bold;border-radius:10px;}
</style>
""", unsafe_allow_html=True)

# =========================
# ALERT SOUND
# =========================
def strong_alert():
    for _ in range(3):
        winsound.Beep(2500, 500)

# =========================
# SAFE CLOSE
# =========================
def safe_close(df):
    try:
        return df["Close"].iloc[-1].item(), df["Close"].iloc[-2].item()
    except:
        return 0,0

# =========================
# MARKET DIRECTION
# =========================
def get_market_direction(n_p, n_prev, b_p, b_prev):
    if n_p > n_prev and b_p > b_prev:
        return "BULLISH"
    elif n_p < n_prev and b_p < b_prev:
        return "BEARISH"
    else:
        return "SIDEWAYS"

# =========================
# SAFE DOWNLOAD
# =========================
def safe_download(ticker, period="5d", interval="1d"):
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        if df.empty or len(df) < 2:
            return None
        return df
    except:
        return None

# =========================
# INDEX DATA
# =========================
nifty = safe_download("^NSEI", "5d", "1d")
if nifty is None:
    nifty = safe_download("NSEI.NS", "5d", "1d")

bank = safe_download("^NSEBANK", "5d", "1d")
dow = safe_download("^DJI", "1d", "5m")
gold = safe_download("GC=F", "1d", "5m")
crude = safe_download("CL=F", "1d", "5m")
vix = safe_download("^INDIAVIX", "1d", "5m")

n_prev = float(nifty["Close"].iloc[-2]) if nifty is not None else 0
b_prev = float(bank["Close"].iloc[-2]) if bank is not None else 0

n_p = float(nifty["Close"].iloc[-1]) if nifty is not None else 0
b_p = float(bank["Close"].iloc[-1]) if bank is not None else 0

d_p, d_prev = safe_close(dow) if dow is not None else (0,0)
g_p, g_prev = safe_close(gold) if gold is not None else (0,0)
c_p, c_prev = safe_close(crude) if crude is not None else (0,0)
v_p, v_prev = safe_close(vix) if vix is not None else (0,0)

market = get_market_direction(n_p, n_prev, b_p, b_prev)

# =========================
# UI
# =========================
st.markdown("<h2 style='text-align:center; margin-top:-125px;'>🚀 ChartArt Intraday Directional Scanner</h2>", unsafe_allow_html=True)

st.markdown(
    f"<p style='text-align:center; color:gray; margin-top:-90px;'>Last Update: {datetime.now().strftime('%H:%M:%S')} &nbsp;&nbsp; | &nbsp;&nbsp; Next Candle Run: {next_run.strftime('%H:%M:%S')}</p>",
    unsafe_allow_html=True

)

def index_display(price, prev_close, name):
    if price > prev_close:
        color = "#2CFF05"; arrow = "⬆️"
    elif price < prev_close:
        color = "#FF46A2"; arrow = "⬇️"
    else:
        color = "#FDBE02"; arrow = "➡️"
   # return f"<div style='background:#1e293b;padding:10px;border-radius:10px;text-align:center'><b style='color:{color}'>{name}</b><br><span style='color:{color}'>{price:.2f}</span><br>{arrow}</div>"
    return f"<div style='background:#1e293b;padding:10px;border-radius:10px;text-align:center; margin-top:-70px;'><b style='color:{color}'>{name}</b><br><span style='color:{color}'>{price:.2f}</span><br>{arrow}</div>"    
cols = st.columns(6)
cols[0].markdown(index_display(n_p,n_prev,"Nifty"), unsafe_allow_html=True)
cols[1].markdown(index_display(b_p,b_prev,"BankNifty"), unsafe_allow_html=True)
cols[2].markdown(index_display(d_p,d_prev,"Dow"), unsafe_allow_html=True)
cols[3].markdown(index_display(g_p,g_prev,"Gold"), unsafe_allow_html=True)
cols[4].markdown(index_display(c_p,c_prev,"CRUDEOIL '$'"), unsafe_allow_html=True)
cols[5].markdown(index_display(v_p,v_prev,"VIX"), unsafe_allow_html=True)

st.subheader(f"Market Direction: {market}")

# =========================
# STOCK LIST (UNCHANGED)
# =========================
stocks = { 

"ABCAPITAL.NS": "ADITYA BIRLA CAPITAL LIMITED",
"ABFRL.NS": "ADITYA BIRLA FASHION AND RETAIL LIMITED",
"ACC.NS": "ACC LIMITED",
"ADANIENSOL.NS": "ADANI ENERGY SOLUTIONS LTD",
"ADANIENT.NS": "ADANI ENTERPRISES LIMITED",
"ADANIGREEN.NS": "ADANI GREEN ENERGY LIMITED",
"ADANIPORTS.NS": "ADANI PORTS AND SPECIAL ECONOMIC ZONE LIMITED",
"ALKEM.NS": "ALKEM LABORATORIES LTD",
"AMBUJACEM.NS": "AMBUJACEM",
"ANGELONE.NS": "ANGEL ONE LIMITED",
"APLAPOLLO.NS": "APL APOLLO TUBES LIMITED",
"APOLLOHOSP.NS": "APOLLO HOSPITALS ENT LTD",
"APOLLOTYRE.NS": "APOLLO TYRES LIMITED",
"ASHOKLEY.NS": "ASHOK LEYLAND LIMITED",
"ASIANPAINT.NS": "ASIAN PAINTS LIMITED",
"ASTRAL.NS": "ASTRAL LIMITED",
"ATGL.NS": "ADANI TOTAL GAS LIMITED",
"AUBANK.NS": "AU SMALL FINANCE BANK LIMITED",
"AUROPHARMA.NS": "AUROBINDO PHARMA LIMITED",
"AXISBANK.NS": "AXIS BANK LIMITED",
"BAJAJ-AUTO.NS": "BAJAJ AUTO LIMITED",
"BAJAJFINSV.NS": "BAJAJ FINSERV LIMITED",
"BAJFINANCE.NS": "BAJAJ  FINANCE LTD",
"BALKRISIND.NS": "BALKRISHNA INDUSTRIES LIMITED",
"BANDHANBNK.NS": "BANDHAN BANK LIMITED",
"BANKBARODA.NS": "BANK OF BARODA",
"BANKINDIA.NS": "BANK OF INDIA",
"BEL.NS": "BHARAT ELECTRONICS LIMITED",
"BERGEPAINT.NS": "BERGER PAINTS INDIA LIMITED",
"BHARATFORG.NS": "BHARAT FORGE LIMITED",
"BHARTIARTL.NS": "BHARTI AIRTEL LIMITED",
"BHEL.NS": "BHARAT HEAVY ELECTRICALS LIMITED",
"BIOCON.NS": "BIOCON",
"BPCL.NS": "BHARAT PETROLEUM CORPORATION LIMITED",
"BRITANNIA.NS": "BRITANNIA INDUSTRIES LIMITED",
"BSE.NS": "BSE LIMITED",
"BSOFT.NS": "BIRLASOFT LIMITED",
"CAMS.NS": "COMPUTER AGE MANAGEMENT SERVICES LIMITED",
"CANBK.NS": "CANARA BANK",
"CDSL.NS": "CENTRAL DEPOSITORY SERVICES (INDIA)  LTD",
"CESC.NS": "CESC LIMITED",
"CGPOWER.NS": "CG POWER AND INDUSTRIAL SOLUTIONS LIMITED",
"CHAMBLFERT.NS": "CHAMBAL FERTILISERS & CHEMICALS LIMITED",
"CHOLAFIN.NS": "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED",
"CIPLA.NS": "CIPLA LIMITED",
"COALINDIA.NS": "COALINDIA",
"COFORGE.NS": "COFORGE LIMITED",
"COLPAL.NS": "COLGATE PALMOLIVE (INDIA) LIMITED",
"CONCOR.NS": "CONTAINER CORPORATION OF INDIA LIMITED",
"CROMPTON.NS": "CROMPTON GREAVES CONSUMER ELECTRICAL LIMITED",
"CUMMINSIND.NS": "CUMMINS INDIA LIMITED",
"CYIENT.NS": "CYIENT LIMITED",
"DABUR.NS": "DABUR INDIA LIMITED",
"DALBHARAT.NS": "DALMIA BHARAT LIMITED",
"DEEPAKNTR.NS": "DEEPAK NITRITE LIMITED",
"DELHIVERY.NS": "DELHIVERY LIMITED",
"DIVISLAB.NS": "DIVI'S LABORATORIES LIMITED",
"DIXON.NS": "DIXON TECHNOLOGIES (INDIA) LIMITED",
"DLF.NS": "DLF LIMITED",
"DMART.NS": "AVENUE SUPERMARTS LIMITED",
"DRREDDY.NS": "DR. REDDYS LABORATORIES LIMITED",
"EICHERMOT.NS": "EICHER MOTORS LIMITED",
"ESCORTS.NS": "ESCORTS KUBOTA LIMITED",
"ETERNAL.NS": "ETERNAL LIMITED",
"EXIDEIND.NS": "EXIDE INDUSTRIES LIMITED",
"FEDERALBNK.NS": "FEDERAL BANK LIMITED",
"GAIL.NS": "GAIL (INDIA) LIMITED",
"GLENMARK.NS": "GLENMARK PHARMACEUTICALS",
"GMRAIRPORT.NS": "GMR AIRPORTS LIMITED",
"GODREJCP.NS": "GODREJ CONSUMER PRODUCTS LIMITED",
"GODREJPROP.NS": "GODREJ PROPERTIES LIMITED",
"GRANULES.NS": "GRANULES INDIA LIMITED",
"GRASIM.NS": "GRASIM INDUSTRIES LIMITED",
"HAL.NS": "HINDUSTAN AERONAUTICS LIMITED",
"HAVELLS.NS": "HAVELLS INDIA LIMITED",
"HCLTECH.NS": "HCL TECHNOLOGIES LIMITED",
"HDFCAMC.NS": "HDFC ASSET MANAGEMENT COMPANY LIMITED",
"HDFCBANK.NS": "HDFC BANK LIMITED",
"HDFCLIFE.NS": "HDFC LIFE INSURANCE COMPANYLTD",
"HEROMOTOCO.NS": "HERO MOTOCORP LIMITED",
"HFCL.NS": "HFCL LIMITED",
"HINDALCO.NS": "HINDALCO INDUSTRIES LIMITED",
"HINDCOPPER.NS": "HINDUSTAN COPPER LIMITED",
"HINDPETRO.NS": "HINDUSTAN PETROLEUM CORPORATION LIMITED",
"HINDUNILVR.NS": "HINDUSTAN UNILEVER LIMITED",
"HUDCO.NS": "HOUSING AND URBAN DEVELOPMENT CORP LTD",
"ICICIBANK.NS": "ICICIBANK",
"ICICIGI.NS": "ICICI LOMBARD GENERAL INSURANCE COMPANY LIMITED",
"ICICIPRULI.NS": "ICICI PRUDENTIAL LIFE LTD",
"IDEA.NS": "VODAFONE IDEA LIMITED",
"IDFCFIRSTB.NS": "IDFC FIRST BANK LIMITED",
"IEX.NS": "INDIAN ENERGY EXCHANGE LIMITED",
"IGL.NS": "INDRAPRASTHA GAS LIMITED",
"IIFL.NS": "IIFL FINANCE LIMITED",
"INDHOTEL.NS": "INDIAN HOTELS COMPANY LIMITED",
"INDIANB.NS": "INDIAN BANK",
"INDIGO.NS": "INTERGLOBE AVIATION LIMITED",
"INDUSINDBK.NS": "INDUSIND BANK LIMITED",
"INDUSTOWER.NS": "INDUS TOWERS LIMITED",
"INFY.NS": "INFY",
"IOC.NS": "INDIAN OIL CORPORATION LIMITED",
"IRB.NS": "IRB INFRASTRUCTURE DEVELOP LTD",
"IRCTC.NS": "INDIAN RAILWAY CATERING AND TOURISM COR LTD",
"IREDA.NS": "INDIAN RENEWABLE ENERGY DEVELOPMENT AGENCY LIMITED",
"IRFC.NS": "INDIAN RAILWAY FINANCE CORPORATION LIMITED",
"ITC.NS": "ITC LIMITED",
"JINDALSTEL.NS": "JINDAL STEEL & POWER LTD",
"JIOFIN.NS": "JIO FINANCIAL SERVICES LTD",
"JKCEMENT.NS": "J.K.CEMENT LIMITED.",
"JSL.NS": "JINDAL STAINLESS LIMITED",
"JSWENERGY.NS": "JSW ENERGY LIMITED",
"JSWSTEEL.NS": "JSW STEEL LIMITED",
"JUBLFOOD.NS": "JUBILANT FOODWORKS LIMITED",
"KALYANKJIL.NS": "KALYAN JEWELLERS INDIA LIMITED",
"KEI.NS": "KEI INDUSTRIES LIMITED",
"KOTAKBANK.NS": "KOTAK MAHINDRA BANK LIMITED",
"KPITTECH.NS": "KPIT TECHNOLOGIES LIMITED",
"LAURUSLABS.NS": "LAURUS LABS LIMITED",
"LICHSGFIN.NS": "LIC HOUSING FINANCE LTD",
"LICI.NS": "LIFE INSURANCE CORPORATION OF INDIA",
"LODHA.NS": "MACROTECH DEVELOPERS LIMITED",
"LT.NS": "LARSEN & TOUBRO LTD",
"LTF.NS": "L&T FINANCE LIMITED",
"LTM.NS": "LTIMINDTREE LIMITED",
"LTTS.NS": "L&T TECHNOLOGY SERVICES LIMITED",
"LUPIN.NS": "LUPIN LIMITED",
"M&M.NS": "MAHINDRA & MAHINDRA LTD",
"M&MFIN.NS": "MAHINDRA & MAHINDRA FIN",
"MANAPPURAM.NS": "MANAPPURAM FINANCE LTD",
"MARICO.NS": "MARICO INDUSTRIES LTD",
"MARUTI.NS": "MARUTI SUZUKI INDIA LTD",
"MAXHEALTH.NS": "MAX HEALTHCARE INSTITUTE LIMITED",
"MCX.NS": "MULTI COMMODITY EXCHANGE OF INDIA LTD",
"MFSL.NS": "MAX FINANCIAL SERVICES LIMITED",
"MGL.NS": "MAHANAGAR GAS LIMITED",
"MOTHERSON.NS": "SAMVARDHANA MOTHERSON INTERNATIONAL LIMITED",
"MPHASIS.NS": "MPHASIS LIMITED",
"MUTHOOTFIN.NS": "MUTHOOTFIN",
"NATIONALUM.NS": "NATIONAL ALUMINIUM CO LTD",
"NAUKRI.NS": "INFO EDGE (INDIA) LIMITED",
"NBCC.NS": "NBCC (INDIA) LIMITED",
"NCC.NS": "NCC LIMITED",
"NESTLEIND.NS": "NESTLE INDIA LTD",
"NHPC.NS": "NHPC LIMITED",
"NMDC.NS": "NMDC LIMITED",
"NTPC.NS": "NATIONAL THERMAL POWER CORP",
"NYKAA.NS": "FSN E-COMMERCE VENTURES LIMITED",
"OBEROIRLTY.NS": "OBEROI REALTY LIMITED",
"OFSS.NS": "ORACLE FINANCIAL SERVICES SOFTWARE LIMITED",
"OIL.NS": "OIL INDIA LIMITED",
"ONGC.NS": "OIL AND NATURAL GAS CORP.",
"PATANJALI.NS": "PATANJALI FOODS LIMITED",
"PAYTM.NS": "ONE97 COMMUNICATIONS LTD",
"TMPV.NS": "Tatamotor Personal ",
"PERSISTENT.NS": "PERSISTENT SYSTEMS LIMITED",
"PETRONET.NS": "PETRONET LNG LTD",
"PFC.NS": "POWER FINANCE CORPORATION LTD.",
"PHOENIXLTD.NS": "PHOENIX MILLS LIMITED",
"PIDILITIND.NS": "PIDILITE INDUSTRIES LTD",
"PIIND.NS": "PI INDUSTRIES LTD.",
"PNB.NS": "PUNJAB NATIONAL BANK",
"POLICYBZR.NS": "PB FINTECH LIMITED",
"POLYCAB.NS": "POLYCAB INDIA LIMITED",
"POONAWALLA.NS": "POONAWALLA FINCORP LIMITED",
"POWERGRID.NS": "POWER GRID CORP. OF INDIA LTD.",
"PRESTIGE.NS": "PRESTIGE ESTATE LTD",
"RAMCOCEM.NS": "RAMCO CEMENTS LIMITED",
"RBLBANK.NS": "THE RATNAKAR BANK LTD",
"RECLTD.NS": "REC LIMITED",
"RELIANCE.NS": "RELIANCE INDUSTRIES LTD",
"SAIL.NS": "STEEL AUTHORITY OF INDIA LTD",
"SBICARD.NS": "SBI CARDS AND PAYMENT SERVICES LIMITED",
"SBILIFE.NS": "SBI LIFE INSURANCE COMPANY LIMITED",
"SBIN.NS": "STATE BANK OF INDIA",
"SHRIRAMFIN.NS": "SHRIRAM FINANCE LIMITED",
"SIEMENS.NS": "SIEMENS LTD",
"SJVN.NS": "SJVN LIMITED",
"SOLARINDS.NS": "SOLAR INDUSTRIES INDIA LIMITED",
"SONACOMS.NS": "SONA BLW PRECISION FORGINGS LIMITED",
"SRF.NS": "SRF LIMITED",
"SUNPHARMA.NS": "SUN PHARMACEUTICAL INDUST LTD",
"SUPREMEIND.NS": "SUPREME INDUSTRIES LTD",
"SYNGENE.NS": "SYNGENE INTERNATIONAL LIMITED",
"TATACHEM.NS": "TATA CHEMICALS LIMITED",
"TATACOMM.NS": "TATA COMMUNICATIONS LIMITED",
"TATACONSUM.NS": "TATA CONSUMER PRODUCTS LIMITED",
"TATAELXSI.NS": "TATA ELXSI LIMITED",
"TMCV.NS": "TATA MOTORS Comm",
"TATAPOWER.NS": "TATA POWER COMPANY LIMITED",
"TATASTEEL.NS": "TATA STEEL LIMITED",
"TATATECH.NS": "TATA TECHNOLOGIES LIMITED",
"TCS.NS": "TATA CONSULTANCY SERVICES LTD",
"TECHM.NS": "TECH MAHINDRA LIMITED",
"TIINDIA.NS": "TUBE INVESTMENTS OF INDIA LIMITED",
"TITAGARH.NS": "TITAGARH RAIL SYSTEMS LIMITED",
"TITAN.NS": "TITAN COMPANY  LTD",
"TORNTPHARM.NS": "TORRENT PHARMACEUTICALS LIMITE",
"TORNTPOWER.NS": "TORRENT POWER LIMITED",
"TRENT.NS": "TRENT LIMITED",
"TVSMOTOR.NS": "TVS MOTOR COMPANY LIMITED",
"ULTRACEMCO.NS": "ULTRATECH CEMENT LIMITED",
"UNIONBANK.NS": "UNION BANK OF INDIA",
"UNITDSPR.NS": "UNITED SPIRITS LIMITED",
"UPL.NS": "UPL LIMITED",
"VBL.NS": "VARUN BEVERAGES LIMITED",
"VEDL.NS": "VEDANTA LIMITED",
"VOLTAS.NS": "VOLTAS LIMITED",
"WIPRO.NS": "WIPRO LIMITED",
"YESBANK.NS": "YES BANK LTD.",
"ZYDUSLIFE.NS": "ZYDUS LIFESCIENCES LIMITED"
}

# =========================
# BULK DOWNLOAD
# =========================
data = yf.download(
    tickers=" ".join(stocks),
    period="1d",
    interval="5m",
    group_by="ticker",
    progress=False
)

# =========================
# SQUEEZE
# =========================
def is_squeeze(df):
    bb = ta.volatility.BollingerBands(df["Close"], window=20)
    bandwidth = (bb.bollinger_hband() - bb.bollinger_lband()) / bb.bollinger_mavg()
    return bandwidth.rolling(20).mean().iloc[-1] < 0.05

# =========================
# SCAN
# =========================
signals = []

if market != "SIDEWAYS":
    for stock in stocks:
        try:
            df = data[stock].dropna()
            if len(df) < 50:
                continue

            df["rsi"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
            bb = ta.volatility.BollingerBands(df["Close"], window=20)

            last = df.iloc[-1]
            prev = df.iloc[-2]
            avg_vol = df["Volume"].rolling(20).mean().iloc[-1]

            if not is_squeeze(df):
                continue

            # BUY
            if market == "BULLISH":
                if (last["Close"] > bb.bollinger_hband().iloc[-1]
                    and prev["rsi"] < 60
                    and last["rsi"] > 60
                    and 60 < last["rsi"] < 65
                    and last["Volume"] > 1.5 * avg_vol):
                    signals.append({"Stock":stock,"Signal":"BUY"})

            # SELL
            elif market == "BEARISH":
                if (last["Close"] < bb.bollinger_lband().iloc[-1]
                    and prev["rsi"] > 40
                    and last["rsi"] < 40
                    and 35 < last["rsi"] < 40
                    and last["Volume"] > 1.5 * avg_vol):
                    signals.append({"Stock":stock,"Signal":"SELL"})

        except:
            continue

# =========================
# OUTPUT
# =========================
if signals:
    st.subheader("📊 Signals")
    st.dataframe(pd.DataFrame(signals))
    strong_alert()
else:
    st.warning("No signals")
    
##################
# =========================
# ONE BREATH CYCLE
# =========================
import time

st.markdown("---")
st.subheader("🧘 One Breathing Cycle")

placeholder = st.empty()

phases = ["Breathe In", "Hold", "Breathe Out", "Hold"]

for phase in phases:
    for i in range(7, 0, -1):
        placeholder.markdown(f"""
        <div style="text-align:center;">
            <h2>{phase}</h2>
            <h1>{i}</h1>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1)