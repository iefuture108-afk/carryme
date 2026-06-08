import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="CarryMe Store - Premium Handcrafted Home Decor India",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {font-size: 3.2rem; color: #FF6B6B; text-align: center; margin-bottom: 10px;}
    .product-image {border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);}
    .stButton>button {width: 100%; border-radius: 10px; font-weight: 600;}
    .discount-badge {background: #FF6B6B; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'cart' not in st.session_state: st.session_state.cart = []
if 'wishlist' not in st.session_state: st.session_state.wishlist = []
if 'orders' not in st.session_state: st.session_state.orders = []
if 'user' not in st.session_state: st.session_state.user = None  

# ====================== PRODUCTS ======================
products = [
    {"id": 1, "name": "Handcrafted Terracotta Beaded Necklace for Women", "category": "Jewelry", "price": 599, "rating": 4.8,
     "description": "Premium ethnic terracotta beaded necklace.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0011.jpg", "stock": 25},
    {"id": 2, "name": "Traditional Terracotta Jewelry Set", "category": "Jewelry", "price": 449, "rating": 4.7,
     "description": "Beautiful terracotta earrings & necklace set.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/734eeecae73fc3c8aa1fb635b1b8aaef983a0ecd/images/IMG-20260608-WA0000.jpg", "stock": 20},
    {"id": 3, "name": "Waterproof PVC Table Cover - Floral Print", "category": "Table Covers", "price": 299, "rating": 4.6,
     "description": "Heavy duty waterproof PVC table cover.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0012.jpg", "stock": 35},
    {"id": 4, "name": "Luxury Quilted Sofa Cover with Lace Border", "category": "Sofa Covers", "price": 1299, "rating": 4.9,
     "description": "Premium quilted sofa cover with elegant lace detailing.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/ba13288c6a2841298ba356abea281818e3e8ccbc/images/Sofa%20cover.png", "stock": 18},
    {"id": 5, "name": "Premium Cotton Hand & Face Towel Set", "category": "Towels", "price": 449, "rating": 4.9,
     "description": "Ultra soft cotton towels.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0016.jpg", "stock": 30},
]

ig_url = "https://www.instagram.com/carryme_stores"

# Sidebar Login
st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("**Premium Handcrafted Home Decor**")

if st.sidebar.button("📱 Login / Register"):
    with st.sidebar.expander("Login with Mobile & Pincode", expanded=True):
        mobile = st.text_input("Mobile Number *", value="9", max_chars=10)
        pin = st.text_input("4-digit PIN (Demo)", type="password", max_chars=4)
        pincode = st.text_input("Delivery Pincode * (6 digits)", max_chars=6)
        
        if st.button("Login Now"):
            if len(mobile) < 10:
                st.error("Mobile number must be at least 10 digits")
            elif len(pin) != 4:
                st.error("PIN must be 4 digits")
            elif not pincode.isdigit() or len(pincode) != 6:
                st.error("Pincode must be exactly 6 digits")
            else:
                st.session_state.user = {
                    "mobile": mobile,
                    "pincode": pincode,
                    "orders_count": 0
                }
                st.success(f"✅ Login successful! Pincode: {pincode}")
                st.rerun()

if st.session_state.user:
    st.sidebar.success(f"👤 {st.session_state.user['mobile']}")
    st.sidebar.info(f"📍 Pincode: {st.session_state.user.get('pincode', 'Not set')}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

page = st.sidebar.selectbox("Menu", ["🏠 Home", "🛍️ Shop", "❤️ Wishlist", "🛒 Cart", "📦 My Orders", "📞 Contact"])

# Home Page
if page == "🏠 Home":
    st.image("https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0009.jpg", use_column_width=True)
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 India’s Most Trusted Handcrafted Home Decor Brand")

# Shop Page (keep your existing shop code)

# ====================== CART WITH PINCODE VALIDATION ======================
elif page == "🛒 Cart":
    st.title("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = sum(item['price'] * item.get("qty", 1) for item in st.session_state.cart)
        discount_applied = st.session_state.user and st.session_state.user.get('orders_count', 0) < 2
        final_total = total * 0.4 if discount_applied else total
        
        for idx, item in enumerate(st.session_state.cart):
            col1, col2, col3, col4 = st.columns([3,2,2,2])
            with col1: st.write(f"**{item['name']}**")
            with col2:
                qty = st.number_input("Qty", 1, 20, item.get("qty",1), key=f"qty_{idx}")
                st.session_state.cart[idx]["qty"] = qty
            with col3: st.write(f"₹{item['price']*qty}")
            with col4:
                if st.button("Remove", key=f"rem_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
        
        st.divider()
        st.subheader(f"Subtotal: ₹{total}")
        if discount_applied:
            st.success("🎉 60% OFF applied for first 2 orders!")
            st.subheader(f"**Final Total: ₹{final_total:.0f}**")
        
        st.subheader("📱 WhatsApp Checkout")
        with st.form("checkout_form"):
            name = st.text_input("Full Name *")
            phone = st.text_input("Phone Number *", value=st.session_state.user['mobile'] if st.session_state.user else "9")
            address = st.text_area("Full Delivery Address *")
            
            default_pin = st.session_state.user.get('pincode', '') if st.session_state.user else ''
            pincode_input = st.text_input("Pincode * (6 digits)", value=default_pin, max_chars=6)
            
            if st.form_submit_button("Send Order on WhatsApp", type="primary"):
                if not name or not phone or not address:
                    st.error("Please fill Name, Phone and Address")
                elif not pincode_input.isdigit() or len(pincode_input) != 6:
                    st.error("Pincode must be exactly 6 digits")
                else:
                    items_str = "%0A".join([f"• {item['name']} x{item.get('qty',1)} - ₹{item['price']*item.get('qty',1)}" for item in st.session_state.cart])
                    discount_text = " (60% OFF Applied)" if discount_applied else ""
                    msg = f"*New Order - CarryMe Store*{discount_text}%0A%0AName: {name}%0APhone: {phone}%0AAddress: {address}%0APincode: {pincode_input}%0A%0AOrder:%0A{items_str}%0A%0ATotal: ₹{final_total}"
                    wa_url = f"https://wa.me/919250036334?text={msg}"
                    st.markdown(f"[📱 Open WhatsApp]({wa_url})", unsafe_allow_html=True)
                    
                    if st.session_state.user:
                        st.session_state.user['orders_count'] += 1
                    st.session_state.cart = []
                    st.success("Order prepared successfully!")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    © 2026 CarryMe Store • Authentic Handcrafted Home Decor<br>
    <b>New users get 60% OFF on first 2 orders!</b>
</div>
""", unsafe_allow_html=True)
