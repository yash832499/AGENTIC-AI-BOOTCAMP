# Day 3 Project: CrewAI Multi-Agent System 🤖🤝

This project demonstrates a **Multi-Agent System** using [CrewAI](https://crewai.com).
Instead of a single bot doing everything, we have a team of specialized agents working together.

## The Crew
1.  **Researcher Agent:** Uses DuckDuckGo to find real-time information.
2.  **Writer Agent:** Takes the research and writes a beginner-friendly summary.

## How It Works
The user provides a topic. The **Researcher** searches for it and passes notes to the **Writer**, who produces the final article.

## How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set Up API Key:**
    -   Create a `.env` file in this folder.
    -   Add your `GOOGLE_API_KEY`.

3.  **Run the App:**
    ```bash
    streamlit run app.py
    ```
