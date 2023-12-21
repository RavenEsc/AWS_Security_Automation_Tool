module "eventbridge" {
  source = "terraform-aws-modules/eventbridge/aws"

  create_bus = false

  rules = {
    crons = {
      description         = "Trigger for a Lambda"
      schedule_expression = "rate(1 day)"
      timezone            = "America/Chicago"
    }
  }

  targets = {
      crons = [
        {
          name  = "lambda-ec2-event"
          arn   = "arn:aws:lambda:${var.reg}:${local.account_id}:function:${module.ec2lambda.lambda_function_name}"
          input = jsonencode({"job": "cron-by-rate"})
        },
        {
          name  = "lambda-iam-event"
          arn   = "arn:aws:lambda:${var.reg}:${local.account_id}:function:${module.iamlambda.lambda_function_name}"
          input = jsonencode({"job": "cron-by-rate"})
        }
      ]
    }
}