import streamlit as st
from web3 import Web3
import streamlit.components.v1 as components
import requests
import pandas as pd

# --- الإعدادات الأساسية ---
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

# --- إعدادات الصفحة واللغة ---
st.set_page_config(page_title="ROON AL VIP", layout="wide")

# نظام اختيار اللغة
if 'lang' not in st.session_state:
    st.session_state['lang'] = "العربية"

with st.sidebar:
    st.session_state['lang'] = st.radio("Select Language / اختر اللغة", ["العربية", "English"])
    st.divider()

# قاموس اللغات
L = {
    "العربية": {
        "ver_title": "🔐 التحقق من الحساب",
        "input_label": "أدخل محفظتك للدخول:",
        "admin_msg": "✅ مرحباً أياد (المطور)",
        "success_msg": "✅ تم التحقق (الرصيد: ",
        "fail_msg": "❌ رصيدك أقل من 100 قطعة",
        "main_title": "📊 لوحة تحكم ROON AL VIP",
        "sub_title": "نظام التحليل الفني الأذكى لمجتمعنا الخاص",
        "join_presale": "### 🔥 انضم للبيع المسبق",
        "get_now": "احصل على عملتك الآن لتتمكن من استخدام المحلل الفني فور الإطلاق.",
        "buy_btn": "🚀 اشترِ ROON AL الآن",
        "note": "💡 ملاحظة: يتطلب الدخول امتلاك 100 قطعة على الأقل.",
        "dir": "rtl"
    },
    "English": {
        "ver_title": "🔐 Account Verification",
        "input_label": "Enter wallet to enter:",
        "admin_msg": "✅ Hello Ayad (Developer)",
        "success_msg": "✅ Verified (Balance: ",
        "fail_msg": "❌ Balance is less than 100 tokens",
        "main_title": "📊 ROON AL VIP Dashboard",
        "sub_title": "The smartest technical analysis system for our community",
        "join_presale": "### 🔥 Join Presale",
        "get_now": "Get your tokens now to use the technical analyzer immediately.",
        "buy_btn": "🚀 Buy ROON AL Now",
        "note": "💡 Note: Entry requires holding at least 100 tokens.",
        "dir": "ltr"
    }
}

lang = st.session_state['lang']

# --- الستايل المحدث مع دعم الاتجاهين ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; direction: {L[lang]['dir']}; }}
    .main-header {{ text-align: center; padding-top: 50px; }}
    .logo-img {{ display: block; margin-left: auto; margin-right: auto; width: 350px !important; }}
    .buy-button {{ background-color: #f3ba2f !important; color: black !important; font-weight: bold !important; border-radius: 10px !important; }}
    .centered-content {{ display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (بوابة التحقق) ---
with st.sidebar:
    st.markdown(f"<h3 style='text-align: center;'>{L[lang]['ver_title']}</h3>", unsafe_allow_html=True)
    user_wallet = st.text_input(L[lang]['input_label'], placeholder="0x...")
    
    access_granted = False
    if user_wallet:
        balance = get_token_balance(user_wallet)
        if user_wallet.lower() == MY_ADMIN_WALLET.lower():
            st.success(L[lang]['admin_msg'])
            access_granted = True
        elif balance >= 100:
            st.success(f"{L[lang]['success_msg']}{balance:,.0f})")
            access_granted = True
        else:
            st.error(L[lang]['fail_msg'])

# --- المحتوى الرئيسي ---
if access_granted:
    st.title(L[lang]['main_title'])
    m1, m2, m3 = st.columns(3)
    m1.metric("BTC / USDT", "$63,840", "+1.2%")
    m2.metric("BNB / USDT", "$585.4", "+0.5%")
    m3.metric("ROON AL", "$0.00045", "New")
    
    st.divider()
    tradingview_html = f"""
    <div style="height:600px;"><div id="tv-chart" style="height:100%;"></div><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script><script type="text/javascript">
    new TradingView.widget({{"autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "H", "theme": "dark", "style": "1", "locale": "{"ar" if lang=="العربية" else "en"}", "container_id": "tv-chart"}});
    </script></div>
    """
    components.html(tradingview_html, height=620)

else:
    # --- واجهة الدخول (الشعار في الوسط) ---
    st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
    
    # تأكد من وجود ملف logo.png في مستودع GitHub
    try:
        st.image("logo.png", width=400) 
    except:
        st.markdown("<h1 style='color: #f3ba2f;'>ROON AL</h1>", unsafe_allow_html=True)
    
    st.markdown(f"<h1 style='font-size: 3em; margin-bottom: 0;'>ROON AL VIP</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 1.5em; color: #94a3b8;'>{L[lang]['sub_title']}</p>", unsafe_allow_html=True)
    
    st.divider()
    
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown(L[lang]['join_presale'])
        st.write(L[lang]['get_now'])
        st.link_button(L[lang]['buy_btn'], "https://thirdweb.com/binance/0x881D12E3a4d32f3dF439EF0F73546A9a67004723")
        st.info(L[lang]['note'])
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Powered by ROON AL Ecosystem | 2026")
