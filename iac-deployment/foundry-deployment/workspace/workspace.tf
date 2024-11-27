# This file contains the terraform code to create a new Azure Machine Learning workspace in the East US 2 region.
terraform {
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
      purge_soft_delete_on_destroy = false
      recover_soft_deleted_key_vaults = false
    }
  }
}

data "azurerm_client_config" "current" {}

output "client_id" {
  value = data.azurerm_client_config.current.client_id
}


// AzAPI Hub Resource
resource "azapi_resource" "azureaistudio-hub" {
  type = "Microsoft.MachineLearningServices/workspaces@2024-07-01-preview"
  name = var.name  #required
  location = var.location
  parent_id = var.resource_group_id #required
  tags = {
    tagName1 = "terraform-workspace"
    tagName2 = "azapi-terraform"
  }
  identity {
    type = "SystemAssigned"
  }
  body = {
    properties = {
      allowPublicAccessWhenBehindVnet = true # Takes boolean (true/false)
      allowRoleAssignmentOnRG = true # New in this API (true/false)
      description = "Azure AI Studio"
      enableDataIsolation = true # New in this API (true/false) boolean
      enableSoftwareBillOfMaterials = true # New in this API (true/false) boolean
      storageAccount = var.storage_account_id
      friendlyName = "azureaistudio-eastus200"
      hbiWorkspace = false #High Business Impact (this adds more security to this workload as a criticality of importance)
      keyVault = var.key_vault_id
      publicNetworkAccess = "Disabled" # Toggle on if you'd want it private
      managedNetwork = {
        isolationMode = "AllowInternetOutbound"
        outboundRules = {
          rule1 = {
            category = "Required"
            status   = "Active"
            type     = "PrivateEndpoint"
            destination = {
              serviceResourceId = var.storage_account_id
              subresourceTarget = "blob"
            }
          },
          rule2 = {
            category = "Required"
            status   = "Active"
            type     = "PrivateEndpoint"
            destination = {
              serviceResourceId = var.key_vault_uri
              subresourceTarget = "vault"
            }
          },
          rule3 = {
            category = "Required"
            status   = "Active"
            type     = "ServiceTag"
            destination = {
              serviceTag = "AzureActiveDirectory"
            }
          }
            }
          }
        }
    
    sku = {
      name = "S0"
      size = "Basic"
      tier = "Basic"
    }
    kind = "hub"
  }
  
  depends_on = [
    var.key_vault_name,
    var.user_assigned_identity,
    ]
}
