import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Sử dụng trực tiếp chìa khóa API của bạn
api_key = "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"
client = OpenAI(api_key=api_key)

# Thiết lập màn hình rộng (Bắt buộc để chia 2 cột)
st.set_page_config(page_title="AI Content Machine cho Seller Việt", page_icon="🚀", layout="wide")

# Khởi tạo kho lưu trữ tạm thời nếu chưa có
if "content_history" not in st.session_state:
    st.session_state.content_history = []

st.title("🚀 AI Content Machine")
st.subheader("1-Click Tạo Lịch Content & Bài Viết Chốt Đơn (Bản Nâng Cấp Có Kho Lưu)")
st.markdown("---")

# Chia đôi màn hình thành 2 cột rõ ràng
col1, col2 = st.columns([1.2, 1])

with col1:
    with st.form("content_form"):
        st.markdown("### 📝 Điền thông tin sản phẩm của bạn")
        product_name = st.text_input("Tên sản phẩm/dịch vụ:", placeholder="Ví dụ: Lót Giày Hương Quế, Mỳ chay nhà làm...")
        industry = st.selectbox("Ngành hàng dọc (Vertical):", ["Thực phẩm/F&B nhà làm", "Mỹ phẩm/Làm đẹp", "Thời trang/Váy vóc", "Dịch vụ Spa/Thẩm mỹ", "Khác..."])
        key_features = st.text_area("Điểm nổi bật nhất (Sợi mì dai, hương quế tự nhiên khử mùi...):", placeholder="Nhập các ý chính thô sơ...")
        promotion = st.text_input("Chương trình ưu đãi (Nếu có):", placeholder="Ví dụ: Mua 2 tặng 1...")
        target_output = st.radio("Bạn muốn AI tạo ra loại content nào?", ["Kịch bản Video ngắn", "Bài viết bán hàng Facebook/Zalo"], horizontal=True)
        submit_button = st.form_submit_button(label="⚡ Bắt đầu tạo Content")

SYSTEM_PROMPT = "Bạn là một chuyên gia Content Marketing thực chiến cao cấp tại Việt Nam. Nhiệm vụ của bạn là nhận thông tin sản phẩm thô từ người dùng và chuyển đổi nó thành nội dung có tính chuyển đổi cao. Ngôn ngữ tiếng Việt tự nhiên, có tiêu đề giật gân, chia bài viết rõ ràng kèm icon trực quan và kết thúc bằng CTA kêu gọi mua hàng."
USER_PROMPT_TEMPLATE = "Tạo nội dung bán hàng cho sản phẩm: {name}, Ngành: {industry}, Tính năng: {features}, Ưu đãi: {promo}, Định dạng: {output}"

if submit_button:
    if not product_name or not key_features:
        st.warning("⚠️ Vui lòng điền đầy đủ Tên sản phẩm và Tính năng nổi bật!")
    else:
        with st.spinner("🤖 AI đang rặn chữ chuẩn văn phong chốt đơn..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": USER_PROMPT_TEMPLATE.format(name=product_name, industry=industry, features=key_features, promo=promotion if promotion else "Không có", output=target_output)}
                    ],
                    temperature=0.7
                )
                result = response.choices[0].message.content
                # Ghi bài viết mới vào đầu kho lưu trữ
                st.session_state.content_history.insert(0, {"product": product_name, "type": target_output, "content": result})
            except Exception as e:
                st.error(f"❌ Có lỗi xảy ra: {str(e)}")

# HIỂN THỊ KHO LƯU TRỮ CHẮC CHẮN Ở CỘT BÊN PHẢI
with col2:
    st.markdown("### 🗄️ Kho lưu trữ bài viết (Tự động lưu)")
    if not st.session_state.content_history:
        st.info("Chưa có bài viết nào được tạo trong phiên này. Hãy điền form bên trái để kích hoạt kho lưu trữ!")
    else:
        st.markdown("#### 🌟 Bài viết vừa tạo mới nhất:")
        latest_item = st.session_state.content_history[0]
        st.success(f"Sản phẩm: {latest_item['product']} ({latest_item['type']})")
        st.markdown(latest_item['content'])
        st.markdown("---")
        
        if len(st.session_state.content_history) > 1:
            st.markdown("#### 📜 Các bài viết đã lưu trước đó:")
            for idx, item in enumerate(st.session_state.content_history[1:]):
                with st.expander(f"Bài cũ {idx+1}: {item['product']} ({item['type']})"):
                    st.markdown(item['content'])

st.markdown("---")
st.markdown("<center>💡 <i>Tham gia <b>Cộng đồng tự làm Content bằng AI</b> để nhận thêm nhiều mẹo và prompt độc quyền!</i></center>", unsafe_allow_html=True)