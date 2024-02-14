# Presentation Layer

In this section, we will guide you through setting up the presentation layer and establishing communication between your Single Page Application (SPA) and the microservice created using CAEP. Effective communication between the client and the microservice is crucial for the seamless functioning of your eCommerce application.

## RESTful API Endpoints

To facilitate communication between the SPA and the microservice, you can utilize the RESTful API endpoints provided by the microservice. These endpoints enable the SPA to send HTTP requests to the microservice, which in turn processes these requests and returns the required data.

### Example: Retrieving a Cart

Let's take an example of how to retrieve a user's cart from the microservice using a GET request. In this scenario, the SPA needs to display the contents of the user's cart.

To begin, add the Store microservice to the ShoppingCart services section in the shoppingCart.yml file:

```yml
name: ShoppingCart
type: application
...
services:
  ...
  - service: Store
```

This action will generate the following TypeScript files:

A file representing an injectable service for communicating with the Store microservice:

```typescript
// shopping-cart\client\src\app\shopping-cart\services\store_service.ts

/**
 * Retrieves a cart by its unique identifier.
 */
export interface IGetCartByIdResponse {
  /**
   * The retrieved cart.
   */
  cart: StoreModels.CartDto;
}
/* #end-template service/common-delegates-interfaces.ejs */
@Injectable()
export class StoreDelegates extends BaseDelegateService {
  protected api = `${Config.API}/api/app/shoppingcart/store/`;
  public constructor(injector: Injector) {
    super(injector);
  }
  /**
   * Retrieves a cart by its unique identifier.
   */
  public getCartById(id: string) {
    return this.request<IGetCartByIdResponse>('GET', 'getCartById', { id }, false);
  }
  /**
   * Retrieves a cart by its unique identifier.
   */
  public getCartByIdAsync(id: string) {
    return this.request<IGetCartByIdResponse>('GET', 'getCartById', { id }, false).toPromise();
  }
}
```

A file containing the DTOs (Data Transfer Objects) of the Store microservice:

```typescript
// shopping-cart\client\src\app\shopping-cart\models\store.ts

/**
 * Represents a cart that contains orders placed by the user, which are to be processed together.
 */
@JsonObject({ name: 'App.ShoppingCart.Store.Dto.CartDto, App.ShoppingCart.Store' })
@Entity({
  name: 'App.ShoppingCart.Store.Dto.CartDto',
  keys: ['id']
})
export class CartDto extends ShellModelEntity {
  @JsonIgnore() private _orders!: OrderDto[];
  public constructor(initializer?: Partial<CartDto>) {
    super();
    if (initializer && !(initializer instanceof CartDto)) {
      for (const fieldName in initializer) {
        this[fieldName as keyof this] = (<any>initializer)[fieldName];
      }
    }
  }
  /**
   * property: The orders the cart is comprised of.
   */
  @Enumerable()
  public get orders(): OrderDto[] {
    return this.getProperty<OrderDto[]>('orders');
  }
  public set orders(value: OrderDto[]) {
    this.setProperty<OrderDto[]>('orders', value);
  }
}
/**
 * Represents an order order placed by users.
 */
@JsonObject({ name: 'App.ShoppingCart.Store.Dto.OrderDto, App.ShoppingCart.Store' })
@Entity({
  name: 'App.ShoppingCart.Store.Dto.OrderDto',
  keys: ['id']
})
export class OrderDto extends ShellModelEntity {
  @JsonIgnore() private _quantity!: number;
  @JsonIgnore() private _unitPrice!: number;
  @JsonIgnore() private _totalPrice!: number;
  public constructor(initializer?: Partial<OrderDto>) {
    super();
    if (initializer && !(initializer instanceof OrderDto)) {
      for (const fieldName in initializer) {
        this[fieldName as keyof this] = (<any>initializer)[fieldName];
      }
    }
  }
  /**
   * property: The quantity of product the order specifies.
   */
  @Enumerable()
  public get quantity(): number {
    return this.getProperty<number>('quantity');
  }
  public set quantity(value: number) {
    this.setProperty<number>('quantity', value);
  }
  /**
   * property: The price of the product the order refers to.
   */
  @Enumerable()
  public get unitPrice(): number {
    return this.getProperty<number>('unitPrice');
  }
  public set unitPrice(value: number) {
    this.setProperty<number>('unitPrice', value);
  }
  /**
   * property: The total price of the order.
   */
  @Enumerable()
  public get totalPrice(): number {
    return this.getProperty<number>('totalPrice');
  }
  public set totalPrice(value: number) {
    this.setProperty<number>('totalPrice', value);
  }
}
```

