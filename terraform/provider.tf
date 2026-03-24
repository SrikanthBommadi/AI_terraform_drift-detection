terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "reddy.tf"
    key            = "Drift-Detection"
    region         = "us-east-1"
   # dynamodb_table = "terraform-locks"   # optional but recommended
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project = var.project_name
    }
  }
}
