variable "name" {
  default     = "azureaiservices1000"
  description = "The name of the cognitive service"
  type        = string
}

variable "resource_group_name" {
  default     = "ai-demo-rg-1000"
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  default     = "eastus"
  description = "The location of the resource group"
  type        = string
}

variable "kind" {
  default     = "OpenAI"
  description = "The kind of cognitive service"
  type        = string
}

variable "sku_name" {
  default     = "S0"
  description = "The SKU name of the cognitive service"
  type        = string
}