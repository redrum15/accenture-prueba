module "vpc-acc" {
  source = "./modules/vpc"
  name   = "vpc-acc"
}

module "first_ec2" {
  source              = "./modules/ec2"
  key_name            = var.key_name
  public_subnet_id_1  = module.first_vpc.public_subnet_1.id
  public_subnet_id_2  = module.first_vpc.public_subnet_2.id
  private_subnet_id_1 = module.first_vpc.private_subnet_1.id
  private_subnet_id_2 = module.first_vpc.private_subnet_2.id
  vpc_id              = module.first_vpc.vpc.id
  connection_ip       = var.connection_ip
}