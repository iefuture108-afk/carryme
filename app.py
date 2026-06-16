import streamlit as st
from urllib.parse import quote
import requests
from PIL import Image
from io import BytesIO
import json
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="CarryMe Store",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- SESSION STATE INIT ----------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "wishlist" not in st.session_state:
    st.session_state.wishlist = []
if "active_page" not in st.session_state:
    st.session_state.active_page = "🏠 Home"
if "shop_search" not in st.session_state:
    st.session_state.shop_search = ""
if "shop_category" not in st.session_state:
    st.session_state.shop_category = "All"
if "cart_loaded" not in st.session_state:
    st.session_state.cart_loaded = False
if "wishlist_loaded" not in st.session_state:
    st.session_state.wishlist_loaded = False

# ---------- QUERY PARAM SYNC (load from localStorage) ----------
if not st.session_state.cart_loaded:
    params = st.query_params
    if "cart" in params:
        try:
            cart_data = json.loads(params["cart"])
            st.session_state.cart = cart_data
        except:
            pass
        del st.query_params["cart"]
    st.session_state.cart_loaded = True

if not st.session_state.wishlist_loaded:
    params = st.query_params
    if "wishlist" in params:
        try:
            wish_data = json.loads(params["wishlist"])
            st.session_state.wishlist = wish_data
        except:
            pass
        del st.query_params["wishlist"]
    st.session_state.wishlist_loaded = True

# ---------- CONSTANTS ----------
WHATSAPP_NUMBER = "91925035334"
WHATSAPP_DISPLAY = "+91 9250035334"
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUMBER}"
INSTAGRAM_URL = "https://www.instagram.com/carryme_stores?igsh=MWh1M2l3MHl5ZXYzMg=="
BROADCAST_URL = "https://wa.me/91925035334?text=I%20want%20to%20join%20CarryMe%20updates"

# ---------- IMAGE LOADING WITH ERROR HANDLING ----------
@st.cache_data(ttl=3600)
def load_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        st.warning(f"Failed to load image from {url}: {str(e)}")
        return None

def display_image_with_fallback(url, width=None, use_container_width=False):
    img = load_image(url)
    if img is not None:
        if width:
            st.image(img, width=width)
        else:
            st.image(img, use_container_width=use_container_width)
    else:
        st.markdown("<div style='background:#f0f2f6; padding:50px; text-align:center; border-radius:10px;'>🖼️ Image Unavailable</div>", unsafe_allow_html=True)

