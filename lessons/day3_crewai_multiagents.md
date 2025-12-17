# 🤖 Day 3 — Multi-Agent Systems with CrewAI

**Theme:** “How Do Many AIs Think Together Like a Team?”  
**Goal:** Build your first multi-agent system: a Researcher Agent + Writer Agent working together.

---

# 1️⃣ Story Time — “Two Kids Doing a Project”
Imagine you ask two kids:

- **Kid 1: Researcher** → “Find all the information.”
- **Kid 2: Writer** → “Turn it into a neat explanation.”

They work together like a team.

Now imagine both kids are **AI agents**.  
That’s a **multi-agent system**.

---

# 2️⃣ What Are Agents? (Explain Like I'm 5)
Agents are like **tiny smart workers** inside your computer.

Each agent has:

🧠 **A brain** → LLM  
🎯 **A goal** → What they must do  
🔧 **Tools** → Google search, calculator, APIs  
📄 **Tasks** → Their assignment  

Put many agents together → they behave like a **team of helpers**.

---

# 3️⃣ Whiteboard Visuals for Today

### A. One Brain vs Many

> Single agent → One smart worker
> Multi-agent → A whole team working together

### B. Agent Anatomy

> [ Goal ]
> [ Role ]
> [ LLM Brain ]
> [ Tools ]

### C. The Team Pipeline

> Researcher → Writer → Final Output

### D. Multi-Agent Cycle

> Task → Agent → Tool → Result → Next Agent

These diagrams are perfect to draw during class.

---

# 4️⃣ Why Do We Need Multi-Agent Systems?

| If Only 1 Agent… | If Multiple Agents… |
|------------------|---------------------|
| Does everything | Specializes work |
| Risky | Distributed intelligence |
| Slow | Faster |
| No collaboration | Real teamwork |
| Hard to scale | Easy to extend |

Agents are like departments in a company:
- Research team  
- Writing team  
- Coding team  
- Testing team  

Today we build a **2-agent company**.

---

# 5️⃣ What is CrewAI?

CrewAI is a framework to:

- Create **agents**  
- Give them **roles + goals**  
- Assign them **tasks**  
- Make them **work together**  
- Use **tools** (search, APIs, custom functions)  

It's the easiest way for beginners to understand multi-agent systems.

---

# 6️⃣ Today’s Mini-Project  
We will build:

### 🎓 **Researcher Agent**
- Uses a search tool  
- Finds important points  
- Summarizes raw information  

### ✍️ **Writer Agent**
- Reads researcher’s notes  
- Writes friendly explanation  
- Uses simple language  

### Final Output  
A **5-paragraph beginner-friendly summary** on *any topic*.

---

# 7️⃣ Full Code (Put in `projects/day3_crewai_multiagents/app.py`)

```python
"""
Day 3 — Multi-Agent System using CrewAI
Agents:
1) Researcher → Gathers information
2) Writer → Converts research into a clean summary

One Task: Summarize any topic given by the user.
"""

import os
from dotenv import load_dotenv
import streamlit as st

from crewai import Agent, Task, Crew
from langchain.tools import DuckDuckGoSearchRun
import google.generativeai as genai

# -----------------------------
# Load API Keys
# -----------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    raise ValueError("❌ Missing GOOGLE_API_KEY in .env")

genai.configure(api_key=GOOGLE_API_KEY)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="CrewAI Multi-Agent Demo", page_icon="🤖")
st.title("🤖 CrewAI Multi-Agent System")
st.write("Give the agents a topic and let them work together!")

topic = st.text_input("Enter a topic to research (e.g., 'Blockchain', 'AI in healthcare')")
run_button = st.button("Run Agents")

# -----------------------------
# Create Tool
# -----------------------------
search_tool = DuckDuckGoSearchRun()

# -----------------------------
# Create Agents
# -----------------------------
researcher = Agent(
    role="Senior Researcher",
    goal="Find accurate information about the topic.",
    backstory=(
        "You are an expert researcher who gathers reliable, simple explanations "
        "for any topic. You break concepts into child-friendly language."
    ),
    verbose=True,
    allow_delegation=False,
    llm="gemini/gemini-flash-lite-latest",
    tools=[search_tool],
)

writer = Agent(
    role="Content Writer",
    goal="Convert research notes into a clear, friendly summary.",
    backstory=(
        "You write like a teacher explaining to a beginner. Your tone is simple, "
        "friendly, and helpful."
    ),
    verbose=True,
    allow_delegation=False,
    llm="gemini/gemini-flash-lite-latest",
)

# -----------------------------
# Run Crew
# -----------------------------
if run_button:
    if not topic.strip():
        st.error("Please enter a topic first!")
    else:
        with st.spinner("Agents are working together... 🤝"):

            # Define tasks dynamically using the user's topic
            research_task = Task(
                description=(
                    f"Research the topic: {topic}. Use the search tool "
                    "and collect 4–6 important points. "
                    "Write them as short bullet points."
                ),
                expected_output="Bullet-point research notes.",
                agent=researcher,
            )

            writing_task = Task(
                description=(
                    "Take the research notes and convert them into a final explanation "
                    "that a college student can understand. Use simple examples."
                ),
                expected_output="A friendly 5-paragraph explanation.",
                agent=writer,
            )

            crew = Crew(
                agents=[researcher, writer],
                tasks=[research_task, writing_task],
                verbose=True
            )

            result = crew.kickoff()

        st.subheader("📘 Final Summary")
        st.write(result)

        st.markdown("---")
        st.subheader("🛠️ Raw Agent Output (Debug Info)")
        st.caption("Useful if students want to see how agents talk internally.")
        st.write(result)
```

# 8️⃣ How Students Run It
```bash
pip install crewai langchain duckduckgo-search python-dotenv google-generativeai streamlit
streamlit run app.py
```

# 9️⃣ Hands-On Activity (20 mins)

### Challenge

1. Each team chooses a random topic:
   - Gaming
   - Investing
   - Fitness
   - Space tech
   - AI
   - Anime
   - History events

2. Each team runs the multi-agent system and compares:
   - Which topics were easiest?
   - Which were hardest?
   - Did researcher find enough info?
   - Did writer explain it clearly?

# 🔟 Day Summary (Simple Table)

| Concept | Explanation |
|---------|-------------|
| What is an agent? | A small worker with a goal |
| Multi-agent systems | A team of workers |
| Tools | Search, APIs |
| Tasks | Instructions for each agent |
| Crew | The whole coordinated system |

# 1️⃣1️⃣ Resume Line for Students

> Built a multi-agent AI system using CrewAI with researcher and writer agents collaborating using real web search tools.

# 1️⃣2️⃣ Homework

1. Add 3rd agent → “Fact Checker Agent”
2. Add a translation agent (English → Telugu/Hindi)
3. Add a diagram generator using ASCII art
4. Add a UI feature → “Download summary as PDF”

---
