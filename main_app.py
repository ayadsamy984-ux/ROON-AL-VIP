import streamlit as st
from web3 import Web3
import pandas as pd
import ccxt

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ROON AL VIP Analyzer", layout="wide")

# --- بيانات العملة والشبكة ---
# ⚠️ ضع عنوان عقد عملتك هنا
CONTRACT_ADDRESS = "0x881D12E3a4d32f3df439EF0F73546A9a67004723" 
RPC_URL = "https://bsc-dataseed.binance.org/"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# ABI المختصر للفحص (اسم، رصيد)
abi = [
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"}
]

# --- واجهة تسجيل الدخول ---
st.sidebar.title("🔐 بوابة المشتركين")
user_wallet = st.sidebar.text_input("أدخل عنوان محفظتك (BEP-20)", placeholder="0x...")

access_granted = False

if user_wallet:
    try:
        if not w3.is_address(user_wallet):
            st.sidebar.error("العنوان غير صحيح!")
        else:
            contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
            balance = contract.functions.balanceOf(user_wallet).call()
            decimals = contract.functions.decimals().call()
            
            real_balance = balance / (10**decimals)
            
            if real_balance >= 100:
                st.sidebar.success(f"مرحباً بك! رصيدك: {real_balance:,.0f} ROON AL")
                access_granted = True
            else:
                st.sidebar.warning(f"عذراً! تحتاج لـ 100 قطعة. رصيدك الحالي: {real_balance:,.0f}")
                st.info("💡 للحصول على الوصول، يرجى شراء عملة ROON AL من المنصة.")
    except Exception as e:
        st.sidebar.error("خطأ في الاتصال بالعقد. تأكد من العنوان.")

# --- محتوى التطبيق العام (يظهر فقط إذا تم التحقق) ---
if access_granted:
    st.title("📈 محلل العملات العالمي - نسخة حاملي ROON AL")
    
    # هنا نضع كود التحليل القديم (البيتكوين وغيره)
    symbol = st.selectbox("اختر العملة للتحليل", ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"])
    
    # جلب البيانات من Binance كمثال
    exchange = ccxt.binance()
    bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=50)
    df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
    
    st.write(f"السعر الحالي لـ {symbol}: **{df['close'].iloc[-1]} $**")
    st.line_chart(df.set_index('time')['close'])
    
else:
    # --- شاشة القفل الاحترافية ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # كود ذكي جداً للبحث عن أي صورة تبدأ بكلمة logo
        import os
        image_file = None
        for file in os.listdir():
            if file.lower().startswith("logo"):
                image_file = file
                break
        
        if image_file:
            st.image(image_file, width=200)
        else:
            st.error("⚠️ لم يتم العثور على ملف الشعار. تأكد من وجود الصورة بجانب ملف app.py")
            st.stop()
        
        st.markdown(f"<h1 style='text-align: center; color: white;'>لوحة تحكم ROON AL VIP مقفلة</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #ffcc00; text-align: center;">
            <p style="color: #cccccc; font-size: 18px;">
                هذا المحلل الفني الذكي هو ميزة حصرية لمجتمع <b>ROON AL</b>.
                <br><br>
                للفتح، يجب أن تملك <b>100 قطعة</b> من عملة ROON AL في محفظتك.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
       # قسم زر الشراء الاحترافي المرتبط بـ Thirdweb
st.markdown("""
    <div style="text-align: center; margin-top: 30px; margin-bottom: 30px;">
        <a href="https://thirdweb.com/binance/0x881D12E3a4d32f3dF439EF0F73546A9a67004723" 
           target="_blank" 
           style="
            background: linear-gradient(45deg, #ffcc00, #ffaa00);
            color: #1a1a1a; 
            padding: 18px 45px; 
            border-radius: 50px; 
            text-decoration: none; 
            font-weight: bold; 
            font-size: 24px; 
            display: inline-block; 
            box-shadow: 0px 0px 25px rgba(255, 204, 0, 0.7); 
            border: 2px solid #ffffff;
            transition: transform 0.3s ease-in-out;
           " 
           onmouseover="this.style.transform='scale(1.1)'" 
           onmouseout="this.style.transform='scale(1)'">
            🔥 انضم للبيع المسبق الآن | Presale 🚀
        </a>
        <p style="color: #cccccc; margin-top: 10px; font-size: 14px;">(اضغط للذهاب لصفحة الشراء الرسمية على Thirdweb)</p>
    </div>
    """, unsafe_allow_html=True)
