# Identity profile e multitenancy

L'identity profile fornisce una rappresentazione fortemente tipizzata del claim associati ad un utente autenticato. Questo servizio viene modellato come un'interfaccia avente almeno due proprietà `IsAuthenticated` e `UserId` ereditate dall'interfaccia base `IIdentityProfile<TUserId>` ed, opzionalmente, la proprietà `TenantId` ereditata da `ITenantProfile<TTenantId>`, se l'applicazione è multi-tenant; oltre a queste proprietà, se ne possono definire altre, a seconda del modello dei claim dell'utente.
Utilizzando l'identity profile, si può accedere ai claim dell'utente tramite proprietà, anziché tramite l'interfaccia simile a quella di un dizionario fornita da `ClaimsPrincipal`, avendo anche la conversione del claim nel tipo che lo rappresenta, a partire dalla stringa in cui il suo valore è memorizzato.

## HowTo: Definire l'IdentityProfile

La seguente sezione si basa sull'assunzione che l'autenticazione sia stata già configurata utilizzando il metodo `AddAuthentication` di ASP.NET Core, la cui documentazione è disponibile [qui](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/?view=aspnetcore-7.0).

Per definire l'interfaccia che modella l'identity profile, utilizzare la sezione `identity`. All'interno, definire una lista di `claims` (che può essere anche vuota) definendo, per ciascun claim, `name` (nome del claim, ovvero della proprietà), `type` (tipo del claim), `key` (chiave del claim utilizzata nella serializzazione) e `isOptional` (specifica se il claim è opzionale o meno):

```yml
identity:
  claims:
    - name: givenName
      type: string
      key: given_name
      isOptional: false
```

Ciò genererà:

```cs
public interface IApplicationIdentityProfile : IIdentityProfile<Guid>
{
    string GivenName { get; }
}

public class ApplicationClaimsIdentityProfile : ClaimsIdentityProfile<Guid>, IApplicationIdentityProfile
{
    public ApplicationClaimsIdentityProfile(IHttpContextAccessor httpContextAccessor)
        : base(httpContextAccessor)
    {
    }

    public string GivenName => ...;
}
```

Il servizio sarà registrato nel container di IoC e sarà possibile richiedere un'istanza dell'interfaccia `IApplicationIdentityProfile` normalmente tramite Dependency Injection.

Di default, il claim `UserId` è di tipo `Guid`. Per utilizzare un altro tipo, specificarlo nella sotto-sezione `userId`. Ad esempio, per renderlo di tipo `string`:

```yml
identity:
  claims:
    - name: givenName
      type: string
      key: given_name
      isOptional: false
  userId:
    type: string
```

Se l'applicazione è multi-tenant, specificare tramite la sotto-sezione `tenantId` la chiave da usare per tale claim e, opzionalmente, il tipo (di default è `Guid`).

```yml
identity:
  claims:
    - name: givenName
      type: string
      key: given_name
      isOptional: false
  userId:
    type: string
  tenantId:
    key: http://schemas.microsoft.com/identity/claims/tenantid
```

Il generato in questo caso è:

```cs
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

## HowTo: Impostare la feature multitenancy (solo con EFCore 7+)
 
Dopo aver definito il claim tenant id, nella sezione `data` definire il campo `multitenancy` con valore a `true`:

```yml
data:
  orm: EntityFrameworkCore
  multitenancy: true
```

Tutte le entità segregate per tenant potranno essere definite tramite `isTenantEntity: true`, ad esempio:

```yml
entities:
  - name: Customer
    description: Customer Entity
    useRepository: true
    isTenantEntity: true
    fields:
      - name: name
        type: string
        description: Customer name
      - name: surname
        type: string
        description: Customer surname
```

In questa maniera, le query che coinvolgono queste entità conterranno automaticamente un filtro che utilizzerà il valore del tenant id dell'utente che ha effettuato la richiesta.

Per disabilitare il filtro puntualmente (a livello della singola query), utilizzare il metodo di estensione `AsNoMultitenancy()` di `IQueryable<T>`, ad esempio:

```cs
var bobCustomers = context.Set<Customer>()
    .AsNoMultitenancy()
    .Where(name => name == "Bob")
    .ToList();
```