Updates to an existing class called "Delegates," which is automatically injected into the application layer and its domains:

```typescript
export abstract class BaseShoppingCartDelegates extends BaseDelegates {
  ...
  public store: StoreDelegates;
  ...
  public constructor(injector: Injector) {
    super(injector);
    ...
    this.store = injector.get(StoreDelegates);
  }
}
```

The delegates service exposes all microservices proxies and simplifies communication between them and the single page application. This feature eliminates the need for developers to implement logic for interacting through HTTP RESTful APIs with microservices.

#### Using Delegates to Retrieve the Cart

Now, let's use the scaffolder to create a new scenario for retrieving the cart and displaying its orders in a table.

A scenario is essentially a state machine, where each state represents a navigable page, and transitions between states facilitate navigation within the scenario. When creating a new scenario, you can use a dedicated task in Visual Studio Code. Simply navigate to the `Tasks` section in the sidebar and select `Scarface: Generate scenario.`

Upon clicking the "Scarface: Generate scenario" task, you will be prompted to enter information about the scenario, including the application, domain, scenario name, and scenario states. For example, let's create two scenario states: browse-orders and order-details, along with their transitions. So let's create two scenario states `browse-orders` and `order-details`, and their transitions: from `browse-orders` to `order-details`. The state `browse-orders` was elected to be the first state correlated to `start` state.

? Please choose the application `shopping-cart`

? Please choose the domain `store`

? Please insert the scenario name `cart`

? Please insert a scenario state `browse-orders`

? Do you want to introduce a new state? `Yes`

? Please insert a scenario state `order-details`

? Do you want to introduce a new state? `No`

? The start state has been generated. Please choose the state associated with it `browse-orders`
Please define at least a transition from a state to another

? From `browse-orders`

? To `order-details`

? Do you want to introduce a new transition? `No`

The output of the scaffold is a scenario with a `start` state with a transition for `browse-orders` state, `browse-orders` state with a transition for `order-details`, and an `order-details` state. Please note that the `start` state is primarily used for navigation to a specific state within the scenario. Avoid implementing complex logic in the `start` state; its main purpose is to facilitate the initial navigation to the correct state. Instead, utilize the generated transition to navigate from the `start` state to the `browse-orders` state, and then from `browse-orders` to `order-details.`

This can be achieved by invoking the `browseOrders` method within the `start` state's OnInit hook. As a result, when the `start` state is loaded, it will immediately initiate navigation to the `browse-orders` state.

```typescript
// shopping-cart\client\src\app\shopping-cart\store\cart\components\start\start.ts
@ActivityComponent({ extends: Base.StartComponent })
@Component({ templateUrl: 'start.html', providers: [Base.CartServices] })
export class StartComponent extends Base.StartComponent implements IOnInit {
  public constructor(injector: Injector, services: Base.CartServices) {
    super(injector, services);
  }
  onInit(params: { [key: string]: any }) {
    this.browseOrders();
  }
}
```

Now we can use the delegates service into the browse_orders.ts component to retrieve cart by user identifier (simulated in this sample):

```typescript
// shopping-cart\client\src\app\shopping-cart\store\cart\components\start\browse_orders.ts

@ActivityComponent({ extends: Base.BrowseOrdersComponent })
@Component({ templateUrl: 'browse_orders.html', providers: [Base.CartServices] })
export class BrowseOrdersComponent extends Base.BrowseOrdersComponent implements IOnInit {
  public cart: CartDto;

  public constructor(injector: Injector, services: Base.CartServices) {
    super(injector, services);
  }
  async onInit(params: { [key: string]: any }) {
    const response = await this.delegates.store.getCartByIdAsync('123');
    this.cart = response.cart;
  }
}
```

and show its orders into browse.html component file:

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
      <tr *ngFor="let order of cart.orders">
        <td>{{order.id}}</td>
        <td>{{order.quantity}}</td>
        <td>{{order.unitPrice}}</td>
        <td>{{order.totalPrice}}</td>
      </tr>
    </tbody>
  </table>
</sh-card>
```

### Adding Cart Scenario to the Sidebar

To enable users to access the Cart scenario from the sidebar, follow these steps:

1. Create a `sidebar.json` file in the assets directory.

2. Insert the following snippet into the `sidebar.json` file:

```json
[
  {
    "id": "store",
    "icon": "grid",
    "title": "Store",
    "children": [
      {
        "id": "cart",
        "icon": "card",
        "title": "Cart",
        "routerLink": ["store", "cart"]
      }
    ]
  }
]
```

Next step: [Navigation](../presentation-layer/navigation.md)