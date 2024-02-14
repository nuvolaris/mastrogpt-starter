# Codegen

## GraphQL

GraphQL è un linguaggio di interrogazione e manipolazione dei dati open-source per API e un runtime per soddisfare query con dati esistenti.
GraphQL può essere utitilizzato in alternativa ed in combinazione con le API REST; infatti, è possibile definire le query e le mutations utilizzando la sezione `contracts.operations`.

Come esempio si definisce una query base per leggere una lista di `Customer` dal database specificando il tipo di operazione come `graphql_query`:

```yml
contracts:
  operations:
    - name: customers
      type: graphql_query
      description: Get customers
      entity:
        name: Customer
        isArray: true
```

Ciò genererà, nella classe `RootQuery` nella cartella `GraphQL` il metodo che implementerà la query:

```cs
public partial class RootQuery
{
  public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context
  // <custom:customersParameters>
  // </custom:customersParameters>
  )
  {
    // <custom:customersImplementation>
    // </custom:customersImplementation>
  }
}
```

L'implementazione di questo metodo restituirà la lista di `Customer`, ad esempio utilizzando un repository (iniettandolo all’interno del metodo) oppure Entity Framework Core (i cui esempi sono riportati sotto).

È possibile definire dei parametri da passare alla query. Ad esempio, se si vuole filtrare per nome, basta aggiungere un parametro, in questo caso chiamato `name`.

```yml
contracts:
  operations:
    - name: customers
      type: graphql_query
      description: Get customers
      entity:
        name: Customer
        isArray: true
      parameters:
        - name: name
          type: string
          description: Name
          direction: in
          isOptional: true
```

E ciò aggiungerà un parametro utilizzabile all'interno della query.

```cs
public partial class RootQuery
{
  public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context, string name
  // <custom:customersParameters>
  // </custom:customersParameters>
  )
  {
    // <custom:customersImplementation>
    // </custom:customersImplementation>
  }
}
```

Sono supportati, tramite la sezione `annotations`, gli attributi `[UsePaging]`, `[UseProjection]`, `[UseFiltering]`, `[UseSorting]`:

```yml
contracts:
  operations:
    - name: customers
      type: graphql_query
      description: Get customers
      entity:
        name: Customer
        isArray: true
      annotations:
        - name: usePaging
          namespace: GraphQL
          value:
            inclueTotalCount: true
            maxPageSize: 500
        - name: useProjection
          namespace: GraphQL
        - name: useFiltering
          namespace: GraphQL
        - name: useSorting
          namespace: GraphQL
      parameters:
        - name: name
          type: string
          description: Name
          direction: in
          isOptional: true
```

Di seguito è riportata una possibile implementazione di questo metodo utilizzando Entity Framework Core.

```yml
public partial class RootQuery
{
[UsePaging(MaxPageSize = 500)]
[UseProjection]
[UseFiltering]
[UseSorting]
public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context, string name
// <custom:customersParameters>
, [Service] IMapper mapper
// </custom:customersParameters>
)
{
// <custom:customersImplementation>
return context.Customer.Where(customer => customer.Name == name).ProjectTo<Dto.Customer>(mapper.ConfigurationProvider);
// </custom:customersImplementation>
}
}
```

Di seguito invece, una possibile implementazione di questo metodo utilizzando un repository.

```cs
public partial class RootQuery
{
  [UsePaging(MaxPageSize = 500)]
  [UseProjection]
  [UseFiltering]
  [UseSorting]
  public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context, string name
  // <custom:customersParameters>
, [Service] ICustomerEntityRepository repository, [Service] IMapper mapper
  // </custom:customersParameters>
  )
  {
    // <custom:customersImplementation>
var customerEntity = await repository.GetAllAsync();
      return mapper.Map<IEnumerable<Dto.Customer>>(customerEntity);
    // </custom:customersImplementation>
  }
}
```

Le mutations sono gestite in maniera simile, specificando `graphql_mutation` come tipo di operazione.

