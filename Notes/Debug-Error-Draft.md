Errors->Fixes From Github:Branch:Rough-Draft:

# Corrected:

1.
    # with module.lambda_layer_discord.data.

        ## Could not locate source_path "/Discord-Webhook-Dependencies.zip".  Paths are relative to directory where `terraform plan` is being run
            ### set source_path from "\Discor.." to "Discor.."
2.
    # with module.lambda_s3.aws_lambda_event_source_mapping.
        ## "event_source_arn" must be specified
            ### Changed ".arn" to ".event_source_arn"
                ### Changed back to ".arn"
                    ### Enclosed event_source_arn with sqs = {}, doing the same to Discord-Lambda

3.
    # with module.lambda_s3.aws_lambda_event_source_mapping.
        ## "self_managed_event_source" must be specified
            ### Removed input: starting position (not neant for SQS events)