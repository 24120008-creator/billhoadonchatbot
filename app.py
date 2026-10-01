import streamlit as st
from datetime import datetime
from io import BytesIO


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Bill Trà Sữa",
    page_icon="🧋",
    layout="centered"
)


# =========================================================
# DỮ LIỆU MENU
# Bạn có thể thay đổi tên và giá ở đây
# =========================================================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa bạc hà": 35000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Trà tắc": 25000,
}

TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Thạch dừa": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
}


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_money(number):
    return f"{number:,.0f} VNĐ".replace(",", ".")


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.title("🧋 QUÁN TRÀ SỮA")
st.subheader("Hệ thống tính bill & xuất hóa đơn")


st.divider()


# =========================================================
# THÔNG TIN KHÁCH HÀNG
# =========================================================

st.header("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)


# =========================================================
# CHỌN TRÀ SỮA
# =========================================================

st.header("🧋 Chọn đồ uống")

drink = st.selectbox(
    "Loại trà sữa / đồ uống",
    list(MENU.keys())
)

drink_price = MENU[drink]

st.write(
    f"💰 Giá: **{format_money(drink_price)}**"
)


# =========================================================
# SỐ LƯỢNG
# =========================================================

quantity = st.number_input(
    "Số lượng",
    min_value=1,
    max_value=50,
    value=1,
    step=1
)


# =========================================================
# MỨC ĐỘ ĐƯỜNG
# =========================================================

st.header("🍬 Mức độ đường")

sugar = st.radio(
    "Chọn mức đường",
    ["100%", "70%", "0%"],
    horizontal=True
)


# =========================================================
# MỨC ĐỘ ĐÁ
# =========================================================

st.header("🧊 Mức độ đá")

ice = st.radio(
    "Chọn mức đá",
    ["100%", "70%", "0%"],
    horizontal=True
)


# =========================================================
# TOPPING
# =========================================================

st.header("🍡 Topping")

selected_toppings = st.multiselect(
    "Chọn topping",
    list(TOPPINGS.keys())
)


# =========================================================
# TÍNH TIỀN
# =========================================================

topping_total = sum(
    TOPPINGS[topping]
    for topping in selected_toppings
)

price_per_cup = drink_price + topping_total

total = price_per_cup * quantity


# =========================================================
# HIỂN THỊ KẾT QUẢ ĐÃ NHẬP
# =========================================================

st.divider()

st.header("🧾 Thông tin đơn hàng")

if customer_name.strip() == "":
    display_name = "Khách hàng chưa nhập tên"
else:
    display_name = customer_name


st.info(
    f"""
**Khách hàng:** {display_name}

**Đồ uống:** {drink}

**Số lượng:** {quantity}

**Đường:** {sugar}

**Đá:** {ice}
"""
)


# =========================================================
# HIỂN THỊ TOPPING
# =========================================================

if selected_toppings:
    st.write("**🍡 Topping:**")

    for topping in selected_toppings:
        st.write(
            f"- {topping}: {format_money(TOPPINGS[topping])}"
        )
else:
    st.write("**🍡 Topping:** Không có")


# =========================================================
# BẢNG CHI TIẾT
# =========================================================

st.subheader("💵 Chi tiết thanh toán")

col1, col2 = st.columns(2)

with col1:
    st.write("Giá đồ uống:")
    st.write("Topping:")
    st.write("Số lượng:")
    st.write("**TỔNG THANH TOÁN:**")

with col2:
    st.write(format_money(drink_price))
    st.write(format_money(topping_total))
    st.write(quantity)
    st.success(format_money(total))


# =========================================================
# NỘI DUNG HÓA ĐƠN
# =========================================================

now = datetime.now()

invoice_number = now.strftime("%Y%m%d%H%M%S")

invoice_text = f"""
========================================
             QUÁN TRÀ SỮA
              HÓA ĐƠN
========================================

Mã hóa đơn: {invoice_number}
Thời gian: {now.strftime("%d/%m/%Y %H:%M:%S")}

Khách hàng: {display_name}

----------------------------------------
THÔNG TIN ĐƠN HÀNG
----------------------------------------

Đồ uống:
{drink}

Đơn giá:
{format_money(drink_price)}

Số lượng:
{quantity}

Mức đường:
{sugar}

Mức đá:
{ice}

Topping:
"""

if selected_toppings:
    for topping in selected_toppings:
        invoice_text += (
            f"- {topping}: {format_money(TOPPINGS[topping])}\n"
        )
else:
    invoice_text += "Không có\n"


invoice_text += f"""
----------------------------------------
TẠM TÍNH
----------------------------------------

Giá đồ uống:
{format_money(drink_price)}

Tổng tiền topping:
{format_money(topping_total)}

Tổng tiền / ly:
{format_money(price_per_cup)}

Số lượng:
{quantity}

========================================
TỔNG THANH TOÁN:
{format_money(total)}
========================================

       CẢM ƠN QUÝ KHÁCH!
          HẸN GẶP LẠI
========================================
"""


# =========================================================
# NÚT THANH TOÁN
# =========================================================

st.divider()

st.header("💳 Thanh toán")

if st.button(
    "💰 THANH TOÁN & XUẤT HÓA ĐƠN",
    use_container_width=True
):

    if customer_name.strip() == "":
        st.warning("⚠️ Vui lòng nhập tên khách hàng trước khi thanh toán.")

    else:
        st.success(
            f"✅ Thanh toán thành công! Tổng tiền: {format_money(total)}"
        )

        st.download_button(
            label="📄 TẢI HÓA ĐƠN",
            data=invoice_text.encode("utf-8"),
            file_name=f"hoa_don_{invoice_number}.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.write("### 🧾 Hóa đơn")

        st.code(
            invoice_text,
            language="text"
        )
