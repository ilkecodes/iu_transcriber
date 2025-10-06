"""
İstanbul Üniversitesi İletişim Fakültesi
Ses Transkriptor Uygulaması (Streamlit Web Versiyonu)

Özellikler:
- Ses dosyası yükleme
- Whisper ile Türkçe transkripsiyon
- Progress bar ile işlem takibi
- Web üzerinden erişilebilir

Çalıştırma: streamlit run app.py
"""

import streamlit as st
import whisper
import tempfile
import os
from datetime import datetime

# Sayfa ayarları
st.set_page_config(
    page_title="İÜ İletişim - Ses Transkriptor",
    page_icon="🎓",
    layout="wide"
)

# Özel CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #8B1538;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #a01848;
    }
    .header-container {
        background: linear-gradient(135deg, #8B1538 0%, #a01848 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .info-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #8B1538;
        margin: 1rem 0;
    }
    .transcript-box {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        min-height: 300px;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Başlık
st.markdown("""
<div class="header-container">
    <h1>🎓 İstanbul Üniversitesi İletişim Fakültesi</h1>
    <h2>Ses Transkriptor Uygulaması</h2>
    <p>Türkçe ses kayıtlarınızı metne dönüştürün</p>
</div>
""", unsafe_allow_html=True)

# Session state başlatma
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'model' not in st.session_state:
    st.session_state.model = None

# Whisper modelini yükle (cache ile)
@st.cache_resource
def load_whisper_model(model_size="base"):
    """Whisper modelini yükle ve cache'le"""
    return whisper.load_model(model_size)

def transcribe_audio(audio_file, language="tr"):
    """Ses dosyasını transkript et"""
    try:
        # Dosya boyutunu kontrol et
        audio_file.seek(0, 2)  # Dosya sonuna git
        file_size = audio_file.tell()  # Boyutu al
        audio_file.seek(0)  # Başa dön
        
        file_size_mb = file_size / (1024 * 1024)
        
        if file_size_mb > 500:
            st.error(f"❌ Dosya çok büyük ({file_size_mb:.1f}MB). Lütfen 500MB'dan küçük bir dosya yükleyin.")
            return None
        
        if file_size_mb > 100:
            st.warning(f"⚠️ Büyük dosya ({file_size_mb:.1f}MB) - İşlem biraz uzun sürebilir...")
        
        # Progress bar oluştur
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Adım 1: Model yükleme
        status_text.text('🔄 Whisper modeli yükleniyor...')
        progress_bar.progress(20)
        
        if st.session_state.model is None:
            st.session_state.model = load_whisper_model("base")
        
        # Adım 2: Dosya hazırlama
        status_text.text('📁 Ses dosyası hazırlanıyor...')
        progress_bar.progress(40)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        # Adım 3: Transkripsiyon
        status_text.text('✍️ Transkript oluşturuluyor... (Bu adım biraz zaman alabilir)')
        progress_bar.progress(60)
        
        result = st.session_state.model.transcribe(tmp_path, language=language, verbose=False)
        
        # Adım 4: Temizlik
        status_text.text('🧹 Tamamlanıyor...')
        progress_bar.progress(90)
        
        os.unlink(tmp_path)
        
        # Tamamlandı
        progress_bar.progress(100)
        status_text.text('✅ Transkripsiyon başarıyla tamamlandı!')
        
        return result
    
    except Exception as e:
        st.error(f"❌ Hata: {str(e)}")
        return None

# Ana içerik
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📁 Ses Dosyası Yükle")
    
    # Dosya boyutu uyarısı
    st.info("💡 Maksimum dosya boyutu: 500MB. Daha büyük dosyalar için ses dosyanızı bölmeniz önerilir.")
    
    uploaded_file = st.file_uploader(
        "WAV, MP3, M4A veya FLAC formatında ses dosyası seçin",
        type=['wav', 'mp3', 'm4a', 'flac', 'ogg'],
        help="En iyi sonuçlar için WAV formatı önerilir. Çok büyük dosyalar işlem süresini artırabilir."
    )
    
    if uploaded_file:
        st.audio(uploaded_file, format=f'audio/{uploaded_file.name.split(".")[-1]}')
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            if st.button("✍️ Transkript Oluştur", use_container_width=True):
                result = transcribe_audio(uploaded_file)
                
                if result:
                    # Zaman damgalı transkript
                    transcript_lines = []
                    transcript_lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                    transcript_lines.append(f"📅 Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                    transcript_lines.append(f"📄 Dosya: {uploaded_file.name}")
                    transcript_lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
                    
                    if 'segments' in result:
                        for seg in result['segments']:
                            start = seg['start']
                            mins = int(start // 60)
                            secs = int(start % 60)
                            timestamp = f"[{mins:02d}:{secs:02d}]"
                            text = seg['text'].strip()
                            transcript_lines.append(f"{timestamp} {text}")
                    else:
                        transcript_lines.append(result['text'])
                    
                    st.session_state.transcript = "\n".join(transcript_lines)
                    st.success("✅ Transkripsiyon tamamlandı!")
                    st.balloons()
        
        with col_btn2:
            if st.session_state.transcript:
                # İndirme butonu
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"transkript_{timestamp}.txt"
                
                st.download_button(
                    label="💾 İndir",
                    data=st.session_state.transcript,
                    file_name=filename,
                    mime="text/plain",
                    use_container_width=True
                )

with col2:
    st.markdown("### ⚙️ Ayarlar")
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**Model Boyutu:**")
    model_size = st.selectbox(
        "Model seçin",
        ["tiny", "base", "small", "medium"],
        index=1,
        help="Tiny: En hızlı, Base: Dengeli, Small/Medium: En iyi kalite"
    )
    
    if st.button("🔄 Modeli Yenile"):
        st.session_state.model = None
        st.cache_resource.clear()
        st.success("Model temizlendi!")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**💡 İpuçları:**")
    st.markdown("""
    - Sessiz ortamda kayıt yapın
    - Net ve açık konuşun
    - WAV formatı en iyi sonucu verir
    - Örtüşen konuşmalar tanımayı zorlaştırır
    - İlk kullanımda model indirileceği için biraz bekleyin
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Transkript gösterimi
st.markdown("### 📝 Transkript")

if st.session_state.transcript:
    st.markdown('<div class="transcript-box">', unsafe_allow_html=True)
    st.text_area(
        "Transkript İçeriği",
        value=st.session_state.transcript,
        height=400,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👆 Bir ses dosyası yükleyin ve 'Transkript Oluştur' butonuna tıklayın")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎓 İstanbul Üniversitesi İletişim Fakültesi | Ses Transkriptor v1.0</p>
    <p style='font-size: 0.8rem;'>Whisper AI ile güçlendirilmiştir 🚀</p>
</div>
""", unsafe_allow_html=True)