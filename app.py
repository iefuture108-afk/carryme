import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="CarryMe Store - India's Premium Custom Home Decor",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {font-size: 3.5rem; color: #FF6B6B; text-align: center; margin-bottom: 10px;}
    .product-card {border: 1px solid #eee; border-radius: 16px; padding: 15px; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.08);}
    .stButton>button {width: 100%; border-radius: 10px; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'cart' not in st.session_state: st.session_state.cart = []
if 'custom_requests' not in st.session_state: st.session_state.custom_requests = []

products = [
    {"id": 1, "name": "Handcrafted Terracotta Beaded Necklace", "category": "Jewelry", "price": 599, "rating": 4.8,
     "description": "Premium ethnic terracotta jewelry.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0011.jpg"},
    {"id": 3, "name": "Waterproof PVC Table Cover", "category": "Table Covers", "price": 299, "rating": 4.6,
     "description": "Elegant & durable PVC table cover.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0012.jpg"},
    {"id": 4, "name": "Luxury Quilted Sofa Cover", "category": "Sofa Covers", "price": 1299, "rating": 4.9,
     "description": "Premium sofa protector with lace.", 
     "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/ba13288c6a2841298ba356abea281818e3e8ccbc/images/Sofa%20cover.png"},
]

wa_number = "919250036334"
ig_url = "https://www.instagram.com/carryme_stores"

st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("**India's Premium Custom Home Decor**")
st.sidebar.markdown(f"[💬 WhatsApp](https://wa.me/{wa_number})", unsafe_allow_html=True)
st.sidebar.markdown(f"[📸 Instagram]({ig_url})", unsafe_allow_html=True)

page = st.sidebar.selectbox("Menu", ["🏠 Home", "🛍️ Shop", "✨ Customize", "🛒 Cart", "📞 Contact"])

if page == "🏠 Home":
    st.image("https://raw.githubusercontent.com/iefuture108-afk/carryme/3b5a5dc3cf6ba73e16c43eb91bb8705035316e79/images/IMG-20260608-WA0009.jpg", use_column_width=True)
    st.markdown('<h1 class="main-header">CarryMe Store</h1>', unsafe_allow_html=True)
    st.markdown("### 🌿 India’s First D2C Custom Home Decor Brand")
    st.caption("Made in India • Customized for You")

    st.divider()
    st.subheader("Featured Products")
    cols = st.columns(3)
    for idx, p in enumerate(products):
        with cols[idx]:
            st.image(p["image"], use_column_width=True)
            st.subheader(p["name"])
            st.write(f"**₹{p['price']}**")
            if st.button("Add to Cart", key=f"feat_{p['id']}"):
                st.session_state.cart.append({**p, "qty": 1})
                st.success("Added!")

elif page == "🛍️ Shop":
    st.title("🛍️ Shop Collection")
    # Existing shop code (tabs + search) can be added here

elif page == "✨ Customize":
    st.title("✨ Custom Product Request")
    st.write("Tell us what you want. We'll make it for you!")
    
    with st.form("custom_form"):
        name = st.text_input("Your Name")
        phone = st.text_input("WhatsApp Number", value="9")
        product_type = st.selectbox("Product Type", ["PVC Table Cover", "Sofa Cover", "Terracotta Jewelry", "Towel Set", "Other"])
        description = st.text_area("Describe your custom requirement (color, size, design, personalization, etc.)")
        budget = st.selectbox("Budget Range", ["₹200-500", "₹500-1000", "₹1000-2000", "Above ₹2000"])
        
        submitted = st.form_submit_button("Send Custom Request on WhatsApp", type="primary")
        
        if submitted:
            if name and phone and description:
                msg = f"""*Custom Order Request - CarryMe Store*

Name: {name}
Phone: {phone}
Product: {product_type}
Budget: {budget}

Requirements:
{description}

Please help me create this custom product. Thank you!"""
                
                wa_url = f"https://wa.me/{wa_number}?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
                st.markdown(f"[📱 Send Custom Request on WhatsApp]({wa_url})", unsafe_allow_html=True)
                st.success("Request ready! Click the link above.")
            else:
                st.error("Please fill required fields")

elif page == "🛒 Cart":
    st.title("🛒 Your Cart")
    # Your existing cart code here

elif page == "📞 Contact":
    st.title("📞 Contact Us")
    st.markdown(f"[💬 WhatsApp Chat](https://wa.me/{wa_number})")
    st.markdown(f"[📸 Instagram]({ig_url})")

st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    © 2026 CarryMe Store • India's D2C Custom Home Decor Brand<br>
    <b>Handcrafted • Customized • Delivered with Love</b>
</div>
""", unsafe_allow_html=True)
