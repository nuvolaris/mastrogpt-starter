# State management with Dapr

Dapr offers a simple API for persisting state, on which we built an even simpler and intuitive wrapper that implements the `IStateStore` interface.

## Dapr configuration : State

The `State` section of the configuration file will be used for configuring the messaging infrastructure.

Currently, this section only contains the `DefaultStore` property that can be used to configure the name of the default state store the application will use.

```json
{
    "State": {
        "DefaultStore": "statestore"
    }
}
```

If you specify a default store, consumers will use that name by default, if no store name is specified.

## Dapr configuration : Dependency Injection

Normally, you will use Dependency Injection to access the state store in your consumer classes. If a default store is configured, you can request an `IStateStore` instance into the class' constructor.

```c#
public class StatefulClass
{
    private readonly IStateStore _store;

    public StatefulClass(IStateStore store)
    {
        _store = store;
    }
}
```

However, Dapr lets you use multiple state stores at the same time in your application, which are identified by a name. You can manually resolve a specific message store by name, using the `IServiceResolver` generic interface.

```c#
public class StatefulClass
{
    private readonly IStateStore _store;

    public StatefulClass(IServiceResolver<IStateStore> storeResolver)
    {
        _store = storeResolver.Resolve("storeName");
    }
}
```

## Dapr configuration:  In Startup.cs

To start configuring the Dapr infrastructure, call the `AddDaprInfrastructure` extension method on your `IServiceCollection` instance. There are two overload of this method. The first one takes an optional `DaprConfiguration` argument, which contains the configuration instance to use; we recommend using that for prototyping and testing purposes only. For production, we recommend using the overload that takes a building action, which allows to fluently add configuration options from your `IConfiguration` instance and from other sources.

To enable the use of the state stores, chain a `AddStateStore` call to the infrastructure configuration method. This will inject an `IServiceResolver<IStateStore>` as a singleton service. Instances of `IStateStore` are lazily created when needed and available as singletons. Furthermore, if a default store is configured, a default `IStateStore` will be added to the services: this is expecially useful when only a single store is used in the architecture.

An example of what discussed is shown below.

```c#
services.AddDaprInfrastructure(cfg => cfg.AddServiceOptions(Configuration))
    .AddStateStore();
```