# ---------- PRODUCT CATALOG (16 products) ----------
products = {
    # Table Covers (8)
    1: {"id": 1, "name": "PVC Waterproof Floral Table Cover", "category": "Table Covers", "price": 299, "rating": 4.5,
        "description": "Waterproof PVC table cover with beautiful floral print. Easy to clean and perfect for daily use.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/file_00000000f900720ba80eca2293d8bd22.png"},
    2: {"id": 2, "name": "Premium Rose Print Table Cover", "category": "Table Covers", "price": 449, "rating": 4.8,
        "description": "Premium quality table cover with elegant rose print design. Adds a touch of luxury to your dining table.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/file_00000000f3887207953b80b42ae8aa39.png"},
    3: {"id": 3, "name": "PVC Basket Weave Table Cover", "category": "Table Covers", "price": 349, "rating": 4.6,
        "description": "Stylish PVC table cover with basket weave texture. Durable, waterproof, and easy to maintain.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/file_000000009eb0720bbc5b9d608913af84.png"},
    4: {"id": 4, "name": "Luxury Dining Table Cover", "category": "Table Covers", "price": 399, "rating": 4.4,
        "description": "Premium dining table cover with elegant finish. Perfect for special occasions and daily use.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/file_000000004d787207b430ff9fe69e5d20.png"},
    5: {"id": 5, "name": "Designer Floral Table Cover", "category": "Table Covers", "price": 429, "rating": 4.7,
        "description": "Beautiful designer floral print table cover. High-quality material with vibrant colors.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/file_00000000f900720ba80eca2293d8bd22.png"},
    6: {"id": 6, "name": "Premium Waterproof Table Cover", "category": "Table Covers", "price": 399, "rating": 4.5,
        "description": "Premium waterproof table cover that protects your table from spills and stains.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/file_00000000f3887207953b80b42ae8aa39.png"},
    7: {"id": 7, "name": "Modern PVC Table Cover", "category": "Table Covers", "price": 299, "rating": 4.3,
        "description": "Modern design PVC table cover. Easy to clean, waterproof, and durable for everyday use.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/file_000000009eb0720bbc5b9d608913af84.png"},
    8: {"id": 8, "name": "Elegant Dining Table Cover", "category": "Table Covers", "price": 449, "rating": 4.9,
        "description": "Elegant dining table cover that enhances your dining experience. Premium quality material.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/file_000000004d787207b430ff9fe69e5d20.png"},
    # Sofa Covers (1)
    9: {"id": 9, "name": "Premium Quilted Sofa Cover", "category": "Sofa Covers", "price": 599, "rating": 4.7,
        "description": "Premium quilted sofa cover designed to protect and enhance your furniture. Soft, durable and easy to maintain for everyday use.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/Sofa%20cover.png"},
    # Terracotta Jewellery (4)
    10: {"id": 10, "name": "Terracotta Beaded Necklace", "category": "Terracotta Jewellery", "price": 149, "rating": 4.6,
        "description": "Beautiful handcrafted terracotta beaded necklace. Perfect for ethnic wear and casual outings.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/IMG-20260608-WA0000.jpg"},
    11: {"id": 11, "name": "Terracotta Pendant Set", "category": "Terracotta Jewellery", "price": 149, "rating": 4.7,
        "description": "Handcrafted terracotta pendant with matching earrings. Unique traditional design.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/IMG-20260608-WA0010.jpg"},
    12: {"id": 12, "name": "Terracotta Earrings", "category": "Terracotta Jewellery", "price": 149, "rating": 4.5,
        "description": "Beautiful terracotta earrings with intricate designs. Lightweight and comfortable.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/IMG-20260608-WA0011.jpg"},
    13: {"id": 13, "name": "Terracotta Bangles Set", "category": "Terracotta Jewellery", "price": 149, "rating": 4.6,
        "description": "Set of 6 terracotta bangles with traditional paintings. Perfect for festivals.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/IMG-20260608-WA0001.jpg"},
    # Towels (1)
    14: {"id": 14, "name": "Premium Cotton Hand & Face Towel", "category": "Towels", "price": 99, "rating": 4.4,
        "description": "Soft cotton hand and face towel with excellent absorbency. Ideal for daily home use and quick drying.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/IMG-20260608-WA0013.jpg"},
    # Wall Decor (2)
    15: {"id": 15, "name": "Decorative Wall Art - Floral", "category": "Wall Decor", "price": 60, "rating": 4.5,
        "description": "Decorative wall art crafted to enhance your living room, bedroom or office interiors with a modern aesthetic appeal.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/fedc9ef879758e6f61b94c12c240ac4b2a933756/images/file_000000002cb871f8a511a4257f06dd37.png"},
    16: {"id": 16, "name": "Decorative Wall Art - Modern", "category": "Wall Decor", "price": 60, "rating": 4.6,
        "description": "Modern wall art piece that adds elegance to any room. Perfect for home and office decor.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/fedc9ef879758e6f61b94c12c240ac4b2a933756/images/file_000000002cb871f8a511a4257f06dd37.png"},
}

categories = ["All", "Table Covers", "Sofa Covers", "Terracotta Jewellery", "Towels", "Wall Decor"]

# ---------- TRUST & URGENCY DATA ----------
BEST_SELLER_IDS = [2, 8, 9, 11] # Premium Rose, Elegant Dining, Sofa Cover, Pendant Set
LIMITED_STOCK_IDS = [4, 7, 13, 15] # Luxury Dining, Modern PVC, Bangles, Floral Wall Art
BUNDLE_PRODUCTS = [2, 14] # Premium Rose Table Cover + Cotton Towel
BUNDLE_PRICE = 449 + 99 - 50 # ₹498 (save ₹50)

TESTIMONIALS = [
    {"name": "Priya S.", "text": "Absolutely love the table covers! Premium quality and fast delivery. Highly recommend CarryMe!"},
    {"name": "Rahul M.", "text": "The terracotta jewellery is stunning. Perfect for gifting. Will order again."},
    {"name": "Ananya K.", "text": "Great experience – the WhatsApp ordering is so convenient. The products match the photos exactly."}
]

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
    save_cart_to_localstorage()

def remove_from_cart(product_id):
    st.session_state.cart = [item for item in st.session_state.cart if item["id"] != product_id]
    save_cart_to_localstorage()

def update_quantity(product_id, new_qty):
    for item in st.session_state.cart:
        if item["id"] == product_id:
            if new_qty > 0:
                item["quantity"] = new_qty
            else:
                remove_from_cart(product_id)
            save_cart_to_localstorage()
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

def toggle_wishlist(product_id):
    if product_id in st.session_state.wishlist:
        st.session_state.wishlist.remove(product_id)
    else:
        st.session_state.wishlist.append(product_id)
    save_wishlist_to_localstorage()
    st.rerun()

