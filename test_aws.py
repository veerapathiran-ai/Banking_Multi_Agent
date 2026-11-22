
import boto3

from app.config import AWS_REGION


def test_aws_connection():

    try:
        sts = boto3.client(
            "sts",
            region_name=AWS_REGION
        )

        response = sts.get_caller_identity()

        print("AWS connection successful!")
        print("AWS Account:", response["Account"])
        print("AWS Region:", AWS_REGION)

    except Exception as error:
        print("AWS connection failed!")
        print(type(error).__name__)
        print(str(error))


if __name__ == "__main__":
    test_aws_connection()
