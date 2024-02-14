# Task Management and State Persistence in Scenario Navigation

In this section, we'll delve into the intricacies of task management and state persistence during scenario navigation within your Single Page Application (SPA). Understanding these concepts is essential for efficiently managing user interactions and data flow across different scenarios in your application.

## Task Identification: The taskId

Whenever you initiate navigation from the `start` state of a scenario, a task is created. This task is essentially a human task workflow that persists throughout the entire navigation process. Each task is assigned a unique identifier known as the `taskId`, often represented as a GUID (Globally Unique Identifier).

### Task Identification in the URL

The taskId plays a crucial role in identifying and managing tasks within your SPA. You can easily spot the taskId in the URL displayed in your browser's address bar as part of the navigation path. The URL structure typically follows this pattern: `address/application/domain/scenario/taskId/state`
For example: `http://localhost:4200/shopping-cart/store/cart/873ac04a-0cc2-4644-b9a5-73960bab317a/browse-orders`.
Even when transitioning from one state of a scenario to another (excluding the "start" state), the taskId remains unchanged. This means that as long as you're navigating within the same task, the taskId remains constant.

### Task Creation and New Scenarios

However, a new task and, consequently, a new taskId are created when you initiate navigation to a new scenario starting from the "start" state. In this from-scratch transition, the application generates a fresh task, isolating it from the previous one. This approach provides enhanced task and state management, ensuring clear separation between different user interactions.

## Task Payload: Data Transfer Between States

One of the key benefits of task management in your SPA is the ability to transfer data seamlessly between states without the need for query parameters or complex data passing mechanisms. Each task is associated with a payload, which is essentially a serializable object capable of holding and persisting information throughout state transitions within the same task.

### Payload Persistence

The payload is entirely serializable and, by default, is stored in the browser's localStorage. The taskId serves as the key for storing and retrieving the payload. This storage mechanism ensures that data remains accessible and consistent as the user navigates through different states of the same task.

## Leveraging Task Management for Efficient Navigation

Understanding task management and the use of payloads can significantly simplify data transfer and state persistence within your SPA. By embracing these concepts, you can streamline user interactions and maintain a smooth and context-rich experience as users navigate through your application.

### Example: Navigating from `browse-orders` to `order-details`

To illustrate the practical implementation of task management and payload usage, consider the scenario of navigating from the browse-orders state to the order-details state, passing an OrderDTO object selected by double-clicking a row in a table.

- Models a generic payload for store `OrderDTO` into a YAML of type `Payload`:

  ```yml
  name: Order
  type: payload
  description: Order payload
  fields:
    - name: order
      type: OrderDto
      description: Selected order
      container:
        type: application
        service: Store
  ```

  Note that we've used a type (`OrderDTO`) defined into a microservice yaml (`Store`). To do this, populate the container property with the service name (`Store`) and the type where the microservice is referred (`application`).

- Refers the `Order` Payload into `Cart` scenario yaml:

  ```yml
  name: Cart
  type: task
  ---
  payloads:
    - name: Order
  ```

  This action will generate the content of the payload in the following TypeScript file:

  ```typescript
  export interface CartPayload extends IActivityPayload {
    /**
     * optional version of payload data
     */
    version?: number;
    /**
     * Selected order
     */
    order: ApplicationModels.StoreModels.OrderDto;
    // --inject:classDeclaration--
  }
  ```

  Note that you can add other serializable informations also without define it inside the payload YAML, but definig them manually in the payload file, outside the injection points.
  You can also define others contextual payloads and refer them into scenarios YAMLs.

- User double-clicks on an order in the browse-orders state, triggering an event.

  ```html
  <!-- shopping-cart\client\src\app\shopping-cart\store\cart\components\start\browse_orders.html -->

  <sh-card title="Cart">
    <table *ngIf="cart">
      <thead>
        <tr>
          <th>Id</th>
          <th>Quantity</th>
          <th>Unit Price</th>
          <th>Total Price</th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let order of cart.orders" (dblclick)="selectOrder(order)">
          <td>{{order.id}}</td>
          <td>{{order.quantity}}</td>
          <td>{{order.unitPrice}}</td>
          <td>{{order.totalPrice}}</td>
        </tr>
      </tbody>
    </table>
  </sh-card>
  ```

