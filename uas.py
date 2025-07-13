import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(page_title="Optimasi Minuman", layout="centered")
st.title("Simulasi Optimasi Produksi Minuman Kemasan")
st.markdown("Gunakan aplikasi ini untuk menentukan jumlah optimal produksi **Teh Botol** dan **Jus Buah** agar keuntungan maksimal dengan keterbatasan bahan.")

st.header("🧃 Parameter Produk")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Teh Botol")
    profit_tea = st.number_input("Keuntungan per botol (Rp)", value=3000, min_value=0)
    air_tea = st.number_input("Kebutuhan Air (ml)", value=500)
    gula_tea = st.number_input("Kebutuhan Gula (gr)", value=50)
    tenaga_tea = st.number_input("Tenaga Kerja (menit)", value=10)

with col2:
    st.subheader("Jus Buah")
    profit_juice = st.number_input("Keuntungan per botol (Rp)", value=5000, min_value=0)
    air_juice = st.number_input("Kebutuhan Air (ml)", value=400)
    gula_juice = st.number_input("Kebutuhan Gula (gr)", value=70)
    tenaga_juice = st.number_input("Tenaga Kerja (menit)", value=12)

st.header("📦 Ketersediaan Bahan Baku")
water_limit = st.slider("Total Air Tersedia (ml)", 1000, 50000, 20000)
sugar_limit = st.slider("Total Gula Tersedia (gr)", 500, 10000, 4000)
labor_limit = st.slider("Total Tenaga Kerja (menit)", 60, 5000, 1000)

if st.button("🔍 Jalankan Optimasi"):
    # Fungsi tujuan (maksimalkan keuntungan)
    c = [-profit_tea, -profit_juice]

    A = [
        [air_tea, air_juice],
        [gula_tea, gula_juice],
        [tenaga_tea, tenaga_juice]
    ]
    b = [water_limit, sugar_limit, labor_limit]

    bounds = [(0, None), (0, None)]

    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    st.subheader("📊 Hasil Perhitungan")

    if res.success:
        tea_qty = res.x[0]
        juice_qty = res.x[1]
        profit = -res.fun

        st.success("Solusi optimal ditemukan!")
        st.write(f"- Produksi Teh Botol: **{tea_qty:.2f} botol**")
        st.write(f"- Produksi Jus Buah: **{juice_qty:.2f} botol**")
        st.write(f"- Keuntungan Maksimal: **Rp {profit:,.2f}**")

        # Visualisasi batasan
        fig, ax = plt.subplots(figsize=(8, 6))
        x = np.linspace(0, max(tea_qty, juice_qty) + 20, 300)

        # Gambar garis batas
        if air_juice != 0:
            ax.plot(x, (water_limit - air_tea * x) / air_juice, label="Batas Air")
        if gula_juice != 0:
            ax.plot(x, (sugar_limit - gula_tea * x) / gula_juice, label="Batas Gula")
        if tenaga_juice != 0:
            ax.plot(x, (labor_limit - tenaga_tea * x) / tenaga_juice, label="Batas Tenaga")

        # Titik optimal
        ax.plot(tea_qty, juice_qty, 'ro', label="Solusi Optimal")
        ax.set_xlabel("Teh Botol (unit)")
        ax.set_ylabel("Jus Buah (unit)")
        ax.set_title("Batasan Produksi dan Titik Optimal")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Gagal menemukan solusi. Coba ubah nilai input atau batas sumber daya.")
