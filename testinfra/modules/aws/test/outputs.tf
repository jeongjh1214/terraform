output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.bastion.id
}

output "bastion_sg_id" {
  description = "EC2에 접속하는 SG ID"
  value       = [aws_security_group.bastion.id]
}

output "ec2_sg_id" {
  description = "EC2을 통한 연결을 허용하는 SG ID"
  value       = [aws_security_group.ec2.id]
}

output "eip_id" {
  description = "EC2에 할당된 EIP ID"
  value       = [aws_eip.ec2.id]
}