```yml
contracts:
  operations:
    - name: updateCustomer
      type: graphql_mutation
      description: Update customer
      parameters:
        - name: customer
          type: Customer
          description: Customer to be updated
          direction: in
        - name: success
          type: boolean
          description: Operation result
          direction: out
```

In questo caso, vengono specificati dei parametri `in` e `out`: il primo contiene i dati del `Customer` da aggiornare, mentre il secondo indica se l'operazione è andata a buon fine. Anche le mutation possono utilizzare gli attributi, esattamente come le query.

```cs
public partial class Mutation
{
  // <custom:updateCustomerAttributes>
  // </custom:updateCustomerAttributes>
  public async Task<bool> UpdateCustomer(Customer customer, [Service] BusinessDataContext context
  // <custom:updateCustomerParameters>
  , [Service] IMapper mapper
  // </custom:updateCustomerParameters>
  )
  {
    // <custom:updateCustomerImplementation>
    var customerEntity = mapper.Map<CustomerEntity>(customer);
    context.Update(customerEntity);
    await context.SaveChangesAsync();
    return true;
    // </custom:updateCustomerImplementation>
  }
}
```

Lato client, le operazioni graphql saranno invocabili in maniera molto simile alle operation REST. Aggiungendo almeno una operation di tipo graphql ad un microservizio raggiungibile dal client, verrà generato un servizio "graphQL", direttamente raggiungibile dall’istanza del servizio relativo al microservizio, e così facendo si potrà accedere alle query ed alle mutation disponibili
"this.delegates.business.graphQL.customer".
Prendendo come esempio i seguenti DTO:

```yml
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
      - name: fiscalCode
        description: Customer fiscal code
        type: string
        isOptional: true
      - name: email
        description: Customer email
        type: string
      - name: version
        description: Customer version
        type: numeric
      - name: updateDate
        type: dateOnly
        description: Update Date
        isOptional: true
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

e definendo la seguente operation:

```yml
operations:
  - name: customers
    type: graphql_query
    description: Get customers
    entity:
      name: Customer
      isArray: true
    annotations:
      - name: usePaging
        namespace: GraphQL
        value:
          inclueTotalCount: true
          maxPageSize: 500
      - name: useProjection
        namespace: GraphQL
      - name: useFiltering
        namespace: GraphQL
```

lato client si potrà effettuare la query graphql, come nell’esempio seguente:

```ts
await this.delegates.business.graphQL
  .customers(
    'id',
    'email',
    x => x.surname,
    c => ShGraphQL.queryArray(c.demographics, 'name', 'value')
  )
  .paginate()
  .toPromise();
```

Osservando la query, possiamo porre l’attenzione su alcuni punti:

- Si stanno selezionando solamente i campi diretti id, email e surname del customer.
- I campi possono essere selezionati semplicemente indicandone il nome (ovviamente in maniera guidata), oppure definendo una callback (come per surname).
- I campi di tipo array (come demographics), dovranno essere selezionati definendo una callback ed utilizzando la funzione queryArray di ShGraphQL.
- Considerando che nella modellazione si è inserita la paginazione, è necessario inserire il metodo paginate prima di lanciare la query.
  - Nel metodo paginate potranno essere definiti opzionalmente il pageIndex ed il pageSize (es. .paginate({ pageSize: 2, pageIndex: 1}))
- Avendo abilitato il filtering ed il sorting, si potranno opzionalmente filtrare e ordinare i dati da ottenere, come nell’esempio seguente

  ```ts
  await this.delegates.business.graphQL
    .customers(
      'name',
      'id',
      'email',
      x => x.surname,
      'version',
      'updateDate',
      c => ShGraphQL.queryArray(c.demographics, 'name', 'value', 'trackingState', 'id')
    )
    .paginate({ pageSize: 2, pageIndex: 1 })
    .where({
      name: {
        operator: ShGraphQLWhereOperator.Like,
        value: this.payload.searchText
      }
    })
    .sortBy({ email: ShGraphQLSortDirection.DESC, name: ShGraphQLSortDirection.ASC })
    .toPromise();
  ```

Aggiungendo un parametro di input all’operation:

```yml
operations:
  - name: customers
    type: graphql_query
    description: Get customers
    entity:
      name: Customer
      isArray: true
    parameters:
      - name: name
        type: string
        description: name
        direction: in
        isOptional: true
    annotations:
      - name: usePaging
        namespace: GraphQL
        value:
          inclueTotalCount: true
          maxPageSize: 500
      - name: useProjection
        namespace: GraphQL
      - name: useFiltering
        namespace: GraphQL
