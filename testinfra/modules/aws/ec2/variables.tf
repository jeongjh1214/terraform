variable "name" {
  description = "모듈에서 정의하는 모든 리소스 이름의 prefix"
  type        = string
}

variable "ec2_count" {
  description = "EC2 생성 개수"
  type        = string
}

variable "ec2_eip_create" {
  description = "EC2 EIP 생성 여부"
  type        = bool 
  default     = true
}

variable "associate_public_ip_address" {
  description = "Public_IP 생성 여부"
  type        = bool 
  default     = true
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "ami" {
  description = "EC2 생성에 사용할 AMI"
  type        = string
}

variable "instance_type" {
  description = "EC2 EC2 instance type"
  default     = "t2.nano"
}

variable "azs" {
  description = "EC2 instance availability zone"
  type        = list(string)
}

variable "subnet_ids" {
  description = "EC2 instance Subnet ID"
  type        = list(string)
}

variable "keypair_name" {
  description = "EC2이 사용할 keypair name"
  type        = string
}

variable "ingress_cidr_blocks" {
  description = "EC2 허용할 CIDR block 리스트"
  type        = list(string)
}

variable "ingress_protocol" {
  description = "EC2 접속을 허용할 protocol"
  type        = string
}

variable "ingress_from_ports" {
  description = "EC2 접속을 허용할 from_port 리스트"
  type        = string 
}

variable "ingress_to_ports" {
  description = "EC2 접속을 허용할 to_port 리스트"
  type        = string 
}

variable "egress_cidr_blocks" {
  description = "EC2 허용할 CIDR block 리스트"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "egress_protocol" {
  description = "EC2 접속을 허용할 protocol"
  type        = string
  default     = "-1"
}

variable "egress_from_ports" {
  description = "EC2 접속을 허용할 from_port 리스트"
  type        = string 
  default     = 0
}

variable "egress_to_ports" {
  description = "EC2 접속을 허용할 to_port 리스트"
  type        = string 
  default     = 0
}

variable "command_line" {
  description = "EC2 시작할 때 실행할 명령어"
  type        = string 
  default     = "" 
}

variable "tags" {
  description = "모든 리소스에 추가되는 tag 맵"
  type        = map(string)
}

