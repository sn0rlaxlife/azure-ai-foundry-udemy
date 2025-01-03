terraform {
  backend "local" {
  }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.11.0"
    }
    azapi = {
      source  = "Azure/azapi"
      version = "2.0.1"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy    = true # This means when the key vault is destroyed, any keys, secrets, and certificates are not purged, they remain in a soft-delete
      recover_soft_deleted_key_vaults = false # This means that when the key vault is destroyed, it cannot be recovered
    }
  }
}

provider "azapi" {
}

# Create the resource group - variables define the location/name
resource "azurerm_resource_group" "westsnorlax" {
  name     = var.resource_group_name
  location = var.location
}

# Create our virtual network that will house the private endpoints
resource "azurerm_virtual_network" "westsnorlax" {
  name                = "westsnorlax-vnet"
  resource_group_name = var.resource_group_name
  location            = var.location
  address_space       = ["10.0.0.0/16"]

  depends_on = [
    azurerm_resource_group.westsnorlax,
  ]
}

# Create a subnet for the private endpoints
resource "azurerm_subnet" "subnetpe" {
  name                 = "westsnorlax-subnet"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.westsnorlax.name
  address_prefixes     = ["10.0.1.0/24"]

  depends_on = [
    azurerm_virtual_network.westsnorlax,
  ]
}


# User assigned identity - this is used to assign permissions to the key vault
resource "azurerm_user_assigned_identity" "keyvault-identity" {
  name                = var.user_assigned_identity
  resource_group_name = var.resource_group_name
  location            = var.location

  depends_on = [
    azurerm_resource_group.westsnorlax,
  ]
}

data "azurerm_client_config" "current" {}

output "client_id" {
  value = data.azurerm_client_config.current.client_id
}

# Create the key vault
resource "azurerm_key_vault" "azure-kv-vault" {
  name                     = var.key_vault_name
  location                 = var.location
  resource_group_name      = var.resource_group_name
  sku_name                 = "standard"
  purge_protection_enabled = false
  tenant_id                = data.azurerm_client_config.current.tenant_id

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = var.key_permissions
    secret_permissions  = var.secret_permissions
    storage_permissions = var.storage_permissions
  }

  access_policy {
    tenant_id = azurerm_user_assigned_identity.keyvault-identity.tenant_id
    object_id = azurerm_user_assigned_identity.keyvault-identity.principal_id
    
     key_permissions = [
      "Create",
      "Get",
      "Delete",
      "List",
      "Restore",
      "Release",
      "UnwrapKey",
      "WrapKey",
      "GetRotationPolicy",
      "SetRotationPolicy",
      "Rotate"
    ]
  }

  depends_on = [
    azurerm_user_assigned_identity.keyvault-identity,
    azurerm_resource_group.westsnorlax,
  ]
}

# Create an encrypted key in the key vault if you'd desire CMK ensure Purge Protection is enabled on the Key Vault above
resource "azurerm_key_vault_key" "encryptedkey" {
  name         = "ai-studio-key"
  key_vault_id = azurerm_key_vault.azure-kv-vault.id
  key_type     = "RSA"
  key_size     = 2048

  key_opts = [
    "decrypt",
    "encrypt",
    "sign",
    "unwrapKey",
    "verify",
    "wrapKey",
  ]

  depends_on = [
    azurerm_key_vault.azure-kv-vault,
  ]
}

# RBAC assignment for the user assigned identity
resource "azurerm_role_assignment" "keyvault-assignment" {
  scope                = azurerm_key_vault.azure-kv-vault.id
  role_definition_name = "Key Vault Contributor"
  principal_id         = azurerm_user_assigned_identity.keyvault-identity.principal_id

  depends_on = [
    azurerm_user_assigned_identity.keyvault-identity,
  ]
}

# Create the storage account
resource "azurerm_storage_account" "westsnorlaxml" {
  name                     = var.storage_account_name
  location                 = var.location
  resource_group_name      = var.resource_group_name
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"

  depends_on = [
    azurerm_resource_group.westsnorlax,
  ]
}

# Defining private endpoint for storage account this is used to secure the storage account from public access
resource "azurerm_private_endpoint" "storage" {
  name                = "pe-storage-endpoint"
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = azurerm_subnet.subnetpe.id
  private_service_connection {
    name                           = "storage-connection"
    private_connection_resource_id = azurerm_storage_account.westsnorlaxml.id
    is_manual_connection            = false
    subresource_names               = ["blob"]
  }

  depends_on = [
    azurerm_storage_account.westsnorlaxml,
    azurerm_virtual_network.westsnorlax,
  ]
}

# Defining private endpoint for keyvault this is used to secure the key vault from public access
resource "azurerm_private_endpoint" "keyvault" {
  name                = "pe-keyvault-endpoint"
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = azurerm_subnet.subnetpe.id
  private_service_connection {
    name                           = "keyvault-connection"
    private_connection_resource_id = azurerm_key_vault.azure-kv-vault.id
    is_manual_connection            = false
    subresource_names               = ["vault"]
  }
}

# Assign public access as disabled to the storage account
resource "azurerm_storage_account_network_rules" "westsnorlaxml" {
  storage_account_id         = azurerm_storage_account.westsnorlaxml.id
  default_action             = "Deny"
  bypass                     = ["AzureServices", "Logging", "Metrics"]
}

# Module workspace contains components such as Hub/Studio for Azure AI Services
module "workspace" {
  source                 = "./workspace"
  name                   = "azureaiservices10001"
  resource_group_name    = var.resource_group_name
  resource_group_id      = azurerm_resource_group.westsnorlax.id
  location               = var.location
  storage_account_name   = var.storage_account_name
  storage_account_id     = azurerm_storage_account.westsnorlaxml.id
  subnet_id              = azurerm_subnet.subnetpe.id
  virtual_network_name   = azurerm_virtual_network.westsnorlax.name
  key_vault_name         = azurerm_key_vault.azure-kv-vault.name
  key_vault_id           = azurerm_key_vault.azure-kv-vault.id
  key_vault_key_name     = azurerm_key_vault_key.encryptedkey.name
  key_id                 = azurerm_key_vault_key.encryptedkey.id
  key_vault_uri          = azurerm_key_vault.azure-kv-vault.vault_uri
  user_assigned_identity = azurerm_user_assigned_identity.keyvault-identity.name
  user_assigned_identity_id = azurerm_user_assigned_identity.keyvault-identity.id
  user_assigned_identity_principal_id = azurerm_user_assigned_identity.keyvault-identity.principal_id
  user_assigned_identity_client_id = azurerm_user_assigned_identity.keyvault-identity.client_id
}
