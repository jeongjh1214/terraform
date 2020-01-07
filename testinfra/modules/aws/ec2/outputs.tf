output "instance_id" {
  description = "EC2 instance ID"
  value       = [aws_instance.this.*.id]
}

output "ec2_sg_id" {
  description = "EC2에 접속하는 SG ID"
  value       = [aws_security_group.ec2.id]
}

