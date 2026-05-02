import streamlit as st
from web3 import Web3
import streamlit.components.v1 as components

# --- إعدادات المشروع الأساسية ---
CONTRACT_ADDRESS = "0x881D12E3a4d32f3dF439EF0F73546A9a67004723"
RPC_URL = "https://bsc-dataseed.binance.org/" 
MY_ADMIN_WALLET = "0x83b3864a8DdbF6F8eB666C66F11FA01d75eDE156"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

abi = [
    {"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"stateMutability":"view","type":"function"}
]

def get_token_balance(user_address):
    try:
        if not w3.is_address(user_address): return 0
        contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
        raw_balance = contract.functions.balanceOf(w3.to_checksum_address(user_address)).call()
        decimals = contract.functions.decimals().call()
        return raw_balance / (10**decimals)
    except: return 0

# --- تحسين الواجهة وتجنب التداخل ---
st.set_page_config(page_title="ROON AL VIP", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child { background-color: #f3ba2f; color: black; font-weight: bold; }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("### 🔐 بوابة التحقق")
    user_wallet = st.text_input("عنوان المحفظة:", placeholder="0x...")
    
    access_granted = False
    if user_wallet:
        balance = get_token_balance(user_wallet)
        if user_wallet.lower() == MY_ADMIN_WALLET.lower():
            st.success("✅ مرحباً أياد (المطور)")
            access_granted = True
        elif balance >= 100:
            st.success(f"✅ تم التحقق (الرصيد: {balance:,.0f})")
            access_granted = True
        else:
            st.error("❌ الرصيد غير كافٍ")

# --- عرض المحتوى بشكل منظم ---
if access_granted:
    st.header("📊 لوحة تحكم ROON AL VIP")
    
    # صف الأسعار مع مسافات
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("BTC / USDT", "$63,840", "+1.2%")
    with m2: st.metric("BNB / USDT", "$585.4", "+0.5%")
    with m3: st.metric("ROON AL", "$0.00045", "New")

    st.write("---") # خط فاصل للتنظيم

    # تحسين عرض الرسم البياني
    st.subheader("📈 التحليل الفني المباشر")
    tradingview_html = """
    <div style="height:600px; margin-bottom: 20px;">
      <div id="tv-chart" style="height:100%;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true,
        "symbol": "BINANCE:BTCUSDT",
        "interval": "H",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "ar",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tv-chart"
      });
      </script>
    </div>
    """
    components.html(tradingview_html, height=620)

    st.write("---")

    # التوصيات بأسلوب نظيف
    c1, c2 = st.columns(2)
    with c1:
        st.info("🎯 **توصية الذكاء الاصطناعي**\n\nالسوق في منطقة تجميع هادئة حالياً.")
    with c2:
        st.warning("🔔 **تنبيه المشروع**\n\nترقب إطلاق البيع المسبق الكامل في سبتمبر.")

else:
    # واجهة الزوار
    st.image("logo.png", width=250)
    st.title("ROON AL VIP")
    st.markdown("قم بتسجيل الدخول بمحفظتك للوصول إلى أدوات التحليل الذكية.")
    st.divider()
    st.link_button("🚀 شراء ROON AL من البيع المسبق", "https://thirdweb.com/binance/0x881D12E3a4d32f3dF439EF0F73546A9a67004723")
