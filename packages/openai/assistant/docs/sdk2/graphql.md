# GraphQL Integration

GraphQL is an open-source data query and manipulation language for APIs, along with a runtime for executing queries with existing data. GraphQL can be used alternatively or in combination with REST APIs. You can define queries and mutations using the `contracts.operations` section. Let's define a basic query to read a list of `Customer` records from the database by specifying the operation type as `graphql_query`.

**Note:** When generating GraphQL operations for the first time, you need to perform a Clean operation on the solution.

```yaml
contracts:
  operations:
    - name: customers
      type: graphql_query
      description: Get customers
      entity:
        name: Customer
        isArray: true
```

This configuration will generate a method in the RootQuery class in the GraphQL folder that implements the query:

```csharp
public partial class RootQuery
{
  public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context
  // <custom:customersParameters>
  // </custom:customersParameters>
  )
  {
    // <custom:customersImplementation>
    // </custom:customersImplementation>
  }
}
```

The implementation of this method should return the list of Customer records, such as by using a repository (injecting it into the method) or EF Core.

You can define parameters to pass to the query. For example, if you want to filter by name, simply add a parameter, in this case named name.

```yml
contracts:
  operations:
    - name: customers
      type: graphql_query
      description: Get customers
      entity:
        name: Customer
        isArray: true
      parameters:
        - name: name
          type: string
          description: Name
          direction: in
          isOptional: true
```

This will add a parameter that can be used within the query:

```cs
public partial class RootQuery
{
  public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context, string name
  // <custom:customersParameters>
  // </custom:customersParameters>
  )
  {
    // <custom:customersImplementation>
    // </custom:customersImplementation>
  }
}
```

Attributes such as [UsePaging], [UseProjection], [UseFiltering], and [UseSorting] are supported through the annotations section:

```yml
contracts:
  operations:
    - name: customers
      type: graphql_query
      description: Get customers
      entity:
        name: Customer
        isArray: true
      annotations:
        - name: usePaging
          namespace: GraphQL
          value:
            inclueTotalCount: true
            maxPageSize: 500
        - name: useProjection
          namespace: GraphQL
        - name: useFiltering
          namespace: GraphQL
        - name: useSorting
          namespace: GraphQL
      parameters:
        - name: name
          type: string
          description: Name
          direction: in
          isOptional: true
```

Below is a sample implementation of this method using Entity Framework Core:

```cs
public partial class RootQuery
{
  [UsePaging(MaxPageSize = 500)]
  [UseProjection]
  [UseFiltering]
  [UseSorting]
  public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context, string name
  // <custom:customersParameters>
  , [Service] IMapper mapper
  // </custom:customersParameters>
  )
  {
    // <custom:customersImplementation>
    return context.Customer.Where(customer => customer.Name == name).ProjectTo<Dto.Customer>(mapper.ConfigurationProvider);
    // </custom:customersImplementation>
  }
}
```

You can also implement this method using a repository:

```cs
public partial class RootQuery
{
  [UsePaging(MaxPageSize = 500)]
  [UseProjection]
  [UseFiltering]
  [UseSorting]
  public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context, string name
  // <custom:customersParameters>
  , [Service] ICustomerEntityRepository repository, [Service] IMapper mapper
  // </custom:customersParameters>
  )
  {
    // <custom:customersImplementation>
    var customerEntity = await repository.GetAllAsync();
    return mapper.Map<IEnumerable<Dto.Customer>>(customerEntity);
    // </custom:customersImplementation>
  }
}
```

Mutations are handled similarly by specifying graphql_mutation as the operation type:

```yml
contracts:
  operations:
    - name: updateCustomer
      type: graphql_mutation
      description: Update customer
      parameters:
        - name: customer
          type: Customer
          description: Customer to be updated
          direction: in
        - name: success
          type: boolean
          description: Operation result
          direction: out
```

In this case, input and output parameters are specified. The first parameter contains the data of the Customer to be updated, while the second indicates whether the operation was successful. Mutations can also use attributes, just like queries.

