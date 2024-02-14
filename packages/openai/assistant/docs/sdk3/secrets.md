# Secrets Support

To generate the necessary files for using secrets, you can use the following configuration within the YAML file of the relevant microservice:

```yaml
secrets:
  - provider: azurekeyvault
```

Among the generated files, you will find a JSON file intended to contain the secrets: nome-microservizio-secrets-azurekeyvault.json:

```json
{
  "sample-key": "This is a sample secret"
}
```

Once you have added the secrets to the nome-microservizio-secrets-azurekeyvault.json file, you need to clean the Visual Studio solution to correctly load the Dapr configuration files during the Docker environment execution.

Accessing secrets within the application is identical to accessing data in the appsettings.json file. Here's an example of using a secret within the Program.cs of a microservice:

```cs
string? sampleKey = app.Configuration["sample-key"];
if (sampleKey == "This is a sample secret")
{
  app.Run();
}

app.Run();
```

In this example, the secret is retrieved from the configuration, and the application logic can proceed based on the secret's value.
