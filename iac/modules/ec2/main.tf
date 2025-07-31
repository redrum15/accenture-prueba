locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_security_group" "lb_sg" {
  name   = var.lb_sg_name
  vpc_id = var.vpc_id


  tags = merge(local.common_tags, {
    Name = "${var.lb_sg_name}"
  })


  ingress {
    description = "Port 22 access"
    cidr_blocks = [var.connection_ip]
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
  }

  egress {
    description = "Security Group egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_instance" "accenture-instance" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  ebs_optimized               = false
  associate_public_ip_address = true
  key_name                    = var.key_name
  subnet_id                   = var.public_subnet_id
  monitoring                  = true
  vpc_security_group_ids      = [aws_security_group.lb_sg.id]

  root_block_device {
    volume_type = var.root_volume_type
    volume_size = var.root_volume_size
    iops        = var.root_iops
  }
}
