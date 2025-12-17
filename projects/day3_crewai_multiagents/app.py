"""
Day 3 — Multi-Agent System using CrewAI

Theme: "How Do Many AIs Think Together Like a Team?"

This application demonstrates a TRUE multi-agent system with THREE specialized agents:
1. Researcher Agent → Gathers and structures information
2. Writer Agent → Creates a polished summary
3. Editor Agent → Reviews and improves the content

The agents work SEQUENTIALLY - each uses the previous agent's output!
"""

import os
from dotenv import load_dotenv
import streamlit as st

from crewai import Agent, Task, Crew

# -----------------------------
# Load API Keys
# -----------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    try:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    except:
        pass

if not GOOGLE_API_KEY:
    st.error("❌ Missing GOOGLE_API_KEY. Please set it in a .env file or Streamlit secrets.")
    st.stop()

# Set the API key for CrewAI
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# CrewAI uses Gemini via string notation
LLM_MODEL = "gemini/gemini-flash-lite-latest"

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Multi-Agent Research Team",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Multi-Agent System: Research → Write → Edit")
st.markdown("""
**Theme:** *"How Do Many AIs Think Together Like a Team?"*

This demonstrates a **true multi-agent system** with THREE specialized agents working sequentially:
- 🔍 **Researcher Agent** → Gathers information
- ✍️ **Writer Agent** → Creates content
- ✏️ **Editor Agent** → Reviews and improves

They work **sequentially** - each agent uses the previous one's output!
""")

st.divider()

# User Input
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input(
        "Enter a topic to research:",
        placeholder="e.g., 'Blockchain', 'Quantum Computing', 'AI in Healthcare'",
        label_visibility="collapsed"
    )
with col2:
    run_button = st.button("🚀 Run Agents", type="primary", use_container_width=True)

# -----------------------------
# Create Three Agents
# -----------------------------
researcher = Agent(
    role="Senior Research Analyst",
    goal="Gather comprehensive, accurate information about the given topic and organize it into clear, structured bullet points.",
    backstory=(
        "You are a meticulous researcher with years of experience. "
        "You excel at breaking down complex topics into digestible, well-organized points. "
        "Your research is always fact-based, structured, and covers all important aspects of a topic."
    ),
    verbose=True,
    allow_delegation=False,
    llm=LLM_MODEL,
)

writer = Agent(
    role="Content Writer & Educator",
    goal="Transform research notes into a clear, engaging, and beginner-friendly written explanation.",
    backstory=(
        "You are a skilled writer who specializes in making complex topics accessible. "
        "You take raw research and turn it into polished, easy-to-understand content. "
        "Your writing style is friendly, clear, and uses simple examples. "
        "You excel at creating engaging narratives from structured data."
    ),
    verbose=True,
    allow_delegation=False,
    llm=LLM_MODEL,
)

editor = Agent(
    role="Content Editor & Quality Reviewer",
    goal="Review written content for clarity, accuracy, flow, and overall quality. Improve it while maintaining the original message.",
    backstory=(
        "You are an experienced editor with a keen eye for detail. "
        "You review content for grammar, clarity, logical flow, and engagement. "
        "You improve content while preserving the writer's voice and message. "
        "You ensure the final output is polished, professional, and easy to understand."
    ),
    verbose=True,
    allow_delegation=False,
    llm=LLM_MODEL,
)

