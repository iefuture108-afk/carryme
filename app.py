import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="CarryMe Store - Home Decor India",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .product-card {
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Products Data
products = [
    {
        "id": 1,
        "name": "Terracotta Beaded Necklace",
        "category": "Jewelry",
        "price": 599,
        "description": "Handcrafted terracotta jewelry with ethnic design. Perfect for daily wear.",
        "image": "https://via.placeholder.com/300x300/FF6B6B/FFFFFF?text=Terracotta+Necklace",
        "stock": 15
    },
    {
        "id": 2,
        "name": "Terracotta Earrings Set",
        "category": "Jewelry",
        "price": 399,
        "description": "Lightweight terracotta earrings with traditional motifs.",
        "image": "https://via.placeholder.com/300x300/FF6B6B/FFFFFF?text=Terracotta+Earrings",
        "stock": 25
    },
    {
        "id": 3,
        "name": "PVC Table Cover - Floral Print",
        "category": "Table Covers",
        "price": 299,
        "description": "Durable PVC table cover with beautiful floral design. Water resistant.",
        "image": "https://via.placeholder.com/300x300/4ECDC4/FFFFFF?text=PVC+Table+Cover",
        "stock": 30
    },
    {
        "id": 4,
        "name": "Hand Towel Set (3 pcs)",
        "category": "Towels",
        "price": 449,
        "description": "Soft cotton hand towels. Highly absorbent and stylish.",
        "image": "https://via.placeholder.com/300x300/45B8AC/FFFFFF?text=Hand+Towels",
        "stock": 20
    },
    {
        "id": 5,
        "name": "Face Towel Set (4 pcs)",
        "category": "Towels",
        "price": 349,
        "description": "Premium quality face towels for daily use.",
        "image": "https://via.placeholder.com/300x300/45B8AC/FFFFFF?text=Face+Towels",
        "stock": 35
    },
]

# Sidebar
st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("**India's First Home Decor E-commerce**")

page = st.sidebar.selectbox(
    "Navigate",
    ["🏠 Home", "🛍️ Shop Products", "📂 Categories", "🎥 Videos", "🛒 My Cart", "📞 Contact Us"]
)

# ====================== PAGES ======================

if page == "🏠 Home":
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 Authentic Indian Home Decor & Lifestyle Products")
    
    st.image("https://via.placeholder.com/1200x400/FF6B6B/FFFFFF?text=Welcome+to+CarryMe+Store", use_column_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Happy Customers", "500+")
    with col2:
        st.metric("Products Delivered", "1,200+")
    with col3:
        st.metric("States Reached", "15+")
    
    st.divider()
    st.subheader("Featured Products")
    cols = st.columns(3)
    for idx, product in enumerate(products[:3]):
        with cols[idx]:
            st.image(product["image"], use_column_width=True)
            st.write(f"**{product['name']}**")
            st.write(f"₹{product['price']}")
            if st.button("Add to Cart", key=f"feat_{product['id']}"):
                st.session_state.cart.append(product.copy())
                st.success(f"✅ {product['name']} added!")

elif page == "🛍️ Shop Products":
    st.title("🛍️ All Products")
    
    search = st.text_input("🔍 Search products", "")
    category_filter = st.selectbox("Filter by Category", ["All"] + sorted(list(set(p["category"] for p in products))))
    
    filtered = [p for p in products if 
                (not search or search.lower() in p["name"].lower()) and
                (category_filter == "All" or p["category"] == category_filter)]
    
    cols = st.columns(3)
    for idx, product in enumerate(filtered):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(product["image"], use_column_width=True)
                st.subheader(product["name"])
                st.caption(product["description"])
                st.write(f"**₹{product['price']}** | Stock: {product['stock']}")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("🛒 Add to Cart", key=f"add_{product['id']}"):
                        st.session_state.cart.append(product.copy())
                        st.success("Added to cart!")
                with c2:
                    msg = f"Hi CarryMe! I want to buy: {product['name']} (₹{product['price']})"
                    wa_url = f"https://wa.me/919250036334?text={msg.replace(' ', '%20')}"
                    st.markdown(f"[💬 WhatsApp]({wa_url})", unsafe_allow_html=True)

elif page == "📂 Categories":
    st.title("📂 Product Categories")
    cat_cols = st.columns(3)
    cats = {"Jewelry": "🪔", "Table Covers": "🪑", "Towels": "🧖‍♀️"}
    for i, (cat, emoji) in enumerate(cats.items()):
        with cat_cols[i]:
            st.subheader(f"{emoji} {cat}")
            for p in [p for p in products if p["category"] == cat]:
                st.write(f"• {p['name']} — ₹{p['price']}")

elif page == "🎥 Videos":
    st.title("🎥 Our Story & Products")
    st.video("https://youtu.be/dQw4w9wgxcq")  # Replace with your real video
    st.subheader("More Videos Coming Soon...")

elif page == "🛒 My Cart":
    st.title("🛒 Your Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Cart is empty. Start shopping!")
    else:
        total = 0
        for idx, item in enumerate(st.session_state.cart[:]):
            col1, col2, col3 = st.columns([4, 2, 2])
            with col1:
                st.write(f"**{item['name']}**")
            with col2:
                st.write(f"₹{item['price']}")
            with col3:
                if st.button("Remove", key=f"rem_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
            total += item['price']
        
        st.divider()
        st.subheader(f"**Total: ₹{total}**")
        
        if st.button("📱 Order via WhatsApp", type="primary", use_container_width=True):
            items_list = "\n".join([f"• {item['name']} - ₹{item['price']}" for item in st.session_state.cart])
            msg = f"""Hello CarryMe Store!%0A%0AI want to order:%0A{items_list}%0A%0A*Total: ₹{total}*%0A%0APlease share your name, address and phone number."""
            wa_url = f"https://wa.me/919250036334?text={msg}"
            st.markdown(f"[💬 Open WhatsApp to Place Order]({wa_url})", unsafe_allow_html=True)

elif page == "📞 Contact Us":
    st.title("📞 Get in Touch")
    st.markdown("**CarryMe Store** — Authentic Indian Home Decor")
    
    st.subheader("📱 WhatsApp Business")
    st.markdown("[💬 Chat on WhatsApp](https://wa.me/919250036334)")
    
    st.subheader("📷 Instagram")
    st.markdown("[Follow us on Instagram](https://www.instagram.com/carryme_stores)")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    © 2026 CarryMe Store • Made with ❤️ in India<br>
    Authentic • Handcrafted • Premium Quality
</div>
""", unsafe_allow_html=True)
