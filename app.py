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
    .main-header {font-size: 3.2rem; color: #FF6B6B; text-align: center; margin-bottom: 10px;}
    .product-image {border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);}
    .stButton>button {width: 100%; border-radius: 10px; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'cart' not in st.session_state: st.session_state.cart = []
if 'wishlist' not in st.session_state: st.session_state.wishlist = []
if 'orders' not in st.session_state: st.session_state.orders = []

# ====================== REAL PRODUCTS ======================
products = [
    {
        "id": 1, "name": "Terracotta Beaded Necklace", "category": "Jewelry",
        "price": 599, "rating": 4.8, "description": "Handcrafted terracotta beaded necklace with ethnic design.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3369732de9ecaae75947f217dbfc3218156c9c65/images/Gemini_Generated_Image_7ylmma7ylmma7ylm.png",
        "stock": 25
    },
    {
        "id": 2, "name": "Terracotta Jewelry Set", "category": "Jewelry",
        "price": 449, "rating": 4.7, "description": "Beautiful terracotta jewelry set.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/734eeecae73fc3c8aa1fb635b1b8aaef983a0ecd/images/IMG-20260608-WA0000.jpg",
        "stock": 20
    },
    {
        "id": 3, "name": "PVC Table Cover - Premium Print", "category": "Table Covers",
        "price": 299, "rating": 4.6, "description": "High quality waterproof PVC table cover.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/734eeecae73fc3c8aa1fb635b1b8aaef983a0ecd/images/IMG-20260605-WA0023.jpg",
        "stock": 35
    },
    {
        "id": 4, "name": "Elegant PVC Table Cover", "category": "Table Covers",
        "price": 329, "rating": 4.5, "description": "Stylish and durable PVC table cover.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/734eeecae73fc3c8aa1fb635b1b8aaef983a0ecd/images/IMG-20260606-WA0031.jpg",
        "stock": 28
    },
    {
        "id": 5, "name": "Premium Hand Towel Set (3 pcs)", "category": "Towels",
        "price": 449, "rating": 4.9, "description": "Ultra-soft cotton hand towels.",
        "image": "https://via.placeholder.com/400x400/45B8AC/FFFFFF?text=Hand+Towels",
        "stock": 22
    },
]

ig_url = "https://www.instagram.com/carryme_stores"

# Sidebar
st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("**India's Handcrafted Home Decor**")
if st.sidebar.button("📸 Follow on Instagram"):
    st.sidebar.markdown(f"[Open Instagram]({ig_url})", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Menu", ["🏠 Home", "🛍️ Shop", "❤️ Wishlist", "🛒 Cart", "📦 My Orders", "📞 Contact"]
)

# ====================== HOME ======================
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 India’s Most Trusted Handcrafted Home Decor Brand")
    
    st.image("https://via.placeholder.com/1200x450/FF6B6B/FFFFFF?text=CarryMe+Store", use_column_width=True)
    
    st.divider()
    st.subheader("👤 Meet Our Founder")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://raw.githubusercontent.com/iefuture108-afk/carryme/cfd07c238447041c56cb6b796e778d57d4e99bdd/images/IMG-20260608-WA0006.jpg", width=220)
    with col2:
        st.write("Passionate about bringing authentic Indian craftsmanship directly to your home.")
    
    st.divider()
    st.subheader("📸 As Seen on Instagram")
    st.markdown(f"[Follow @carryme_stores]({ig_url})")
    
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
                st.success("Added to cart!")

# ====================== SHOP ======================
elif page == "🛍️ Shop":
    st.title("🛍️ Shop All Products")
    col1, col2, col3 = st.columns([3,2,2])
    with col1: search = st.text_input("🔍 Search", "")
    with col2: category = st.selectbox("Category", ["All"] + sorted({p["category"] for p in products}))
    with col3: sort_by = st.selectbox("Sort", ["Recommended", "Price Low-High", "Price High-Low"])
    
    filtered = [p for p in products if (not search or search.lower() in p["name"].lower()) and (category == "All" or p["category"] == category)]
    if "Low" in sort_by: filtered = sorted(filtered, key=lambda x: x["price"])
    elif "High" in sort_by: filtered = sorted(filtered, key=lambda x: x["price"], reverse=True)
    
    cols = st.columns(3)
    for idx, p in enumerate(filtered):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(p["image"], use_column_width=True)
                st.subheader(p["name"])
                st.caption(p["description"])
                st.write(f"⭐ {p['rating']} • **₹{p['price']}**")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("🛒 Add to Cart", key=f"add_{p['id']}"):
                        st.session_state.cart.append({**p, "qty": 1})
                        st.success("Added!")
                with c2:
                    st.markdown(f"[📸 Instagram]({ig_url})", unsafe_allow_html=True)

# ====================== CART WITH WHATSAPP CHECKOUT ======================
elif page == "🛒 Cart":
    st.title("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        total = 0
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
            total += item['price'] * qty
        
        st.divider()
        st.subheader(f"**Total: ₹{total}**")
        
        st.subheader("📱 WhatsApp Checkout")
        with st.form("checkout"):
            name = st.text_input("Full Name *")
            phone = st.text_input("Phone Number *", value="9")
            address = st.text_area("Delivery Address *")
            pincode = st.text_input("Pincode *")
            
            if st.form_submit_button("Send Order on WhatsApp", type="primary"):
                if name and phone and address and pincode:
                    items_str = "%0A".join([f"• {item['name']} x{item.get('qty',1)} - ₹{item['price']*item.get('qty',1)}" for item in st.session_state.cart])
                    msg = f"""*New Order - CarryMe Store*\n\nName: {name}\nPhone: {phone}\nAddress: {address}\nPincode: {pincode}\n\nOrder:\n{items_str}\n\nTotal: ₹{total}\n\nPlease confirm."""
                    wa_url = f"https://wa.me/919250036334?text={msg}"
                    st.markdown(f"[📱 Open WhatsApp]({wa_url})", unsafe_allow_html=True)
                    st.session_state.orders.append({"date": datetime.now().strftime("%d %b %Y"), "total": total})
                    st.session_state.cart = []
                else:
                    st.error("Please fill all fields")

# Other Pages
elif page == "❤️ Wishlist":
    st.title("❤️ Wishlist")
    # Add logic if needed

elif page == "📦 My Orders":
    st.title("📦 My Orders")
    if st.session_state.orders:
        for order in reversed(st.session_state.orders):
            st.write(f"**{order['date']}** - Total: ₹{order.get('total','N/A')}")
    else:
        st.info("No orders yet")

elif page == "📞 Contact":
    st.title("📞 Contact Us")
    st.markdown("**WhatsApp:** [9250036334](https://wa.me/919250036334)")
    st.markdown(f"**Instagram:** [@carryme_stores]({ig_url})")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    © 2026 CarryMe Store • Authentic Indian Handcrafted Products<br>
    <b>Made with ❤️ in India</b>
</div>
""", unsafe_allow_html=True)
