# Messaging

Con la sezione `messaging` è possibile generare messaggi e handlers. Un handler è l'entry point che riceve i messaggi cui il microservizio è in ascolto e che altri microservizi inviano sulla coda. Un handler può gestire più messaggi ed avere 0, 1 o più tipi di ritorno.

## Handlers senza tipo di ritorno

Questi handlers gestiscono i messaggi senza produrre alcun valore di ritorno: ricevono il messaggio ed eseguono una certa logica. Un esempio potrebbe essere un handler che stampa su console una certa stringa.

```yml
messaging:
  handlers:
    - name: ConsoleHandler
      description: Handler of OutputToConsoleCommand
      messages:
        - OutputToConsoleCommand
  messages:
    - name: OutputToConsoleCommand
      description: Asks to print a message to the console
      fields:
        - name: id
          description: The message id
          type: uuid
        - name: text
          description: The text to print to the console
          type: string
```

La precedente sezione genererà:

- Un comando che chiede di stampare un testo su console
- Un handler che riceverà tale comando

```cs
/// <summary>
/// Asks to print a message to the console
/// </summary>
/// <param name="Id">The message id</param>
/// <param name="Text">The text to print to the console</param>
public record OutputToConsoleCommand(Guid Id, string Text);

/// <summary>
/// Handler of OutputToConsoleCommand
/// </summary>
public class ConsoleHandler : IMessageHandler<OutputToConsoleCommand>
{

}
```

Il compilatore obbligherà ad implementare il metodo `HandleAsync` per ciascuna interfaccia implementata. Di seguito, una possibile implementazione.

```cs
/// <summary>
/// Handler of OutputToConsoleCommand
/// </summary>
public class ConsoleHandler : IMessageHandler<OutputToConsoleCommand>
{
    public Task HandleAsync(OutputToConsoleCommand message, CancellationToken cancellationToken)
    {
        Console.WriteLine(message.Text);
        return Task.CompletedTask;
    }
}
```

## Handlers con uno o più tipi di ritorno

