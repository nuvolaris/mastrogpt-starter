# Annotations

Le "annotation" sono un modo per aggiungere metadati o informazioni aggiuntive a snippet di codice. Sono spesso utilizzate per scopi di documentazione, ottimizzazione del codice o per scopi specifici di alcune tecnologie e framework.  

Nell'esempio seguente vengono utilizzate delle annotazioni recuperate da uno specifico namespace di un catalogo pubblicato online. Le annotazioni dell'esempio seguente permettono di generare degli attributi C# che vengono applicati su entità e relative proprietà:

```yaml
entities:
  - name: Category
    description: The product category
    useRepository: true
    repositoryName: Category
    annotations:
      - name: table.ejs
        namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
        value: Categories
    fields:
      - name: name
        type: string
        description: The name of the category
        annotations:
          - name: key
            namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
```

Questo andrà a generare una classe `Category` sulla quale verrà applicato l'attributo `Table`. La classe conterrà una proprietà `Name` sulla quale troveremo l'attributo `Key`.

Le annotation hanno tre proprietà:
1. **name**: indica il nome del template (è possibile omettere l'estensione).
2. **namespace**: indica il namespace dal quale recuperare l'annotazione (può riferirsi anche all'url di un catalogo online).
3. **value**: indica il valore da applicare all'attributo (se previsto).

Ad esempio, nel caso precedente, il template verrà scaricato dall'url `https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/key.ejs`
```
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Ca.ShoppingCart.Store.Domain.Model
{
  /// <summary>
  /// The product category
  /// </summary>
  [Table("Categories")]
  public partial class Category : EntityBase
  {
    /// <summary>
    /// The name of the category
    /// </summary>
    [Key]
    public string Name
    {
      get;
      set;
    }
  }
}
```
## Key
### Può essere applicato ad una proprietà per rendere, la colonna corrispondente del database, una colonna PrimaryKey. Per ulteriori informazioni fare riferimento alla [documentazione ufficiale](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.keyattribute?view=net-5.0).

**YAML:**
```
annotations:
  - name: key
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
```
**Codice generato:**
```
[Key]
...
```
## MaxLength
### Può essere applicato ad una proprietà per specificare la lunghezza massima della stringa consentita nella colonna corrispondente nel database. Per ulteriori informazioni fare riferimento alla [documentazione ufficiale](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.maxlengthattribute?view=net-5.0).

**YAML:**
```
annotations:
  - name: maxLength
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
    value: 20
```
**Codice generato:**
```
[MaxLength(20)]
...
```
## MinLength
### Può essere applicato ad una proprietà per specificare la lunghezza minima della stringa consentita nella colonna corrispondente nel database. Per ulteriori informazioni fare riferimento alla [documentazione ufficiale](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.minlengthattribute?view=net-5.0).

**YAML:**
```
annotations:
  - name: minLength
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
    value: 5
```
**Codice generato:**
```
[MinLength(5)]
...
```
## Table
### Può essere applicato ad una classe per configurare il nome della tabella e lo schema corrispondenti nel database. Per ulteriori informazioni fare riferimento alla [documentazione ufficiale](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.schema.tableattribute?view=net-5.0).

**YAML:**
```
annotations:
  - name: table
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
    value: TableName
```
**Codice generato:**
```
[Table("TableName")]
...
```
## Column
### Può essere applicato ad una proprietà per configurare il nome, l'ordine e il tipo di dati della colonna corrispondente nel database. Per ulteriori informazioni fare riferimento alla [documentazione ufficiale](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.schema.columnattribute?view=net-5.0).

**YAML:**
```
annotations:
  - name: column
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
    value: PropertyName
```
**Codice generato:**
```
[Column("PropertyName")]
...
```
## ForeignKey
### Può essere applicato ad una proprietà per marcarla come chiave esterna. Per ulteriori informazioni fare riferimento alla [documentazione ufficiale](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.schema.foreignkeyattribute?view=net-5.0).

