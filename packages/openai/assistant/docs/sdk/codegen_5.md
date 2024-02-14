# Codegen

## Templates

I template EJS sono il cuore della generazione del codice. I template sono utilizzati per trasformare in codice organizzato, ingegnerizzato, compilabile ed eseguibile tutto ciò che è stato definito all'interno dei file YAML (container, entities, operations, ...).

E' possibile sovrascrivere qualsiasi template EJS utilizzando il task di Scarface: "Override Codegen template". Scarface chiederà all'utente il percorso esatto del template da sovrascrivere. Al termine di questa procedura, il template verrà copiato nella folder "codegen\\templates" del progetto e potrà essere modificato, applicando le novità introdotte al successivo ciclo di generazione.

Ricavare il template utilizzato per generare uno snippet di codice, è molto semplice: tutti gli snippet iniziano con il commento /_ #begin-template <template-path> _/ e terminano con il commento /_ #end-template <template-path> _/, dove <template-path> indica il percorso del template EJS di riferimento:

```js
/* #begin-template component/state.ejs */
  ...
  /* #end-template component/state.ejs */
```

Tutti i file generati, sono contrassegnati con un "header" al top del file che indica come comportarsi con il file in questione. Il seguente header indica che il file NON deve essere assolutamente modificato, in quanto ad ogni nuovo ciclo di generazione verrà totalmente sovrascritto.

```js
/**********************************************************\
  * Automatically produced by CA code generator            *
  *                                                      *
  * IMPORTANT NOTE:                                        *
  *                                                      *
  * Auto generated file. Do not modify please.             *
\**********************************************************/
```

Il seguente header invece indica che il file può essere modificato, in quanto dopo la prima generazione non verrà più toccato:

```js
/**********************************************************\
  * Automatically produced by CA code generator            *
  *                                                      *
  * IMPORTANT NOTE:                                        *
  *                                                      *
  * Auto generated file. This file CAN be modified by you. *
\**********************************************************/
```

Quest ultimo header infine indica che è possibile modificare il file in tutti i punti, tranne che nei "punti di iniezione":

```js
/**********************************************************\
  * Automatically produced by CA code generator            *
  *                                                      *
  * IMPORTANT NOTE:                                        *
  *                                                      *
  * Auto generated file. This file CAN be modified by you. *
  * Do not change injection points please.                 *
\**********************************************************/
```

contrassegnati come di seguito:

```ts
// --inject:imports--
import { JsonObject, JsonIgnore } from '@ca-webstack/reflection';
import { IActivityPayload, IActivityAnnotation } from '@ca-webstack/ng-shell';
// --inject:imports--
import { Employee } from './../../../models/index';
```

Quest'ultimo header infine indica che è possibile modificare il file solo all'interno delle custom zone:

```ts
/**********************************************************\
  * Automatically produced by CA code generator            *
  *                                                        *
  * IMPORTANT NOTE:                                        *
  *                                                        *
  * Auto generated file. This file CAN be modified by you  *
  * Only in the custom zone.                               *
\**********************************************************/
```

contrassegnate come di seguito:

```cs
using AutoMapper;
using CodeArchitects.Platform.Common.Collections;
// <custom:using>
// </custom:using>

namespace Ca.BackOffice.Business.Mappings
{
  public class CustomerProfile : Profile
  {
    // <custom:parameters>
    // </custom:parameters>

    // <custom:constructor>
    public CustomerProfile()
    {
      // </custom:constructor>
      MapCustomerEntityToCustomerDto();
      MapCustomerEntityToCustomerBrowseDto();
      MapCustomerDtoToCustomerEntity();
      MapCustomerBrowseDtoToCustomerEntity();

      // <custom:mappings>
      // </custom:mappings>
    }
```
