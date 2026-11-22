
from app.llm import invoke_llm

response = invoke_llm(
    "What is fraud detection in banking?"
)

print("\nAWS BEDROCK RESPONSE:")
print(response)
