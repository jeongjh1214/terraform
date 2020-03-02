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

