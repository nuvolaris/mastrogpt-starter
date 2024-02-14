# SignalR

SignalR is an open-source library for adding real-time functionality to web applications. It enables bidirectional communication between a web server and clients, allowing instant updates and notifications to be sent from the server to connected clients and vice versa. CAEP enables the use of SignalR with a simple abstraction. For more in-depth explainations of the actors and the CodeArchitects.Platform implementation, see the [Operations Docs - Signalr Section](../../sdk/operations.md#signalr).

## Creating a SignalR subscription

Let's now create a subscription for receiving notifications when a product is available. We add a new operation:

```yml
- name: productAvailable
  type: signalr_subscription
  description: Notify clients when a product is available again
  parameters:
    - name: productId
      description: The id of the product
      direction: in
      type: string
```

We will have to implement the `ProductAvailable` method of the `CartHub` class.

```cs
public Task ProductAvailable(ProductAvailableParams @params)
{
    return _context.Clients.All.ProductAvailable(@params);
}
```

## Sending notifications

To send a notification to the clients upon product availability, we can just inject the `ICartHub` interface inside the `ProductEventHandler` class and use it when the `ProductAvailableEvent` is received:

```cs
public class ProductEventHandler : IMessageHandler<ProductUnavailableEvent>, IMessageHandler<ProductAvailableEvent>
{
    private readonly ICartHub _hub;

    public ProductEventHandler(ICartHub hub)
    {
        _hub = hub;
    }

    public async Task HandleAsync(ProductAvailableEvent message)
    {
        await _hub.ProductAvailable(new ProductAvailableParams { ProductId = message.ProductId });
    }
}
```

## Subscribing to the Hub Method

Subscribing to a method in the StoreHub called ProductAvailable is straightforward with the SignalR integration. You can achieve this by applying the SignalREvent decorator to a method within a scenario's state. Here's how to do it:

```ts
@SignalREvent({
  hub: StoreHub,
  methodName: 'ProductAvailable'
})
public onProductAvailable(params: IProductAvailableParams) {
  console.log(`Product available ${params.productId}`);
}
```

This code sets up a subscription to the ProductAvailable method of the StoreHub. When this method is invoked on the server, your client-side code will automatically receive and handle the incoming notifications. In this example, it logs a message to the console when a product becomes available.

This subscription mechanism enables you to respond to real-time updates and notifications sent from the server, making your web application interactive and responsive to changes.

Next step: [Secrets](../misc/secrets.md)
