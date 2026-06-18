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

# Asset URLs (adjust paths if needed)
LOGO_URL = "https://raw.githubusercontent.com/iefuture108-afk/carryme/main/assets/logo.png"
FOUNDER_IMG_URL = "https://raw.githubusercontent.com/iefuture108-afk/carryme/main/assets/founder.jpg"
# Fallback if images not available
if not requests.head(LOGO_URL).ok:
    LOGO_URL = "https://picsum.photos/200/80?random=1"
if not requests.head(FOUNDER_IMG_URL).ok:
    FOUNDER_IMG_URL = "https://picsum.photos/300/300?random=2"

# ---------- FIREBASE INIT (with fallback) ----------
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
    st.warning(f"Firebase not configured. Running in guest mode (local storage only). Error: {e}")
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
        # Create user document
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

# ---------- PRODUCT CATALOG (16 products – same as before) ----------
# (Omitted for brevity – same as previous version, will include in final)

# ... (Keep all product definitions, helper functions, display_product_card, etc. from the previous v2.0)

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
        st.sidebar.write(f"🔗 Your referral code: {st.session_state.referral_code}")
        share_link = f"https://carryme.store?ref={st.session_state.referral_code}"
        st.sidebar.markdown(f"Share your link: [Copy]({share_link})")
    if st.sidebar.button("Logout"):
        sign_out()

# Navigation
cart_count = sum(item["quantity"] for item in st.session_state.cart)
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
    st.markdown("""
    <script>
    function saveToLocalStorage(key, data) {
        localStorage.setItem(key, JSON.stringify(data));
    }
    (function() {
        const urlParams = new URLSearchParams(window.location.search);
        let needsRedirect = false;
        if (!urlParams.has('cart')) {
            const cartData = localStorage.getItem('cart');
            if (cartData) {
                urlParams.set('cart', cartData);
                needsRedirect = true;
            }
        }
        if (!urlParams.has('wishlist')) {
            const wishData = localStorage.getItem('wishlist');
            if (wishData) {
                urlParams.set('wishlist', wishData);
                needsRedirect = true;
            }
        }
        if (needsRedirect) {
            const newUrl = window.location.pathname + '?' + urlParams.toString();
            window.location.replace(newUrl);
        }
    })();
    window.cartData = """ + json.dumps(st.session_state.cart) + """;
    window.wishlistData = """ + json.dumps(st.session_state.wishlist) + """;
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

# ---------- FALLBACK ----------
else:
    st.error("Page not found.")
    st.session_state.active_page = "🏠 Home"
    st.rerun()
    "'
