terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.18.0"
    }
  }
  cloud {
    organization = "raven-for-aws"

    workspaces {
      name = "AWS_SAT"
    }
  }
}


provider "aws" {
  region  = var.reg
}