**YAML:**
```
annotations:
  - name: foreign-key
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
    value: PropertyName
```
**Codice generato:**
```
[ForeignKey("PropertyName")]
...
```
## NotMapped
### Può essere applicato ad una proprietà o ad una classe che deve essere esclusa dalla generazione del modello e non deve generare la corrispondente colonna/tabella nel database. Per ulteriori informazioni fare riferimento alla [documentazione ufficiale](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.schema.notmappedattribute?view=net-5.0).

**YAML:**
```
annotations:
  - name: not-mapped
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
```
**Codice generato:**
```
[NotMapped]
...
```
## DatabaseGenerated
### Può essere applicato ad una proprietà per indicare come il database sottostante dovrebbe generare il valore per la colonna corrispondente. Ammette tre valori: None, Identity, Computed. Nel caso in cui venga inserito un valore errato, verrà stampato un messaggio di log e sarà impostato None come valore di default. Per ulteriori informazioni fare riferimento alla [documentazione ufficiale](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.schema.databasegeneratedattribute?view=net-5.0).

**YAML:**
```
annotations:
  - name: database-generated
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
    value: Identity # Valori consentiti: None, Identity, Computed
```
**Codice generato:**
```
[DatabaseGenerated(DatabaseGeneratedOption.None)]
...
```
## InverseProperty
### Può essere applicato ad una proprietà per specificare l'inverso di una proprietà di navigazione, che rappresenta l'altrà estremità della stessa relazione. Per ulteriori informazioni fare riferimento alla [documentazione ufficiale](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.schema.inversepropertyattribute?view=net-5.0).

**YAML:**
```
annotations:
  - name: inverse-property
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
    value: PropertyName
```
**Codice generato:**
```
[InverseProperty("PropertyName")]
...
```
## ComplexType
### Può essere applicato ad una classe per marcarla come tipo complesso. Per ulteriori informazioni fare riferimento alla [documentazione ufficiale](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.schema.complextypeattribute?view=net-5.0).

**YAML:**
```
annotations:
  - name: complex-type
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
    value: PropertyName
```
**Codice generato:**
```
[ComplexType("ClassName")]
...
```
## Required
### Può essere applicato ad una proprietà per specificare che la corrispondente colonna del database non può contenere valori nulli. Per ulteriori informazioni fare riferimento alla [documentazione ufficiale](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.requiredattribute?view=net-5.0).

**YAML:**
```
annotations:
  - name: required
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
```
**Codice generato:**
```
[Required]
...
```
## Attribute
### Questa particolare annotazione consente di generare degli attributi custom. Il valore del parametro `value` sarà inserito all'interno di parentesi quadre. Può essere, quindi, applicato ad una classe o ad una sua proprietà a seconda del tipo di annotazione generata.

**YAML:**
```
annotations:
  - name: attribute
    namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
    value: CanBeAnything
```
**Codice generato:**
```
[CanBeAnything]
...
```
L'esempio seguente invece andrà a generare una classe `Category`. La classe conterrà una proprietà `Name` alla quale sarà applicato l'attributo `CustomValues(Key=1, Value="randomValue")` contenente il valore specificato.

**YAML:**
```
entities:
  - name: Category
    description: The product category
    useRepository: true
    repositoryName: Category
    fields:
      - name: name
        type: string
        description: The name of the category
        annotations:
          - name: attribute
            namespace: https://schemacodearchitects.blob.core.windows.net/templates/entityfwk/
            value: CustomValues(Key=1, Value="randomValue")
```
**Codice generato:**
```
...
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Ca.ShoppingCart.Store.Domain.Model
{
  /// <summary>
  /// The product category
  /// </summary>
  public partial class Category : EntityBase
  {
    /// <summary>
    /// The name of the category
    /// </summary>
    [CustomValues(Key=1, Value="randomValue")]
    public string Name
    {
      get;
      set;
    }
  }
}
...
```