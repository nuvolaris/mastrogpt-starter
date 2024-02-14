# Change tracking

Il change tracking è una feature presente in alcune librerie di accesso ai dati che permette di tracciare lo stato delle entità lette dal database. Attraverso il change tracking, è possibile annotare le entità contrassegnandole con un valore che rappresenta lo stato corrente dell'entità, tipicamente:

- Modificata rispetto all'ultima lettura (Modified)
- Da rimuovere (Removed)
- Da aggiungere (Added)
- Inalterata (Unchanged)

All'interno della comunicazione client-server è possibile specificare lo stato delle entità annidate all'interno di un'altra entità, in modo tale da eseguire diverse operazioni per diverse entità, secondo il loro stato.

Ad esempio, data una relazione 1 a N tra un'entità "padre" ed un'entità "figlio", si potrebbe, utilizzando il change tracking, aggiungere, modificare e rimuovere le entità figlie indipendentemente l'una dall'altra, all'interno di un'operazione di modifica del padre.

## Abilitare il change tracking

Definiamo un aggregato composto da due entità: `Customer`, rappresentante un cliente, e `Demographic` rappresentante un fatto riguardante tale cliente, come genere, età, etnia, eccetera. La relazione è 1 a N perché ad un `Customer` possono corrispondere diversi `Demographic`. Assumiamo di aver definito entità e DTO come nel seguente yml, con operazioni di CRUD (omesse per brevità) su `Customer`:

```yml
entities:
  - name: Customer
    description: Customer Entity
    useRepository: true
    fields:
      - name: name
        type: string
        description: Customer name
      - name: surname
        type: string
        description: Customer surname
      - name: demographics
        type: DemographicEntity
        isArray: true
        description: Customer demographics
  - name: Demographic
    description: Demographic Entity
    fields:
      - name: name
        type: string
        description: Name
      - name: value
        type: string
        description: Value
associations:
  - type: aggregate
    multiplicity: one-to-many
    from:
      entity: Customer
      navigation: Demographics
    to:
      entity: Demographic
contracts:
  dto:
    - name: Customer
      type: entity
      description: Customer entity
      fields:
        - name: name
          description: Customer name
          type: string
        - name: surname
          description: Customer surname
          type: string
        - name: demographics
          type: Demographic
          isArray: true
          description: Customer demographics
          value: default
    - name: Demographic
      description: Demographic
      type: entity
      fields:
        - name: name
          type: string
          description: Name
        - name: value
          type: string
          description: Value
```

Immaginiamo di aver creato un `Customer` con 3 `Demographic`:

```json
{
  "customer": {
    "name": "John",
    "surname": "Doe",
    "demographics": [
      {
        "name": "age",
        "value": "32"
      },
      {
        "name": "address",
        "value": "858 Valley Farms Road Sioux Falls, SD 57103"
      },
      {
        "name": "ethnicity",
        "value": "Caucasian"
      }
    ]
  }
}
```

Adesso, supponiamo di aver bisogno di aggiornare, _all'interno della stessa operazione (PUT)_, questo `Customer`, modificando (opzionalmente i campi `name` e `surname`) le sue `demographics` in modo tale da:

- Aggiornare il valore di `age` da 32 a 30,
- Rimuovere `address`
- Aggiungere un nuovo `Demographic` con `name: gender` e `value: "Male"`
- Lasciare invariato `ethnicity`

Per far ciò, possiamo annotare il DTO `Demographic` con il campo `isTrackable: true`.

```yml
contracts:
  dto:
    - name: Demographic
      description: Demographic
      isTrackable: true
      type: entity
      fields:
        - name: name
          type: string
          description: Name
        - name: value
          type: string
          description: Value
```

A questo punto, il change tracker integrato all'interno del client farà in modo di aggiungere al DTO `Demographic` un campo, chiamato `trackingState`, che conterrà lo stato dell'oggetto. La richiesta `PUT` che verrà inoltrata al server sarà (supponendo di non aver modificato `name` e `surname`) del tipo:

```json
{
  "customer": {
    "name": "John",
    "surname": "Doe",
    "demographics": [
      {
        "name": "age",
        "value": "30",
        "trackingState": 4 // MODIFIED = 4
      },
      {
        "name": "address",
        "value": "858 Valley Farms Road Sioux Falls, SD 57103",
        "trackingState": 8 // REMOVED = 8
      },
      {
        "name": "gender",
        "value": "Male",
        "trackingState": 2 // ADDED = 2
      }
    ]
  }
}
```

