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

# Khởi khởi tạo kho lưu trữ tạm thời nếu chưa có
if "content_history" not in st.session_state:
    st.session_state.content_history = []

st.title("🚀 AI Content Machine")
st.subheader("1-Click Tạo Lịch Content & Bài Viết Chốt Đơn (Bản Nâng Cấp Có Kho Lưu)")
st.markdown("---")

# Chia giao diện làm 2 cột: Cột trái nhập liệu - Cột phải hiện kết quả
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Điền thông tin sản phẩm của bạn")
    
    product_name = st.text_input("Tên sản phẩm/dịch vụ:", placeholder="Ví dụ: Lót Giày Hương Quế, Mỳ chay nhà làm...")
    
    category = st.selectbox("Ngành hàng dọc (Vertical):", [
        "Thời trang & Phụ kiện", 
        "Mỹ phẩm & Chăm sóc cá nhân", 
        "Thực phẩm/F&B nhà làm", 
        "Đồ gia dụng & Đời sống",
        "Sản phẩm số / Khóa học"
    ])
    
    usp = st.text_area("Điểm nổi bật nhất (Sợi mì dai, hương quế tự nhiên khử mùi...):")
    promo = st.text_input("Chương trình ưu đãi (Nếu có):", placeholder="Ví dụ: Mua 2 tặng 1...")
    
    content_type = st.radio("Bạn muốn AI tạo ra loại content nào?", ["Kịch bản Video ngắn", "Bài viết bán hàng Facebook/Zalo"])
    
    submit_btn = st.button("⚡ Bắt đầu tạo Content")

with col2:
    st.header("🗄️ Kho lưu trữ bài viết (Tự động lưu)")
    
    if submit_btn:
        if not product_name or not usp:
            st.warning("Vui lòng điền Tên sản phẩm và Điểm nổi bật nhất nhé bạn Nam!")
        else:
            with st.spinner("AI đang vắt óc viết bài chốt đơn cho bạn... Đợi xíu nhé!"):
                try:
                    # Thiết lập lệnh tạo bài cho AI tùy theo loại content
                    if content_type == "Kịch bản Video ngắn":
                        prompt = f"Bạn là chuyên gia sáng tạo kịch bản TikTok triệu view. Hãy viết kịch bản video ngắn (thời lượng 60s) cho sản phẩm '{product_name}' thuộc ngành '{category}'. Điểm nổi bật: {usp}. Ưu đãi: {promo}. Kịch bản phải có cấu trúc: 3 giây đầu giữ chân (Hook), nội dung chính (Body) đánh vào nỗi đau khách hàng, và kêu gọi hành động (CTA) chốt đơn."
                    else:
                        prompt = f"Bạn là một copywriter đỉnh cao chuyên viết bài chốt đơn trên Facebook và Zalo. Hãy viết một bài viết bán hàng cực kỳ thu hút cho sản phẩm '{product_name}' thuộc ngành '{category}'. Điểm nổi bật: {usp}. Ưu đãi: {promo}. Bài viết cần có tiêu đề giật tít, icon bắt mắt, chia bố cục rõ ràng và kêu gọi mua hàng mạnh mẽ."
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Bạn là trợ lý viết content bán hàng bằng tiếng Việt siêu hay, thực chiến, tập trung vào chuyển đổi đơn hàng."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7
                    )
                    
                    generated_text = response.choices[0].message.content
                    
                    # Lưu bài viết mới vào đầu danh sách lịch sử
                    st.session_state.content_history.insert(0, {
                        "product": product_name,
                        "type": content_type,
                        "content": generated_text
                    })
                    
                except Exception as e:
                    st.error(f"Có lỗi xảy ra: {str(e)}")
    
    # Hiển thị toàn bộ các bài viết đã tạo trong kho lưu trữ
    if st.session_state.content_history:
        for idx, item in enumerate(st.session_state.content_history):
            with st.expander(f"📦 Bài {idx+1}: {item['product']} ({item['type']})", expanded=(idx==0)):
                st.write(item['content'])
                st.markdown("---")
    else:
        st.info("Chưa có bài viết nào được tạo trong phiên này. Hãy điền form bên trái để kích hoạt kho lưu trữ!")
