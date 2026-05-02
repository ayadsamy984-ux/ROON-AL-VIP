import streamlit as st
from web3 import Web3
import streamlit.components.v1 as components

# --- الإعدادات الأساسية ---
# محفظة جمع الأموال (المحفظة التي زودتني بها)
PRESALE_WALLET = "0x83b3864a8DdbF6F8eB666C66F11FA01d75eDE156"
# عقد العملة (للتحقق من الدخول)
TOKEN_CONTRACT = "0x881D12E3a4d32f3dF439EF0F73546A9a67004723"
RPC_URL = "https://bsc-dataseed.binance.org/" 

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# --- وظائف البلوكشين ---
def get_bnb_balance(address):
    try:
        balance_wei = w3.eth.get_balance(w3.to_checksum_address(address))
        return float(w3.from_wei(balance_wei, 'ether'))
    except: return 0.0

def get_token_balance(user_address):
    abi = [{"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]
    try:
        if not w3.is_address(user_address): return 0
        contract = w3.eth.contract(address=w3.to_checksum_address(TOKEN_CONTRACT), abi=abi)
        raw_balance = contract.functions.balanceOf(w3.to_checksum_address(user_address)).call()
        decimals = contract.functions.decimals().call()
        return raw_balance / (10**decimals)
    except: return 0

# --- تصميم الواجهة ---
st.set_page_config(page_title="ROON AL VIP", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .centered-content { text-align: center; }
    .stat-box { background-color: #1e293b; padding: 20px; border-radius: 15px; border: 1px solid #f3ba2f; }
    .stProgress > div > div > div > div { background-color: #f3ba2f; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("### 🔐 بوابة VIP")
    user_wallet = st.text_input("أدخل محفظتك للدخول:", placeholder="0x...")
    access_granted = False
    if user_wallet:
        balance = get_token_balance(user_wallet)
        if user_wallet.lower() == PRESALE_WALLET.lower() or balance >= 100:
            st.success("✅ أهلاً بك في المنطقة الخاصة")
            access_granted = True
        else: st.error("❌ مطلوب 100 $RAL للدخول")

# --- عرض المحتوى ---
if access_granted:
    # لوحة التحليل الفني (تظهر بعد الدخول)
    st.title("📊 لوحة تحكم ROON AL VIP")
    # (كود الأسعار والتشارت يبقى كما هو)
    st.info("نظام التحليل الفني نشط الآن...")
else:
    # واجهة العداد المباشر (تظهر للجميع عند الدخول من Carrd)
    st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
    st.image("logo.png", width=350)
    st.markdown("<h1>ROON AL LIVE TRACKER</h1>", unsafe_allow_html=True)
    
    st.divider()

    # --- العداد الآلي ---
    current_bnb = get_bnb_balance(PRESALE_WALLET)
    target_bnb = 50.0 # يمكنك تغيير الهدف من هنا
    progress = min(current_bnb / target_bnb, 1.0)

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown(f"### 🚀 حالة البيع المسبق (بث مباشر)")
        st.progress(progress)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='stat-box'><b>المحصل حالياً</b><br>{current_bnb:.2f} BNB</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-box'><b>الهدف الكلي</b><br>{target_bnb} BNB</div>", unsafe_allow_html=True)
        
        st.write("")
        st.warning(f"🔔 يتم تحديث البيانات مباشرة من محفظة المشروع: {PRESALE_WALLET[:10]}...")
        
    st.markdown("</div>", unsafe_allow_html=True)
