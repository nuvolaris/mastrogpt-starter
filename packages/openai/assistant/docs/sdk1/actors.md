# Actor model

L'Actor Model è un paradigma di programmazione utilizzato per creare sistemi distribuiti e concurrenti. In questo modello, gli attori sono unità indipendenti di lavoro che possono inviare messaggi gli uni agli altri e modificare il proprio stato interno in base ai messaggi ricevuti. Gli attori non condividono la memoria e non hanno accesso diretto agli stati degli altri attori, il che li rende facili da scrivere e testare in modo indipendente. Inoltre, gli attori possono processare un solo messaggio alla volta e questo, unito al fatto che non condividono lo stato interno, li porta ad essere degli oggetti intrinsicamente liberi da race conditions (thread-safe).

L'Actor Model è nato negli anni 70 ed è stato adottato in diverse varianti all'interno dei vari linguaggi di programmazione. Ad esempio, alcuni linguaggi nativamente adottano questo paradigma (es. Erlang, Elixir), mentre si può dire che il concetto di "oggetto" nella programmazione ad oggetti sia stato influenzato dal concetto di attore.

## Definizione di un attore

Un attore è caratterizzato da tre componenti fondamentali.

- Identità: ciascun attore è distinto dal proprio tipo e dal proprio id: attraverso questi due, un attore può essere univocamente identificato.
- Comportamento: gli attori definiscono dei metodi che sono invocabili dall'esterno.
- Stato: gli attori possono disporre di uno stato mutabile, che viene persistito esternamente e permette ad un'istanza di un attore di essere facilmente spostata da un processo all'altro.

In un contesto distribuito, in cui esistono diverse repliche dello stesso servizio in cui un attore è definito, l'invocazione di un attore può avvenire a cavallo di repliche diverse: ovvero, il chiamante può invocare un metodo di un attore che verrà eseguito su un'altra replica, in maniera totalmente trasparente. Le istanze potranno anche essere ricollocate su altre repliche, in base alle necessità e alle contingenze dell'applicazione.

Un attore è definito a partire da una normale classe e interfaccia che la classe implementa: l'interfaccia definisce dei metodi che il client dell'attore può utilizzare per invocarlo, la cui logica è implementata nella classe che modella l'attore.

> Nota: negli esempi mostrati in seguito, l'attore è configurato attraverso attributi applicati su classi e membri, che definiscono i metadati utili alla gestione dell'attore. L'utilizzo degli attributi non è l'unico metodo di configurazione, ma è quello più semplice e immediato. In seguito, verrà spiegato come configurare l'attore utilizzando le fluent API di configurazione.

Di seguito, verrà descritto un esempio di implementazione di un attore che modella un semaforo che controlla un'intersezione.

## Interfaccia e implementazione

Il semaforo modellato è un oggetto che può trovarsi in quattro stati:

- Verde: è possibile attraversare l'intersezione.
- Giallo: è possibile attraversare l'intersezione, ma per meno tempo rispetto al verde.
- Rosso: non è possibile attraversare l'intersezione.
- Spento: il semaforo non è attivo e non può essere utilizzato.

Quando il semaforo non è attivo, può essere attivato e diventerà verde. Dopo 30 secondi, la luce diventa gialla, per poi diventare rossa dopo 10 secondi. Anche il rosso dura 30 secondi, per poi diventare verde e ripetere il ciclo. Quando il semaforo è attivo (verde, giallo o rosso), il client del semaforo può interrogare l'attore sul colore attuale della luce, chiedere di superare l'incrocio e disattivare il semaforo, riportandolo nello stato "spento". Inoltre, la particolare logica di questo semaforo prevede che, quando è verde, dopo che un numero prestabilito di macchine supera l'incrocio, il colore della luce diventa giallo senza aspettare che siano passati i regolari 30 secondi. I metodi che l'attore espone all'esterno saranno i seguenti.

```cs
public interface ITrafficLight
{
    Task TurnOnAsync(CancellationToken cancellationToken = default);
    
    Task TurnOffAsync(CancellationToken cancellationToken = default);
    
    ValueTask<string> GetLightColorAsync(CancellationToken cancellationToken = default);
    
    Task<TrafficLightResponse> CrossIntersectionAsync(int numberOfCars, CancellationToken cancellationToken = default);
}

public class TrafficLightResponse
{
    public bool CanCross { get; set; } // Indica se le auto possono superare l'incrocio

    public DateTime TurnsGreenAt { get; set; } // Se la luce è rossa, comunica quando ritornerà verde
}
```

