# Metadati e decoratori
In questa sezione sono spiegati i concetti di gestione del contesto applicativo, di metaprogrammazione, aspect-oriented e validations.

## OVERVIEW

### Context
Il framework offre la possibilità di gestire il contesto applicativo differenziandolo in contesto di browse (visualizzazione/consultazione/default) e contesto di edit (modifica). Questo può agevolare molto il riutilizzo, permettendo dunque di avere ad esempio uno stesso form per la gestione della modifica e per la visualizzazione (invece che gestire due form con la medesima struttura).

Per prima cosa, è necessario importare l'enumerato Context ed il servizio che lo gestisce (ContextService) dal pacchetto ng-aspects.
 ```ts
import { ContextService, Context } from '@ca-webstack/ng-aspects';
 ```
Iniettiamo il servizio laddove vogliamo utilizzarlo. Di default la gestione del context non è abilitata. Per abilitarla andrà chiamato il metodo enable del servizio. Se si vuole gestire una applicazione interamente col context, è consigliabile effettuare l'enable nell'index component di applicazione.
 ```ts
public constructor(
  ...
  protected contextService: ContextService,
) {
  this.contextService.enable();
}
 ```
Di default il contesto (se abilitato) è impostato su 'browse'. Per cambiarlo basterà modificare la proprietà context del ContextService come di seguito:

 ```ts
...
this.contextService.enable();
...
 ```
Per disabilitare la gestione del contesto basterà chiamare il metodo disable del servizio. Nel caso si voglia gestire il contesto solo in determinati strati dell'applicazione, è consigliabile disabilitare l'annessa gestione nel metodo onDestroy.
 ```ts
public onDestroy() {
  this.contextService.disable();
}
 ```

### Aspects

L'Aspect è utilizzato nella programmazione ad aspetti per modularizzare i comportamenti trasversali all'applicazione che si ripercuotono in più punti dell'object model. Grazie agli aspect è possibile aggiungere dinamicamente comportamenti agli oggetti di dominio senza che questi ne siano a conoscenza. Nel nostro caso, applicando il decoratore @Aspect su una proprietà di un qualsiasi oggetto, siamo in grado di descriverne il modo in cui essa verrà mostrata (con che componente), la label localizzata (o no) che verrà apposta su di essa e suddividere tutto per contesto (con la possibilità dunque di avere componenti e label diverse in funzione del contesto).

Nell'esempio seguente, la property verrà mostrata con la label 'Browse label' e con il componente ShCaption in contesto di browse, con la label localizzata con chiave 'edit-label-key' (con fallback 'Edit Label') e con il componente ShTextArea in contesto di edit, con la label localizzata con chiave 'default-label-key' (con fallback 'Default Label') e con il componente ShText nel caso in cui non sia abilitata la gestione del contesto. Non è dunque obbligatorio inserire le proprietà 'browse' ed 'edit' nel decoratore @Aspect.

```ts
@Aspect({
  default: {
    label: {
      key: 'default-label-key',
      default: 'Default Label'
    },
    template: 'text'
  },
  browse: {
    label: 'Browse Label',
    template: 'caption'
  },
  edit: {
    label: {
      key: 'edit-label-key',
      default: 'Edit Label'
    },
    template: 'textarea'
  }
})
protected property: string;
```

### Entry Components

Una entry component è una qualsiasi componente che il sistema carica in modo imperativo (il che significa che non va referenziata nel Document Object Model), per tipo. È possibile rendere una componente una entry component eseguendone il bootstrap in un NgModule ed aggiungendola al templates-dictionary di applicazione (applicationname-template.dictionary.ts). Scarf-Ace automatizza questo processo (in fase di generazione di una nuova componente) chiedendo all'utente se si vuole rendere entry component la nuova componente. In tal caso lo Scarf-Ace aggiungerà la nuova componente nelle entry components del modulo 'Components' applicativo e nel templates-dictionary aggiungerà una nuova chiave corrispondente al nome della componente stessa in UPPERCASE (senza trattini o underscore) con come valore il riferimento alla stessa.

Generando una nuova componente con lo Scarf-Ace (e scegliendo dunque entry-component), il tool inserirà la componente anche nell'array entryComponents dell'ngModule del modulo ComponentsModule di applicazione. Non utilizzando il tool, questo procedimento andrà eseguito manualmente.

