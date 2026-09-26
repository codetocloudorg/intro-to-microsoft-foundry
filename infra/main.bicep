// Copyright (c) Code To Cloud Inc. Licensed under the MIT License.
//
// Minimal Microsoft Foundry environment for this workshop: one Foundry resource, one project,
// one model deployment. Adapted from Microsoft's official 00-basic template
// (github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep).
//
// Differences from Microsoft's sample, on purpose:
//   - Key-based access is DISABLED. Only Microsoft Entra ID works, matching the Azure AI Landing
//     Zones design checklist (identity area) and the "no API keys" rule used across this workshop.
//   - The deploying user is granted the Foundry User role, so the workshop scripts can call the
//     project's data plane. Owner and Contributor alone do not include those data actions.
//   - The model is gpt-5-mini, matching the samples in Modules 1 and 2.

@description('Globally unique name for the Foundry resource (2-64 chars: lowercase letters, numbers, hyphens). Also becomes the endpoint subdomain.')
param aiFoundryName string = 'foundry-${uniqueString(resourceGroup().id)}'

@description('Name of the Foundry project the workshop scripts connect to.')
param aiProjectName string = 'intro-workshop'

@description('Azure region. eastus2 has the broadest model availability; check your model per region before changing it.')
param location string = 'eastus2'

@description('Model deployment name. Modules 1 and 2 use this name as-is.')
param modelName string = 'gpt-5-mini'

@description('Model version.')
param modelVersion string = '2025-08-07'

@description('Capacity in thousands of tokens per minute (GlobalStandard). Keep small for a workshop.')
param modelCapacity int = 30

@description('Object ID of the user running the workshop. Get it with: az ad signed-in-user show --query id -o tsv')
param principalId string = ''

// Built-in role, formerly named "Azure AI User". Same role ID, renamed "Foundry User".
var foundryUserRoleId = '53ca6127-db72-4b80-b1b0-d745d6d5456d'

resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: aiFoundryName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  properties: {
    allowProjectManagement: true
    customSubDomainName: aiFoundryName
    disableLocalAuth: true
  }
}

resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  name: aiProjectName
  parent: aiFoundry
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {}
}

// Account-level child resources must be created one at a time; deploying the project and the model
// in parallel intermittently fails with RequestConflict ("another operation is in progress").
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: aiFoundry
  dependsOn: [aiProject]
  name: modelName
  sku: {
    name: 'GlobalStandard'
    capacity: modelCapacity
  }
  properties: {
    model: {
      name: modelName
      format: 'OpenAI'
      version: modelVersion
    }
  }
}

resource userAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(aiFoundry.id, principalId, foundryUserRoleId)
  scope: aiFoundry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', foundryUserRoleId)
    principalId: principalId
    principalType: 'User'
  }
}

@description('Set FOUNDRY_PROJECT_ENDPOINT to this value.')
output projectEndpoint string = 'https://${aiFoundryName}.services.ai.azure.com/api/projects/${aiProjectName}'

output modelDeploymentName string = modelDeployment.name
