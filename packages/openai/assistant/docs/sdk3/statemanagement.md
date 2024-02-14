# State management

State management is a feature that enables you to write stateful services and, in some cases, replace the database. You can easily store state using the `IStateStore` service. This interface provides a simple API for storing key-value pairs. The keys are of `string` type, while the stored values can be of any type.

## Saving the state

You can persist a state object by using the `SaveAsync` method. It accepts a key with which you will be able to retrieve the state later, the state object and, like all asynchronous methods on this API, an optional `CancellationToken` that can be used to cancel the operation.

```c#
public class MyState
{
    public string String { get; set; }
    public int Number { get; set; }
}

public class StatefulClass
{
    private readonly IStateStore _store;

    public async Task DoSomethingAndSaveStateAsync(string message)
    {
        // Some business logic
        MyState state = new MyState { String = "string", Number = 0 };
        await _store.SaveAsync("key", state);
        // Other business logic
    }
}
```

## Retrieving the state

To get back a persisted state, use the `GetAsync` method, providing a key value which you saved the state with.

```c#
public class StatefulClass
{
    private readonly IStateStore _store;

    public async Task DoSomethingWithTheStateAsync(string message)
    {
        MyState state = await _store.GetAsync<MyState>("key");
        // Do something with the state
    }
}
```

## Deleting the state

Deleting the persisted state is as simple as calling the `DeleteAsync` method.

```c#
public class StatefulClass
{
    private readonly IStateStore _store;

    public async Task CleanUpTheStateAsync(string message)
    {
        await _store.DeleteAsync("key");
        // Do something else
    }
}
```

## Implementations

The state management interface is defined in the `CodeArchitects.Infrastructure` namespace, while its implementations can be found in more specific namespaces, i.e., `CodeArchitects.Infrastructure.Dapr`. Each implementation has its own feature and is configured differently, so be sure to read the documentation for your implementation of choice as well.

Available implementations are listed below:

- [State management with Dapr](statemanagement-dapr.md)
