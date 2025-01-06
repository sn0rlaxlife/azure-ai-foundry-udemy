#!/bin/bash

RESOURCE_GROUP_NAME="rg-srodriguezai"

# Create a search service
az search service create \
    --name rag-searching \
    --resource-group $RESOURCE_GROUP_NAME \
    --sku Standard \
    --public-access enabled # or disabled if you want to keep this resource behind a firewall


