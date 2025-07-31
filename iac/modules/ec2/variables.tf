variable "ami_id" {
  type    = string
  default = "ami-0eb070c40e6a142a3"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "vpc_id" {
  type = string
}

variable "connection_ip" {
  type = string
}

variable "project_name" {
  type    = string
  default = "Course"
}

variable "lb_name" {
  type    = string
  default = "myloadbalancer"
}

variable "ec2_private_instances_sg_name" {
  type    = string
  default = "ec2_private_instances_sg_name"
}

variable "public_subnet_id_1" {
  type = string
}

variable "public_subnet_id_2" {
  type = string
}

variable "private_subnet_id_1" {
  type = string
}

variable "private_subnet_id_2" {
  type = string
}

variable "key_name" {
  type = string
}

variable "root_volume_type" {
  type    = string
  default = "gp3"
}

variable "root_volume_size" {
  type    = number
  default = 8
}

variable "root_iops" {
  type    = number
  default = 3000
}

variable "environment" {
  type    = string
  default = "test"
}

variable "app_name" {
  type    = string
  default = "server"
}

variable "bastionhost_name" {
  type    = string
  default = "bastionhost"
}

variable "bastionhost_sg_name" {
  type    = string
  default = "bastionhost_sg"
}

variable "lb_sg_name" {
  type    = string
  default = "lb_sg"
}