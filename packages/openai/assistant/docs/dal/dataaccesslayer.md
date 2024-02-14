# Data Access Layer

Il Data Access Layer (DAL) la parte di un'applicazione web che si occupa di gestire l'accesso ai dati. Il suo compito principale è quello di fornire un'interfaccia tra il codice applicativo e il database, nascondendo la complessità di quest'ultimo e della comunicazione con lo stesso. Solitamente, il DAL fornisce una serie di metodi per creare, leggere, aggiornare e cancellare i dati. In questo modo, il resto del codice dell'applicazione non deve preoccuparsi dei dettagli tecnici del database.

## Il pattern Repository

I repository sono componenti che incapsulano la logica di accesso ai dati. Centralizzando tali funzionalità, è possibile raggiungere una manutenibilità maggiore del codice, insieme al disaccoppiamento dell'infrastruttura e/o della tecnologia usata per accedere al database (ORM) dal resto dell'applicazione.

La libreria CodeArchitects.Platform.Data definisce l'interfaccia generica `IRepository`, che modella il pattern appena descritto.

```c#
public interface IRepository<TEntity, TKey>
  where TEntity : class
  where TKey : IEquatable<TKey>
{
  Task<TEntity?> FindAsync(TKey key, CancellationToken cancellationToken = default);
  Task<TEntity?> FindAsync(TKey key, IncludeAction<TEntity> includeAction, CancellationToken cancellationToken = default);
  Task InsertAsync(TEntity entity, CancellationToken cancellationToken = default);
  Task InsertManyAsync(IEnumerable<TEntity> entities, CancellationToken cancellationToken = default);
  Task UpdateAsync(TEntity entity, CancellationToken cancellationToken = default);
  Task UpdateManyAsync(IEnumerable<TEntity> entities, CancellationToken cancellationToken = default);
  Task UpsertAsync(TEntity entity, CancellationToken cancellationToken = default);
  Task RemoveAsync(TEntity entity, CancellationToken cancellationToken = default);
  Task RemoveAsync(TKey key, CancellationToken cancellationToken = default);
  
  TEntity? Find(TKey key);
  TEntity? Find(TKey key, IncludeAction<TEntity> includeAction);
  void Insert(TEntity entity);
  void InsertMany(IEnumerable<TEntity> entities);
  void Update(TEntity entity);
  void UpdateMany(IEnumerable<TEntity> entities);
  void Upsert(TEntity entity);
  void Remove(TEntity entity);
  void Remove(TKey key);
}
```

In cui `TEntity` rappresenta il tipo di entità che il repository gestisce e `TKey` il tipo della chiave primaria dell'entità.
Questa interfaccia definisce le operazioni di accesso ai dati più comuni; in particolare:

- `FindAsync` esegue una ricerca dell'entità per chiave primaria.
- `InsertAsync` inserisce nel database una nuova entità.
- `InsertManyAsync` inserisce nel database nuove entità in blocco.
- `UpdateAsync` aggiorna i valori di un'entità esistente.
- `UpdateManyAsync` aggiorna i valori di entità esistenti in blocco.
- `UpsertAsync` se l'entità già esiste nel database, aggiorna i suoi dati, altrimenti la inserisce.
- `RemoveAsync` rimuove un'entità dal database.

Inoltre, sono presenti anche le rispettive varianti non asincrone. Sebbene questi siano le più comuni (CRUD), molto spesso è necessario eseguire delle operazioni specializzate (sia in lettura che scrittura) per un particolare tipo di entità. Per questo motivo, questa interfaccia è pensata per essere estesa da interfacce specializzate per singola entità che, oltre a tipizzare l'interfaccia base, definiscono metodi che rappresentano le suddette operazioni specializzate, in modo tale da centralizzarle e isolarle dal resto della logica applicativa, oltre a consolidarle semanticamente. Questo approccio prende il nome di pattern Repository generico.

Ad esempio, consideriamo un'entità chiamata `Product`, la cui chiave primaria è di tipo `Guid`.

```c#
public class Product
{
  public Guid Id { get; set; }
  public decimal Price { get; set; }
  public int SaleCount { get; set; }
}
```

Definiamo un'interfaccia specializzata per `Product` che estende la generica `IRepository<TEntity, TKey>` e che definisce un metodo per recuperare i prodotti più venduti.

