module "ec2_was_cluster" {
  source                 = "../modules/terraform-aws-ec2-instance"
  appinstall             = true
  name                   = "jjh-was"
  instance_count         = 1
  ami                    = "ami-0bea7fd38fabe821a"
  instance_type          = "t2.micro"
  key_name               = "jaehoon-test1"
  vpc_security_group_ids = [module.was_sg.this_security_group_id]
  subnet_ids              = module.vpc.private_subnets

  connection {
	bastion_host = module.bastion.host_id
        bastion_user = "ec2-user"
	type = "ssh"
	bastion_host_key = file("/home/ec2-user/.ssh/jaehoon-test1.pem")
	bastion_private_key = file("/home/ec2-user/.ssh/jaehoon-test1.pem")
	timeout = "2m"
}

  tags = {
    System   = "jjhtest"
  }
}

