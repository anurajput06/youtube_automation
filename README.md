# 🎥 YouTube Automation using Python, Selenium & Pytest

This project automates YouTube using **Python** and **Selenium WebDriver**.  
It automatically searches for a topic, opens the first video, and verifies successful playback.  
Detailed HTML test reports are generated using **Pytest**.

---

## 🚀 Features
✅ Launches YouTube automatically  
✅ Searches for any topic (customizable)  
✅ Clicks and plays the first video result  
✅ Generates a beautiful HTML test report  
✅ Uses Page Object Model (POM) for better maintainability  

---

## 🧠 Project Description
This project demonstrates a **real-world web automation framework**.  
It’s built with **Python + Selenium + Pytest** and is ideal for automation portfolios.  
The script searches for a topic (like “Data Structure and Algorithm lecture”) and plays the first YouTube video found.

---

## 🗂️ Folder Structure
youtube_automation/
├── config/ # Configuration (browser, keyword, waits)
├── pages/ # Page Object (YouTube actions)
├── tests/ # Test scripts
├── utils/ # Driver and config helper files
├── report.html # Generated test report
└── requirements.txt # Dependencies

---

## ⚙️ How to Run
```bash
### 1️⃣ Create and activate virtual environment

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest --html=report.html --self-contained-html
Then open report.html in your browser to view results ✅
[DEFAULT]
search_keyword = Data Structure and Algorithm lecture...You can edit this anytime..

