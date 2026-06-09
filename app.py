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
if 'cart' not in st.session_state: st.session_state.cart = []
if 'wishlist' not in st.session_state: st.session_state.wishlist = []
if 'orders' not in st.session_state: st.session_state.orders = []
if 'user' not in st.session_state: st.session_state.user = None  

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

# Sidebar Login (same as before - fixed version)
st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("**Premium Handcrafted Home Decor**")

# Login code (keep the fixed login from previous message)

page = st.sidebar.selectbox("Menu", ["🏠 Home", "🛍️ Shop", "❤️ Wishlist", "🛒 Cart", "📦 My Orders", "📞 Contact"])

# Home Page
if page == "🏠 Home":
    st.image("https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0009.jpg", use_column_width=True)
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 India’s Most Trusted Handcrafted Home Decor Brand")

# ====================== ENHANCED PRODUCT CATALOG ======================
elif page == "🛍️ Shop":
    st.title("🛍️ Product Catalog")
    
    # Category Tabs
    tab_list = ["All"] + sorted({p["category"] for p in products})
    tabs = st.tabs(tab_list)
    
    search = st.text_input("🔍 Search in catalog", "")
    
    for i, tab_name in enumerate(tab_list):
        with tabs[i]:
            filtered = [p for p in products if 
                        (tab_name == "All" or p["category"] == tab_name) and
                        (not search or search.lower() in p["name"].lower() or search.lower() in p["description"].lower())]
            
            if not filtered:
                st.info("No products found.")
                continue
                
            cols = st.columns(3)
            for idx, p in enumerate(filtered):
                with cols[idx % 3]:
                    with st.container(border=True):
                        st.image(p["image"], use_column_width=True)
                        st.subheader(p["name"])
                        st.caption(p["description"])
                        st.write(f"⭐ {p['rating']} | **₹{p['price']}** | Stock: {p['stock']}")
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("🛒 Add to Cart", key=f"add_{p['id']}_{tab_name}"):
                                st.session_state.cart.append({**p, "qty": 1})
                                st.success("Added to cart!")
                        with c2:
                            if st.button("❤️", key=f"wl_{p['id']}_{tab_name}"):
                                if p not in st.session_state.wishlist:
                                    st.session_state.wishlist.append(p)
                                    st.success("Added to wishlist!")

# Cart Page (same as before with discount and pincode)
elif page == "🛒 Cart":
    # Paste your full cart code from previous version here

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    © 2026 CarryMe Store • Authentic Handcrafted Home Decor<br>
    <b>Made with ❤️ in India</b>
</div>
""", unsafe_allow_html=True)
