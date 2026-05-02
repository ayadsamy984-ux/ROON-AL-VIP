import streamlit as st
from web3 import Web3
import streamlit.components.v1 as components

# --- الإعدادات الأساسية (العودة للأصل) ---
# عقد العملة للتحقق من ملكية 100 قطعة للدخول
TOKEN_CONTRACT = "0x881D12E3a4d32f3dF439EF0F73546A9a67004723"
RPC_URL = "https://bsc-dataseed.binance.org/" 
MY_ADMIN_WALLET = "0x83b3864a8DdbF6F8eB666C66F11FA01d75eDE156"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# --- وظيفة التحقق من الرصيد ---
def get_token_balance(user_address):
    abi = [
        {"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
        {"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"stateMutability":"view","type":"function"}
    ]
    try:
        if not w3.is_address(user_address): return 0
        contract = w3.eth.contract(address=w3.to_checksum_address(TOKEN_CONTRACT), abi=abi)
        raw_balance = contract.functions.balanceOf(w3.to_checksum_address(user_address)).call()
        decimals = contract.functions.decimals().call()
        return raw_balance / (10**decimals)
    except: return 0

# --- إعدادات الواجهة الأصلية ---
st.set_page_config(page_title="ROON AL VIP", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .centered-container { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 70vh; }
    .main-title { font-size: 3.5rem; font-weight: bold; margin-top: -20px; color: white; }
    .sub-title { color: #94a3b8; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية للتحقق ---
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("### 🔐 بوابة الأعضاء")
    user_wallet = st.text_input("أدخل عنوان محفظتك للدخول:", placeholder="0x...")
    access_granted = False
    if user_wallet:
        balance = get_token_balance(user_wallet)
        # السماح بالدخول لمحفظتك كآدمن أو لمن يملك 100 قطعة
        if user_wallet.lower() == MY_ADMIN_WALLET.lower() or balance >= 100:
            st.success(f"✅ تم التحقق بنجاح")
            access_granted = True
        else:
            st.error("❌ عذراً، يجب امتلاك 100 $RAL على الأقل")

# --- عرض المحتوى بناءً على التحقق ---
if access_granted:
    # واجهة الأدوات (المحلل الفني)
    st.title("📊 لوحة تحكم ROON AL VIP")
    st.markdown("### مرحباً بك في منطقة التحليل الفني المتقدم")
    
    # مصفوفة الأسعار السريعة
    m1, m2, m3 = st.columns(3)
    m1.metric("BTC / USDT", "$63,840", "+1.2%")
    m2.metric("BNB / USDT", "$585.4", "+0.5%")
    m3.metric("ROON AL", "$0.00045", "New")
    
    st.divider()
    
    # تضمين تشارت TradingView
    tradingview_html = '<div style="height:600px;"><div id="tv-chart" style="height:100%;"></div><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script><script type="text/javascript">new TradingView.widget({"autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "H", "theme": "dark", "style": "1", "locale": "ar", "container_id": "tv-chart"});</script></div>'
    components.html(tradingview_html, height=620)

else:
    # واجهة الترحيب الأصلية (بدون عدادات)
    st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
    st.image("logo.png", width=400)
    st.markdown("<div class='main-title'>ROON AL Project</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>المنصة الرسمية لأدوات الذكاء الاصطناعي والتحليل الفني لعملة $RAL</div>", unsafe_allow_html=True)
    st.divider()
    st.info("⚠️ يرجى إدخال عنوان محفظتك في القائمة الجانبية للوصول إلى الأدوات.")
    st.markdown("</div>", unsafe_allow_html=True)
