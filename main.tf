terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.16"
    }
  }
}

variable "my_access_key" {
  description = "AWS-Keypair"
  default = "no_access_key_value_found"
}

variable "my_secret_key" {
  description = "AWS-Keypair"
  default = "no_secret_key_value_found"
}

resource "aws_key_pair" "my_key_pair" {
  key_name   = "aws"
  public_key = file("/Tu PATH hasta el archivo/ansiblekey.pub")  # Adjust the path to your public key file
}

provider "aws" {
  region = "us-east-1" # Cambia esto a la región de AWS que prefieras
  access_key = "YOUR AWS ACCESS_KEY" #Adjust your AWS access_key
	secret_key = "YOUR AWS SECRET_KEY" #Adjust your AWS secret_key
}


resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
    tags = {
    Name = "my-VPC"
  }
}

resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.main.id
   tags = {
    Name = "my-IGW"
  }
}

resource "aws_subnet" "my_subnet" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1c" # Cambia esto a la zona de AWS que prefieras
  map_public_ip_on_launch = true
  tags = {
    Name = "my_public_subnet"
  }
}


resource "aws_route_table" "my_route_table" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my_igw.id
  }
  tags = {
    Name = "my_route_table"
  }
}

resource "aws_route_table_association" "public_association" {
  subnet_id      = aws_subnet.my_subnet.id
  route_table_id = aws_route_table.my_route_table.id
}

resource "aws_security_group" "my_security_group" {
  name        = "my-security-group"
  vpc_id      = aws_vpc.main.id
  description = "Allow inbound traffic on ports 80, 443, 5000, and 22"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
  from_port   = 5432  # Puerto de PostgreSQL
  to_port     = 5432  # Puerto de PostgreSQL
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]  # Permitir tráfico desde cualquier dirección IP. Considera restringir esto según tu configuración de red.
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = -1
    to_port   = -1
    protocol  = "icmp"
    cidr_blocks = ["0.0.0.0/0"]  # Adjust the CIDR block based on your requirements
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "Client" {
  ami            = "ami-058bd2d568351da34" # Reemplaza con la AMI de AWS que desees
  instance_type  = "t2.micro"
  subnet_id      = aws_subnet.my_subnet.id
  security_groups = [aws_security_group.my_security_group.id]
  key_name      = aws_key_pair.my_key_pair.key_name
  #subnet_id     = "subnet-09f35a2351872c0b5"  # Update with your subnet ID
  #vpc_security_group_ids = ["sg-04d03e3084e26d15d"]  # Update with your security group ID
  ##key_name = "franklin.riera" # Reemplaza con el nombre de tu clave en AWS
  tags = {
    Name = "terraform-client"
  }
}

resource "aws_instance" "API" {
  ami            = "ami-058bd2d568351da34" # Reemplaza con la AMI de AWS que desees
  instance_type  = "t2.micro"
  subnet_id      = aws_subnet.my_subnet.id
  security_groups = [aws_security_group.my_security_group.id]
  key_name      = aws_key_pair.my_key_pair.key_name
  #subnet_id     = "subnet-09f35a2351872c0b5"  # Update with your subnet ID
  #vpc_security_group_ids = ["sg-04d03e3084e26d15d"]  # Update with your security group ID
  ##key_name = "franklin.riera" # Reemplaza con el nombre de tu clave en AWS
  tags = {
    Name = "terraform-api"
  }
}


output "public_ip_Client" {
  value       = aws_instance.Client.public_ip
  description = "La dirección IP pública de la instancia creada"
}

output "public_ip_API" {
  value       = aws_instance.API.public_ip
  description = "La dirección IP pública de la instancia creada"
}
