# .NET 6

Il nuovo template che utilizza .NET 6 prevede alcune differenze con i template precedenti, legate all'introduzione dei top-level statements. In particolare, la classe Startup non è più necessaria, in quanto la configurazione dell'applicazione avviene direttamente in Program.cs. Ciononostante, il nuovo template definisce un file, chiamato App.cs che conterrà i metodi che configurano i vari servizi nel container di Dependency Injection, in maniera tale da identificare semanticamente i vari pezzi della configurazione e rendere pulito il codice all'interno di Program.cs.

Per utilizzare .NET 6, impostare la versione 6 del framework .NET nello yml del microservizio.

```yml
target:
  framework: net
  version: 6
```

Un esempio di Program generato con il template .NET 6 è il seguente.

```cs
WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

builder
  .AddCaepServices()
  .AddAutoMapper()
  .AddControllers()
  .AddCors()
  .AddDaprInfrastructure()
  .AddSignalR();

var app = builder.Build();

app.UseHttpsRedirection();

app.UseCors("CorsPolicy");

if (builder.Environment.IsDevelopment())
{
  app.UseDeveloperExceptionPage();
  app.UseSwagger();
  app.UseSwaggerUI(c => c.SwaggerEndpoint("/swagger/v1/swagger.json", "Ca.ShoppingCart.Business v1"));
}

app.UseRouting();

app.UseAuthorization();

app.UseEndpoints(endpoints =>
{
  endpoints.MapControllers();
});

app.Run();
```

Mentre, le implementazioni dei metodi di estensione `AddCaepServices`, eccetera si troveranno nel file App.cs.
