variable "environment" {
  type    = string
  default = "test"
}

variable "name" {
  type    = string
  default = "acc_vpc"
}


variable "public_subnet_name" {
  type    = string
  default = "acc_public_subnet"
}


variable "region_name" {
  type    = string
  default = "us-east-2"
}

variable "internet_gateway_name" {
  type    = string
  default = "acc_internet_gateway"
}

variable "public_route_table_name" {
  type    = string
  default = "acc_route_table"
}