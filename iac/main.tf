module "vpc-acc" {
  source = "./modules/vpc"
  name   = "vpc-acc"
}

module "acc-ec2" {
  source           = "./modules/ec2"
  key_name         = var.key_name
  public_subnet_id = module.vpc-acc.public_subnet.id
  vpc_id           = module.vpc-acc.vpc.id
  connection_ip    = var.connection_ip
}
