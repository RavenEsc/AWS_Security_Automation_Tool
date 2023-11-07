# Change Log
All notable changes to this project will be documented in this file.
 
## [Unreleased] - ????-??-??
 
Testing Terraform Cloud VCS and any potential additions to testing.
 
### Added
- [Patchwork-yaml-GitActions](https://github.com/RavenEsc/AWS_Security_Automation_Tool/blob/06b6d07cf9c775ea54180cac560afee536f32108/.github/workflows/Patchwork.yml)
  Restricted from utilizing the lambda module in a Terraform VCS enviornment. GitHub Enviornment runs the Discord-Lambda-Notification package while a solution is decided.
 
<!-- ### Changed
 
### Fixed -->
 
## [1.0.0] - 2023-10-31

Initial/Finalized Commit

<center><img src="docs/Draft_3.png" alt="v1.0.0" width="100%"/></center>

## Added
- [Discord-Lambda-Notification](https://github.com/RavenEsc/AWS_Security_Automation_Tool/blob/3c857eeabac85828bfaf7105a902d4701d27ddaf/tf/3-DiscordLambdaFunction.tf)
    Terraform -- Handles notifications to Discord

- [S3-Lambda-logStorage](https://github.com/RavenEsc/AWS_Security_Automation_Tool/blob/9b8e3ae92e9274c5f87ef3ff487eff1c35b2c6dc/tf/3-S3LambdaFunction.tf)
    Terraform -- Handles JSON log storage to S3

- [SQS-Fanout](https://github.com/RavenEsc/AWS_Security_Automation_Tool/blob/b44e65336e914c4b26719e2a672aa621e42b8fa6/tf/2-FanoutResources.tf)
    Terraform -- Handles decoupling and sending the messages to storage and discord for processing.

- [Public-EC2-Check](https://github.com/RavenEsc/AWS_Security_Automation_Tool/blob/2b04deba78b880f16e681c47f1db1ee6a866696b/tf/1-EC2checkLambdaFunction.tf)
    Terraform -- Handles the Python script to check for unwanted open ports on EC2 instances.

- [IAM-Admin-Check](https://github.com/RavenEsc/AWS_Security_Automation_Tool/blob/2b04deba78b880f16e681c47f1db1ee6a866696b/tf/1-IAMcheckLambdaFunction.tf)
    Terraform -- Handles the Python Script to check for Unauthorized Admin privileges granted.

- [Daily-EventBridge-Scheduler](https://github.com/RavenEsc/AWS_Security_Automation_Tool/blob/b44e65336e914c4b26719e2a672aa621e42b8fa6/tf/1-EventBridgeLambdaTrigger.tf)
    Terraform -- Handles daily triggering the Lambda Checks