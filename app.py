import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="CarryMe Store - Premium Handcrafted Home Decor India",
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

# ====================== UPDATED PRODUCTS WITH NEW IMAGES ======================
products = [
    {
        "id": 1, 
        "name": "Handcrafted Terracotta Beaded Necklace for Women",
        "category": "Jewelry",
        "price": 599, 
        "rating": 4.8, 
        "description": "Premium ethnic terracotta beaded necklace. Perfect for daily wear and festive occasions.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0011.jpg",
        "stock": 25
    },
    {
        "id": 2, 
        "name": "Traditional Terracotta Jewelry Set",
        "category": "Jewelry",
        "price": 449, 
        "rating": 4.7, 
        "description": "Beautiful terracotta earrings & necklace set. Traditional Indian design.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/734eeecae73fc3c8aa1fb635b1b8aaef983a0ecd/images/IMG-20260608-WA0000.jpg",
        "stock": 20
    },
    {
        "id": 3, 
        "name": "Waterproof PVC Table Cover - Floral Print",
        "category": "Table Covers",
        "price": 299, 
        "rating": 4.6, 
        "description": "Heavy duty waterproof PVC table cover with beautiful floral design.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0012.jpg",
        "stock": 35
    },
    {
        "id": 4, 
        "name": "Luxury Quilted Sofa Cover with Lace Border",
        "category": "Sofa Covers",
        "price": 1299, 
        "rating": 4.9, 
        "description": "Premium quilted sofa cover with elegant lace detailing. Protects and beautifies your sofa.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/ba13288c6a2841298ba356abea281818e3e8ccbc/images/Sofa%20cover.png",
        "stock": 18
    },
    {
        "id": 5, 
        "name": "Premium Cotton Hand & Face Towel Set",
        "category": "Towels",
        "price": 449, 
        "rating": 4.9, 
        "description": "Ultra soft & highly absorbent cotton hand and face towels. Perfect daily use.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0016.jpg",
        "stock": 30
    },
]

ig_url = "https://www.instagram.com/carryme_stores"

# Sidebar
st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("**Premium Handcrafted Home Decor**")
if st.sidebar.button("📸 Follow on Instagram"):
    st.sidebar.markdown(f"[Open Instagram]({ig_url})", unsafe_allow_html=True)

page = st.sidebar.selectbox("Menu", ["🏠 Home", "🛍️ Shop", "❤️ Wishlist", "🛒 Cart", "📦 My Orders", "📞 Contact"])

# ====================== HOME PAGE WITH LOGO ======================
if page == "🏠 Home":
    # Logo at top
    st.image(
        "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0009.jpg", 
        use_column_width=True
    )
    
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 India’s Most Trusted Handcrafted Home Decor Brand")
    
    st.divider()
    st.subheader("👤 Meet Our Founder")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://raw.githubusercontent.com/iefuture108-afk/carryme/cfd07c238447041c56cb6b796e778d57d4e99bdd/images/IMG-20260608-WA0006.jpg", width=220)
    with col2:
        st.write("Passionate about bringing authentic Indian craftsmanship directly to your home.")
    
    st.divider()
    st.subheader("Featured Products")
    cols = st.columns(3)
    for idx, p in enumerate(products[:4]):
        with cols[idx % 3]:
            st.image(p["image"], use_column_width=True)
            st.subheader(p["name"])
            st.write(f"⭐ {p['rating']} | **₹{p['price']}**")
            if st.button("🛒 Add to Cart", key=f"home_{p['id']}"):
                st.session_state.cart.append({**p, "qty": 1})
                st.success("Added to cart!")

# Shop Page
elif page == "🛍️ Shop":
    st.title("🛍️ Shop Premium Handcrafted Products")
    col1, col2, col3 = st.columns([3,2,2])
    with col1: search = st.text_input("🔍 Search products", "")
    with col2: category = st.selectbox("Category", ["All"] + sorted({p["category"] for p in products}))
    with col3: sort_by = st.selectbox("Sort by", ["Recommended", "Price: Low to High", "Price: High to Low"])
    
    filtered = [p for p in products if 
                (not search or search.lower() in p["name"].lower() or search.lower() in p["description"].lower()) and
                (category == "All" or p["category"] == category)]
    
    if sort_by == "Price: Low to High": filtered = sorted(filtered, key=lambda x: x["price"])
    elif sort_by == "Price: High to Low": filtered = sorted(filtered, key=lambda x: x["price"], reverse=True)
    
    cols = st.columns(3)
    for idx, p in enumerate(filtered):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(p["image"], use_column_width=True)
                st.subheader(p["name"])
                st.caption(p["description"])
                st.write(f"⭐ {p['rating']} • **₹{p['price']}**")
                if st.button("🛒 Add to Cart", key=f"add_{p['id']}"):
                    st.session_state.cart.append({**p, "qty": 1})
                    st.success("Added!")

# Cart Page (WhatsApp Checkout)
elif page == "🛒 Cart":
    st.title("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
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
        with st.form("checkout_form"):
            name = st.text_input("Full Name *")
            phone = st.text_input("Phone Number *", value="9")
            address = st.text_area("Delivery Address *")
            pincode = st.text_input("Pincode *")
            
            if st.form_submit_button("Send Order on WhatsApp", type="primary"):
                if name and phone and address and pincode:
                    items_str = "%0A".join([f"• {item['name']} x{item.get('qty',1)} - ₹{item['price']*item.get('qty',1)}" for item in st.session_state.cart])
                    msg = f"*New Order - CarryMe Store*%0A%0AName: {name}%0APhone: {phone}%0AAddress: {address}%0APincode: {pincode}%0A%0AOrder:%0A{items_str}%0A%0ATotal: ₹{total}"
                    wa_url = f"https://wa.me/919250036334?text={msg}"
                    st.markdown(f"[📱 Open WhatsApp]({wa_url})", unsafe_allow_html=True)
                    st.session_state.orders.append({"date": datetime.now().strftime("%d %b %Y"), "total": total})
                    st.session_state.cart = []
                else:
                    st.error("Please fill all fields.")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    © 2026 CarryMe Store • Authentic Handcrafted Home Decor<br>
    <b>Made with ❤️ in India</b>
</div>
""", unsafe_allow_html=True)
