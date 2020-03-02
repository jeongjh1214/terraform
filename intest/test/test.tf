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

module "alb_pub_sg" {
  source = "../modules/terraform-aws-security-group"

  name        = "jjhtest-alb"
  description = "Security group for alb"
  vpc_id      = module.vpc.vpc_id

  ingress_cidr_blocks      = ["0.0.0.0/0"]
  ingress_rules            = ["https-443-tcp","http-80-tcp"]
}

module "was_sg" {
  source = "../modules/terraform-aws-security-group"
  
  name        = "jjhtest-aws"
  description = "Security group for was"
  vpc_id = module.vpc.vpc_id

  computed_ingress_with_source_security_group_id = [
    {
      rule                     = "http-8080-tcp"
      source_security_group_id = "${module.alb_pub_sg.this_security_group_id}"
    },
    {
      rule                     = "ssh-tcp"
      source_security_group_id = "${module.alb_pub_sg.this_security_group_id}"
    }
  ]
  number_of_computed_ingress_with_source_security_group_id = 1
}

module "ec2_was_cluster" {
  source                 = "../modules/terraform-aws-ec2-instance"
  name                   = "jjh-was"
  instance_count         = 2
  ami                    = "ami-0bea7fd38fabe821a"
  instance_type          = "t2.micro"
  key_name               = "jaehoon-test1"
  vpc_security_group_ids = [module.was_sg.this_security_group_id]
  subnet_ids              = module.vpc.private_subnets
  tags = {
    System   = "jjhtest"
  }
}

module "alb_pub" {
  source  = "../modules/terraform-aws-alb"

  name = "jjhalb"

  load_balancer_type = "application"

  vpc_id             = module.vpc.vpc_id
  subnets            = module.vpc.public_subnets
  security_groups    = [module.alb_pub_sg.this_security_group_id]

  target_groups = [
    {
      name_prefix      = "test"
      backend_protocol = "HTTP"
      backend_port     = 80
      target_type      = "instance"
    }
  ]

  http_tcp_listeners = [
    {
      port               = 80
      protocol           = "HTTP"
      target_group_index = 0
    }
  ]

  tags = {
    "System" = "jjhtest"
  }
}
