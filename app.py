import streamlit as st
import time

st.set_page_config(page_title="CarryMe Store", page_icon="🛍️", layout="wide")

# Session State
if 'user' not in st.session_state:
    st.session_state.user = None
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'discount_used' not in st.session_state:
    st.session_state.discount_used = 0

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #FF6B6B; text-align: center; }
    .product-card { border: 1px solid #ddd; padding: 10px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Sidebar (Always Visible)
with st.sidebar:
    st.image("https://raw.githubusercontent.com/iefuture108-afk/carryme/main/images/IMG-20260608-WA0009.jpg", width=200)
    st.title("CarryMe Store")
    
    # Login
    if not st.session_state.user:
        with st.expander("🔑 Login / Register", expanded=True):
            name = st.text_input("Full Name")
            mobile = st.text_input("Mobile Number", max_chars=10)
            pincode = st.text_input("Delivery Pincode", max_chars=6)
            if st.button("Login"):
                if mobile and len(mobile) >= 10 and pincode:
                    st.session_state.user = {"name": name or "Customer", "mobile": mobile, "pincode": pincode}
                    st.success("Login Successful! 🎉")
                    st.rerun()
    else:
        st.success(f"👤 {st.session_state.user['name']}")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

    page = st.selectbox("Menu", ["🏠 Home", "🛍️ Shop", "✨ AI Generator", "🛒 Cart", "📞 Contact"])

# Products Data
products = [
    {"id":1, "name":"Premium Cotton Hand & Face Towel Set", "category":"Towels", "price":449, "image":"https://raw.githubusercontent.com/iefuture108-afk/carryme/main/images/IMG-20260608-WA0016.jpg", "desc":"Ultra soft cotton towels."},
    # Add more products here...
]

# Pages
if page == "🏠 Home":
    st.title("Welcome to CarryMe Store")
    st.subheader("India's Premium D2C Custom Home Decor Brand")
    # Your existing homepage content here

elif page == "🛍️ Shop":
    st.title("🛍️ Shop")
    search = st.text_input("Search products...")
    # Filtering logic here...

elif page == "✨ AI Generator":
    st.title("✨ AI Product Description & Quick Order")
    selected_product = st.selectbox("Select Product", [p["name"] for p in products])
    
    tone = st.selectbox("Tone", ["Luxury", "Simple", "Promotional"])
    if st.button("Generate Description & Order Link"):
        with st.spinner("Generating..."):
            time.sleep(1)
            st.success("Description Generated!")
            st.write("**Quick Order Message:**")
            st.code(f"Hi, I want to order {selected_product} from CarryMe Store. Please confirm price & delivery to {st.session_state.user['pincode'] if st.session_state.user else 'my pincode'}.")
    
    if st.button("📱 Order on WhatsApp Now"):
        st.markdown(f"[Open WhatsApp](https://wa.me/919250036334?text=Hi%20I%20want%20to%20buy%20{selected_product.replace(' ', '%20')})")

elif page == "🛒 Cart":
    st.title("Your Cart")
    # Cart logic...

# Footer
st.divider()
st.markdown("© 2026 CarryMe Store | [WhatsApp](https://wa.me/919250036334) | [Instagram](https://www.instagram.com/carryme_stores)")
