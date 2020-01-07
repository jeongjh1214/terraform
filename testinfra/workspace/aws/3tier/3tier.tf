# module키워드를 사용해서 vpc module을 정의한다.
module "vpc" {
  # source는 variables.tf, main.tf, outputs.tf 파일이 위치한 디렉터리 경로를 넣어준다.
  source = "../../../modules/aws/vpc"

  # VPC이름을 넣어준다. 이 값은 VPC module이 생성하는 모든 리소스 이름의 prefix가 된다.
  name = "test"
  # VPC의 CIDR block을 정의한다.
  cidr = "10.1.0.0/16"

  # VPC가 사용할 AZ를 정의한다.
  azs              = ["eu-west-3a", "eu-west-3b"]
  # VPC의 Public Subnet CIDR block을 정의한다.
  public_subnets   = ["10.1.0.0/24", "10.1.1.0/24"]
  # VPC의 Private Subnet CIDR block을 정의한다.
  private_subnets  = ["10.1.2.0/24", "10.1.3.0/24"]
  # VPC의 Private DB Subnet CIDR block을 정의한다. (RDS를 사용하지 않으면 이 라인은 필요없다.)
  database_subnets = ["10.1.4.0/24", "10.1.5.0/24"]

  # VPC module이 생성하는 모든 리소스에 기본으로 입력될 Tag를 정의한다.
  tags = {
    "TerraformManaged" = "true"
  }
}
	
