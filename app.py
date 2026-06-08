import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="CarryMe Store - Premium Indian Home Decor",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-header {font-size: 3.2rem; color: #FF6B6B; text-align: center; margin: 10px 0;}
    .product-card {border: 1px solid #eee; border-radius: 15px; padding: 15px; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.08);}
    .price {font-size: 1.4rem; font-weight: bold; color: #FF6B6B;}
    .stButton>button {width: 100%; border-radius: 8px;}
    .cart-total {font-size: 1.5rem; font-weight: bold;}
    .rating {color: #FFD700;}
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'wishlist' not in st.session_state:
    st.session_state.wishlist = []
if 'orders' not in st.session_state:
    st.session_state.orders = []

# ==================== PRODUCTS (Easy to expand) ====================
products = [
    {"id": 1, "name": "Terracotta Beaded Necklace", "category": "Jewelry", "price": 599, "rating": 4.8,
     "description": "Handcrafted ethnic terracotta necklace. Lightweight & perfect for daily wear.",
     "image": "https://via.placeholder.com/400x400/FF6B6B/FFFFFF?text=Terracotta+Necklace", "stock": 25},
    {"id": 2, "name": "Terracotta Earrings Set", "category": "Jewelry", "price": 399, "rating": 4.7,
     "description": "Beautiful traditional terracotta earrings with vibrant colors.", 
     "image": "https://via.placeholder.com/400x400/FF6B6B/FFFFFF?text=Terracotta+Earrings", "stock": 30},
    {"id": 3, "name": "PVC Table Cover - Floral Print", "category": "Table Covers", "price": 299, "rating": 4.5,
     "description": "Waterproof, durable & elegant PVC table cover. Easy to clean.", 
     "image": "https://via.placeholder.com/400x400/4ECDC4/FFFFFF?text=PVC+Table+Cover", "stock": 40},
    {"id": 4, "name": "Premium Hand Towel Set (3 pcs)", "category": "Towels", "price": 449, "rating": 4.9,
     "description": "Ultra-soft cotton hand towels. Highly absorbent & stylish.", 
     "image": "https://via.placeholder.com/400x400/45B8AC/FFFFFF?text=Hand+Towels", "stock": 22},
    {"id": 5, "name": "Luxury Face Towel Set (4 pcs)", "category": "Towels", "price": 349, "rating": 4.6,
     "description": "Premium face towels for everyday use. Gift-ready packaging.", 
     "image": "https://via.placeholder.com/400x400/45B8AC/FFFFFF?text=Face+Towels", "stock": 35},
]

# ==================== SIDEBAR ====================
st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("**Premium Indian Home Decor**")

page = st.sidebar.selectbox(
    "Menu",
    ["🏠 Home", "🛍️ Shop", "❤️ Wishlist", "🛒 Cart", "📦 My Orders", "🎥 Videos", "📞 Contact"]
)

# ==================== PAGES ====================

if page == "🏠 Home":
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌱 India’s Most Trusted Handcrafted Home Decor Brand")
    
    st.image("https://via.placeholder.com/1200x450/FF6B6B/FFFFFF?text=CarryMe+Store+-+Authentic+Indian+Home+Decor", use_column_width=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Customers", "1,200+")
    with c2: st.metric("Products Sold", "4,500+")
    with c3: st.metric("Cities", "28+")
    with c4: st.metric("Rating", "4.8⭐")
    
    st.divider()
    st.subheader("Featured Products")
    cols = st.columns(3)
    for idx, p in enumerate(products[:3]):
        with cols[idx]:
            st.image(p["image"], use_column_width=True)
            st.write(f"**{p['name']}**")
            st.write(f"⭐ {p['rating']} | ₹{p['price']}")
            if st.button("Add to Cart", key=f"home_{p['id']}"):
                st.session_state.cart.append({**p, "qty": 1})
                st.success("Added!")

elif page == "🛍️ Shop":
    st.title("🛍️ Shop All Products")
    
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        search = st.text_input("🔍 Search", "")
    with col2:
        category = st.selectbox("Category", ["All"] + sorted(set(p["category"] for p in products)))
    with col3:
        sort_by = st.selectbox("Sort by", ["Price: Low to High", "Price: High to Low", "Rating"])
    
    filtered = [p for p in products if 
                (not search or search.lower() in p["name"].lower()) and
                (category == "All" or p["category"] == category)]
    
    if sort_by == "Price: Low to High":
        filtered.sort(key=lambda x: x["price"])
    elif sort_by == "Price: High to Low":
        filtered.sort(key=lambda x: x["price"], reverse=True)
    else:
        filtered.sort(key=lambda x: x["rating"], reverse=True)
    
    cols = st.columns(3)
    for idx, p in enumerate(filtered):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(p["image"], use_column_width=True)
                st.subheader(p["name"])
                st.write(p["description"])
                st.write(f"⭐ {p['rating']} | **₹{p['price']}**")
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("🛒 Add", key=f"add_{p['id']}"):
                        st.session_state.cart.append({**p, "qty": 1})
                        st.success("Added to cart!")
                with c2:
                    if st.button("❤️", key=f"wl_{p['id']}"):
                        if p not in st.session_state.wishlist:
                            st.session_state.wishlist.append(p)
                            st.success("Added to wishlist!")
                with c3:
                    wa_msg = f"I%20want%20to%20buy:%20{p['name']}%20(₹{p['price']})"
                    st.markdown(f"[💬 WhatsApp](https://wa.me/919250036334?text={wa_msg})", unsafe_allow_html=True)

elif page == "❤️ Wishlist":
    st.title("❤️ My Wishlist")
    if not st.session_state.wishlist:
        st.info("Your wishlist is empty.")
    else:
        for p in st.session_state.wishlist:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.image(p["image"], width=120)
                st.write(f"**{p['name']}** - ₹{p['price']}")
            with col2:
                if st.button("Remove", key=f"remwl_{p['id']}"):
                    st.session_state.wishlist = [x for x in st.session_state.wishlist if x['id'] != p['id']]
                    st.rerun()

elif page == "🛒 Cart":
    st.title("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Cart is empty. Start shopping!")
    else:
        total = 0
        for idx, item in enumerate(st.session_state.cart):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            with col1:
                st.write(f"**{item['name']}**")
            with col2:
                qty = st.number_input("Qty", min_value=1, value=item.get("qty", 1), key=f"qty_{idx}")
                st.session_state.cart[idx]["qty"] = qty
            with col3:
                st.write(f"₹{item['price'] * qty}")
            with col4:
                if st.button("Remove", key=f"rem_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
            total += item['price'] * qty
        
        st.divider()
        st.subheader(f"Total: ₹{total}")
        
        if st.button("📱 Place Order via WhatsApp", type="primary", use_container_width=True):
            items_str = "%0A".join([f"• {item['name']} x{item.get('qty',1)} - ₹{item['price']*item.get('qty',1)}" for item in st.session_state.cart])
            msg = f"Hello%20CarryMe!%0A%0AI%20want%20to%20order:%0A{items_str}%0A%0ATotal:%20₹{total}%0A%0APlease%20share%20your%20details."
            st.markdown(f"[💬 Open WhatsApp](https://wa.me/919250036334?text={msg})", unsafe_allow_html=True)
            # Save as order
            st.session_state.orders.append({"date": datetime.now().strftime("%d %b %Y"), "items": st.session_state.cart.copy(), "total": total})

elif page == "📦 My Orders":
    st.title("📦 My Orders")
    if not st.session_state.orders:
        st.info("No orders yet.")
    else:
        for order in reversed(st.session_state.orders):
            st.write(f"**{order['date']}** - Total: ₹{order['total']}")
            for item in order["items"]:
                st.write(f"   • {item['name']} x{item.get('qty',1)}")

elif page == "🎥 Videos":
    st.title("🎥 Behind the Craft")
    st.video("https://youtu.be/dQw4w9wgxcq")  # Replace with real videos
    st.write("Watch how our terracotta jewelry and home products are lovingly handcrafted in India.")

elif page == "📞 Contact":
    st.title("📞 Connect With Us")
    st.markdown("**WhatsApp Business:** [💬 Chat Now](https://wa.me/919250036334)")
    st.markdown("**Instagram:** [Follow @carryme_stores](https://www.instagram.com/carryme_stores)")
    st.write("We reply within minutes during business hours.")

# ==================== FOOTER ====================
st.divider()
st.markdown("""
<div style="text-align:center; color:#666; padding:20px;">
    © 2026 CarryMe Store • Authentic Indian Handcrafted Products<br>
    <b>Made with ❤️ for Every Indian Home</b>
</div>
""", unsafe_allow_html=True)
