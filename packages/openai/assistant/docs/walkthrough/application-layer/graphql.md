# REST API with GraphQL Walkthrough

Let's see how to convert a REST operation into a GraphQL operation. For more in-depth explainations of GraphQL, see the [GraphQL Integration](../../sdk/graphql.md).

For example convert `getProductById`. First, we change the type of the operation in the YAML file to `graphql_query`. We also remove the `out` parameter and instead, add an `entity` section with `name` set to `Cart` and `isOptional` set to `true`.

```yml
contracts:
  operations:
    - name: getCartById
      type: graphql_query
      entity:
        name: Cart
        isOptional: true
      description: Retrieves a cart by its unique identifier.
      parameters:
        - name: id
          description: The unique identifier of the cart to retrieve.
          direction: in
          type: uuid
```

This configuration will generate a GraphQL query operation for fetching a product by its id. A method for this query will be generated in the `RootQuery` class within the GraphQL folder of your project. The generated method will have the name you specified in the YAML file (e.g., GetProductById).

```cs
public partial class RootQuery
{
  public async Task<Dto.Product> GetProductById(Guid id, [Service] BusinessDataContext context
  // <custom:getProductByIdParameters>
  // </custom:getProductByIdParameters>
  )
  {
    // <custom:getProductByIdImplementation>
    throw new NotImplementedException();
    // </custom:getProductByIdImplementation>
  }
}
```

We can inject services as parameter to the method, as long as we decorate them with the `[Service]` attribute. The implementation of this GraphQL operation may look like this:

```cs
public partial class RootQuery
{
  public async Task<Dto.Product> GetProductById(Guid id, [Service] BusinessDataContext context
  // <custom:getProductByIdParameters>
  , [Service] IMapper mapper, [Service] ICartService cartService
  // </custom:getProductByIdParameters>
  )
  {
    // <custom:getProductByIdImplementation>
    Cart? cart = await cartService.GetCartByIdAsync(id);
    if (cart is null)
      return null;

    return _mapper.Map<CartDto>(cart);
    // </custom:getProductByIdImplementation>
  }
}
```

Next step: [Identity](identity)