```c#
using CodeArchitects.Platform.Data;

public interface IProductRepository : IRepository<Product, Guid>
{
  Task<IEnumerable<Product>> GetTopSellingProductsAsync(int count, CancellationToken cancellationToken = default);
}
```

Il metodo `GetTopSellingProducts` recupera gli N (parametro `count`) prodotti più venduti; altri metodi specializzati potranno essere definiti allo stesso modo e le parti dell'applicazione che utilizzano `IProductRepository` avranno accesso a questi metodi specializzati attraverso l'istanza del repository, oltre ai metodi definiti dall'interfaccia base generica.

## Implementazione del pattern Repository

Dall'interfaccia dei repository non si evince né il provider di database, né l'ORM utilizzato per accedervi, in quanto questi, essendo dettagli implementativi, saranno utilizzati dalle classi che forniranno l'implementazione dei metodi.

Al momento, sono disponibili due implementazioni del repository (e del resto del DAL):

- CodeArchitects.Platform.Data.EntityFrameworkCore: implementazione del DAL che utilizza Entity Framework Core 7.
- CodeArchitects.Platform.Data.AdoNet: implementazione del DAL che utilizza direttamente ADO.NET, da utilizzare tipicamente in congiunzione con Dapper.

> Nota: Entity Framework Core 7 richiede l'utilizzo di .NET 6 o superiore. Per progetti .NET Core 3.1 e .NET 5, esiste il pacchetto CodeArchitects.Platform.Data.EntityFrameworkCore che utilizza Entity Framework Core 5 ed è compatibile con .NET Core 3.1 e versioni superiori.

Queste due librerie forniscono l'implementazione di `IRepository<TEntity, TKey>` che potrà essere utilizzata come classe base per l'implementazione dei repository specializzati. Ad esempio, nel caso di `IProductRepository`, si ha il seguente schema:

![Generic repository](assets/resources/genericrepository.png)

Vediamo come implementare `IProductRepository` utilizzando Entity Framework Core, con `EFCoreRepository<TEntity, TKey>` come classe base.

```c#
using CodeArchitects.Platform.Data.EntityFrameworkCore;

public class ProductRepository : EFCoreRepository<Product, Guid>, IProductRepository
{
  public ProductRepository(IDataContext context)
    : base(context)
  {
  }

  public async Task<IEnumerable<Product>> GetTopSellingProductsAsync(int count, CancellationToken cancellationToken = default)
  {
    return await Entities
      .OrderBy(x => x.SaleCount)
      .Take(count)
      .ToListAsync(cancellationToken);
  }
}
```

La classe `EFCoreRepository` espone una proprietà protetta chiamata `Entities`, che corrisponde al `DbSet<TEntity>` (`DbSet<Product>` in questo caso). Attraverso il `DbSet` si potranno effettuare tutte le operazioni sull'entità `Product` che Entity Framework Core permette. Inoltre, `EFCoreRepository` espone anche l'istanza del `DbContext` utilizzato dall'applicazione tramite la proprietà protetta `DbContext`. Per ultimo, il costruttore richiede un'istanza dell'interfaccia `IDataContext` che, oltre a contenere il riferimento al `DbContext` dell'applicazione, fornisce l'implementazione dei metodi del repository generico, ma tipizzabili per qualsiasi tipo di entità (ad esempio `FindAsync<TEntity, TKey>`), in modo tale da poter aver accesso ai metodi base degli altri repository, senza dover iniettare il repository base; ciò può essere utile quando un repository espone i metodi di accesso ad un'intero aggregato, anziché ad una singola entità. Questo oggetto è disponibile tramite la proprietà protetta `Context` della classe base.

L'implementazione utilizzando ADO.NET (e Dapper) è strutturalmente molto simile, ma la query andrà scritta a mano o con qualche altro strumento di generazione di codice SQL (ad esempio SqlKata).

```c#
using CodeArchitects.Platform.Data.AdoNet;

public class ProductRepository : AdoNetRepository<Product, Guid>, IProductRepository
{
  public ProductRepository(IDataContext context)
    : base(context)
  {
  }

  public async Task<IEnumerable<Product>> GetTopSellingProductsAsync(int count, CancellationToken cancellationToken = default)
  {
    const string query = "SELECT [Id], [Price], [SaleCount] FROM [Products] ORDER BY [SaleCount] LIMIT @count";
    return await Connection.QueryAsync<Product>(query, new { count });
  }
}
```

