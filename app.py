import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="CarryMe Store - India's Premium Custom Home Decor",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {font-size: 3.4rem; color: #FF6B6B; text-align: center; margin: 20px 0; font-weight: bold;}
    .product-card {border: 1px solid #eee; border-radius: 16px; padding: 15px; background: white; 
                   box-shadow: 0 4px 15px rgba(0,0,0,0.08); transition: transform 0.2s;}
    .product-card:hover {transform: translateY(-5px);}
    .stButton>button {width: 100%; border-radius: 10px; font-weight: 600; height: 48px;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'cart' not in st.session_state:
    st.session_state.cart = []

# ====================== PRODUCTS ======================
products = [
    {"id": 1, "name": "Handcrafted Terracotta Beaded Necklace", "category": "Jewelry", "price": 599, "rating": 4.8,
     "description": "Premium ethnic terracotta beaded necklace for women.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0011.jpg"},
    {"id": 2, "name": "Traditional Terracotta Jewelry Set", "category": "Jewelry", "price": 449, "rating": 4.7,
     "description": "Beautiful terracotta earrings & necklace set.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/734eeecae73fc3c8aa1fb635b1b8aaef983a0ecd/images/IMG-20260608-WA0000.jpg"},
    {"id": 3, "name": "Waterproof PVC Table Cover - Floral Print", "category": "Table Covers", "price": 299, "rating": 4.6,
     "description": "Heavy duty waterproof PVC table cover with beautiful floral design.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0012.jpg"},
    {"id": 4, "name": "Luxury Quilted Sofa Cover with Lace", "category": "Sofa Covers", "price": 1299, "rating": 4.9,
     "description": "Premium quilted sofa cover with elegant lace border.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/ba13288c6a2841298ba356abea281818e3e8ccbc/images/Sofa%20cover.png"},
    {"id": 5, "name": "Premium Cotton Hand & Face Towel Set", "category": "Towels", "price": 449, "rating": 4.9,
     "description": "Ultra soft & highly absorbent cotton towels.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0016.jpg"},
]

wa_url = "https://wa.me/919250036334"
ig_url = "https://www.instagram.com/carryme_stores"

# Sidebar
st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("**India's Premium Custom Home Decor**")
st.sidebar.markdown(f"[💬 WhatsApp]({wa_url})", unsafe_allow_html=True)
st.sidebar.markdown(f"[📸 Instagram]({ig_url})", unsafe_allow_html=True)

page = st.sidebar.selectbox("Menu", ["🏠 Home", "🛍️ Shop", "✨ Custom Order", "🛒 Cart", "📞 Contact"])

# ====================== HOME ======================
if page == "🏠 Home":
    st.image("https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0009.jpg", use_column_width=True)
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 India’s Premium D2C Custom Home Decor Brand")
    st.caption("Handcrafted • Customized • Delivered with Love")

    st.divider()
    st.subheader("Featured Products")
    cols = st.columns(4)
    for idx, p in enumerate(products):
        with cols[idx % 4]:
            with st.container(border=True):
                st.image(p["image"], use_column_width=True)
                st.subheader(p["name"])
                st.write(f"⭐ {p['rating']} | **₹{p['price']}**")
                if st.button("🛒 Add to Cart", key=f"home_{p['id']}"):
                    st.session_state.cart.append({**p, "qty": 1})
                    st.success("Added to cart!")

# ====================== SHOP ======================
elif page == "🛍️ Shop":
    st.title("🛍️ Product Catalog")
    tab_list = ["All", "Jewelry", "Table Covers", "Sofa Covers", "Towels"]
    tabs = st.tabs(tab_list)
    search = st.text_input("🔍 Search products", "")
    
    for i, tab_name in enumerate(tab_list):
        with tabs[i]:
            filtered = [p for p in products if 
                        (tab_name == "All" or p["category"] == tab_name) and
                        (not search or search.lower() in p["name"].lower())]
            
            cols = st.columns(3)
            for idx, p in enumerate(filtered):
                with cols[idx % 3]:
                    with st.container(border=True):
                        st.image(p["image"], use_column_width=True)
                        st.subheader(p["name"])
                        st.caption(p["description"])
                        st.write(f"⭐ {p['rating']} | **₹{p['price']}**")
                        if st.button("🛒 Add to Cart", key=f"shop_{p['id']}_{i}"):
                            st.session_state.cart.append({**p, "qty": 1})
                            st.success("Added to cart!")

# ====================== CUSTOM ORDER ======================
elif page == "✨ Custom Order":
    st.title("✨ Custom Product Request")
    st.write("Tell us your requirement. We will make it specially for you!")
    
    with st.form("custom_form"):
        name = st.text_input("Your Name *")
        phone = st.text_input("WhatsApp Number *", value="9")
        product_type = st.selectbox("What do you want?", 
                                  ["PVC Table Cover", "Sofa Cover", "Terracotta Jewelry", "Towel Set", "Other Custom Item"])
        requirements = st.text_area("Describe your custom requirement (color, size, design, name, etc.) *")
        budget = st.selectbox("Approx Budget", ["₹200-500", "₹500-1000", "₹1000-2000", "Above ₹2000"])
        
        if st.form_submit_button("📱 Send Request on WhatsApp", type="primary"):
            if name and phone and requirements:
                msg = f"""*Custom Order Request - CarryMe Store*

Name: {name}
Phone: {phone}
Product Type: {product_type}
Budget: {budget}

Requirements:
{requirements}

Please help me create this custom product. Thank you!"""
                
                final_url = f"https://wa.me/919250036334?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
                st.markdown(f"[📱 Open WhatsApp to Send Custom Request]({final_url})", unsafe_allow_html=True)
                st.success("Request ready!")
            else:
                st.error("Please fill all required fields")

# ====================== CART ======================
elif page == "🛒 Cart":
    st.title("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = 0
        for idx, item in enumerate(st.session_state.cart):
            col1, col2, col3 = st.columns([4, 2, 2])
            with col1: st.write(f"**{item['name']}**")
            with col2: 
                qty = st.number_input("Qty", 1, 20, item.get("qty",1), key=f"qty_{idx}")
                st.session_state.cart[idx]["qty"] = qty
            with col3: 
                st.write(f"₹{item['price']*qty}")
                total += item['price']*qty
                if st.button("Remove", key=f"rem_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
        
        st.divider()
        st.subheader(f"**Total: ₹{total}**")
        if st.button("📱 Checkout on WhatsApp", type="primary", use_container_width=True):
            st.markdown(f"[💬 Message CarryMe Store]({wa_url})", unsafe_allow_html=True)

# Contact
elif page == "📞 Contact":
    st.title("📞 Get in Touch")
    st.markdown(f"[💬 Chat on WhatsApp]({wa_url})")
    st.markdown(f"[📸 Follow on Instagram]({ig_url})")

st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 30px;">
    © 2026 CarryMe Store • India's D2C Custom Home Decor Brand<br>
    <b>Handcrafted with Love in India</b>
</div>
""", unsafe_allow_html=True)
