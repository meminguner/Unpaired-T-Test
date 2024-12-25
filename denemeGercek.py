import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

st.title("T Testi Uygulaması")

# 1. Dosya yükleme
uploaded_file = st.file_uploader("Lütfen bir CSV dosyası yükleyin", type=["csv"])

if uploaded_file is not None:
    # 2. Yüklenen dosyanın içeriğini göster
    data = pd.read_csv(uploaded_file)
    st.write("Yüklenen Veri:")
    st.dataframe(data)

    # 3. Kullanıcıdan güven düzeyi ve sütun seçimi
    confidence_level = st.selectbox("Güven düzeyi:", [90, 95, 99])
    selected_columns = st.multiselect("T testi yapılacak sütunları seçin (iki sütun):", data.columns)

    if len(selected_columns) == 2:
        col1, col2 = selected_columns
        
        # Kategorik sütunlar için grup sayılarını hesapla
        if not pd.api.types.is_numeric_dtype(data[col1]):
            # İlk sütun için değer sayılarını hesapla
            value_counts1 = data[col1].value_counts()
            st.write(f"{col1} sütunu değer dağılımı:")
            st.write(value_counts1)
            
            # Kullanıcıdan hangi kategoriyi test etmek istediğini seç
            selected_category1 = st.selectbox(f"{col1} için test edilecek kategoriyi seçin:", value_counts1.index)
            series1 = (data[col1] == selected_category1).astype(float)
        else:
            # Sayısal sütun için NaN değerleri temizle ve float'a çevir
            series1 = pd.to_numeric(data[col1], errors='coerce').dropna()

        if not pd.api.types.is_numeric_dtype(data[col2]):
            # İkinci sütun için değer sayılarını hesapla
            value_counts2 = data[col2].value_counts()
            st.write(f"{col2} sütunu değer dağılımı:")
            st.write(value_counts2)
            
            # Kullanıcıdan hangi kategoriyi test etmek istediğini seç
            selected_category2 = st.selectbox(f"{col2} için test edilecek kategoriyi seçin:", value_counts2.index)
            series2 = (data[col2] == selected_category2).astype(float)
        else:
            # Sayısal sütun için NaN değerleri temizle ve float'a çevir
            series2 = pd.to_numeric(data[col2], errors='coerce').dropna()

        # Veri setlerinin boyutlarını kontrol et
        if len(series1) > 0 and len(series2) > 0:
            # T testi
            alpha = 1 - (confidence_level / 100)
            t_stat, p_value = ttest_ind(series1, series2, equal_var=False)
            
            # Sonuçları göster
            st.write(f"T istatistiği: {t_stat:.4f}")
            
            # P değerini bilimsel notasyonla göster
            if p_value < 0.0001:
                st.write(f"P değeri: {p_value:.2e}")  # Bilimsel notasyon
            else:
                st.write(f"P değeri: {p_value:.4f}")  # Normal format
                
            if p_value < alpha:
                st.success("Sonuç: H0 hipotezi reddedilir.")
            else:
                st.info("Sonuç: H0 hipotezi reddedilemez.")
        else:
            st.error("Seçilen sütunlarda yeterli veri bulunamadı!")
    else:
        st.warning("Lütfen iki sütun seçin!")
else:
    st.info("Bir dosya yüklemeden devam edemezsiniz.")
