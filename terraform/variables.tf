variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "cloud-resume"
}

variable "domain_name" {
  description = "Custom domain name for the resume site"
  type        = string
  default     = ""
}

variable "enable_dns" {
  description = "Set to true after registering a domain"
  type        = bool
  default     = false
}
