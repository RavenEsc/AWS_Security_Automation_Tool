terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  cloud {
    organization = var.org

    workspaces {
      name = var.ws
    }
  }
}


provider "aws" {
  region  = var.reg
}