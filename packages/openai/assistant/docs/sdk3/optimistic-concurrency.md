# Optimistic Concurrency

Entity Framework Core permette di configurare il controllo di concorrenza ottimistico sia a livello di database (se esso lo permette), che a livello di applicazione, come spiegato in [questa guida](https://learn.microsoft.com/en-us/ef/core/saving/concurrency?tabs=data-annotations).

## Concorrenza ottimistica con Entity Framework Core

Attraverso l'attributo `[ConcurrencyCheck]`, si può contrassegnare una proprietà di una entità in modo tale che venga utilizzata come concurrency token. Normalmente, nel codice applicativo dev'essere previsto l'aggiornamento di tale proprietà ad ogni modifica.

```cs
var person = context.People.Single(b => b.FirstName == "John");
person.FirstName = "Paul";
person.Version = Guid.NewGuid();
context.SaveChanges();
```

Tuttavia, utilizzando il repository `EFCoreRepository` e abilitando il plugin della concorrenza ottimistica, si può evitare di farlo manualmente e rendere automatico l'aggiornamento del concurrency token ad ogni chiamata al metodo `UpdateAsync` del repository.

```cs
var person = await repository.FindAsync("John");
person.FirstName = "Paul";
await repository.UpdateAsync(person);
```

Per abilitare l'utilizzo della concorrenza ottimistica quando si utilizza Entity Framework Core, utilizzare il plugin `UseOptimisticConcurrency` dell'estensione CAEP.

```cs
services.AddDbContext<MyDbContext>(options => options
    .UseSqlServer("...")
    .UseCaep(caep => caep
        .UseOptimisticConcurrency()));
```

## Concorrenza ottimistica con ADO.NET

Questa feature è automaticamente abilitata in ADO.NET e si applica alle entità che utilizzano il controllo di concorrenza ottimistico. La configurazione di un'entità per la concorrenza ottimistica avviene nel seguente modo.

```cs
public class MyModelConfiguration : ModelConfiguration
{
    protected void Configure()
    {
        Entity<Person>(entity => entity.WithConcurrencyToken(person => person.Version));
    }
}
```

Anche in questo caso, le chiamate ad `UpdateAsync` includeranno un controllo di concorrenza.
