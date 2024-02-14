# Database

## Component: SQLServer
### Tra i componenti di infrastruttura di un microservizio, è possibile definirne uno di tipo database. In questa sezione verrà analizzato il component di tipo database con provider sqlserver.
La creazione e l'utilizzo di un database possono essere eseguiti aggiungendo le seguenti righe alla sezione \"components\" del file yaml di un microservizio.
```yml
components:
  ...

  - name: sqlserver
    type: database
    provider: sqlserver

  ...
  ```
Il codice soprastante genererà un container che ospiterà un'istanza di un database SQLServer, che sarà dedicata al microservizio che l'ha richiesta.

Di seguito, il codice generato automaticamente nel file \"docker-compose.yml\"
```YML
services:
  ...

  sqlserver:
    image: mcr.microsoft.com/mssql/server:2019-latest

  ...
  ```
Di seguito il codice generato automaticamente nel file \"docker-compose.override.yml\"
```YML
services:
  ...

  sqlserver:
    environment:
      - SA_PASSWORD=Password1
      - ACCEPT_EULA=Y
    ports:
      - 5433:1433
    volumes:
      - sqlservervolume:/var/opt/mssql

  ...
  ```
Ovviamente, nella pipeline di produzione andranno sovrascritte le variabili d'ambiente, le porte e i volumi predefiniti.

Quest'azione genera anche un paio di righe nel progetto del microservizio atte ad integrare il componente SQLServer (appena aggiunto) nel microservizio, usando EntityFramework Core.

**Startup.cs**
```CS
services.AddDbContext<StoreDataContext>(opt => opt.UseSqlServer(Configuration["ConnectionString"]));
```
**Program.cs**
```Cs
using (IServiceScope scope = host.Services.CreateScope())
{
    IServiceProvider services = scope.ServiceProvider;

    StoreDataContext context = services.GetRequiredService<StoreDataContext>();
    context.Database.Migrate();

    scope.Seed<StoreDataSeed>();
}
```
È possibile utilizzare la classe `DbContext` (nell'esempio, `StoreDataContext`) per configurare le impostazioni di EntityFramework Core, e la classe seed (nell'esempio, `StoreDataSeed`) per eseguire il seeding del database.

Dopo aver registrato alcune entità, sarà possibile creare una migrazione. Questa feature può essere usata per creare o aggiornare il database all'avvio. Per creare una migrazione, selezionare il progetto del microservizio in questione, come progetto di avvio.
Quindi, assicurarsi di includere una sezione `ConnectionString` nel file `appsettings.json`; questo passaggio è necessario perché EntityFramework Core necessita di una stringa di connessione per creare un'istanza di `DbContext`. Includere questa sezione ovunque nel file json:
```JSON
{
    "ConnectionString": "Server=sqlserver;Database=couriers_db;User Id=sa;Password=Password1"
}
```
È possibile eliminarlo una volta creata la migrazione. Per farlo, aprire la Package Manager Console di Visual Studio ed eseguire il seguente comando:
```shell
Add-Migration Initial -o Infrastructure/Data/Migrations
```
Consigliamo di aggiungere le migrazioni nella cartella `Infrastructure/Data/Migrations`.

Una volta avviata l'applicazione, la migrazione verrà applicata al database; se il database non esiste, verrà creato.

Dopo aver seguito tutti questi passaggi, sarà possibile utilizzare i repository generati automaticamente utilizzando il generatore di codice.

 [Per maggiori dettagli sulla sintassi codegen delle componenti infrastrutturali, visita il paragrafo "Components" della sezione "Codegen"](https://caep.codearchitects.com/docs/sdk/codegen/#components)

 ## Repository Pattern
 ### Il Code Architects platform supporta l'uso del Repository Pattern (https://martinfowler.com/eaaCatalog/repository.html).
 Una volta definito il modello di un'entità di dominio, è possibile dotarlo automaticamente di un repository utilizzando la proprietà `useRepository`:
 ```yml
entities:
  ...
  - name: Product
    ...
    useRepository: true
    ...
  ...
 ```
Questo flag imposterà la creazione di un repository per l'entità Product che implementa il Generic Repository Pattern. In particolare, verrà generata un'interfaccia che estende l'interfaccia generica `IRepository`
```cs
public interface IProductRepository : IRepository<Product, Guid>
{
}
```
Verrà anche generata una classe che estende la classe generica Repository e che implementa l'interfaccia generata:
```cs
public interface ProductRepository : Repository<Product, Guid>, IProductRepository
{
}
```
Il repository conterrà le query e i comandi per recuperare o modificare le entità. Per farlo, è sufficiente definire i metodi nell'interfaccia ed implementarli nel repository concreto.

 [Per maggiori dettagli sulla sintassi codegen dei repository, visita il paragrafo "Entities" della sezione "Codegen"](https://caep.codearchitects.com/docs/sdk/codegen/#entities)

 ## Mappings
 ###Scrivere a mano il codice per mappare le entità nei DTO (e viceversa) è un'attività noiosa e ripetitiva. Per evitare di dover fare ciò, è possibile usare AutoMapper, che permette di mappare automaticamente le proprietà con nome uguale, ma anche di poter personalizzare il mapping quando esso diventa complicato.
È possibile generare i mappings compilando l'omonima sezione dello yaml del microservizio. Assumedo di aver creato l'entità `Product` e il DTO `ProductDto`, è possibile generare i mapping tra le due entità nel seguente modo:
```yml
mappings:
  - entity: Product
    contract: ProductDto
    fields:
      - from: price
        to: unitPrice
  - entity: Product
    contract: ProductDto
    fields:
      - from: unitPrice
        to: price
    inverse: true
  - entity: Product
    contract: ProductDto
```
Il primo mapping è quello da `Product` a `ProductDto` e genererà la seguente istruzione nel file di mapping presente nella cartella `Mappings`.
```cs
CreateMap<Domain.Model.Product, Contracts.ProductDto>()
  .ForMember(d => d.UnitPrice, opt => opt.MapFrom(s => s.Price));
```
Il secondo mapping è inverso e genera la seguente istruzione:
```cs
CreateMap<Contracts.ProductDto, Domain.Model.Product>()
  .ForMember(d => d.Price, opt => opt.MapFrom(s => s.UnitPrice));
```
La sezione `fields` permette di mappare una specifica coppia di campi quando i loro nomi differiscono.

Il terzo mapping è quello automatico da `Product` a `ProductDto` (presupponendo che i field abbiano stessi nomi). Lo snippet genererà la seguente istruzione nel file di mapping presente nella cartella `Mappings`.
```cs
CreateMap<Domain.Model.Product, Contracts.ProductDto>();
```
Una volta configurato il mapping, è possibile usarlo richiedendo un'istanza dell'interfaccia `IMapper`. Ad esempio:
```cs
public class ProductController : ProductControllerBase
{
  private readonly IMapper _mapper;

  public ProductController(IMapper mapper)
  {
    _mapper = mapper;
  }

  public async Task<ActionResult<FindProductResponse>> FindProduct(Guid id, CancellationToken requestAborted)
  {
    Product? product = ...; // Recupera il prodotto dal database

    if (product is not null)
    {
      return Ok(new FindProductResponse
      {
        Product = _mapper.Map<ProductDto>(product)
      });
    }

    return NotFound();
  }
}
```
[Per maggiori dettagli sulla sintassi codegen dei mapping, visita il paragrafo "Mappings" della sezione "Codegen"](https://caep.codearchitects.com/docs/sdk/codegen/#mappings)