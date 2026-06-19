import streamlit as st
from urllib.parse import quote
import requests
from PIL import Image
from io import BytesIO
import json
import time
import google.generativeai as genai

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="CarryMe.store – Elevate Your Everyday",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- BRAND CONSTANTS ----------
BRAND_NAME = "CarryMe.store"
TAGLINE = "ELEVATE YOUR EVERYDAY"
SUBTITLE = "LUXURY · FASHION · HOME · GIFTING"
FOUNDER_NAME = "Priya Srivastava"
FOUNDER_TITLE = "Fashion Designer | 15 Years of Experience"
FOUNDER_DESC = (
    "With a passion for design and a keen eye for detail, Priya brings 15 years of "
    "experience in the fashion and home decor industry. Her vision is to blend "
    "luxury with everyday comfort, making premium products accessible to every home."
)

# Asset URLs – replace with your actual images
LOGO_URL = "https://raw.githubusercontent.com/iefuture108-afk/carryme/main/assets/logo.png"
FOUNDER_IMG_URL = "https://raw.githubusercontent.com/iefuture108-afk/carryme/main/assets/founder.jpg"
# Fallback if images not available
def check_url(url):
    try:
        return requests.head(url, timeout=5).ok
    except:
        return False
if not check_url(LOGO_URL):
    LOGO_URL = "https://picsum.photos/200/80?random=1"
if not check_url(FOUNDER_IMG_URL):
    FOUNDER_IMG_URL = "https://picsum.photos/300/300?random=2"

# ---------- GEMINI SETUP ----------
GEMINI_AVAILABLE = False
try:
    gemini_key = st.secrets.get("GEMINI_API_KEY")
    if gemini_key:
        genai.configure(api_key=gemini_key)
        GEMINI_AVAILABLE = True
except:
    pass

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

# ---------- LOAD CART/WISHLIST FROM localStorage ----------
def load_cart_from_local():
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

load_cart_from_local()

# ---------- CONSTANTS ----------
WHATSAPP_NUMBER = "91925035334"
WHATSAPP_DISPLAY = "+91 9250035334"
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUMBER}"
INSTAGRAM_URL = "https://www.instagram.com/carryme_stores?igsh=MWh1M2l3MHl5ZXYzMg=="
BROADCAST_URL = "https://wa.me/91925035334?text=I%20want%20to%20join%20CarryMe%20updates"

# ---------- IMAGE LOADING ----------
@st.cache_data(ttl=3600)
def load_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except:
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
    9: {"id": 9, "name": "Premium Quilted Sofa Cover", "category": "Sofa Covers", "price": 599, "rating": 4.7,
        "description": "Premium quilted sofa cover designed to protect and enhance your furniture. Soft, durable and easy to maintain for everyday use.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/Sofa%20cover.png"},
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
    14: {"id": 14, "name": "Premium Cotton Hand & Face Towel", "category": "Towels", "price": 99, "rating": 4.4,
        "description": "Soft cotton hand and face towel with excellent absorbency. Ideal for daily home use and quick drying.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/af68f285b673ad84dd018c10b79e697c3450a910/images/IMG-20260608-WA0013.jpg"},
    15: {"id": 15, "name": "Decorative Wall Art - Floral", "category": "Wall Decor", "price": 60, "rating": 4.5,
        "description": "Decorative wall art crafted to enhance your living room, bedroom or office interiors with a modern aesthetic appeal.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/fedc9ef879758e6f61b94c12c240ac4b2a933756/images/file_000000002cb871f8a511a4257f06dd37.png"},
    16: {"id": 16, "name": "Decorative Wall Art - Modern", "category": "Wall Decor", "price": 60, "rating": 4.6,
        "description": "Modern wall art piece that adds elegance to any room. Perfect for home and office decor.",
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/fedc9ef879758e6f61b94c12c240ac4b2a933756/images/file_000000002cb871f8a511a4257f06dd37.png"},
}

categories = ["All", "Table Covers", "Sofa Covers", "Terracotta Jewellery", "Towels", "Wall Decor"]

