import streamlit as st
from urllib.parse import quote

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="CarryMe Store",
    page_icon="🛍️",
    layout="wide"
)

# ---------- SESSION STATE INIT ----------
if "cart" not in st.session_state:
    st.session_state.cart = []          # each item: {"id": int, "quantity": int}
if "active_page" not in st.session_state:
    st.session_state.active_page = "🏠 Home"
if "shop_search" not in st.session_state:
    st.session_state.shop_search = ""
if "shop_category" not in st.session_state:
    st.session_state.shop_category = "All"

# ---------- CONSTANTS ----------
WHATSAPP_NUMBER = "91925035334"          # without '+' for wa.me link
WHATSAPP_DISPLAY = "+91 9250035334"
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUMBER}"
INSTAGRAM_URL = "https://www.instagram.com/carryme_stores?igsh=MWh1M2l3MHl5ZXYzMg=="

# ---------- PRODUCT CATALOG (16 items, realistic image URLs) ----------
# Using GitHub raw image placeholders that are category-appropriate
# (Replace these with actual product images if available)
products = {
    # Table Covers (8)
    1: {"id": 1, "name": "Floral Cotton Table Cover", "category": "Table Covers", "price": 299, "rating": 4.5,
        "description": "100% cotton, floral print, machine washable. Perfect for daily use.",
        "image": "https://picsum.photos/id/20/400/300"},
    2: {"id": 2, "name": "Premium Jacquard Table Cover", "category": "Table Covers", "price": 449, "rating": 4.8,
        "description": "Luxurious jacquard weave, elegant pattern, durable fabric.",
        "image": "https://picsum.photos/id/30/400/300"},
    3: {"id": 3, "name": "Traditional Block Print Table Cover", "category": "Table Covers", "price": 349, "rating": 4.6,
        "description": "Hand block printed with natural dyes, unique design.",
        "image": "https://picsum.photos/id/40/400/300"},
    4: {"id": 4, "name": "Modern Geometric Table Cover", "category": "Table Covers", "price": 399, "rating": 4.4,
        "description": "Contemporary geometric pattern, stain resistant, easy care.",
        "image": "https://picsum.photos/id/50/400/300"},
    5: {"id": 5, "name": "Linen Blend Table Cover", "category": "Table Covers", "price": 429, "rating": 4.7,
        "description": "Premium linen blend, natural texture, wrinkle resistant.",
        "image": "https://picsum.photos/id/60/400/300"},
    6: {"id": 6, "name": "Festive Golden Table Cover", "category": "Table Covers", "price": 399, "rating": 4.5,
        "description": "Golden accents, perfect for festivals and celebrations.",
        "image": "https://picsum.photos/id/70/400/300"},
    7: {"id": 7, "name": "Waterproof PVC Table Cover", "category": "Table Covers", "price": 299, "rating": 4.3,
        "description": "Easy-clean waterproof, protects from spills and stains.",
        "image": "https://picsum.photos/id/80/400/300"},
    8: {"id": 8, "name": "Embroidered Table Cover", "category": "Table Covers", "price": 449, "rating": 4.9,
        "description": "Hand-embroidered with intricate thread work, premium finish.",
        "image": "https://picsum.photos/id/90/400/300"},
    # Sofa Covers (1)
    9: {"id": 9, "name": "Stretchable Velvet Sofa Cover", "category": "Sofa Covers", "price": 599, "rating": 4.7,
        "description": "Premium velvet, stretchable, universal fit, includes cushion covers.",
        "image": "https://picsum.photos/id/100/400/300"},
    # Terracotta Jewellery (4)
    10: {"id": 10, "name": "Terracotta Round Earrings", "category": "Terracotta Jewellery", "price": 149, "rating": 4.6,
         "description": "Handcrafted, lightweight, traditional design, nickel-free.",
         "image": "https://picsum.photos/id/110/400/300"},
    11: {"id": 11, "name": "Terracotta Necklace Set", "category": "Terracotta Jewellery", "price": 149, "rating": 4.7,
         "description": "Necklace with matching earrings, perfect for ethnic wear.",
         "image": "https://picsum.photos/id/120/400/300"},
    12: {"id": 12, "name": "Terracotta Bangles Set", "category": "Terracotta Jewellery", "price": 149, "rating": 4.5,
         "description": "Set of 6 bangles with traditional paintings, comfortable.",
         "image": "https://picsum.photos/id/130/400/300"},
    13: {"id": 13, "name": "Terracotta Pendant", "category": "Terracotta Jewellery", "price": 149, "rating": 4.6,
         "description": "Hand-painted pendant with adjustable chain, unique art piece.",
         "image": "https://picsum.photos/id/140/400/300"},
    # Towels (1)
    14: {"id": 14, "name": "Premium Cotton Towel Pack (2 pcs)", "category": "Towels", "price": 99, "rating": 4.4,
         "description": "Highly absorbent, quick drying, set of 2, ideal for daily use.",
         "image": "https://picsum.photos/id/150/400/300"},
    # Wall Decor (2)
    15: {"id": 15, "name": "Wall Hanging Dreamcatcher", "category": "Wall Decor", "price": 60, "rating": 4.5,
         "description": "Beautiful dreamcatcher with feathers and beads, boho decor.",
         "image": "https://picsum.photos/id/160/400/300"},
    16: {"id": 16, "name": "Wooden Wall Art", "category": "Wall Decor", "price": 60, "rating": 4.6,
         "description": "Handcrafted wooden wall art with traditional Indian patterns.",
         "image": "https://picsum.photos/id/170/400/300"},
}

