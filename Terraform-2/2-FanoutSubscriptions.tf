resource "aws_sns_topic_subscription" "orders_to_process_subscription" {
  protocol             = "sqs"
  raw_message_delivery = true
  topic_arn            = aws_sns_topic.orders.arn
  endpoint             = aws_sqs_queue.orders_to_process.arn
}

resource "aws_sns_topic_subscription" "orders_to_notify_subscription" {
  protocol             = "sqs"
  raw_message_delivery = true
  topic_arn            = aws_sns_topic.orders.arn
  endpoint             = aws_sqs_queue.orders_to_notify.arn
}