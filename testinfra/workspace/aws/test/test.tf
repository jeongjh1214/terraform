locals { 
  azs              = ["eu-west-3a", "eu-west-3b"]
  public_subnets   = ["10.1.0.0/24", "10.1.1.0/24"]
}

# module키워드를 사용해서 vpc module을 정의한다.
module "vpc" {
  # source는 variables.tf, main.tf, outputs.tf 파일이 위치한 디렉터리 경로를 넣어준다.
  source = "../../../modules/aws/vpc"

  # VPC이름을 넣어준다. 이 값은 VPC module이 생성하는 모든 리소스 이름의 prefix가 된다.
  name = "test"
  # VPC의 CIDR block을 정의한다.
  cidr = "10.1.0.0/16"

  # VPC가 사용할 AZ를 정의한다.
  azs              = local.azs
  # VPC의 Public Subnet CIDR block을 정의한다.
  public_subnets   = local.public_subnets
  # VPC의 Private Subnet CIDR block을 정의한다.
  private_subnets  = ["10.1.2.0/24", "10.1.3.0/24"]
  # VPC의 Private DB Subnet CIDR block을 정의한다. (RDS를 사용하지 않으면 이 라인은 필요없다.)
  database_subnets = ["10.1.4.0/24", "10.1.5.0/24"]

  # VPC module이 생성하는 모든 리소스에 기본으로 입력될 Tag를 정의한다.
  tags = {
    "TerraformManaged" = "true"
  }
}

# module 키워드를 사용해서 vpc ec2을 정의한다.
module "ec2_test" {
  # source는 variables.tf, main.tf, outputs.tf 파일이 위치한 디렉터리 경로를 넣어준다.
  source = "../../../modules/aws/ec2"

  # VPC이름을 넣어준다. 이 값은 ec2 module이 생성하는 모든 리소스 이름의 prefix가 된다.
  name   = "webec2_test"
  # module.vpc에서 생성된 vpc_id가 입력된다.
  vpc_id = module.vpc.vpc_id

  # ec2 생성 개수
  ec2_count = 2

  # 최신 버전의 amazon_linux AMI id가 입력된다.
  ami                 = data.aws_ami.amazon_linux.id
  # ec2을 생성할 AZ을 정의한다.
  azs                 = local.azs
  # ec2을 생성할 subnet id를 정의한다.
  subnet_ids          = flatten([module.vpc.public_subnets_ids])
  # ec2에서 inbound 허용할 정책 
  ingress_from_ports  = 80
  ingress_to_ports    = 80
  ingress_protocol    = "tcp"
  ingress_cidr_blocks = ["0.0.0.0/0"]
  # ec2에서 inbound 허용할 정책 
  egress_from_ports  = 0
  egress_to_ports    = 0
  egress_protocol    = "-1"
  egress_cidr_blocks = ["0.0.0.0/0"] 
  # ec2 SSH 접속에 사용할 keypair_name을 var.keypair_name의 값으로 정의한다.
  keypair_name        = var.keypair_name

  # ec2 module이 생성하는 모든 리소스에 기본으로 입력될 Tag를 정의한다.
  tags = {
    "TerraformManaged" = "true"
  }
}
