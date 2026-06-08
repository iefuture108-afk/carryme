import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="CarryMe Store - Premium Home Decor",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 3.2rem; color: #FF6B6B; text-align: center; margin-bottom: 8px;}
    .stImage {border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'wishlist' not in st.session_state:
    st.session_state.wishlist = []
if 'orders' not in st.session_state:
    st.session_state.orders = []

# ====================== PRODUCTS ======================
products = [
    {
        "id": 1,
        "name": "Terracotta Beaded Necklace",
        "category": "Jewelry",
        "price": 599,
        "rating": 4.8,
        "description": "Handcrafted terracotta beaded necklace with traditional ethnic design.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3369732de9ecaae75947f217dbfc3218156c9c65/images/Gemini_Generated_Image_7ylmma7ylmma7ylm.png",
        "stock": 25
    },
    {
        "id": 2,
        "name": "Terracotta Earrings Set",
        "category": "Jewelry",
        "price": 399,
        "rating": 4.7,
        "description": "Lightweight terracotta earrings with vibrant traditional motifs.",
        "image": "https://via.placeholder.com/400x400/FF6B6B/FFFFFF?text=Terracotta+Earrings",  # Replace when you upload
        "stock": 30
    },
    {
        "id": 3,
        "name": "PVC Table Cover - Floral Print",
        "category": "Table Covers",
        "price": 299,
        "rating": 4.5,
        "description": "Premium waterproof PVC table cover with beautiful floral design.",
        "image": "https://via.placeholder.com/400x400/4ECDC4/FFFFFF?text=PVC+Table+Cover",
        "stock": 40
    },
    {
        "id": 4,
        "name": "Premium Hand Towel Set (3 pcs)",
        "category": "Towels",
        "price": 449,
        "rating": 4.9,
        "description": "Ultra-soft cotton hand towels.",
        "image": "https://via.placeholder.com/400x400/45B8AC/FFFFFF?text=Hand+Towels",
        "stock": 22
    },
    {
        "id": 5,
        "name": "Luxury Face Towel Set (4 pcs)",
        "category": "Towels",
        "price": 349,
        "rating": 4.6,
        "description": "Premium quality face towels.",
        "image": "https://via.placeholder.com/400x400/45B8AC/FFFFFF?text=Face+Towels",
        "stock": 35
    },
]

# Sidebar
st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("**Premium Indian Handcrafted Decor**")

page = st.sidebar.selectbox(
    "Menu", ["🏠 Home", "🛍️ Shop", "❤️ Wishlist", "🛒 Cart", "📦 My Orders", "🎥 Videos", "📞 Contact"]
)

if page == "🏠 Home":
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 Authentic Indian Home Decor & Lifestyle Products")
    
    st.image("https://via.placeholder.com/1200x450/FF6B6B/FFFFFF?text=CarryMe+Store", use_column_width=True)
    
    # Founder Section
    st.divider()
    st.subheader("👤 Meet Our Founder")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(
            "https://raw.githubusercontent.com/iefuture108-afk/carryme/cfd07c238447041c56cb6b796e778d57d4e99bdd/images/IMG-20260608-WA0006.jpg", 
            width=220
        )
    with col2:
        st.write("**Founder of CarryMe Store**")
        st.write("Passionate about bringing authentic Indian handcrafted products directly to your home.")
    
    st.divider()
    st.subheader("Featured Products")
    cols = st.columns(3)
    for idx, p in enumerate(products[:3]):
        with cols[idx]:
            st.image(p["image"], use_column_width=True)
            st.subheader(p["name"])
            st.write(f"⭐ {p['rating']} | **₹{p['price']}**")
            if st.button("🛒 Add to Cart", key=f"home_{p['id']}"):
                st.session_state.cart.append({**p, "qty": 1})
                st.success("Added!")

# Shop Page (same as before)
elif page == "🛍️ Shop":
    st.title("🛍️ Shop All Products")
    # ... (keeping the same shop logic as previous version for brevity)
    # You can copy the Shop, Cart, Wishlist sections from my last message

# Add other pages (Wishlist, Cart, etc.) from the previous full code I gave you

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    © 2026 CarryMe Store • Authentic Indian Handcrafted Products<br>
    <b>Made with ❤️ in India</b>
</div>
""", unsafe_allow_html=True)
