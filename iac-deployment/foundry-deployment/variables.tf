# Storage name
variable "storage_account_name" {
    default     = "westsnorlaxml"
    description = "The name of the storage account"
    type        = string
}

# Ensures support of services East US2
variable "location" {
    default     = "eastus2"
    description = "The location of the resource group"
    type        = string
}

# RG name can be changed
variable "resource_group_name" {
    default     = "westsnorlax"
    description = "The name of the resource group"
    type        = string
}

variable "user_assigned_identity" {
  default     = "keyvault-identity"
  description = "The name of the user assigned identity"
  type        = string
}

variable "azure_key_vault" {
    default     = "azurekeyvault1008523"
    description = "The name of the key vault"
    type        = string
}

variable "key_vault_name" {
  default     = "kv-aiservices100024"
  description = "The name of the key vault"
  type        = string
}

# List of permissions for Storage
variable "storage_permissions" {
  default = ["Get"]
  description = "The permissions for the storage account"
  type = list(string)
}

# List of permissions to KV
variable "key_permissions" {
  description = "List of key permissions for the Key Vault access policy"
  type        = list(string)
  default     = ["Get", "Create", "GetRotationPolicy", "SetRotationPolicy"]
}

# List of permissions secrets
variable "secret_permissions" {
  description = "List of secret permissions for the Key Vault access policy"
  type        = list(string)
  default     = ["Get"]
}
