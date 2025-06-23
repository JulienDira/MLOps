variable "MachineName" {
  type    = string
  default = "DefaultName"
}

provider "aws" {
  region                   = "us-east-1"
  shared_credentials_files = ["../_credentials/aws_learner_lab_credentials"]
  profile                  = "awslearnerlab"
}

data "aws_ami" "debian" {
  most_recent = true
  owners      = ["136693071363"]

  filter {
    name   = "name"
    values = ["debian-12-amd64-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_ssh"
  }
}

resource "aws_security_group" "mlflow_sg" {
  name        = "mlflow-sg"
  description = "Allow MLflow traffic on port 5000"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mlflow_ingress"
  }
}


resource "aws_security_group" "mlflow_sgApi" {
  name        = "mlflow-sgApi"
  description = "Allow MLflow API traffic on port 5001"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 5001
    to_port     = 5001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mlflow_ingressApi"
  }
}




resource "aws_security_group" "streamlit" {
  name        = "streamlit"
  description = "Allow streamlit traffic on port 8501"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "streamlit"
  }
}


resource "aws_security_group" "training" {
  name        = "mlflow-sg1"
  description = "Allow training traffic on port 4000"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 4000
    to_port     = 4000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "training"
  }
}

resource "aws_instance" "Serveur" {
  ami           = data.aws_ami.debian.id
  instance_type = "t2.micro"
  key_name      = "vockey"

  vpc_security_group_ids = [
    aws_security_group.allow_ssh.id,
    aws_security_group.mlflow_sg.id,
    aws_security_group.mlflow_sgApi.id,
    aws_security_group.streamlit.id,
    aws_security_group.training.id,
  ]

  tags = {
    Name = var.MachineName
  }
}

output "Serveur_public_ip" {
  value = aws_instance.Serveur.public_ip
}

output "Serveur_private_ip" {
  value = aws_instance.Serveur.private_ip
}
