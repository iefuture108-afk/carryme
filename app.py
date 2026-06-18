import streamlit as st
from urllib.parse import quote
import requests
from PIL import Image
from io import BytesIO
import json
import time
import uuid
import os
import hmac
import hashlib

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

# Asset URLs – adjust to your actual image paths
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

# ---------- FIREBASE INIT (with graceful fallback) ----------
FIREBASE_AVAILABLE = False
db = None
auth = None

try:
    firebase_creds = st.secrets["firebase_creds"]
    firebase_config = st.secrets["firebase_config"]
    import pyrebase4 as pyrebase
    import firebase_admin
    from firebase_admin import credentials, firestore

    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    auth = pyrebase.initialize_app(firebase_config).auth()
    FIREBASE_AVAILABLE = True
except Exception as e:
    st.warning(f"Firebase not available. Running in guest mode (local storage only). Error: {e}")
    FIREBASE_AVAILABLE = False
    db = None
    auth = None

# ---------- SESSION STATE INIT ----------
if "user" not in st.session_state:
    st.session_state.user = None          # { "uid": "...", "email": "..." }
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
if "points" not in st.session_state:
    st.session_state.points = 0
if "referral_code" not in st.session_state:
    st.session_state.referral_code = None
if "used_referral" not in st.session_state:
    st.session_state.used_referral = False

# ---------- QUERY PARAM SYNC (guest cart) ----------
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

if not st.session_state.user:
    load_cart_from_local()

# ---------- FIREBASE AUTH FUNCTIONS ----------
def login(email, password):
    if not FIREBASE_AVAILABLE:
        st.error("Firebase not available. Please check configuration.")
        return
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state.user = {"uid": user["localId"], "email": email}
        load_user_data()
        st.success("Logged in!")
        st.rerun()
    except Exception as e:
        st.error(f"Login failed: {e}")

def register(email, password, referral_code=None):
    if not FIREBASE_AVAILABLE:
        st.error("Firebase not available. Please check configuration.")
        return
    try:
        user = auth.create_user_with_email_and_password(email, password)
        uid = user["localId"]
        st.session_state.user = {"uid": uid, "email": email}
        # Create user document in Firestore
        user_ref = db.collection("users").document(uid)
        user_ref.set({
            "email": email,
            "points": 0,
            "referral_code": generate_referral_code(uid),
            "referred_by": referral_code,
            "used_referral": False,
            "cart": [],
            "wishlist": [],
            "orders": [],
            "created_at": firestore.SERVER_TIMESTAMP
        })
        # Handle referral points
        if referral_code:
            referrer_query = db.collection("users").where("referral_code", "==", referral_code).get()
            if referrer_query:
                referrer_doc = referrer_query[0]
                referrer_ref = db.collection("users").document(referrer_doc.id)
                referrer_ref.update({"points": firestore.Increment(50)})
                user_ref.update({"used_referral": True})
        load_user_data()
        st.success("Account created!")
        st.rerun()
    except Exception as e:
        st.error(f"Registration failed: {e}")

def generate_referral_code(uid):
    return uid[:6].upper()

def load_user_data():
    if not FIREBASE_AVAILABLE or not st.session_state.user:
        return
    uid = st.session_state.user["uid"]
    doc = db.collection("users").document(uid).get()
    if doc.exists:
        data = doc.to_dict()
        st.session_state.cart = data.get("cart", [])
        st.session_state.wishlist = data.get("wishlist", [])
        st.session_state.points = data.get("points", 0)
        st.session_state.referral_code = data.get("referral_code", "")
        st.session_state.used_referral = data.get("used_referral", False)
    else:
        # create default document
        db.collection("users").document(uid).set({
            "email": st.session_state.user["email"],
            "points": 0,
            "referral_code": generate_referral_code(uid),
            "referred_by": None,
            "used_referral": False,
            "cart": [],
            "wishlist": [],
            "orders": []
        })
        st.session_state.points = 0
        st.session_state.referral_code = generate_referral_code(uid)

def save_user_data():
    if not FIREBASE_AVAILABLE or not st.session_state.user:
        return
    uid = st.session_state.user["uid"]
    db.collection("users").document(uid).update({
        "cart": st.session_state.cart,
        "wishlist": st.session_state.wishlist,
        "points": st.session_state.points
    })

