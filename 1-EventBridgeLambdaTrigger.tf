module "eventbridge" {
  source = "terraform-aws-modules/eventbridge/aws"

  bus_name = "Lambda_Trigger_Scheduler" # "default" bus already support schedule_expression in rules

  attach_lambda_policy = true
  lambda_target_arns   = ["arn:aws:lambda:${var.reg}:${local.account_id}:function:${module.lambda.function_name}"]

  schedules = {
    lambda-cron = {
      description         = "Trigger for a Lambda"
      schedule_expression = "rate(1 day)"
      timezone            = "America/Chicago"
      arn                 = "arn:aws:lambda:${var.reg}:${local.account_id}:function:${module.lambda.function_name}"
      input               = jsonencode({ "job" : "cron-by-rate" })
    }
  }
}