Questi handlers gestiscono i messaggi producendo un valore di ritorno che potrà essere posto in binding con diverse azioni (vedere sezione [Bindings](#bindings)).

```yml
messaging:
  handlers:
    - name: MathHandler
      description: Handler of MultiplyNumbersCommand and DivideNumbersCommand
      messages:
        - name: MultiplyNumbersCommand
          result: NumbersMultipliedEvent
        - name: DivideNumbersCommand
          result:
            - NumbersDividedEvent
            - DivisionByZeroEvent
  messages:
    - name: MultiplyNumbersCommand
      description: Asks to compute the product of two numbers
      fields:
        - name: id
          description: The message id
          type: uuid
        - name: firstFactor
          description: The first factor
          type: numeric
        - name: secondFactor
          description: The second factor
          type: numeric
    - name: NumbersMultipliedEvent
      description: Signals that two numbers were multiplied
      fields:
        - name: id
          description: The message id
          type: uuid
        - name: product
          description: The product of the numbers
          type: numeric
    - name: DivideNumbersCommand
      description: Asks to compute the quotient of two numbers
      fields:
        - name: id
          description: The message id
          type: uuid
        - name: numerator
          description: The numerator
          type: numeric
        - name: denominator
          description: The denominator
          type: numeric
    - name: NumbersDividedEvent
      description: Signals that two numbers were divided successfully
      fields:
        - name: id
          description: The message id
          type: uuid
        - name: quotient
          description: The quotient of the numbers
          type: numeric
    - name: DivisionByZeroEvent
      description: Signals that there was an attempt to divide by 0
      fields:
        - name: id
          description: The message id
          type: uuid
```

La precedente sezione genererà:

- Un comando che chiede di moltiplicare due numeri
- Un evento che comunica la moltiplicazione di due numeri
- Un comando che chiede di dividere due numeri
- Un evento che comunica la divisione di due numeri
- Un evento che comunica una divisione per 0
- Un handler che gestisce entrambi i comandi e produce i rispettivi eventi

```cs
/// <summary>
/// Asks to compute the product of two numbers
/// </summary>
/// <param name="Id">The message id</param>
/// <param name="FirstFactor">The first factor</param>
/// <param name="SecondFactor">The second factor</param>
public record MultiplyNumbersCommand(Guid Id, double FirstFactor, double SecondFactor);

/// <summary>
/// Signals that two numbers were multiplied
/// </summary>
/// <param name="Id">The message id</param>
/// <param name="Product">The product of the numbers</param>
public record NumbersMultipliedEvent(Guid Id, double Product);

/// <summary>
/// Asks to compute the quotient of two numbers
/// </summary>
/// <param name="Id">The message id</param>
/// <param name="Numerator">The numerator</param>
/// <param name="Denominator">The denominator</param>
public record DivideNumbersCommand(Guid Id, double Numerator, double Denominator);

/// <summary>
/// Signals that two numbers were divided successfully
/// </summary>
/// <param name="Id">The message id</param>
/// <param name="Quotient">The quotient of the numbers</param>
public record NumbersDividedEvent(Guid Id, double Quotient);

/// <summary>
/// Signals that there was an attempt to divide by 0
/// </summary>
/// <param name="Id">The message id</param>
public record DivisionByZeroEvent(Guid Id);

/// <summary>
/// Handler of OutputToConsoleCommand
/// </summary>
public class MathHandler : IMessageHandler<MultiplyNumbersCommand, NumbersMultipliedEvent>, IMessageHandler<DivideNumbersCommand, OneOf<NumbersDividedEvent, DivisionByZeroEvent>>
{

}
```

Di seguito, una possibile implementazione.

```cs
/// <summary>
/// Handler of MultiplyNumbersCommand and DivideNumbersCommand
/// </summary>
public class MathHandler : IMessageHandler<MultiplyNumbersCommand, NumbersMultipliedEvent>, IMessageHandler<DivideNumbersCommand, OneOf<NumbersDividedEvent, DivisionByZeroEvent>>
{
    public async Task<NumbersMultipliedEvent> HandleAsync(MultiplyNumbersCommand message, CancellationToken cancellationToken)
    {
        await Task.Delay(1000);
        double product = message.FirstFactor * message.SecondFactor;
        return new NumbersMultipliedEvent(message.Id, product);
    }

    public async Task<OneOf<NumbersDividedEvent, DivisionByZeroEvent>> HandleAsync(DivideNumbersCommand message, CancellationToken cancellationToken)
    {
        await Task.Delay(1000);
        if (message.Denominator == 0.0)
        {
            return new DivisionByZeroEvent(message.Id);
        }

        double quotient = message.Numerator / message.Denominator;
        return new NumbersDividedEvent(message.Id, quotient);
    }
}
```

## Dependency injection

Per aggiungere il supporto al messaging, utilizzare il metodo di estensione `AddMessaging` di `IDaprInfrastructureBuilder`:

```cs
services.AddDaprInfrastructure(options => options.SetConfiguration(Configuration))
    .AddMessaging();
```

Di base, nessun handler verrà registrato tramite reflection. Per fare ciò, esistono diversi metodi:

- `AddHandler(Type handlerType)` o `AddHandler<THandler>()`: registra uno specifico handler
- `ScanAssembly(Assembly assembly)`: registra tutti gli handler marcati con l'attributo `[MessageHandler]` nel dato assembly
- `ScanAssemblyOfType<T>()`: registra tutti gli handler marcati con l'attributo `[MessageHandler]` nell'assembly del dato tipo

Ad esempio:

```cs
services.AddDaprInfrastructure(options => options.SetConfiguration(Configuration))
    .AddMessaging(messaging => messaging.ScanAssemblyOfType<Startup>());
```

E ciò tenterà di registrare tutti gli handlers contenuti nell'assembly della classe `Startup`, a patto che siano ben configurati tramite attributi (vedere sezione [Input binding](#input-binding)).

Per esporre gli handlers sugli endpoint dedicati alla ricezione dei messaggi, utilizzare il metodo di estensione `MapMessageHandlers` di `IEndpointRouteBuilder`:

```cs
endpoints.MapMessageHandlers();
```

## Bindings

Per rendere effettivi gli handlers, bisogna legarli in ingresso ad un message bus ed ad un topic (input binding). Gli handlers che producono un valore di ritorno possono essere legati ad una o più azioni che reagiscono al valore prodotto (output binding). Esistono due modi di specificare queste caratteristiche: tramite reflection e tramite configurazione; di seguito viene spiegato come farlo tramite reflection, mentre la configurazione verrà documentata nella sezione [Configurazione](#configurazione).

### Input binding

Per registrare uno o più handler tramite reflection, aggiungere l'attributo `[MessageHandler]` sulla classe:

```cs
/// <summary>
/// Handler of MultiplyNumbersCommand and DivideNumbersCommand
/// </summary>
[MessageHandler]
public class MathHandler : IMessageHandler<MultiplyNumbersCommand, NumbersMultipliedEvent>, IMessageHandler<DivideNumbersCommand, OneOf<NumbersDividedEvent, DivisionByZeroEvent>>
{
    public async Task<NumbersMultipliedEvent> HandleAsync(MultiplyNumbersCommand message, CancellationToken cancellationToken)
    {
        ...
    }

    public async Task<OneOf<NumbersDividedEvent, DivisionByZeroEvent>> HandleAsync(DivideNumbersCommand message, CancellationToken cancellationToken)
    {
        ...
    }
}
```

Con questo attributo, è possibile specificare il nome del bus e del topic a cui legare questo handler; ad esempio, per legare l'handler al bus `messagebus` e al topic `math`, si scrive:

```cs
[MessageHandler("messagebus", "mathtopic")]
```

Se non viene specificato il topic, verrà utilizzato il topic di default (`__global`). Se non viene specificato il message bus, verrà utilizzato quello di default, se è stato impostato un bus di default in configurazione; in caso contrario, verrà sollevato un warning e l'handler non sarà attivo.

Inoltre, è possibile utilizzare lo stesso attributo nella stessa maniera sui vari metodi per effettuare l'override dei dati impostati nell'attributo della classe. Di seguito, un esempio:

```cs
/// <summary>
/// Handler of MultiplyNumbersCommand and DivideNumbersCommand
/// </summary>
[MessageHandler("messagebus")]
public class MathHandler : IMessageHandler<MultiplyNumbersCommand, NumbersMultipliedEvent>, IMessageHandler<DivideNumbersCommand, OneOf<NumbersDividedEvent, DivisionByZeroEvent>>
{
    [MessageHandler(Topic = "multiply")]
    public async Task<NumbersMultipliedEvent> HandleAsync(MultiplyNumbersCommand message, CancellationToken cancellationToken)
    {
        ...
    }

    [MessageHandler(Topic = "divide")]
    public async Task<OneOf<NumbersDividedEvent, DivisionByZeroEvent>> HandleAsync(DivideNumbersCommand message, CancellationToken cancellationToken)
    {
        ...
    }
}
```

### Output binding

Un output binding è un'azione che reagisce al valore di ritorno del metodo legato ad esso e permette di essere configurata in maniera aspect-oriented. Ad esempio, il binding `MessageBus` pubblica il valore di ritorno sul dato topic del dato bus. È possibile dichiarare gli output binding di un metodo attraverso il corrispondente attributo sul valore di ritorno del metodo:

```cs
/// <summary>
/// Handler of MultiplyNumbersCommand and DivideNumbersCommand
/// </summary>
[MessageHandler("messagebus")]
public class MathHandler : IMessageHandler<MultiplyNumbersCommand, NumbersMultipliedEvent>, IMessageHandler<DivideNumbersCommand, OneOf<NumbersDividedEvent, DivisionByZeroEvent>>
{
    [MessageHandler(Topic = "multiply")]
    [return: MessageBus("messagebus", "multiply-ok")]
    public async Task<NumbersMultipliedEvent> HandleAsync(MultiplyNumbersCommand message, CancellationToken cancellationToken)
    {
        ...
    }

    [MessageHandler(Topic = "divide")]
    [return: MessageBus("messagebus", "divide-ok", typeof(NumbersDividedEvent))]
    [return: MessageBus("messagebus", "divide-ko", typeof(DivisionByZeroEvent))]
    public async Task<OneOf<NumbersDividedEvent, DivisionByZeroEvent>> HandleAsync(DivideNumbersCommand message, CancellationToken cancellationToken)
    {
        ...
    }
}
```

Al momento, gli output binding supportati sono `MessageBus` e `StateStore`, dove quest'ultimo salva in un dato state store il valore di ritorno. Entrambi supportano il filtro per tipo di ritorno (vedere sezione [Output binding personalizzati](#output-binding-personalizzati)).

### Output binding personalizzati

È anche possibile creare degli output binding personalizzati, in modo da poter riutilizzare la stessa logica su diversi handler. Nel seguente esempio, verrà implementato un binding che effettua il log dei un messaggio utilizzando il valore di ritorno prodotto dall'handler come parametro.

Per prima cosa, è necessario definire un'interfaccia che definisca il binding e che contenga i metadati del binding (ad esempio, i metadati del binding `MessageBus` sono il nome del bus e nome del topic). L'interfaccia deve implementare `IOutputMetadata`:

```cs
using CodeArchitects.Platform.Messaging.Bindings;
using Microsoft.Extensions.Logging;

namespace Example
{
    public interface ILogOutputMetadata : IOutputMetadata
    {
        LogLevel LogLevel { get; }
        string Template { get; }
    }
}
```

Una volta dichiarata questa interfaccia, definire la logica in una classe che deve implementare l'interfaccia `IOutputBinding<TMetadata>` ed il suo metodo `ExecuteAsync`. In suddetta classe, è possibile utilizzare la dependency injection.

```cs
using CodeArchitects.Platform.Messaging.Bindings;
using Microsoft.Extensions.Logging;
using System.Text.Json;

namespace Example
{
    public class LogOutputBinding : IOutputBinding<ILogOutputMetadata>
    {
        private readonly ILogger<LogOutputBinding> _logger;

        public LogOutputBinding(ILogger<LogOutputBinding> logger)
        {
            _logger = logger;
        }

        public Task ExecuteAsync<TMessage, TResult>(OutputBindingContext<ILogOutputMetadata, TMessage, TResult> context, CancellationToken cancellationToken)
        {
            _logger.Log(context.Metadata.LogLevel, context.Metadata.Template, JsonSerializer.Serialize(context.Result));
            return Task.CompletedTask;
        }
    }
}
```

A questo punto, il binding va registrato. Ciò può essere fatto in due modi.

Si può utilizzare il metodo `RegisterOutputBinding` di `IDaprMessagingOptionsBuilder`, indicando il lifetime del servizio:

```cs
services.AddDaprInfrastructure(options => options.SetConfiguration(Configuration))
    .AddMessaging(messaging => messaging
        .ScanAssemblyOfType<Startup>()
        .AddOutputBinding<LogOutputBinding>(ServiceLifetime.Singleton));
```

Oppure, si può registrare come un normale servizio nel container di dependency injection, attraverso l'interfaccia che la classe implementa:

```cs
services.AddSingleton<IOutputBinding<ILogOutputMetadata>, LogOutputBinding>();
```

Si può definire un alias per il binding, che potrà essere utilizzato per riferirsi al binding in configurazione (vedere sezione [Configurazione](#configurazione)).

```cs
services.AddDaprInfrastructure(options => options.SetConfiguration(Configuration))
    .AddMessaging(messaging => messaging
        .ScanAssemblyOfType<Startup>()
        .AddOutputBinding<LogOutputBinding>(ServiceLifetime.Singleton)
        .RegisterOutputMetadataAlias<ILogOutputMetadata>("Log"));
```

Per utilizzare il binding tramite reflection, dichiarare un attributo per i valori di ritorno che implementa l'interfaccia precedentemente definita:

```cs
using System;
using Microsoft.Extensions.Logging;

namespace Example
{
    [AttributeUsage(AttributeTargets.ReturnValue)]
    public class LogAttribute : Attribute, ILogOutputMetadata
    {
        public LogAttribute(LogLevel logLevel, string template)
        {
            LogLevel = logLevel;
            Template = template;
        }

        public LogLevel LogLevel { get; }

        public string Template { get; }
    }
}
```

Una volta fatto questo, si può usare come mostrato precedentemente:

```cs
/// <summary>
/// Handler of MultiplyNumbersCommand and DivideNumbersCommand
/// </summary>
[MessageHandler("messagebus")]
public class MathHandler : IMessageHandler<MultiplyNumbersCommand, NumbersMultipliedEvent>, IMessageHandler<DivideNumbersCommand, OneOf<NumbersDividedEvent, DivisionByZeroEvent>>
{
    [MessageHandler(Topic = "multiply")]
    [return: Log(LogLevel.Information, "The handler returned {result}")]
    public async Task<NumbersMultipliedEvent> HandleAsync(MultiplyNumbersCommand message, CancellationToken cancellationToken)
    {
        ...
    }
}
```

È possibile anche abilitare il binding solo per alcuni tipi di ritorno; in questo caso, l'interfaccia deve implementare `ITypedOutputMetadata` anziché `IOutputMetadata`.

```cs
using CodeArchitects.Platform.Messaging.Bindings;
using Microsoft.Extensions.Logging;

namespace Example
{
    public interface ILogOutputMetadata : ITypedOutputMetadata
    {
        LogLevel LogLevel { get; }
        string Template { get; }
    }
}
```

L'interfaccia `ITypedOutputMetadata` contiene un'unica proprietà di tipo `Type[]` chiamata `AllowedTypes` che contiene i tipi per cui il binding verrà eseguito. Ciò significa che è necessario modificare l'attributo includendo questa proprietà, ad esempio:

```cs
using System;
using Microsoft.Extensions.Logging;

namespace Example
{
    [AttributeUsage(AttributeTargets.ReturnValue, AllowMultiple = true)]
    public class LogAttribute : Attribute, ILogOutputMetadata
    {
        public LogAttribute(LogLevel logLevel, string template, params Type[] allowedTypes)
        {
            LogLevel = logLevel;
            Template = template;
            AllowedTypes = allowedTypes;
        }

        public LogLevel LogLevel { get; }

        public string Template { get; }

        public Type[] AllowedTypes { get; }
    }
}
```

Notare come sia stato aggiunto anche `AllowMultiple = true`. Un esempio di utilizzo è il seguente:

```cs
/// <summary>
/// Handler of MultiplyNumbersCommand and DivideNumbersCommand
/// </summary>
[MessageHandler("messagebus")]
public class MathHandler : IMessageHandler<MultiplyNumbersCommand, NumbersMultipliedEvent>, IMessageHandler<DivideNumbersCommand, OneOf<NumbersDividedEvent, DivisionByZeroEvent>>
{
    [MessageHandler(Topic = "divide")]
    [return: Log(LogLevel.Information, "Handler returned {result}", typeof(NumbersDividedEvent))]
    [return: Log(LogLevel.Warning, "Attempted to divide by 0", typeof(DivisionByZeroEvent))]
    public async Task<OneOf<NumbersDividedEvent, DivisionByZeroEvent>> HandleAsync(DivideNumbersCommand message, CancellationToken cancellationToken)
    {
        ...
    }
}
```

## Configurazione

Gli attributi non sono l'unico modo per configurare gli handler. Si possono ottenere gli stessi risultati tramite la configurazione dell'applicazione. La sezione della configurazione predefinita per il messaging è "Caep:Dapr:Messaging".

### MessagingConfig

```json
{
  "DefaultBus": ...,
  "Handlers": {...}
}
```

**DefaultBus** (`string`, optional): Il nome del bus da usare quando non diversamente specificato.
  
**Handlers** (`map`<`string`, `HandlerClassBindingConfig`>): Sezione usata per registrare gli handler tramite configurazione. La chiave è il fully-qualified name del tipo dell'handler.

### HandlerClassBindingConfig

```json
{
  "Bus": ...,
  "Topic": ...,
  "Methods": [...]
}
```

**Bus** (`string`, optional): Il nome del bus da usare quando non specificato nei singoli metodi. Ripiega sulla proprietà "DefaultBus" dell'oggetto *MessagingConfig* quando non specificato.
  
**Topic** (`string`, optional): Il nome del topic da usare quando non specificato nei singoli metodi.
  
**Methods** (`list`<`HandlerBindingConfig`>, optional): Usato per registrare i singoli metodi come handler.

### HandlerBindingConfig

```json
{
  "Bus": ...,
  "Topic": ...,
  "MessageType": ...,
  "ResultType": ...,
  "ResultTypes": [...],
  "Output": [...]
}
```

**Bus** (`string`, optional): Il nome del bus a cui il metodo dell'handler è sottoscritto. Ripiega sulla proprietà "Bus" dell'oggetto *HandlerClassBindingConfig* quando non specificato.
  
**Topic** (`string`, optional): Il nome del topic a cui il metodo dell'handler è sottoscritto. Ripiega sulla proprietà "Topic" dell'oggetto *HandlerClassBindingConfig* quando non specificato.
  
**MessageType** (`string`, required): Il fully-qualified name del tipo di messaggio che questo metodo riceve.
  
**ResultType** (`string`, optional): Il fully-qualified name del tipo di ritorno che questo metodo produce. Prioritario rispetto a *ResultTypes*.
  
**ResultTypes** (`list`<`string`>, optional): La lista dei fully-qualified name dei tipi di ritorno che questo metodo produce.
  
**Output** (`list`<`OutputBindingConfig`>, optional): La lista degli output binding.

### OutputBindingConfig

```json
{
  "Name": ...,
  "Metadata": {...}
}
```

**Name** (`string`, required):  Il fully-qualified name del tipo di metadati del binding, o il suo alias.
  
**Metadata**: (`map`<`string`, `any`>): I metadati del binding.

### Esempio

Di seguito è riportata una configurazione che produce una registrazione degli handler equivalente a quanto visto precedentemente tramite attributi.

```json
{
    "Caep": {
        "Dapr": {
            "Messaging": {
                "DefaultBus": "messagebus",
                "Handlers": {
                    "Application.Infrastructure.Handlers.MathHandler, Application": {
                        "Methods": [
                            {
                                "Topic": "multiply",
                                "MessageType": "Application.Domain.Messaging.MultiplyNumbersCommand, Application",
                                "ResultType": "Application.Domain.Messaging.NumbersMultipliedEvent, Application",
                                "Output": [
                                    {
                                        "Name": "$MessageBus", // alias per 'CodeArchitects.Platform.Messaging.Dapr.Bindings.IMessageBusOutputMetadata, CodeArchitects.Platform.Messaging.Dapr'
                                        "Metadata": {
                                            "Topic": "multiply-ok" // "Bus" non è specificato, verrà utilizzato "DefaultBus"
                                        }
                                    },
                                    {
                                        "Name": "Example.ILogOutputMetadata, Example",
                                        "Metadata": {
                                            "LogLevel": "Information",
                                            "Template": "The handler returned {result}"
                                        }
                                    }
                                ]
                            },
                            {
                                "Topic": "divide",
                                "MessageType": "Application.Domain.Messaging.DivideNumbersCommand, Application",
                                "ResultTypes": [
                                    "Application.Domain.Messaging.NumbersDividedEvent, Application",
                                    "Application.Domain.Messaging.DivisionByZeroEvent, Application",
                                ],
                                "Output": [
                                    {
                                        "Name": "$MessageBus",
                                        "Metadata": {
                                            "Topic": "divide-ok",
                                            "AllowedTypes": [
                                                "Application.Domain.Messaging.NumbersDividedEvent, Application"
                                            ]
                                        }
                                    },
                                    {
                                        "Name": "$MessageBus",
                                        "Metadata": {
                                            "Topic": "divide-ko",
                                            "AllowedTypes": [
                                                "Application.Domain.Messaging.DivisionByZeroEvent, Application"
                                            ]
                                        }
                                    },
                                    {
                                        "Name": "$Log", // Alias per 'Example.ILogOutputMetadata, Example'
                                        "Metadata": {
                                            "LogLevel": "Information",
                                            "Template": "The handler returned {result}",
                                            "AllowedTypes": [
                                                "Application.Domain.Messaging.NumbersDividedEvent, Application"
                                            ]
                                        }
                                    },
                                    {
                                        "Name": "$Log",
                                        "Metadata": {
                                            "LogLevel": "Warning",
                                            "Template": "Attempted to divide by 0",
                                            "AllowedTypes": [
                                                "Application.Domain.Messaging.DivisionByZeroEvent, Application"
                                            ]
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
    }
}
```
