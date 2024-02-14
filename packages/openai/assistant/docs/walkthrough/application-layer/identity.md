# Identity

This section will explain how to read claims from the user's access token in a simple way. For more in-depth explainations of the identity and the CodeArchitects.Platform implementation, see the [Identity](../../sdk/identity.md).

## Identity profile

Claims of a token should be accessed in a name-safe and type-safe way, through a standardized object. That's what the `IIdentityProfile` interface is for. It serves as the base interface for identity profiles that contain properties which are mapped onto claims of a JWT.

Imagine our JWT contains a key-value pair `username`, which is the user name of the current user. Let's model this by adding a new section in the microservice's YAML.

```yml
identity:
  claims:
    - name: username
      type: string
      key: username
      isOptional: false
```

In the `claims` section of the `identity` section we can model the claims the JWT carries. This will generate an `IStoreIdentityProfile` interface and a `StoreIdentityProfile` class which implements that interface.

```cs
public interface IStoreIdentityProfile : IIdentityProfile<Guid>
{
    string Username
    {
        get;
    }
    // <custom:CLAIMS>
    // </custom:CLAIMS>
}

public class StoreClaimsIdentityProfile : ClaimsIdentityProfile<Guid>, IStoreIdentityProfile
{
    // <custom:CONSTRUCTOR>
    public StoreClaimsIdentityProfile(IHttpContextAccessor httpContextAccessor) : base(httpContextAccessor)
    { }
    // </custom:CONSTRUCTOR>

    public string Username
    {
        get
        {
            return GetRequiredClaim(StoreClaimTypes.Username);
        }
    }
    // <custom:CLAIMS>
    // </custom:CLAIMS>
}
```

The base interface `IIdentityProfile<TUserId>` defines a `TUserId` property which is used to retrieve the current user's id. In addition to this, our interface lets us retrieve its username. By default, `TUserId` is `Guid`, but we can customize this by specifying another type in the YAML section.

```yml
identity:
  userId:
    type: integer
  claims:
    - name: username
      type: string
      key: username
      isOptional: false
```

Now, our `UserId` claim will be interpreted as an integer value.

Next step: [Communication between microservices](communication-between-microservices.md)
