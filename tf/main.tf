terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.79.0"
    }
    docker = {
      source = "kreuzwerker/docker"
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