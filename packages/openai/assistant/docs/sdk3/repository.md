# Repository

Il Code Architects platform supporta l'uso del [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html).

Una volta definito il modello di un'entità di dominio, è possibile dotarlo automaticamente di un repository utilizzando la proprietà `useRepository`:

```yaml
entities:
  ...
  - name: Product
    ...
    useRepository: true
    ...
  ...
```

Questo flag imposterà la creazione di un repository per l'entità `Product` che implementa il Generic Repository Pattern. In particolare, verrà generata un'interfaccia che estende l'interfaccia generica `IRepository<TEntity, TKey>`:

```c#
public interface IProductRepository : IRepository<Product, Guid>
{
}
```

Verrà anche generata una classe che estende la classe generica `Repository<TEntity, TKey>` e che implementa l'interfaccia generata:

```c#
public interface ProductRepository : Repository<Product, Guid>, IProductRepository
{
}
```

Il repository conterrà le query e i comandi per recuperare o modificare le entità. Per farlo, è sufficiente definire i metodi nell'interfaccia ed implementarli nel repository concreto.
