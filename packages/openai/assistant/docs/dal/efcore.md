# DAL con Entity Framework Core 7

Per utilizzare Entity Framework Core come ORM, impostare appropriatamente il valore del campo `data.orm` dello yml.

```yml
data:
  orm: EntityFrameworkCore
```

## Configurazione

Per utilizzare le funzionalità della libreria CodeArchitects.Platform.Data.EntityFrameworkCore all'interno di un'applicazione ASP.NET Core, è necessario configurare il container di Dependency Injection attraverso gli appositi metodi.

In particolare, dopo aver abilitato l'uso di EFCore attraverso

```cs
services.AddDbContext<MyDbContext>(...);
```

è necessario configurare l'intero DAL tramite il seguente metodo:

```cs
services.AddData<MyDbContext>();
```

## Seeding

Per effettuare il seeding del database, è sufficiente utilizzare l'overload di `AddData` che consente di specificare ulteriori opzioni e successivamente utilizzare il metodo `UseSeed`:

```cs
services.AddData<MyDbContext>(options => options.UseSeed<MyDataSeed>());
```

per poi effettuare il seeding tramite il metodo di estensione `Seed`, tipicamente dopo la chiamata al metodo `Migrate` (o `EnsureCreated` se non si utilizzano le migrazioni).

```cs
using (IServiceScope scope = app.ApplicationServices.CreateScope())
{
  MyDbContext context = scope.Services.GetRequiredService<MyDbContext>();
  context.Migrate();
  context.Seed();
}
```

## CAEP extensions

L'estensione CAEP per EFCore permette di abilitare una serie di funzionalità, tra cui:

- Multitenancy
- Soft delete

Per utilizzare questa estensione, utilizzare il metodo di estensione `UseCaep` del `DbContextOptionsBuilder` all'interno della chiamata ad `AddDbContext` (o all'interno del metodo `OnConfiguring` di `DbContext`).

```cs
services.AddDbContext<MyDbContext>(options => options
  .UseSqlServer(...)
  .UseCaep()); // Da inserire dopo la chiamata all'estensione del provider (UseSqlServer in questo caso)
```

## Multitenancy

Il multi-tenancy è un concetto utilizzato per descrivere la capacità di un'applicazione web di fornire servizi a più clienti (noti come "tenant") all'interno di un'unica istanza di software. Ciò significa che un'unica versione dell'applicazione è in grado di gestire dati e configurazioni per più clienti, utilizzando meccanismi di isolamento per garantire che i dati e le configurazioni dei singoli tenant non si interfaccino tra loro.

Il multi-tenancy può essere implementato in diversi modi, a seconda delle esigenze dell'applicazione. Ad esempio, può essere realizzato utilizzando database separati per ogni tenant (separate database), oppure utilizzando schemi separati all'interno dello stesso database (shared database, separate schema) per isolare i dati dei tenant.

Quando non è possibile adottare nessuna delle due soluzioni, è necessario utilizzare meccanismi di isolamento a livello di codice per garantire che le azioni di un tenant non interferiscano con gli altri.

Per abilitare la separazione a livello di codice, si può usare l'estensione `UseMultitenancy` all'interno di `UseCaep`:

```cs
services.AddDbContext<MyContext>(options => options
  .UseSqlServer("...")
  .UseCaep(caep => caep.UseMultitenancy()));
```
  
Per indicare che un'entità è multi-tenant è sufficiente utilizzare il metodo di estensione `IsMultiTenant` all'interno del metodo `OnModelCreating`. Supponendo di avere la seguente entità:

```cs
public class MyEntity
{
  public Guid Id { get; set; }
  public Guid TenantId { get; set; }
  ...
}
```

Si avrebbe:

```cs
modelBuilder.Entity<MyEntity>(entity =>
{
  entity.IsMultiTenant(x => x.TenantId);
});
```

Una volta fatto ciò, le query effettuate su questa entità saranno automaticamente filtrate secondo il tenant dell'utente corrente.

> Nota: Di default, è necessario utilizzare l'interfaccia IIdentityProfile per recuperare il tenant id dai claims dell'utente corrente.

## Soft delete

Il soft delete è un meccanismo che consente di eliminare logicamente un record dal database senza eliminarlo fisicamente. Invece di eliminare fisicamente il record dal database, viene impostato un indicatore che segnala che il record è stato eliminato. Questo meccanismo consente di mantenere una traccia dei record eliminati e di poterli eventualmente ripristinare in futuro. Il soft delete può essere implementato utilizzando una colonna di stato (ad esempio, una colonna `IsDeleted` con valori `true` e `false`).

Per abilitare il meccanismo di soft delete, utilizzare il metodo `UseSoftDelete` all'interno di `UseCaep`:

```cs
services.AddDbContext<MyContext>(options => options
  .UseSqlServer("...")
  .UseCaep(caep => caep.UseSoftDelete()));
```

Nel metodo `OnModelCreating`, utilizzare il metodo `IsSoftDelete` per marcare la proprietà da utilizzare come colonna di stato:

```cs
modelBuilder.Entity<MyEntity>(entity =>
{
  entity.IsSoftDelete(x => x.IsDeleted);
});
```

## Associazioni

