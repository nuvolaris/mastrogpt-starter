# Entities and database

We will define and model the essential entities for our eCommerce application, including User, Product, Cart, and Order. We will also specify the relationships between these entities to accurately represent our application's data model.

## Entities

- `User`: Represents a user of the eCommerce platform.
- `Product`: Represents a product available for purchase.
- `Order`: Represents an order order placed by users.
- `Cart`: Represents a cart that contains orders placed by the user, which are to be processed together.

## Database component

For more in-depth explainations of the database and the CodeArchitects.Platform implementation, see the [Database docs](../../sdk/database.md).

Let's add a SQL Server component to our application, that will scaffold the necessary code and configuration to add a SQL Server Docker container and will instruct EF Core to use that as its persistence source.

```yml
components:
  - type: database
    provider: sqlserver
    name: sqlserver
```

In the C# project, the `StoreDataContext` class will be created, and the Dependency Injection code will be configured inside `App.cs`.

## Model

For more in-depth explainations of the entities and the CodeArchitects.Platform implementation, see the [Codegen docs - Entities](../../sdk/codegen.md#entities).

```yml
entities:
  - name: User
    description: Represents a user of the eCommerce platform.
    fields:
      - name: username
        type: string
        description: The username of the user.
      - name: email
        type: string
        description: The email address of the user.
  - name: Product
    description: Represents a product available for purchase.
    fields:
      - name: name
        type: string
        description: The name of the product.
      - name: description
        type: string
        description: A description of the product.
      - name: price
        type: decimal
        description: The price of the product.
  - name: Order
    description: Represents an order order placed by users.
    fields:
      - name: quantity
        type: integer
        description: The quantity of product the order specifies.
      - name: product
        type: Product
        description: The product the order is referred to.
  - name: Cart
    description: Represents a cart that contains orders placed by the user, which are to be processed together.
    fields:
      - name: orders
        type: Order
        isArray: true
        description: The orders the cart is comprised of.
      - name: user
        type: User
        description: The user the cart belongs to.
```

This will generate the following C# classes.
Note that we can avoid to add an Id field, because it is inherited from base entity EntityBase.

```cs
public class User : EntityBase
{
    public string Username { get; set; }
    public string Email { get; set; }
}

public class Product : EntityBase
{
    public string Name { get; set; }
    public string Description { get; set; }
    public decimal Price { get; set; }
}

public class Order : EntityBase
{
    public int Quantity { get; set; }
    public Product? Product { get; set; }
}

public class Cart : EntityBase
{
    public List<Order>? Orders { get; set; }
    public User? User { get; set; }
}
```

Note the presence of navigation properties. We avoid as much as possible bi-directional navigations in order not to deal with circular references.
Furthermore, since `Order`s can only exist inside a cart, `Cart` and `Order` form an aggregate, with `Cart` being the aggregate root.

## Relationships

For more in-depth explainations of the relationship and the CodeArchitects.Platform implementation, see the [DAL/EF docs](../../dal/efcore.md#Associazioni) or [DAL/ADO.NET docs](../../dal/adonet.md#Associazioni).

The relationships between the entities are:

- An `Order` references a `Product`, which in return can be referenced by many different orders: the `Order`-`Product` relationship is many-to-one.
- A `Cart` belongs to a `User`, where each `User` can have multiple `Cart`s: the `Cart`-`User` relationship is many-to-one.
- A `Cart` is comprised of multiple `Order`s, where each `Order` is part of a single cart: the `Cart`-`Order` relationship is one-to-many.

Although EF Core is capable of inferring the relationships between the entity from the navigation properties, we should also state them explicitly inside the `association` section. This ensures the correct behavior of the repository methods. Furthermore, other repository providers (e.g., ADO.NET) might not be able to infer relationships like EF Core does.

```yml
associations:
  - type: associate
    multiplicity: one-to-many
    from:
      entity: Product
    to:
      entity: Order
      navigation: Product
  - type: associate
    multiplicity: one-to-many
    from:
      entity: User
    to:
      entity: Cart
      navigation: User
  - type: aggregate
    multiplicity: one-to-many
    from:
      entity: Cart
      navigation: Orders
    to:
      entity: Order
```

This will update the `OnModelCreating` method in the DataContext.
WARN: Remember to add missing usings (outside injection points or inside custom zones)

```cs
public class StoreDataContext : DbContext
{
  protected override void OnModelCreating(ModelBuilder modelBuilder)
  {
      modelBuilder.Entity<Order>()
          .HasOne(o => o.Product)
          .WithMany()
          .Associate();

      modelBuilder.Entity<User>()
          .HasMany<Cart>()
          .WithOne(c => c.User)
          .Associate();

      modelBuilder.Entity<Cart>()
          .HasMany(c => c.Orders)
          .WithOne()
          .Aggregate();
  }
}
```

## Migrations

Migrations are a way to manage changes to your database schema over time, making it easier to evolve your database along with your application.

When you start working with a new database or project, the first step is to create an initial migration. This migration captures the current state of your data model. To create our first migration, we run the following command inside the Package Manager Console.

```bash
Add-Migration Initial
```

This command will generate a new migration folder containing migration files and a snapshot of your data model's current state. After creating the initial migration, you'll find a new folder named "Migrations" in your project. Inside this folder, you'll see migration files named like "XXXXXXXXXXXXXX_Initial.cs.". The migrations will be automatically applied at application startup.

## Seeding

For more in-depth explainations of the seeding and the CodeArchitects.Platform implementation, see the [DAL docs](../../dal/dataaccesslayer.md#Seeding).

Database seeding is populating a database with an initial set of data. For example, the set of user roles for an authenticated application can be seeded at startup.

In our application, a class named `StoreDataSeed` was generated inside the `Infrastructure.Data` folder. The class contains a single method, `Seed`, where the initial set of data can be specified using the `ISeeder` parameter of the method, by calling `Add(entity)` on it. A set of entities of a particular type will be added only if its table is empty.

Let's add three products to our database.

```cs
public class StoreDataSeed : DataSeed
{
  public void Seed(ISeeder seeder)
  {
    seeder.Seed(
      new Product
      {
        Id = Guid.Parse("8d055ff5-f8fc-4434-b7c0-0cd18a53f8ee"),
        Name = "Wireless Headphones",
        Description = "High-quality audio wireless headphones.",
        Price = 149.99m
      },
      new Product
      {
        Id = Guid.Parse("a22c0e06-b1d7-4ad2-9cd8-38fb56bbc984"),
        Name = "Smartphone Case",
        Description = "Protects your smartphone.",
        Price = 29.99m
      },
      new Product
      {
        Id = Guid.Parse("783d857e-d11d-42c6-83fc-6241a06578c4"),
        Name = "Coffee Maker",
        Description = "Brews coffee with ease.",
        Price = 79.99m
      }
    );
  }
}
```

Next step: [Repository and service layer](repositories-and-service-layer.md)
