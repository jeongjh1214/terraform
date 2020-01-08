locals { 
  azs              = ["eu-west-3a", "eu-west-3b"]
}

module "vpc" {
  source = "../../../modules/aws/vpc"

  name = "test"
  cidr = "10.1.0.0/16"

  azs              = local.azs
  public_subnets   = ["10.1.0.0/24", "10.1.1.0/24"] 
  private_subnets  = ["10.1.2.0/24", "10.1.3.0/24"]
  database_subnets = ["10.1.4.0/24", "10.1.5.0/24"]

  tags = {
    "TerraformManaged" = "true"
  }
}

module "ec2_test" {
  source = "../../../modules/aws/ec2"

  name   = "webec2_test"
  vpc_id = module.vpc.vpc_id

  ec2_count = 2

  ami                 = data.aws_ami.amazon_linux.id
  azs                 = local.azs
  subnet_ids          = flatten([module.vpc.public_subnets_ids])
  
  ingress_from_ports  = 80
  ingress_to_ports    = 80
  ingress_protocol    = "tcp"
  ingress_cidr_blocks = ["0.0.0.0/0"]
  
  egress_from_ports  = 0
  egress_to_ports    = 0
  egress_protocol    = "-1"
  egress_cidr_blocks = ["0.0.0.0/0"] 
  
  keypair_name       = var.keypair_name

  tags = {
    "TerraformManaged" = "true"
  }
}

module "ec2_test_pri" {
  source = "../../../modules/aws/ec2"

  name   = "wasec2_test"
  vpc_id = module.vpc.vpc_id

  ec2_count = 2

  ami                 = data.aws_ami.amazon_linux.id
  azs                 = local.azs
  subnet_ids          = flatten([module.vpc.private_subnets_ids])
  
  ingress_from_ports  = 80
  ingress_to_ports    = 80
  ingress_protocol    = "tcp"
  ingress_cidr_blocks = ["0.0.0.0/0"]
  
  egress_from_ports  = 0
  egress_to_ports    = 0
  egress_protocol    = "-1"
  egress_cidr_blocks = ["0.0.0.0/0"] 
  
  keypair_name       = var.keypair_name

  tags = {
    "TerraformManaged" = "true"
  }
}

module "alb" {
  source  = "../../../modules/aws/elb"
  
  name = "my-alb"

  load_balancer_type = "application"

  vpc_id             = module.vpc.vpc_id 
  subnets            = flatten([module.vpc.public_subnets_ids]) 
  security_groups    = module.ec2_test.ec2_sg_id
 

  access_logs = {
    bucket = "my-alb-logs"
  }

  target_groups = [
    {
      name_prefix      = "default"
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
    "TerraformManaged" = "true"
  }
}

module "mysql_test" {
  source  = "../../../modules/aws/db"

  identifier = "mysqltest"

  engine            = "mysql"
  engine_version    = "5.7.19"
  instance_class    = "db.t2.large"
  allocated_storage = 5

  name     = "demodb"
  username = "user"
  password = "Bespin1!"
  port     = "3306"

  iam_database_authentication_enabled = true

  vpc_security_group_ids = [module.vpc.default_security_group_id]

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"

  # Enhanced Monitoring - see example for details on how to create the role
  # by yourself, in case you don't want to create it automatically
  monitoring_interval = "30"
  monitoring_role_name = "MyRDSMonitoringRole"
  create_monitoring_role = true

  tags = {
    Owner       = "user"
    Environment = "dev"
  }

  # DB subnet group
  subnet_ids = flatten([module.vpc.database_subnets_ids])

  # DB parameter group
  family = "mysql5.7"

  # DB option group
  major_engine_version = "5.7"

  # Snapshot name upon DB deletion
  final_snapshot_identifier = "demodb"

  # Database Deletion Protection
  deletion_protection = false	 

  parameters = [
    {
      name = "character_set_client"
      value = "utf8"
    },
    {
      name = "character_set_server"
      value = "utf8"
    }
  ]

  options = [
    {
      option_name = "MARIADB_AUDIT_PLUGIN"

      option_settings = [
        {
          name  = "SERVER_AUDIT_EVENTS"
          value = "CONNECT"
        },
        {
          name  = "SERVER_AUDIT_FILE_ROTATIONS"
          value = "37"
        },
      ]
    },
  ]
}