categories = ["All", "Table Covers", "Sofa Covers", "Terracotta Jewellery", "Towels", "Wall Decor"]

# ---------- HELPER FUNCTIONS ----------
def get_cart_item_count():
    return sum(item["quantity"] for item in st.session_state.cart)

def add_to_cart(product_id, quantity=1, replace_cart=False):
    if replace_cart:
        st.session_state.cart = [{"id": product_id, "quantity": quantity}]
    else:
        for item in st.session_state.cart:
            if item["id"] == product_id:
                item["quantity"] += quantity
                return
        st.session_state.cart.append({"id": product_id, "quantity": quantity})

def remove_from_cart(product_id):
    st.session_state.cart = [item for item in st.session_state.cart if item["id"] != product_id]

def update_quantity(product_id, new_qty):
    for item in st.session_state.cart:
        if item["id"] == product_id:
            if new_qty > 0:
                item["quantity"] = new_qty
            else:
                remove_from_cart(product_id)
            return

def get_cart_total():
    total = 0
    for item in st.session_state.cart:
        product = products[item["id"]]
        total += product["price"] * item["quantity"]
    return total

def get_cart_items_details():
    cart_items = []
    for item in st.session_state.cart:
        prod = products[item["id"]]
        cart_items.append({
            "id": prod["id"],
            "name": prod["name"],
            "price": prod["price"],
            "quantity": item["quantity"],
            "subtotal": prod["price"] * item["quantity"],
            "image": prod["image"]
        })
    return cart_items

def generate_whatsapp_order_message():
    if not st.session_state.cart:
        return ""
    message = "🛍️ *CarryMe Store Order* 🛍️\n\n"
    message += "*Order Details:*\n"
    for item in get_cart_items_details():
        message += f"• {item['name']} x {item['quantity']} = ₹{item['subtotal']}\n"
    message += f"\n*Total Amount:* ₹{get_cart_total()}\n\n"
    message += "*Customer Information:*\n"
    message += "Name: \n"
    message += "Address: \n"
    message += "Phone: \n\n"
    message += "Thank you for shopping at CarryMe Store! 🏠✨"
    return message

def set_active_page(page_name):
    st.session_state.active_page = page_name
    st.rerun()

