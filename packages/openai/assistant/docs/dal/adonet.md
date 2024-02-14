# DAL con ADO.NET

Per utilizzare Dapper come ORM, che a sua volta utilizza l'implementazione ADO.NET del repository, impostare appropriatamente il valore del campo `data.orm` dello yml.

```yml
data:
  orm: Dapper
```

## Entità

Il DAL ADO.NET utilizza la classe base `ModelConfiguration` per la configurazione di entità e relazioni. Per configurare il modello relazionale, è necessario estendere questa classe e dichiarare le entità e le relazioni tra di esse.

Per quanto riguarda le entità, esse si dichiarano utilizzando il metodo `Entity` che accetta come parametro di tipo l'entità e come parametro una lambda che configura le proprietà dell'entità.

Ad esempio, supponiamo di avere un'entità modellata dal seguente yml:

```yml
entities:
  - name: Category
    description: A category
    type: entity
    useRepository: true
    fields:
      - name: name
        type: string
        description: Category name
      - name: description
        type: string
        description: Category description
```

Questo, oltre a generare l'entità in sé, grazie alla flag `useRepository`, genererà la seguente configurazione:

```cs
public class MyModelConfiguration : ModelConfiguration
{
  protected override void Configure()
  {
    Entity<Category>(builder =>
    {
      // configurazione
    });
  }
}
```

## Associazioni

Le associazioni vengono definite attraverso i metodi `Aggregate` e `Associate`, che accettano come parametri di tipo le due entità da mettere in relazione e come parametro una lambda che configura la relazione tramite un'API fluent.

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
public class MyModelConfiguration : ModelConfiguration
{
  protected override void Configure()
  {
    Aggregate<Customer, Address>(builder => builder
      .OneToOne()
      .Navigation(x => x.ShippingAddress)
      .InverseNavigation(x => x.Customer));
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
public class MyModelConfiguration : ModelConfiguration
{
  protected override void Configure()
  {
    Associate<Customer, Address>(builder => builder
      .OneToOne()
      .Navigation(x => x.ShippingAddress)
      .InverseNavigation(x => x.Customer));
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
public class MyModelConfiguration : ModelConfiguration
{
  protected override void Configure()
  {
    Aggregate<Cart, Product>(builder => builder
      .OneToMany()
      .Navigation(x => x.Products)
      .InverseNavigation(x => x.Cart));
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
public class MyModelConfiguration : ModelConfiguration
{
  protected override void Configure()
  {
    Associate<Cart, Product>(builder => builder
      .OneToMany()
      .Navigation(x => x.Products)
      .InverseNavigation(x => x.Cart));
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
public class MyModelConfiguration : ModelConfiguration
{
  protected override void Configure()
  {
    Associate<Student, Teacher>(builder => builder
      .ManyToMany()
      .Navigation(x => x.Teachers)
      .InverseNavigation(x => x.Students));
  }
}
```
