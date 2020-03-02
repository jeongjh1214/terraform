module "was_sg" {
  source = "../modules/terraform-aws-security-group"
  
  name        = "jjhtest-was"
  description = "Security group for was"
  vpc_id = module.vpc.vpc_id

  computed_ingress_with_source_security_group_id = [
    {
      rule                     = "http-8080-tcp"
      source_security_group_id = "${module.alb_pub_sg.this_security_group_id}"
    },
    {
      rule                     = "ssh-tcp"
      source_security_group_id = "${module.bastion_sg.this_security_group_id}"
    }
  ]
  number_of_computed_ingress_with_source_security_group_id = 2
}