def sign_out():
    save_user_data()
    st.session_state.user = None
    st.session_state.cart = []
    st.session_state.wishlist = []
    st.session_state.points = 0
    st.session_state.referral_code = None
    st.session_state.used_referral = False
    st.rerun()

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
    except Exception as e:
        # Don't show warning for every image; just return None
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
    if st.session_state.user:
        save_user_data()

def remove_from_cart(product_id):
    st.session_state.cart = [item for item in st.session_state.cart if item["id"] != product_id]
    if st.session_state.user:
        save_user_data()

def update_quantity(product_id, new_qty):
    for item in st.session_state.cart:
        if item["id"] == product_id:
            if new_qty > 0:
                item["quantity"] = new_qty
            else:
                remove_from_cart(product_id)
            if st.session_state.user:
                save_user_data()
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
    if st.session_state.user:
        save_user_data()
    st.rerun()

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

# ---------- SIDEBAR NAVIGATION & AUTH ----------
pages = ["🏠 Home", "🛒 Shop", "🎨 AI Marketing Studio", "🛍️ Cart", "📦 Orders", "❤️ Wishlist", "📞 Contact"]
if st.query_params.get("admin") == "true":
    pages.append("📊 Admin")

# Auth sidebar
st.sidebar.title(BRAND_NAME)
st.sidebar.caption(TAGLINE)
if not st.session_state.user:
    st.sidebar.subheader("🔐 Account")
    with st.sidebar.expander("Login / Register"):
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                login(email, password)
        with tab2:
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_pass")
            ref_code = st.text_input("Referral Code (optional)", key="reg_ref")
            if st.button("Register"):
                register(email, password, ref_code.strip() if ref_code else None)
else:
    st.sidebar.write(f"👋 Welcome, {st.session_state.user['email']}")
    st.sidebar.write(f"⭐ Points: {st.session_state.points}")
    if st.session_state.referral_code:
        st.sidebar.write(f"🔗 Your referral code: `{st.session_state.referral_code}`")
        share_link = f"https://carryme.store?ref={st.session_state.referral_code}"
        st.sidebar.markdown(f"Share your link: [Copy]({share_link})")
    if st.sidebar.button("Logout"):
        sign_out()

# Navigation
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

# ---------- JS SYNC FOR GUESTS ----------
if not st.session_state.user:
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