```

il primo parametro dell’operation generata sarà proprio quello inserito nello YAML:

```ts
await this.delegates.business.graphQL.customers(‘PARAMETRO NAME’,'id', 'email', x => x.surname, c => ShGraphQL.queryArray(c.demographics, 'name', 'value')).paginate().toPromise()
```

è ovviamente possibile modellare una query che ritorni una sola istanza del DTO indicato, come nell’esempio di seguito:

```yml
- name: customer
      type: graphql_query
      description: Retrieves a customer
      entity:
        name: Customer
      parameters:
        - name: id
          type: uuid
          description: id
          direction: in
```

che permette di utilizzare l’operation generata come segue:

```ts
const result = await this.delegates.business.graphQL
  .customer(customer.id, 'id', 'email', 'surname', 'version', 'updateDate', c =>
    ShGraphQL.queryArray(c.demographics, 'name', 'value')
  )
  .toPromise();
```

dove result conterrà la envelop con all’interno il singolo customer.

**Nota:** Nelle modellazione delle operation di tipo graphql_query, non andranno mai specificati parametri di ritorno.

Per quanto riguarda invece la modellazione delle mutation, queste ultime potranno prevedere parametri di ritorno:

```yml
- name: updateCustomer
  type: graphql_mutation
  description: Update customer
  parameters:
    - name: customer
      type: Customer
      description: Customer to be updated
      direction: in
    - name: success
      type: boolean
      description: Operation result
      direction: out
```

La precedente mutation, potrà essere invocata dal client, come segue:

```ts
await this.delegates.business.graphQL.updateCustomer(this.payload.customer).toPromise();
```

Tra i parametri di ritorno, è possibile inserire anche un DTO sul quale effettuare una query, come nell’esempio seguente:

```yml
- name: updateCustomerAndReturn
  type: graphql_mutation
  description: Update customer and return it
  parameters:
    - name: customer
      type: Customer
      description: Customer to be updated
      direction: in
    - name: customer
      type: Customer
      description: Updated customer
      direction: out
```

che potrà essere invocata dal cliente, come segue:

```ts
await this.delegates.business.graphQL
  .updateCustomerAndReturn(this.payload.customer, 'email', 'name', 'updateDate')
  .toPromise();
