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
</style>
""", unsafe_allow_html=True)

# Session State
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'user' not in st.session_state:
    st.session_state.user = None

# ====================== PRODUCTS ======================
products = [
    {"id": 1, "name": "Handcrafted Terracotta Beaded Necklace", "category": "Jewelry", "price": 599, "rating": 4.8,
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

login_expander = st.sidebar.expander("📱 Login / Register", expanded=not bool(st.session_state.user))

with login_expander:
    mobile = st.text_input("Mobile Number *", value="9", max_chars=10, key="mobile")
    pin = st.text_input("4-digit PIN (Demo)", type="password", max_chars=4, key="pin")
    pincode = st.text_input("Delivery Pincode * (6 digits)", max_chars=6, key="pincode")
    
    if st.button("Login Now", type="primary"):
        if len(mobile) < 10:
            st.error("Mobile number must be at least 10 digits")
        elif len(pin) != 4:
            st.error("PIN must be 4 digits")
        elif not pincode.isdigit() or len(pincode) != 6:
            st.error("Pincode must be exactly 6 digits")
        else:
            st.session_state.user = {"mobile": mobile, "pincode": pincode, "orders_count": 0}
            st.success(f"✅ Logged in! Pincode: {pincode}")
            st.rerun()

if st.session_state.user:
    st.sidebar.success(f"👤 {st.session_state.user['mobile']}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

page = st.sidebar.selectbox("Menu", ["🏠 Home", "🛍️ Shop", "🛒 Cart", "📦 My Orders", "📞 Contact"])

# Home Page
if page == "🏠 Home":
    st.image("https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0009.jpg", use_column_width=True)
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 India’s Most Trusted Handcrafted Home Decor Brand")

# Shop Page with Category Tabs
elif page == "🛍️ Shop":
    st.title("🛍️ Product Catalog")
    
    tab_list = ["All", "Jewelry", "Table Covers", "Sofa Covers", "Towels"]
    tabs = st.tabs(tab_list)
    
    search = st.text_input("🔍 Search products", "")
    
    for i, tab_name in enumerate(tab_list):
        with tabs[i]:
            filtered = [p for p in products if 
                        (tab_name == "All" or p["category"] == tab_name) and
                        (not search or search.lower() in p["name"].lower() or search.lower() in p["description"].lower())]
            
            if not filtered:
                st.info("No products found in this category.")
                continue
                
            cols = st.columns(3)
            for idx, p in enumerate(filtered):
                with cols[idx % 3]:
                    with st.container(border=True):
                        st.image(p["image"], use_column_width=True)
                        st.subheader(p["name"])
                        st.caption(p["description"])
                        st.write(f"⭐ {p['rating']} | **₹{p['price']}**")
                        if st.button("🛒 Add to Cart", key=f"add_{p['id']}_{i}"):
                            st.session_state.cart.append({**p, "qty": 1})
                            st.success("Added to cart!")

# Cart Page
elif page == "🛒 Cart":
    st.title("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = sum(item['price'] * item.get("qty", 1) for item in st.session_state.cart)
        st.subheader(f"Total: ₹{total}")
        
        if st.button("📱 Checkout on WhatsApp", type="primary"):
            st.success("WhatsApp checkout ready (add your full checkout code here)")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    © 2026 CarryMe Store • Authentic Handcrafted Home Decor<br>
    <b>Made with ❤️ in India</b>
</div>
""", unsafe_allow_html=True)
