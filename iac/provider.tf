terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.84.0"
    }
  }

  backend "s3" {
    bucket = "<nombre_bucket>"
    key    = "<path>"
    region = "<region>"
  }
}

