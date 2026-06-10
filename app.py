import streamlit as st
import random
from datetime import datetime

st.set_page_config(
    page_title="CarryMe Store - India's Premium Custom Home Decor",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {font-size: 3.4rem; color: #FF6B6B; text-align: center; margin: 20px 0;}
    .product-card {border-radius: 16px; padding: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);}
    .generated-text {background-color: #f0f2f6; padding: 20px; border-radius: 10px; font-size: 16px; white-space: pre-wrap;}
    .stButton>button {width: 100%; border-radius: 10px; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Products
products = [
    {"id": 1, "name": "Handcrafted Terracotta Beaded Necklace", "category": "Jewelry", "price": 599, "rating": 4.8,
     "description": "Premium ethnic terracotta beaded necklace.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0011.jpg"},
    {"id": 3, "name": "Waterproof PVC Table Cover - Floral Print", "category": "Table Covers", "price": 299, "rating": 4.6,
     "description": "Heavy duty waterproof PVC table cover.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0012.jpg"},
    {"id": 4, "name": "Luxury Quilted Sofa Cover with Lace Border", "category": "Sofa Covers", "price": 1299, "rating": 4.9,
     "description": "Premium quilted sofa cover.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/ba13288c6a2841298ba356abea281818e3e8ccbc/images/Sofa%20cover.png"},
    {"id": 5, "name": "Premium Cotton Hand & Face Towel Set", "category": "Towels", "price": 449, "rating": 4.9,
     "description": "Ultra soft cotton towels.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0016.jpg"},
]

wa_url = "https://wa.me/919250036334"
ig_url = "https://www.instagram.com/carryme_stores"

# Sidebar
st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("**Premium Custom Home Decor**")
st.sidebar.markdown(f"[💬 WhatsApp]({wa_url})", unsafe_allow_html=True)
st.sidebar.markdown(f"[📸 Instagram]({ig_url})", unsafe_allow_html=True)

page = st.sidebar.selectbox("Menu", ["🏠 Home", "🛍️ Shop", "✨ AI Description Generator", "🛒 Cart", "📞 Contact"])

if page == "🏠 Home":
    st.image("https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0009.jpg", use_column_width=True)
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 India’s Premium D2C Custom Home Decor Brand")

elif page == "🛍️ Shop":
    st.title("🛍️ Product Catalog")
    tab_list = ["All", "Jewelry", "Table Covers", "Sofa Covers", "Towels"]
    tabs = st.tabs(tab_list)
    search = st.text_input("🔍 Search", "")
    
    for i, tab_name in enumerate(tab_list):
        with tabs[i]:
            filtered = [p for p in products if (tab_name == "All" or p["category"] == tab_name)]
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
                            st.success("Added!")

elif page == "✨ AI Description Generator":
    st.title("✨ AI Product Description Generator")
    tone = st.selectbox("Tone", ["Professional", "Luxury", "Casual"])
    features = st.text_area("Product Features", height=150)
    if st.button("Generate"):
        if features:
            desc = f"Premium product with {features}. Perfect for your home."
            st.markdown(f"**Generated:**\n{desc}")
        else:
            st.error("Enter features")

elif page == "🛒 Cart":
    st.title("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        total = sum(item['price'] * item.get("qty",1) for item in st.session_state.cart)
        st.write(f"**Total: ₹{total}**")
        if st.button("Checkout on WhatsApp"):
            st.markdown(f"[Open WhatsApp]({wa_url})", unsafe_allow_html=True)

elif page == "📞 Contact":
    st.title("📞 Contact Us")
    st.markdown(f"[💬 WhatsApp]({wa_url})")

st.divider()
st.markdown("© 2026 CarryMe Store")
