import streamlit as st
from web3 import Web3

# --- إعدادات المشروع الأساسية ---
CONTRACT_ADDRESS = "0x881D12E3a4d32f3dF439EF0F73546A9a67004723"
RPC_URL = "https://bsc-dataseed.binance.org/" 
MY_ADMIN_WALLET = "0x83b3864a8DdbF6F8eB666C66F11FA01d75eDE156"

# الاتصال بالبلوكشين
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# تعريف وظائف العقد
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

# --- تصميم الواجهة الاحترافية ---
st.set_page_config(page_title="ROON AL VIP | المحلل الذكي", layout="wide")

# تخصيص الألوان والخلفية
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #f3ba2f; color: black; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ffcc00; color: black; }
    </style>
    """, unsafe_allow_html=True)

# شريط جانبي للبوابة
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🔐 بوابة المشتركين</h2>", unsafe_allow_html=True)
    user_wallet = st.text_input("أدخل عنوان محفظتك (BEP-20):", placeholder="0x...")
    
    access_granted = False
    if user_wallet:
        balance = get_token_balance(user_wallet)
        if user_wallet.lower() == MY_ADMIN_WALLET.lower():
            st.success("✅ أهلاً بك يا مطور ROON AL")
            access_granted = True
        elif balance >= 100:
            st.success(f"✅ تم التحقق! رصيدك: {balance:,.0f}")
            access_granted = True
        else:
            st.error(f"❌ رصيدك {balance:,.0f} غير كافٍ")

# المحتوى الرئيسي عند الدخول
if access_granted:
    st.title("📊 لوحة تحكم المحلل الفني الذكي")
    st.info("مرحباً بك في المنطقة الخاصة. نظام التحليل الفني قيد التفعيل...")
    # هنا سيتم إضافة كود التحليل الفني لاحقاً
else:
    # واجهة العرض العامة (قبل الدخول)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_container_width=True)
        st.markdown("<h1 style='text-align: center;'>ROON AL VIP</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2em;'>اكتشف قوة التحليل الفني المعتمد على الذكاء الاصطناعي</p>", unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("### 🔥 فرصة استثمارية: البيع المسبق مفتوح الآن")
        st.write("احصل على عملة ROON AL قبل الجميع واستفد من ميزات المحلل الذكي الحصرية.")
        
        # رابط الشراء من Thirdweb (استبدل الرابط أدناه برابط صفحة الشراء الخاصة بك)
        buy_link = "https://thirdweb.com/binance/0x881D12E3a4d32f3dF439EF0F73546A9a67004723"
        st.link_button("🚀 اشترِ عملة ROON AL الآن", buy_link)
        
        st.warning("⚠️ يتطلب دخول المحلل الفني امتلاك 100 قطعة على الأقل.")
