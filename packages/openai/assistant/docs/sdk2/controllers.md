# Controllers

I controllers e i metodi che essi espongono sono generati automaticamente a seguito della definizione di una o più operation.

```yml
operations:
  - name: withdrawProducts
    type: http_post
    description: Preleva una certa quantità di un prodotto dal magazzino
    parameters:
      - name: productId
        description: L'id del prodotto da prelevare
        type: uuid
        direction: in
      - name: quantity
        description: La quantità da prelevare
        type: integer
        direction: in
      - name: success
        description: Indica se l'operazione ha avuto successo
        type: boolean
        direction: out
      - name: newQuantity
        description: La quantità aggiornata
        type: integer
        direction: out
```

Questa operazione genererà un metodo astratto nella classe `ControllerBase` che conterrà la definizione dell'operazione.

```c#
[HttpPost("withdrawProducts")]
public abstract Task<WithdrawProductsResponse> WithdrawProducts(WithdrawProductsRequest request, CancellationToken requestAborted);
```

Questo metodo dovrà essere implementato nella classe concreta che implementa il `ControllerBase`. Ciò può essere velocemente fatto su Visual Studio premendo la combinazione di tasti 'CTRL + .' sulla definizione della classe del controller (in corrispondenza dell'avviso di errore). Il metodo creato avrà la seguente forma:

```c#
[HttpPost("withdrawProducts")]
public override Task<WithdrawProductsResponse> WithdrawProducts(WithdrawProductsRequest request, CancellationToken requestAborted)
{
    throw new NotImplementedException();
}
```

A questo punto, è possibile procedere ad implementare l'operazione.

Insieme al metodo, verranno create anche le classi che modellano la richiesta e la risposta specificate nell'operation, in questo caso `WithdrawProductsRequest` e `WithdrawProductsResponse`.

```c#
public class WithdrawProductsRequest
{
    public Guid ProductId { get; set; }
    public int Quantity { get; set; }
}

public class WithdrawProductsResponse
{
    public bool Success { get; set; }
    public int NewQuantity { get; set; }
}
```
