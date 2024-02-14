# Table entities

Sometimes, the database representation of entities can differ from the form we want to work with inside the business layer of our application. Although ORMs like EF Core provide many way to map between the two, in some cases you want to have two separate classes modelling the same entity: the table entity and the domain entity. The table entity is the model used to perform operations agaist the database with, while the domain entity is used to perform business-related operations. A layer of mapping is needed to communicate the changes between the two representations. For more in-depth explainations of the Table Entities, see the [DAL docs](../../dal/dataaccesslayer.md#creare-table-and-domain-entities).

## Code generation

In our simple example, this is not needed; however, in this section we will see how to implement such scenario. Adding a table entity is very similar to adding a domain entity, with the exception of the `type` field, which must be set to `table`. For example, if we were to create a table entity for the `Product` entity, we would write:

```yml
  - name: ProductTable
    type: table
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
```

The generated class looks the same as a regular entity, but the file is located inside the `Infrastructure/Data/Model` folder.

It is crucial to note that if you want to use tables for the data layer, they must not be mixed with domain entities. Therefore, each database table must be modelled by a table entity; then, for some or for all of them, there could be a corresponding domain entity. Given this requirement, it otften happens that only a limited number of table entities differ so much from their domain counterparts that a separation is needed; all other domain and table entities will pretty much look the same. In this case, writing the same yaml model for both the entities could be weary and error prone, so we use the type `table and domain` to generate both classes from a single yaml section.

```yml
  - name: ProductTable
    type: table and domain
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
```

## Mapped repository

If you are using repositories, like we are in this example project, it must use the table entity to query the database, as well as expose the domain entities to the callers. This requires a mapping between the two entities, so we should use a `MappedRepository`. To do so, we add the `useMappedRepository` field to the table entity, whose value must be the name of the domain entity. Also, remember to remove the `useRepository` flag from the domain entity.

```yml
  - name: ProductTable
    type: table
    description: Represents a product available for purchase.
    useMappedRepository: Product
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
```

This YAML will result in the following code:

```cs
public class ProductRepository : EFCoreMappedRepository<Infrastructure.Data.Model.ProductTable, Domain.Model.Product, Guid>, IProductRepository
{
  // --inject:CLASS_DEFINITION_1--
  public ProductRepository(IDataContext context) : base(context)
  { }

  // --inject:CLASS_DEFINITION_2--
}
```

`EFCoreMappedRepository` (or `AdoNetMappedRepository`) are abstract classes that define two abstract methods `TEntity TableToEntity(TTable table)` and `TTable EntityToTable(TEntity entity)`, which must be implemented by derived classes. These methods are responsible for performing the mapping in both directions. Press `CTRL + .` to implement the methods and be careful not to do so inside the injection zones. The mapping logic is not generated, but you can use AutoMapper to map the entities with a single line of code. You can inject `IMapper`, as well as any other registered dependency, inside the constructor, call the `Map` method inside the overridden method and be done with it.

```cs
public class ProductRepository : EFCoreMappedRepository<Infrastructure.Data.Model.ProductTable, Domain.Model.Product, Guid>, IProductRepository
{
  // --inject:CLASS_DEFINITION_1--
  private readonly IMapper _mapper;

  public ProductRepository(IDataContext context, IMapper mapper) : base(context)
  {
    _mapper = mapper;
  }

  protected override ProductTable EntityToTable(Product entity)
  {
    return _mapper.Map<ProductTable>(entity);
  }

  protected override Product TableToEntity(ProductTable table)
  {
    return _mapper.Map<Product>(table);
  }

  // --inject:CLASS_DEFINITION_2--
}
```

## Mapping

Of course, AutoMapper should be configured to map the entities in both directions. Doing that is as simple as we saw before with DTOs and domain entities. Just specify the name of the `entity` and the name of the `table`, and do not forget to add an inverse mapping too.

```yml
mappings:
  - entity: Product
    table: ProductTable
  - entity: Product
    table: ProductTable
    inverse: true
```

With the generated code being:

```cs
public class ProductProfile : Profile
{
  // <custom:parameters>
  // </custom:parameters>
  // <custom:constructor>
  public ProductProfile()
  {
    // </custom:constructor>
    MapProductEntityToProductTableTable();
    MapProductTableTableToProductEntity();
    // <custom:mappings>
    // </custom:mappings>
  }

  public void MapProductEntityToProductTableTable()
  {
    CreateMap<Domain.Model.Product, Infrastructure.Data.Model.ProductTable>()
    // <custom:mappings1>
    ; // </custom:mappings1>
  }

  public void MapProductTableTableToProductEntity()
  {
    CreateMap<Infrastructure.Data.Model.ProductTable, Domain.Model.Product>()
    // <custom:mappings2>
    ; // </custom:mappings2>
  }
  // <custom:methods>
  // </custom:methods>
}
```

Next step: [Dtos and mappings](../application-layer/dtos-and-mapping.md)