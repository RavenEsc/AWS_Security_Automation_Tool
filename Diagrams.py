from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.integration import SimpleNotificationServiceSnsTopic
from diagrams.aws.integration import SimpleQueueServiceSqsQueue
from diagrams.aws.integration import Eventbridge

with Diagram("Security Check Solution", show=False):
    with Cluster("AWS Account: Terraform-Test"):
        # Note: Do not make a variable name below matching the above imports ex. S3 and S3 instead of s3_bucket
        function = Lambda("SNS Topic Function")
        functionD = Lambda("Discord Webhook Function")
        functionS3 = Lambda("S3 Storage Function")
        SNS = SimpleNotificationServiceSnsTopic("SNS")
        SQSa = SimpleQueueServiceSqsQueue("SQS Queue")
        SQSb = SimpleQueueServiceSqsQueue("SQS Queue: Discord")
        s3_bucket = S3("S3 Bucket")
        eveb = Eventbridge("Scheduler")

    eveb >> function >> SNS
    SNS >> [SQSa, SQSb]
    SQSa >> functionS3 >> s3_bucket
    SQSb >> functionD