def display_product_card(product, key_prefix=""):
    with st.container():
        st.image(product["image"], use_container_width=True)
        st.markdown(f"**{product['name']}**")
        st.markdown(f"⭐ {product['rating']}/5.0")
        st.markdown(f"**₹{product['price']}**")
        st.caption(product["description"][:80] + "...")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛒 Add to Cart", key=f"{key_prefix}_add_{product['id']}"):
                add_to_cart(product["id"], quantity=1, replace_cart=False)
                st.toast(f"✅ {product['name']} added to cart!", icon="🛒")
                st.rerun()
        with col2:
            if st.button("⚡ Buy Now", key=f"{key_prefix}_buy_{product['id']}"):
                add_to_cart(product["id"], quantity=1, replace_cart=True)
                st.toast("Proceeding to checkout...", icon="⚡")
                set_active_page("🛍️ Cart")
        st.markdown("---")

def render_footer():
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center;padding:20px'>
        <h4>🛍️ CarryMe Store</h4>
        <p>India's Premium Home Decor & Lifestyle Store</p>
        <p>© 2026 CarryMe Store | <a href='{WHATSAPP_URL}' target='_blank'>💬 WhatsApp</a> | <a href='{INSTAGRAM_URL}' target='_blank'>📸 Instagram</a></p>
    </div>
    """, unsafe_allow_html=True)

# ---------- SIDEBAR NAVIGATION ----------
pages = ["🏠 Home", "🛒 Shop", "🎨 AI Marketing Studio", "🛍️ Cart", "📞 Contact"]
cart_count = get_cart_item_count()
cart_label = f"🛍️ Cart ({cart_count})" if cart_count > 0 else "🛍️ Cart"
display_pages = pages.copy()
display_pages[pages.index("🛍️ Cart")] = cart_label

selected_page = st.sidebar.radio("Navigate", display_pages, index=pages.index(st.session_state.active_page))

if selected_page == cart_label:
    selected_page = "🛍️ Cart"

if selected_page != st.session_state.active_page:
    st.session_state.active_page = selected_page
    st.rerun()

# ---------- PAGE: HOME ----------
if st.session_state.active_page == "🏠 Home":
    st.markdown("""
    <div style='text-align:center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 3rem; border-radius: 20px; color: white; margin-bottom: 2rem;'>
        <h1 style='font-size: 3rem;'>CarryMe Store</h1>
        <p style='font-size: 1.5rem;'>India's Premium Home Decor & Lifestyle Store</p>
        <p>Transform Your Home with Elegance & Style 🏠✨</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    st.markdown("## 📊 CarryMe at a Glance")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏷️ Products", "16+")
    with col2:
        st.metric("📂 Categories", "5")
    with col3:
        st.metric("⭐ Avg Rating", "4.6/5")
    with col4:
        st.metric("🚚 Delivery", "Pan India")
    st.markdown("---")

    # Why Choose
    st.markdown("## 🌟 Why Choose CarryMe?")
    cols = st.columns(5)
    benefits = [
        "🏠 Premium Home Decor Collection",
        "🚚 Pan India Delivery",
        "💬 Easy WhatsApp Ordering",
        "⭐ Quality Assured Products",
        "🛍️ Affordable Luxury For Every Home"
    ]
    for i, col in enumerate(cols):
        with col:
            st.info(benefits[i])
    st.markdown("---")

    # Shop by Category
    st.markdown("## 📂 Shop by Category")
    cat_cols = st.columns(len(categories))
    for i, cat in enumerate(categories):
        with cat_cols[i]:
            if st.button(cat, key=f"home_cat_{cat}"):
                st.session_state.shop_category = cat
                st.session_state.shop_search = ""
                set_active_page("🛒 Shop")
    st.markdown("---")

    # Featured Products
    featured_ids = [2, 9, 11, 16]
    featured_products = [products[pid] for pid in featured_ids]
    st.markdown("## 🔥 Featured Products")
    cols = st.columns(4)
    for idx, prod in enumerate(featured_products):
        with cols[idx]:
            display_product_card(prod, key_prefix="featured")

    # WhatsApp CTA
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center; background: #25D366; padding: 2rem; border-radius: 20px; margin: 2rem 0;'>
        <h2 style='color: white;'>Need Help? Chat with us on WhatsApp!</h2>
        <p style='color: white;'>Get personalized recommendations and order assistance</p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("💬 Chat Now on WhatsApp", WHATSAPP_URL, use_container_width=True)

    render_footer()

