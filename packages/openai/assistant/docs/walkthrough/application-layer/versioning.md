# Versioning

Real-world services evolve, and so do their APIs. When this happens, keeping older versions of the APIs accessible and maintained is often required. We can do this by keeping multiple versions of the same controllers, by instructing the code generator to use versioning. To do so, we set the `useVersioning` flag to `true` and specify a current version number with the `version` field.

```yml
target:
  framework: net
  version: 7

useVersioning: true
version: 1
```

For each operation, we can specify the version it belongs to using the `version` field. If not specified, the code generator will assume they belong to the current version. For example, assume we want to increase the service's version to `2` and to define a new version of the `getCartById` operation, and still keeping the older version. We modify the YAML in the following way:

```yml
useVersioning: true
version: 2

contracts:
  operations:
    - name: getCartById
      type: http_get
      version: "1"
      description: Retrieves a cart by its unique identifier.
      parameters:
        - name: id
          description: The unique identifier of the cart to retrieve.
          direction: in
          type: uuid
        - name: cart
          type: Cart
          direction: out
          isOptional: true
          description: The retrieved cart.
    - name: getCartById
      type: http_get
      description: Retrieves a cart by its unique identifier.
      parameters:
        - name: id
          description: The unique identifier of the cart to retrieve.
          direction: in
          type: uuid
        - name: includeExpired
          description: If false, expired carts are not included in the query.
          direction: in
          type: boolean
        - name: cart
          type: Cart
          direction: out
          isOptional: true
          description: The retrieved cart.
```

This will create separate controller classes for each version. In this case, the generated folder structure may look like this:

- C# - `V1/StoreController.cs`
- C# - `V2/StoreController.cs`

Each controller class will be annotated with the appropriate API version. For instance, the V1 controller will have `[ApiVersion("1")]`, and the V2 controller will have `[ApiVersion("2")]`. Inside each controller class, the operations will be defined based on their respective versions. For example, in the `V1/StoreController.cs`:

```cs
[ApiController]
[Route("api/app/versione/store/v{version:apiVersion}")]
[ApiVersion("1")]
public class StoreController : ControllerBase
{
    // Controller for Version 1

    [HttpGet("getProductById")]
    public async Task<ActionResult<GetProductByIdResponse>> GetProductById(Guid id, CancellationToken requestAborted)
    {
        // ...
    }
}
```

## Swagger

In addition to the different versions of the controllers, a file named `ConfigureSwaggerOptions.cs` will be generated with the logic for generating Swagger documentation.

```cs
// --inject:VERSIONING--
services.AddApiVersioning(options =>
{
  options.DefaultApiVersion = ApiVersion.Default;
  options.AssumeDefaultVersionWhenUnspecified = true;
  options.ReportApiVersions = true;
  options.ApiVersionReader = new UrlSegmentApiVersionReader();
});
services.AddVersionedApiExplorer(options =>
{
  options.GroupNameFormat = "'v'VVV";
  options.SubstituteApiVersionInUrl = true;
});
services.AddSwaggerGen();
services.ConfigureOptions<ConfigureSwaggerOptions>();
// --inject:VERSIONING--

// --inject:SWAGGER_ENDPOINT--
app.UseSwaggerUI(c =>
{
  var provider = app.ApplicationServices.GetRequiredService<IApiVersionDescriptionProvider>();
  foreach (var description in provider.ApiVersionDescriptions)
  {
    c.SwaggerEndpoint($"/swagger/{description.GroupName}/swagger.json", description.ApiVersion.ToString());
  }
});
// --inject:SWAGGER_ENDPOINT--
```

Next step: [GraphQL](graphql.md)
