module "alb_pub" {
  source  = "../modules/terraform-aws-alb"

  name = "jjh-alb"

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

  target_id = flatten([module.ec2_was_cluster.id])

  tags = {
    "System" = "jjhtest"
  }
}
