provider "azurerm" {
  # Configuration options

    features {}
}

##provider "azapi" {
    # Configuration options
##}

terraform {
    backend "local" {
    }

    required_providers {
       ## azapi = {
       ##     source  = "Azure/azapi"
       ##     version = "~>1.13.1"
       ## }
        azurerm = {
            source = "hashicorp/azurerm"
            version = "3.104.0"
        }
    }
}

resource "azurerm_resource_group" "airesourcegroup" {
    name     = "ai-demo-rg-1000"
    location = "eastus"
}

module "cognitiveservice" {
    source = "./cognitiveservice"
    name = "azureaiservices1000"
    resource_group_name = azurerm_resource_group.airesourcegroup.name
    location = azurerm_resource_group.airesourcegroup.location
    kind = "OpenAI"
    sku_name = "S0"
}