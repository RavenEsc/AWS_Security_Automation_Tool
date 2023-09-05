from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.integration import SimpleNotificationServiceSnsTopic
from diagrams.aws.integration import SimpleQueueServiceSqsQueue
from diagrams.aws.integration import Eventbridge

with Diagram("Security Automation Tool", show=False):
    with Cluster("AWS Account: Terraform-Test"):
        with Cluster("1"):
            eveb = Eventbridge("EventBridgeLambdaTrigger")
            function = Lambda("IndexLambdaFunction")
        
        with Cluster("2"):
            SNS = SimpleNotificationServiceSnsTopic("SNS")
            SQSa = SimpleQueueServiceSqsQueue("SQS Queue: S3")
            SQSb = SimpleQueueServiceSqsQueue("SQS Queue: Discord")
            
        with Cluster("3"):
            s3_bucket = S3("S3LambdaBucket")
            functionD = Lambda("DiscordLambdaFunction")
            functionS3 = Lambda("S3LambdaFunction")
            
eveb >> function >> SNS
SNS >> [SQSa, SQSb]
SQSa >> functionS3 >> s3_bucket
SQSb >> functionD
