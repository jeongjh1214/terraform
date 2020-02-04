locals { 
  azs              = ["ap-northeast-2a", "ap-northeast-2c"]
}

module "vpc" {
  source = "../modules/terraform-aws-vpc/"

  name = "jjhtest"
  cidr = "10.3.0.0/16"

  azs              = local.azs
  public_subnets   = ["10.3.0.0/24", "10.3.1.0/24"] 
  private_subnets  = ["10.3.2.0/24", "10.3.3.0/24"]
  database_subnets = ["10.3.4.0/24", "10.3.5.0/24"]

  tags = {
    "System" = "jjhtest"
  }
}