# SG for EC2
resource "aws_security_group" "ec2" {
  name        = var.name
  description = "Allow SSH connect to ec2 instance"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = var.ingress_from_ports
    to_port     = var.ingress_to_ports
    protocol    = var.ingress_protocol
    cidr_blocks = var.ingress_cidr_blocks
  }

  egress {
    from_port   = var.egress_from_ports
    to_port     = var.egress_to_ports
    protocol    = var.egress_protocol
    cidr_blocks = var.egress_cidr_blocks
  }

  tags = merge(
    var.tags,
    {
      "Name" = format("%s-ec2", var.name)
    },
  )
}

# EC2 Create
resource "aws_instance" "this" {

  count = var.ec2_count

  ami               = var.ami
  instance_type     = var.instance_type
  availability_zone = var.azs[count.index]
  subnet_id         = var.subnet_ids[count.index]
  key_name          = var.keypair_name
  vpc_security_group_ids = [aws_security_group.ec2.id]

  associate_public_ip_address = var.associate_public_ip_address 

  tags = merge(
    var.tags,
    {
      "Name" = format("%s-ec2-%s", var.name, var.azs[count.index])
    },
  )
}

