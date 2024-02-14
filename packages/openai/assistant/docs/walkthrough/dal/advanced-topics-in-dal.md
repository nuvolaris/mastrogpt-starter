# Advanced topics in DAL

In this section, we will assess more advanced topics that concern the Data Access Layer.

## MultiDB

You can have multiple database at the same time and migrate from one database to another with ease.
Let's add a PostgreSQL component to our 'Store' microservice.

```yml
components:
  - type: database
    provider: sqlserver
    name: sqlserver
  - type: database
    provider: postgres
    name: postgres
```

The generator will produce the necessary code to create a Postgres Docker container and the necessary code inside the 'Store' microservice to reference it. In particular, in the `appsettings.Development.json` file, we will have

```json
{
    "Provider": "sqlserver",
    "ConnectionStrings": {
        "sqlserver": "Server=sqlserver;Database=store_db;User Id=sa;Password=Password1;TrustServerCertificate=True;",
        "postgres": "Server=postgres;Database=store_db;Username=postgres;Password=postgres"
    }
}
```

We can switch from one database to the other by changing the `Provider` value.

## Multitenancy

Multitenancy is a software architecture and deployment model that allows a single instance of an application or system to serve multiple clients or tenants. In a multitenant system, each client or tenant operates in isolation, with its own data, configurations, and user access rights, while sharing the same underlying infrastructure and application codebase. If an entity is multi-tenant, then each entity of that kind must belong to a tenant and only users belonging to that tenant can access it. In our example, there are no tenants, but we can use the same feature for segregating user data. The `Cart` entity will be multi-tenant, so that it is only visible to the user who created it.

To enable multitenancy in the 'Store' microservice, let's first add the `identity` section. Here, we will specify what claim are carried in the access token, which we will left empty for now.

```yml
identity:
  claims:
    - name: username
      type: string
      key: username
      isOptional: false
```

This will create the `IStoreIdentityProfile`, which is an interface that can be used for accessing the current user's claims.

Then, we add the `multitenancy` flag under the `data` section and set it to `true`:

```yml
data:
  orm: EntityFrameworkCore
  multitenancy: true
```

And finally, we add `isTenantEntity: true` to the `Cart` entity:

```yml
- name: Cart
  description: Represents a cart that contains orders placed by the user, which are to be processed together.
  useRepository: true
  isTenantEntity: true
  fields:
    - name: id
      type: uuid
      description: The unique identifier for the cart.
    - name: orders
      type: Order
      isArray: true
      description: The orders the cart is comprised of.
    - name: user
      type: User
      description: The user the cart belongs to.
```

Now `Cart` will extend `TenantBaseEntity` which contains a `TenantId` property indicating the tenant (or user in this case) the entity belongs to.

Next step: [Actors](../misc/actors.md)