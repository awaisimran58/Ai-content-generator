import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.caption("Create ready-to-publish social media content with Groq AI.")

# Get API key from Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    st.warning("GROQ_API_KEY is not configured. Add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = Groq(api_key=api_key)

content_type = st.selectbox(
    "Content Type",
    ["Social Media Post", "LinkedIn Post", "Instagram Caption", "Facebook Post",
     "X/Twitter Post", "Promotional Post"]
)

platform = st.selectbox(
    "Platform",
    ["LinkedIn", "Instagram", "Facebook", "X/Twitter", "General"]
)

topic = st.text_area(
    "Topic",
    placeholder="Example: Benefits of smart electricity meters",
    height=100
)

target_audience = st.text_input(
    "Target Audience",
    placeholder="Example: Energy professionals and utility customers"
)

tone = st.selectbox(
    "Tone",
    ["Professional", "Friendly", "Educational", "Persuasive",
     "Inspirational", "Casual", "Technical"]
)

generate = st.button("🚀 Generate Content", type="primary", use_container_width=True)

if generate:
    if not topic.strip():
        st.error("Please enter a topic.")
        st.stop()

    if not target_audience.strip():
        st.error("Please enter the target audience.")
        st.stop()

    prompt = f"""
You are an expert social media content writer.

Create a complete, ready-to-publish piece of content using these requirements:

Content type: {content_type}
Platform: {platform}
Topic: {topic}
Target audience: {target_audience}
Tone: {tone}

Return the result in exactly this structure:

TITLE:
A short, engaging title.

POST:
Write the complete post/caption. Make it clear, useful and engaging.
Adapt the length and style to the selected platform.

CALL TO ACTION:
A natural call to action.

HASHTAGS:
Provide 8-12 relevant hashtags. Do not use irrelevant or spammy hashtags.

Do not explain your process. Return only the requested content.
"""

    try:
        with st.spinner("Creating your content..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional content creation assistant."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1200,
            )

        result = response.choices[0].message.content

        st.success("Content generated successfully!")
        st.subheader("Your Content")
        st.text_area("Copy your content", result, height=500)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
        st.info("Check that your Groq API key is correct and that the selected model is available.")
