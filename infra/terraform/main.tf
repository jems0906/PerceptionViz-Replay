terraform {
  required_version = ">= 1.6.0"
}

variable "project_name" {
  type    = string
  default = "perceptionviz-replay"
}

output "railway_note" {
  value = "Provision Railway services from railway.json or map this module to your team's Railway provider workflow."
}
