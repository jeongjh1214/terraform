resource "aws_internet_gateway" "test-jaehoon-gw" {
  vpc_id = aws_vpc.test-jaehoon-vpc.id

  tags = {
    Name = "test-jaehoon"
  }
}

