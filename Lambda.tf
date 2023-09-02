# module "lambda_function" {
#   source = "terraform-aws-modules/lambda/aws"

#   function_name = "lambda-sat-ec2"
#   description   = "Checks for public facing ec2 instances"
#   handler       = "index.lambda_handler"
#   runtime       = "python3.8"

#   source_path = "/python_lambda.py"

#   tags = {
#     Name = "my-lambda1"
#   }
# }