# Repository providers

In this section, we will explore the differences between implementing the Repository Pattern in Entity Framework Core (EF Core) and ADO.NET. Both approaches provide a structured way to access data, but they have distinct implementations and usage patterns.

The primary difference between EF Core and ADO.NET repositories lies in their data access mechanisms:

- EF Core: EF Core repositories leverage an Object-Relational Mapping (ORM) framework, allowing you to work with entities directly. You interact with your database using LINQ queries and rely on the EF Core library to generate SQL statements.

- ADO.NET: ADO.NET repositories provide more direct control over SQL queries. You write SQL queries manually or with a query-building library like Dapper. This approach gives you greater flexibility but requires writing and managing SQL statements.

## Entity Framework Core

Let's dive into the EF Core implementation first, since this is the one we are using in this project.

`EFCoreRepository` exposes the `Entities` property, which corresponds to `DbSet<TEntity>` (e.g., `DbSet<Cart>`). You can use this property to perform various operations on the `Cart` entity.
The constructor of `CartRepository` requires an instance of `IDataContext`, which contains a reference to the application's `DbContext`. It also provides implementations of generic repository methods that can be used without injecting the base repository.

Since `ICartRepository` extends `IRepository<Cart, Guid>`, we can add specific methods that we may need. For example, let's add a method to retrieve all carts of a user.

```cs
public interface ICartRepository : IRepository<Cart, Guid>
{
    Task<IEnumerable<Cart>> GetCartsByUserIdAsync(Guid userId, CancellationToken cancellationToken = default);
}

public class CartRepository : EFCoreRepository<Cart, Guid>, ICartRepository
{
    public CartRepository(IDataContext context)
        : base(context)
    {
    }

    public async Task<IEnumerable<Cart>> GetCartsByUserIdAsync(Guid userId, CancellationToken cancellationToken = default)
    {
        return await Entities
            .Where(cart => cart.User.Id == userId)
            .ToListAsync(cancellationToken);
    }
}
```

The implementation is quite simple, we use the `Where` method to filter by user id.

For more in-depth explainations of the Entity Framework Core Repository Provider, see the [DAL/EF docs](../../dal/efcore.md).

## ADO.NET

If you choose to use ADO.NET instead of EF Core, you'll need to specify "Dapper" as the chosen ORM. This time, the base class is `AdoNetRepository`. It exposes the Connection property (of type `IDbConnection`), which you can use to execute SQL queries manually or with a query-building library like Dapper. Similar to EF Core, the constructor requires an instance of `IDataContext`, which provides generic CRUD methods and access to the database connection. Here's the same method implemented with Dapper.

```cs
public class CartRepository : AdoNetRepository<Cart, Guid>, ICartRepository
{
    public CartRepository(IDataContext context)
        : base(context)
    {
    }

    public async Task<IEnumerable<Cart>> GetCartsByUserIdAsync(Guid userId, CancellationToken cancellationToken = default)
    {
        const string query = "SELECT [Id] FROM [Carts] WHERE [UserId] = @userId";
        return await Connection.QueryAsync<Cart>(query, new { userId });
    }
}
```

For more in-depth explainations of the ADO.NET Repository Provider, see the [DAL/ADO.NET docs](../../dal/adonet.md).

Next step: [Table entities](table-entities.md)
