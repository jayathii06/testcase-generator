def build_test_gen_prompt(java_code: str) -> str:
    return f"""You are a Java testing expert. Analyze the following Java method and generate JUnit test cases.

Java method:
```
{java_code}
```

Respond with ONLY a valid JSON object, no other text, no markdown, no explanation outside the JSON. Use this exact structure:

{{
  "method_summary": "one line description of what the method does",
  "test_cases": [
    {{
      "name": "descriptive test name",
      "category": "normal | edge | boundary",
      "input": "example input values as a plain string, e.g. a=5, b=3",
      "expected_output": "expected result",
      "junit_code": "a single @Test method as a string"
    }}
  ],
  "complexity": {{
    "time": "Big-O notation",
    "space": "Big-O notation",
    "explanation": "one short sentence why"
  }}
}}

Generate at least 4 test cases covering normal, edge, and boundary scenarios. Output ONLY the JSON object, nothing else.
"""
