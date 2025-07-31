variable "environment" {
  type    = string
  default = "test"
}

variable "name" {
  type    = string
  default = "myfirstvpc"
}


variable "public_subnet_name" {
  type    = string
  default = "mypublic_subnet"
}


variable "region_name" {
  type    = string
  default = "us-east-2"
}

variable "internet_gateway_name" {
  type    = string
  default = "myinternet_gateway"
}

variable "public_route_table_name" {
  type    = string
  default = "mypublic_route_table"
}