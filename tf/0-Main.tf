terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.18.1"
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