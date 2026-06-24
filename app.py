import streamlit as st
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from linkedin_architect.crew import LinkedinArchitect

st.set_page_config(page_title="LinkedIn Architect", page_icon="🚀", layout="wide")
# UI Styling
st.title("🚀 LinkedIn Post Architect")
st.subheader("Turn trends into professional thought-leadership.")

# Sidebar Configuration
with st.sidebar:
    st.header("Campaign Settings")
    topic = st.selectbox("Industry Topic", ["AI/ML", "Data Science", "Project Management", "Marketing", "Data Engineering", "Cloud Computing", "Cybersecurity", "Software Development", "Leadership", "Career Growth", "Finance", "Entrepreneurship"])
    frequency = st.slider("Number of Posts", 1, 5, 3)
    tone = st.select_slider(
        "Content Tone",
        options=["Educational", "Contrarian", "Supportive Mentor", "Aggressive", "Humorous"]
    )
    
    generate_btn = st.button("🚀 Generate Campaign", use_container_width=True)

# Main Execution Logic
if generate_btn:
    with st.status("Executing Agent Workflow...", expanded=True) as status:
        st.write("🔍 Researching current 2026 trends...")
        inputs = {
            'topic': topic,
            'frequency': str(frequency),
            'tone': tone
        }
        
        try:
            # Run the Crew
            result = LinkedinArchitect().crew().kickoff(inputs=inputs)
            st.session_state['last_result'] = result
            status.update(label="✅ Campaign Generated!", state="complete", expanded=False)
        except Exception as e:
            st.error(f"Error: {e}")

# Output and Saving Logic
if 'last_result' in st.session_state:
    st.markdown("### 📝 Your Generated Posts")
    content = st.session_state['last_result'].raw # Access the raw text output
    st.markdown(content)
    
    # Saving Logic
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        filename = f"linkedin_{topic.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
        if st.button(f"💾 Save to {filename}"):
            with open(filename, "w") as f:
                f.write(content)
            st.success(f"Saved to project root as {filename}")

    with col2:
        st.download_button(
            label="📥 Download as Markdown",
            data=content,
            file_name=filename,
            mime="text/markdown"
        )
