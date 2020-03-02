module "bastion_sg" {
  source = "../modules/terraform-aws-security-group"

  name        = "jjhtest-bastion"
  description = "Security group for bastion"
  vpc_id      = module.vpc.vpc_id

  # 15.165.104.130 = 테스트서버 아이피, 106.101.0.0/16 = 개인아이피

  ingress_cidr_blocks      = ["15.165.104.130/32","106.101.0.0/16"]
  ingress_rules            = ["ssh-tcp"]
  
  egress_cidr_blocks      = ["0.0.0.0/0"]
  egress_rules            = ["all-all"]
}
