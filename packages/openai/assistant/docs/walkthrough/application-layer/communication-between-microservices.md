# Communication between microservices

It is time to make our example more complex by adding a new microservice to handle the warehouse of functionality of the eCommerce application.

## Adding the Warehouse microservice

We will call the new microservice `Warehouse` and have a `Product` entity as well, where this time it will contain information about the quantity at hand.

```yml
name: Warehouse
type: service
description: Warehouse service
namespace: App.ShoppingCart.Warehouse
target:
  framework: net
  version: 7

data:
  orm: EntityFrameworkCore

components:
  - type: database
    provider: sqlserver
    name: sqlserver

entities:
  - name: Product
    description: Represents a product in the warehouse.
    fields:
      - name: id
        type: uuid
        description: The unique identifier for the product.
      - name: name
        type: string
        description: The name of the product.
      - name: description
        type: string
        description: A description of the product.
      - name: quantity
        type: integer
        description: The quantity of the product in stock.

dependencies:
  - name: Product
    type: Scoped
    methods:
      - name: addStock
        description: Adds stock of a product to the warehouse.
        mode: async
        parameters:
          - name: productId
            type: uuid
            description: The unique identifier of the product to update.
            direction: in
          - name: quantity
            type: integer
            description: The quantity of stock to add.
            direction: in
          - name: newQuantity
            type: integer
            description: The quantity after addition.
            direction: retval
      - name: withdrawStock
        description: Withdraws stock of a product to the warehouse.
        mode: async
        parameters:
          - name: productId
            type: uuid
            description: The unique identifier of the product to update.
            direction: in
          - name: quantity
            type: integer
            description: The quantity of stock to withdraw.
            direction: in
          - name: newQuantity
            type: integer
            description: The quantity after withdrawal.
            direction: retval

contracts:
  operations:
    - name: addStock
      type: http_post
      description: Adds stock of a product to the warehouse.
      parameters:
        - name: productId
          type: uuid
          description: The unique identifier of the product to update.
          direction: in
        - name: quantity
          type: integer
          description: The quantity of stock to add.
          direction: in
        - name: newQuantity
          type: integer
          description: The quantity after addition.
          direction: out
    - name: withdrawStock
      type: http_post
      description: Withdraws stock of a product from the warehouse.
      parameters:
        - name: productId
          type: uuid
          description: The unique identifier of the product to update.
          direction: in
        - name: quantity
          type: integer
          description: The quantity of stock to withdraw.
          direction: in
        - name: newQuantity
          type: integer
          description: The quantity after withdrawal.
          direction: out
```

The two operations are there to simply update the quantity at hand of a product in the warehouse. There are two noteworthy events that can happen:

1. a product becomes unavailable when a withdrawal reduces its quantity to zero
2. a product becomes available when its quantity is zero and an addition happens

The `Store` microservice is interested in those two events because it should tell to the user which products are available for purchase.

## Gateway

These two services run on different docker container, which are exposed to different ports of your machine. The SPA gateway, which is automatically generated from the start, is a component that sits in between the client and the microservices. The gateway is exposed on another port of your machine and the client will only know about this port; then the gateway will redirect the requests to the appropriate microservice automatically, based on the request path. Gateways' YAMLs can be found in the `codegen/model` folder and now it will look like this:

```yml
name: SPA
type: gateway
description: SPA gateway
port: 10000
services:
- service: Warehouse
- service: Store
- service: Shell
```

You can modify this YAML for gateway customization.

## Messaging

We will use messaging to handle the communication of these events. Start by defining the messages and their corresponding handlers in your YAML configuration file. In this example, we have two messages, `ProductUnavailableEvent` and `ProductAvailableEvent`, and a handler named `ProductEventHandler` that handles both messages.

We need to add a component of type `messagebus` to both microservices.

```yml
components:
  - type: messagebus
    provider: rabbit
    name: messagebus
  # other components...
```

This will add a RabbitMQ container and all the necessary plumbing to connect it to the microservices. Note that the name must be the same for all microservices, otherwise multiple message busses will be generated. Then, we need to define the messages and their handler.