# ---------- PAGE: SHOP ----------
elif st.session_state.active_page == "🛒 Shop":
    st.markdown("# 🛒 Shop Our Collection")
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search Products", value=st.session_state.shop_search, key="shop_search_input")
        st.session_state.shop_search = search
    with col2:
        category = st.selectbox("Category", categories, index=categories.index(st.session_state.shop_category), key="shop_category_select")
        st.session_state.shop_category = category

    filtered = []
    for prod in products.values():
        if category != "All" and prod["category"] != category:
            continue
        if search and search.lower() not in prod["name"].lower() and search.lower() not in prod["description"].lower():
            continue
        filtered.append(prod)

    st.markdown(f"**Showing {len(filtered)} products**")
    st.markdown("---")

    if len(filtered) == 0:
        st.warning("😕 No products found. Try adjusting your search or category filter.")
    else:
        cols_per_row = 4
        for i in range(0, len(filtered), cols_per_row):
            row_cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(filtered):
                    with row_cols[j]:
                        display_product_card(filtered[i + j], key_prefix=f"shop_{i+j}")

    render_footer()

# ---------- PAGE: AI MARKETING STUDIO ----------
elif st.session_state.active_page == "🎨 AI Marketing Studio":
    st.markdown("# 🎨 AI Marketing Studio")
    st.markdown("Generate compelling marketing content for your products")

    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product Name", placeholder="e.g., Premium Cotton Table Cover")
        product_features = st.text_area("Product Features (one per line)",
                                        placeholder="100% Cotton\nEasy to wash\nBeautiful design\nAvailable in 5 colors")
        if st.button("✨ Generate Marketing Content", type="primary"):
            if product_name and product_features.strip():
                features_list = [line.strip() for line in product_features.split("\n") if line.strip()]
                st.session_state.generated = {"name": product_name, "features": features_list}
                st.rerun()
            else:
                st.error("Please fill both Product Name and Features")

    with col2:
        st.info("💡 **Tips:**\n- Be specific about material & design\n- List 3-5 key features\n- Mention unique selling points")

    if "generated" in st.session_state:
        gen = st.session_state.generated
        st.markdown("---")
        st.markdown("### 📝 Product Description")
        desc = f"Introducing **{gen['name']}** from CarryMe Store! 🌟\n\n✨ **Features:**\n"
        for f in gen["features"]:
            desc += f"• {f}\n"
        desc += "\n🏠 Perfect for your home decor\n🚚 Free Pan India delivery\n💬 Order via WhatsApp\n⭐ Quality assured"
        st.markdown(desc)

        st.markdown("### 📸 Instagram Caption")
        caption = f"🌟 Elevate your space with {gen['name']}! 🌟\n\n"
        caption += "Transform your home with our premium collection.\n\n✨ " + " ✨ ".join(gen["features"][:3]) + "\n\n"
        caption += f"🛍️ Shop now at CarryMe Store\n💬 DM or WhatsApp to order: {WHATSAPP_DISPLAY}\n\n#HomeDecor #CarryMeStore"
        st.markdown(caption)

        st.markdown("### 💬 WhatsApp Message")
        wa_msg = f"*✨ New Arrival at CarryMe Store! ✨*\n\n*Product:* {gen['name']}\n\n*Features:*\n"
        for f in gen["features"]:
            wa_msg += f"✓ {f}\n"
        wa_msg += f"\n*Price:* Starting from ₹149\n*Order Now:* {WHATSAPP_URL}\n\n*Visit CarryMe Store!*"
        st.markdown(wa_msg)

        st.markdown("### 🔍 SEO Title")
        seo = f"{gen['name']} | Premium Home Decor | CarryMe Store India"
        st.markdown(f"**{seo}**")

        if st.button("Clear Generated Content"):
            del st.session_state.generated
            st.rerun()

    render_footer()

