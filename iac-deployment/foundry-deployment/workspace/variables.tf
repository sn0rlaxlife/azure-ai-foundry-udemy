# Add the virtual network edition 11-26-24 add
variable "subnet_id" {
  description = "The ID of the subnet of the private endpoint"
  type        = string
}

# Variable for the virtual network name
variable "virtual_network_name" {
  description = "The name of the virtual network"
  type        = string
}


variable "user_assigned_identity" {
  description = "The name of the user assigned identity"
  type        = string
}

variable "user_assigned_identity_id" {
  description = "The ID of the user assigned identity"
  type        = string
}

variable "user_assigned_identity_client_id" {
  description = "The client ID of the user assigned identity"
  type        = string
}

variable "user_assigned_identity_principal_id" {
  description = "The principal ID of the user assigned identity"
  type        = string
}



variable "name" {
  default     = "azureaiservices1000"
  description = "The name of the cognitive service"
  type        = string
}


variable "resource_group_name" {
  default     = "westsnorlax"
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  default     = "eastus2"
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

variable "storage_account_name" {
    default     = "westsnorlaxml"
    description = "The name of the storage account"
    type        = string
}

variable "azure_key_vault" {
    default     = "azurekeyvault1008523"
    description = "The name of the key vault"
    type        = string
}

variable "key_vault_name" {
    description = "The name of the key vault"
    type        = string
}


# How do you want the AI Hub/Workspace to be isolated?
variable "isolationMode" {
    default     = "AllowOnlyApprovedOutbound"
    description = "The isolation mode of the managed network"
    type        = string
}

# Disable this for private access / Enable this for public access - you can also segment on authorized IP ranges from the VNET.
variable "publicNetworkAccess" {
    default     = "Enabled"
    description = "The public network access of the AI Hub/Workspace"
    type        = string
}

variable "resource_group_id" {
    description = "The ID of the resource group"
    type        = string
}

variable "storage_account_id" {
    description = "The ID of the storage account"
    type        = string
}

variable "key_vault_id" {
    description = "The ARM ID of the key vault"
    type        = string
}

variable "key_id" {
  description = "The created encryption key ID"
  type        = string
}

variable "key_vault_key_name" {
    description = "The name of the key vault key"
    type        = string
}

variable "key_vault_uri" {
    description = "The URI of the key vault required for the PE to the hub"
    type        = string
}
