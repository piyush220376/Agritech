# 🌾 AI Farmer Chat Bot

<div align="center">

**A multilingual desktop assistant for Indian farmers — powered by local AI, live mandi prices, and plant disease detection.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-Desktop%20UI-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Plant%20AI-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Offline](https://img.shields.io/badge/LLM-100%25%20Offline-green?style=for-the-badge&logo=lock&logoColor=white)]()

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Project Structure](#-project-structure) • [API Setup](#-api-setup) • [Contributing](#-contributing)

</div>

---

## 📖 About

**AI Farmer Chat Bot** is a fully offline-capable desktop application built specifically for Indian farmers. It combines a locally-running Large Language Model (LLM) for agricultural Q&A, real-time mandi (crop market) price fetching via the Government of India's open data API, and a deep learning model for plant disease detection — all wrapped in a clean, multilingual PyQt5 interface.

> 🗣️ Supports **Hindi, Gujarati, Telugu**, and **English** — designed to reach farmers across different states of India.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 **AI Chat Assistant** | Powered by a local LLM via [LM Studio](https://lmstudio.ai) — works fully offline, no data sent to the cloud |
| 🌱 **Plant Disease Detection** | Upload a crop photo → detects disease using a fine-tuned Xception CNN (38 disease classes) |
| 📊 **Live Mandi Prices** | Fetches real-time wholesale crop prices from [data.gov.in](https://data.gov.in) (official Govt. of India API) |
| 🎙️ **Voice Input** | Speak your query in English or Hindi using offline Vosk speech recognition |
| 🌐 **4-Language UI** | Full UI translation: English, हिन्दी, ગુજરાતી, తెలుగు |
| 🔒 **Privacy First** | LLM runs 100% locally; only mandi price API calls touch the internet |

---

## 🏗️ Project Structure

```
Agritech/
│
├── src/
│   ├── main.py            # Entry point — loads .env, launches PyQt5 app
│   ├── ui.py              # Main window: Chat, Disease Detection, Mandi Prices tabs
│   ├── chat_model.py      # LM Studio (local LLM) integration
│   ├── classifier.py      # Zero-shot agriculture topic classifier (BART)
│   ├── translation.py     # Multilingual translation via googletrans
│   ├── prices.py          # Live mandi prices via data.gov.in REST API
│   ├── mandi.py           # Re-exports prices.py (backward compatibility)
│   ├── plant_model.py     # Xception plant disease detection
│   └── voice_model.py     # Offline voice input via Vosk
│
├── models/                          # Git LFS — split zip archive
│   ├── models.z01                   # Part 1 of 3
│   ├── models.z02                   # Part 2 of 3
│   ├── models.zip                   # Part 3 (final) — extract all together
│   ├── vosk-model-small-en-us-0.15/ # ← after extraction: English ASR model
│   └── vosk-model-small-hi-0.22/   # ← after extraction: Hindi ASR model
│
├── plant_detection/                       # Git LFS — split zip archive
│   ├── xception_best_phase4.z01           # Part 1 of 4
│   ├── xception_best_phase4.z02           # Part 2 of 4
│   ├── xception_best_phase4.z03           # Part 3 of 4
│   ├── xception_best_phase4.zip           # Part 4 (final) — extract all together
│   └── xception_best_phase4.h5            # ← after extraction: trained CNN model
│
├── ui/
│   └── image.png          # Background image for the app
│
├── .gitattributes         # Git LFS tracking config
├── .gitignore
├── .env                   # API keys (never commit this file)
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python **3.9 or 3.10** (required for TensorFlow compatibility)
- [LM Studio](https://lmstudio.ai) running locally with an agriculture-tuned model loaded
- A microphone *(optional, for voice input)*

### 1. Clone the repository

```bash
git clone https://github.com/piyush220376/Agritech.git
cd Agritech

# Pull Git LFS files (required to download the model archives)
git lfs install
git lfs pull
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

### 4. Download & extract AI models

The model files are stored in the repository using **Git LFS** as split zip archives. After cloning, you need to reassemble and extract them manually.

#### Vosk Speech Models (offline voice recognition)

The `models/` folder contains three split parts: `models.z01`, `models.z02`, and `models.zip`.

**Step 1 — Install Git LFS and pull the files** *(skip if already done)*
```bash
git lfs install
git lfs pull
```

**Step 2 — Reassemble and extract**

On **Windows** (using 7-Zip):
```bash
# Right-click models.zip → 7-Zip → Extract Here
# OR from command line:
"C:\Program Files\7-Zip\7z.exe" x models.zip -o models/
```

On **Linux / macOS**:
```bash
cd models/
cat models.z01 models.z02 models.zip > models_combined.zip
unzip models_combined.zip
rm models_combined.zip
```

After extraction, the `models/` folder should look like:
```
models/
├── models.z01
├── models.z02
├── models.zip
├── vosk-model-small-en-us-0.15/   ← extracted
└── vosk-model-small-hi-0.22/      ← extracted
```

#### Plant Disease Model

The `plant_detection/` folder contains four split parts: `xception_best_phase4.z01`, `.z02`, `.z03`, and `.zip`.

**Reassemble and extract:**

On **Windows** (using 7-Zip):
```bash
"C:\Program Files\7-Zip\7z.exe" x xception_best_phase4.zip -o plant_detection/
```

On **Linux / macOS**:
```bash
cd plant_detection/
cat xception_best_phase4.z01 xception_best_phase4.z02 xception_best_phase4.z03 xception_best_phase4.zip > model_combined.zip
unzip model_combined.zip
rm model_combined.zip
```

After extraction:
```
plant_detection/
├── xception_best_phase4.z01
├── xception_best_phase4.z02
├── xception_best_phase4.z03
├── xception_best_phase4.zip
└── xception_best_phase4.h5     ← extracted model file
```

> 💡 **Tip:** If `unzip` fails on split archives, install [7-Zip](https://www.7-zip.org/) — it handles `.z01`/`.z02` multi-part zips natively on all platforms.

### 5. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
# Get your free key at https://data.gov.in/
DATA_GOV_API_KEY=your_40_character_key_here

# LM Studio settings (defaults shown)
LM_STUDIO_BASE_URL=http://127.0.0.1:1234/v1
LM_STUDIO_MODEL=farmer-chatbot
```

### 6. Launch the app

```bash
cd src
python main.py
```

---

## 🚀 Usage

### 💬 Chat Tab

1. Select your preferred language from the dropdown (English / Hindi / Gujarati / Telugu)
2. Type or click the **Voice** button to speak an agriculture-related question
3. The bot classifies the query, sends it to the local LLM, and replies in your selected language

> ⚠️ Questions unrelated to farming are politely rejected: *"I can only answer agriculture-related questions."*

### 🌿 Disease Detection Tab

1. Click **Upload Image** and select a photo of a plant leaf
2. Click **Analyze**
3. The app returns the detected condition from 38 possible disease classes (e.g., Apple Scab, Tomato Blight)

### 📊 Mandi Prices Tab

1. Select a **commodity** (Wheat, Rice, Soyabean, Tomato, Onion, Potato, Cotton)
2. Select a **market** (Indore, Bhopal, Ujjain, Gwalior, Jabalpur)
3. Click **Fetch Prices**
4. Live wholesale **Min / Modal / Max** prices are displayed — sourced directly from the Government of India

### 🎙️ Voice Input

Click the **Voice** button, speak your question, and it will be auto-submitted to the chat.

---

## 🌐 API Setup — data.gov.in (Free)

The mandi price feature uses the official Government of India Open Data API.

| Field | Value |
|---|---|
| Dataset | Current Daily Price of Various Commodities from Various Markets |
| Resource ID | `9ef84268-d588-465a-a308-a864a43d0070` |
| Endpoint | `https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070` |
| Cost | **Free** |

**Steps to get your API key:**

1. Register at [data.gov.in](https://data.gov.in)
2. Find the commodity price dataset → go to the **Data API** tab
3. Copy your API key and paste it into `.env` as `DATA_GOV_API_KEY`

---

## 🌿 Supported Plant Diseases (38 Classes)

<details>
<summary>Click to expand the full list</summary>

| Crop | Conditions Detected |
|---|---|
| Apple | Apple Scab, Black Rot, Cedar Apple Rust, Healthy |
| Blueberry | Healthy |
| Cherry | Powdery Mildew, Healthy |
| Corn (Maize) | Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy |
| Grape | Black Rot, Esca (Black Measles), Leaf Blight, Healthy |
| Orange | Huanglongbing (Citrus Greening) |
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
| **Local LLM** | LM Studio (OpenAI-compatible local API) |
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

<div align="center">Made with ❤️ for Indian Farmers 🌾</div>