```ts
@NgModule({
  declarations: [
    ...
    SelectorComponent
  ],
  imports: [
    ...
  ],
  exports: [
    ...
    SelectorComponent
  ],
  providers: [
    ...
  ],
  entryComponents: [
    ...
    SelectorComponent
  ]
})
export class ComponentsModule { }
```

Lo Scarf-Ace si occuperà anche di inserire la componente nel template dictionary (operazione manuale se non si utilizza il tool). Il template dictionary viene creato in fase di scaffolding dell'applicazione ed ha come nome {nomeapp}-template.dictionary.ts. Questo oggetto conterrà tutte le componenti utilizzabili con gli Aspects. Dunque, inserendo una componente nel dizionario, con chiave corrispondente al nome della componente stessa in UPPERCASE (senza trattini o underscore) e valore corrispondente al riferimento della stessa, potremo inserire nella proprietà 'template' del decoratore @Aspect, la chiave della componente in lowercase (es. template: 'selector')

```ts
import { TemplateDictionary, ShTemplate } from '@ca-webstack/ng-components';
import * as _ from 'lodash';
import { SelectorComponent } from './../components/selector/selector.component';

export const StorybookTemplate: TemplateDictionary = _.merge(ShTemplate,
  {
    // Put here components you want to use with AOP
    SELECTOR: SelectorComponent
  });
```

L'application template dictionary estende il template dictionary di framework che già prevede un set di componenti built-in utilizzabili con gli aspects. Per conoscere la chiave corrispondente al componente built-in che ci interessa, basta andare nella sezione (dello Storybook) relativa al componente stesso e leggerne l'Aspect Key.


### Validations
E' possibile applicare criteri di validazione su proprietà ed oggetti utilizzando il decoratore @Validation. In questo modo potremo automatizzare tutti i processi di validazione ed evitare i complessi procedimenti di configurazione dei FormGroup e FormControl. Inoltre, i componenti built-in di framework e le componenti ereditate da essi, inglobano già i controlli di validazione (da metadati).

Nell'esempio seguente, la property (per essere valida) dovrà obbligatoriamente avere un valore e la sua lunghezza non dovrà superare i 20 caratteri. E' possibile applicare i validatori built-in di Angular (es. Validators.required, Validators.maxLength, ecc..) o crearne di nuovi inserendoli (come static) nella classe ShellValidators (situata nel file validators.ts nei servizi di applicazione).
```ts
@Validation({
  validator: Validators.required,
  message: 'The field is mandatory'
}, {
  validator: Validators.maxLength(20),
  message: {
    key: 'max-length-validator-key',
    default: 'The field can be up to 20 characters long'
  }
})
protected property: string;
```
### Warnings

E' possibile applicare criteri di validazione NON bloccanti su proprietà ed oggetti utilizzando il decoratore @Warning. In questo modo potremo automatizzare tutti i processi di validazione NON bloccanti ed evitare i complessi procedimenti di configurazione dei FormGroup e FormControl. Inoltre, i componenti built-in di framework e le componenti ereditate da essi, inglobano già i controlli di validazione NON bloccanti (da metadati).

Nell'esempio accanto, la property per non mostrare dei messaggi di warning, dovrà avere un valore e la sua lunghezza non dovrà superare i 20 caratteri. E' possibile applicare i validatori built-in di Angular (es. Validators.required, Validators.maxLength, ecc..) o crearne di nuovi inserendoli (come static) nella classe ShellValidators (situata nel file validators.ts nei servizi di applicazione).
```ts
@Warning({
  validator: Validators.required,
  message: 'The field is mandatory'
}, {
  validator: Validators.maxLength(20),
  message: {
    key: 'max-length-validator-key',
    default: 'The field can be up to 20 characters long'
  }
})
protected property: string;
```

### Form Handler

Il FormHandler è un servizio offerto dal framework che permette di gestire agevolmente la validità (e molto altro) di uno o più form di validazione.
Per prima cosa, è necessario importare il servizio dal pacchetto ng-components.

```ts 
import { FormHandlerService } from '@ca-webstack/ng-components';
```
Per utilizzare il servizio, dovremo iniettarlo nel costruttore del componente coinvolto.

```ts
public constructor(
  ...
  private _formHandlerService: FormHandlerService
) {
  ...
}
```
Sottoscrivendosi all'osservabile validityChanges del servizio, è possibile ricevere notifiche del cambio di validità del form in binding nel contesto corrente.

