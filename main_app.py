import streamlit as st
from web3 import Web3

# --- إعدادات الشبكة والعقد ---
CONTRACT_ADDRESS = "0x881D12E3a4d32f3dF439EF0F73546A9a67004723"
# جرب هذا الرابط أولاً للشبكة الحقيقية
RPC_URL = "https://bsc-dataseed.binance.org/" 

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# ABI كامل ومتوافق مع معايير Thirdweb و ERC-20
abi = [
    {"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"stateMutability":"view","type":"function"}
]

def get_token_balance(user_address):
    try:
        if not w3.is_address(user_address):
            return 0
        contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
        raw_balance = contract.functions.balanceOf(w3.to_checksum_address(user_address)).call()
        decimals = contract.functions.decimals().call()
        return raw_balance / (10**decimals)
    except Exception as e:
        return -1 # إشارة لوجود خطأ في الاتصال

# --- الواجهة ---
st.set_page_config(page_title="ROON AL VIP", layout="wide")

with st.sidebar:
    st.title("🔐 بوابة المشتركين")
    user_wallet = st.text_input("أدخل عنوان محفظتك (BEP-20):")
    
    if user_wallet:
        balance = get_token_balance(user_wallet)
        if balance >= 100:
            st.success(f"✅ تم التحقق! رصيدك: {balance:,.0f}")
            access = True
        elif balance == -1:
            st.error("⚠️ خطأ في الاتصال بالبلوكشين. تأكد من شبكة العقد.")
            access = False
        else:
            st.warning(f"عذراً! رصيدك الحالي: {balance:,.0f}. تحتاج لـ 100 قطعة.")
            access = False
    else:
        access = False

if access:
    st.title("🚀 مرحباً بك في لوحة تحكم ROON AL VIP")
    st.write("أنت الآن تملك صلاحية الوصول للمحلل الفني.")
else:
    st.image("logo.png", width=200)
    st.info("هذا النظام يتطلب امتلاك 100 قطعة من عملة ROON AL للدخول.")
