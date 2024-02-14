# Operation Bindings

In operations, you can define parameters and specify their binding type in the YAML configuration. Operation bindings allow you to control how parameters are passed to and from API methods. Here are the different parameter binding types you can use:

### `fromQuery` Binding

In operations with a type of `http_post` (or other types that involve a request body), you can use the `fromQuery` binding to specify parameters external to the envelope that should be added as query parameters. Here's an example:

```yml
- name: saveCustomer
  type: http_post
  description: Save customer
  parameters:
    - name: meccanografico
      description: Meccanografico
      direction: in
      type: string
      binding: fromQuery
    - name: customer
      description: Customer to be saved
      direction: inout
      type: Customer
    - name: success
      description: Operation result
      direction: out
      type: boolean
```

This configuration generates a method signature like this:

```cs
public async Task<ActionResult<SaveCustomerResponse>> SaveCustomer(SaveCustomerRequest request, [FromQuery] string meccanografico, CancellationToken requestAborted)
{...}
```

### `fromHeader` Binding

Parameters with the fromHeader binding type are added directly to the request header and are made available to the specific API method using the [FromHeader] attribute. Here's an example:

```yml
- name: saveCustomer
  type: http_post
  description: Save customer
  parameters:
    - name: meccanografico
      description: Meccanografico
      direction: in
      type: string
      binding: fromQuery
    - name: mode
      type: string
      description: Mode
      direction: in
      binding: fromHeader
    - name: customer
      description: Customer to be saved
      direction: inout
      type: Customer
    - name: success
      description: Operation result
      direction: out
      type: boolean
```

This configuration generates a method signature like this:

```cs
public async Task<ActionResult<SaveCustomerResponse>> SaveCustomer(SaveCustomerRequest request, [FromQuery] string meccanografico, [FromHeader] string mode, CancellationToken requestAborted)
{...}
```

### `fromBody` Binding

In operations with a type of http_post (or other types that involve a request body), you can use the fromBody binding to pass a single parameter directly in the request body, without wrapping it in an envelope. Here's an example:

```yml
- name: saveCustomer
  type: http_post
  description: Save customer
  parameters:
    - name: customer
      description: Customer to be saved
      direction: in
      type: Customer
      binding: fromBody
    - name: success
      description: Operation result
      direction: out
      type: boolean
```

This configuration generates a method signature like this:

```cs
public async Task<ActionResult<SaveCustomerResponse>> SaveCustomer([FromBody] Customer customer, CancellationToken requestAborted)
{...}
```

Operation bindings provide fine-grained control over how parameters are passed between your API methods and the request, allowing for flexibility and customization in your API design.