# -----------------------------
# Run Multi-Agent System
# -----------------------------
if run_button:
    if not topic.strip():
        st.warning("⚠️ Please enter a topic first!")
    else:
        # Show the workflow
        st.markdown("### 🔄 Three-Agent Workflow")
        workflow_col1, workflow_col2, workflow_col3 = st.columns(3)
        
        with workflow_col1:
            st.markdown("""
            **Step 1: Researcher** 🔍
            - Analyzing: *{topic}*
            - Gathering information...
            - Structuring findings...
            """.format(topic=topic))
        
        with workflow_col2:
            st.markdown("""
            **Step 2: Writer** ✍️
            - Receiving research notes...
            - Writing content...
            - Creating narrative...
            """)
        
        with workflow_col3:
            st.markdown("""
            **Step 3: Editor** ✏️
            - Reviewing content...
            - Improving clarity...
            - Polishing final draft...
            """)
        
        st.divider()
        
        # Execute the crew
        with st.spinner("🤝 Three agents are collaborating... This may take 60-90 seconds."):
            try:
                # Task 1: Research
                research_task = Task(
                    description=(
                        f"Research the topic: '{topic}'. "
                        "Break down the topic into 6-8 key points covering all important aspects. "
                        "Each point should be a clear, concise bullet point with brief explanations. "
                        "Focus on accuracy, completeness, and logical organization."
                    ),
                    expected_output="A structured list of 6-8 bullet points with brief explanations covering all important aspects of the topic.",
                    agent=researcher,
                )

                # Task 2: Writing (depends on research_task output)
                writing_task = Task(
                    description=(
                        "Using the research notes provided by the Researcher, "
                        "write a comprehensive, beginner-friendly explanation of the topic. "
                        "The explanation should be 5-6 paragraphs long. "
                        "Use simple language, include examples where helpful, and make it engaging. "
                        "Write for a college student audience."
                    ),
                    expected_output="A polished 5-6 paragraph explanation that is clear, engaging, and educational.",
                    agent=writer,
                )

                # Task 3: Editing (depends on writing_task output)
                editing_task = Task(
                    description=(
                        "Review the content written by the Writer. "
                        "Check for clarity, flow, grammar, and overall quality. "
                        "Improve the content while maintaining the writer's voice and message. "
                        "Ensure it's polished, professional, and easy to understand. "
                        "Make any necessary improvements and provide the final version."
                    ),
                    expected_output="A polished, edited version of the content that is clear, well-structured, and professional.",
                    agent=editor,
                )

                # Create and run the crew
                crew = Crew(
                    agents=[researcher, writer, editor],
                    tasks=[research_task, writing_task, editing_task],
                    verbose=True,
                )

                result = crew.kickoff()

                # Display Results - Structured Output
                st.success("✅ Three-Agent System Completed Successfully!")
                
                # Extract result text (handle both string and object results)
                if hasattr(result, 'raw'):
                    result_text = result.raw
                elif isinstance(result, str):
                    result_text = result
                else:
                    result_text = str(result)
                
                # Structured Display
                st.markdown("---")
                st.markdown("## 📊 Multi-Agent Output")
                
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📘 Final Content", "🔍 Agent Workflow", "📋 Raw Output"])
                
                with tab1:
                    st.markdown("### ✏️ Final Edited Content")
                    
                    # Topic header with styling
                    st.markdown(f"""
                    <div style="background-color: #1e3a5f; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                        <h4 style="color: white; margin: 0;">📌 Topic: <span style="color: #4CAF50;">{topic}</span></h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display formatted content in a nice container
                    st.markdown("""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #4CAF50;">
                    """, unsafe_allow_html=True)
                    st.markdown(result_text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # Action buttons
                    col_dl, col_copy = st.columns([1, 1])
                    with col_dl:
                        st.download_button(
                            label="📥 Download as TXT",
                            data=result_text,
                            file_name=f"{topic.replace(' ', '_')}_content.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col_copy:
                        if st.button("📋 Copy to Clipboard", use_container_width=True):
                            st.code(result_text, language=None)
                            st.success("Content displayed above - select and copy!")
                
                with tab2:
                    st.markdown("### 🔄 Agent Collaboration Flow")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("""
                        #### 🔍 Researcher Agent
                        **Role:** Research Analyst
                        
                        **Task:** Gather and structure information
                        
                        **Output:** Organized bullet points
                        
                        ✅ **Completed**
                        """)
                    
                    with col2:
                        st.markdown("""
                        #### ✍️ Writer Agent
                        **Role:** Content Writer
                        
                        **Task:** Transform research into content
                        
                        **Output:** Draft explanation
                        
                        ✅ **Completed**
                        """)
                    
                    with col3:
                        st.markdown("""
                        #### ✏️ Editor Agent
                        **Role:** Content Editor
                        
                        **Task:** Review and improve content
                        
                        **Output:** Final polished version
                        
                        ✅ **Completed**
                        """)
                    
                    st.markdown("---")
                    st.markdown("""
                    **Workflow Summary:**
                    1. Researcher gathered information about **{topic}**
                    2. Writer created a comprehensive explanation
                    3. Editor polished and improved the final content
                    
                    **Result:** A high-quality, well-structured explanation ready for use!
                    """.format(topic=topic))
                
                with tab3:
                    st.markdown("### 📋 Raw Output (For Debugging)")
                    st.code(result_text, language="markdown")
                    
                    # Show result type info
                    st.info(f"**Result Type:** {type(result).__name__}")
                
                st.markdown("---")
                
                # Show what happened
                with st.expander("🔍 How Did the Three Agents Collaborate?"):
                    st.markdown("""
                    **This is a TRUE multi-agent system because:**
                    
                    1. **Three Distinct Agents:**
                       - **Researcher** has its own role, goal, and expertise
                       - **Writer** has a different role focused on content creation
                       - **Editor** has a different role focused on quality review
                    
                    2. **Sequential Collaboration:**
                       - Researcher completes Task 1 → produces research notes
                       - Writer receives Researcher's output → creates written content
                       - Editor receives Writer's output → improves and polishes
                    
                    3. **Specialization:**
                       - Each agent is optimized for its specific job
                       - Together they produce better results than any single agent alone
                    
                    4. **True Multi-Agent Workflow:**
                       - Each agent's output becomes the next agent's input
                       - This creates a pipeline: Research → Write → Edit
                    
                    **This demonstrates the power of multi-agent systems!** 🚀
                    """)
                    
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.info("💡 Tip: Make sure your GOOGLE_API_KEY is valid and you have internet connection.")

# -----------------------------
# Sidebar: Educational Info
# -----------------------------
with st.sidebar:
    st.header("📚 About Multi-Agent Systems")
    st.markdown("""
    **What makes this a multi-agent system?**
    
    ✅ **Multiple Agents:** Three specialized AI agents
    
    ✅ **Sequential Collaboration:** Each agent uses the previous one's output
    
    ✅ **Specialization:** Each agent has a unique role and expertise
    
    ✅ **Coordination:** CrewAI orchestrates their workflow
    
    **Key Concept:** 
    Multi-agent systems are like a production line where each worker has a specific job, and they collaborate to create a final product.
    """)
    
    st.divider()
    
    st.markdown("""
    **Agent 1: Researcher** 🔍
    - Role: Research Analyst
    - Job: Gather and structure information
    - Output: Organized bullet points
    
    **Agent 2: Writer** ✍️
    - Role: Content Writer
    - Job: Transform research into written content
    - Output: Draft explanation
    
    **Agent 3: Editor** ✏️
    - Role: Content Editor
    - Job: Review and improve content
    - Output: Final polished version
    
    **Together:** They create better results than any single agent could alone!
    """)