# ---------- TRUST & URGENCY DATA ----------
BEST_SELLER_IDS = [2, 8, 9, 11]
LIMITED_STOCK_IDS = [4, 7, 13, 15]
BUNDLE_PRODUCTS = [2, 14]
BUNDLE_PRICE = 449 + 99 - 50
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
    # Save to localStorage via JS (handled by script on page load)

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
    total = get_cart_total()
    message += f"\n*Total Amount:* ₹{total}\n"
    message += "\n*Customer Information:*\n"
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

# ---------- GEMINI CONTENT GENERATION ----------
def generate_marketing_content(product_name, features):
    if not GEMINI_AVAILABLE:
        return "❌ Gemini API key not set. Please add `GEMINI_API_KEY` to secrets."
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        You are a professional marketing copywriter for a luxury home decor brand called CarryMe.store.

        Product: {product_name}
        Key Features: {features}

        Write the following marketing content:

        1. **Product Description** (50-70 words, persuasive and elegant)
        2. **Instagram Caption** (with hashtags, engaging)
        3. **WhatsApp Message** (short, promotional, with a call to action)
        4. **SEO Title** (optimized for search)

        Format your response clearly with headings and bullet points where appropriate.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Gemini error: {str(e)}"

# ---------- DISPLAY PRODUCT CARD ----------
def display_product_card(product, key_prefix=""):
    with st.container():
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
        <h4>🛍️ {BRAND_NAME}</h4>
        <p>{TAGLINE} | {SUBTITLE}</p>
        <p>© 2026 {BRAND_NAME} | <a href='{WHATSAPP_URL}' target='_blank'>💬 WhatsApp</a> | <a href='{INSTAGRAM_URL}' target='_blank'>📸 Instagram</a></p>
    </div>
    """, unsafe_allow_html=True)

# ---------- SIDEBAR NAVIGATION ----------
pages = ["🏠 Home", "🛒 Shop", "🎨 AI Marketing Studio", "🛍️ Cart", "📦 Orders", "❤️ Wishlist", "📞 Contact"]
st.sidebar.title(BRAND_NAME)
st.sidebar.caption(TAGLINE)
cart_count = get_cart_item_count()
cart_label = f"🛍️ Cart ({cart_count})" if cart_count > 0 else "🛍️ Cart"
display_pages = pages.copy()
if "🛍️ Cart" in display_pages:
    display_pages[display_pages.index("🛍️ Cart")] = cart_label

selected_page = st.sidebar.radio("Navigate", display_pages, index=pages.index(st.session_state.active_page) if st.session_state.active_page in pages else 0)
if selected_page == cart_label:
    selected_page = "🛍️ Cart"
if selected_page != st.session_state.active_page:
    st.session_state.active_page = selected_page
    st.rerun()

# ---------- JS SYNC FOR localStorage ----------
st.markdown(f"""
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
""", unsafe_allow_html=True)

# ---------- AUTO-CLOSE SIDEBAR ----------
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

# ---------- PAGE RENDERING ----------
# HOME
if st.session_state.active_page == "🏠 Home":
    st.markdown(f"""
    <div style='text-align:center; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                padding: 3rem; border-radius: 20px; color: white; margin-bottom: 2rem;'>
        <img src='{LOGO_URL}' style='width: 120px; margin-bottom: 0.5rem;' alt='CarryMe.store'>
        <h1 style='font-size: 3rem; margin: 0;'>{BRAND_NAME}</h1>
        <p style='font-size: 2rem; font-weight: 300; margin: 0;'>{TAGLINE}</p>
        <p style='font-size: 1.2rem; letter-spacing: 4px; opacity: 0.9;'>{SUBTITLE}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 👩‍🎨 Meet Our Founder")
    col1, col2 = st.columns([1, 2])
    with col1:
        display_image_with_fallback(FOUNDER_IMG_URL, width=250)
    with col2:
        st.markdown(f"### {FOUNDER_NAME}")
        st.markdown(f"*{FOUNDER_TITLE}*")
        st.write(FOUNDER_DESC)
        st.caption("“Design is not just what it looks like – it's how it makes you feel.”")
    st.markdown("---")

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

    st.markdown("## 🎁 Special Bundle Offer")
    st.markdown(f"**Buy Premium Rose Table Cover + Cotton Towel together and save ₹50!**")
    st.markdown(f"**Bundle Price: ₹{BUNDLE_PRICE}** (instead of ₹{449+99})")
    if st.button("🛒 Add Bundle to Cart", use_container_width=True):
        for pid in BUNDLE_PRODUCTS:
            add_to_cart(pid, quantity=1, replace_cart=False)
        st.toast("✅ Bundle added to cart! You saved ₹50.", icon="🎁")
        st.rerun()
    st.markdown("---")

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

    st.markdown("## 💬 What Our Customers Say")
    test_cols = st.columns(len(TESTIMONIALS))
    for i, test in enumerate(TESTIMONIALS):
        with test_cols[i]:
            st.markdown(f"*“{test['text']}”*")
            st.caption(f"— {test['name']}")
    st.markdown("---")

    st.markdown("## 📂 Shop by Category")
    cat_cols = st.columns(len(categories))
    for i, cat in enumerate(categories):
        with cat_cols[i]:
            if st.button(cat, key=f"home_cat_{cat}"):
                st.session_state.shop_category = cat
                st.session_state.shop_search = ""
                set_active_page("🛒 Shop")
    st.markdown("---")

    featured_ids = [2, 8, 9, 11]
    featured_products = [products[pid] for pid in featured_ids]
    st.markdown("## 🔥 Featured Products")
    cols = st.columns(4)
    for idx, prod in enumerate(featured_products):
        with cols[idx]:
            display_product_card(prod, key_prefix="featured")

    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center; background: #25D366; padding: 2rem; border-radius: 20px; margin: 2rem 0;'>
        <h2 style='color: white;'>Stay Updated!</h2>
        <p style='color: white;'>Get exclusive offers and new arrivals on WhatsApp</p>
        <a href='{BROADCAST_URL}' target='_blank' style='background:white; color:#25D366; padding:0.8rem 2rem; 
                text-decoration:none; border-radius:50px; font-weight:bold; display:inline-block;'>📨 Join Our Broadcast List</a>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("💬 Chat Now on WhatsApp", WHATSAPP_URL, use_container_width=True)
    render_footer()