```ts
this._formHandlerService.validityChanges
.subscribe(isValid => {
  this.isValid = isValid
});
```

Per evitare di introdurre memory leaks è necessario gestire l'unsubscribe della sottoscrizione. E' possibile gestirla in due modi. Se stiamo lavorando su una componente che estende una delle base components di framework, possiamo aggiungere il takeUntil sull'osservabile destroy$ (che lancerà una notifica nel momento in cui il componente verrà deallocato):
```ts
this._formHandlerService.validityChanges
.pipe(takeUntil(this.destroy$))
.subscribe(isValid => {
  this.isValid = isValid
});
```
Se stiamo invece lavorando su una activity component (componente nodo del workflow di uno scenario), possiamo pushare la sottoscrizione nell'array delle subscriptions. Il framework si occuperà (durante la deallocazione del componente) di eseguire l'unsubscribe di tutte le sottoscrizioni inserite nell'array delle subscriptions:
```ts
this.subscriptions.push(
  this._formHandlerService.validityChanges
    .subscribe(isValid => {
      this.isValid = isValid
    })
);
```
E' possibile sapere se un oggetto è valido o non valido (se non ha criteri di validazione applicati, risulterà essere sempre valido) chiamando il metodo 'isValid' del servizio e passando come parametro l'oggetto stesso
```ts
this._formHandlerService.isValid(this.person);
```
Stessa cosa per una proprietà di un oggetto, passando come parametro anche il nome della proprietà interessata. Come nell'esempio seguente:
```ts
this._formHandlerService.isValid(this.person, 'surname');
```
Un'altra interessante feature di questo servizio, è quella di conoscere lo stato dirty sia di un oggetto che di una proprietà di un oggetto, come di seguito:
```ts
this._formHandlerService.isDirty(this.person);
this._formHandlerService.isDirty(this.person, 'age');
```
Per ricavare il FormGroup legato ad un oggetto (automaticamente creato per gli oggetti con criteri di validazione) è possibile richiamare il metodo getGroup del servizio, passando come parametro l'oggetto interessato:
```ts
this.formGroup = this._formHandlerService.getGroup(this.person);
```
Per ricavare invece il FormControl legato ada una proprietà di un oggetto è possibile richiamare il metodo getControl del servizio, passando come parametro la proprietà dell'oggetto interessato:
```ts
const formControl = this._formHandlerService.getControl(this.person, 'surname');
```

### ShFormControlComponent

Tutti i concetti illustrati sopra (ed ovviamente utilizzabili singolarmente), confluiscono in un unico componente jolly: ShFormControl. Questo speciale componente è in grado di leggere i metadati applicati su una proprietà di un oggetto ed istanziare automaticamente il componente con la relativa label indicati negli aspects in funzione del contesto corrente, impostare il binding ed applicarne le validazioni. Per maggiori dettagli consultare l'API Reference.

Definiamo una entità applicando aspects e validations come metadati (mediante i decoratori) sulle properties.
```ts
export class Person {
  @Validation({
    validator: Validators.required,
    message: { key: 'field-mandatory', default: 'Campo obbligatorio' }
  }, {
    validator: Validators.minLength(6),
    message: { key: 'at-least-six', default: 'Almeno 6 caratteri' }
  })
  @Aspect({
    default: {
      label: { key: 'name', default: 'Name' },
      template: 'text'
    }
  })
  name: string;
  @Aspect({
    default: {
      label: { key: 'surname', default: 'Surname' },
      template: 'select'
    }
  })
  surname: string;
}
```

