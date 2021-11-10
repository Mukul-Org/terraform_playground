

variable "activate_apis" {
  description = "Service APIs to enable."
  type        = list(string)
  default     = ["compute.googleapis.com"]
}

variable "billing_account" {
  description = "Billing account id."
  type        = string
}

variable "name" {
  description = "Project name, joined with prefix."
  type        = string
  default     = "fabric-project-test"
}

variable "owners" {
  description = "Optional list of IAM-format members to set as project owners."
  type        = list(string)
  default     = []
}

variable "parent" {
  description = "Organization or folder id, in the `organizations/nnn` or `folders/nnn` format."
  type        = string
}

variable "prefix" {
  description = "Prefix prepended to project name, uses random id by default."
  type        = string
  default     = ""
}
