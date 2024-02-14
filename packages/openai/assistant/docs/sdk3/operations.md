# Operations
   
## Controllers
### I controller e i metodi che essi espongono sono generati automaticamente a seguito della definizione di una o più operation.
[Per maggiori dettagli sulla sintassi codegen delle operation, visita il paragrafo "Operations" della sezione "Codegen"](https://caep.codearchitects.com/docs/sdk/codegen/#operations)

*ATTENZIONE: dalla versione 3.0.1 di Codegen ("@ca-codegen/ms-gen": "^3.0.1"), i controller generati sono passati da modalità "Inject" (con injection points) a modalità "Custom" (con custom zones). La retrocompatibilità con i controller già generati in modalità "Inject" è garantita: non verranno sovrascritti e rimarranno tali. Il controller in modalità "Custom" sarà generato di default per tutti i nuovi servizi e i nuovi contract services. Per migrare un controller da modalità "Inject" a modalità "Custom", sarà necessario eliminare il file `[NomeController]ControllerBase.cs` ed effettuare una nuova generazione. Dopo la generazione, i metodi del controller (migrato da "Inject" a "Custom"), presenteranno nel corpo una "throw new NotImplementedException();" e dunque andranno copiate ed incollate, nei rispettivi metodi del controller migrato, le implementazioni fatte nel controller generato in modalità "Inject". Questa procedura non è assolutamente obbligatoria, in quanto la generazione continuerà a funzionare anche con la modalità "Inject" e solo i nuovi controller verranno generati in modalità "Custom".*
```yml
...
operations:
  - name: withdrawProducts
    type: http_post
    description: Preleva una certa quantità di un prodotto dal magazzino
    parameters:
      - name: productId
        description: L'id del prodotto da prelevare
        type: uuid
        direction: in
      - name: quantity
        description: La quantità da prelevare
        type: integer
        direction: in
      - name: success
        description: Indica se l'operazione ha avuto successo
        type: boolean
        direction: out
      - name: newQuantity
        description: La quantità aggiornata
        type: integer
        direction: out
...
```
Lato server, in funzione delle versioni del generatore di codice e di Scarface installate nel progetto, quest'operazione genererà:

* **[SCARFACE≥1.1.9 / codegen≥3.0.1]** un metodo vuoto che rispecchia la definizione dell'operazione, nella classe `Controller`

    **C#**
    ```cs
    ...
    /// <summary>
    /// Preleva una certa quantità di un prodotto dal magazzino
    /// </summary>
    /// <param name="request">The request object</param>
    /// <param name="requestAborted">Cancellation Token request</param>
    [HttpPost("withdrawProducts")]
    // <custom:customAttributesWithdrawProducts>
    // </custom:customAttributesWithdrawProducts>
    public async Task<ActionResult<WithdrawProductsResponse>> WithdrawProducts(WithdrawProductsRequest request, CancellationToken requestAborted)
    {
    // <custom:WithdrawProducts>
    throw new NotImplementedException();
    // </custom:WithdrawProducts>
    }
    ...
    ```
    Al posto dell'istruzione "throw new NotImplementedException();" (nella zona custom che riporta il nome del metodo, e.g.: custom:WithdrawProducts) andrà inserita l'implementazione.

    È fondamentale non effettuare modifiche al di fuori delle zone custom, in quanto verranno sovrascritte al successivo ciclo di generazione.

    La zona custom custom:customAttributes[MethodName] permette di associare degli attributi custom al metodo.

    Andando ad esplorare l'intero file del controller, si possono osservare ulteriori zone custom:

    **C#**
    ```cs
    /**********************************************************\
    * Automatically produced by CA code generator            *
    *                                                        *
    * IMPORTANT NOTE:                                        *
    *                                                        *
    * Auto generated file. This file CAN be modified by you  *
    * Only in the custom zone.                               *
    \**********************************************************/

    /* #begin-template microservice-root/controller/controller-class.ejs */

    using AutoMapper;
    using Ca.BackOffice.Business.Domain.Model;
    using Ca.BackOffice.Business.Dto;
    using CodeArchitects.Platform.Common.Collections;
    using Microsoft.AspNetCore.Mvc;
    using System;
    using System.Threading;
    using System.Threading.Tasks;
    // <custom:using>
    using Ca.BackOffice.Business.Hubs;
    using Ca.BackOffice.Business.Domain.Services;
    using Ca.BackOffice.Business.Domain.Repositories;
    using System.Collections.Generic;
    // </custom:using>

    namespace Ca.BackOffice.Business.Controllers.Business.V1
    {
    [ApiController]
    [Route("api/ca/backoffice/business")]
    // <custom:classAttributes>
    // </custom:classAttributes>
    public class BusinessController : ControllerBase
    {
        private readonly IMapper _mapper;
        // <custom:parameters>
        private readonly ILegacyService _legacyService;

        private readonly IBusinessHub _businessHub;

        private readonly IUnitOfWork _uow;
        // </custom:parameters>

        // <custom:constructor>
        public BusinessController(IMapper mapper, ILegacyService legacyService, IBusinessHub businessHub, IUnitOfWork uow)
        {
        _mapper = mapper;
        _legacyService = legacyService;
        _businessHub = businessHub;
        _uow = uow;
        }
        // </custom:constructor>

        /// <summary>
        /// Preleva una certa quantità di un prodotto dal magazzino
        /// </summary>
        /// <param name="request">The request object</param>
        /// <param name="requestAborted">Cancellation Token request</param>
        [HttpPost("withdrawProducts")]
        // <custom:customAttributesWithdrawProducts>
        // </custom:customAttributesWithdrawProducts>
        public async Task<ActionResult<WithdrawProductsResponse>> WithdrawProducts(WithdrawProductsRequest request, CancellationToken requestAborted)
        {
        // <custom:WithdrawProducts>
        throw new NotImplementedException();
        // </custom:WithdrawProducts>
        }

        ...

        // <custom:methods>
        // </custom:methods>
    }
    }
    /* #end-template microservice-root/controller/controller-class.ejs */
    ```
    Zona custom "using", nella quale inserire gli using custom:

    **C#**
    ```cs
    // <custom:using>
    using Ca.BackOffice.Business.Hubs;
    using Ca.BackOffice.Business.Domain.Services;
    using Ca.BackOffice.Business.Domain.Repositories;
    using System.Collections.Generic;
    // </custom:using>
    ```
    Zona custom "classAttributes", nella quale inserire gli attributi custom sulla classe del controller:

    **C#**
    ```cs [ApiController]
    [Route("api/ca/backoffice/business")]
    // <custom:classAttributes>
    // </custom:classAttributes>
    public class BusinessController : ControllerBase
    ```
    Zona custom "parameters", nella quale inserire proprietà custom della classe del controller:

    **C#**
    ```cs
    private readonly IMapper _mapper;
    // <custom:parameters>
    private readonly ILegacyService _legacyService
    private readonly IBusinessHub _businessHub
    private readonly IUnitOfWork _uow;
    // </custom:parameters>
    ```
    Zona custom "constructor", nella quale poter modificare il costruttore del controller:

    **C#**
    ```cs
    // <custom:constructor>
    public BusinessController(IMapper mapper, ILegacyService legacyService, IBusinessHub businessHub, IUnitOfWork uow)
    {
    _mapper = mapper;
    _legacyService = legacyService;
    _businessHub = businessHub;
    _uow = uow;
    }
    // </custom:constructor>
    ```
    Zona custom "methods", nella quale poter aggiungere metodi custom al controller:

    **C#**
    ```cs
    ...
    // <custom:methods>
    // </custom:methods>
    ```
* **[SCARFACE<1.1.9 / codegen<3.0.1]** un metodo astratto nella classe `ControllerBase` che conterrà la definizione dell'operazione

    **C#**
    ```cs
    ...
    /// <summary>
    /// Preleva una certa quantità di un prodotto dal magazzino
    /// </summary>
    /// <param name="request">The request object</param>
    /// <param name="requestAborted">Cancellation Token request</param>
    [HttpPost("withdrawProducts")]
    public abstract Task<WithdrawProductsResponse> WithdrawProducts(WithdrawProductsRequest request, CancellationToken requestAborted);
    ...
    ```
    Il metodo astratto (C#) dovrà essere implementato nella classe concreta che implementa il `ControllerBase`. Ciò può essere velocemente fatto su Visual Studio premendo la combinazione di tasti 'CTRL + .' sulla definizione della classe del controller (in corrispondenza dell'avviso di errore). Il metodo creato avrà la seguente forma:

    **C#**
    ```cs
    ...
    [HttpPost("withdrawProducts")]
    public override Task<WithdrawProductsResponse> WithdrawProducts(WithdrawProductsRequest request, CancellationToken requestAborted)
    {
        throw new NotImplementedException();
    }
    ...
    ```
    Al posto dell'istruzione "throw new NotImplementedException();", andrà inserita l'implementazione del metodo.


Lato client, l'operazione modellata nello yaml soprastante, genererà un proxy delegate per effettuare la richiesta nel file `[service-name]_service.ts`:

**Typescript**
```ts
...
/**
 * Preleva una certa quantità di un prodotto dal magazzino
 */
public withdrawProducts(productId: string,
  quantity: number) {
  return this.request<IWithdrawProductsResponse>('POST', 'withdrawProducts', { productId, quantity }, false);
}
...
```
A questo punto, è possibile procedere con l'implementazione dell'operazione. Insieme al metodo, verranno generate anche le classi che modellano la richiesta e la risposta specificate nell'operation, in questo caso `WithdrawProductsRequest` e `WithdrawProductsResponse` (lato server) e `IWithdrawProductsResponse` (lato client).

**C#**
```cs
...
public class WithdrawProductsRequest
{
    public Guid ProductId { get; set; }
    public int Quantity { get; set; }
}

public class WithdrawProductsResponse
{
    public bool Success { get; set; }
    public int NewQuantity { get; set; }
}
...
```
**Typescript**
```ts
...
/**
* Preleva una certa quantità di un prodotto dal magazzino
*/
export interface IWithdrawProductsResponse {
  /**
   * Indica se l'operazione ha avuto successo
   */
  success: boolean;
  /**
   * La quantità aggiornata
   */
  newQuantity: number;
}
...
```
Le operazioni di tipo `Post` creano sia un DTO di richiesta (`WithdrawProductsRequest`) che uno di risposta (`WithdrawProductsResponse`). Invece le operazioni `Get` presentano i parametri di richiesta in query string. Ad esempio il seguente yaml:
```yml
...
operations:
  - name: getProducts
    type: http_get
    description: Restituisce una pagina di prodotti
    parameters:
      - name: pageIndex
        description: L'indice della pagina
        type: integer
        direction: in
      - name: pageSize
        description: Il numero di elementi della pagina
        type: integer
        direction: in
      - name: products
        description: La pagina di prodotti
        type: ProductDTO
        direction: out
        isArray: true
...
```
Produrrà il seguente metodo:
```yml
...
/// <summary>
/// Restituisce una pagina di prodotti
/// </summary>
/// <param name="pageIndex">L'indice della pagina</param>
/// <param name="pageSize">Il numero di elementi della pagina</param>
/// <param name="requestAborted">Cancellation Token request</param>
[HttpGet("getProducts")]
// <custom:customAttributesGetProducts>
// </custom:customAttributesGetProducts>
public async Task<ActionResult<GetProductsResponse>> GetProducts(int pageIndex, int pageSize, CancellationToken requestAborted)
{
  // <custom:GetProducts>
  throw new NotImplementedException();
  // </custom:GetProducts>
}
...
```
**Typescript**
```ts
...
/**
 * Restituisce una pagina di prodotti
 */
public getProducts(pageIndex: number,
  pageSize: number) {
  return this.request<IGetProductsResponse>('GET', 'getProducts', { pageIndex, pageSize }, false);
}
...
```
Il cui DTO di risposta è:

**C#**
```cs
...
public class GetProductsResponse
{
  public IEnumerable<ProductDTO> Products { get; set; }
}
...
```
**Typescript**
```ts
...
/**
* Restituisce una pagina di prodotti
*/
export interface IGetProductsResponse {
  /**
   * La pagina di prodotti
   */
  products: ConnectModels.ProductDTO[];
}
...
```
Infine, per richiamare le action del controller dal client, basterà richiamare i proxy delegates accedendo all'oggetto delegates (presente in ogni scenario state), al microservizio in questione (serviceName nell'esempio sottostante) ed ai proxy delegates (utilizzando promise o observable). Come di seguito:

**Typescript**
```ts
...
const response = await this.delegates.serviceName.getProducts(1, 20).toPromise();
...
this.delegates.serviceName.withdrawProducts(id,3).subscribe(response => {
  ...
});
...
```

## Versioning
### Dalla versione 3.0.1 di codegen (e 1.1.9 di Scarface), è possibile versionare i controller del microservizio. Per farlo, è necessario inizializzare il parametro `useVersioning` a `true` all'interno del file yml del microservizio, e specificare il numero di versione con il parametro `version` (default: 1):
```yml
name: Store
useVersioning: true
version: 2
contracts:
  services:
    - name: Negozio
      description: negozio controller
      version: 3
...
operations:
  - name: getProductById
    type: http_get
    description: get product by id
    parameters:
      - name: id
        type: uuid
        description: product id
        direction: in
      - name: product
        type: Product
        description: product found
        direction: out
    ...
  - name: addProduct
    type: http_post
    description: add a new product to the catalog
    version: "2"
    parameters:
      - name: products
        type: Product
        description: product to add
        direction: out
  ...
```
Nell'esempio soprastante, verrano generati due controller. Il controller contenuto nella cartella `V1` conterrà l'operation `getProductById`, in quanto non è stata specificata la versione. Invece, il controller contenuto nella cartella `V2` conterrà l'operation `addProduct`, proprio perchè in tale operation è stato specificato il numero di versione di appartenenza (version: "2"). Inoltre, è possibile utilizzare la versione anche all'interno dei `services` definiti sotto `contracts` e, prendendo ancora come esempio lo yaml soprastante, verrà generata una cartella "Negozio" per il contract service "Negozio", contenente 3 cartelle (V1,V2 e V3), una per ogni versione disponibile (la versione è incrementale, dunque incrementandone il valore, verrà aggiunto un nuovo controller).

![](./assets/resources/operations-versioning-folder-structure.png)

**C# - V1/StoreController.cs**
```cs
...
  [ApiController]
  [Route("api/app/versione/store/v{version:apiVersion}")]
  [ApiVersion("1")]
  // <custom:classAttributes>
  // </custom:classAttributes>
  public class StoreController : ControllerBase
  {
   ...
    /// <summary>
    /// get product by id
    /// </summary>
    /// <param name="id">product id</param>
    /// <param name="requestAborted">Cancellation Token request</param>
    [HttpGet("getProductById")]
    // <custom:customAttributesGetProductById>
    // </custom:customAttributesGetProductById>
    public async Task<ActionResult<GetProductByIdResponse>> GetProductById(Guid id, CancellationToken requestAborted)
    {
      // <custom:GetProductById>
      throw new NotImplementedException();
      // </custom:GetProductById>
    }
    ...
```
**C# - V2/StoreController.cs**
```cs
...
  [ApiController]
  [Route("api/app/versione/store/v{version:apiVersion}")]
  [ApiVersion("2")]
  // <custom:classAttributes>
  // </custom:classAttributes>
  public class StoreController : ControllerBase
  {
   ...
    /// <summary>
    /// add a product
    /// </summary>
    /// <param name="request">The request object</param>
    /// <param name="requestAborted">Cancellation Token request</param>
    [HttpPost("addProduct")]
    // <custom:customAttributesAddProduct>
    // </custom:customAttributesAddProduct>
    public async Task<ActionResult<AddProductResponse>> AddProduct(AddProductRequest request, CancellationToken requestAborted)
    {
      // <custom:AddProduct>
      throw new NotImplementedException()
      // </custom:AddProduct>
    }
    ...
```
È inoltre possibile specificare, su una operation, una versione minor o una versione patch, senza modificarne la major. Questo porterà a generare il metodo all'interno dello stesso controller (v2 ad esempio), ma a modificarne solamente la sottoversione, come nell'esempio seguente:

**YAML**
```yml
name: Store
        useVersioning: true
        version: 2
        ...
        operations:
            ...
          - name: addProduct
            type: http_post
            description: add a new product to the catalog
            version: "2"
            parameters:
              - name: products
                type: Product
                description: product to add
                direction: out
          - name: saveProduct
            type: http_post
            description: add a new product to the catalog
            version: "2.1"
            parameters:
              - name: products
                type: Product
                description: product to add
                direction: out
          ...
```   
**C# - V2/StoreController**
```cs
...
  [ApiController]
  [Route("api/app/versione/store/v{version:apiVersion}")]
  [ApiVersion("2.1")]
  [ApiVersion("2")]
  // <custom:classAttributes>
  // </custom:classAttributes>
  public class BusinessController : ControllerBase
  {
    private readonly IMapper _mapper;
    // <custom:parameters>
    // </custom:parameters>

    // <custom:constructor>
    public BusinessController(IMapper mapper)
    {
      _mapper = mapper;
    }
    // </custom:constructor>

    /// <summary>
    /// add a new product to the catalog
    /// </summary>
    /// <param name="request">The request object</param>
    /// <param name="requestAborted">Cancellation Token request</param>
    [HttpPost("addProduct")]
    [MapToApiVersion("2")]
    // <custom:customAttributesAddProduct>
    // </custom:customAttributesAddProduct>
    public async Task<ActionResult<AddProductResponse>> AddProduct(AddProductRequest request, CancellationToken requestAborted)
    {
      // <custom:AddProduct>
      throw new NotImplementedException();
      // </custom:AddProduct>
    }

    /// <summary>
    /// add a new product to the catalog
    /// </summary>
    /// <param name="request">The request object</param>
    /// <param name="requestAborted">Cancellation Token request</param>
    [HttpPost("saveProduct")]
    [MapToApiVersion("2.1")]
    // <custom:customAttributesSaveProduct>
    // </custom:customAttributesSaveProduct>
    public async Task<ActionResult<SaveProductResponse>> SaveProduct(SaveProductRequest request, CancellationToken requestAborted)
    {
      // <custom:SaveProduct>
      throw new NotImplementedException();
      // </custom:SaveProduct>
    }
    ...
```
Abilitando il versionamento verrà generato anche il file `ConfigureSwaggerOptions.cs` contenente la logica per generare la documentazione di swagger. Il file è generato in "Overwrite" mode, ed è dunque possibile modificarlo in base alle proprie esigenze. Infine, all'interno del file `Startup.cs` vengono generate delle zone di iniezione il cui contenuto cambia se si utilizza il versionamento o meno.

**C# - Startup.cs**
```cs
...
// --inject:USING_VERSIONING--
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Versioning;
using Ca.BackOffice.Store.SwaggerOptions;
using Microsoft.AspNetCore.Mvc.ApiExplorer;
// --inject:USING_VERSIONING--

...
// --inject:VERSIONING--
services.AddApiVersioning(options =>
{
  options.DefaultApiVersion = ApiVersion.Default;
  options.AssumeDefaultVersionWhenUnspecified = true;
  options.ReportApiVersions = true;
  options.ApiVersionReader = new UrlSegmentApiVersionReader();
});
services.AddVersionedApiExplorer(options =>
{
  options.GroupNameFormat = "'v'VVV";
  options.SubstituteApiVersionInUrl = true;
});
services.AddSwaggerGen();
services.ConfigureOptions<ConfigureSwaggerOptions>();
// --inject:VERSIONING--

...
// --inject:SWAGGER_DOC--

// --inject:SWAGGER_DOC--
...

// --inject:SWAGGER_ENDPOINT--
    app.UseSwaggerUI(c =>
    {
      var provider = app.ApplicationServices.GetRequiredService<IApiVersionDescriptionProvider>();
      foreach (var description in provider.ApiVersionDescriptions)
      {
        c.SwaggerEndpoint($"/swagger/{description.GroupName}/swagger.json", description.ApiVersion.ToString());
      }
    });
// --inject:SWAGGER_ENDPOINT--
...
```
Nel caso in cui fosse necessario modificare la logica presente all'interno di tali zone di iniezione, per applicare ad esempio delle configurazione custom a Swagger, basterà incapsulare tale zona di iniezione all'interno di un commento, inibendone dunque il funzionamento ed aggiungendo fuori il codice di configurazione custom.

**C# - Startup.cs**
```cs
...
/*
    // --inject:VERSIONING--
    services.AddApiVersioning(options =>
    {
      options.DefaultApiVersion = ApiVersion.Default;
      options.AssumeDefaultVersionWhenUnspecified = true;
      options.ReportApiVersions = true;
      options.ApiVersionReader = new UrlSegmentApiVersionReader();
    });
    services.AddVersionedApiExplorer(options =>
    {
      options.GroupNameFormat = "'v'VVV";
      options.SubstituteApiVersionInUrl = true;
    });
    services.AddSwaggerGen();
    services.ConfigureOptions<ConfigureSwaggerOptions>();
    // --inject:VERSIONING--
*/
...
```
Lato client verrà generato un proxy delegate per effettuare la richiesta nel file `[service_name]_service`, anteponendo la versione al nome del metodo.

**Typescript**
```ts
...
/**
 * Uploads the image of a product to complete the insertion in the catalog
 */
public addProduct(product: Store.Product) {
  return this.request<IAddProductResponse>('POST', 'v2.1.1/addProduct', { product }, false);
}
...
```
Nel caso di operation aventi lo stesso nome, ma versione di controller differente, la versione verrà aggiunta come suffisso al nome del proxy delegate. Analogamente per l'interfaccia che ne modella l'envelop della richiesta / risposta.

**Typescript**
```ts
...
/**
* add a new product to the catalog
*/
export interface IAddProductResponseV21 {
  ...
}
/**
 * Uploads the image of a product to complete the insertion in the catalog
 */
public addProductV21(product: Store.Product) {
  return this.request<IAddProductResponseV21>('POST', 'v2.1/addProduct', { product }, false);
}
...
```

## SignalR
Come per i controllers, è possibile generare dei metodi sugli hubs, descrivendo l'operazione e i suoi parametri in un'apposita sezione dello yaml. Di default, esistono già due metodi su ciascun hub: JoinGroup, che inserisce il client in un determinato gruppo, e LeaveGroup che rimuove il chiamante dal gruppo:
```yml
...
public interface IPaymentHub
{
}

public class PaymentHub : Hub<IPaymentHub>, IPaymentHub
{
    private readonly IHubContext<PaymentHub, IPaymentHub> _context;

    public PaymentHub(IHubContext<PaymentHub, IPaymentHub> context)
    {
        _context = context;
    }

    public Task JoinGroup(JoinGroupParams @params)
    {
        return _context.Groups.AddToGroupAsync(Context.ConnectionId, @params.GroupId);
    }

    public Task LeaveGroup(LeaveGroupParams @params)
    {
        return _context.Groups.RemoveFromGroupAsync(Context.ConnectionId, @params.GroupId);
    }
}
...
```
I gruppi serviranno nel momento in cui si vorrà inviare un messaggio solo ad un determinato gruppo di client, anziché a tutti. Per aggiungere una nuova operazione all'hub, nella sezione contracts > operations definire una nuova operazione di tipo signalr_subscription:
```yml
...
contracts:
  operations:
    - name: paymentProcessed
      type: signalr_subscription
      description: Sottoscrizione che notifica che il pagamento è stato correttamente processato
      parameters:
        - name: subscriptionId
          description: L'id della sottoscrizione
          type: string
          direction: in
        - name: paymentId
          description: L'id del pagamento
          type: string
          direction: in
        - name: dateTime
          description: Data e ora dell'avvenuto processo
          type: date
          direction: in
...
```
[Per maggiori dettagli sulla sintassi codegen delle operation signalR, visita il paragrafo "Operation" della sezione "Codegen"](https://caep.codearchitects.com/docs/sdk/codegen/#operations)

La direzione di tutti i parametri dell'operazione dovrà essere "in". Il risultato è la definizione di un nuovo metodo sull'interfaccia:
```yml
...
  public interface IPaymentHub
  {
      Task PaymentProcessed(PaymentProcessedParams @params)
  }
  ...
```
E di una classe contenente i parametri dell'operazione:
```yml
...
public class PaymentProcessedParams
{
    public string SubscriptionId { get; set; }
    public string PaymentId { get; set; }
    public DateTime DateTime { get; set; }
}
...
```
Questo metodo dovrà essere implementato sulla classe dell'hub. Ad esempio per notificare i client sottoscritti ad uno specifico gruppo:
```yml
...
public class PaymentHub : Hub<IPaymentHub>, IPaymentHub
  {
      public Task PaymentProcessed(PaymentProcessedParams @params)
      {
          return _context.Clients.Group(@params.SubscriptionId).PaymentProcessed(@params);
      }
  }
...
```
O per notificare tutti i client sottoscritti al metodo:
```yml
...
public class PaymentHub : Hub<IPaymentHub>, IPaymentHub
  {
      public Task PaymentProcessed(PaymentProcessedParams @params)
      {
          return _context.Clients.All.PaymentProcessed(@params);
      }
  }
...
```
[Per maggiori informazioni su SignalR, visita la documentazione ufficiale Microsoft](https://docs.microsoft.com/it-it/aspnet/signalr/overview/getting-started/introduction-to-signalr)

Lato client, verrà generato allo stesso modo un proxy per l'hub (da non sovrascrivere), come di seguito:
```yml
...
/**
 * Sottoscrizione che notifica che il pagamento è stato correttamente processato
 */
export interface IPaymentProcessedParams {
  /**
   * L'id della sottoscrizione
   */
  subscriptionId: string;
  /**
   * L'id del pagamento
   */
  paymentId: string;
  /**
   * Data e ora dell'avvenuto processo
   */
  dateTime: Date;
}
@Injectable({ providedIn: StorybookModule })
export class PaymentHub extends ShHubProxy {
  /**
   * Hub name
   */
  public static readonly NAME = '/hub/ca/storybook/payment/paymentHub';
  /**
   * Sottoscrizione che notifica che il pagamento è stato correttamente processato
   */
  public static readonly PaymentProcessed = 'PaymentProcessed';
  /**
   * Hub name
   */
  public get hubName() {
    return PaymentHub.NAME;
  }
  constructor(injector: Injector) {
    super(injector);
  }
  /**
   * Sottoscrizione che notifica che il pagamento è stato correttamente processato
   */
  public paymentProcessed() {
    return this.createHubMethod<IPaymentProcessedParams>(PaymentHub.PaymentProcessed);
  }
}
...
```
Per sottoscriversi al metodo di un hub da uno scenario state, sarà possibile utilizzare il decoratore SignalREvent con il riferimento alla classe generata dell'hub ed al nome del metodo al quale sottoscriversi:
```yml
...
@SignalREvent({
  hub: PaymentHub,
  methodName: 'PaymentProcessed'
})
public async onPaymentProcessed(params: IPaymentProcessedParams) {
  ...
}
...
```
Per tutti gli altri casi, sarà possibile iniettare l'istanza dell'hub nel costruttore della classe di un componente, servizio, scenario state, ecc.
```yml
...
constructor(
  ...
  private _paymentHub: PaymentHub,
  ...
)
...
```
Sottoscriversi ai suoi metodi:
```yml
...
this._paymentHub.paymentProcessed().subscribe(params => {
  ...
})
...
```
Invocarli:
```yml
...
await this._paymentHub.paymentProcessed().invoke({ dateTime: new Date(), paymentId: id })
...
```
Iscriversi ad uno specifico gruppo (per ricevere solo un determinato gruppo di notifiche):
```yml
...
await this._paymentHub.joinGroup(idSottoscrizione);
...
```
Cancellarsi da uno specifico gruppo (per smettere di ricevere un determinato gruppo di notifiche):
```yml
...
await this._paymentHub.leaveGroup(idSottoscrizione);
...
```