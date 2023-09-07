from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.integration import SimpleNotificationServiceSnsTopic
from diagrams.aws.integration import SimpleQueueServiceSqsQueue
from diagrams.aws.integration import Eventbridge
from diagrams.onprem.compute import Server

with Diagram("Security Automation Tool", show=False):

    with Cluster("AWS-Account: Terraform-Test"):

        SNS = SimpleNotificationServiceSnsTopic("SNS")
        SQSa = SimpleQueueServiceSqsQueue("SQS Queue: S3")
        SQSb = SimpleQueueServiceSqsQueue("SQS Queue: Dcord")
        SNS >> [SQSa, SQSb]

        with Cluster("Trigger-Lambda"):
            eveb = Eventbridge("EventBLambTrigger")
            function = Lambda("IndexLambFunction")
            eveb >> function >> SNS

        with Cluster("S3-Discord-Functions"):
            s3_bucket = S3("S3LambBucket")
            functionD = Lambda("DcordLambFunction")
            functionS3 = Lambda("S3LambFunction")
            Discord = Server("DcordNotifiBot")
            SQSa >> functionS3 >> s3_bucket
            SQSb >> functionD >> Discord