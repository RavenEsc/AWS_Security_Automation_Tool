resource "aws_sns_topic" "orders" {
  name = "orders-topic"
}

resource "aws_sqs_queue" "orders_to_process" {
  name                       = "orders-to-process-queue"
  receive_wait_time_seconds  = 20
  message_retention_seconds  = 18400
}

resource "aws_sqs_queue" "orders_to_notify" {
  name                       = "orders-to-notify-queue"
  receive_wait_time_seconds  = 20
  message_retention_seconds  = 18400
}