```yml
messaging:
  handlers:
    - name: ProductEventHandler
      description: Handler for ProductUnavailableEvent and ProductAvailableEvent
      messages:
        - ProductUnavailableEvent
        - ProductAvailableEvent
  messages:
    - name: ProductUnavailableEvent
      description: Event indicating a product is unavailable.
      fields:
        - name: productId
          description: The ID of the unavailable product.
          type: uuid
    - name: ProductAvailableEvent
      description: Event indicating a product is available.
      fields:
        - name: productId
          description: The ID of the available product.
          type: uuid
```

This configuration generates C# classes for the messages and the handler with appropriate fields. In the generated C# code, implement the HandleAsync method for each message type within the "ProductEventHandler" class. This method will contain the logic to handle the received messages, which for now we won't implement, because later we will show how to send notifications to the client upon the occurence of these events.

```cs
public class ProductEventHandler : IMessageHandler<ProductUnavailableEvent>, IMessageHandler<ProductAvailableEvent>
{
    public async Task HandleAsync(ProductUnavailableEvent message)
    {
        // Handle ProductUnavailableEvent logic here
        // Access message.productId to perform actions
    }

    public async Task HandleAsync(ProductAvailableEvent message)
    {
        // Handle ProductAvailableEvent logic here
        // Access message.productId to perform actions
    }
}
```

To send a message from the Warehouse microservice, we will use the `IMessageBus` interface.

```cs
public class ProductService : IProductService
{
    private readonly WarehouseDataContext _dataContext;
    private readonly IMessageBus _messageBus;

    public ProductService(WarehouseDataContext dataContext, IMessageBus messageBus)
    {
        _dataContext = dataContext;
        _messageBus = messageBus;
    }

    public Task<int> AddStock(Guid productId, int quantity)
    {
        if (quantity <= 0)
            throw new InvalidOperationException();

        Product product = await _dataContext.Set<Product>().FirstAsync(x => x.Id == productId);
        bool wasUnavailable = product.Quantity == 0;

        product.Quantity += quantity;
        await _dataContext.SaveChangesAsync();

        if (wasUnavailable)
        {
            await _messageBus.SendAsync(new ProductAvailableEvent { ProductId = productId });
        }
    }

    public Task<int> WithdrawStock(Guid productId, int quantity)
    {
        if (quantity <= 0)
            throw new InvalidOperationException();

        Product product = await _dataContext.Set<Product>().FirstAsync(x => x.Id == productId);
        if (quantity > product.Quantity)
            throw new InvalidOperationException();

        product.Quantity -= quantity;
        await _dataContext.SaveChangesAsync();

        if (product.Quantity == 0)
        {
            await _messageBus.SendAsync(new ProductUnavailableEvent { ProductId = productId });
        }
    }
}
```

## Service-to-service invocation

Messaging is good for communicating messages that can be handled in an asynchronous way, that is, when a response to the message is not expected or, at least, not needed right away. Sometimes, the response to an action is required immediately; in this kind of scenarios, a microservice can directly invoke another one (via HTTP or gRPC) and block until the response is received.

For this simple example, we imagine that we defined a 'Payment' microservice that will be directly invoked to process an order from the 'Order' microservice. Let's define an operation on the newly created microservice:

```yml
contracts:
  operations:
    - name: processPayment
      type: http_post
      description: Process payment for a customer order
      parameters:
        - name: orderId
          type: uuid
          description: The id of the order to process payment for.
        - name: paymentResult
          type: boolean
          description: True if the payment is successful, false otherwise.
```

Imagine we want to invoke this API from the 'Order' microservice. We add the `services` section in its yml and specify the name of the 'Payment' microservice

```yml
services:
  - name: Payment
```

This will generate the `IPaymentService` interface:

```cs
public interface IPaymentService
{
    public async Task<ProcessPaymentResponse> ProcessPaymentAsync(Guid orderId, CancellationToken cancellationToken = default);
}
```

We can inject this service and use it anywhere it is required to invoke the 'Payment' microservice.

Next step: [SignalR](signalr.md)
