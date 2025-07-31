resource "aws_vpc" "acc-vpc" {
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Environment = var.environment
    Name        = var.name
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id            = aws_vpc.myfirstvpc.id
  cidr_block        = "10.0.100.0/24"
  availability_zone = "${var.region_name}a"

  tags = {
    Name = "${var.public_subnet_name}_1"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.myfirstvpc.id

  tags = {
    Name = var.internet_gateway_name
  }
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.myfirstvpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = var.public_route_table_name
  }
}

resource "aws_route_table_association" "public_subnet_1_association" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_route_table.id
}
