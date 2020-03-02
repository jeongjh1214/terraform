module "bastion" {
  source                 = "../modules/terraform-aws-ec2-instance"
  name                   = "jjh-bastion"
  instance_count         = 1
  # ami-0185fd13b4270de70 = nat instance , ami-0bea7fd38fabe821a = amazon2
  ami                    = "ami-0bea7fd38fabe821a"
  instance_type          = "t2.micro"
  key_name               = "jaehoon-test1"
  vpc_security_group_ids = [module.bastion_sg.this_security_group_id]
  subnet_ids              = module.vpc.public_subnets
  tags = {
    System   = "jjhtest"
  }
}