# ---------- PAGE: CART ----------
elif st.session_state.active_page == "🛍️ Cart":
    st.markdown("# 🛍️ Your Shopping Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty. Start shopping! 🛒")
        if st.button("Browse Products"):
            set_active_page("🛒 Shop")
    else:
        cart_items = get_cart_items_details()
        for idx, item in enumerate(cart_items):
            col_img, col_name, col_qty, col_price, col_remove = st.columns([1, 3, 1, 1, 1])
            with col_img:
                st.image(item["image"], width=70 if st.session_state.get("is_mobile", False) else 80)
            with col_name:
                st.markdown(f"**{item['name']}**")
                st.caption(f"₹{item['price']} each")
            with col_qty:
                new_qty = st.number_input("Qty", min_value=0, max_value=10, value=item['quantity'],
                                          key=f"cart_qty_{item['id']}", label_visibility="collapsed")
                if new_qty != item['quantity']:
                    update_quantity(item['id'], new_qty)
                    st.rerun()
            with col_price:
                st.markdown(f"**₹{item['subtotal']}**")
            with col_remove:
                if st.button("❌", key=f"cart_remove_{item['id']}"):
                    remove_from_cart(item['id'])
                    st.rerun()
            st.divider()

        total = get_cart_total()
        st.markdown(f"## Total Amount: ₹{total}")

        st.markdown("---")
        st.markdown("### 📱 Complete your order via WhatsApp")
        if st.button("💬 Generate WhatsApp Order Message", type="primary"):
            message = generate_whatsapp_order_message()
            encoded_msg = quote(message)
            wa_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_msg}"
            st.markdown(f"""
            <div style='background:#25D366; padding:1.5rem; border-radius:10px; margin:1rem 0; text-align:center;'>
                <p style='color:white; font-size:1.2rem;'>✅ Click below to place your order on WhatsApp</p>
                <a href='{wa_url}' target='_blank' style='background:white; color:#25D366; padding:0.8rem 2rem; 
                text-decoration:none; border-radius:50px; font-weight:bold; display:inline-block;'>💬 Place Order on WhatsApp</a>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Preview Order Message"):
                st.text(message)

        if st.button("Clear Cart", use_container_width=True):
            st.session_state.cart = []
            st.rerun()

    render_footer()

# ---------- PAGE: CONTACT ----------
elif st.session_state.active_page == "📞 Contact":
    st.markdown("# 📞 Contact Us")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        ### 📱 Get in Touch
        **WhatsApp:** {WHATSAPP_DISPLAY}  
        **Instagram:** [@carryme_stores]({INSTAGRAM_URL})  
        **Email:** care@carrymestore.com  
        **Business Hours:** Mon-Sat, 10 AM – 7 PM
        """)
        col_a, col_b = st.columns(2)
        with col_a:
            st.link_button("💬 WhatsApp Us", WHATSAPP_URL, use_container_width=True)
        with col_b:
            st.link_button("📸 Follow on Instagram", INSTAGRAM_URL, use_container_width=True)

    with col2:
        st.markdown("""
        ### 🏠 Visit Us
        **CarryMe Store**  
        India's Premium Home Decor & Lifestyle Store  
        **Customer Support:** Order assistance, product info, returns, bulk orders.  
        **Fastest response via WhatsApp!**
        """)
        st.info("💡 **Tip:** For fastest response, reach out via WhatsApp. We reply within 15 minutes during business hours!")

    st.markdown("---")
    st.markd
