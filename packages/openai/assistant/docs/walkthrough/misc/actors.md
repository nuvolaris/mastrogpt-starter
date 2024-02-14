# Actors

In our eCommerce application, we will model a Cart actor for handling shopping cart operations efficiently. We'll create an actor that can be used to add and remove products from the cart and perform the checkout process. For more in-depth explainations of the actors and the CodeArchitects.Platform implementation, see the [Actors](../../sdk/actors.md).

## Defining the Cart Actor

We'll define an ICartActor interface that represents the methods available for interacting with the cart, and then we'll implement this interface in the `CartActor` class.

```yml
actors:
  - name: CartActor
    state:
      components:
        - name: cartItems
          type: dictionary
          description: Cart items
          dictionaryOptions:
            key: string
            value: integer
    methods:
      - name: addProductAsync
        description: Adds a quantity of product to the cart.
        parameters:
          - name: productId
            description: The id of the product to add.
            direction: in
            type: uuid
          - name: quantity
            description: The quantity of product to add.
            direction: in
            type: integer
      - name: removeProductAsync
        description: Removes a quantity of product to the cart.
        parameters:
          - name: productId
            description: The id of the product to add.
            direction: in
            type: uuid
          - name: quantity
            description: The quantity of product to remove.
            direction: in
            type: integer
      - name: getProductIdsAsync
        description: Retrieves the ids of the products added to the cart.
        parameters:
          - name: ids
            description: The product ids.
            direction: retval
            type: uuid
            isArray: true
```

We specified the state components and the methods. Here's the generated ICartActor interface:

```cs
public interface ICartActor
{
  /// <summary>
  /// Adds a quantity of product to the cart.
  /// </summary>
  /// <param name="productId">The id of the product to add.</param>
  /// <param name="quantity">The quantity of product to add.</param>
  /// <param name="CancellationToken">Cancellation Token</param>
  Task AddProductAsync(Guid productId, int quantity, CancellationToken cancellationToken);

  /// <summary>
  /// Removes a quantity of product to the cart.
  /// </summary>
  /// <param name="productId">The id of the product to add.</param>
  /// <param name="quantity">The quantity of product to remove.</param>
  /// <param name="CancellationToken">Cancellation Token</param>
  Task RemoveProductAsync(Guid productId, int quantity, CancellationToken cancellationToken);

  /// <summary>
  /// Retrieves the ids of the products added to the cart.
  /// </summary>
  /// <param name="CancellationToken">Cancellation Token</param>
  Task<IEnumerable<Guid>> GetProductIdsAsync(CancellationToken cancellationToken);
}
```

In this interface, we have methods to add and remove products from the cart and to retrieve the product ids. Now, let's implement the `CartActor` class:

```cs
[Actor]
public class CartActor : ICartActor
// <custom:baseList>
// </custom:baseList>
{
  [State]
  protected Dictionary<string, int> _cartItems;

  // <custom:fields>
  // </custom:fields>
  // <custom:constructorAttributes>
  // </custom:constructorAttributes>
  public CartActor(Dictionary<string, int> cartItems
  // <custom:constructorDependencies>
  // </custom:constructorDependencies>
  )
  {
    _cartItems = cartItems;
    // <custom:constructor>
    // </custom:constructor>
  }

  // <custom:methods>

  public async Task AddProductAsync(Guid productId, int quantity)
  {
    _cartItems[productId] = _cartItems.GetValueOrDefault(productId) + quantity;
    return Task.CompletedTask;
  }
  
  public async Task RemoveProductAsync(Guid productId, int quantity)
  {
    _cartItems[productId] = _cartItems.GetValueOrDefault(productId) - quantity;
    return Task.CompletedTask;
  }
  
  public async Task<IEnumerable<Guid>> GetCartItemIdsAsync()
  {
    return Task.FromResult(_cartItems.Keys);
  }
  // </custom:methods>
}
```

In the `CartActor` class, we use the `[State]` attribute to manage the state of the cart, specifically the `_cartItems` dictionary, which holds the product IDs and quantities in the cart.

## Actor Factory

To interact with the `Cart` actor, we'll create an actor proxy using a factory. CAEP automatically generates a factory interface for each actor, making it easy to create and interact with actors. Here's an example of an actor factory for our CartActor:

```cs
[ActorFactory(typeof(CartActor))]
public interface ICartActorFactory
{
    ICartActor Get(string actorId);
}
```

We can resolve the factory using dependency injection and use it to create actor instances.

```cs
ICartActorFactory cartActorFactory = ...; // Resolved through DI

ICartActor cartActor = cartActorFactory.Get("user123_cart");
await cartActor.AddProductAsync("123", 2);
await cartActor.RemoveProductAsync("456", 1);
IEnumerable<CartItem> cartItems = await cartActor.GetCartItemsAsync();
```

Next step: [Presentation Layer](../presentation-layer/presentation.md)