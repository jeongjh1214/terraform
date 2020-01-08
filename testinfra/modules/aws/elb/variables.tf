variable "create_lb" {
  description = "Load Balance 생성 여부"
  type        = bool
  default     = true
}

variable "enable_deletion_protection" {
  description = "LB 삭제 관련 (true 면 삭제 불가능)"
  type        = bool
  default     = false
}

variable "enable_http2" {
  description = "http2 프로토콜 허용 가능여부"
  type        = bool
  default     = true
}

variable "enable_cross_zone_load_balancing" {
  description = "LB 교차적용 관련"
  type        = bool
  default     = false
}

variable "extra_ssl_certs" {
  description = "추가 인증서 관련 내용. key/values: certificate_arn, https_listener_index"
  type        = list(map(string))
  default     = []
}

variable "https_listeners" {
  description = "https 리스너 적용. Required key/values: port, certificate_arn. Optional key/values: ssl_policy (defaults to ELBSecurityPolicy-2016-08), target_group_index (defaults to 0)"
  type        = list(map(string))
  default     = []
}

variable "http_tcp_listeners" {
  description = "TCP 포트 이용한 리스너 적용. Required key/values: port, protocol. Optional key/values: target_group_index (defaults to 0)"
  type        = list(map(string))
  default     = []
}

variable "idle_timeout" {
  description = "The time in seconds that the connection is allowed to be idle."
  type        = number
  default     = 60
}

variable "ip_address_type" {
  description = "IP version 타입"
  type        = string
  default     = "ipv4"
}

variable "listener_ssl_policy_default" {
  description = "The security policy if using HTTPS externally on the load balancer. [See](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-security-policy-table.html)."
  type        = string
  default     = "ELBSecurityPolicy-2016-08"
}

variable "internal" {
  description = "Boolean determining if the load balancer is internal or externally facing."
  type        = bool
  default     = false
}

variable "load_balancer_create_timeout" {
  description = "Timeout value when creating the ALB."
  type        = string
  default     = "10m"
}

variable "load_balancer_delete_timeout" {
  description = "Timeout value when deleting the ALB."
  type        = string
  default     = "10m"
}

variable "name" {
  description = "The resource name and Name tag of the load balancer."
  type        = string
  default     = null
}

variable "name_prefix" {
  description = "The resource name prefix and Name tag of the load balancer."
  type        = string
  default     = null
}

variable "load_balancer_type" {
  description = "The type of load balancer to create. Possible values are application or network."
  type        = string
  default     = "application"
}

variable "load_balancer_update_timeout" {
  description = "Timeout value when updating the ALB."
  type        = string
  default     = "10m"
}

variable "access_logs" {
  description = "Map containing access logging configuration for load balancer."
  type        = map(string)
  default     = {}
}

variable "log_location_prefix" {
  description = "S3 prefix within the log_bucket_name under which logs are stored."
  type        = string
  default     = ""
}

variable "subnets" {
  description = "A list of subnets to associate with the load balancer. e.g. ['subnet-1a2b3c4d','subnet-1a2b3c4e','subnet-1a2b3c4f']"
  type        = list(string)
  default     = null
}

variable "subnet_mapping" {
  description = "A list of subnet mapping blocks describing subnets to attach to network load balancer"
  type        = list(map(string))
  default     = []
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}

variable "security_groups" {
  description = "The security groups to attach to the load balancer. e.g. [\"sg-edcd9784\",\"sg-edcd9785\"]"
  type        = list(string)
  default     = []
}

variable "target_groups" {
  description = "A list of maps containing key/value pairs that define the target groups to be created. Order of these maps is important and the index of these are to be referenced in listener definitions. Required key/values: name, backend_protocol, backend_port. Optional key/values are in the target_groups_defaults variable."
  type        = any
  default     = []
}

variable "vpc_id" {
  description = "VPC id where the load balancer and other resources will be deployed."
  type        = string
  default     = null
}
