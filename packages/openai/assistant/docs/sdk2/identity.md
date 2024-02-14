# Identity Profile

The identity profile provides a strongly-typed representation of claims associated with an authenticated user. This service is modeled as an interface, inheriting at least two properties: `IsAuthenticated` and `UserId` from the base interface `IIdentityProfile<TUserId>`. Additionally, you can define other properties based on the user's claim model.

Using the identity profile, you can access user claims as properties rather than using a dictionary-like interface provided by `ClaimsPrincipal`. This also includes the automatic conversion of claim values from strings to their respective types. Assuming you have already configured authentication using the `AddAuthentication` method in ASP.NET Core, you can define the interface modeling the identity profile in the `identity` section of your YAML service configuration.

Inside this section, create a list of `claims` (which can be empty), defining for each claim: `name` (the name of the claim or property), `type` (the type of the claim), `key` (the claim's key used in serialization), and `isOptional` (specifying whether the claim is optional or not):

```yml
identity:
  claims:
    - name: givenName
      type: string
      key: given_name
      isOptional: false
```

This configuration will generate an interface like this:

```cs
public interface IApplicationIdentityProfile : IIdentityProfile<Guid>
{
    string GivenName { get; }
}
```

And a class implementing it:

```cs
public class ApplicationClaimsIdentityProfile : ClaimsIdentityProfile<Guid>, IApplicationIdentityProfile
{
    public ApplicationClaimsIdentityProfile(IHttpContextAccessor httpContextAccessor)
        : base(httpContextAccessor)
    {
    }

    public string GivenName => ...;
}
```

The service will be registered in the IoC container, and you can request an instance of the IApplicationIdentityProfile interface using Dependency Injection.

By default, the UserId claim is of type Guid. To use a different type, specify it in the userId sub-section. For example, to make it of type string:

```yml
identity:
  claims:
    - name: givenName
      type: string
      key: given_name
      isOptional: false
  userId:
    type: string
```

# Multitenancy
If your application is multi-tenant, you can specify the key to use for the tenant claim in the tenantId sub-section. Optionally, you can specify the type (default is Guid).

```yml
identity:
  claims:
    - name: givenName
      type: string
      key: given_name
      isOptional: false
  userId:
    type: string
  tenantId:
    key: http://schemas.microsoft.com/identity/claims/tenantid
```

In this case, the generated interface will include:

```cs
public interface IApplicationIdentityProfile : IIdentityProfile<string>, ITenantIdProfile<Guid>
{
    string GivenName { get; }
}
```

And the class implementing it will include:

```cs
public class ApplicationClaimsIdentityProfile : ClaimsIdentityProfile<string>, IApplicationIdentityProfile
{
    public ApplicationClaimsIdentityProfile(IHttpContextAccessor httpContextAccessor)
        : base(httpContextAccessor)
    {
    }

    public string GivenName => ...;

    public Guid TenantId => ...;
}
```

After defining the tenant claim, in the data section, set the multitenancy field to true:

```yml
data:
  orm: EntityFrameworkCore
  multitenancy: true
```

Entities that are segregated by tenant can be defined with isTenantEntity: true (make sure to run migrations):

```yml
entities:
  - name: Customer
    description: Customer Entity
    useRepository: true
    isTenantEntity: true
    fields:
      - name: name
        type: string
        description: Customer name
      - name: surname
        type: string
        description: Customer surname
```

With this setup, queries involving these entities will automatically include a filter based on the user's tenant id when executed. To temporarily disable the filter for a specific query, you can use the AsNoMultitenancy() extension method on IQueryable<T>. For example:

```cs
var bobCustomers = context.Set<Customer>()
    .AsNoMultitenancy()
    .Where(name => name == "Bob")
    .ToList();
```

This allows you to control the application's behavior regarding multitenancy at both the global and query levels.