# Codegen

## Entities

In questa sezione è possibile definire una lista di entità di dominio. Le entity sono le classi che modellano la struttura del database, e sono dunque anche gli oggetti che vengono persistiti in esso.

```yml
entities:
  - name: MyEntity
    type: entity
    description: My entity
    annotations: ...
    useRepository: true
    isTenantEntity: true
    repositoryName: MyRepository
    ancestor: MyAncestorEntity
    annotations: ...
    fields: ...
```

Le proprietà disponibili sono le seguenti:

**name:** Nome dell'entità. Il nome deve rispettare la notazione PascalCase.

**type:** Tipologia di oggetto, può essere 'entity' o 'enum'.

**description:** Descrizione dell'entità.

**useRepository:** Se true, verrà generato un repository per l'entità.

**isTenantEntity:** Se true, indica che l'entità verrà segregata per tentant.

**repositoryName:** Se specificato, imposta il nome del repository.

**ancestor:** Con questa proprietà è possibile impostare come classe padre, una delle classi definite nello stesso file YAML appartenente allo stesso dominio.

[**fields**:](#entityfields) Lista di proprietà dell'entità.

## Entity Fields

La proprietà "fields" di una entity, permette di definire la lista delle proprietà che definiscono le caratteristiche di una entità.

```yml
entities:
- name: MyEntity
  ...
  fields:
  - name: myProperty
    type: string
    description: My property
    annotations: ...
```

Le proprietà disponibili sono le seguenti:

**name:** Nome della proprietà dell'entità. Il nome deve rispettare la notazione camelCase.

**description:** Descrizione del field.

**isNullable:** **_[DEPRECATED]_** - usare la proprietà isOptional.

**isOptional:** Se impostato a true, rende il campo nullable lato C#.

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

## Mappings

Questa sezione permette di definire i mappings tra i DTO e le entity. Il risultato è la generazione di classi di configurazione dei mappings, utilizzando la liberia AutoMapper. Nell'esempio, viene creato il mapping dall'entità MyProperty al DTO MyDto. Il mapping è unidirezionale; è possibile invertire la direzione del mapping utilizzando il campo "inverse".

```yml
mappings:
  - entity: MyProperty
    contract: MyDto
    inverse: false
    fields:
      - from: entityFieldName
        to: dtoFieldName
    annotations: ...
```

Le proprietà disponibili sono le seguenti:

**entity:** Nome della entità.

**contract:** Nome del DTO.

**inverse:** Se true, inverte il mapping, definendolo dal DTO alla entità.

**fields:** La sezione permette di mappare una specifica coppia di campi quando i loro nomi differiscono.

## Partials

Questa sezione permette di specificare diverse entità di un microservizio descritte in file YAML separati, in modo da rendere più leggibili e navigabili i file YAML di un microservizio.
È possibile creare un file partial attraverso il task "Generate Partial" di "Scarface". Eseguendo il task verrà richiesto di inserire il nome del file da creare e di selezionare il servizio "padre" a cui verranno aggiunte le proprietà definite all'interno del file YAML parziale. Al termine del task verrà creato il file YAML parziale all'interno della cartella "codegen/model/NomeDelMicroservizioPadre/":

```yaml
name: Operations
type: partial
description: Partial service related to Shell service
```

e, al file yaml del microservizio padre, verrà aggiunta la sezione partials con il riferimento al file creato:

```yaml
name: Shell
type: service
description: Shell microservice
partials:
  - file: operations
```

**Nota:** Poichè i file partial non sono altro che dei file che modellano una parte del microservizio, è possibile utilizzare `service` come valore della proprietà `type`. Tuttavia, consigliamo di utilizzare il valore `partial` per una questione di leggibilità. Analogamente, per i microservizi è possibile utilizzare `partial` come valore della proprietà `type`. Tuttavia, per i motivi sopra descritti, sconsigliamo di farlo.

È possibile, inoltre, creare un file partial manualmente, senza utilizzare il task di Scarface. Per farlo, bisognerà creare un file YAML con estensione `.partial.yml` all'interno della cartella model. È consigliato creare questo file all'interno di una sotto cartella avente come nome il nome del microservizio a cui il file partial fa riferimento. Per aggiungere il riferimento del file partial creato, bisognerà aggiungere la sezione `partials` al microservizio padre insieme ai nomi dei file partial in kebab case. Tutti i file partial creati e non referenziati all'interno della sezione "partials" non verranno considerati ai fini della generazione:

```yaml
name: Shell
type: service
description: Shell service
---
partials:
  - file: operations
  - file: dtos
```

## Dependencies

Questa sezione consente di generare dei business services all'interno del microservizio. Ad esempio, è possibile creare un servizio denominato "Cart" al cui interno contiene il metodo "getProductById" di tipo "Transient":

```yml
name: Shell
type: service
author: CodeArchitects
description: Shell system repository
namespace: App.Segregation.Shell
dependencies:
  - name: Cart
    type: Transient # Scoped | Singleton
    namespace: Administration
    mode: async # sync (Default: async)
    methods:
      - name: getProductById
        description: Get product by id
        parameters:
          - name: id
            description: Product identifier
            direction: in
            type: uuid
          - name: product
            type: Product
            direction: out
            description: Product
```

Nello specifico verrà generata una interfaccia e la relativa classe all'interno della cartella "Domain/Services/Administration". Nel caso in cui NON venga specificato il namespace, i file verranno generati nella cartella "Domain/Services".

Contratto software:

```cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Ca.Segregation.Model.Dto;

namespace App.Segregation.Shell.Domain.Services
{
  // --inject:RESPONSES--

  // --inject:RESPONSES--

  // --inject:SERVICE_NAME--
  public interface ICartService
  // --inject:SERVICE_NAME--
  {
    // --inject:METHODS--
    /// <summary>
    /// Get Product by Id
    /// </summary>
    /// <param name="id">Product identifier</param>
    Task<ProductDto> GetProductByIdAsync(Guid id);

    // --inject:METHODS--
  }
}
```

Nel caso in cui ci siano più parametri aventi `direction: retval`, verranno generate delle interfacce (nella zona di iniezione "RESPONSES" contenente tutti i parametri indicati come response). Invece, i parametri con `direction: out` saranno inseriti come parametri del metodi, ma saranno preceduti dalla parola chiave "out". Ad esempio:

```yml
methods:
  - name: getProductById
    description: Get product by id
    parameters:
      - name: id
        description: Product identifier
        direction: in
        type: uuid
      - name: foo
        type: string
        direction: retval
        description: foo
      - name: bar
        type: string
        direction: retval
        description: bar
      - name: fooBar
        type: string
        direction: out
        description: fooBar
```

```cs
// --inject:RESPONSES--
public interface ICartGetProductByIdAsyncResponse
{
  public string Foo {get; set;}
  public string Bar {get; set;}
}
// --inject:RESPONSES--
Task<ICartGetProductByIdAsyncResponse> GetProductByIdAsync(Guid id, out string fooBar);
```

Classe concreta, la cui implementazione è lasciata allo sviluppatore:

```cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace App.Segregation.Shell.Domain.Services
{
  // --inject:SERVICE_NAME--
  public class CartService : ICartService
  // --inject:SERVICE_NAME--
  {
    public CartService()
    { }
  }
}
```

Oltre alla generazione di questi file, verrà predisposta la Dependency Injection per il servizio creato:

- **.NET 5:** all'interno del file "EspServiceCollectionExtensions.cs":

```cs
namespace App.Segregation.Shell
{
  public static class EspServiceCollectionExtensions
  {
    public static void AddEspServices(this IServiceCollection services)
    {
      services.AddTransient<Domain.Services.Administration.ICartService, Domain.Services.Administration.CartService>();
    }
  }
}
```

- **.NET 6:** e 7 all'interno del file "App.cs":

```cs
namespace App.Segregation.Shell
{
  public static class EspServiceCollectionExtensions
  {
    public static WebApplicationBuilder AddData(this WebApplicationBuilder builder)
    {
      builder.Services.AddTransient<Domain.Services.Administration.ICartService, Domain.Services.Administration.CartService>();
    }
  }
}
```

## Secrets

Questa sezione permette di utilizzare i secrets tramite Dapr utilizzando un provider specificato. I provider attualmente supportati sono:

- **azurekeyvault:** [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault/).

```yml
secrets:
  - provider: azurekeyvault
```

Tra i file generati vi sarà un file json atto a contenere i secrets, dal path "server/Dapr/components/nome-microservizio-secrets-azurekeyvault.json":

```json
{
  "sample-key": "This is a sample secret"
}
```

Una volta inseriti i secret desiderati, è necessario effettuare una clean della solution di Visual Studio (Barra degli strumenti > Build > Clean Solution) per poter caricare correttamente i file di configurazione Dapr durante l'esecuzione dell'ambiente Docker.
La modalità di accesso ai secrets all'interno dell'applicazione è identico a quello dei dati presenti all'interno di appsettings.json.
Di seguito un esempio di utilizzo del secret all’interno del file "Program.cs" di un microservizio:

```cs
string? sampleKey = app.Configuration["sample-key"];
if (sampleKey == "This is a sample secret")
{
  app.Run();
}

app.Run();
```

%% Sezione actors omessa perché duplicata di actors.md

## Configurable indentation

È possibile configurare l’indentazione dei file generati:

- Per impostare una indentazione custom per il codice generato lato server, sarà sufficiente modificare i seguenti file come segue (dove 4 è il valore di indentazione di esempio):

  - Aggiungere la seguente riga nel file "codegen/configs/all.yml":

    ```yml
    server.indentSize: 4
    ```

  - Aggiungere la seguente riga nel file "codegen/configs/server.yml":

    ```yml
    indentSize: 4
    ```

  Dopo aver salvato i precedenti file, lanciare il comando "Scarface: Format server" per formattare il codice dei file esistenti lato server. Questo comando andrà lanciato solamente al cambio dell’indentSize.

- Per impostare una indentazione custom per il codice generato lato client, sarà sufficiente modificare i seguenti file come segue (dove 4 è il valore di indentazione di esempio):

  - Aggiungere la seguente riga nel file "codegen/configs/all.yml":

    ```yml
    client.indentSize: 4
    ```

  - Aggiungere la seguente riga nel file "codegen/configs/client.yml":

    ```yml
    indentSize: 4
    ```

  Dopo aver salvato i precedenti file, lanciare il comando "Scarface: Format client" per formattare il codice dei file esistenti lato client. Questo comando andrà lanciato solamente al cambio dell’indentSize.

- Per ri-formattare tutti i file (sia lato client che lato server), basterà lanciare il comando "Scarface: Format all".

## Payloads

Questa sezione consente di specificare vari payloads relativi ad uno scenario, in modo da consentire la condivisione di payload diversi tra differenti scenari. È, tuttavia, preservata la possibilità di modellare il payload manualmente.

```yml
name: CustomerPayload
type: payload
description: Customer payload
fields:
  - name: ...
  - type: ...
  - description: ...
  - isArray: ...
  - isOptional: ...
  - container: ...
  - dictionaryOptions: ...
```

Le proprietà disponibili sono le seguenti:

**name:** Nome del payload.

**type:** Tipo del file yaml, in questo caso "payload".

**description:** Descrizione del payload.

**fields:** Lista di oggetti desiderati all'interno del payload, caratterizzati da:

- **name:** Nome dell'oggetto.
- **type:** Tipo dell'oggetto, identici ai tipi disponibili per i [dto fields](#fields).
- **description**: Descrizione dell'oggetto.
- **isArray:** Se impostato a true, rende la proprietà una lista della tipologia indicata nel campo "type".
- **isOptional:** Se impostato a true, rende il campo nullable lato C#.
- **container:** Indica il tipo di container da cui recuperare le informazioni dell'oggetto indicato, indicando:
  - **type:** Tipo del container (applicazione, dominio, scenario).
  - **service:** Nome del servizio del container.
- **dictionaryOptions:** Permette di modificare chiave e valore del dizionario utilizzando le proprietà "key"e "value".

Come esempio, ipotizziamo che uno scenario "customers" debba proseguire il suo flusso nello scenario "suppliers" inserendo nel payload una stringa di ricerca e il customer selezionato (DTO del servizio Business):

```yml
name: CustomerPayload
type: payload
description: Customer payload
fields:
  - name: customer
    type: Customer
    description: Customer DTO
    container:
      type: application
      service: Business
  - name: searchText
    type: string
    description: Search Text
```

In questa situazione, sarà necessario definire la proprietà customer sia nel contratto software del payload dello scenario "customers" che in quello dello scenario "suppliers":

```yml
name: Customers
type: task
description: Customers scenario
domain: Crm
namespace: Ca.BackOffice.Crm.Customers
activity: CustomersActivity
payloads:
  - name: CustomerPayload
```

```yml
name: Suppliers
type: task
description: Suppliers scenario
domain: Crm
namespace: Ca.BackOffice.Crm.Suppliers
activity: SuppliersActivity
payloads:
  - name: CustomerPayload
```

Il codice generato sarà il seguente:

```ts
import * as ApplicationModels from '../../../models/index';
...
export interface CustomersPayload extends IActivityPayload {
  /**
  * optional version of payload data
  */
  version?: number;
  /**
   * Customer DTO
   */
  customer: ApplicationModels.BusinessModels.Customer;
  /**
   * Search Text
   */
  searchText: string;
  // --inject:classDeclaration--
}
```