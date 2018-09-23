## Amazon Infrastructure
provider "aws" {
  region = "${var.aws_region}"
}

## Create swarm security group
resource "aws_security_group" "swarm_sg" {
  name        = "swarm_sg"
  description = "Allow all inbound traffic necessary for Swarm"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 2377
    to_port     = 2377
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 7946
    to_port     = 7946
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 7946
    to_port     = 7946
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 4789
    to_port     = 4789
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }

  tags {
    Name = "swarm_sg"
  }
}

# ## Find latest AMI
# data "aws_ami" "ubuntu" {
#   most_recent = true
#
#   filter {
#     name   = "tag-value"
#     values = ["docker_host_ubuntu_16_04"]
#   }
#
#   owners = ["self"]
# }
data "aws_ami" "moby" {
  most_recent = true

  filter {
    name   = "name"
    values = ["Moby Linux 18.06.0-ce-aws1 stable"]
  }

  owners = ["041673875206"]
}

# TODO: Open Azure ports to allow managers
# ## Create Swarm Managers
# resource "aws_instance" "aws-swarm-managers" {
#   depends_on             = ["aws_security_group.swarm_sg"]
#   ami                    = "${data.aws_ami.moby.id}"
#   instance_type          = "${var.manager_instance_type}"
#   vpc_security_group_ids = ["${aws_security_group.swarm_sg.id}"]
#   key_name               = "${var.aws_key_name}"
#   count                  = "${var.manager_count}"
#
#   tags {
#     Name = "swarm-manager-${count.index}"
#   }
# }

## Create AWS Swarm Workers
resource "aws_instance" "aws-swarm-workers" {
  depends_on             = ["aws_security_group.swarm_sg"]
  ami                    = "${data.aws_ami.moby.id}"
  instance_type          = "${var.worker_instance_type}"
  vpc_security_group_ids = ["${aws_security_group.swarm_sg.id}"]
  key_name               = "${var.aws_key_name}"
  count                  = "${var.worker_count}"

  tags {
    Name = "swarm-worker-${count.index}"
  }
}