def save_cart_to_localstorage():
    pass # handled by script in main render

def save_wishlist_to_localstorage():
    pass

def get_recommendations(cart_items, max_recs=3):
    if not cart_items:
        sorted_products = sorted(products.values(), key=lambda x: x["rating"], reverse=True)
        return [p for p in sorted_products if p["id"] not in [item["id"] for item in cart_items]][:max_recs]
    cart_categories = set()
    for item in cart_items:
        prod = products[item["id"]]
        cart_categories.add(prod["category"])
    recs = []
    for prod in products.values():
        if prod["id"] in [item["id"] for item in cart_items]:
            continue
        if prod["category"] in cart_categories:
            recs.append(prod)
    recs = sorted(recs, key=lambda x: x["rating"], reverse=True)
    if len(recs) < max_recs:
        others = [p for p in products.values() if p["id"] not in [item["id"] for item in cart_items] and p not in recs]
        others = sorted(others, key=lambda x: x["rating"], reverse=True)
        recs.extend(others[:max_recs - len(recs)])
    return recs[:max_recs]

# ---------- JAVASCRIPT FOR localStorage SYNC ----------
js_sync_script = f"""
<script>
function saveToLocalStorage(key, data) {{
    localStorage.setItem(key, JSON.stringify(data));
}}
(function() {{
    const urlParams = new URLSearchParams(window.location.search);
    let needsRedirect = false;
    if (!urlParams.has('cart')) {{
        const cartData = localStorage.getItem('cart');
        if (cartData) {{
            urlParams.set('cart', cartData);
            needsRedirect = true;
        }}
    }}
    if (!urlParams.has('wishlist')) {{
        const wishData = localStorage.getItem('wishlist');
        if (wishData) {{
            urlParams.set('wishlist', wishData);
            needsRedirect = true;
        }}
    }}
    if (needsRedirect) {{
        const newUrl = window.location.pathname + '?' + urlParams.toString();
        window.location.replace(newUrl);
    }}
}})();
window.cartData = {json.dumps(st.session_state.cart)};
window.wishlistData = {json.dumps(st.session_state.wishlist)};
saveToLocalStorage('cart', window.cartData);
saveToLocalStorage('wishlist', window.wishlistData);
</script>
"""

# ---------- DISPLAY PRODUCT CARD (with badges) ----------
def display_product_card(product, key_prefix=""):
    with st.container():
        # Badges
        badges = []
        if product["id"] in BEST_SELLER_IDS:
            badges.append("⭐ Best Seller")
        if product["id"] in LIMITED_STOCK_IDS:
            badges.append("🔥 Limited Stock")
        if badges:
            badge_html = " ".join([f"<span style='background:#ff6b6b; color:white; padding:2px 8px; border-radius:12px; font-size:12px; margin-right:5px;'>{b}</span>" for b in badges])
            st.markdown(f"<div style='margin-bottom:5px;'>{badge_html}</div>", unsafe_allow_html=True)

        display_image_with_fallback(product["image"], use_container_width=True)

        col_heart, col_name = st.columns([1, 5])
        with col_heart:
            is_wish = product["id"] in st.session_state.wishlist
            heart_icon = "❤️" if is_wish else "🤍"
            if st.button(heart_icon, key=f"wish_{key_prefix}_{product['id']}", help="Add to wishlist"):
                toggle_wishlist(product["id"])
        with col_name:
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

# ---------- FOOTER ----------
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
pages = ["🏠 Home", "🛒 Shop", "🎨 AI Marketing Studio", "🛍️ Cart", "📦 Orders", "❤️ Wishlist", "📞 Contact"]
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

# ---------- INJECT SYNC SCRIPT ----------
st.markdown(js_sync_script, unsafe_allow_html=True)

# ---------- AUTO‑CLOSE SIDEBAR ----------
st.markdown("""
<script>
function closeSidebarAutomatically() {
    setTimeout(function() {
        const collapseButton = document.querySelector('[data-testid="stSidebarCollapsedButton"]');
        if (collapseButton) {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar && !sidebar.classList.contains('collapsed')) {
                collapseButton.click();
            }
        }
    }, 200);
}
const observer = new MutationObserver(function(mutations) {
    closeSidebarAutomatically();
});
observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

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

    # Bundle Offer (NEW)
    st.markdown("## 🎁 Special Bundle Offer")
    st.markdown(f"**Buy Premium Rose Table Cover + Cotton Towel together and save ₹50!**")
    st.markdown(f"**Bundle Price: ₹{BUNDLE_PRICE}** (instead of ₹{449+99})")
    if st.button("🛒 Add Bundle to Cart", use_container_width=True)
