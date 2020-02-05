module "sg" {
  source = "../modules/terraform-aws-security-group"

  name        = "jjhtesttf"
  description = "Security group for user-service with custom ports open within VPC, and PostgreSQL publicly open"
  vpc_id      = "vpc-41a3742a"

  ingress_cidr_blocks      = ["0.0.0.0/0"]
  ingress_rules            = ["https-443-tcp","http-80-tcp"]
}

module "abc" {
  source = "../modules/terraform-aws-security-group"
  name        = "jjhtesttf"
  vpc_id = "vpc-41a3742a"

  computed_ingress_with_source_security_group_id = [
    {
      rule                     = "http-8080-tcp"
      source_security_group_id = "${module.sg.this_security_group_id}"
    }
  ]
  number_of_computed_ingress_with_source_security_group_id = 1
}