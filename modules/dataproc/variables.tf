variable "project_name" {
  type        = string
  description = "Project name"
}

variable "region" {
  type        = string
  default     = "europe-west1"
  description = "GCP region"
}

variable "subnet" {
  type        = string
  description = "VPC subnet used for deployment"
}

variable "machine_type" {
  type        = string
  default     = "e2-medium"
  description = "Machine type to use for both worker and master nodes"
}

variable "image_version" {
  type    = string
  default = "2.2.69-ubuntu22"
}

variable "secondary_num_instances" {
  type        = number
  default     = 4
  description = "Number of secondary nodes"
}

variable "secondary_preemptibility" {
  type        = string
  default     = "SPOT"
  description = "Preemptibility of the secondary workers"
}