Il backend, se correttamente configurato, potrà interpretare questi stati in modo tale da produrre le corrette operazioni all'interno dello stesso update, utilizzando il repository di `Customer`.

## Modificare le entità trackable

Le operazioni necessarie lato backend ad interpretare il `trackingState` sono:

1. Mappare il DTO nell'entità preservando le informazioni di tracking. Esistono due metodi per preservare le informazioni di tracking all'interno del mapping, descritti in seguito.
2. Chiamare il metodo UpdateAsync del repository di `Customer`.

### Mapping con AutoMapper

Se si utilizza AutoMapper per il mapping, il tracking è già preservato se è stato definito il mapping nello yml, come nel seguente esempio:

```yml
mappings:
  - entity: Customer
    contract: Customer
  - entity: Customer
    contract: Customer
    inverse: true
  - entity: Demographic
    contract: Demographic
  - entity: Demographic
    contract: Demographic
    inverse: true
```

Allora, dato che il DTO `Demographic` è stato indicato come trackable, verrà generato:

```cs
public void MapDemographicDtoToDemographicEntityEntity()
{
  CreateMap<Dto.Demographic, Domain.Model.Demographic>()
  /* Preserve tracking */
  .PreserveTracking()
  // <custom:mappings2>
  ; // </custom:mappings2>
}
```

L'istruzione `PreserveTracking` preserverà automaticamente le informazioni di tracking quando viene effettuato il mapping. L'operazione definita nel controller potrà essere di questo tipo:

```cs
public class CustomerController : ControllerBase
{
  private readonly IMapper _mapper;
  private readonly ICustomerRepository _repository;

  public CustomerController(IMapper mapper, ICustomerRepository repository)
  {
    _mapper = mapper;
    _repository = repository;
  }

  [HttpPut("updateCustomer")]
  public async Task<ActionResult<UpdateCustomerResponse>> UpdateCustomer(UpdateCustomerRequest request, CancellationToken requestAborted)
  {
    Customer customer = _mapper.Map<Customer>(request.Customer);

    await _repository.UpdateAsync(customer, requestAborted);

    return Ok();
  }
}
```

### Mapping manuale

Se non si utilizza AutoMapper, allora è necessario utilizzare l'interfaccia `ITrackingContext` ed effettuare il mapping utilizzando il metodo di estensione `Map`/`MapList`/`MapArray`:

```cs
public class CustomerController : ControllerBase
{
  private readonly ITrackingContext _trackingContext;
  private readonly ICustomerRepository _repository;

  public CustomerController(ITrackingContext trackingContext, ICustomerRepository repository)
  {
    _trackingContext = trackingContext;
    _repository = repository;
  }

  [HttpPut("updateCustomer")]
  public async Task<ActionResult<UpdateCustomerResponse>> UpdateCustomer(UpdateCustomerRequest request, CancellationToken requestAborted)
  {
    Dto.Customer customerDto = request.Customer;
    Customer customer = new Customer
    {
      Id = customerDto.Id,
      Name = customerDto.Name,
      Surname = customerDto.Surname,
      Demographics = customerDto.Demographics.MapList(_trackingContext, demographicDto => new Demographic
      {
        Name = demographicDto.Name,
        Value = demographicDto.Value
      })
    };

    await _repository.UpdateAsync(customer, requestAborted);

    return Ok();
  }
}
```

## Client

Lato client, è possibile accedere allo stato della singola entità attraverso la proprietà `trackingState`.

```ts
const trackingState = this.payload.customer.trackingState;
```

Oppure, all'intero change tracker tramite la proprietà `changeTracker`.

Per modificare lo stato dell'entità, è sufficiente impostare il valore di `trackingState`. Ad esempio, per eliminare un'entità attraverso una callback sul click di un pulsante:

```html
<sh-button (clicked)="customer.trackingState = ObjectState.deleted">Delete</sh-button>
```

Una volta effettuata un'operazione (add, update, remove) su un'entità, si dovrebbe effettuare la chiamata al metodo `acceptChanges()` per reimpostare il valore del `trackingState` dopo che l'operazione è andata a buon fine. Ad esempio:

```ts
await this.delegates.business.saveCustomerAsync(this.payload.customer);
this.payload.customer.acceptChanges();
```
