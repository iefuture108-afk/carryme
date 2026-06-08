import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="CarryMe Store - Premium Handcrafted Home Decor India",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Image Zoom
st.markdown("""
<style>
    .main-header {font-size: 3.2rem; color: #FF6B6B; text-align: center; margin-bottom: 10px;}
    .zoom-image {
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    .zoom-image:hover {
        transform: scale(1.05);
    }
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.9);
        display: none;
        z-index: 1000;
        justify-content: center;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# Session State
if 'cart' not in st.session_state: st.session_state.cart = []
if 'wishlist' not in st.session_state: st.session_state.wishlist = []
if 'orders' not in st.session_state: st.session_state.orders = []

# ====================== PRODUCTS ======================
products = [
    {
        "id": 1, "name": "Handcrafted Terracotta Beaded Necklace for Women", "category": "Jewelry",
        "price": 599, "rating": 4.8, "description": "Premium ethnic terracotta beaded necklace. Perfect for daily wear and festive occasions.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0011.jpg",
        "stock": 25
    },
    {
        "id": 2, "name": "Traditional Terracotta Jewelry Set", "category": "Jewelry",
        "price": 449, "rating": 4.7, "description": "Beautiful terracotta earrings & necklace set.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/734eeecae73fc3c8aa1fb635b1b8aaef983a0ecd/images/IMG-20260608-WA0000.jpg",
        "stock": 20
    },
    {
        "id": 3, "name": "Waterproof PVC Table Cover - Floral Print", "category": "Table Covers",
        "price": 299, "rating": 4.6, "description": "Heavy duty waterproof PVC table cover with beautiful floral design.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0012.jpg",
        "stock": 35
    },
    {
        "id": 4, "name": "Luxury Quilted Sofa Cover with Lace Border", "category": "Sofa Covers",
        "price": 1299, "rating": 4.9, "description": "Premium quilted sofa cover with elegant lace detailing.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/ba13288c6a2841298ba356abea281818e3e8ccbc/images/Sofa%20cover.png",
        "stock": 18
    },
    {
        "id": 5, "name": "Premium Cotton Hand & Face Towel Set", "category": "Towels",
        "price": 449, "rating": 4.9, "description": "Ultra soft & highly absorbent cotton towels.",
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

# ====================== HOME PAGE ======================
if page == "🏠 Home":
    st.image("https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0009.jpg", use_column_width=True)
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 India’s Most Trusted Handcrafted Home Decor Brand")
    
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

# ====================== SHOP PAGE WITH IMAGE ZOOM ======================
elif page == "🛍️ Shop":
    st.title("🛍️ Shop All Products")
    
    search = st.text_input("🔍 Search products", "")
    all_categories = sorted({p["category"] for p in products})
    selected_categories = st.multiselect("Filter by Category", all_categories, default=all_categories)
    sort_by = st.selectbox("Sort by", ["Recommended", "Price: Low to High", "Price: High to Low", "Rating: High to Low"])
    
    filtered_products = [p for p in products if 
                         (not search or search.lower() in p["name"].lower() or search.lower() in p["description"].lower()) and
                         (p["category"] in selected_categories)]
    
    if sort_by == "Price: Low to High":
        filtered_products = sorted(filtered_products, key=lambda x: x["price"])
    elif sort_by == "Price: High to Low":
        filtered_products = sorted(filtered_products, key=lambda x: x["price"], reverse=True)
    elif sort_by == "Rating: High to Low":
        filtered_products = sorted(filtered_products, key=lambda x: x["rating"], reverse=True)
    
    st.write(f"**Showing {len(filtered_products)} products**")
    
    cols = st.columns(3)
    for idx, p in enumerate(filtered_products):
        with cols[idx % 3]:
            with st.container(border=True):
                # Clickable Zoom Image
                st.markdown(f"""
                <div style="cursor: pointer;" onclick="window.open('{p['image']}', '_blank')">
                    <img src="{p['image']}" style="width:100%; border-radius:12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);" title="Click to zoom">
                </div>
                """, unsafe_allow_html=True)
                
                st.subheader(p["name"])
                st.caption(p["description"])
                st.write(f"⭐ {p['rating']} • **₹{p['price']}** • Stock: {p['stock']}")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("🛒 Add to Cart", key=f"add_{p['id']}"):
                        st.session_state.cart.append({**p, "qty": 1})
                        st.success("Added to cart!")

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
