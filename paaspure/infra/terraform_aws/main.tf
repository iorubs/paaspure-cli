variable "stack_name" {}
variable "region" {}
variable "parameters" { type = "map" }

## Infrastructure
provider "aws" {
  region = "${var.region}"
}

resource "aws_cloudformation_stack" "paaspure_infra" {
  name = "${var.stack_name}"

  parameters = "${var.parameters}"

  capabilities = ["CAPABILITY_IAM"]

  template_url = "https://editions-us-east-1.s3.amazonaws.com/aws/stable/Docker.tmpl"
}
