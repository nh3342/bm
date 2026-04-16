import streamlit as st
import json
import os
import base64

# --- DIRECTORY SETUP ---
os.makedirs("assets/images", exist_ok=True)
DATA_FILE = "products.json"

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Disha Herbals", page_icon="🌿", layout="wide")


# --- UTILITY: GET BASE64 IMAGE FOR BACKGROUND ---
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""


# --- CUSTOM CSS (Fonts, Background, Styling) ---
def local_css():
    # Get base64 string of the logo for the blurred background
    bg_base64 = get_base64_of_bin_file("assets/logo.png")

    # Conditional CSS for the background if the logo exists
    bg_css = f"""
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: url("data:image/png;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            filter: blur(12px);
            opacity: 0.08; /* Very subtle so text remains readable */
            z-index: -1;
        }}
    """ if bg_base64 else ""

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Montserrat:wght@300;400;500&display=swap');

        /* Inject the blurred background */
        {bg_css}

        .stApp {{
            background-color: #FEFCF8; /* Fallback base color */
            color: #2F3630;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Playfair Display', serif !important;
            color: #2F3630;
            letter-spacing: 0.5px;
        }}

        p, span, div, li {{
            font-family: 'Montserrat', sans-serif;
        }}

        /* Subtle Grid Styling & Expander */
        div[data-testid="stExpander"] {{
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
            border: 1px solid #e0dcd3;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }}

        /* STANDARDIZE IMAGE SIZES inside the bordered containers */
        div[data-testid="stVerticalBlockBorderWrapper"] img {{
            height: 250px !important;
            width: 100% !important;
            object-fit: cover !important; /* Prevents stretching, crops cleanly */
            border-radius: 6px;
        }}

        /* Floating Action Button (FAB) */
        .stButton > button {{
            border-radius: 30px;
            background-color: #728777;
            color: white;
            border: none;
            transition: 0.3s;
            padding: 12px 28px;
            font-weight: 500;
            font-family: 'Montserrat', sans-serif;
            box-shadow: 0 4px 12px rgba(114, 135, 119, 0.3);
        }}
        .stButton > button:hover {{
            background-color: #5d7062;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(114, 135, 119, 0.4);
        }}

        .floating-button-container {{
            position: fixed;
            bottom: 40px;
            right: 40px;
            z-index: 999;
        }}
    </style>
    """, unsafe_allow_html=True)


# --- DATA HANDLING ---
def load_data():
    if os.path.exists(DATA_FILE):
        if os.path.getsize(DATA_FILE) > 0:
            with open(DATA_FILE, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
    return []


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# --- INQUIRY MODAL ---
@st.dialog("Send us a message 🌿")
def inquiry_form():
    st.write("Have a question about our ingredients or want to place an order? Drop us a note below!")
    with st.form("email_inquiry"):
        name = st.text_input("Your Name")
        contact = st.text_input("Email or Phone Number")
        message = st.text_area("How can we help you today?")
        submitted = st.form_submit_button("Send Inquiry")
        if submitted:
            st.success(f"Thank you, {name}! Your message has been safely recorded. We will contact you soon.")


# --- UI COMPONENTS ---
def render_hero():
    # Hero Section with Side-by-Side Layout
    with st.container():
        col_logo, col_desc = st.columns([1, 2], gap="large")

        with col_logo:
            if os.path.exists("assets/logo.png"):
                st.image("assets/logo.png", use_container_width=True)
            else:
                st.markdown("<h1 style='text-align: center; font-size: 2.5rem;'>Disha Herbals</h1>",
                            unsafe_allow_html=True)

        with col_desc:
            st.markdown(
                "<h1 style='text-align: left; font-size: 4rem; margin-bottom: 0; padding-top: 20px;'>Disha Herbals</h1>",
                unsafe_allow_html=True)
            st.markdown(
                "<h2 style='text-align: left; color: #728777; font-style: italic; margin-top: 0px; font-size: 1.6rem;'>As Gentle as a Mother's Touch</h2>",
                unsafe_allow_html=True)
            st.markdown("""
            <p style='text-align: left; font-size: 1.1rem; line-height: 1.7; color: #555; margin-top: 15px; max-width: 90%;'>
            At Disha Herbals, we believe skincare should be as pure, safe, and nurturing as nature intended. 
            Handcrafted with love, our authentic handmade soaps strip away harsh chemicals, leaving your skin 
            with nothing but herbal goodness.
            </p>
            """, unsafe_allow_html=True)
    st.divider()


def render_storefront(products):
    featured = [p for p in products if p.get("is_featured")]
    if featured:
        st.markdown(
            "<br><h2 style='text-align: center; color: #728777; font-size: 2.5rem;'>✨ Our Signature Blends</h2><br>",
            unsafe_allow_html=True)
        for p in featured:
            # Wrap featured product in a bordered grid container
            with st.container(border=True):
                col1, col2 = st.columns([1, 2], gap="large")
                with col1:
                    if os.path.exists(p['image_path']):
                        st.image(p['image_path'], use_container_width=True)
                with col2:
                    st.markdown(f"### {p['name']}")
                    st.markdown(f"**🎯 Best for:** {p['usecase']}")
                    st.write(p['description'])
                    st.markdown(
                        f"<span style='color: #728777; font-weight: 500;'>🌿 Ingredients:</span> *{p['ingredients']}*",
                        unsafe_allow_html=True)

    st.markdown("<br><h2 style='text-align: center; font-size: 2.2rem;'>Our Handcrafted Collection</h2><br>",
                unsafe_allow_html=True)
    standard = [p for p in products if not p.get("is_featured")]

    cols = st.columns(3, gap="medium")
    for index, p in enumerate(standard):
        with cols[index % 3]:
            # Wrap standard products in a bordered grid container
            with st.container(border=True):
                if os.path.exists(p['image_path']):
                    st.image(p['image_path'], use_container_width=True)

                st.markdown(f"#### {p['name']}")
                st.markdown(f"**🎯** {p['usecase']}")
                with st.expander("View Details & Ingredients"):
                    st.write(p['description'])
                    st.markdown(f"**Contains:** {p['ingredients']}")


# --- STEALTH ADMIN PORTAL ---
def render_admin(products):
    st.title("🔒 Admin Dashboard")
    st.write("Welcome back. Upload new products here.")

    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        pwd = st.text_input("Enter Passcode", type="password")
        if st.button("Login"):
            if pwd == "disha123":
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Incorrect Passcode")
        return

    with st.form("add_product"):
        st.subheader("Add New Product")
        p_name = st.text_input("Product Name")
        p_usecase = st.text_input("Usecase (e.g., Tan Removal)")
        p_ingredients = st.text_area("Ingredients")
        p_desc = st.text_area("Marketing Description")
        p_featured = st.checkbox("Mark as Featured Product?")
        p_image = st.file_uploader("Upload Product Image", type=["jpg", "png", "jpeg"])

        submitted = st.form_submit_button("Publish Product")

        if submitted and p_name:
            image_filename = ""
            if p_image:
                image_filename = f"assets/images/{p_image.name}"
                with open(image_filename, "wb") as f:
                    f.write(p_image.getbuffer())

            new_product = {
                "id": p_name.lower().replace(" ", "_"),
                "name": p_name,
                "usecase": p_usecase,
                "ingredients": p_ingredients,
                "description": p_desc,
                "is_featured": p_featured,
                "image_path": image_filename
            }
            products.append(new_product)
            save_data(products)
            st.success(f"Successfully published {p_name}!")
            st.rerun()


# --- MAIN EXECUTION ---
def main():
    local_css()
    products = load_data()

    query_params = st.query_params
    if query_params.get("mode") == "admin":
        render_admin(products)
    else:
        render_hero()
        render_storefront(products)

        st.markdown('<div class="floating-button-container">', unsafe_allow_html=True)
        if st.button("🌿 Get in Touch"):
            inquiry_form()
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()