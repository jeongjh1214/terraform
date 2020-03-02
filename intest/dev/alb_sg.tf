module "alb_pub_sg" {
  source = "../modules/terraform-aws-security-group"

  name        = "jjhtest-alb"
  description = "Security group for alb"
  vpc_id      = module.vpc.vpc_id

  ingress_cidr_blocks      = ["0.0.0.0/0"]
  ingress_rules            = ["http-80-tcp"]
}
