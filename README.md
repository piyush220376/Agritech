<div align="center">

# 🌾 AI Farmer Chat Bot

**A multilingual desktop assistant for Indian farmers — powered by local AI, live mandi prices, and plant disease detection.**

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-Desktop%20UI-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Plant%20AI-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

[Features](#-features) • [Screenshots](#-screenshots) • [Installation](#-installation) • [Usage](#-usage) • [Project Structure](#-project-structure) • [API Setup](#-api-setup)

</div>

---

## 📖 About

**AI Farmer Chat Bot** is a fully offline-capable desktop application built for Indian farmers. It combines a local Large Language Model (LLM) for agricultural Q&A, real-time mandi (crop market) price fetching via the Government of India's open data API, and a deep learning model for plant disease detection — all wrapped in a clean, multilingual PyQt5 interface.

> Designed to work in **Hindi, Gujarati, Telugu**, and **English** to reach farmers across different states of India.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 **AI Chat Assistant** | Powered by a local LLM via [LM Studio](https://lmstudio.ai) — works offline, no data sent to the cloud |
| 🌱 **Plant Disease Detection** | Upload a crop photo → the app identifies the disease using a fine-tuned Xception model (38 disease classes) |
| 📊 **Live Mandi Prices** | Fetches real-time crop prices from [data.gov.in](https://data.gov.in) (official Govt. of India API) |
| 🎙️ **Voice Input** | Speak your query in English or Hindi using offline Vosk speech recognition |
| 🌐 **4-Language UI** | Full UI translation: English, हिन्दी, ગુજરાતી, తెలుగు |
| 🔒 **Privacy First** | LLM runs 100% locally; only mandi price API calls go to the internet |

---

## 🖥️ Screenshots

> *(Add screenshots of the Chat, Disease Detection, and Mandi Prices tabs here)*

---

## 🏗️ Project Structure

```
ai farmer chat bot/
│
├── src/
│   ├── main.py            # Entry point — loads .env, launches PyQt5 app
│   ├── ui.py              # Main window: Chat, Disease Detection, Mandi Prices tabs
│   ├── chat_model.py      # LM Studio (local LLM) integration
│   ├── classifier.py      # Zero-shot agriculture topic classifier (BART)
│   ├── translation.py     # Multilingual translation via googletrans
│   ├── prices.py          # Live mandi prices via data.gov.in REST API  ← main fetch
│   ├── mandi.py           # Re-exports prices.py (backward compatibility)
│   ├── plant_model.py     # Xception plant disease detection
│   └── voice_model.py     # Offline voice input via Vosk
│
├── models/
│   ├── vosk-model-small-en-us-0.15/   # English speech model (download separately)
│   └── vosk-model-small-hi-0.22/      # Hindi speech model (download separately)
│
├── plant_detection/
│   └── xception_best_phase4.h5        # Trained plant disease model (download separately)
│
├── ui/
│   └── image.png          # Background image for the app
│
├── .env                   # API keys (never commit this file)
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python **3.9 or 3.10** (TensorFlow compatibility)
- [LM Studio](https://lmstudio.ai) running locally with an agriculture-tuned model loaded
- Microphone (optional, for voice input)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-farmer-chat-bot.git
cd "ai-farmer-chat-bot"
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install PyQt5 requests tensorflow pillow numpy \
            vosk pyaudio googletrans==4.0.0-rc1 transformers torch
```

### 4. Download AI models

Download the model files from the **[GitHub Releases](https://github.com/piyush220376/Agritech/releases)** page of this repository.

#### Vosk speech models (offline voice)
Download `models.zip` and extract it directly into the `models/` directory so it looks like this:
```
models/
  ├── vosk-model-small-en-us-0.15/
  ├── vosk-model-small-hi-0.22/
  └── ...
```

#### Plant disease model
Download `xception_best_phase4.zip`, extract it, and place the `xception_best_phase4.h5` file into the `plant_detection/` directory:
```
plant_detection/
  └── xception_best_phase4.h5
```

### 5. Configure environment

Rename `.env.example` to `.env` (or edit the existing `.env`):

```env
# Get your free key at https://data.gov.in/
DATA_GOV_API_KEY=your_40_character_key_here

# LM Studio settings (defaults shown)
LM_STUDIO_BASE_URL=http://127.0.0.1:1234/v1
LM_STUDIO_MODEL=farmer-chatbot
```

### 6. Run the app

```bash
cd src
python main.py
```

---

## 🚀 Usage

### 💬 Chat Tab
1. Select your preferred language (English / Hindi / Gujarati / Telugu)
2. Type or speak an agriculture-related question
3. The bot classifies the query, sends it to the local LLM, and replies in your language

> Questions not related to farming are rejected with: *"I can only answer agriculture-related questions."*

### 🌿 Disease Detection Tab
1. Click **Upload Image** → select a photo of a plant leaf
2. Click **Analyze**
3. The app returns the detected disease from 38 possible classes (Apple scab, Tomato blight, etc.)

### 📊 Mandi Prices Tab
1. Select a **commodity** (Wheat, Rice, Soyabean, Tomato, Onion, Potato, Cotton)
2. Select a **market** (Indore, Bhopal, Ujjain, Gwalior, Jabalpur)
3. Click **Fetch Prices**
4. Live wholesale Min / Modal / Max prices are displayed (sourced from Government of India)

### 🎙️ Voice Input
- Click the **Voice** button — speak your question — query is auto-sent to chat

---

## 🌐 API Setup

### data.gov.in — Mandi Prices (Free)

The mandi price feature uses the official **Government of India Open Data** API.

| Field | Value |
|---|---|
| Dataset | [Current Daily Price of Various Commodities from Various Markets](https://data.gov.in/catalog/current-daily-price-various-commodities-various-markets-mandi) |
| Resource ID | `9ef84268-d588-465a-a308-a864a43d0070` |
| Endpoint | `https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070` |
| Cost | **Free** |

**Steps to get your key:**
1. Register at [data.gov.in](https://data.gov.in/)
2. Open the dataset page → **Data API** tab
3. Copy your API key → paste it in `.env` as `DATA_GOV_API_KEY`

---

## 🤖 Supported Plant Diseases (38 Classes)

<details>
<summary>Click to expand full list</summary>

| Crop | Conditions Detected |
|---|---|
| Apple | Apple Scab, Black Rot, Cedar Apple Rust, Healthy |
| Blueberry | Healthy |
| Cherry | Powdery Mildew, Healthy |
| Corn (Maize) | Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy |
| Grape | Black Rot, Esca (Black Measles), Leaf Blight, Healthy |
| Orange | Haunglongbing (Citrus Greening) |
| Peach | Bacterial Spot, Healthy |
| Pepper | Bacterial Spot, Healthy |
| Potato | Early Blight, Late Blight, Healthy |
| Raspberry | Healthy |
| Soybean | Healthy |
| Squash | Powdery Mildew |
| Strawberry | Leaf Scorch, Healthy |
| Tomato | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy |

</details>

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **UI** | PyQt5 (Desktop GUI) |
| **Local LLM** | LM Studio (OpenAI-compatible API) |
| **Topic Filter** | Facebook BART (zero-shot classification via HuggingFace) |
| **Disease Detection** | TensorFlow / Xception CNN |
| **Voice Input** | Vosk (fully offline ASR) |
| **Translation** | googletrans (Google Translate wrapper) |
| **Mandi Prices** | data.gov.in REST API (JSON) |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Vosk](https://alphacephei.com/vosk/) — Offline speech recognition
- [LM Studio](https://lmstudio.ai) — Local LLM inference
- [data.gov.in](https://data.gov.in) — Government of India Open Data Platform
- [PlantVillage Dataset](https://plantvillage.psu.edu/) — Plant disease training data
- [HuggingFace Transformers](https://huggingface.co/transformers/) — BART zero-shot classifier

---

<div align="center">
Made with ❤️ for Indian Farmers 🌾
</div>
