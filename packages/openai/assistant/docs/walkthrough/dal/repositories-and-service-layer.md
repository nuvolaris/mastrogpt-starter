# Repositories and service layer

In this section, we will guide you through implementing repositories and a service layer in your CAEP-based eCommerce application. Repositories provide a structured way to access data in your database, while a service layer encapsulates the business logic for your application. For more in-depth explainations of the repository pattern and the CodeArchitects.Platform implementation, see the [Data Access Layer docs](../../dal/dataaccesslayer.md).

## Repositories

Let's create repositories for the aggregates we want to access in your data layer. For example, let's create `ProductRepository`, `CartRepository`, and `UserRepository`. We will use the `CartRepository` to access both `Cart`s and their `Order`s, since they belong to the same aggregate. To do so, let's add the `useRepository` flag to the entities that will have a repository and set it to `true`. For example:

```yml
entities:
  - name: User
    description: Represents a user of the eCommerce platform.
    useRepository: true
# rest of the YAML...
```

The generated interfaces will extend `IRepository<TEntity, TKey>`, and will inherit the base data access methods. For now, we won't add others.

## Service layer

Now, let's create a service interface and implementation for managing carts. The following section specifies a service named CartService that will be in charge of managing `Cart`s.

```yml
dependencies:
  - name: Cart
    type: Scoped
    methods:
      - name: getCartByIdAsync
        description: Retrieves a cart by its unique identifier.
        mode: async
        parameters:
          - name: id
            description: The unique identifier of the cart to retrieve.
            direction: in
            type: uuid
          - name: cart
            type: Cart
            direction: retval
            isOptional: true
            description: The retrieved cart.
```

This will create the `CartService` class and its interface `ICartService`, and will add them to the DI container with the specified lifetime. Let's implement the `GetCartByIdAsync` method by forwarding it to the repository, making sure to include details about its order and the product the order is related to; more complex logic can be added in the future.
WARN: Remember to add missing usings in the interface and class files (outside injection points or inside custom zones)

```cs
public class CartService : ICartService
{
    private readonly ICartRepository _cartRepository;

    public CartService(ICartRepository cartRepository)
    {
        _cartRepository = cartRepository;
    }

    public Task<Cart?> GetCartByIdAsync(Guid id)
    {
      return _cartRepository.FindAsync(id, _ => _
        .Include(cart => cart.Orders, _ => _
          .Include(order => order.Product)));
    }
}
```

Next step: [Repository providers](repository-providers.md)