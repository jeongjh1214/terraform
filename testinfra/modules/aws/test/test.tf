# EC2 Create
resource "aws_instance" "ec2" {
  ami               = var.ami
  instance_type     = var.instance_type
  availability_zone = var.availability_zone
  subnet_id         = var.subnet_id
  key_name          = var.keypair_name
  # TF-UPGRADE-TODO: In Terraform v0.10 and earlier, it was sometimes necessary to
  # force an interpolation expression to be interpreted as a list by wrapping it
  # in an extra set of list brackets. That form was supported for compatibility in
  # v0.11, but is no longer supported in Terraform v0.12.
  #
  # If the expression in the following list itself returns a list, remove the
  # brackets to avoid interpretation as a list of lists. If the expression
  # returns a single list item then leave it as-is and remove this TODO comment.
  vpc_security_group_ids = [aws_security_group.ec2.id]

  associate_public_ip_address = true

  tags = merge(
    var.tags,
    {
      "Name" = format("%s-bastion", var.name)
    },
  )
}

# EC2 EIP
resource "aws_eip" "bastion" {
  vpc      = true
  instance = aws_instance.bastion.id
}

