# REST API, DTOs and mappings

In this section, we will guide you through defining Data Transfer Objects (DTOs) and implementing the mapping between your entities and DTOs in your CAEP-based eCommerce application. DTOs help ensure secure and efficient data transfer by decoupling API responses from the internal entity representation. For more in-depth explainations of DTOs and mappings, see the [Codegen docs - DTO](../../sdk/codegen.md#DTO).

## Defining DTOs

DTOs are defined inside the `contracts.dto` section. Do not add an `id` field, because it is inherited from base dto EntityBase. Let's model the `CartDto` and the `OrderDto`:

```yml
contracts:
  dto:
    - name: CartDto
      description: Represents a cart that contains orders placed by the user, which are to be processed together.
      type: entity
      fields:
        - name: orders
          type: OrderDto
          isArray: true
          description: The orders the cart is comprised of.
    - name: OrderDto
      description: Represents an order order placed by users.
      type: entity
      fields:
        - name: quantity
          type: integer
          description: The quantity of product the order specifies.
        - name: unitPrice
          type: decimal
          description: The price of the product the order refers to.
        - name: totalPrice
          type: decimal
          description: The total price of the order.
```

`CartDto` will be the output of our first API, which will invoke the previously implemented `CartService` method which retrieves a cart from the database by id. In the `contracts.operations` section we define:

```yml
operations:
  - name: getCartById
    type: http_get
    description: Retrieves a cart by its unique identifier.
    parameters:
      - name: id
        description: The unique identifier of the cart to retrieve.
        direction: in
        type: uuid
      - name: cart
        type: CartDto
        direction: out
        isOptional: true
        description: The retrieved cart.
```

At the end of this update, we will have the following new DTO classes:

```cs
public partial class CartDTO : EntityDTO
{
  /// <summary>
  /// The unique identifier for the cart.
  /// </summary>
  public Guid Id
  {
    get;
    set;
  }
  /// <summary>
  /// The orders the cart is comprised of.
  /// </summary>
  public required List<OrderDto> Orders
  {
    get;
    set;
  }
}

public partial class OrderDto : EntityDTO
{
  /// <summary>
  /// The unique identifier for the order.
  /// </summary>
  public Guid Id
  {
    get;
    set;
  }
  /// <summary>
  /// The quantity of product the order specifies.
  /// </summary>
  public int Quantity
  {
    get;
    set;
  }
  /// <summary>
  /// The price of the product the order refers to.
  /// </summary>
  public decimal UnitPrice
  {
    get;
    set;
  }
}
```

as well as this new method on the `StoreController`:

```cs
/// <summary>
/// Retrieves a cart by its unique identifier.
/// </summary>
/// <param name="id">The unique identifier of the cart to retrieve.</param>
/// <param name="requestAborted">Cancellation Token request</param>
[HttpGet("getCartById")]
// <custom:customAttributesGetCartById>
// </custom:customAttributesGetCartById>
public async Task<ActionResult<GetCartByIdResponse>> GetCartById(Guid id, CancellationToken requestAborted)
{
  // <custom:GetCartById>
  throw new NotImplementedException();
  // </custom:GetCartById>
}
```

By default, all operations will be added to the `StoreController` class. If we want to have different controllers for different groups of operations, we can use the `services` subsection, which has the same fields of its parent section.

```yml
contracts:
  services:
    - name: Cart
      description: Cart operations
      operations:
      - name: getCartById
        type: http_get
        description: Retrieves a cart by its unique identifier.
        parameters:
          - name: id
            description: The unique identifier of the cart to retrieve.
            direction: in
            type: uuid
          - name: cart
            type: CartDto
            direction: out
            isOptional: true
            description: The retrieved cart.
```

This will place the `getCartById` operation inside the `CartController` class, which will be generated inside the `Controllers/Cart` folder.

The last thing we miss to connect the API to the database is the mapping between the entities and the DTOs. To do so, we introduce the `mappings` section:

```yml
mappings:
  - entity: Cart
    contract: CartDto
  - entity: Order
    contract: OrderDto
```

This will generate the `CartProfile` and `OrderProfile` classes, with a default mapping configuration. Since the property `UnitPrice` of `OrderDto` refers to the price of the product the order is related to, we need to instruct AutoMapper to map `OrderDto.UnitPrice` from `Order.Product.Price`. We can use the custom zone to do so.

```cs
public class OrderProfile : Profile
{
  public void MapOrderEntityToOrderDtoDto()
  {
    CreateMap<Domain.Model.Order, Dto.OrderDto>()
    // <custom:mappings1>
      .ForMember(dst => dst.UnitPrice, opt => opt.MapFrom(src => src.Product.Price))
    ; // </custom:mappings1>
  }
}
```

or use the fields mapping provided by DSL:

```yml
mappings:
  ...
  - entity: Order
    contract: OrderDto
    fields:
      - from: Product.Price
        to: unitPrice
```

```cs
public class OrderProfile : Profile
{
  public void MapOrderEntityToOrderDtoDto()
  {
    CreateMap<Domain.Model.Order, Dto.OrderDto>()
      .ForMember(dst => dst.UnitPrice, opt => opt.MapFrom(src => src.Product.Price))
    // <custom:mappings1>
    ; // </custom:mappings1>
  }
}
```

Now we have everything we need to implement the `GetCartById` method. Let's inject `ICartService` alongside with the already injected `IMapper`:

```cs
public class StoreController : ControllerBase
{
  private readonly IMapper _mapper;
  // <custom:parameters>
  private readonly ICartService _cartService;
  // </custom:parameters>

  // <custom:constructor>
  public StoreController(IMapper mapper, ICartService cartService)
  {
    _mapper = mapper;
    _cartService = cartService;
  }
  // </custom:constructor>

  /// <summary>
  /// Retrieves a cart by its unique identifier.
  /// </summary>
  /// <param name="id">The unique identifier of the cart to retrieve.</param>
  /// <param name="requestAborted">Cancellation Token request</param>
  [HttpGet("getCartById")]
  // <custom:customAttributesGetCartById>
  // </custom:customAttributesGetCartById>
  public async Task<ActionResult<GetCartByIdResponse>> GetCartById(Guid id, CancellationToken requestAborted)
  {
    // <custom:GetCartById>
    Cart? cart = await _cartService.GetCartByIdAsync(id);
    if (cart is null)
      return NotFound();

    return Ok(new GetCartByIdResponse
    {
      Cart = _mapper.Map<CartDto>(cart)
    });
    // </custom:GetCartById>
  }
}
```

As a side note, make sure to only write code inside the custom zones.

## Swagger

The newly created API is already documented based on the information specified inside the YAML section and can be inspected using Swagger. To access swagger, browse to `http://localhost:port/swagger`, where `port` is the port the microservice's container is running on.

Next step: [Versioning](versioning.md)
