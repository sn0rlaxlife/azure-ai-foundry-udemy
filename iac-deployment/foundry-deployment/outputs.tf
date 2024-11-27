output "storage_account_id" {
  value = azurerm_storage_account.westsnorlaxml.id
}

output "resource_group" {
  value = azurerm_resource_group.westsnorlax.name
}

output "location" {
  value = azurerm_resource_group.westsnorlax.location
}

output "key_vault_name" {
  value = azurerm_key_vault.azure-kv-vault.name
}

output "key_vault_uri" {
  value = azurerm_key_vault.azure-kv-vault.vault_uri
}