```

Attenzione, se si ritorna un DTO, sarà sempre necessario inserire almeno un field sul quale effettuare la query.

## Change tracking

Il change tracking è una feature presente in alcune librerie di accesso ai dati che permette di tracciare lo stato delle entità persistite tramite database. Attraverso il change tracking, è possibile annotare le entità contrassegnandole con un valore che rappresenta lo stato corrente dell'entità, tipicamente:

- Modificata rispetto all'ultima lettura (Modified)
- Da rimuovere (Removed)
- Da aggiungere (Added)
- Inalterata (Unchanged)

All'interno della comunicazione client-server è possibile specificare lo stato delle entità annidate all'interno di un'altra entità, in modo tale da eseguire diverse operazioni per diverse entità, a seconda del loro stato.
Ad esempio, data una relazione 1 a N tra un'entità "padre" ed un'entità "figlio", si potrebbe, utilizzando il change tracking, aggiungere, modificare e rimuovere le entità figlie indipendentemente l'una dall'altra, all'interno di un'operazione di modifica del padre.
Definiamo un aggregato composto da due entità: `Customer`, rappresentante un cliente, e `Demographic` rappresentante un fatto riguardante tale cliente, come genere, età, etnia, eccetera. La relazione è 1 a N perché ad un `Customer` possono corrispondere diversi `Demographic`. Assumiamo di aver definito entità e DTO come nel seguente yml, con operazioni CRUD (omesse per brevità) su `Customer`:

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

Adesso, supponiamo di aver bisogno di aggiornare, all'interno della stessa operazione (PUT), questo `Customer`, modificando (opzionalmente i campi `name` e `surname`) le sue `demographics` in modo tale da:

- Aggiornare il valore di `age` da 32 a 30;
- Rimuovere `address`;
- Aggiungere un nuovo `Demographic` con `name: gender` e `value: "Male"`;
- Lasciare invariato `ethnicity`.

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

```yml
{
  'customer':
    {
      'name': 'John',
      'surname': 'Doe',
      'demographics':
        [
          { 'name': 'age', 'value': '30', 'trackingState': 4 // MODIFIED = 4 },
          {
            'name': 'address',
            'value': '858 Valley Farms Road Sioux Falls, SD 57103',
            'trackingState': 8 // REMOVED = 8
          },
          { 'name': 'gender', 'value': 'Male', 'trackingState': 2 // ADDED = 2 }
        ]
    }
}
```

Il backend, se correttamente configurato, potrà interpretare questi stati in modo tale da produrre le corrette operazioni all'interno dello stesso update, utilizzando il repository di `Customer`.
Le operazioni necessarie lato backend ad interpretare il `trackingState` sono:

1. Mappare il DTO nell'entità preservando le informazioni di tracking. Esistono due metodi per preservare le informazioni di tracking all'interno del mapping, descritti in seguito.
2. Chiamare il metodo UpdateAsync del repository di `Customer`.

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

Lato client, è possibile accedere allo stato della singola entità attraverso la proprietà `trackingState`:

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

## EJS

EJS è un semplice "templating language" che consente di generare qualsiasi snippet di codice con JavaScript. Nessuna religiosità su come organizzare le cose. Nessuna reinvenzione dell'iterazione e del flusso di controllo. È solo un semplice JavaScript.

EJS è utilizzato nel platform per generare tutto il codice dei progetti. Il platform fornisce "out of the box" una libreria di template EJS che è possibile sovrascrivere in funzione delle esigenze del progetto. Di seguito un esempio di template EJS del platform:

```js
<%# /* Context = { entity: Entity, container: RootContainer } */ %>
<%
  const rootNamespace = rootNamespaceOfContainer(container);
  const name = entity.name;
  const namespace = fullNamespaceOfContainer(container);
  const fullName = `${namespace}.${name}`;
  const keys = entityKeysSequence(entity);
  const validations = entity.validations;
  const hasValidations = !!validations && validations.length > 0;
  const isAbstract = entity.isAbstract;
  const isTrackable = entity.isTrackable;
  const resource = entity.resource;
-%>
<%- render('documentation/entity.ejs', { entity: entity }); %>
@JsonObject({ name: '<%- fullName %>, <%- rootNamespace %>' })
@Entity({
  name: '<%- fullName %>',
  keys: [<%- keys %>]
})
<% if (hasValidations) { -%>
  <%- render('model/entity/validation-collection.ejs', { validations: validations }); %>
<% } -%>
<% if (resource) { -%>
  <%- render('module/resource.ejs', { uri: resource }); %>
<% } -%>
export <%- isAbstract ? 'abstract ' : '' %>class <%- name %> extends <%- getExtendsClass(entity, container); %> {
  <%- render('model/entity/entity-body.ejs', { entity: entity, container: container }); %>
}
```

[Per maggior dettagli sulla sintassi del linguaggio EJS, visita la documentazione ufficiale](https://ejs.co/)