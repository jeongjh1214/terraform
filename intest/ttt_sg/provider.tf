provider "aws" {
  region                  = "ap-northeast-2"
  shared_credentials_file = "/home/ec2-user/.aws/credentials"
  profile                 = "mfa"
}

