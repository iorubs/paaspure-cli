variable "stack_name" {}
variable "resource_group_name" {}
variable "resource_group_location" {}
variable "parameters" { type = "map" }

## Infrastructure
resource "azurerm_resource_group" "paaspure_infra" {
  name = "${var.resource_group_name}"
  location = "${var.resource_group_location}"
}

resource "azurerm_template_deployment" "paaspure_infra" {
  name = "${var.stack_name}"

  resource_group_name = "${azurerm_resource_group.paaspure_infra.name}"

  template_body = "${file("./Docker.tmpl")}"

  parameters = "${var.parameters}"

  deployment_mode = "Incremental"
}
