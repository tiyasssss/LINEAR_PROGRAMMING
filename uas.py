import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(page_title="Optimasi Produksi PT. Segar Bahagia", layout="centered")

st.title("🍹 Optimasi Produksi PT. Segar Bahagia")
st.markdown("## Menuju Produksi Efisien dan Maksimal Keuntungan")
st.markdown("Optimalkan produksi **Teh Botol** dan **Jus Buah** dengan batasan air, gula, dan tenaga kerja.")

# Data Produksi per botol
st.header("📦 Parameter Produksi per Botol")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧋 Teh Botol")
    profit_tea = st.number_input("Keuntungan per botol (Rp)", value=3000, min_value=0)
    air_tea = st.number_input("Kebutuhan Air (ml)", value=500)
    gula_tea = st.number_input("Kebutuhan Gula (gr)", value=50)
    tenaga_tea = st.number_input("Kebutuhan Tenaga Kerja (menit)", value=10)

with col2:
    st.subheader("🍓 Jus Buah")
    profit_juice = st.number_input("Keuntungan per botol (Rp)", value=5000, min_value=0)
    air_juice = st.number_input("Kebutuhan Air (ml)", value=400)
    gula_juice = st.number_input("Kebutuhan Gula (gr)", value=70)
    tenaga_juice = st.number_input("Kebutuhan Tenaga Kerja (menit)", value=12)

st.header("🔧 Ketersediaan Sumber Daya per Bulan")
air_max = st.slider("Kapasitas Air (ml)", 5000, 50000, 20000, step=1000)
gula_max = st.slider("Kapasitas Gula (gr)", 1000, 10000, 4000, step=100)
tenaga_max = st.slider("Tenaga Kerja (menit)", 100, 5000, 1000, step=100)

if st.button("🚀 Jalankan Optimasi"):

    # Fungsi Tujuan (dalam bentuk minimisasi)
    c = [-profit_tea, -profit_juice]  # Negatif karena linprog hanya minimisasi

    # Batasan-batasan
    A = [
        [air_tea, air_juice],          # Air constraint
        [gula_tea, gula_juice],        # Gula constraint
        [tenaga_tea, tenaga_juice]     # Tenaga kerja constraint
    ]
    b = [air_max, gula_max, tenaga_max]

    # Batasan variabel (non-negatif)
    bounds = [(0, None), (0, None)]

    # Optimasi
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    st.subheader("📈 Hasil Optimasi")
    if result.success:
        x1 = result.x[0]
        x2 = result.x[1]
        total_profit = -result.fun

        st.success("✅ Solusi optimal ditemukan!")
        st.write(f"**Jumlah Teh Botol (X₁)**: {x1:.2f} botol")
        st.write(f"**Jumlah Jus Buah (X₂)**: {x2:.2f} botol")
        st.write(f"**Total Keuntungan Maksimal**: Rp {total_profit:,.2f}")

        # Visualisasi grafik
        st.subheader("📊 Visualisasi Batasan dan Solusi")

        fig, ax = plt.subplots(figsize=(8, 6))
        x_vals = np.linspace(0, max(x1, x2) + 20, 300)

        # Plot garis batasan
        if air_juice != 0:
            y1 = (air_max - air_tea * x_vals) / air_juice
            ax.plot(x_vals, y1, label="Batas Air")

        if gula_juice != 0:
            y2 = (gula_max - gula_tea * x_vals) / gula_juice
            ax.plot(x_vals, y2, label="Batas Gula")

        if tenaga_juice != 0:
            y3 = (tenaga_max - tenaga_tea * x_vals) / tenaga_juice
            ax.plot(x_vals, y3, label="Batas Tenaga Kerja")

        # Titik solusi optimal
        ax.plot(x1, x2, 'ro', label="Solusi Optimal")
        ax.set_xlabel("Teh Botol (X₁)")
        ax.set_ylabel("Jus Buah (X₂)")
        ax.set_title("Grafik Batasan Produksi")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    else:
        st.error("❌ Gagal menemukan solusi optimal. Silakan cek kembali parameter input.")
