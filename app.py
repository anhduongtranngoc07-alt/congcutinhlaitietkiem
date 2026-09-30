import streamlit as st
st.image("logo.jpg")
# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Ứng dụng tính lãi tiền gửi",
    page_icon="💰",
    layout="wide"
)

st.title("💰 ỨNG DỤNG TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.caption("Tính toán theo phương pháp lãi đơn và lãi kép")


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_money(value):
    """Định dạng số tiền theo VNĐ."""
    value = Decimal(str(value)).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    )
    return f"{value:,.0f} VNĐ"


# =========================================================
# NHẬP DỮ LIỆU
# =========================================================

st.sidebar.header("⚙️ Thông tin tiền gửi")

so_tien_gui = st.sidebar.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=200_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.sidebar.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=3,
    step=1
)

loai_lai = st.sidebar.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh = st.sidebar.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

lai_suat_nam = st.sidebar.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1
)

# Nút tính
tinh_toan = st.sidebar.button(
    "🧮 TÍNH LÃI",
    use_container_width=True
)


# =========================================================
# TÍNH TOÁN
# =========================================================

if tinh_toan:

    if so_tien_gui <= 0:
        st.error("❌ Số tiền gửi phải lớn hơn 0.")
        st.stop()

    if lai_suat_nam < 0:
        st.error("❌ Lãi suất không hợp lệ.")
        st.stop()

    P = Decimal(str(so_tien_gui))
    r_nam = Decimal(str(lai_suat_nam)) / Decimal("100")

    # -----------------------------------------------------
    # Xác định số kỳ và lãi suất mỗi kỳ
    # -----------------------------------------------------

    if hinh_thuc_lanh == "Lãnh lãi theo tháng":
        so_ky = int(ky_han)
        so_thang_moi_ky = 1

    elif hinh_thuc_lanh == "Lãnh lãi theo quý":
        # Nếu kỳ hạn không chia hết cho 3,
        # phần thời gian còn lại vẫn được tính theo tháng.
        so_ky = (int(ky_han) + 2) // 3
        so_thang_moi_ky = 3

    else:
        # Cuối kỳ: tính chi tiết theo tháng,
        # nhưng chỉ thanh toán một lần ở cuối kỳ.
        so_ky = int(ky_han)
        so_thang_moi_ky = 1

    # =====================================================
    # LÃI ĐƠN
    # =====================================================

    if loai_lai == "Lãi đơn":

        # Lãi suất theo tháng
        r_thang = r_nam / Decimal("12")

        lai_moi_thang = P * r_thang

        # Tổng lãi toàn bộ kỳ hạn
        tong_lai = P * r_nam * Decimal(str(ky_han)) / Decimal("12")

        tong_tien = P + tong_lai

        # -------------------------------------------------
        # Tạo bảng chi tiết
        # -------------------------------------------------

        data = []

        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            for i in range(1, int(ky_han) + 1):

                lai_ky = lai_moi_thang

                data.append({
                    "Kỳ": i,
                    "Thời gian
