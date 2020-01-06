#test_public
resource "aws_route_table" "test_public" {
  vpc_id = aws_vpc.test-jaehoon-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.test-jaehoon-gw.id
  }

  tags = {
    Name = "test-public"
  }
}

resource "aws_route_table_association" "test_public_1a" {
  subnet_id      = aws_subnet.public_1a.id
  route_table_id = aws_route_table.test_public.id
}

resource "aws_route_table_association" "test_public_1b" {
  subnet_id      = aws_subnet.public_1b.id
  route_table_id = aws_route_table.test_public.id
}

#test_private_1a
resource "aws_route_table" "test_private_1a" {
  vpc_id = aws_vpc.test-jaehoon-vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.test_1a.id
  }

  tags = {
    Name = "test-private-1a"
  }
}

resource "aws_route_table_association" "test_private_1a" {
  subnet_id      = aws_subnet.private_1a.id
  route_table_id = aws_route_table.test_private_1a.id
}

#test_private_1c
resource "aws_route_table" "test_private_1b" {
  vpc_id = aws_vpc.test-jaehoon-vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.test_1b.id
  }

  tags = {
    Name = "test-private-1b"
  }
}

resource "aws_route_table_association" "test_private_1b" {
  subnet_id      = aws_subnet.private_1b.id
  route_table_id = aws_route_table.test_private_1b.id
}
