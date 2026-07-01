
# --- ĐOẠN CODE BỔ SUNG ĐỂ TẢI DỮ LIỆU ---
st.write("---")
st.subheader("🛠️ Khu vực dành riêng cho Quản trị viên")

# Tạo ô nhập mật khẩu bí mật
mat_khau = st.text_input("Nhập mật khẩu để quản lý dữ liệu:", type="password")

if mat_khau == "123456":
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, "rb") as file:
            st.download_button(
                label="📥 BẤM VÀO ĐÂY ĐỂ TẢI FILE EXCEL (CSV) VỀ MÁY",
                data=file,
                file_name="du_lieu_tu_nguoi_choi.csv",
                mime="text/csv"
            )
    else:
        st.info("Chưa có người chơi nào bấm chọn nên chưa có dữ liệu.")import streamlit as st
import random
import pandas as pd
import os

st.set_page_config(page_title="Forwarder Dynamic Pricing Game", layout="wide")
st.title("🎮 Game Mô Phỏng Định Giá Động Trong Vận Tải (Dynamic Pricing)")
st.write("Bạn sẽ đóng vai là Chủ hàng (Shipper). Hãy xem xét tình hình nội bộ của hãng vận chuyển, thị trường và môi trường để quyết định có Thuê với mức giá đề xuất không nhé!")
st.write("---")

DATA_FILE = "du_lieu_dinh_gia_dong.csv"

if 'round_data' not in st.session_state:
    tai_trong_trong = random.randint(10, 100) 
    chi_phi_nhien_lieu = random.randint(18000, 25000) 
    nhu_cau_tt = random.choice(["Thấp", "Trung bình", "Rất cao"])
    gia_doi_thu = random.randint(400, 800) 
    tinh_trang_cang = random.choice(["Thông thoáng", "Ùn tắc nhẹ", "Kẹt cảng nghiêm trọng"])
    thoi_tiet = random.choice(["Thuận lợi", "Bão/Mưa lớn"])

    gia_co_ban = 500
    if tai_trong_trong < 30: gia_co_ban += 150 
    if nhu_cau_tt == "Rất cao": gia_co_ban += 200 
    if tinh_trang_cang == "Kẹt cảng nghiêm trọng": gia_co_ban += 100 
    if thoi_tiet == "Bão/Mưa lớn": gia_co_ban += 50
    
    gia_de_xuat = gia_co_ban + random.randint(-50, 50)

    st.session_state.round_data = {
        'tai_trong_trong': tai_trong_trong, 'chi_phi_nhien_lieu': chi_phi_nhien_lieu,
        'nhu_cau_tt': nhu_cau_tt, 'gia_doi_thu': gia_doi_thu,
        'tinh_trang_cang': tinh_trang_cang, 'thoi_tiet': thoi_tiet,
        'gia_de_xuat': gia_de_xuat
    }

r = st.session_state.round_data

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("🏢 1. Biến Nội Bộ Forwarder")
    st.info(f"• Xe trống/Công suất trống: **{r['tai_trong_trong']}%**\n\n• Chi phí nhiên liệu: **{r['chi_phi_nhien_lieu']:,} VND/lít**")
with col2:
    st.subheader("📈 2. Biến Thị Trường")
    st.warning(f"• Nhu cầu thị trường: **{r['nhu_cau_tt']}**\n\n• Giá của đối thủ cạnh tranh: **${r['gia_doi_thu']}**")
with col3:
    st.subheader("🌧️ 3. Biến Môi Trường")
    st.error(f"• Tình trạng cảng biển: **{r['tinh_trang_cang']}**\n\n• Thời tiết: **{r['thoi_tiet']}**")

st.write("---")
st.markdown(f"<h2 style='text-align: center;'>💰 GIÁ CƯỚC ĐỀ XUẤT CHO BẠN: <span style='color:#00cc66'>${r['gia_de_xuat']}</span></h2>", unsafe_allow_html=True)
st.write("---")

def ghi_nhan_quyet_dinh(choice):
    new_row = pd.DataFrame([{
        'TaiTrongTrong': r['tai_trong_trong'], 'ChiPhiNhienLieu': r['chi_phi_nhien_lieu'],
        'NhuCauThiTruong': r['nhu_cau_tt'], 'GiaDoiThu': r['gia_doi_thu'],
        'TinhTrangCang': r['tinh_trang_cang'], 'ThoiTiet': r['thoi_tiet'],
        'GiaDeXuat': r['gia_de_xuat'], 'ChonThue': choice 
    }])
    if not os.path.isfile(DATA_FILE):
        new_row.to_csv(DATA_FILE, index=False)
    else:
        new_row.to_csv(DATA_FILE, mode='a', header=False, index=False)
    del st.session_state.round_data
    st.rerun()

c1, c2 = st.columns(2)
with c1:
    if st.button("👍 ĐỒNG Ý THUÊ (Chấp nhận mức giá)", use_container_width=True, type="primary"):
        ghi_nhan_quyet_dinh(1)
with c2:
    if st.button("👎 TỪ CHỐI (Tìm hãng khác)", use_container_width=True):
        ghi_nhan_quyet_dinh(0)

if os.path.isfile(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.success(f"📈 Số mẫu dữ liệu thu thập được hiện tại: **{len(df)}** dòng.")
