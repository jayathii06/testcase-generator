import streamlit as st
import requests

st.set_page_config(page_title="AI Test Case Generator", layout="wide")

st.title("🧪 AI Test Case Generator")
st.caption("Paste a Java method → get JUnit test cases + complexity analysis, powered by a local Qwen2.5 model.")

BACKEND_URL = "http://localhost:8000/generate-tests"

default_code = """public int add(int a, int b) {
    return a + b;
}"""

java_code = st.text_area("Paste your Java method:", value=default_code, height=200)

if st.button("Generate Test Cases", type="primary"):
    if not java_code.strip():
        st.warning("Please paste a Java method first.")
    else:
        with st.spinner("Qwen is analyzing your code..."):
            try:
                response = requests.post(BACKEND_URL, json={"java_code": java_code}, timeout=120)
                result = response.json()

                if "error" in result:
                    st.error(result.get("error"))
                    if "raw_output" in result:
                        st.code(result["raw_output"])
                else:
                    st.subheader("📋 Method Summary")
                    st.write(result.get("method_summary", "N/A"))

                    st.subheader("✅ Test Cases")
                    for i, tc in enumerate(result.get("test_cases", []), 1):
                        with st.expander(f"{i}. {tc.get('name', 'Test case')} — [{tc.get('category', '')}]"):
                            st.write(f"**Input:** {tc.get('input', '')}")
                            st.write(f"**Expected Output:** {tc.get('expected_output', '')}")
                            st.code(tc.get("junit_code", ""), language="java")

                    st.subheader("⏱ Complexity Analysis")
                    complexity = result.get("complexity", {})
                    col1, col2 = st.columns(2)
                    col1.metric("Time Complexity", complexity.get("time", "N/A"))
                    col2.metric("Space Complexity", complexity.get("space", "N/A"))
                    st.write(complexity.get("explanation", ""))

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend. Make sure FastAPI server is running on port 8000.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
