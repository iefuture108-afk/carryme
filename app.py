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
    .product-card {border: 1px solid #eee; border-radius: 16px; padding: 16px; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.08);}
    .price {font-size: 1.5rem; font-weight: bold; color: #FF6B6B;}
    .stButton>button {width: 100%; border-radius: 10px; font-weight: 600;}
    .rating {color: #FFD700;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'wishlist' not in st.session_state:
    st.session_state.wishlist = []
if 'orders' not in st.session_state:
    st.session_state.orders = []

# ====================== WAREHOUSE PRODUCTS ======================
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
        "image": "https://via.placeholder.com/400x400/FF6B6B/FFFFFF?text=Terracotta+Earrings",
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
        "description": "Ultra-soft cotton hand towels. Highly absorbent and stylish.",
        "image": "https://via.placeholder.com/400x400/45B8AC/FFFFFF?text=Hand+Towels",
        "stock": 22
    },
    {
        "id": 5,
        "name": "Luxury Face Towel Set (4 pcs)",
        "category": "Towels",
        "price": 349,
        "rating": 4.6,
        "description": "Premium quality face towels with soft texture.",
        "image": "https://via.placeholder.com/400x400/45B8AC/FFFFFF?text=Face+Towels",
        "stock": 35
    },
]

# Sidebar
st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("**Premium Indian Handcrafted Decor**")

page = st.sidebar.selectbox(
    "Menu",
    ["🏠 Home", "🛍️ Shop", "❤️ Wishlist", "🛒 Cart", "📦 My Orders", "🎥 Videos", "📞 Contact"]
)

# ====================== PAGES ======================

if page == "🏠 Home":
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 Authentic Indian Home Decor & Lifestyle Products")
    
    st.image("https://via.placeholder.com/1200x450/FF6B6B/FFFFFF?text=CarryMe+Store+-+Handcrafted+with+Love+in+India", use_column_width=True)
    
    # Founder Section
    st.divider()
    st.subheader("👤 Meet Our Founder")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(
            "https://raw.githubusercontent.com/iefuture108-afk/carryme/cfd07c238447041c56cb6b796e778d57d4e99bdd/images/IMG-20260608-WA0006.jpg", 
            width=200
        )
    with col2:
        st.write("**Founder of CarryMe Store**")
        st.write("Passionate about promoting authentic Indian handcrafted products. Our mission is to bring the best of Indian craftsmanship directly to your home.")
    
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

elif page == "🛍️ Shop":
    st.title("🛍️ Shop All Products")
    
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1: search = st.text_input("🔍 Search", "")
    with col2: 
        category = st.selectbox("Category", ["All"] + sorted(set(p["category"] for p in products)))
    with col3: 
        sort_by = st.selectbox("Sort by", ["Recommended", "Price: Low to High", "Price: High to Low", "Rating"])
    
    filtered = [p for p in products if 
                (not search or search.lower() in p["name"].lower()) and
                (category == "All" or p["category"] == category)]
    
    if sort_by == "Price: Low to High":
        filtered = sorted(filtered, key=lambda x: x["price"])
    elif sort_by == "Price: High to Low":
        filtered = sorted(filtered, key=lambda x: x["price"], reverse=True)
    elif sort_by == "Rating":
        filtered = sorted(filtered, key=lambda x: x["rating"], reverse=True)
    
    cols = st.columns(3)
    for idx, p in enumerate(filtered):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(p["image"], use_column_width=True)
                st.subheader(p["name"])
                st.caption(p["description"])
                st.write(f"⭐ {p['rating']} • **₹{p['price']}** • Stock: {p['stock']}")
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("🛒 Add to Cart", key=f"add_{p['id']}"):
                        st.session_state.cart.append({**p, "qty": 1})
                        st.success("Added!")
                with c2:
                    if st.button("❤️", key=f"wl_{p['id']}"):
                        if p not in st.session_state.wishlist:
                            st.session_state.wishlist.append(p)
                            st.success("Wishlist!")
                with c3:
                    wa_msg = f"I%20want%20to%20buy:%20{p['name']}%20(₹{p['price']})"
                    st.markdown(f"[💬 WhatsApp](https://wa.me/919250036334?text={wa_msg})", unsafe_allow_html=True)

# Wishlist Page
elif page == "❤️ Wishlist":
    st.title("❤️ My Wishlist")
    if not st.session_state.wishlist:
        st.info("Wishlist is empty.")
    else:
        for p in st.session_state.wishlist[:]:
            col1, col2 = st.columns([5,1])
            with col1:
                st.image(p["image"], width=120)
                st.write(f"**{p['name']}** - ₹{p['price']}")
            with col2:
                if st.button("Remove", key=f"remwl_{p['id']}"):
                    st.session_state.wishlist = [x for x in st.session_state.wishlist if x['id'] != p['id']]
                    st.rerun()

# Cart Page
elif page == "🛒 Cart":
    st.title("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Cart is empty.")
    else:
        total = 0
        for idx, item in enumerate(st.session_state.cart[:]):
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
        
        if st.button("📱 Place Order via WhatsApp", type="primary", use_container_width=True):
            items_str = "%0A".join([f"• {item['name']} x{item.get('qty',1)} - ₹{item['price']*item.get('qty',1)}" for item in st.session_state.cart])
            msg = f"Hello%20CarryMe!%0A%0AOrder%20Details:%0A{items_str}%0A%0ATotal:%20₹{total}"
            st.markdown(f"[💬 Open WhatsApp](https://wa.me/919250036334?text={msg})", unsafe_allow_html=True)
            st.session_state.orders.append({"date": datetime.now().strftime("%d %b %Y"), "total": total, "items": st.session_state.cart.copy()})
            st.session_state.cart = []

# Other Pages
elif page == "📦 My Orders":
    st.title("📦 My Orders")
    if not st.session_state.orders:
        st.info("No orders yet.")
    else:
        for order in reversed(st.session_state.orders):
            st.write(f"**{order['date']}** - Total: ₹{order['total']}")

elif page == "🎥 Videos":
    st.title("🎥 Craft Videos")
    st.video("https://youtu.be/dQw4w9wgxcq")  # Replace with real video later

elif page == "📞 Contact":
    st.title("📞 Contact Us")
    st.markdown("**WhatsApp:** [9250036334](https://wa.me/919250036334)")
    st.markdown("**Instagram:** [@carryme_stores](https://www.instagram.com/carryme_stores)")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    © 2026 CarryMe Store • Authentic Indian Handcrafted Products<br>
    <b>Made with ❤️ in India</b>
</div>
""", unsafe_allow_html=True)
