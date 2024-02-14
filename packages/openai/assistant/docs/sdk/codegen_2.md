# Codegen

## Data

Questa sezione viene utilizzata per indicare il tipo di ORM (Object Relational Mapping) utilizzato dal microservizio, insieme al supporto per la multitenancy, utilizzando le seguenti proprietà:

**orm:** È possibile specificare l'ORM desiderato per il microservizio. Gli ORM attualmente supportati sono:

- **EntityFrameworkCore:** [Entity Framework Core](https://learn.microsoft.com/en-us/ef/core/);
- **Dapper:** [Dapper](https://github.com/DapperLib/Dapper).

**multitenancy:** Se specificato a true (di default è false), aggiunge la segregazione per tenant all'interno delle entità persistite nel database. Per maggiori dettagli sulla multitenancy, visita la sezione [multitenancy](#multitenancy).

```yml
data:
  orm: EntityFrameworkCore
  multitenancy: true
```

## Identity

Questa sezione consente di configurare l'identity profile all'interno di un microservizio. In questo modo sarà possibile utilizzare una rappresentazione fortemente tipizzata dei claims associati ad un utente autenticato. L'identity profile è utilizzabile dopo aver configurato il metodo "AddAuthentication" di ASP.NET Core, la cui documentazione è disponibile [qui](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/?view=aspnetcore-7.0). La sezione di identity contiene:

**claims:** Lista dei claims, ciascuno caratterizzato da:

- **name**: Nome del claim, ovvero della proprietà.
- **type**: Tipo del claim.
- **key**: Chiave del claim utilizzata nella serializzazione.
- **isOptional**: Specifica se il claim è opzionale o meno.

**userId:** Specifica il tipo del claim "UserId". Di default è "Guid".

```yml
identity:
  claims:
    - name: name
      type: string
      key: name
      isOptional: true
    - name: surname
      type: string
      key: surname
      isOptional: false
  userId:
    type: string
```

Questa sezione genererà l'interfaccia, che eredita `IIdentityProfile<Guid>`, contenente i claims specificati:

```cs
public interface IApplicationIdentityProfile : IIdentityProfile<Guid>
{
    string? Name { get; }
    string Surname { get; }
}
```

Sarà possibile accedere ad essi, come proprietà, tramite la classe `ApplicationClaimsIdentityProfile`:

```cs
public class ApplicationClaimsIdentityProfile : ClaimsIdentityProfile<Guid>, IApplicationIdentityProfile
{
    public ApplicationClaimsIdentityProfile(IHttpContextAccessor httpContextAccessor)
        : base(httpContextAccessor)
    {
    }

    public string? Name => ...;
    public string Surname => ...;
}
```

Il servizio verrà registrato nel container di IoC e sarà possibile richiedere un'istanza dell'interfaccia `IApplicationIdentityProfile` normalmente tramite Dependency Injection.

## Multitenancy

La multitenancy è configurabile dopo aver impostato [l'identity profile](#identity) all'interno del microservizio. Dopo averla abilitata, impostando a `true` l'omonima opzione della sezione "data", è possibile specificare l'opzione "tenantId" all'interno della sezione "identity". Al suo interno si può opzionalmente indicare anche il tipo della chiave, che di default è "Guid".

```yaml
identity:
  claims: ...
  userId: ...
  tenantId:
    key: http://schemas.microsoft.com/identity/claims/tenantid
```

L'indentity profile precedentemente generato diventerà:

```yaml
public interface IApplicationIdentityProfile : IIdentityProfile<string>, ITenantIdProfile<Guid>
{
    string GivenName { get; }
}

public class ApplicationClaimsIdentityProfile : ClaimsIdentityProfile<string>, IApplicationIdentityProfile
{
    public ApplicationClaimsIdentityProfile(IHttpContextAccessor httpContextAccessor)
        : base(httpContextAccessor)
    {
    }

    public string GivenName => ...;

    public Guid TenantId => ...;
}
```

Per tutte le entità per la quale si desidera la segregazione per tenant è necessario aggiungere la proprietà `isTenantEntity: true` e, successivamente, lanciare una migrazione:

```yaml
entities:
  - name: Customer
    description: Customer Entity
    useRepository: true
    isTenantEntity: true
    fields: ...
```

Tutte le query che coinvolgeranno queste entità saranno caratterizzate da un filtro che utilizzerà il valore del tenant id dell'utente che effettua la richiesta. È possibile, tuttavia, disabilitare il filtro puntualmente (a livello della singola query) utilizzando il metodo di estensione "AsNoMultitenancy()" di "IQuerable\<T\>":

```cs
var bobCustomers = context.Set<Customer>()
  .AsNoMultitenancy()
  .Where(name => name == "Bob")
  .ToList();
```

## Messaging

Questa sezione configura la funzione di messaging (pub/sub) del microservizio. Qui, viene indicata la lista dei messaggi che possono essere ricevuti dal microservizio e gli handlers che li gestiranno:

```yaml
messaging:
  handlers:
    - name: MyMessageHandler
      description: Handler of MyMessage1 and MyMessage2
      messages:
        - name: MyMessage1
        - name: MyMessage2
          result:
            - PingMessage
      metadata:
        topic: MyTopic
        bus: MyBus
  messages:
    - name: MyMessage1
      description: My message 1
      fields:
        - name: id
          description: The id of the message
          type: uuid
        - name: name
          description: The name of the message
          type: string
    - name: MyMessage2
      description: My message 2
      fields:
        - name: id
          description: The id of the message
          type: uuid
        - name: name
          description: The name of the message
          type: string
```

I messaggi (MyMessage1, MyMessage2) dovranno esistere anche in altri microservizi che provvederanno a pubblicarli, così che il message broker possa inoltrarli al microservizio di cui questo YAML fa parte.

## Components

Questa sezione dello YAML contiene la lista dei componenti dell'infrastruttura (ad esempio: database, messagebus, ecc.) utilizzati dal microservizio. Ciascun componente deve avere un tipo, un nome ed un provider. Il provider è l'implementazione scelta del tipo di componente (ad esempio: Sql Server come database, RabbitMQ come message broker, ecc.). Al momento, sono supportati 3 diversi tipi di components:

**database:** Descrive il database utilizzato dal microservizio. Includendo un component di tipo "database", verrà creato un container docker contenente un'istanza del database scelto, insieme ad un volume che ospiterà i suoi dati per persisterli su disco.

```yaml
components:
  - name: sqlserver
    type: database
    provider: sqlserver
```

I provider per il tipo "database" attualmente supportati sono:

- **sqlserver:** SQL Server;
- **postgres:** Postgres Server;
- **oracle:** Oracle Server.

**messagebus:** Descrive il message bus utilizzato dal microservizio. Includendo un component di tipo "messagebus", verrà creato un container docker contenente un'istanza del message broker scelto.

```yaml
components:
  - name: rabbit
    type: messagebus
    provider: rabbitmq
```

I provider per il tipo "messagebus" attualmente supportati sono:

- **rabbit:** RabbitMQ;
- **redis:** Redis Streams.

**statestore:** Descrive lo state store utilizzato dal microservizio. Includendo un component di tipo "statestore", verrà creato un container docker contenente un'istanza dello state store scelto.

```yaml
components:
  - name: redis
    type: statestore
    provider: redis
```

I provider per il tipo "statestore" attualmente supportati sono:

- **redis:** Redis.

## Contracts

Contiene le definizioni dell'API e dei Consumer Driven Contracts esposti dal microservizio (procedure e DTO).

```yaml
contracts:
  operations: ...
  dto: ...
  services:
    - name: MyController
      description: Custom controller
      operations: ...
      dto: ...
```

[**operations**:](#operations) Definisce la lista di actions del controller del microservizio.

[**dto**:](#dto) Definisce la lista dei DTOs (Data Transfer Objects) utilizzati all'interno delle operations.

**services:** Definisce una lista di controller, composti da dto ed operations:

- **name:** Nome del controller (in PascalCase);
- **description:** Descrizione del controller;
- **operations:** Lista di operazioni esposte dal controller del microservizio;
- **dto:** Lista dei DTOs utilizzati all'interno delle operations del controller.

## DTO

La proprietà "dto" permette di definire una lista di DTO (Data Transfer Object) e/o una lista di enumerati relativi al microservizio.

```yml
dto:
  - name: Person
    type: entity
    description: Person entity
    isTrackable: true
    isAbstract: true
    authPolicies: true
  - name: Customer
    type: entity
    description: Customer entity
    authPolicies:
      - Policy1
      - Policy2
    ancestor: Person
    disableMappingTestGeneration: true
    enableGetVariablesGeneration: true
    resource: class://Crm/Customers
    fields: ...
    validations: ...
    warnings: ...
  - name: JobState
    type: enum
    description: Customer job state
    generationMode: client
    position: 0
    enumeratorList:
      - name: Started
        description: Job started
      - name: Fired
        description: Job fired
        value: 0
```

Le classi generate lato Typescript e lato C# saranno isomorfiche. Trasferendole da client a server e viceversa attraverso le operations, i DTO manterranno la loro identità e non sarà necessario effettuare alcuna operazione di conversione. Ciascun DTO potrà essere composto dalle seguenti proprietà:

**name:** Nome del DTO. Il nome deve rispettare la notazione PascalCase (NomeCampo).

**type:** Tipologia di oggetto (entity o enum).

**description:** Descrizione del DTO.

**isTrackable:** Se impostato a true, tale impostazione renderà il DTO Trackable abilitandone il [Change Tracking](#changetracking).

**isAbstract:** Se impostato a true, rende la classe astratta.

**authPolicies:** Applica policy autorizzative sul metodo del controller. Può assumere i seguenti valori:

- **Booleano:** Se true, applica l'attributo [Authorize] sul metodo del controller;
- **Lista di stringhe:** Applica tale lista come "Policy" nell'attributo [Authorize] del metodo del controller.

**ancestor:** Con questa proprietà è possibile impostare come classe padre una delle classi definite nello stesso file YAML (ancestor: NomeClasse).

**disableMappingTestGeneration:** Se impostato a true, disabilita la generazione dei test unitari del mapping per il DTO in questione.

**enableGetVariablesGeneration:** Se impostato a true, crea un metodo a livello di classe che restituisce un dizionario in cui la chiave è il nome della proprietà della classe ed il valore è il valore della proprietà stessa.

**resource:** Resource name da associare alla classe. [Per maggior dettagli sulle resource, policy e claims, visita la sezione "Authorization"](.\authorization.md).

[**fields**:](#fields) Lista di proprietà della classe (concetto approfondito nel paragrafo successivo "DTO Fields").

**generationMode:** Se valorizzato imposta come generare il DTO:

- **client:** Genera il DTO solo lato client.
- **server:** Genera il DTO solo lato server.

**position:** gRPC position, da valorizzare solo quando si utilizza il DTO in una operation di tipo gRPC. Valore del parametro del messaggio (0,1,2,...).

[**enumeratorList**:](#enumeratorList) Proprietà presente solo con `type: enum`. Permette di definire la lista dei valori dell'enumerato, fornendo un nome in PascalCase ed un eventuale value.

[**validations**:](#validations) Lista di regole di validazione da applicare alla classe (concetto approfondito nel paragrafo successivo "DTO Fields").

[**warnings**:](#warnings) Lista di regole di warnings da applicare alla classe (concetto approfondito nel paragrafo successivo "DTO Fields").

## DTO Fields

La proprietà "fields" di una classe (proprietà "dto") permette di definire la lista delle proprietà che definiscono le caratteristiche di un DTO.

```yml
dto:
- name: Customer
  ...
  fields:
  - name: code
    type: numeric
    description: Codice readonly
    isNullable: true
    isReadOnly: true
    annotations: ...
  - name: name
    type: string
    description: Customer name
    isKey: true
    isPublic: true
    variableAlias: nameAlias
    decorators:
      - type: aspect
        default:
          template: text
          label:
            key: name
            default: Nome
    validations:
      - type: mandatory
        message:
          key: field-mandatory
          default: Campo obbligatorio
      - type: custom
        name: containNumbers
        message:
          key: string-no-num
          default: La stringa non contiene un numero
  - name: email
    type: string
    description: Customer email
    decorators:
      - type: aspect
        default:
          template: textarea
          label: Email
    validations:
      - type: pattern
        pattern: ^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$
        message: Mail format error
    warnings:
      - type: mandatory
        message: It's advisable to populate the field
  - name: manager
    type: Customer
    description: Customer Work Manager
  - name: myDictionary
    type: dictionary
    description: myDictionary dictionary
  - name: myCustomDictionary
    type: dictionary
    description: myCustomDictionary dictionary
    dictionaryOptions:
      key: integer
      value: integer
```

**NOTE IMPORTANTI: Ciascun DTO eredita implicitamente tutte le caratteristiche della classe EntityDTO del platform. Tale classe, fornisce tra le proprietà una proprietà id (id lato typescript, Id lato C#) di formato Guid (string lato typescript, System.Guid lato C#). E' imporante dunque non definire nuove proprietà con il nome "id" all'interno delle classi e tenerne conto nei mapping (lato C#, mappando l'eventuale proprietà equivalente dell'entità del DB o inizializzando la proprietà almeno con un nuovo Guid) e nelle inizializzazioni (lato Typescript, utilizzando UUID.UUID()). La proprietà "id" (come indicato poco più sopra), è implicitamente impostata come chiave primaria (isKey: true) della classe; questo (per l'Object Identity, che il platform applica automaticamente) permette di distinguere una istanza della classe descritta da un'altra istanza. Se dunque, due istanze della stessa classe avranno lo stesso id, faranno riferimento alla medesima istanza. Tra gli errori più comuni nell'utilizzo del CA-Platform, c'è quella di ricevere sul client istanze di una medesima classe con lo stesso guid (generalmente guid empty) e vederle come identiche. E' importante dunque avere sempre chiavi differenti per le stesse istanze.**

**name:** Nome della proprietà della classe. Il nome deve rispettare la notazione camelCase (nomeCampo).

**type:** Tipologia della proprietà. Può essere scelto dalla lista dei suggerimenti o può essere identificata in una entità definita nello stesso YAML. La lista dei suggerimenti invece, presenta dei "tipi" rappresentanti una sorta di astrazione rispetto al linguaggio nel quale vengono generati. Di seguito tutti i tipi:

- **boolean:** Boolean (C#) - boolean (Typescript)
- **byte:** System.Byte (C#) - number (Typescript)
- **date:** DateTime? (C#) - Date (Typescript)
- **datetime:** DateTime? (C#) - DateTime (Typescript)
- **dateonly:** DateOnly? (C#) - DateOnly (Typescript)
- **decimal:** decimal (C#) - number (Typescript)
- **float:** float (C#) - number (Typescript)
- **integer:** Int32 (C#) - number (Typescript)
- **numeric:** Double (C#) - number (Typescript)
- **sequence:** Int64 (C#) - number (Typescript)
- **string:** String (C#) - string (Typescript)
- **time:** DateTime? (C#) - Date (Typescript)
- **uint8array:** System.Byte[] (C#) - Uint8Array (Typescript)
- **uuid:** System.Guid (C#) - string (Typescript)
- **short:** short (C#) - number (Typescript)
- **any:** System.Object (C#) - any (Typescript)
- **dictionary:** Dictionary<string, object> (C#) - Map<string, any> (Typescript)

**description:** Descrizione del field.

**isArray:** Se impostato a true, rende la proprietà una lista della tipologia indicata nel campo "type".

**isAbstract:** Se impostato a true, rende la proprietà astratta.

**isStatic:** Se impostato a true, rende la proprietà statica.

**isNullable:** **_[DEPRECATED]_** - Usare la proprietà isOptional.

**isOptional:** Se impostato a true, rende il campo nullable lato C#.

**isReadOnly:** Se impostato a true, rende il campo readonly, rimuovendo i relativi setter lato C# e lato Typescript.

**isKey:** Se impostato a true, rende il campo chiave primaria (insieme alle altre key). Questa proprietà permette di applicare i concetti dell'Object Identity alla classe, rendendo esattamente identici gli oggetti che avranno lo stesso valore della proprietà impostata come key.

**isPublic:** Se impostato a false, rende il campo private.

**resource:** Nome della risorsa da associare al field. [Per maggior dettagli sulle resource, policy e claims, visita la sezione "Authorization"](.\authorization.md).

**variableAlias:** **_[OBSOLETE]_**

**position:** Indica la posizionte gRPC.

**dictionaryOptions:** Permette di modificare chiave e valore del dizionario utilizzando le proprietà "key" e "value". Esempio:

```yml
dictionaryOptions:
  key: string
  value:
    type: any
    isArray: true
```

**decorators:** Decoratore Typescript che permette di applicare il paradigma dell'Aspect Programming ai field dell'entità, associandone delle meta-informazioni. Utilizzando il componente `sh-form-control` con model binding l'istanza della classe e come prop binding il nome del field in questione, ad applicazione avviata, il suddetto componente leggerà le metainformazioni applicate sul field della classe e dinamicamente allocherà il corretto template e l'eventuale label associata. Il decoratore trattato è il decoratore `@Aspect`. [Per maggior dettagli sul "Context", visita la sezione "Metadati & Decoratori"](.\metadata.md).

- **type:** "aspect".
- **default/browse/edit:** Generalmente viene utilizzata la voce "default" per definire le regole Aspect indipendentemente dal "Context". Nel caso in cui si utilizzi il "Context", è possibile definire una regola Aspect per il context "Browse" e per il context "Edit". [Per maggior dettagli sui decoratori @Aspect e @Validation, visita la sezione "Metadati & Decoratori"](.\metadata.md)
  - **label:** Label da associare al template del campo. Può essere una semplice stringa, od una stringa localizzata. La stringa localizzata ha le seguenti proprietà:
    - **key:** Chiave di traduzione da inserire nel dizionario della lingua (generalmente inserito negli assets [es. it.json])
    - **default:** Stringa di fallback, in caso di assenza della chiave
  - **template:** Aspect key del componente da associare al field. L'Aspect Key è indicata al top di ogni playground dei componenti (es. Textarea => Aspect Key: textarea)

**validations:** Decoratore Typescript che permette di applicare regole di validazione ai field dell'entità, associandone delle meta-informazioni. Utilizzando il componente `sh-form-control` con model binding l'istanza della classe e come prop binding il nome del field in questione, ad applicazione avviata, il suddetto componente leggerà le metainformazioni applicate sul field della classe e dinamicamente applicherà la regola di validazione e l'eventuale messaggio di errore associato. Il decoratore trattato è il decoratore `@Validation`. [Per maggior dettagli sui decoratori @Aspect e @Validation, visita la sezione "Metadati & Decoratori"](.\metadata.md).

- **type:** Tipologia di regola di validazione. E' possibile scegliere tra "mandatory" (il campo sarà obbligatorio), "pattern" (il campo deve rispettare la regular expression indicata) o "custom" (validazione custom creata nel progetto)
- **name:** Campo abilitato solo scegliendo come tipologia "custom". Indica il nome del validatore custom. I validatori custom vanno inseriti nel file "validators.ts" situato nella folder "client\\src\\app\\nome-app\\services". [Per maggior dettagli sui custom validators, visita la documentazione ufficiale di "Angular"](https://angular.io/guide/form-validation#defining-custom-validators) .
- **pattern:** Campo abilitato solo scegliendo `type: pattern`. Indica la regular expression da applicare come regola sul campo.
- **value:** Campo abilitato solo scegliendo come tipologia "custom". Campo non obbligatorio che indica l'eventuale valore statico da passare al validatore.
- **message:** Messaggio di errore da associare al template del campo. Il campo comparirà solo in caso di regola di validazione non rispettata. Può essere una semplice stringa, od una stringa localizzata. La stringa localizzata ha le seguenti proprietà:
  - **key:** Chiave di traduzione da inserire nel dizionario della lingua (generalmente inserito negli assets \[es. it.json\]).
  - **default:** Stringa di fallback, in caso di assenza della chiave.

**warnings:** Decoratore Typescript che permette di applicare regole di validazione NON bloccanti ai field dell'entità, associandone delle meta-informazioni. Utilizzando il componente `sh-form-control` con model binding l'istanza della classe e come prop binding il nome del field in questione, ad applicazione avviata, il suddetto componente leggerà le metainformazioni applicate sul field della classe e dinamicamente applicherà la regola di validazione NON bloccante e l'eventuale messaggio di warning associato. Il decoratore trattato è il decoratore `@Warning`. [Per maggior dettagli sui decoratori @Aspect e @Validation, visita la sezione "Metadati & Decoratori"](.\metadata.md)

- **type:** Tipologia di regola di validazione. E' possibile scegliere tra "mandatory" (il campo sarà obbligatorio), "pattern" (il campo deve rispettare la regular expression indicata) o "custom" (validazione custom creata nel progetto).
- **name:** Campo abilitato solo scegliendo come tipologia "custom". Indica il nome del validatore custom. I validatori custom vanno inseriti nel file "validators.ts" situato nella folder "client\\src\\app\\nome-app\\services". [Per maggior dettagli sui custom validators, visita la documentazione ufficiale di "Angular"](https://angular.io/guide/form-validation#defining-custom-validators).
- **pattern:** Campo abilitato solo scegliendo come tipologia "pattern". Indica la regular expression da applicare come regola sul campo.
- **value:** Campo abilitato solo scegliendo come tipologia "custom". Campo non obbligatorio che indica l'eventuale valore statico da passare al validatore.
- **message:** Messaggio di errore da associare al template del campo. Il campo comparirà solo in caso di regola di validazione non rispettata. Può essere una semplice stringa, od una stringa localizzata. La stringa localizzata ha le seguenti proprietà:
  - **key:** Chiave di traduzione da inserire nel dizionario della lingua (generalmente inserito negli assets [es. it.json]).
  - **default:** Stringa di fallback, in caso di assenza della chiave.

## Operations

Definisce una lista di operazioni, ovvero actions, esposte dal servizio e invocabili dall'esterno tramite richieste HTTP.

```yml
operations:
  - name: getCustomers
    type: http_auto
    description: Recupera i customers
    disableContextAttach: true
    disableActionResult: true
    generationMode: ...
    binding: ...
    parameters: ...
    annotations: ...
```

Le operations lato client sono invocabili mediante l'oggetto "delegates" (this.delegates.nomeOperation) ad ogni livello. I delegates ereditano i metodi delegates dei container genitori. Una operation è composta dalle seguenti proprietà:

**name:** Nome dell'operation. Il nome deve rispettare la notazione camelCase (nomeOperation).

**type:** Tipologia di operation (http verb, subscription, ...). E' possibile scegliere tra le seguenti tipologie:

- **http_delete:** Il metodo DELETE richiede che il server di origine elimini la risorsa identificata dall'URI della richiesta.
- **http_get:** Il metodo GET permette di recuperare qualsiasi informazione (sotto forma di entità) identificata dall'URI della richiesta.
- **http_head:** Il metodo HEAD è identico a GET tranne per il fatto che il server NON DEVE restituire il corpo del messaggio nella risposta.
- **http_jsonp:** **_[OBSOLETE]_**
- **http_options:** Il metodo OPTIONS rappresenta una richiesta di informazioni sulle opzioni di comunicazione disponibili sulla catena di richiesta / risposta identificata dalla Request-URI.
- **http_patch:** Il metodo PATCH viene utilizzato per applicare modifiche parziali alle entità.
- **http_post:** Il metodo POST viene utilizzato per richiedere che il server di origine accetti l'entità racchiusa nella richiesta come nuovo subordinato della risorsa identificata dall'URI della richiesta nella riga della richiesta.
- **http_put:** Il metodo PUT richiede che l'entità racchiusa venga archiviata nell'URI di richiesta fornito. Se l'URI della richiesta fa riferimento a una risorsa già esistente, l'entità racchiusa DOVREBBE essere considerata come una versione modificata di quella che risiede sul server di origine.
- **http_auto:** **_[OBSOLETE]_**
- **signalr_subscription:** Genera un metodo nell'Hub di riferimento.
- **grpc**: Se non ancora generato, genera un file .proto nella cartella "Grpc" e nello stesso file genera i messaggi di request e reply in funzione dei parameters inseriti. Se non ancora generato, genera inoltre il Controller.cs nel quale eseguire l'override dei metodi generati. Aggiunge inoltre le dipendenze necessarie al file .csproj. E' fondamentale che tutti i parametri dell'operation grpc valorizzino la proprietà "position" (0,1,2,...) e, se tra i parametri è presente un DTO, anche i field del DTO in questione devono popolare la proprietà "position".
- **graphql_query:** Definisce una query di GraphQL. Per ulteriori informazioni, visionare la sezione su [GraphQL](#graphql).
- **graphql_mutation:** Definisce una mutation di GraphQL. Per ulteriori informazioni, visionare la sezione su [GraphQL](#graphql).

**description:** Descrizione del metodo del controller.

**disableContextAttach:** Disabilita l'attach del data context. Impostando il valore a true, feature come l'Object Identity verranno disabilitate.

**disableActionResult:** Se true, rimuove "ActionResult" dalla firma della response lato server.

**generationMode:** Se valorizzato imposta come generare l'operation:

- **client:** Genera il DTO solo lato client.
- **server:** Genera il DTO solo lato server.

**auth-policies:** Applica l'attributo "Authorize" con "Policy" sul metodo del controller C#.

**resource:** **_[OBSOLETE]_**

**mode:** sync: metodo del controller sincrono - async (default): metodo del controller asincrono.

**binding:** Permette di specificare se i parametri sono query parameter (fromQuery), se provengono dal body (fromBody) o se sono inseriti nell’header della richiesta (fromHeader):

- fromQuery: in operation con type "http_post" (o altri type che prevedono il body), sarà possibile specificare parametri esterni alla envelop, decorati con [FromQuery], che verranno aggiunti tra i query parameter. Esempio di generazione:

  ```cs
  public async Task<ActionResult<SaveCustomerResponse>> SaveCustomer(SaveCustomerRequest request, [FromQuery] string pIva, CancellationToken requestAborted)
  {
    ...
  }
  ```

- fromBody: in operation con type "http_post" (o altri type che prevedono il body), sarà possibile passare un unico parametro "fromBody", decorato con [FromBody], che non verrà inserito all’interno di una envelop. Esempio di generazione:

  ```cs
  public async Task<ActionResult<SaveCustomerResponse>> SaveCustomer([FromBody] Customer customer, CancellationToken requestAborted)
  {
    ...
  }
  ```

- fromHeader: i parametri di questo tipo verranno aggiunti direttamente nell’header della richiesta e saranno messi a disposizione dello specifico metodo dell’API, decorandoli con l’attributo [FromHeader]. Esempio di generazione:

  ```cs
  public async Task<ActionResult<SaveCustomerResponse>> SaveCustomer(SaveCustomerRequest request, [FromQuery] string pIva, [FromHeader] string codFisc, CancellationToken requestAborted)
  {
    ...
  }
  ```

[**parameters**:](#parameters) Lista dei parametri del metodo.

## Operation Parameters

La proprietà "parameters" di una operation, permette di definire la lista dei parametri del metodo del controller.

```yml
operations:
  - name: getCustomers
    type: http_get
    description: Recupera i customers
    parameters:
      - name: customers
        type: Customer
        description: Customers
        direction: retval
        isArray: true
  - name: getCustomerById
    type: http_get
    description: Recupera il customer per identificativo
    parameters:
      - name: id
        type: uuid
        description: Identificativo del customre
        direction: in
      - name: customer
        type: Customer
        description: Customer
        direction: retval
  - name: updateCustomer
    type: http_post
    description: Applica le modifiche al customer
    parameters:
      - name: customer
        description: Customer da modificare
        direction: in
        type: Customer
      - name: success
        description: Risultato operazione
        direction: retval
        type: boolean
  - name: updateCustomerName
    type: http_put
    description: Cambia il nome del customer
    parameters:
      - name: customer
        type: Customer
        description: Customer per il quale cambiare il nome
        direction: inout
        position: 0
      - name: success
        type: boolean
        description: Risultato operazione
        direction: retval
        position: 1
      - name: message
        type: string
        description: Messaggio di ritorno
        direction: out
        position: 2
```

Le proprietà disponibili sono le seguenti:

**name:** Nome del parametro. Il nome deve rispettare la notazione camelCase (nomeParametro).

**description:** Descrizione del parametro.

**type:** Tipologia della proprietà. Può essere scelto dalla lista dei suggerimenti o può essere identificata in una entità definita nello stesso YAML, in uno YAML shared incluso o in un container genitore (lo scenario eredita tutte le entities del dominio e dell'applicazione, come il dominio eredita tutte le entities dell'applicazione). La lista dei suggerimenti invece, presenta dei "tipi" rappresentanti una sorta di astrazione rispetto al linguaggio nel quale vengono generati. Di seguito tutti i tipi:

- **boolean:** Boolean (C#) - boolean (Typescript)
- **byte:** System.Byte (C#) - number (Typescript)
- **date:** DateTime? (C#) - Date (Typescript)
- **datetime:** DateTime? (C#) - DateTime (Typescript)
- **dateonly:** DateOnly? (C#) - DateOnly (Typescript)
- **decimal:** decimal (C#) - number (Typescript)
- **float:** float (C#) - number (Typescript)
- **integer:** Int32 (C#) - number (Typescript)
- **numeric:** Double (C#) - number (Typescript)
- **sequence:** Int64 (C#) - number (Typescript)
- **string:** String (C#) - string (Typescript)
- **time:** DateTime? (C#) - Date (Typescript)
- **uint8array:** System.Byte[] (C#) - Uint8Array (Typescript)
- **uuid:** System.Guid (C#) - string (Typescript)
- **short:** short (C#) - number (Typescript)
- **any:** System.Object (C#) - any (Typescript)
- **dictionary:** Dictionary<string, object> (C#) - Map<string, any> (Typescript)

**direction:** Definisce la tipologia di parametro. Può essere identificato in una delle seguenti tipologie:

- **in:** Parametro inserito nella "busta" (envelop) della richiesta del metodo.
- **out:** Parametro inserito nella "busta" (envelop) della risposta del metodo.
- **inout:** Parametro inserito sia nella "busta" (envelop) della richiesta che nella busta della risposta del metodo. Simula la feature del by-ref da client a server.

**isArray:** Se impostato a true, rende la proprietà una lista della tipologia indicata nel campo "type".

**isOptional:** Se true, rende il campo opzionale.

**position:** gRPC position, da valorizzare solo quando si utilizza una operation di tipo gRPC. Rappresenta il valore del parametro del messaggio (0,1,2,...).