I tipi di associazione vengono definite attraverso i metodi di estensione `Aggregate()` e `Associate()`, da usare in congiunzione con le fluent API di configurazione di EFCore.

### Configurazione associazione uno-a-uno, intra-aggregato

Supponiamo di avere le entità `Customer` e `Address`, in relazione uno-a-uno e facenti parte dello stesso aggregato, con `Customer` come Aggregate Root.

```cs
public class Customer
{
  public Guid Id { get; set; }
  public Address? ShippingAddress { get; set; }
}

public class Address
{
  public Guid Id { get; set; }
  public Customer? Customer { get; set; }
}
```

La relazione è modellabile con il seguente yml:

```yml
associations:
  - type: aggregate
    multiplicity: one-to-one
    from:
      entity: Customer
      navigation: ShippingAddress
    to:
      entity: Address
      navigation: Customer
```

Che genererà la seguente configurazione:

```cs
public class MyDbContext : DbContext
{
  protected override void OnModelCreating(ModelBuilder modelBuilder)
  {
    modelBuilder.Entity<Customer>(entity =>
    {
      entity
        .HasOne(x => x.ShippingAddress)
        .WithOne(x => x.Customer)
        .Aggregate()
        .HasForeignKey<Address>();
    });
  }
}
```

### Configurazione associazione uno-a-uno, inter-aggregato

Supponiamo di avere le entità `Customer` e `Address`, in relazione uno-a-uno e non facenti parte dello stesso aggregato.

```cs
public class Customer
{
  public Guid Id { get; set; }
  public Address? ShippingAddress { get; set; }
}

public class Address
{
  public Guid Id { get; set; }
  public Customer? Customer { get; set; }
}
```

La relazione è modellabile con il seguente yml:

```yml
associations:
  - type: associate
    multiplicity: one-to-one
    from:
      entity: Customer
      navigation: ShippingAddress
    to:
      entity: Address
      navigation: Customer
```

Che genererà la seguente configurazione:

```cs
public class MyDbContext : DbContext
{
  protected override void OnModelCreating(ModelBuilder modelBuilder)
  {
    modelBuilder.Entity<Customer>(entity =>
    {
      entity
        .HasOne(x => x.ShippingAddress)
        .WithOne(x => x.Customer)
        .Associate()
        .HasForeignKey<Address>();
    });
  }
}
```

### Configurazione associazione uno-a-molti, intra-aggregato

Supponiamo di avere le entità `Cart` e `Product`, in relazione uno-a-molti e facenti parte dello stesso aggregato, con `Cart` come Aggregate Root.

```cs
public class Cart
{
  public Guid Id { get; set; }
  public IEnumerable<Product>? Products { get; set; }
}

public class Product
{
  public Guid Id { get; set; }
  public Cart? Cart { get; set; }
}
```

La relazione è modellabile con il seguente yml:

```yml
associations:
  - type: aggregate
    multiplicity: one-to-many
    from:
      entity: Cart
      navigation: Products
    to:
      entity: Product
      navigation: Cart
```

Che genererà la seguente configurazione:

```cs
public class MyDbContext : DbContext
{
  protected override void OnModelCreating(ModelBuilder modelBuilder)
  {
    modelBuilder.Entity<Product>(entity =>
    {
      entity
        .HasMany(x => x.Products)
        .WithOne(x => x.Cart)
        .Aggregate();
    });
  }
}
```

### Configurazione associazione uno-a-molti, inter-aggregato

Supponiamo di avere le entità `Cart` e `Product`, in relazione uno-a-molti e non facenti parte dello stesso aggregato.

```cs
public class Cart
{
  public Guid Id { get; set; }
  public IEnumerable<Product>? Products { get; set; }
}

public class Product
{
  public Guid Id { get; set; }
  public Cart? Cart { get; set; }
}
```

La relazione è modellabile con il seguente yml:

```yml
associations:
  - type: associate
    multiplicity: one-to-many
    from:
      entity: Cart
      navigation: Products
    to:
      entity: Product
      navigation: Cart
```

Che genererà la seguente configurazione:

```cs
public class MyDbContext : DbContext
{
  protected override void OnModelCreating(ModelBuilder modelBuilder)
  {
    modelBuilder.Entity<Product>(entity =>
    {
      entity
        .HasMany(x => x.Products)
        .WithOne(x => x.Cart)
        .Associate();
    });
  }
}
```

### Configurazione associazione molti-a-molti

Supponiamo di avere le entità `Student` e `Teacher`, in relazione molti-a-molti.

```cs
public class Student
{
  public Guid Id { get; set; }
  public IEnumerable<Teacher>? Teachers { get; set; }
}

public class Teacher
{
  public Guid Id { get; set; }
  public IEnumerable<Student>? Students { get; set; }
}
```

La relazione è modellabile con il seguente yml:

```yml
associations:
  - type: associate
    multiplicity: many-to-many
    from:
      entity: Student
      navigation: Teachers
    to:
      entity: Teacher
      navigation: Students
```

Che genererà la seguente configurazione:

```cs
public class MyDbContext : DbContext
{
  protected override void OnModelCreating(ModelBuilder modelBuilder)
  {
    modelBuilder.Entity<Student>(entity =>
    {
      entity
        .HasMany(x => x.Teachers)
        .WithMany(x => x.Students);
    });
  }
}
```