# ---------- PAGE: HOME ----------
if st.session_state.active_page == "🏠 Home":
    # Hero Banner with Branding
    st.markdown(f"""
    <div style='text-align:center; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                padding: 3rem; border-radius: 20px; color: white; margin-bottom: 2rem;'>
        <img src='{LOGO_URL}' style='width: 120px; margin-bottom: 0.5rem;' alt='CarryMe.store'>
        <h1 style='font-size: 3rem; margin: 0;'>{BRAND_NAME}</h1>
        <p style='font-size: 2rem; font-weight: 300; margin: 0;'>{TAGLINE}</p>
        <p style='font-size: 1.2rem; letter-spacing: 4px; opacity: 0.9;'>{SUBTITLE}</p>
    </div>
    """, unsafe_allow_html=True)

    # Founder Section
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

    # Bundle Offer
    st.markdown("## 🎁 Special Bundle Offer")
    st.markdown(f"**Buy Premium Rose Table Cover + Cotton Towel together and save ₹50!**")
    st.markdown(f"**Bundle Price: ₹{BUNDLE_PRICE}** (instead of ₹{449+99})")
    if st.button("🛒 Add Bundle to Cart", use_container_width=True):
        for pid in BUNDLE_PRODUCTS:
            add_to_cart(pid, quantity=1, replace_cart=False)
        st.toast("✅ Bundle added to cart! You saved ₹50.", icon="🎁")
        st.rerun()
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

    # Testimonials
    st.markdown("## 💬 What Our Customers Say")
    test_cols = st.columns(len(TESTIMONIALS))
    for i, test in enumerate(TESTIMONIALS):
        with test_cols[i]:
            st.markdown(f"*“{test['text']}”*")
            st.caption(f"— {test['name']}")
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
    featured_ids = [2, 8, 9, 11]
    featured_products = [products[pid] for pid in featured_ids]
    st.markdown("## 🔥 Featured Products")
    cols = st.columns(4)
    for idx, prod in enumerate(featured_products):
        with cols[idx]:
            display_product_card(prod, key_prefix="featured")

    # WhatsApp CTA + Broadcast
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

        # Loyalty points (if logged in)
        if st.session_state.user:
            st.markdown(f"⭐ You have **{st.session_state.points}** points. Redeem 100 points for ₹50 off!")
            if st.session_state.points >= 100:
                if st.button("🔄 Redeem 100 points for ₹50 off"):
                    st.session_state.points -= 100
                    total -= 50
                    save_user_data()
                    st.success("Points redeemed! ₹50 discount applied.")
                    st.rerun()

        # Recommendations
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
            # Save order to Firestore if logged in
            if st.session_state.user:
                order_data = {
                    "items": cart_items,
                    "total": total,
                    "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "order_id": int(time.time())
                }
                user_ref = db.collection("users").document(st.session_state.user["uid"])
                user_ref.update({
                    "orders": firestore.ArrayUnion([order_data])
                })
                # Award points (1 point per ₹10 spent)
                earned_points = int(total // 10)
                st.session_state.points += earned_points
                save_user_data()
                st.success(f"🎉 You earned {earned_points} points for this order!")

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
            if st.session_state.user:
                save_user_data()
            st.rerun()

    render_footer()

# ---------- PAGE: ORDERS ----------
elif st.session_state.active_page == "📦 Orders":
    st.markdown("# 📦 Order History")
    if not st.session_state.user:
        st.warning("Please log in to view your order history.")
        return
    uid = st.session_state.user["uid"]
    doc = db.collection("users").document(uid).get()
    if doc.exists:
        orders = doc.to_dict().get("orders", [])
        if not orders:
            st.info("No orders yet. Start shopping!")
        else:
            for order in reversed(orders):
                st.markdown(f"**Order #{order['order_id']}** – {order['date']}")
                st.markdown(f"**Total:** ₹{order['total']}")
                for item in order['items']:
                    st.write(f"- {item['name']} x {item['quantity']} = ₹{item['subtotal']}")
                st.markdown("---")
    else:
        st.info("No orders found.")

    render_footer()

# ---------- PAGE: WISHLIST ----------
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

# ---------- PAGE: ADMIN ----------
elif st.session_state.active_page == "📊 Admin":
    st.markdown("# 📊 Admin Dashboard")
    if not st.session_state.user:
        st.warning("Please log in as admin.")
        return
    if st.session_state.user.get("email") != "admin@carryme.store":
        st.error("Unauthorized access.")
        return

    # Fetch stats
    users_ref = db.collection("users")
    users = users_ref.stream()
    total_revenue = 0
    total_orders = 0
    top_products = {}

    for user_doc in users:
        data = user_doc.to_dict()
        orders = data.get("orders", [])
        total_orders += len(orders)
        for order in orders:
            total_revenue += order.get("total", 0)
            for item in order.get("items", []):
                prod_name = item["name"]
                top_products[prod_name] = top_products.get(prod_name, 0) + item["quantity"]

    st.metric("Total Orders", total_orders)
    st.metric("Total Revenue", f"₹{total_revenue}")

    st.markdown("### Top Selling Products")
    if top_products:
        sorted_products = sorted(top_products.items(), key=lambda x: x[1], reverse=True)
        for name, qty in sorted_products[:5]:
            st.write(f"- {name}: {qty} units")
    else:
        st.write("No sales data yet.")

    st.markdown("### Recent Users")
    if FIREBASE_AVAILABLE:
        users = users_ref.order_by("created_at", direction=firestore.Query.DESCENDING).limit(5).get()
        for user in users:
            st.write(f"- {user.to_dict().get('email')} (points: {user.to_dict().get('points', 0)})")
    else:
        st.write("Firebase not available.")

    render_footer()

# ---------- FALLBACK ----------
else:
    st.error("Page not found.")
    st.session_state.active_page = "🏠 Home"
    st.rerun()
