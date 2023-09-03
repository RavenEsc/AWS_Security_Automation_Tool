variable "org" {
  type = string
  default = "raven-for-aws"
}

variable "ws" {
  type = string
  default = "AWS_SAT"
}

variable "reg" {
  type = string
  default = "us-east-1"
}

data "aws_caller_identity" "current" {}

locals {
    account_id = data.aws_caller_identity.current.account_id
}

variable "sns_topic_arn" {
  default = aws_sns_topic.orders.arn
}

variable "s3_bucket_name" {
  type = string
  default = "SAT-Event-Storage"
}

variable "py_runtime" {
  type = string
  default = "python3.10"
}