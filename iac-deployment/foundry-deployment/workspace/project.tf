# Deploy the project

resource "azapi_resource" "project" {
    type     = "Microsoft.MachineLearningServices/workspaces@2024-07-01-preview"
    name     = "azurefoundrysnorlax"
    location = var.location
    parent_id = var.resource_group_id

  identity {
    type = "SystemAssigned"
  }

  body = {
    properties = {
        description = "Azure AI"
        friendlyName = "Azure Foundry"
        hubResourceId = azapi_resource.azureaistudio-hub.id
  }
  kind = "project"
  }
  
}