# SHOP
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

# AI MARKETING STUDIO (Gemini powered)
elif st.session_state.active_page == "🎨 AI Marketing Studio":
    st.markdown("# 🎨 AI Marketing Studio")
    if not GEMINI_AVAILABLE:
        st.warning("⚠️ Gemini API key not set. Add `GEMINI_API_KEY` to Streamlit secrets to enable AI-powered content.")
        st.info("You can still use the template generator (no AI).")
    else:
        st.success("✅ Gemini AI is active – generate professional marketing content!")

    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product Name", placeholder="e.g., Premium Cotton Table Cover")
        product_features = st.text_area("Product Features (one per line)",
                                        placeholder="100% Cotton\nEasy to wash\nBeautiful design\nAvailable in 5 colors")
        if st.button("✨ Generate Marketing Content", type="primary"):
            if product_name and product_features.strip():
                features_list = [line.strip() for line in product_features.split("\n") if line.strip()]
                with st.spinner("Generating content with Gemini..."):
                    if GEMINI_AVAILABLE:
                        content = generate_marketing_content(product_name, "\n".join(features_list))
                        st.session_state.generated = content
                    else:
                        # Fallback template
                        content = f"### 📝 Product Description\nIntroducing **{product_name}** from CarryMe Store!\n\n**Features:**\n"
                        for f in features_list:
                            content += f"• {f}\n"
                        content += "\n🏠 Perfect for your home decor\n🚚 Free Pan India delivery\n💬 Order via WhatsApp\n⭐ Quality assured"
                        st.session_state.generated = content
                st.rerun()
            else:
                st.error("Please fill both Product Name and Features")

    with col2:
        st.info("💡 **Tips:**\n- Be specific about material & design\n- List 3-5 key features\n- Mention unique selling points")
        if GEMINI_AVAILABLE:
            st.info("🤖 Gemini will create: Product Description, Instagram Caption, WhatsApp Message, and SEO Title.")

    if "generated" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state.generated)
        if st.button("Clear Generated Content"):
            del st.session_state.generated
            st.rerun()

    render_footer()

