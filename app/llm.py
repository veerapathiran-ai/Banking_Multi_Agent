
from langchain_aws import ChatBedrockConverse
from app.config import AWS_REGION, BEDROCK_MODEL_ID
import os

if os.getenv("AWS_BEARER_TOKEN_BEDROCK"):
    raise RuntimeError(
        "Remove AWS_BEARER_TOKEN_BEDROCK. "
        "This application uses IAM credentials."
    )

llm = ChatBedrockConverse(
    model=BEDROCK_MODEL_ID,
    region_name=AWS_REGION,
    temperature=0.2,
    max_tokens=1024
)


def invoke_llm(question: str):
    response = llm.invoke(question)
    return response.content


if __name__ == "__main__":
    print("Testing AWS Bedrock IAM connection...")

    response = llm.invoke(
        "Explain the importance of banking security."
    )

    print("\nBedrock Response:")
    print(response.content)