Istanziamo l'entità nel nostro scenario
```ts
this.person = new Person();
this.person.name = 'Mario';
...
protected surnameOptions: IShSelectOptions<string, string> = {
    values: ['Bianchi', 'Rossi', 'Verdi']
};
```
Utilizziamo il componente sh-form-control sia per la proprietà name che per la proprietà surname dell'istanza dell'entita Person. Nel secondo sh-form-control aggiungiamo un altro input binding (options) che avrà un contratto software differente in funzione del tipo di template applicato come negli aspects.
```HTML
<div input-group-h>
    <sh-form-control [model]="person" prop="name"></sh-form-control>
    <sh-form-control [model]="person" prop="surname" [options]="surnameOptions"></sh-form-control>
</div>
```
[Live Demo](https://storybook.codearchitects.com/#/storybook/business/decorators/e52b5ad9-6efb-8e61-f00b-65aa1230cf1f/playground/$ShFormControlComponent)

### Esempio complesso

In questo esempio, oltre all'sh-form-control (con i relativi aspects e validations) viene utilizzato il cambio di contesto ed il form handler service.

```HTML
<div input-group-v>
    <div input-group-h>
      <h2>
        <span>Context: </span>
        <i>{{contextService.context | uppercase}}</i>
      </h2>
      <sh-button [enable]="formGroup?.valid" (clicked)="toggleContext()" [primary]="true">
        toggle-context</sh-button>
    </div>
    <h2>
      <span>Form Group: </span>
      <i translate>{{formGroup?.valid ? 'valid' : 'invalid'}}</i>
    </h2>
    
    <sh-form-control [model]="this" prop="property"></sh-form-control>
</div>
```
```ts
import { Validation, Aspect, ContextService, Context } from '@ca-webstack/ng-aspects';
import { Validators } from '@angular/forms';
import { FormHandlerService } from '@ca-webstack/ng-components';
...
  @Validation({
    validator: Validators.required,
    message: 'The field is mandatory'
  }, {
    validator: Validators.maxLength(20),
    message: {
      key: 'max-length-validator-key',
      default: 'The field can be up to 20 characters long'
    }
  })
  @Aspect({
    default: {
      label: {
        key: 'default-label-key',
        default: 'Default Label'
      },
      template: 'text'
    },
    browse: {
      label: 'Browse Label',
      template: 'caption'
    },
    edit: {
      label: {
        key: 'edit-label-key',
        default: 'Edit Label'
      },
      template: 'textarea'
    }
  })
  protected property: string;

  public constructor(
    ...
    protected contextService: ContextService,
    private _formHandlerService: FormHandlerService
  ) {
    ...
  }

  public async onInit(params: {}) {
    this.contextService.enable();
    this.contextService.context = Context.edit;
    this.formGroup = this._formHandlerService.getGroup(this);
  }

  public onDestroy() {
    this.contextService.disable();
  }

  public toggleContext() {
    this.contextService.context = this.contextService.context === Context.edit ? Context.browse : Context.edit;
  }
...
```
[Live Demo](https://storybook.codearchitects.com/#/storybook/business/decorators/e52b5ad9-6efb-8e61-f00b-65aa1230cf1f/playground/$complex-sample)

## API REFERENCE

### Inputs

| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **options** | Object      | See properties section for options details | undefined         |
| **enable**  | boolean     | Specifies if the control is enabled	     | true              |
| **show**    | boolean     | Specifies if the control is visible	     | true              |
| **resource**| string     | Resource linked to control	        	     | undefined         |
| **model**  | {[id: string]: T;} | The object for which binds a property| undefined         |
| **prop**   |  string  |The model property which will match the value of the control |	""   |


### Outputs

| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **valueChanges** | EventEmitter\<T\>  | Event fired when model property value changes | EventEmitter         |


### Options Properties

| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
|**id**	|string|Control identifier |	auto-generated|
|**tabindex** |number|Control tab-index	|0|
|**autofocus**	|boolean|Specifies if control take focus when is created|	false|
|**containerClass**	|Array\<string>|List of css classes to be applied to control container|	[]|
|**width**	|string \| number \| BehaviorSubject\<string \| number>|Width of the control|	auto|
|**height**	|string \| number \| BehaviorSubject\<string \| number>|Height of the control	|auto|
|**onCanValueChanges**	|\<T>(previousValue: T, nextValue: T): boolean|Event fired just before the value changes. Asks if it's possible to change the value. Returning false,the value will not vary	|()=>true|
|**label**	|string \| boolean \| Mstring |Replaces metadata label. If the value is setted to false, the label will be hidden.	|undefined|
|**labelClass**	|Array\<string>|List of css classes to be applied to label|	[]|
|**showValidationMessage**	|boolean |Specifies whether validation label is visible.|	true|
|**...**	|TOptions|Other options depends of which component ShFormControl dynamically instantiates. For e.g.: if aspect metadata says that the component to be instantiate is an ShSelectComponent, the options must be of type IShSelectOptions.	|{}|