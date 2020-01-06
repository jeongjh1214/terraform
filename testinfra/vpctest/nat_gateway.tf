resource "aws_nat_gateway" "test_1a" {
  allocation_id = aws_eip.nat_test_1a.id
  subnet_id     = aws_subnet.public_1a.id
}
resource "aws_nat_gateway" "test_1b" {
  allocation_id = aws_eip.nat_test_1b.id
  subnet_id     = aws_subnet.public_1b.id
}

