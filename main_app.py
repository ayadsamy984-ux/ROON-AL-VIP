import streamlit as st
from web3 import Web3
import streamlit.components.v1 as components

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

# --- تصميم الواجهة ---
st.set_page_config(page_title="ROON AL VIP | المحلل الذكي", layout="wide")

# CSS لتحسين المظهر
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .price-card { background: #1e293b; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #334155; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #f3ba2f; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- الشريط الجانبي (Sidebar) ---
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("<h2 style='text-align: center;'>🔐 بوابة المشتركين</h2>", unsafe_allow_html=True)
    user_wallet = st.text_input("أدخل عنوان محفظتك (BEP-20):", placeholder="0x...")
    
    access_granted = False
    if user_wallet:
        balance = get_token_balance(user_wallet)
        if user_wallet.lower() == MY_ADMIN_WALLET.lower():
            st.success("✅ أهلاً بك يا مطور المشروع")
            access_granted = True
        elif balance >= 100:
            st.success(f"✅ تم التحقق! رصيدك: {balance:,.0f}")
            access_granted = True
        else:
            st.error(f"❌ رصيدك {balance:,.0f} غير كافٍ (تحتاج 100)")

# --- المحتوى الرئيسي ---
if access_granted:
    st.title("📊 لوحة تحكم ROON AL الذكية")
    
    # 1. عرض أسعار العملات (Widgets)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("BTC / USDT", "$63,840", "+1.2%")
    with col2: st.metric("BNB / USDT", "$585.4", "+0.5%")
    with col3: st.metric("SOL / USDT", "$142.1", "-2.1%")
    with col4: st.metric("ROON AL", "$0.00045", "New")

    st.divider()

    # 2. الرسم البياني الاحترافي (TradingView)
    st.subheader("📈 التحليل الفني المباشر (BTC/USDT)")
    tradingview_html = """
    <div class="tradingview-widget-container" style="height:500px;">
      <div id="tradingview_chart"></div>
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
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_chart"
      });
      </script>
    </div>
    """
    components.html(tradingview_html, height=500)

    # 3. قسم التوصيات والذكاء الاصطناعي
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.info("🎯 **توصية الذكاء الاصطناعي اليوم:**")
        st.write("- اتجاه السوق: **متذبذب يميل للصعود**")
        st.write("- نقطة الدعم القادمة لـ ROON: **0.00040**")
        st.write("- نقطة المقاومة: **0.00055**")
    with c2:
        st.warning("🔔 **تنبيهات الحيتان:**")
        st.write("- تم رصد دخول سيولة كبيرة في شبكة BSC.")
        st.write("- زيادة في عدد المحفظات الحاملة لعملة $RAL بنسبة 5%.")

else:
    # واجهة العرض للزوار (قبل الدخول)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.image("logo.png", use_container_width=True)
        st.markdown("<h1 style='text-align: center;'>ROON AL VIP</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>النظام الأذكى لتحليل العملات الرقمية. تملك 100 قطعة لفتح المميزات.</p>", unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 🔥 شارك في البيع المسبق الآن")
        st.link_button("🚀 اشترِ ROON AL من Thirdweb", "https://thirdweb.com/binance/0x881D12E3a4d32f3dF439EF0F73546A9a67004723")
