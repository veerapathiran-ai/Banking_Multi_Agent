
from app.llm import llm

try:

    response = llm.invoke(
        "Introduce yourself as a banking AI assistant."
    )

    print("SUCCESS: AWS BEDROCK CONNECTED")
    print("\nResponse:")
    print(response.content)

except Exception as error:

    print("BEDROCK CONNECTION FAILED")
    print(type(error).__name__)
    print(str(error))
