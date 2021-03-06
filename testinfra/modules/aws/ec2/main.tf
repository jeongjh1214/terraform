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


  connection {
	host = self.host_id
	user = "ec2-user"
	type = "ssh"
	private_key = file("jaehoon-test1.pem")
	timeout = "2m"
  }
  
  provisioner "remote-exec" {
    inline = [
	"sudo yum update",
	"sudo yum install -y python",
	]
    }

  provisioner "local-exec" {
    command = <<EOF
	echo "[demo]" > inventory
	echo "${self.public_ip} ansible_ssh_user=ec2-user ansible_ssh_private_key_file=/home/ec2-user/.ssh/${var.keypair_name}" >> inventory
    EOF
}

  provisioner "local-exec" {
    command = <<EOF
	ANSIBLE_HOST_KEY_CHECKING=False \
	ansible-playbook -i inventory playbook.yml
	EOF
    }

  associate_public_ip_address = var.associate_public_ip_address 

  tags = merge(
    var.tags,
    {
      "Name" = format("%s-ec2-%s", var.name, var.azs[count.index])
    },
  )
}

