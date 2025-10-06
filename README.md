# 🎓 İstanbul Üniversitesi İletişim Fakültesi
# Ses Transkriptor Uygulaması

Türkçe ses kayıtlarını otomatik olarak metne dönüştüren web tabanlı transkriptor uygulaması.

## ✨ Özellikler

- 🎤 Ses dosyası yükleme (WAV, MP3, M4A, FLAC, OGG)
- 🇹🇷 Türkçe transkripsiyon desteği
- ⏱️ Zaman damgalı çıktı
- 💾 Transkript indirme
- 🎨 Modern ve kullanıcı dostu arayüz
- 🚀 OpenAI Whisper AI teknolojisi

## 🛠️ Kurulum

### Gereksinimler

- Python 3.8+
- pip

### Adımlar

1. Repoyu klonlayın:
```bash
git clone https://github.com/KULLANICI_ADINIZ/ses-transkriptor.git
cd ses-transkriptor
```

2. Sanal ortam oluşturun (önerilen):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## 🚀 Kullanım

Uygulamayı başlatın:
```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak açılacaktır (genellikle `http://localhost:8501`)

## 📦 Gerekli Paketler

- streamlit
- openai-whisper
- torch

Detaylı liste için `requirements.txt` dosyasına bakın.

## 💡 Kullanım İpuçları

- Sessiz bir ortamda kayıt yapın
- Net ve anlaşılır konuşun
- WAV formatı en iyi sonucu verir
- Örtüşen konuşmalar tanımayı zorlaştırabilir

## 🎯 Model Boyutları

- **tiny**: En hızlı, düşük doğruluk
- **base**: Dengeli (varsayılan)
- **small**: İyi doğruluk
- **medium**: Yüksek doğruluk, yavaş

## 📝 Lisans

Bu proje eğitim amaçlıdır.

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

## 📧 İletişim

İstanbul Üniversitesi İletişim Fakültesi

---

**Not**: İlk çalıştırmada Whisper modeli indirilecektir (~140MB - base model)