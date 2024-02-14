# Secrets

Here, we will assess how to use Azure Key Vault as a secret store with Dapr in your microservice. For more in-depth explainations of the secrets and the CodeArchitects.Platform implementation, see the [Secrets](../../sdk/secrets.md).

In your microservice's YAML configuration, add the following section to specify the use of Azure Key Vault as a secret store:

```yml
secrets:
  - provider: azurekeyvault
```

This section instructs the code generator to produce the necessary configuration to tell Dapr to use Azure Key Vault as a secret store.
The following configuration YAML will be generated inside the `Dapr/configuration` folder:

```yml
#begin-template service/dapr/components/secret.ejs 
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: store-secrets-azurekeyvault
  namespace: default
spec:
  type: secretstores.local.file
  version: v1
  metadata:
  - name: secretsFile
    value: ./components/store-secrets-azurekeyvault.json
  - name: nestedSeparator
    value: ":"
#end-template service/dapr/components/secret.ejs
```

This configuration is for local development, as it uses a JSON file instead of the real Azure service. In production, this file must be overridden with the information to access the Vault.

We can use the `store-secrets-azurekeyvault.json` for local development and add the secrets we would find in the Azure Key Vault in production. Add key-value pairs corresponding to your secrets, for example:

```json
{
    "mySecret": "super secret information"
}
```

Next step: [Telemetry](telemetry.md)
