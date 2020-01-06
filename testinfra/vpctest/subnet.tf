resource "aws_subnet" "public_1a" {
  vpc_id            = aws_vpc.test-jaehoon-vpc.id
  availability_zone = "eu-west-3a"
  cidr_block        = "10.1.0.0/24"

  tags = {
    Name = "public-1a"
  }
}

resource "aws_subnet" "private_1a" {
  vpc_id            = aws_vpc.test-jaehoon-vpc.id
  availability_zone = "eu-west-3a"
  cidr_block        = "10.1.2.0/24"

  tags = {
    Name = "private-1a"
  }
}

resource "aws_subnet" "public_1b" {
  vpc_id            = aws_vpc.test-jaehoon-vpc.id
  availability_zone = "eu-west-3b"
  cidr_block        = "10.1.1.0/24"

  tags = {
    Name = "public-1b"
  }
}

resource "aws_subnet" "private_1b" {
  vpc_id            = aws_vpc.test-jaehoon-vpc.id
  availability_zone = "eu-west-3b"
  cidr_block        = "10.1.3.0/24"

  tags = {
    Name = "private-1b"
  }
}