# CART
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
                display_image_with_fallback(item["image"], width=70)
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
        st.markdown("### 💡 You may also like")
        recs = get_recommendations(cart_items, max_recs=3)
        if recs:
            rec_cols = st.columns(len(recs))
            for idx, rec in enumerate(recs):
                with rec_cols[idx]:
                    st.image(rec["image"], use_container_width=True)
                    st.markdown(f"**{rec['name']}**")
                    st.markdown(f"⭐ {rec['rating']}/5.0")
                    st.markdown(f"**₹{rec['price']}**")
                    if st.button(f"➕ Add to Cart", key=f"rec_add_{rec['id']}"):
                        add_to_cart(rec["id"], quantity=1)
                        st.rerun()
        else:
            st.caption("No recommendations at the moment.")

        st.markdown("---")
        st.markdown("### 📱 Complete your order via WhatsApp")
        if st.button("💬 Generate WhatsApp Order Message", type="primary"):
            # Save order to localStorage (via JS)
            order_data = {
                "items": cart_items,
                "total": total,
                "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "order_id": int(time.time())
            }
            st.markdown(f"""
            <script>
            let orders = JSON.parse(localStorage.getItem('orders') || '[]');
            orders.push({json.dumps(order_data)});
            localStorage.setItem('orders', JSON.stringify(orders));
            </script>
            """, unsafe_allow_html=True)
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

# ORDERS
elif st.session_state.active_page == "📦 Orders":
    st.markdown("# 📦 Order History")
    st.markdown("""
    <div id="order-history"></div>
    <script>
    (function() {
        const orders = JSON.parse(localStorage.getItem('orders') || '[]');
        const container = document.getElementById('order-history');
        if (orders.length === 0) {
            container.innerHTML = '<p>No orders yet. Start shopping!</p>';
            return;
        }
        let html = '';
        orders.reverse().forEach(function(order) {
            html += `<div style='border:1px solid #ddd; border-radius:10px; padding:15px; margin-bottom:15px;'>`;
            html += `<p><strong>Order #${order.order_id}</strong> - ${order.date}</p>`;
            html += `<p><strong>Total:</strong> ₹${order.total}</p>`;
            html += `<ul>`;
            order.items.forEach(function(item) {
                html += `<li>${item.name} x ${item.quantity} = ₹${item.subtotal}</li>`;
            });
            html += `</ul></div>`;
        });
        container.innerHTML = html;
    })();
    </script>
    """, unsafe_allow_html=True)
    st.info("💡 Orders are stored only in your browser’s local storage. They persist until you clear browser data.")
    render_footer()

# WISHLIST
elif st.session_state.active_page == "❤️ Wishlist":
    st.markdown("# ❤️ Your Wishlist")
    if not st.session_state.wishlist:
        st.info("Your wishlist is empty. Browse products and click the heart icon to save them.")
        if st.button("Start Shopping"):
            set_active_page("🛒 Shop")
    else:
        wishlist_products = [products[pid] for pid in st.session_state.wishlist if pid in products]
        if not wishlist_products:
            st.info("Some wishlist items are no longer available.")
        else:
            cols = st.columns(3)
            for idx, prod in enumerate(wishlist_products):
                with cols[idx % 3]:
                    display_product_card(prod, key_prefix=f"wish_{idx}")
    render_footer()

# CONTACT
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
        **Fastest response via WhatsApp!
        """)
        st.info("💡 **Tip:** For fastest response, reach out via WhatsApp. We reply within 15 minutes during business hours!")
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center; padding:2rem; background: linear-gradient(135deg, #667eea, #764ba2); 
                border-radius:20px; color:white;'>
        <h3>✨ Let's Decorate Your Dream Home ✨</h3>
        <p>We're here to help you find the perfect pieces for your space!</p>
        <p>🇮🇳 Proudly serving homes across India</p>
        <p><a href='{WHATSAPP_URL}' style='color:white;'>💬 WhatsApp</a> | <a href='{INSTAGRAM_URL}' style='color:white;'>📸 Instagram</a></p>
    </div>
    """, unsafe_allow_html=True)
    render_footer()

# FALLBACK
else:
    st.error("Page not found.")
    st.session_state.active_page = "🏠 Home"
    st.rerun()
