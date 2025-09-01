
# 🌍 NGO Amplify - Amplification Platform for NGOs

**NGO Amplify** is a web-based platform designed to **empower non-governmental organizations (NGOs)** by providing a unified solution for **data management**, **resource sharing**, and **impact visualization**. It aims to foster **collaboration**, **transparency**, and **efficiency** within the social sector.

---

## ✨ Core Features

The platform is built around four core modules to address the common challenges faced by NGOs:

### 📈 Impact Dashboard
- Visualize NGO locations and impact areas on an interactive map.
- Dynamically filter NGOs by their area of impact or founding year.
- View detailed profiles for each organization with specific metrics and goals.
- Export aggregated impact data to CSV for reporting and analysis.

### 🤝 Community Resource Network
- A central hub for NGOs to **share** and **request** resources.
- Filter by type: **Goods**, **Volunteers**, or **Services**.
- Align resources with **UN Sustainable Development Goals (SDGs)**.
- Seamless "Request" and "Donate" features.

### 📝 Field Data Collection
- Mobile-friendly form for field agents to submit impact data directly.
- Features include:
  - Dynamic metric selection
  - Location capture
  - Photo evidence uploads

### 📢 Announcements Board
- A platform-wide announcement system for:
  - Urgent needs
  - Upcoming events
  - Important updates
- Categorized as: **Urgent**, **Event**, or **Information**

---

## 🛠️ Tech Stack

- **Backend**: Python + Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Templating**: Jinja2
- **Mapping**: Leaflet.js

---

## 🚀 Getting Started

Follow these instructions to set up the project for local development and testing.

### ✅ Prerequisites

- Python 3.x
- `pip` package installer

### 📥 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/diveshadivarekar/ngo_platform.git
   cd ngo_platform
    ````

2. **Create and activate a virtual environment**

   **Windows:**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   **macOS / Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python app.py
   ```

5. **Open in browser**

   Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📂 Project Structure

```
ngo_platform/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── static/
│   └── css/
│       └── style.css       # Stylesheet
└── templates/
    ├── base.html           # Base layout
    ├── index.html          # Landing page
    ├── dashboard.html      # Impact Dashboard
    ├── resources.html      # Resource Network
    ├── data_collection.html# Field data collection form
    ├── announcements.html  # Announcements
    ├── ngo_profile.html    # NGO detail page
    ├── donate.html         # Donation form
    └── 404.html            # Custom 404 error page
```


## 🙌 Contributing

We welcome contributions from developers, designers, and changemakers. If you'd like to contribute, please open an issue or submit a pull request!

---

## 🌐 Contact

For questions or collaboration opportunities, reach out via [GitHub Issues](https://github.com/diveshadivarekar/ngo_platform/issues).



