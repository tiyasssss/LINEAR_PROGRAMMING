import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Konfigurasi halaman Streamlit
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
    air_tea = st.number_input("Kebutuhan Air (ml)", value=500, min_value=0)
    gula_tea = st.number_input("Kebutuhan Gula (gr)", value=50, min_value=0)
    tenaga_tea = st.number_input("Kebutuhan Tenaga Kerja (menit)", value=10, min_value=0)

with col2:
    st.subheader("🍓 Jus Buah")
    profit_juice = st.number_input("Keuntungan per botol (Rp)", value=5000, min_value=0)
    air_juice = st.number_input("Kebutuhan Air (ml)", value=400, min_value=0)
    gula_juice = st.number_input("Kebutuhan Gula (gr)", value=70, min_value=0)
    tenaga_juice = st.number_input("Kebutuhan Tenaga Kerja (menit)", value=12, min_value=0)

st.header("🔧 Ketersediaan Sumber Daya per Bulan")
air_max = st.slider("Kapasitas Air (ml)", 5000, 50000, 20000, step=1000)
gula_max = st.slider("Kapasitas Gula (gr)", 1000, 10000, 4000, step=100)
tenaga_max = st.slider("Tenaga Kerja (menit)", 100, 5000, 1000, step=100)

if st.button("🚀 Jalankan Optimasi"):

    # Fungsi Tujuan (dalam bentuk minimisasi)
    # linprog melakukan minimisasi, jadi untuk maksimisasi keuntungan, kita negasikan nilai keuntungan
    c = [-profit_tea, -profit_juice]

    # Matriks koefisien batasan (A_ub * x <= b_ub)
    A = []
    b = []

    # Batasan Air
    if air_tea > 0 or air_juice > 0:
        A.append([air_tea, air_juice])
        b.append(air_max)
    else:
        st.warning("Kebutuhan Air untuk Teh Botol dan Jus Buah tidak boleh nol secara bersamaan jika ada batasan air.")

    # Batasan Gula
    if gula_tea > 0 or gula_juice > 0:
        A.append([gula_tea, gula_juice])
        b.append(gula_max)
    else:
        st.warning("Kebutuhan Gula untuk Teh Botol dan Jus Buah tidak boleh nol secara bersamaan jika ada batasan gula.")

    # Batasan Tenaga Kerja
    if tenaga_tea > 0 or tenaga_juice > 0:
        A.append([tenaga_tea, tenaga_juice])
        b.append(tenaga_max)
    else:
        st.warning("Kebutuhan Tenaga Kerja untuk Teh Botol dan Jus Buah tidak boleh nol secara bersamaan jika ada batasan tenaga kerja.")

    # Batasan variabel (non-negatif)
    # Produksi tidak bisa negatif
    bounds = [(0, None), (0, None)]

    # Optimasi menggunakan linprog
    try:
        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    except ValueError as e:
        st.error(f"Terjadi kesalahan saat menjalankan optimasi: {e}. Pastikan semua parameter input valid.")
        st.stop() # Hentikan eksekusi lebih lanjut jika ada error

    st.subheader("📈 Hasil Optimasi")
    if result.success:
        x1 = result.x[0] # Jumlah Teh Botol
        x2 = result.x[1] # Jumlah Jus Buah
        total_profit = -result.fun # Keuntungan maksimal (kembalikan ke positif)

        st.success("✅ Solusi optimal ditemukan!")
        st.write(f"**Jumlah Teh Botol (X₁)**: {x1:.2f} botol")
        st.write(f"**Jumlah Jus Buah (X₂)**: {x2:.2f} botol")
        st.write(f"**Total Keuntungan Maksimal**: Rp {total_profit:,.2f}")

        # Visualisasi grafik
        st.subheader("📊 Visualisasi Batasan dan Solusi")

        fig, ax = plt.subplots(figsize=(10, 8)) # Ukuran grafik yang lebih besar

        # Menentukan batas sumbu X dan Y yang lebih baik untuk visualisasi
        # Hitung titik potong maksimum untuk setiap sumbu
        max_x_intercept = 0
        if air_tea > 0: max_x_intercept = max(max_x_intercept, air_max / air_tea)
        if gula_tea > 0: max_x_intercept = max(max_x_intercept, gula_max / gula_tea)
        if tenaga_tea > 0: max_x_intercept = max(max_x_intercept, tenaga_max / tenaga_tea)

        max_y_intercept = 0
        if air_juice > 0: max_y_intercept = max(max_y_intercept, air_max / air_juice)
        if gula_juice > 0: max_y_intercept = max(max_y_intercept, gula_max / gula_juice)
        if tenaga_juice > 0: max_y_intercept = max(max_y_intercept, tenaga_max / tenaga_juice)

        # Tambahkan buffer ke batas maksimum untuk memastikan semua terlihat
        plot_x_max = max(x1, max_x_intercept) * 1.2
        plot_y_max = max(x2, max_y_intercept) * 1.2

        # Pastikan batas tidak nol jika semua input nol
        if plot_x_max == 0: plot_x_max = 100
        if plot_y_max == 0: plot_y_max = 100

        x_vals = np.linspace(0, plot_x_max, 500) # Perbanyak titik untuk garis yang lebih halus

        # Plot garis batasan
        # Batasan Air: air_tea * X1 + air_juice * X2 <= air_max
        # X2 = (air_max - air_tea * X1) / air_juice
        if air_juice != 0:
            y_air = (air_max - air_tea * x_vals) / air_juice
            ax.plot(x_vals, y_air, label="Batas Air", color='blue')
        elif air_tea != 0: # Jika air_juice nol, garisnya vertikal
            ax.axvline(x=air_max / air_tea, label="Batas Air", color='blue', linestyle='--')
        
        # Batasan Gula: gula_tea * X1 + gula_juice * X2 <= gula_max
        # X2 = (gula_max - gula_tea * X1) / gula_juice
        if gula_juice != 0:
            y_gula = (gula_max - gula_tea * x_vals) / gula_juice
            ax.plot(x_vals, y_gula, label="Batas Gula", color='green')
        elif gula_tea != 0: # Jika gula_juice nol, garisnya vertikal
            ax.axvline(x=gula_max / gula_tea, label="Batas Gula", color='green', linestyle='--')

        # Batasan Tenaga Kerja: tenaga_tea * X1 + tenaga_juice * X2 <= tenaga_max
        # X2 = (tenaga_max - tenaga_tea * X1) / tenaga_juice
        if tenaga_juice != 0:
            y_tenaga = (tenaga_max - tenaga_tea * x_vals) / tenaga_juice
            ax.plot(x_vals, y_tenaga, label="Batas Tenaga Kerja", color='orange')
        elif tenaga_tea != 0: # Jika tenaga_juice nol, garisnya vertikal
            ax.axvline(x=tenaga_max / tenaga_tea, label="Batas Tenaga Kerja", color='orange', linestyle='--')

        # Titik solusi optimal
        ax.plot(x1, x2, 'ro', markersize=10, label="Solusi Optimal") # Ukuran marker lebih besar
        ax.text(x1 + 0.02 * plot_x_max, x2 + 0.02 * plot_y_max, f'({x1:.1f}, {x2:.1f})', fontsize=10, color='red')

        # Pengaturan sumbu dan judul
        ax.set_xlabel("Teh Botol (X₁)")
        ax.set_ylabel("Jus Buah (X₂)")
        ax.set_title("Grafik Batasan Produksi dan Solusi Optimal")
        ax.legend()
        ax.grid(True)

        # Atur batas sumbu agar dimulai dari 0 dan mencakup semua titik relevan
        ax.set_xlim(0, plot_x_max)
        ax.set_ylim(0, plot_y_max)

        st.pyplot(fig)

    else:
        st.error("❌ Gagal menemukan solusi optimal. Silakan cek kembali parameter input atau pastikan ada daerah layak.")
        st.write(f"Status: {result.message}") # Tampilkan pesan error dari linprog