```cs
public partial class Mutation
{
  // <custom:updateCustomerAttributes>
  // </custom:updateCustomerAttributes>
  public async Task<bool> UpdateCustomer(Customer customer, [Service] BusinessDataContext context
  // <custom:updateCustomerParameters>
  , [Service] IMapper mapper
  // </custom:updateCustomerParameters>
  )
  {
    // <custom:updateCustomerImplementation>
    var customerEntity = mapper.Map<CustomerEntity>(customer);
    context.Update(customerEntity);
    await context.SaveChangesAsync();
    return true;
    // </custom:updateCustomerImplementation>
  }
}
```

On the client side, GraphQL operations can be invoked similarly to REST operations. By adding at least one GraphQL operation to a microservice reachable from the client, a GraphQL service will be generated and can be accessed directly from the microservice's instance. You can access the available queries and mutations.

Example of a GraphQL query on the client:

```typescript
await this.delegates.business.graphQL
  .customers(
    'id',
    'email',
    x => x.surname,
    c => ShGraphQL.queryArray(c.demographics, 'name', 'value')
  )
  .paginate()
  .toPromise();
```

In the query, you can observe:

- Selecting specific fields like id, email, and surname of the customer.
- Fields can be selected by simply specifying their names or by defining a callback (as in the case of surname).
- Fields of type array (e.g., demographics) should be selected using a callback and the queryArray function from ShGraphQL.
- Considering that pagination has been enabled, you need to use the paginate method before executing the query. You can optionally specify the pageIndex and pageSize (e.g., .paginate({ pageSize: 2, pageIndex: 1 })).
- With filtering and sorting enabled, you can optionally filter and sort the data to retrieve, as shown in the example.
- If you add an input parameter to the operation:

```yml
contracts:
  operations:
    - name: customers
      type: graphql_query
      description: Get customers
      entity:
        name: Customer
        isArray: true
      parameters:
        - name: name
          type: string
          description: name
          direction: in
          isOptional: true
```

The first parameter in the generated operation will match the one defined in the YAML:

```typescript
await this.delegates.business.graphQL
  .customers(
    'PARAMETRO NAME',
    'id',
    'email',
    x => x.surname,
    c => ShGraphQL.queryArray(c.demographics, 'name', 'value')
  )
  .paginate()
  .toPromise();
```

You can also model a query that returns a single instance of the specified DTO:

```yml
- name: customer
  type: graphql_query
  description: Retrieves a customer
  entity:
    name: Customer
  parameters:
    - name: id
      type: uuid
      description: id
```

This query can be used on the client as follows:

```typescript
const result = await this.delegates.business.graphQL
  .customer(customer.id, 'id', 'email', 'surname', 'version', 'updateDate', c =>
    ShGraphQL.queryArray(c.demographics, 'name', 'value')
  )
  .toPromise();
```

Where result will contain the envelope with the single customer inside.

Note: In the modeling of graphql_query operations, return parameters should never be specified.

Regarding the modeling of mutations, they can include return parameters:

```yml
- name: updateCustomer
  type: graphql_mutation
  description: Update customer
  parameters:
    - name: customer
      type: Customer
      description: Customer to be updated
      direction: in
    - name: success
      type: boolean
      description: Operation result
      direction: out
```

This mutation can be invoked from the client as follows:

```typescript
await this.delegates.business.graphQL.updateCustomer(this.payload.customer).toPromise();
```

Among the return parameters, you can also include a DTO on which to perform a query. For example:

```yml
- name: updateCustomerAndReturn
  type: graphql_mutation
  description: Update customer and return it
  parameters:
    - name: customer
      type: Customer
      description: Customer to be updated
      direction: in
    - name: customer
      type: Customer
      description: Updated customer
      direction: out
```

This mutation can be invoked from the client as follows:

```typescript
await this.delegates.business.graphQL
  .updateCustomerAndReturn(this.payload.customer, 'email', 'name', 'updateDate')
  .toPromise();
```

Please note that if you return a DTO, you will always need to include at least one field on which to perform the query.
