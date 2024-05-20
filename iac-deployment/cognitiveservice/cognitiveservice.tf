
resource "azurerm_cognitive_account" "azureaiservices" {
    name                = var.name
    resource_group_name = var.resource_group_name
    location            = var.location
    kind                = var.kind
    sku_name            = var.sku_name
    
}

# Deploy the service as a deployment
resource "azurerm_cognitive_deployment" "azureaiservices" {
    name                    = var.name
    cognitive_account_id    = azurerm_cognitive_account.azureaiservices.id
    ##rai_policy_name         =  "policyforai"
    model {
        format  = "OpenAI"
        name    = "gpt-35-turbo"
        version = "0613"
    }

    scale {
        type = "Standard"
    }
}


##resource "azapi_resource" "content_filter" {
##    type = "Microsoft.CognitiveServices/accounts/raiPolicies@2023-10-01-preview"
##    name = "policyai"
##    parent_id = azurerm_cognitive_account.azureaiservices.id

##    schema_validation_enabled = false

##    body = jsonencode({
##    properties = {
##      mode           = "Default",
##      basePolicyName = "Microsoft.Default",
##      contentFilters = [
##        { name = "hate", blocking = true, enabled = true, allowedContentLevel = "High", source = "Prompt" },
##        { name = "sexual", blocking = true, enabled = true, allowedContentLevel = "High", source = "Prompt" },
##        { name = "selfharm", blocking = true, enabled = true, allowedContentLevel = "High", source = "Prompt" },
##        { name = "violence", blocking = true, enabled = true, allowedContentLevel = "High", source = "Prompt" },
##        { name = "hate", blocking = true, enabled = true, allowedContentLevel = "High", source = "Completion" },
##        { name = "sexual", blocking = true, enabled = true, allowedContentLevel = "High", source = "Completion" },
##        { name = "selfharm", blocking = true, enabled = true, allowedContentLevel = "High", source = "Completion" },
##        { name = "violence", blocking = true, enabled = true, allowedContentLevel = "High", source = "Completion" },
##        { name = "jailbreak", blocking = true, enabled = true, source = "Prompt" },
##        { name = "protected_material_text", blocking = true, enabled = true, source = "Completion" },
##        { name = "protected_material_code", blocking = true, enabled = true, source = "Completion" }
##      ]
##    }
##  })
##  depends_on = [
##    azurerm_resource_group.airesourcegroup,
##    azurerm_cognitive_account.azureaiservices,
##    azurerm_cognitive_deployment.azureaiservices
##  ]
##}