Notare come è il tipo di ritorno dei metodi può essere di tipo `Task`, `Task<T>`, `ValueTask`, `ValueTask<T>`, dove `T` deve essere serializzabile (come `string`, o un oggetto complesso come `TrafficLightResponse`, composto da proprietà a loro volta serializzabili). Anche i parametri dei metodi (fatta eccezione per l'opzionale `CancellationToken`, che dev'essere l'ultimo parametro del metodo) devono essere serializzabili secondo lo stesso criterio.

L'interfaccia potrà essere normalmente implementata, senza l'estensione di alcuna classe base.

```cs
using CodeArchitects.Platform.Actors;

[Actor]
public class TrafficLight : ITrafficLight
{
    public Task TurnOnAsync(CancellationToken cancellationToken = default)
    {
        ...
    }
    
    public Task TurnOffAsync(CancellationToken cancellationToken = default)
    {
        ...
    }
    public ValueTask<string> GetLightColorAsync(CancellationToken cancellationToken = default)
    {
        ...
    }
    
    public Task<TrafficLightResponse> CrossIntersectionAsync(int numberOfCars, CancellationToken cancellationToken = default)
    {
        ...
    }
}
```

La classe dev'essere decorata con l'attributo `[Actor]` che, oltre a permettere il riconoscimento dell'attore quando viene registrato l'intero assembly (vedere sez ...), rende la classe oggetto dell'analizzatore che segnalerà a compile-time errori nel design che altrimenti sarebbero rilevati a runtime (vedere sez ...).

## Gestione dello stato

Questo attore avrà bisogno di memorizzare le informazioni sul suo stato, che è modellato dalla seguente classe.

```cs
public class TrafficLightState
{
    public int MaxCarsBeforeYellow { get; set; } // Indica il numero di auto che può passare con il verde prima che la luce diventi gialla
    
    public int CarsBeforeYellow { get; set; } // Tiene traccia del numero di auto passate con il verde
    
    public DateTime TurnsGreenAt { get; set; } // Memorizza l'orario in cui la luce ritorna verde

    public LightColor Color { get; set; } // Indica il colore del semaforo
}

public enum LightColor
{
    Green,
    Yellow,
    Red,
    Off
}
```

Sebbene lo stato sia persistito al di fuori dell'applicazione (in uno state store), non c'è bisogno di leggerlo esplicitamente quando necessario, in maniera imperativa. Invece, la gestione dello stato avviene in maniera dichiarativa, marcando con l'attributo `[State]` il campo o la proprietà dell'attore che si vuole rendere parte dello stato.

```cs
using CodeArchitects.Platform.Actors;

[Actor]
public class TrafficLight : ITrafficLight
{
    [State]
    private TrafficLightState _state;

    public TrafficLight(TrafficLightState state)
    {
        _state = state;
    }

    ...
}
```

Ci deve essere una corrispondenza uno-ad-uno tra i parametri del costruttore e le componenti dello stato dell'attore. Il nome del parametro dovrebbe adottare la notazione camelCase, mentre i membri dichiarati come stato possono utilizzare le seguenti notazioni:

- camelCase,
- _camelCase (con `_` come prefisso),
- m_camelCase (con `m_` come prefisso),
- PascalCase (le proprietà devono utilizzare questa notazione).

Ogni cambiamento fatto allo stato sarà implicitamente salvato al termine dell'esecuzione del metodo.

## Dependency injection e actor context

Oltre alle componenti dello stato, è possibile iniettare nei parametri del costruttore qualsiasi servizio registrato nel container di IoC.
Inoltre, è possibile richiedere un'istanza del servizio `IActorContext<TActor>` (o della sua versione non generica, `IActorContext`). Questo servizio, disponibile unicamente per gli attori, permette di accedere ad informazioni contestuali (ad esempio, l'id dell'attore) e a funzioni della runtime che ospita l'actor system (ad esempio, scheduling).

> Nota: `IActorContext<TActor>` e `IActorContext` non sono registrati all'interno del container di IoC, pertanto qualsiasi tentativo di iniezione all'interno di un servizio che non sia un attore provocherà un'eccezione.

Ad esempio, per utilizzare l'actor context ed un logger all'interno dell'attore, si aggiornerebbe la lista delle dipendenze nel seguente modo.

```cs
using CodeArchitects.Platform.Actors;

[Actor]
public class TrafficLight : ITrafficLight
{
    [State]
    private TrafficLightState _state;
    private readonly ILogger<TrafficLight> _logger;
    private readonly IActorContext<TrafficLight> _context;

    public TrafficLight(TrafficLightState state, ILogger<TrafficLight> logger, IActorContext<TrafficLight> context)
    {
        _state = state;
        _logger = logger;
        _context = context;
    }

    ...
}
```

## Attori virtuali e invocazione

Per richiamare i metodi di un attore, è necessario creare il proxy che invocherà l'attore, potenzialmente in maniera remota, specificando l'id dell'attore da invocare. La libreria CodeArchitects.Platform.Actors include un generatore di codice che genera automaticamente una factory fortemente tipizzata per ciascun attore; in altre parole, non si ha un'interfaccia con un metodo `Create` generico, ma si utilizza una factory specifica per ciascun attore. Uno dei motivi riguarda l'inizializzazione dell'attore.

Gli attori sono divisi in due categorie: virtuali e non. Un attore virtuale non ha bisogno di un'inizializzazione esplicita dello stato: non essendoci il bisogno di inizializzarli, non esiste il concetto di esplicita creazione (o di distruzione) dell'attore. Se un attore viene invocato e la sua memoria non è stata ancora allocata, verrà allocata in quel momento. Se, invece, l'attore necessita di un'esplicita inizalizzazione dello stato, sarà necessario distinguere la sua creazione dalla sua invocazione.

La factory degli attori espone due metodi per la creazione del proxy.

- `CreateAsync`: utilizzato per la creazione degli gli attori non virtuali; va utilizzato per creare il proxy per la prima invocazione dell'attore.
- `Get`: utilizzato per gli attori virtuali e per tutte le invocazioni di un attore non-virtuale successive alla creazione.

Per l'attore `TrafficLight`, la factory generata avrà la seguente struttura.

```cs
[ActorFactory(typeof(TrafficLight))]
public interface ITrafficLightFactory
{
    Task<ITrafficLight> CreateAsync(string id, TrafficLightState state, CancellationToken cancellationToken = default);

    ITrafficLight Get(string id);
}
```

Il metodo `CreateAsync` è asincrono perché procede all'inizializzazione remota dell'attore, valorizzando il lo stato con il valore assegnato al parametro state. È da notare come i parametri di questo metodo devono essere sincronizzati con la struttura dello stato dell'attore: aggiungendo un altro membro marcato con `[State]`, ai parametri di questo metodo verrà aggiunto il corrispondente parametro che valorizzerà la nuova componente dello stato; ciò spiega la necessità di generare dinamicamente l'interfaccia a compile-time tramite un generatore di codice, in modo tale che sia sempre aggiornata e rispecchi la struttura dello stato dell'attore. La factory è registrata all'interno del container di IoC ed è possibile utilizzare la Dependency Injection per risolverne un'istanza.

Un esempio di utilizzo della factory è il seguente:

```cs
ITrafficLightFactory factory = ...; // Risolta tramite DI

ITrafficLight actor = await factory.CreateAsync("id-attore", new TrafficLightState());
await actor.TurnOnAsync();

// ... in un contesto successivo alla creazione ...

ITrafficLight actor = factory.Get("id-attore");
string color = await actor.GetLightColorAsync();
```

In questo caso, l'attore non richiede una esplicita inizializzazione dello stato da parte del chiamante, perciò è idoneo ad essere considerato un attore virtuale. Ciò va indicato esplicitamente attraverso l'attributo `[Virtual]`.

```cs
using CodeArchitects.Platform.Actors;

[Actor, Virtual]
public class TrafficLight : ITrafficLight
{
    ...
}
```

L'interfaccia della factory verrà immediatamente sincronizzata e verrà rimosso il metodo `CreateAsync`.

```cs
[ActorFactory(typeof(TrafficLight))]
public interface ITrafficLightFactory
{
    ITrafficLight Get(string id);
}
```

Per utilizzare quest'attributo, è necessario che ciascuna componente dello stato sia inizializzabile tramite:

- valore di default, se il tipo è un value-type: ad esempio, una componente dello stato di tipo `int` ha come valore di default `0`;
- costruttore senza parametri, se il tipo è una classe come nel caso di `TrafficLightState`.

Un esempio in cui queste condizioni non si verificano è per componenti di tipo `string`: questo tipo non ha un valore di default (`null` non è accettato). In questi casi, si può specificare un valore di default tramite la proprietà `Default` dell'attributo `[State]`.

```cs
[State(Default = "default-state")]
private string _state;
```

## Impostare il tipo di id

Di default, il tipo utilizzato per l'id degli attori è `string`, ma si può scegliere qualsiasi altro tipo che possa essere convertito in una stringa. In particolare, per utilizzare un altro tipo per l'id, esso deve definire un metodo statico `Parse(string)` oppure `Parse(string, IFormatProvider)`, il cui valore di ritorno sia proprio di quel tipo. Ad esempio, `Guid`, `int`, `long` sono tutti tipi adatti.

> Nota: in .NET 7 è stata introdotta una nuova interfaccia, `IParsable<TSelf>` che definisce il metodo `Parse(string, IFormatProvider)` sfruttando la nuova feature nota come "[static abstract members](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/proposals/csharp-11.0/static-abstracts-in-interfaces)". Pertanto, tutti i tipi che implementano questa interfaccia sono adatti ad essere utilizzati per l'id di un attore.

Per impostare il tipo di id da utilizzare, si applica l'attributo `[ActorIdType]` (o anche la sua versione generica, se si utilizza C#11) sull'attore.

```cs
using CodeArchitects.Platform.Actors;
[Actor, Virtual, ActorIdType<Guid>] // alternativamente, ActorIdType(typeof(Guid))
public class TrafficLight : ITrafficLight
{
    ...
}
```

In questo esempio, si indica che il tipo di id dell'attore sarà `Guid`. Il generatore di codice riconoscerà questa indicazione e modificherà la firma dei metodi della factory.

```cs
[ActorFactory(typeof(TrafficLight))]
public interface ITrafficLightFactory
{
    ITrafficLight Get(System.Guid id);
}
```

## Accedere all'id dell'attore

L'interfaccia `IActorContext` espone una proprietà chiamata `ActorId` che contiene il valore dell'id dell'attore. Questa proprietà è di tipo `string`, perché gli id di qualunque tipo vengono trasformati in stringa per poter essere gestiti dalla runtime. Se, però, è stato scelto un altro tipo di id, è possibile evitare di dover convertire la stringa, nel nostro esempio, utilizzando `Guid.Parse(_context.ActorId)`, marcando il membro a cui verrà assegnato l'id tramite l'attributo `[ActorId]`.

```cs
using CodeArchitects.Platform.Actors;

[Actor, Virtual, ActorIdType<Guid>]
public class TrafficLight : ITrafficLight
{
    [State]
    private TrafficLightState _state;
    private readonly ILogger<TrafficLight> _logger;
    private readonly IActorContext<TrafficLight> _context;
    [ActorId]
    private readonly Guid _id;

    public TrafficLight(TrafficLightState state, ILogger<TrafficLight> logger, IActorContext<TrafficLight> context, Guid id)
    {
        _state = state;
        _logger = logger;
        _context = context;
        _id = id;
    }

    ...
}
```

Questo rende anche superfluo l'utilizzo dell'attributo `[ActorIdType]`, in quanto esso verrà dedotto dal tipo del membro marcato con `[ActorId]`. È possibile decorare con questo attributo anche membri già decorati con l'attributo `[State]`.

Inoltre, se l'id fosse stato parte della classe `TrafficLightState`, sarebbe stato possibile segnalarlo utilizzando l'interfaccia `IActorIdSource<TActorId>`, implementando i metodi `GetActorId` e `SetActorId`.

```cs
public class TrafficLightState : IActorIdSource<Guid>
{
    public Guid Id { get; set; }

    public int MaxCarsBeforeYellow { get; set; }
    
    public int CarsBeforeYellow { get; set; }
    
    public DateTime TurnsGreenAt { get; set; }

    public LightColor Color { get; set; }

    public Guid GetActorId() => Id;

    public void SetActorId(Guid id) => Id = id;
}
```

Anche in questo caso, l'aver specificato il tipo di id rende superfluo l'uso dell'attributo `[ActorIdType]`.

## Scheduling

L'actor context offre la possibilità di programmare l'esecuzione di un'attività nel futuro, in maniera periodica o meno. Attraverso i vari overload del metodo `ScheduleAsync` si può indicare quale metodo dell'attore eseguire, quando e con che frequenza.

In questo esempio, una volta acceso, il semaforo diventa verde e dovrà diventare giallo dopo 30 secondi, poi rosso dopo 10 secondi e di nuovo verde dopo 30 secondi.

```cs
using CodeArchitects.Platform.Actors;

[Actor, Virtual]
public class TrafficLight : ITrafficLight
{
    ...

    public async Task TurnOnAsync(CancellationToken cancellationToken = default)
    {
        if (_state.Color is not LightColor.Off)
            throw new InvalidOperationException("I was already started!");

        await TurnGreenAsync("traffic light is starting");
    }

    private async Task TurnRedAsync(string reason)
    {
        _logger.LogInformation("Turning red. Reason: {reason}.", reason);

        _state.Color = LightColor.Red;

        TimeSpan timer = TimeSpan.FromSeconds(30);
        _state.TurnsGreenAt = DateTime.Now + timer;

        await _context.ScheduleAsync(self => self.TurnGreenAsync("regular schedule"), SchedulingOptions.In(timer));
    }

    private async Task TurnYellowAsync(string reason)
    {
        _logger.LogInformation("Turning yellow. Reason: {reason}.", reason);

        _state.Color = LightColor.Yellow;

        await _context.ScheduleAsync(self => self.TurnRedAsync("regular schedule"), SchedulingOptions.In(10.Seconds()));
    }

    private async Task TurnGreenAsync(string reason)
    {
        _logger.LogInformation("Turning green. Reason: {reason}", reason);

        _state.Color = LightColor.Green;

        await _context.ScheduleAsync(self => self.TurnYellowAsync("regular schedule"), SchedulingOptions.In(30.Seconds()));
    }
}
```

`ScheduleAsync` accetta una lambda che rappresenta il metodo da eseguire, completo degli argumenti da passargli. Il parametro di tipo `SchedulingOptions` è utilizzato per indicare il timer che farà scattare l'esecuzione dell'attività e/o il periodo. Inoltre, è possibile utilizzare i metodi di estensione `Seconds()`, `Minutes()` e `Hours()` per rendere più leggibili questi intervalli di tempo.

Se si vuole annullare lo scheduling di un'attività, è possibile farlo attraverso il metodo `UnscheduleAsync`. Esso accetta un parametro di tipo `ScheduleId`, che identifica uno scheduling in maniera univoca: tale id dovrà essere stato passato anche alla chiamata a `ScheduleAsync`. Ad esempio, è necessario annullare il cambio di colore quando il semaforo viene spento.

```cs
using CodeArchitects.Platform.Actors;

[Actor, Virtual]
public class TrafficLight : ITrafficLight
{
    private static readonly ScheduleId _turnGreenSchedule = ScheduleId.New("TurnGreen");
    private static readonly ScheduleId _turnRedSchedule = ScheduleId.New("TurnRed");
    private static readonly ScheduleId _turnYellowSchedule = ScheduleId.New("TurnYellow");

    ...

    public async Task TurnOffAsync(CancellationToken cancellationToken = default)
    {
        if (_state.Color is LightColor.Off)
            throw new InvalidOperationException("I am already off!");

        ScheduleId scheduleId = _state.Color switch
        {
            LightColor.Green => _turnRedSchedule,
            LightColor.Yellow => _turnRedSchedule,
            LightColor.Red => _turnGreenSchedule
        };

        _state.Color = Color.Off;

        await _context.UnscheduleAsync(scheduleId, cancellationToken);
    }

    private async Task TurnRedAsync(string reason)
    {
        _logger.LogInformation("Turning red. Reason: {reason}.", reason);

        _state.Color = LightColor.Red;

        TimeSpan timer = TimeSpan.FromSeconds(30);
        _state.TurnsGreenAt = DateTime.Now + timer;

        await _context.ScheduleAsync(_turnGreenSchedule, self => self.TurnGreenAsync("regular schedule"), SchedulingOptions.In(timer));
    }

    private async Task TurnYellowAsync(string reason)
    {
        _logger.LogInformation("Turning yellow. Reason: {reason}.", reason);

        _state.Color = LightColor.Yellow;

        await _context.ScheduleAsync(_turnRedSchedule, self => self.TurnRedAsync("regular schedule"), SchedulingOptions.In(10.Seconds()));
    }

    private async Task TurnGreenAsync(string reason)
    {
        _logger.LogInformation("Turning green. Reason: {reason}", reason);

        _state.Color = LightColor.Green;
        _state.CarsBeforeYellow = 0;

        await _context.ScheduleAsync(_turnYellowSchedule, self => self.TurnYellowAsync("regular schedule"), SchedulingOptions.In(30.Seconds()));
    }
}
```

## Polimorfismo

Completiamo l'implementazione di `TrafficLight` aggiungendo i due metodi mancanti.

```cs
using CodeArchitects.Platform.Actors;

[Actor, Virtual]
public class TrafficLight : ITrafficLight
{
    ...

    public ValueTask<string> GetLightColorAsync(CancellationToken cancellationToken = default)
    {
        if (_state.Color is LightColor.Off)
            ValueTask.FromException<string>(new InvalidOperationException("I was not started!"));

        return ValueTask.FromResult(_state.Color switch
        {
            LightColor.Green => "#00FF00",
            LightColor.Yellow => "#FFFF00",
            LightColor.Red => "#FF0000"
        });
    }

    public async Task<TrafficLightResponse> CrossIntersectionAsync(int numberOfCars, CancellationToken cancellationToken = default)
    {
        switch (_state.Color)
        {
            case LightColor.Red:
                return new TrafficLightResponse
                {
                    CanCross = false,
                    TurnsGreenAt = _state.TurnsGreenAt
                };
            case LightColor.Yellow:
                return new TrafficLightResponse
                {
                    CanCross = true
                };
            case LightColor.Green:
                _state.CarsBeforeYellow += numberOfCars;
                if (_state.CarsBeforeYellow >= _state.MaxCarsBeforeYellow)
                {
                    _state.MaxCarsBeforeYellow += 3;
                    await _context.UnscheduleAsync(_turnRedSchedule, cancellationToken);
                    await TurnYellowAsync("too many cars have passed");
                }

                return new TrafficLightResponse
                {
                    CanCross = true;
                };
            case LightColor.Off:
                throw new InvalidOperationException("I was not started!");
        }
    }
}
```

È evidente che il comportamento del semaforo cambia parecchio in base al colore in cui si trova, ovvero in base al suo stato, come si vede dall'utilizzo massiccio di `if` e `switch`. Se in casi semplici come questo, ciò non rappresenta un problema, in scenari più complessi è consigliabile utilizzare il polimorfismo, creando un'implementazione per ciascuno degli stati in cui si può trovare l'attore che cambiano pesantemente il suo comportamento. In questo caso, creeremo un'implementazione per ciascuno dei valori che può assumere `LightState`, rendendo la classe base `TrafficLight` astratta. Ciascuna implementazione andrà decorata con l'attributo `[ActorImplementation]` (o, alternativamente, con la sua versione generica `[ActorImplementation<TActor>]`).

```cs
[Actor, Virtual]
public abstract class TrafficLight : ITrafficLight
{
    protected static readonly ScheduleId _turnGreenSchedule = ScheduleId.New("TurnGreen");
    protected static readonly ScheduleId _turnRedSchedule = ScheduleId.New("TurnRed");
    protected static readonly ScheduleId _turnYellowSchedule = ScheduleId.New("TurnYellow");

    [State]
    protected TrafficLightState _state;
    protected readonly IActorContext<TrafficLight> _context;
    [ActorId]
    protected readonly Guid _id;
  
    public TrafficLight(Guid id, TrafficLightState state, IActorContext<TrafficLight> context)
    {
      _id = id;
      _state = state;
      _context = context;
    }

    protected abstract ILogger<TrafficLight> Logger { get; }

    public abstract Task TurnOnAsync(CancellationToken cancellationToken = default);

    public abstract Task TurnOffAsync(CancellationToken cancellationToken = default);

    public abstract ValueTask<string> GetLightColorAsync(CancellationToken cancellationToken = default);

    public abstract Task<TrafficLightResponse> CrossIntersectionAsync(CancellationToken cancellationToken = default);
    
    protected virtual async Task TurnRedAsync(string reason)
    {
        Logger.LogInformation("Turning red. Reason: {reason}.", reason);

        _context.Become<RedTrafficLight>();

        TimeSpan timer = TimeSpan.FromSeconds(30);
        _state.TurnsGreenAt = DateTime.Now + timer;

        await _context.ScheduleAsync(_turnGreenSchedule, self => self.TurnGreenAsync("regular schedule"), SchedulingOptions.In(timer));
    }

    protected virtual async Task TurnYellowAsync(string reason)
    {
        Logger.LogInformation("Turning yellow. Reason: {reason}.", reason);

        _context.Become<YellowTrafficLight>();

        await _context.ScheduleAsync(_turnRedSchedule, self => self.TurnRedAsync("regular schedule"), SchedulingOptions.In(10.Seconds()));
    }

    protected virtual async Task TurnGreenAsync(string reason)
    {
        Logger.LogInformation("Turning green. Reason: {reason}.", reason);

        _state.CarsBeforeYellow = 0;
        _context.Become<GreenTrafficLight>();

        await _context.ScheduleAsync(_turnYellowSchedule, self => self.TurnYellowAsync("regular schedule"), SchedulingOptions.In(30.Seconds()));
    }
}

[ActorImplementation<TrafficLight>] // alternativamente, ActorImplementation(typeof(TrafficLight))
public class InactiveTrafficLight : TrafficLight
{
    private readonly ILogger<InactiveTrafficLight> _logger;

    public InactiveTrafficLight(Guid id, TrafficLightState state, IActorContext<TrafficLight> context, ILogger<InactiveTrafficLight> logger)
        : base(id, state, context)
    {
        _logger = logger;
    }

    protected override ILogger<TrafficLight> Logger => _logger;

    public override async Task TurnOnAsync(CancellationToken cancellationToken = default)
    {
        await TurnGreenAsync("traffic light is starting");
    }

    public override Task TurnOffAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromException(new InvalidOperationException("I am already off!"));
    }

    public override ValueTask<string> GetLightColorAsync(CancellationToken cancellationToken = default)
    {
        return ValueTask.FromException<string>(new InvalidOperationException("I was not started!"));
    }

    public override Task<TrafficLightResponse> CrossIntersectionAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromException<TrafficLightResponse>(new InvalidOperationException("I was not started!"));
    }
}

public abstract class ActiveTrafficLight : TrafficLight // questa non è ancora un'implementazione concreta dell'attore, ma un'ulteriore classe base per le implementazioni GreenTrafficLight, YellowTrafficLight e RedTrafficLight
{
    protected ActiveTrafficLight(Guid id, TrafficLightState state, IActorContext<TrafficLight> context)
        : base(id, state, context)
    {
    }

    protected abstract ScheduleId ChangeColorSchedule { get; }

    public override Task TurnOnAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromException(new InvalidOperationException("I was already started!"));
    }

    public override async Task TurnOffAsync(CancellationToken cancellationToken = default)
    {
        Logger.LogInformation("Traffic light is stopping.");

        await _context.UnscheduleAsync(ChangeColorSchedule, cancellationToken);

        _context.Become<InactiveTrafficLight>();
    }
}

[ActorImplementation<TrafficLight>]
public class GreenTrafficLight : ActiveTrafficLight
{
    private readonly ILogger<GreenTrafficLight> _logger;

    public GreenTrafficLight(Guid id, TrafficLightState state, IActorContext<TrafficLight> context, ILogger<GreenTrafficLight> logger)
        : base(id, state, context)
    {
        _logger = logger;
    }

    protected override ILogger<TrafficLight> Logger => _logger;

    protected override ScheduleId ChangeColorSchedule => _turnYellowSchedule;

    public override ValueTask<string> GetLightColorAsync(CancellationToken cancellationToken = default)
    {
        return ValueTask.FromResult("#00FF00");
    }

    public override Task<TrafficLightResponse> CrossIntersectionAsync(CancellationToken cancellationToken = default)
    {
        _state.CarsBeforeYellow++;
        if (_state.CarsBeforeYellow >= _state.MaxCarsBeforeYellow)
        {
            await OnTooManyCarsAsync(cancellationToken);
        }

        return Task.FromResult(new TrafficLightResponse
        {
            CanCross = true
        });
    }

    protected override Task TurnGreenAsync(string reason, int maxCarsIncrement)
    {
        return Task.FromException(new InvalidOperationException("I am already green!"));
    }

    private async Task OnTooManyCarsAsync(CancellationToken cancellationToken = default)
    {
        _state.MaxCarsBeforeYellow += 3;

        await _context.UnscheduleAsync(_turnYellowSchedule);

        await TurnYellowAsync("too many cars have passed");
    }
}

[ActorImplementation<TrafficLight>]
public class YellowTrafficLight : ActiveTrafficLight
{
    private readonly ILogger<YellowTrafficLight> _logger;

    public YellowTrafficLight(Guid id, TrafficLightState state, IActorContext<TrafficLight> context, ILogger<YellowTrafficLight> logger)
        : base(id, state, context)
    {
        _logger = logger;
    }

    protected override ILogger<TrafficLight> Logger => _logger;

    protected override ScheduleId ChangeColorSchedule => _turnRedSchedule;

    public override ValueTask<string> GetLightColorAsync(CancellationToken cancellationToken = default)
    {
        return ValueTask.FromResult("#FFFF00");
    }

    public override Task<TrafficLightResponse> CrossIntersectionAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromResult(new TrafficLightResponse
        {
            CanCross = true
        });
    }

    protected override Task TurnYellowAsync(string reason)
    {
        return Task.FromException(new InvalidOperationException("I am already yellow!"));
    }
}

[ActorImplementation<TrafficLight>]
public class RedTrafficLight : ActiveTrafficLight
{
    private readonly ILogger<RedTrafficLight> _logger;

    public RedTrafficLight(Guid id, TrafficLightState state, IActorContext<TrafficLight> context, ILogger<RedTrafficLight> logger)
        : base(id, state, context)
    {
        _logger = logger;
    }

    protected override ILogger<TrafficLight> Logger => _logger;

    protected override ScheduleId ChangeColorSchedule => _turnGreenSchedule;

    public override ValueTask<string> GetLightColorAsync(CancellationToken cancellationToken = default)
    {
        return ValueTask.FromResult("#FF0000");
    }

    public override Task<TrafficLightResponse> CrossIntersectionAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromResult(new TrafficLightResponse
        {
            CanCross = false,
            TurnsGreenAt = _state.TurnsGreenAt
        });
    }

    protected override Task TurnRedAsync(string reason)
    {
        return Task.FromException(new InvalidOperationException("I am already red!"));
    }
}
```

È evidente come il codice risulta più object-oriented e pulito, in quanto privo di `if` e `switch` legati al valore di `_state.Color` che, inoltre, risulta adesso superfluo.

```cs
public class TrafficLightState
{
    public int MaxCarsBeforeYellow { get; set; }
    
    public int CarsBeforeYellow { get; set; }
    
    public DateTime TurnsGreenAt { get; set; }
}
```

Notare come sia stato utilizzato il metodo `Become<TImplementation>` fornito dall'interfaccia `IActorContext` per cambiare dinamicamente l'implementazione dell'attore. Una volta che è chiamato questo metodo, l'attore cambierà implementazione a partire dalla chiamata successiva (tramite interfaccia o scheduling).

## Bindings

A volte, si presenta la necessità di eseguire un'azione ogni volta che si verifica una particolare transizione di stato, ovvero quando lo stato passa da un determinato valore ad un altro. Questo si traduce nella scrittura di blocchi `if` ogni volta che viene modificato lo stato in una maniera che potenzialmente inneschi la condizione per eseguire l'azione desiderata. La funzione "bindings" degli attori permette di automatizzare questa procedura, evitando di dover scrivere tutte queste istruzioni `if`: in particolare, un binding è un'azione la cui esecuzione è innescata da una determinata transizione di stato. Ad esempio, volendo rimpiazzare il controllo `if (_state.CarsBeforeYellow >= _state.MaxCarsBeforeYellow) { await OnTooManyCarsAsync(); }` a seguito dell'operazione sullo stato `_state.CarsBeforeYellow++;` con un binding automatico, è necessario registrare il binding nel costruttore dell'attore e abilitarlo.

```cs
[ActorImplementation<TrafficLight>]
public class GreenTrafficLight : ActiveTrafficLight
{
    public GreenTrafficLight(Guid id, TrafficLightState state, IActorContext<TrafficLight> context, ILogger<GreenTrafficLight> logger)
        : base(id, state, context)
    {
        ...

        context.RegisterBinding<GreenTrafficLight>(binding => binding
            .WithPostCondition(self => self._state.CarsBeforeYellow >= self._state.MaxCarsBeforeYellow)
            .IsEnabled()
            .BindTo((self, cancellationToken) => self.OnTooManyCarsAsync(cancellationToken)));
    }

    ...

    public override Task<TrafficLightResponse> CrossIntersectionAsync(CancellationToken cancellationToken = default)
    {
        _state.CarsBeforeYellow++;
        // if (_state.CarsBeforeYellow >= _state.MaxCarsBeforeYellow)
        // {
        //     await OnTooManyCarsAsync(cancellationToken);
        // }

        return Task.FromResult(new TrafficLightResponse
        {
            CanCross = true
        });
    }
}
```

È importante tenere in considerazione che il metodo `OnTooManyCarsAsync` sarà eseguito dopo l'esecuzione del metodo `CrossIntersectionAsync`, anziché dopo l'istruzione `_state.CarsBeforeYellow++`, come accadeva prima.
È chiaro che il vantaggio di questa funzione è maggiore quando ci sono molti punti del codice in cui una determinata azione viene eseguita a seguito di una determinata transizione di stato.

Il metodo `RegisterBinding` può essere richiamato solo all'interno del costruttore e restituisce un'istanza di tipo `BindingId` che può essere memorizzata all'interno di un campo privato dell'attore per poi essere utilizzata per abilitare e disabilitare dinamicamente il binding tramite i metodi `EnableBinding` e `DisableBinding` esposti da `IActorContext`. Nell'esempio mostrato, non è stato necessario richiamare `EnableBinding` perché il binding non è mai disabilitato ed è stato indicato come attivo (`IsEnabled`) in fase di registrazione.
Il metodo `RegisterBinding` accetta opzionalmente un parametro di tipo che indica qual è l'implementazione da utilizzare per l'esecuzione del binding. Il tipo dell'implementazione nel quale il binding è registrato deve poter essere assegnabile al parametro di tipo specificato (nell'esempio, `GreenTrafficLight` è esattamente il tipo dell'implementazione in cui il binding è registrato, ma si sarebbe potuto usare anche `ActiveTrafficLight` se il binding fosse stato definito in quella classe). Se non specificato, il parametro di tipo sottinteso è quello della classe base dell'attore (in questo caso, `TrafficLight`).

L'argomento da passare a `RegisterBinding` è una lambda che configura il binding tramite un builder con API fluent, che espone i seguenti metodi:

- `WithPreCondition`: indica la condizione che dev'essere verificata all'inizio dell'esecuzione di un metodo dell'attore affinché il binding venga eseguito.
- `WithPostCondition`: indica la condizione che dev'essere verificata alla fine dell'esecuzione di un metodo dell'attore affinché il binding venga eseguito.
- `IsEnabled`: permette di abilitare il binding già in fase di registrazione.
- `BindTo`: indica l'azione che verrà richiamata quando le condizioni specificate sono verificate. Notare che se non si specifica né pre-condizione, né post-condizione, il binding verrà eseguito ad ogni chiamata all'attore.

> Nota: è possibile registrare fino ad un massimo di 32 bindings.

## Messaging

Un attore può implementare l'interfaccia `IMessageHandler` definita nella libreria CodeArchitects.Platform.Messaging e sottoscriversi ad uno (o più) messaggi pubblicati utilizzando l'interfaccia `IMessageBus`. Il messaggio deve necessariamente implementare l'interfaccia `IActorMessage<TActorId>` che espone la proprietà `ActorId` attraverso la quale è possibile stabilire quale attore debba ricevere il messaggio.

A titolo di esempio, rimpiazziamo l'invocazione diretta del metodo `TurnOffAsync` con un pattern di tipo pub/sub.

```cs
using CodeArchitects.Platform.Actors.Messaging;

public interface ITrafficLight
{
    Task TurnOnAsync(CancellationToken cancellationToken = default);

    ValueTask<string> GetLightColorAsync(CancellationToken cancellationToken = default);

    Task<TrafficLightResponse> CrossIntersectionAsync(CancellationToken cancellationToken = default);
}

[Message]
public class TurnOffCommand : IActorMessage<Guid>
{
    public Guid ActorId { get; set; }

    public string Reason { get; set; } = "no reason";
}

public abstract class TrafficLight : ITrafficLight, IMessageHandler<TurnOffCommand>
{
    ...
    
    protected abstract Task TurnOffAsync(string reason, CancellationToken cancellationToken = default);

    [MessageHandler(Topic = "traffic-light")]
    public async Task HandleAsync(TurnOffCommand message, CancellationToken cancellationToken)
    {
        await TurnOffAsync(message.Reason, cancellationToken);
    }
```

L'utilizzo dell'interfaccia `IMessageHandler` e dell'attributo `MessageHandler` è identica a quella descritta nella documentazione della libreria CodeArchitects.Platform.Messaging.

## Specificare un costruttore

In caso la classe dell'attore contenga più di un costruttore, è necessario specificare quale verrà utilizzato per la creazione dell'attore quando invocato. Per far ciò, si utilizza l'attributo `[ActorConstructor]`, da applicare al costruttore desiderato.

```cs
public class InactiveTrafficLight : TrafficLight
{
    ...

    public InactiveTrafficLight(TrafficLightState state, IActorContext<TrafficLight> context) // Usato per i test, dove magari l'id non è importante e il logging non serve
        : base(Guid.NewGuid(), state, context)
    {
      _logger = NullLogger<InactiveTrafficLight>.Instance;
    }

    [ActorConstructor]
    public InactiveTrafficLight(Guid id, TrafficLightState state, IActorContext<TrafficLight> context, ILogger<InactiveTrafficLight> logger) // Costruttore usato dalla runtime
        : base(id, state, context)
    {
      _logger = logger;
    }

    ...
}
```

## Configurazione con API fluent

Negli esempi mostrati finora, i metadati utili alla configurazione dell'attore sono stati specificati utilizzando gli attributi, come `[Actor]`, `[Virtual]`, eccetera. Questa è la modalità di configurazione consigliata, in quanto permette all'analizzatore e generatore di codice di rilevare a compile-time eventuali errori e, sempre a compile-time, generare le factory. Tuttavia, se l'utilizzo degli attributi non fosse desiderabile, è possibile configurare l'attore tramite una classe di configurazione con API fluent. Questa classe deve estendere la classe base `ActorConfiguration` e implementare il metodo astratto `Configure`. Nel metodo configure, è possibile utilizzare il metodo `Actor<TActor>` per configurare l'attore. Di seguito è riportato un esempio di configurazione equivalente a quello ottenuto dagli attributi per l'attore `TrafficLight`.

```cs
using CodeArchitects.Platform.Actors.Metadata.Builder;

public class MyActorConfiguration : ActorConfiguration
{
    protected internal override void Configure()
    {
        Actor<TrafficLight>(actor => actor
            .HasFactoryType<ITrafficLightFactory>() // Se la factory non è stata auto-generata, va creata a mano
            .IsVirtual()
            .HasId("_id")
            .HasState("_state")
            .IsMessageHandler(typeof(TurnOffCommand), message => message
                .WithTopic("traffic-light"))
            .HasImplementation<GreenTrafficLight>()
            .HasImplementation<YellowTrafficLight>()
            .HasImplementation<RedTrafficLight>()
            .HasImplementation<InactiveTrafficLight>(impl => impl
                .IsDefault()
                .HasConstructor(arg => new InactiveTrafficLight(
                    arg.OfType<Guid>(),
                    arg.OfType<ActorApp.Domain.TrafficLightState>(),
                    arg.Context(),
                    arg.OfType<ILogger<InactiveTrafficLight>>()))));
    }
}
```

> Nota: questa classe deve definire un costruttore senza parametri (o di default) oppure un costruttore che accetta un'istanza di `IConfiguration`.

## Utilizzo con Dapr e ASP.NET Core

L'attuale implementazione della libreria CodeArchitects.Platform.Messaging è ottenuta utilizzando la runtime per gli attori di Dapr. Per utilizzare questa implementazione, è necessario installare il pacchetto CodeArchitects.Platform.Dapr.AspNetCore. A seguito di questo, è necessario registrare gli actors nel contesto del container di IoC e mappare gli endpoint che riceveranno le invocazioni degli attori. Come altre librerie basate su Dapr, è definito un metodo di estensione dell'interfaccia `IDaprInfrastructureBuilder` (risultato della chiamata a `services.AddDaprInfrastructure`) chiamato `AddActors`. Questo metodo accetta una lambda usata per configurare il sistema ad attori.

```cs
services.AddDaprInfrastructure(options => options.SetConfiguration(configuration))
    .AddActors(actors => actors
        .AddActor<TrafficLight>()
        .AccessPrivates());
```

`AddActor` registra un singolo attore, insieme a tutte le implementazioni e la factory definite nello stesso assembly della classe. Invece di registrare ogni singola classe, è anche possibile registrare tutte le classi marcate con l'attributo [Actor] definite in un assembly tramite il metodo ScanAssembly. `AccessPrivates` è necessario se, come nell'esempio, è necessario che la runtime acceda a metodi privati/protetti dell'attore, ad esempio com'è avvenuto per lo scheduling: ScheduleAsync(self => self.TurnGreenAsync(...)).

Se si ha configurato l'attore tramite fluent API, la registrazione cambia nel seguente modo.

```cs
services.AddDaprInfrastructure(options => options.SetConfiguration(configuration))
    .AddActors(actors => actors
        .UseActorConfiguration<MyActorConfiguration>()
        .AccessPrivates());
```

Mentre i metodi `AddActor` e `ScanAssembly` possono essere utilizzati insieme (perché sono basati entrambi sull'analisi dei metadati tramite reflection), il loro utilizzo è incompatibile con `UseActorConfiguration`, quindi le due modalità di configurazione (reflection e fluent API) sono mutualmente esclusive.

L'altro passaggio necessario è la chiamata al metodo `MapActorsHandlers`, estensione di `IEndpointConventionBuilder`.

```cs
    app.UseEndpoints(endpoints =>
    {
        ...
        endpoints.MapActorsHandlers();
    });
```

### Opzioni di Dapr

Si possono anche configurare le opzioni utilizzate da Dapr per l'actor system, utilizzando il metodo `ConfigureRuntimeOptions`.

```cs
services.AddDaprInfrastructure(options => options.SetConfiguration(configuration))
    .AddActors(actors => actors
        .AddActor<TrafficLight>()
        .AccessPrivates()
        .ConfigureRuntimeOptions(options =>
        {
            runtimeOptions.ActorScanInterval = TimeSpan.FromSeconds(10);
        }));
```

### Integrazione con messaging

Se si utilizza il messaging, è anche necessario registrare gli handler generati per ricevere i messaggi degli attori. Nella sezione di configurazione del messaging (`AddMessaging`) si può fare utilizzando il metodo `ScanAssembly` con l'assembly `ActorMessaging.Assembly`.

```cs
using CodeArchitects.Platform.Actors.Messaging;

services.AddDaprInfrastructure(options => options.SetConfiguration(configuration))
    .AddActors(actors => actors
        .AddActor<TrafficLight>()
        .AccessPrivates()
        .ConfigureRuntimeOptions(options =>
        {
            runtimeOptions.ActorScanInterval = TimeSpan.FromSeconds(10);
        }))
    .AddMessaging(messaging => messaging
        .AddMessage<TurnOffCommand>()
        .ScanAssembly(ActorMessaging.Assembly));
```

## Disabilitare l'analizzatore/generatore di codice

È possibile disabilitare l'analisi e la generazione del codice attraverso degli attributi:

- `[assembly: DisableActorDiagnostics]`: disabilita la produzione della diagnostica; utilizzando questo attributo, eventuali errori di design dell'attore non saranno rilevati a compile-time, bensì verranno rilevati a startup-time e provocheranno un'eccezione di tipo `InvalidActorException`.
- `[assembly: DisableActorFactoryGeneration]`: disabilita la generazione delle factory degli attori; utilizzando questo attributo, le factory dovranno essere scritte a mano e marcate con l'attributo `[ActorFactory]` o `[ActorFactory<TActor>]`.

L'utilizzo di questi attributi è scoraggiato. Tuttavia, l'analizzatore potrebbe (in rari casi, per classi molto grandi) peggiorare l'esperienza di sviluppo, in quanto l'analisi è, in alcuni casi, eseguita ad ogni cambiamento del codice sorgente (anche l'inserimento di una lettera); tuttavia, l'analizzatore è ottimizzato per essere eseguito solo quando veramente serve e la situazione appena descritta non dovrebbe mai accadere. Se, comunque, si dovessero riscontrare problemi di questo tipo, è possibile utilizzare questi attributi, anche solo momentaneamente, per poi attivarli nel momento in cui non si prevede di modificare la struttura degli attori, per rilevare errori e generare le factory.

## Modellazione tramite YML

All'interno della sezione `actors` è possibile definire una lista di elementi che modellano gli attori. Ad esempio, il seguente yml definisce un attore chiamato `TrafficLight`.

```yml
actors:
    - name: TrafficLight
```

E ciò genererà la classe `TrafficLight` e la rispettiva interfaccia `ITrafficLight`. È possibile utilizzare la sezione `state` per definire tipi e componenti che faranno parte dello stato dell'attore. Ad esempio, il seguente yml definisce la classe `TrafficLightState`, con le proprietà viste negli esempi precedenti, e utilizza questa classe come componente dello stato dell'attore.

```yml
actors:
  - name: TrafficLight
    state:
      types:
        - name: TrafficLightState
          fields:
            - name: maxCarsBeforeYellow
              type: integer
              description: Indica il numero di auto che può passare con il verde prima che la luce diventi gialla
            - name: carsBeforeYellow
              type: integer
              description: Tiene traccia del numero di auto passate con il verde
            - name: turnsGreenAt
              type: datetime
              description: Memorizza l'orario in cui la luce ritorna verde
      components:
        - name: state
          type: TrafficLightState
          description: Lo stato dell'attore
```

Per indicare che un attore è virtuale, si utilizza la flag `isVirtual` (di default è `false`).

```yml
actors:
  - name: TrafficLight
    isVirtual: true
    state:
      types:
        - name: TrafficLightState
          fields:
            - name: maxCarsBeforeYellow
              type: integer
              description: Indica il numero di auto che può passare con il verde prima che la luce diventi gialla
            - name: carsBeforeYellow
              type: integer
              description: Tiene traccia del numero di auto passate con il verde
            - name: turnsGreenAt
              type: datetime
              description: Memorizza l'orario in cui la luce ritorna verde
      components:
        - name: state
          type: TrafficLightState
          description: Lo stato dell'attore
```

Utilizzando la sezione `implementations` si può indicare che un attore è polimorfico, specificando le sue implementazioni.

```yml
actors:
  - name: TrafficLight
    isVirtual: true
    state:
      types:
        - name: TrafficLightState
          fields:
            - name: maxCarsBeforeYellow
              type: integer
              description: Indica il numero di auto che può passare con il verde prima che la luce diventi gialla
            - name: carsBeforeYellow
              type: integer
              description: Tiene traccia del numero di auto passate con il verde
            - name: turnsGreenAt
              type: datetime
              description: Memorizza l'orario in cui la luce ritorna verde
      components:
        - name: state
          type: TrafficLightState
          description: Lo stato dell'attore
    implementations:
      - name: GreenTrafficLight
      - name: YellowTrafficLight
      - name: RedTrafficLight
      - name: OffTrafficLight
        isDefault: true
```

Per aggiungere il supporto al messaging, utilizzare la sezione `messaging`. Ad esempio, per specificare che l'attore riceve il messaggio `TurnOffCommand`, è necessario specificarlo nella lista dei messaggi (`messages`) dell'attore e definire la struttura dello stesso messaggio nella sezione `messaging` dello yml.

```yml
actors:
  - name: TrafficLight
    isVirtual: true
    state:
      types:
        - name: TrafficLightState
          fields:
            - name: maxCarsBeforeYellow
              type: integer
              description: Indica il numero di auto che può passare con il verde prima che la luce diventi gialla
            - name: carsBeforeYellow
              type: integer
              description: Tiene traccia del numero di auto passate con il verde
            - name: turnsGreenAt
              type: datetime
              description: Memorizza l'orario in cui la luce ritorna verde
      components:
        - name: state
          type: TrafficLightState
          description: Lo stato dell'attore
    implementations:
      - name: GreenTrafficLight
      - name: YellowTrafficLight
      - name: RedTrafficLight
      - name: OffTrafficLight
        isDefault: true
    messaging:
      messages:
        - TurnOffCommand
messaging:
  handlers: []
  messages:
    - name: TurnOffCommand
      description: Ordina di spegnere un semaforo
      fields:
        - name: id
          type: string
          description: L'id del semaforo
```

Per ultimo, attraverso la sezione `id` si può specificare il tipo di id dell'attore e/o un campo dell'attore che verrà valorizzato con il valore del proprio id.

```yml
actors:
  - name: TrafficLight
    isVirtual: true
    state:
      types:
        - name: TrafficLightState
          fields:
            - name: maxCarsBeforeYellow
              type: integer
              description: Indica il numero di auto che può passare con il verde prima che la luce diventi gialla
            - name: carsBeforeYellow
              type: integer
              description: Tiene traccia del numero di auto passate con il verde
            - name: turnsGreenAt
              type: datetime
              description: Memorizza l'orario in cui la luce ritorna verde
      components:
        - name: state
          type: TrafficLightState
          description: Lo stato dell'attore
    implementations:
      - name: GreenTrafficLight
      - name: YellowTrafficLight
      - name: RedTrafficLight
      - name: OffTrafficLight
        isDefault: true
    messaging:
      messages:
        - TurnOffCommand
    id:
      member: id
      type: uuid
messaging:
  handlers: []
  messages:
    - name: TurnOffCommand
      description: Ordina di spegnere un semaforo
      fields:
        - name: id
          type: string
          description: L'id del semaforo
```

## Possibili errori di configurazione

Di seguito, una lista di tutti i possibili errori possibili in fase di configurazione. Questi errori sono sia segnalati dall'analizzatore, se abilitato, che rilevati in fase di registrazione degli attori, a startup.

### Duplicate actor attribute

Utilizzo combinato degli attributi `[Actor]` e `[Actor<TInterface>]`.

```cs
[Actor, Actor<ITrafficLight>]
public class TrafficLight : ITrafficLight
{
    ...
}
```

Soluzione: utilizzare solo uno dei due attributi.

### Generic actors are not supported

Un'implementazione (o l'interfaccia) dell'attore è una classe (o interfaccia) generica.

```cs
[Actor]
public class TrafficLight<T> : ITrafficLight
{
    ...
}
```

Soluzione: rendere non-generico l'attore.

### Missing actor interface

L'attore non implementa un'interfaccia tramite la quale è possibile invocarlo.

```cs
[Actor]
public class TrafficLight
{
    ...
}
```

Soluzione: definire un'interfaccia che l'attore implementa.

### Ambiguous actor interface

L'attore implementa più di un'interfaccia (eccetto per quelle note, come `IMessageHandler`).

```cs
[Actor]
public class TrafficLight : ITrafficLight, IMyOtherInterface
{
    ...
}
```

Soluzione: indicare quale interfaccia utilizzare all'interno dell'attributo, ad esempio `[Actor(InterfaceType = typeof(ITrafficLight))]` o `[Actor<ITrafficLight>]`.

### Interface not implemented

Un'interfaccia è stata specificata all'interno dell'attributo, ma l'attore non la implementa.

```cs
[Actor<ITrafficLight>]
public class TrafficLight : IMyOtherInterface
{
    ...
}
```

Soluzione: implementare l'interfaccia indicata con l'attributo.

### Interface type is not an interface

Il tipo indicato come interfaccia dell'attore non è un'interfaccia.

```cs
[Actor<BaseTrafficLight>] // dove BaseTrafficLight è una classe
public class TrafficLight : ITrafficLight
{
    ...
}
```

Soluzione: indicare un'interfaccia anziché una classe.

### Properties are not supported

L'interfaccia dell'attore definisce una o più proprietà.

```cs
public interface ITrafficLight
{
    int MyProperty { get; }
}
```

Soluzione: Rimuovere le proprietà dall'interfaccia, in quanto non supportate.

### Events are not supported

L'interfaccia dell'attore definisce uno o più eventi.

```cs
public interface ITrafficLight
{
    event Action Event;
}
```

Soluzione: Rimuovere gli eventi dall'interfaccia, in quanto non supportati.

### Actor cannot be virtual

Un attore è dichiarato come virtuale, ma non è possibile determinare un valore dello stato di default.

```cs
[Actor, Virtual]
public class TrafficLight : ITrafficLight
{
    [State] private string _state;

    ...
}
```

Soluzione: indicare un valore di default per ciascuna componente dello stato che non definisce un costruttore senza parametri (ad esempio `[State(Default = "default-value")]`) o, se la componente dello stato è un oggetto composto, definire un costruttore senza parametri sulla sua classe.

### Duplicate implementation attribute

Utilizzo combinato degli attributi `[ActorImplementation]` e `[ActorImplementation<TActor>]`.

```cs
[ActorImplementation(typeof(TrafficLight)), ActorImplementation<TrafficLight>]
public class InactiveTrafficLight : TrafficLight
{
    ...
}
```

Soluzione: utilizzare solo uno dei due attributi.

### Multiple default implementations

Più di una implementazione è indicata come di default.

```cs
[ActorImplementation<TrafficLight>(IsDefault = true)]
public class GreenTrafficLight : TrafficLight
{
    ...
}

[ActorImplementation<TrafficLight>(IsDefault = true)]
public class RedTrafficLight : TrafficLight
{
    ...
}
```

Soluzione: Indicare solo una implementazione di default.

### Actor not inherited

L'implementazione non estende (direttamente o indirettamente) la classe indicata nel proprio attributo.

```cs
[ActorImplementation<TrafficLight>]
public class GreenTrafficLight : ITrafficLight
{
    ...
}
```

Soluzione: Estendere la classe indicata nell'attributo.

### Abstract implementation

L'implementazione di un attore è una classe astratta.

```cs
[ActorImplementation<TrafficLight>]
public abstract class GreenTrafficLight : TrafficLight
{
    ...
}
```

Soluzione: rendere concreta l'implementazione.

### Invalid state type

Una componente dello stato ha un tipo che non può essere utilizzato come stato (come un'interfaccia).

```cs
[Actor]
public class TrafficLight : ITrafficLight
{
    [State] private IDisposable _state;
}
```

Soluzione: utilizzare un tipo primitivo, una classe POCO o una lista o dizionario.

### Invalid default value

Il valore di default indicato per una componente dello stato non può essere assegnato al membro.

```cs
[Actor]
public class TrafficLight : ITrafficLight
{
    [State(Default = 1)] private string _state;
}
```

Soluzione: specificare un valore di default avente tipo corretto.

### State must be defined in base actor

Una componente dello stato non è definita nella classe base dell'attore.

```cs
[ActorImplementation<TrafficLight>]
public class GreenTrafficLight : TrafficLight
{
    [State] private string _state;
}
```

Soluzione: definire tutte le componenti dello stato all'interno della classe base.

### Ambiguous actor id source

Più di un membro è marcato con l'attributo `[ActorId]`.

```cs
[Actor]
public class TrafficLight : ITrafficLight
{
    [ActorId] private string _id1;
    [ActorId] private int _id2;
}
```

Soluzione: marcare un solo membro con l'attributo `[ActorId]`.

### Invalid id type

Un tipo utilizzato come id non definisce il metodo `Parse(string)` o `Parse(string, IFormatProvider)`, avente come tipo di ritorno il tipo stesso.

```cs
[Actor, ActorIdType<(int, string)>]
public class TrafficLight : ITrafficLight
{
}
```

Soluzione: utilizzare un tipo che definisce uno dei due metodi.

### Multiple id source interfaces

Un tipo implementa l'intefaccia `IActorIdSource<TActorId>` più di una volta.

```cs
public class TrafficLightState : IActorIdSource<string>, IActorIdSource<int>
{
    string IActorIdSource<string>.GetActorId() { ... }
    void IActorIdSource<string>.SetActorId(string actorId) { ... }

    int IActorIdSource<int>.GetActorId() { ... }
    void IActorIdSource<int>.SetActorId(int actorId) { ... }
}
```

Soluzione: implementare l'interfaccia una sola volta.

### Duplicate actor id type attribute

Utilizzo combinato degli attributi `[ActorIdType]` e `[ActorIdType<TActorId>]`.

```cs
[Actor, ActorIdType(typeof(int)), ActorIdType<int>]
public class TrafficLight : ITrafficLight
{
    ...
}
```

Soluzione: utilizzare solo uno dei due attributi.

### State component name mismatch

Non è possibile determinare i parametri del costruttore corrispondenti a ciascuna componente dello stato.

```cs
[Actor]
public class TrafficLight : ITrafficLight
{
    [State] private string _myState;

    public TrafficLight(string state)
    {
        _myState = state;
    }
}
```

Soluzione: rinominare i parametri in modo tale da poter risolvere la rispettiva componente dello stato tramite convenzione.

### Ambiguous actor constructor

Un attore definisce più costruttori e nessuno di essi è marcato con l'attributo `[ActorConstructor]`, oppure più di un costruttore è marcato con tale attributo.

```cs
[Actor]
public class TrafficLight : ITrafficLight
{
    [State] private string _myState;

    public TrafficLight(string myState)
    {
        _myState = state;
    }

    public TrafficLight()
    {
        _myState = "";
    }
}
```

Soluzione: decorare un solo costruttore con l'attributo `[ActorConstructor]`.

### Wrong generic actor context

Un parametro del costruttore è di tipo `IActorContext<TActor>` ma `TActor` non corrisponde all'attore in cui è utilizzato.

```cs
[Actor]
public class TrafficLight : ITrafficLight
{
    public TrafficLight(IActorContext<OtherActor> context)
    {
        ...
    }
}
```

Soluzione: utilizzare il tipo di context corretto.

### Generic methods are not supported

Un metodo di interfaccia è generico.

```cs
public interface ITrafficLight
{
    Task MyMethod<T>();
}
```

Soluzione: utilizzare metodi di interfaccia non generici.

### Invalid method return type

Un metodo di interfaccia non ritorna `Task`, `Task<T>`, `ValueTask` o `ValueTask<T>`.

```cs
public interface ITrafficLight
{
    void MyMethod();
}
```

Soluzione: utilizzare i tipi di ritorno supportati.

### Cancellation token must be last parameter

Un metodo definisce un parametro di tipo `CancellationToken` che non compare per ultimo nella firma del metodo.

```cs
public interface ITrafficLight
{
    void MyMethod(CancellationToken cancellationToken, int arg);
}
```

Soluzione: spostare il parametro di tipo `CancellationToken` in modo che sia l'ultimo.

### Duplicate actor factory attribute

Utilizzo combinato degli attributi `[ActorFactory]` e `[ActorFactory<TActor>]`.

```cs
[ActorFactory(typeof(TrafficLight)), ActorFactory<TrafficLight>]
public interface ITrafficLightFactory
{
    ITrafficLight Get(Guid id);
}
```

Soluzione: utilizzare solo uno dei due attributi.

### Generic factories are not supported

La factory di un attore è un'interfaccia generica.

```cs
[ActorFactory<TrafficLight>]
public interface ITrafficLightFactory<T>
{
    ITrafficLight Get(Guid id);
}
```

Soluzione: rendere non-generica l'interfaccia.

### Missing actor factory type

Non è possibile determinare un'interfaccia che sia la factory di un attore.

Ciò può accadere quando l'actor è configurato tramite fluent API e non è marcato con l'attributo `[Actor]`, oppure è stata disabilitata la generazione delle factory.

Soluzione: ripristinare la generazione della factory o definire a mano l'interfaccia dell'attore.

### Invalid actor factory type

L'interfaccia di una factory non definisce i metodi corretti.

```cs
[ActorFactory<TrafficLight>]
public interface ITrafficLightFactory
{
    ITrafficLight Get(Guid id, string otherArg);
}
```

Soluzione: definire i metodi `Get` e `CreateAsync` (solo `Get` per attori virtuali) con le firme corrette.

### Ambiguous factory type

Più di un'interfaccia è marcata come factory di un attore.

```cs
[ActorFactory<TrafficLight>]
public interface ITrafficLightFactory1
{
    ITrafficLight Get(Guid id);
}

[ActorFactory<TrafficLight>]
public interface ITrafficLightFactory2
{
    ITrafficLight Get(Guid id);
}
```

Soluzione: definire una sola factory per attore.

### Invalid actor message

Il tipo di un messaggio a cui l'attore è sottoscritto non implementa l'interfaccia `IActorMessage<TActorId>` o `TActorId` non corrisponde con il tipo di id utilizzato dall'attore.

```cs
[Actor, ActorIdType<Guid>]
public class TrafficLight : ITrafficLight, IMessageHandle<MyActorMessage>
{
    ...
}

[Message]
public class MyActorMessage : IActorMessage<string>
{
    ...
}
```

Soluzione: utilizzare messaggi che implementano un'interfaccia `IActorMessage<TActorId>` compatibile con il tipo di id utilizzato.