- In response to the event, the selected OrderDTO is added to the task's payload.

  ```typescript
  // shopping-cart\client\src\app\shopping-cart\store\cart\components\start\browse_orders.ts

  @ActivityComponent({ extends: Base.BrowseOrdersComponent })
  @Component({ templateUrl: 'browse_orders.html', providers: [Base.CartServices] })
  export class BrowseOrdersComponent extends Base.BrowseOrdersComponent implements IOnInit {
    ...

    public selectOrder(order: OrderDto) {
      this.payload.order = order;
      this.orderDetails();
    }
  }
  ```

- The user initiates navigation to the order-details state. In the order-details state, the payload is accessed to retrieve the selected OrderDTO and display its details.

  ```html
  <!-- shopping-cart\client\src\app\shopping-cart\store\cart\components\start\order_details.html -->

  <sh-card title="Order">
    <row>
      <column> ID: {{payload.order.id}} </column>
      <column> Quantity: {{payload.order.quantity}} </column>
    </row>
    <row>
      <column> Unit Price: {{payload.order.unitPrice}} </column>
      <column> Total Price: {{payload.order.totalPrice}} </column>
    </row>
  </sh-card>
  ```

This process allows for seamless data transfer and continuity of user interactions between different states while maintaining a clear separation of tasks and consistent user experience.

### Example: Navigating to "Browse" State in the "Products" Scenario

Let's explore a scenario where you need to navigate from the current state to the "browse" state in another scenario called "products," which belongs to the same domain. To achieve this, you can use the navigate method, specifically designed for cross-scenario navigation. The navigate method accepts parameters such as "application," "domain," "scenario," and "action," where "action" represents the state to navigate to. If the source state and the destination state share the same application, domain, or scenario, you can omit those parameters for simplicity. In this case, you can use the following code to initiate the navigation:

```typescript
this.navigate({ scenario: 'products', action: 'browse' });
```

For example:

```html
<sh-card title="Order">
  ...
  <row>
    <column>
      <sh-button (clicked)="navigate({ scenario: 'products', action: 'browse' })">See products</sh-button>
    </column>
  </row>
  ...
</sh-card>
```

By using the navigate method in this way, you can seamlessly transition from the current state to the "browse" state in the "products" scenario, enabling efficient cross-scenario navigation within your Single Page Application.

### Navigational Stack Persistence and "Return" Navigation

Within the payload, not only is data seamlessly transferred between states, but also the navigational stack is persistently maintained. Each item in the navigational stack represents a navigated state within the same task. Suppose you want to implement a "return" functionality that allows users to navigate back from the "browse" state of the "products" scenario to the "order-details" state of the "cart" scenario.

To achieve this, you can create a button in the "browse" state of the "products" scenario, which, when clicked, invokes a "return" method. This method performs a step back in the navigational stack, essentially acting like a "gosub" operation in programming terms. The "return" action takes the user back to the previous state within the same task, enabling a smooth and intuitive way to backtrack through their interactions.

```html
<sh-card title="Products">
  ...
  <table *ngIf="products">
    ...
  </table>
  ...
  <sh-button (clicked)="return()">Back</sh-button>
</sh-card>
```

By using the CAEP breadcrumb feature, you may have noticed that each item's title is typically derived from the state name. However, you have the flexibility to assign custom and more meaningful names to these items by using the `setTitle` method within each state:

```typescript
  async onInit(params: { [key: string]: any }) {
    this.setTitle(`Products' list`);
  }
```

### Enhanced Navigation with `navigateWithReturn`

In scenarios where you need to perform a navigation with a specific intent, such as retrieving particular information while bypassing multiple states and returning directly to a designated state, the navigateWithReturn method comes into play. This method shares the same signature as the standard navigate method but adds an extra layer of functionality.

The primary purpose of navigateWithReturn is to create a navigation path that serves as a return journey to a predefined state, often referred to as the "return point." This is particularly useful when you need to temporarily venture into different states to gather information, perform actions, or complete a specific task, but ultimately want to return to a known starting point efficiently.

Consider a scenario where you're deep within a multi-step process but need to access specific details from a state that's several steps back. By using navigateWithReturn, you can initiate a navigation sequence that takes you through the necessary states to gather the required data. When it's time to return to your original context, invoking the return method will efficiently guide you back to the exact state where you initially called navigateWithReturn.

Here's an example of how to use navigateWithReturn:

```typescript
this.navigateWithReturn({ scenario: 'order-processing', action: 'view-details' });
```
