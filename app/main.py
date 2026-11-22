
import boto3
import re

from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File
)

from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from app.config import (
    AWS_REGION,
    S3_BUCKET_NAME,
    UPLOAD_DIR
)

from workflow.banking_graph import banking_graph


app = FastAPI(
    title="Banking Multi-Agent AI System",
    version="1.0"
)


class ChatRequest(BaseModel):
    question: str


s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
)


@app.get("/health")
def health():

    return {
        "status": "running",
        "application": "Banking Multi-Agent AI",
        "bedrock_model": "Configured",
        "s3_bucket": S3_BUCKET_NAME or "Not configured"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        result = banking_graph.invoke({
            "messages": [
                HumanMessage(content=request.question)
            ]
        })

        answer = result["messages"][-1].content

        return {
            "question": request.question,
            "answer": answer,
            "agent": result.get(
                "agent_used", "Unknown Agent"
            )
        }

    except Exception as error:

        print("Chat error:", repr(error))

        raise HTTPException(
            status_code=500,
            detail="Banking AI processing failed. Check backend logs."
        )


@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".pdf",
        ".txt",
        ".docx"
    }

    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, TXT and DOCX files are supported."
        )

    safe_name = re.sub(
        r"[^a-zA-Z0-9._-]",
        "_",
        filename
    )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Maximum file size is 10 MB."
        )

    local_path = UPLOAD_DIR / safe_name

    try:

        if not S3_BUCKET_NAME:
            raise RuntimeError(
                "S3_BUCKET_NAME is missing in .env"
            )

        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"banking-documents/{safe_name}",
            Body=content
        )

        local_path.write_bytes(content)

        return {
            "status": "success",
            "filename": safe_name,
            "s3_bucket": S3_BUCKET_NAME,
            "s3_key": f"banking-documents/{safe_name}",
            "message": "Uploaded to S3 and saved for Python retrieval."
        }

    except Exception as error:

        print("Upload error:", repr(error))

        raise HTTPException(
            status_code=500,
            detail="Document upload failed. Check S3 permissions and backend logs."
        )
