"""
İstanbul Üniversitesi İletişim Fakültesi
Ses Transkriptor Uygulaması (Streamlit Web Versiyonu)

Özellikler:
- Mikrofondan ses kaydı
- Ses dosyası yükleme
- Whisper ile Türkçe transkripsiyon
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

# Özel CSS - Dark mode desteği ile
st.markdown("""
<style>
/* Butonlar */
.stButton>button {
    background-color: #8B1538 !important;
    color: white !important;
    font-weight: bold;
    border-radius: 5px;
    padding: 0.5rem 2rem;
    border: none;
}
.stButton>button:hover {
    background-color: #a01848 !important;
}

/* Başlık */
.header-container {
    background: linear-gradient(135deg, #8B1538 0%, #a01848 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}

/* Info kutucukları - Dark mode uyumlu */
.info-box {
    background-color: rgba(139, 21, 56, 0.1);
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 5px solid #8B1538;
    margin: 1rem 0;
}

/* Transkript kutusu - Dark mode uyumlu */
.transcript-box {
    background-color: rgba(139, 21, 56, 0.05);
    padding: 2rem;
    border-radius: 10px;
    border: 2px solid rgba(139, 21, 56, 0.3);
    min-height: 300px;
    font-family: 'Courier New', monospace;
}

/* Selectbox ve diğer input'lar için dark mode düzeltmesi */
[data-baseweb="select"] {
    background-color: transparent !important;
}

/* File uploader düzeltmesi */
[data-testid="stFileUploader"] {
    background-color: transparent !important;
}

/* Text area düzeltmesi */
.stTextArea textarea {
    background-color: rgba(139, 21, 56, 0.05) !important;
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
if 'model' not in st.session_state:
    st.session_state.model = None
if 'model_size' not in st.session_state:
    st.session_state.model_size = "base"

# Whisper modelini yükle (cache ile)
@st.cache_resource
def load_whisper_model(model_size="base"):
    return whisper.load_model(model_size)

def transcribe_audio(audio_file, language="tr"):
    try:
        if st.session_state.model is None:
            with st.spinner('🔄 Whisper modeli yükleniyor...'):
                st.session_state.model = load_whisper_model("base")
        
        # Dosya uzantısını koru
        file_extension = audio_file.name.split('.')[-1]
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        with st.spinner('✍️ Transkript oluşturuluyor...'):
            # FFmpeg olmadan çalışması için fp16=False ekle
            result = st.session_state.model.transcribe(
                tmp_path, 
                language=language,
                fp16=False  # CPU için gerekli
            )
        
        os.unlink(tmp_path)
        return result
    except FileNotFoundError as e:
        if 'ffmpeg' in str(e):
            st.error("❌ FFmpeg bulunamadı! Lütfen FFmpeg'i kurun:")
            st.code("Windows: choco install ffmpeg\nmacOS: brew install ffmpeg\nLinux: sudo apt install ffmpeg")
        else:
            st.error(f"❌ Hata: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Hata: {str(e)}")
        return None

# Ana içerik
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📁 Ses Dosyası Yükle")
    uploaded_file = st.file_uploader(
        "WAV, MP3, M4A veya FLAC seçin",
        type=['wav','mp3','m4a','flac','ogg']
    )
    if uploaded_file:
        st.audio(uploaded_file, format=f'audio/{uploaded_file.name.split(".")[-1]}')
        
        col_btn1, col_btn2 = st.columns([1,1])
        with col_btn1:
            if st.button("✍️ Transkript Oluştur", use_container_width=True):
                result = transcribe_audio(uploaded_file)
                if result:
                    lines = [
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                        f"📅 Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                        f"📄 Dosya: {uploaded_file.name}",
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    ]
                    if 'segments' in result:
                        for seg in result['segments']:
                            mins, secs = int(seg['start']//60), int(seg['start']%60)
                            lines.append(f"[{mins:02d}:{secs:02d}] {seg['text'].strip()}")
                    else:
                        lines.append(result['text'])
                    st.session_state.transcript = "\n".join(lines)
                    st.success("✅ Transkripsiyon tamamlandı!")
                    st.balloons()
        with col_btn2:
            if st.session_state.transcript:
                filename = f"transkript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                st.download_button("💾 İndir", st.session_state.transcript, filename, "text/plain")

with col2:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**Model Boyutu:**")
    st.session_state.model_size = st.selectbox(
        "Seçin", 
        ["tiny", "base", "small", "medium"], 
        index=["tiny", "base", "small", "medium"].index(st.session_state.model_size),
        key="model_size_select"
    )
    if st.button("🔄 Modeli Yenile"):
        st.session_state.model = None
        st.cache_resource.clear()
        st.success("Model temizlendi!")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**💡 İpuçları:**\n- Sessiz ortamda kayıt yapın\n- Net konuşun\n- WAV formatı en iyi sonucu verir\n- Örtüşen konuşmalar zorlaştırır")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### 📝 Transkript")
if st.session_state.transcript:
    st.markdown('<div class="transcript-box">', unsafe_allow_html=True)
    st.text_area("Transkript Metni", st.session_state.transcript, height=400, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👆 Bir ses dosyası yükleyin ve 'Transkript Oluştur' butonuna tıklayın")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎓 İstanbul Üniversitesi İletişim Fakültesi | Ses Transkriptor v1.0</p>
    <p style='font-size: 0.8rem;'>Whisper AI ile güçlendirilmiştir 🚀</p>
</div>
""", unsafe_allow_html=True)