resource "null_resource" "ansible-provision" {
  # depends_on = ["aws_instance.aws-swarm-managers", "aws_instance.aws-swarm-workers"]
  depends_on = ["aws_instance.aws-swarm-workers"]

  # provisioner "local-exec" {
  #   command = "echo \"[swarm-managers]\" >> swarm-inventory"
  # }
  #
  # provisioner "local-exec" {
  #   command = "echo \"${join("\n",formatlist("%s ansible_user=%s ansible_ssh_private_key_file=%s.pem", aws_instance.aws-swarm-managers.*.public_ip, var.ssh_user, var.aws_key_name))}\" >> swarm-inventory"
  # }

  provisioner "local-exec" {
    command = "echo \"[swarm-workers]\" >> swarm-inventory"
  }

  provisioner "local-exec" {
    command = "echo \"${join("\n",formatlist("%s ansible_user=%s ansible_ssh_private_key_file=%s.pem", aws_instance.aws-swarm-workers.*.public_ip, var.ssh_user, var.aws_key_name))}\" >> swarm-inventory"
  }
}