In questo caso, la classe `AdoNetRepository` espone una proprietà protetta chiamata `Connection` (di tipo `IDbConnection`) con cui è possibile effettuare delle query. Anche in questo caso, si ha un'interfaccia `IDataContext` che, similmente all'implementazione con Entity Framework Core, espone i metodi CRUD generici e l'istanza della connessione.

## Il pattern Unit of Work

Il pattern Unit of Work è un pattern utilizzato per raggruppare delle modifiche effettuate al database in una singola operazione (l'unità di lavoro), ed è comunemente utilizzato in congiunzione con il pattern Repository.

La libreria CodeArchitects.Platform.Data definisce l'interfaccia `IUnitOfWork`:

```c#
public interface IUnitOfWork : IAsyncDisposable
{
  Task SaveAsync(CancellationToken cancellationToken = default);
}
```

L'unico metodo esposto da quest'interfaccia è il metodo `SaveAsync`, che serve a finalizare tutti i cambiamenti avvenuti all'interno dell'unità di lavoro.

Esistono due modi per creare un'unità di lavoro. Il primo è quello di creare puntualmente l'istanza di `IUnitOfWork` utilizzando l'interfaccia `IUnitOfWorkManager`:

```c#
public interface IUnitOfWorkManager
{
  IUnitOfWork Begin(CancellationToken cancellationToken = default);
  IUnitOfWork Begin(bool autoSave, CancellationToken cancellationToken = default);
}
```

Questa interfaccia definisce il metodo `Begin` che crea una nuova unità di lavoro; considerando che `IUnitOfWork` implementa `IAsyncDisposable`, questo metodo va utilizzato insieme al costrutto `await using`.

```c#
public class ShopService
{
  private readonly IUnitOfWorkManager _uowManager;
  private readonly IProductRepository _productRepo;
  private readonly ICartRepository _cartRepo;

  public MyService(IUnitOfWorkManager uowManager, IProductRepository productRepo, ICartRepository cartRepo)
  {
    _uowManager = uowManager;
    _productRepo = productRepo;
    _cartRepo = cartRepo;
  }

  public async Task FinalizeCartAsync(Cart cart, CancellationToken cancellationToken = default)
  {
    await using (IUnitOfWork uow = _uowManager.Begin(cancellationToken))
    {
      await _cartRepo.SetStatusToCompletedAsync(cart.Id, cancellationToken);
      foreach (Product product in cart.Products)
      {
        await _productRepo.IncrementSaleCountAsync(product.Id);
      }

      await uow.SaveAsync(cancellationToken);
    }
  }
}
```

In questo caso, all'interno dell'unità di lavoro (rappresentata dallo scope definito dal costrutto `await using`) avvengono operazioni su più entità (sul carrello e sui prodotti che esso contiene), che vengono eseguite tutte insieme nel momento in cui viene chiamato il metodo `SaveAsync`. In questo modo, tutte le operazioni vanno a compimento insieme oppure falliscono insieme, impedendo che il database si trovi in uno stato incoerente (ad esempio, carrello segnato come completato ma il numero di vendite dei prodotti che esso contiene non è stato incrementato).

Di default, è necessario chiamare il metodo `SaveAsync` quando si vuole effettuare il commit dei cambiamenti, ma esiste un'overload del metodo `Begin` che accetta un parametro `autoSave` di tipo `boolean` che, se impostato a `true`, effettua automaticamente l'invocazione a `SaveAsync` nel momento in cui lo scope definito dalla chiamata al metodo `Begin` termina.

```c#
await using (IUnitOfWork uow = _uowManager.Begin(autoSave: true, cancellationToken))
{
  await _cartRepo.SetStatusToCompletedAsync(cart.Id, cancellationToken);
  foreach (Product product in cart.Products)
  {
    await _productRepo.IncrementSaleCountAsync(product.Id);
  }
}
```

> Nota: è possibile invocare il metodo `SaveAsync` più volte all'interno dello stesso scope.

Il secondo modo per utilizzare l'interfaccia `IUnitOfWork` è quello di richiederne direttamente un'istanza tramite Dependency Injection. In questo caso, verrà creata una singola unità di lavoro per l'intero contesto di esecuzione (in altre parole, `IUnitOfWork` è registrato con `ServiceLifetime.Scoped`).

```c#
public class ShopService
{
  private readonly IUnitOfWork _uow;
  private readonly IProductRepository _productRepo;
  private readonly ICartRepository _cartRepo;

  public MyService(IUnitOfWork uow, IProductRepository productRepo, ICartRepository cartRepo)
  {
    _uow = uow;
    _productRepo = productRepo;
    _cartRepo = cartRepo;
  }

  public async Task FinalizeCartAsync(Cart cart, CancellationToken cancellationToken = default)
  {
    await _cartRepo.SetStatusToCompletedAsync(cart.Id, cancellationToken);
    foreach (Product product in cart.Products)
    {
      await _productRepo.IncrementSaleCountAsync(product.Id);
    }
    
    await _uow.SaveAsync(cancellationToken);
  }
}
```

## Associazioni e aggregati

Nell'esempio precedente, le entità `Cart` e `Product` venivano gestite da due repository diversi (`ICartRepository` e `IProductRepository`, rispettivamente). Il Domain Driven Design (DDD) introduce il concetto di aggregato, ovvero di insieme di entità relazionate tra loro e trattate come una sola, in cui esiste un'entità, chiamata Aggregate Root, dalla quale accedere all'intero aggregato.

In questo caso, si può pensare di costruire un aggregato formato da `Cart` e `Product` legati da una relazione 1-a-molti (un carrello contiene più prodotti), in cui `Cart` è l'Aggregate Root. Per far ciò, oltre a fare in modo che ci sia almeno una proprietà di navigazione tra le due entità (ad esempio, `Cart.Products` o `Product.Cart`), è necessario istruire il Data Access Layer in modo tale che tenga conto di queste relazioni quando vengono effettuate delle letture o delle scritture.

Ovviamente, se due entità sono relazionate (e quindi c'è almeno una proprietà di navigazione) non è detto che facciano parte dello stesso aggregato. In generale, le associazioni si distinguono in due tipi.

1. Intra-aggregato: quando le due entità fanno parte dello stesso aggregato e la seconda è gerarchicamente dipendente dalla prima
2. Inter-aggregato: quando le due entità non fanno parte dello stesso aggregato oppure le due entità sono gerarchicamente indipendenti

Per quanto riguarda le molteplicità, sono supportati i seguenti tipi di relazione:

- Uno-a-uno: sia intra-aggregato che inter-aggregato
- Uno-a-molti: sia intra-aggregato che inter-aggregato
- Molti-a-molti: solo inter-aggregato, in quanto sempre gerarchicamente indipendenti

### Lettura

Per quanto riguarda la lettura dal database, non c'è distinzione tra i due tipi di associazione, in quanto il metodo `FindAsync` presenta due overload: il primo accetta solo l'id dell'entità e non legge le varie proprietà di navigazione, mentre il secondo accetta una funzione che specifica, in maniera fluente, le proprietà di navigazione da includere nella query.

```cs
ICartRepository repo = ...;

Cart cart1 = await repo.FindAsync(id1); // cart1.Products è null
Cart cart2 = await repo.FindAsync(id2, _ => _
  .Include(cart => cart.Products)); // cart2.Products non è null
```

Questo comportamento è identico, che l'associazione sia intra-aggregato o inter-aggregato.

### Scrittura

Per quanto riguarda le scritture, InsertAsync e UpdateAsync hanno un comportamento diverso in base al tipo di associazione.

Tenendo in considerazione il fatto che l'Aggregate Root è l'oggetto dal quale si accede a tutto l'aggregato, l'operazione di Insert fatta sull'Aggregate Root provocherà la Insert di tutte le proprietà e sub-proprietà di navigazione che rientrano nell'aggregato (intra-aggregate). Invece, la Insert non verrà provocata per le proprietà di navigazione che non rientrano nell'aggregato (inter-aggregate); queste entità saranno considerate già esistenti e verrà creata solo la rappresentazione della relazione inter-aggregato a livello di database. Questo significa che verranno valorizzate eventuali foreign keys e record nelle tabelle associative (junction tables, in caso di relazioni molti-a-molti). L'operazione di Update funziona esattamente allo stesso modo. Invece il funzionamento dell'operazione di Delete è uguale a quello dell'operazione di Find; ciononostante, se si vuole predisporre l'eliminazione a cascata di tutte le entità dell'aggregato quando si elimina l'Aggregate Root, basterà impostare il delete behavior a livello di database.

### Configurazione

Per la configurazione delle associazioni, vedere le rispettive sezioni della documentazione dei due provider:

- [Entity Framework Core](efcore.md#associazioni)
- [ADO.NET](adonet.md#associazioni)

## Seeding

Per effettuare il seeding del database è possibile estendere la classe base `DataSeed`:

```cs
public class ApplicationDataSeed : DataSeed
{
  public void Seed(ISeeder seeder)
  {
    seeder.Seed(
      new Product { ... },
      new Product { ... },
      new Product { ... },
      ...
    );
  }
}
```

## Mapped repository

Uno dei compiti principali di un ORM è quello di semplificare lo sviluppo del proprio modello delle entità, permettendo di accedere al database utilizzando un modello dati che è progettato secondo le regole di business. Per questo motivo, la struttura delle classi che vengono persistite non rispecchia perfettamente la struttura tabellare propria di un database. L'ORM si occupa di colmare questa differenza attraverso opportuni mapping.

Qualora, però, si voglia avere il controllo completo sul processo di mapping, oppure il mapping sia troppo complicato per le capacità di un ORM, è possibile utilizzare la classe base `MappedRepository` (nelle sue due varianti `EFCoreMappedRepository` e `AdoNetMappedRepository`), che prevede la definizione di un livello di mapping personalizzato tra classi che modellano esattamente la struttura del database ed entità di business. Si dovranno implementare i due metodi astratti `EntityToTable` e `TableToEntity` in cui verrà effettuato il mapping.

Ad esempio, considerando l'entità `Product` e il suo equivalente lato database `ProductTable` e il provider ADO.NET, il repository verrebbe modificato nel seguente modo:

```cs
using CodeArchitects.Platform.Data.AdoNet;

public class ProductRepository : MappedAdoNetRepository<ProductTable, Product, Guid>, IProductRepository
{
  public ProductRepository(IDataContext context)
    : base(context)
  {
  }

  protected override ProductTable EntityToTable(Product entity)
  {
    // Mapping Product -> ProductTable
  }

  protected override Product TableToEntity(ProductTable table)
  {
    // Mapping ProductTable -> Product
  }
}
```

> Nota: l'overload del metodo FindAsync che permette di specificare le proprietà di navigazione da includere tramite lambda, non è supportato dai mapped repository. Ciononostante, questo metodo (come tutti i metodi delle classi base dei repository) sono virtuali ed è possibile definirne un override secondo necessità.

## How-to

### Impostare un livello di persistenza specificando l'ORM

Analizziamo lo yml di un microservizio di nome Store.

```yml
name: Store
type: service
description: Store service
namespace: Ca.ShoppingCart.Store
components:
  - type: database
    provider: sqlserver
    name: store
data:
  orm: EntityFrameworkCore
entities:
  - name: Category
    description: Category entity
    type: entity
    fields:
      - name: name
        type: string
        description: Category name
      - name: description
        type: string
        description: Category description
  - name: Product
    description: Product Entity
    useRepository: true
    fields:
      - name: denomination
        type: string
        description: Product name
      - name: category
        type: Category
        description: Product category
        isOptional: true
      - name: description
        type: string
        description: Product description
      - name: price
        type: decimal
        description: Product price
associations:
  - type: associate
    multiplicity: one-to-many
    from:
      entity: Category
    to:
      entity: Product
      navigation: Category
```

La sezione `components` contiene un elemento di tipo `database` con provider `sqlserver`, e questo genera un container Docker con SQLServer per lo sviluppo locale nel file `docker-compose`, oltre ad istruire il livello di persistenza ad utilizzare SQLServer.

La sezione `data` contiene il campo `orm` che specifica che si vuole utilizzare Entity Framework Core come ORM. Questo installerà i pacchetti di `CodeArchitects.Platform.Data.EntityFrameworkCore.*` e genererà i repository utilizzando la rispettiva classe base `EFCoreRepository`.

La sezione `entities` definisce le entità, e per `Product` verrà generato anche un repository.

La sezione `associations` definisce l'associazione uno-a-molti tra l'entità `Category` e l'entità `Product`.

### Utilizzare database multipli

Per utilizzare database multipli, è sufficiente indicare più components di tipo `database`.

```yml
name: Store
type: service
description: Store service
namespace: Ca.ShoppingCart.Store
components:
  - type: database
    provider: sqlserver
    name: store_sqlserver
  - type: database
    provider: postgres
    name: store_postgres
```

Questo farà in modo che venga generato il codice che servirà ad abilitare la possibilità di utilizzare un database o l'altro secondo delle particolari condizioni.

In particolare, in `appsettings.Development.json` verranno generate le stringhe di connessione ai database e una proprietà chiamata `Provider` che servirà a selezionare il database da utilizzare:

```json
  "Provider": "sqlserver",
  "ConnectionStrings": {
    "sqlserver": "...",
    "postgres": "..."
  }
```

La proprietà `Provider` potrà assumere valori diversi a seconda dell'ambiente, in modo tale da poter selezionare il database giusto in ogni circostanza.

In modalità split (`generationMode: split`), utilizzando Entity Framework Core, verranno creati anche dei progetti che conterranno le migrazioni di ciascun provider. Questi progetti saranno nominati secondo la convenzione {Prefisso}.{NomeSoluzione}.Data.{NomeSoluzione}_{NomeProvider} (ad esempio Ca.ShoppingCart.Store.Data.Store_postgres). Per effettuare le migrazioni, impostare il progetto eseguibile come progetto di startup e includere i riferimenti ai progetti in cui si vogliono effettuare le migrazioni. Selezionare poi questi come progetto di default nel package manager quando si lancia il comando Add-Migration.

### Creare table and domain entities

Ci sono due modi per utilizzare la feature delle table entities. Il primo è quello di creare separatamente l'entità di dominio e la rispettiva table.

```yml
entities:
  - name: Product
    description: Product
    type: domain
    fields:
      - name: name
        type: string
        description: Name
      - name: price
        type: decimal
        description: Price
  - name: ProductTable
    description: Product table
    useMappedRepository: Product
    type: table
    fields:
      - name: name
        type: string
        description: Name
      - name: price
        type: decimal
        description: Price
```

Avendo specificato `useMappedRepository`, verrà creato un repository che eredita da (supponendo di utilizzare EFCore) `EFCoreMappedRepository<ProductTable, Product, Guid>`. Bisognerà definire gli override dei metodi di mapping; in questo esempio, il mapping viene effettuato a mano, ma si potrebbe utilizzare AutoMapper, richiedendo un'istanza di `IMapper` tramite Dependency Injection.

```cs
using CodeArchitects.Platform.Data.EntityFrameworkCore;

public class ProductRepository : EFCoreMappedRepository<ProductTable, Product, Guid>, IProductRepository
{
  public ProductRepository(IDataContext context)
    : base(context)
  {
  }

  protected override ProductTable EntityToTable(Product entity)
  {
    return new ProductTable
    {
      Id = entity.Id,
      Name = entity.Name,
      Price = entity.Price
    };
  }

  protected override Product TableToEntity(ProductTable table)
  {
    return new Product
    {
      Id = table.Id,
      Name = table.Name,
      Price = table.Price
    };
  }
}
```

Il secondo modo è quello di specificare `table and domain` come `type` dell'entità.

```yml
entities:
  - name: Product
    description: Product
    type: table and domain
    useRepository: true
    fields:
      - name: name
        type: string
        description: Name
      - name: price
        type: decimal
        description: Price
```

In questo modo, verranno automaticamente generati entrambi i tipi di entità, che avranno esattamente la stessa struttura.

### Generare dei mappings tra entità table e domain

Il procedimento è analogo a quello per la generazione dei mappings tra entità e DTO.

```yml
mappings:
  - entity: Product
    table: ProductTable
  - entity: Product
    table: ProductTable
    inverse: true
```

Questo yml genererà nella configurazione di AutoMapper il codice per mappare da `Product` a `ProductTable` e viceversa (mapping bidirezionale).
