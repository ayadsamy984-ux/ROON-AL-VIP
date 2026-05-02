import streamlit as st
from web3 import Web3

# --- الإعدادات الأساسية ---
CONTRACT_ADDRESS = "0x881D12E3a4d32f3dF439EF0F73546A9a67004723"
RPC_URL = "https://bsc-dataseed.binance.org/" 
MY_ADMIN_WALLET = "0x83b3864a8DdbF6F8eB666C66F11FA01d75eDE156"
PRESALE_LINK = "https://thirdweb.com/binance/0x881D12E3a4d32f3dF439EF0F73546A9a67004723" # رابط الشراء الخاص بك

# --- واجهة احترافية (CSS) ---
st.set_page_config(page_title="ROON AL VIP", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{
        background-color: #0e1117;
    }}
    .main-logo {{
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 300px; /* حجم الشعار */
        margin-bottom: 20px;
    }}
    .presale-btn {{
        background-color: #f1c40f;
        color: black !important;
        padding: 15px 30px;
        text-align: center;
        text-decoration: none;
        display: block;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        margin: 20px auto;
        width: 250px;
        transition: 0.3s;
    }}
    .presale-btn:hover {{
        background-color: #d4ac0d;
        transform: scale(1.05);
    }}
    </style>
""", unsafe_allow_html=True)

# --- منطق البلوكشين ---
w3 = Web3(Web3.HTTPProvider(RPC_URL))
abi = [
    {{"inputs":[{{"name":"account","type":"address"}}],"name":"balanceOf","outputs":[{{"name":"","type":"uint256"}}],"stateMutability":"view","type":"function"}},
    {{"inputs":[],"name":"decimals","outputs":[{{"name":"","type":"uint8"}}],"stateMutability":"view","type":"function"}}
]

def get_balance(address):
    try:
        if not w3.is_address(address): return 0
        contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
        raw = contract.functions.balanceOf(w3.to_checksum_address(address)).call()
        dec = contract.functions.decimals().call()
        return raw / (10**dec)
    except: return 0

# --- عرض الشعار والواجهة ---
st.image("logo.png", width=350) # تأكد أن الصورة بنفس الاسم في GitHub

access = False

with st.sidebar:
    st.header("🔐 دخول المشتركين")
    wallet = st.text_input("أدخل عنوان محفظتك:")
    
    if wallet:
        bal = get_balance(wallet)
        if wallet.lower() == MY_ADMIN_WALLET.lower():
            st.success("✅ مرحباً يا مطور المشروع")
            access = True
        elif bal >= 100:
            st.success(f"✅ تم التحقق! رصيدك: {bal:,.0f}")
            access = True
        else:
            st.error(f"رصيدك {bal:,.0f} غير كافٍ.")
            st.markdown(f'<a href="{PRESALE_LINK}" class="presale-btn">🔥 اشترِ الآن لتفعيل الدخول</a>', unsafe_allow_html=True)

# --- منطقة المحتوى المحمي ---
if access:
    st.title("📊 لوحة التحليل الفني الذكي")
    st.info("هنا تضع أدوات التحليل الخاصة بك...")
else:
    st.markdown("<h2 style='text-align: center;'>هذا النظام مخصص حصرياً لمجتمع ROON AL</h2>", unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center"><a href="{PRESALE_LINK}" class="presale-btn">🚀 انضم للبيع المسبق</a></div>', unsafe_allow_html=True)

### ماذا تفعل الآن؟
1.  امسح الكود القديم في **GitHub** وضع هذا مكانه.
2.  اضغط **Commit changes**.
3.  افتح الموقع، وستجد أن الواجهة أصبحت مبهرة واحترافية جداً!

لقد صممت لك العرض التوضيحي المرفق لترى كيف أصبح هيكل مشروعك الآن بشكل VIP. هل تريد إضافة أي شيء آخر؟
