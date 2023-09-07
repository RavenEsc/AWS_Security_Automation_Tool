Errors->Fixes From Github:Branch:Rough-Draft:

# Corrected 1:

1.
    # with module.lambda_layer_discord.data.

        ## Could not locate source_path "/Discord-Webhook-Dependencies.zip".  Paths are relative to directory where `terraform plan` is being run

            ### set source_path from "\Discor.." to "Discor.."
2.
    # with module.lambda_s3.aws_lambda_event_source_mapping.
        ## "event_source_arn" must be specified
            ### Changed ".arn" to ".event_source_arn"
                Corrected 2:
                    # on 3-S3LambdaFunction.tf line 29, in module "lambda_s3" (Also on Discord_lambda)
                        ## This object has no argument, nested block, or exported attribute named "event_source_arn".
                            ### Changed back to ".arn"

3.
    # with module.lambda_s3.aws_lambda_event_source_mapping.
        ## "self_managed_event_source" must be specified
            ### Removed input: starting position (not neant for SQS
            events)