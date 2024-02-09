# Componenti di base

Il framework fornisce un set di componenti base estendibili, distribuite con il pacchetto ng-components. Numerosi sono i vantaggi derivati dall'utilizzo di queste componenti, ma il vantaggio principale è quello di avere a disposizione già delle opzioni/funzionalità che altrimenti lo sviluppatore avrebbe dovuto definire manualmente per ogni nuovo componente. Inoltre, ogni componente base (grazie all'integrazione del policy engine) fornisce le informazioni necessarie per sapere se il contenuto è visibile, nascosto, abilitato o disabilitato. Le componenti illustrate in questa sezione sono astratte e dunque non utilizzabili se non estese. Sono componenti base anche tutte quelle descritte nelle altre sezioni, con l'unica differenza che queste ultime sono utilizzabili anche senza necessità di essere estese.

## Options
Ogni componente base fornisce un input binding principale chiamato 'options' e rappresentante la configurazione base del componente stesso. Questo oggetto ovviamente può essere esteso nella componente ereditante. L'oggetto options deve essere costituito da proprietà non aggiornabili, ciò significa che una volta creato l'oggetto options da passare in binding alla componente, le proprietà di quest ultimo non andranno aggiornate. E' possibile aggiornare tali proprietà in due modi. Il primo è quello di creare un oggetto che rispetti il contratto delle options della componente, assegnarlo in input binding alla componente stessa e nel momento in cui una delle proprietà cambia, riassegnare l'oggetto a se stesso. Il secondo è quello di rendere osservabili tutte le proprietà dell'oggetto options che potranno essere cambiate (Subject/BehaviorSubject). Il componente base internamente esegue un merge tra le options passate in input dall'utente e le options che si ritengono essere di default. Ogni componente ereditata da una di base dunque dovrà implementare il metodo getDefaultOptions mergiando le opzioni (di default) della componente padre con quelle (della componente figlia) aventi un valore di default. Internamente la componente crea un oggetto chiamato 'internalOptions' che rappresenta esattamente il merge tra le options passate alla componente stessa e le options di default. Nell'implementazione della logica e del template della nuova componente quindi, si dovrà sempre far riferimento ad internalOptions invece che ad options.

```ts
protected getDefaultOptions() {
  return _.merge(super.getDefaultOptions(), {
    action: () => undefined,
    text: 'Default text'
  });
}
```
## Proprietà e metodi protected
Estendendo una componente base, è importante conoscerne le proprietà pubbliche e protected (oltre options ed internalOptions sopra descritte), ed i metodi che potranno essere overridati (oltre getDefaultOptions sopra descritto).
La proprietà width contiente la larghezza effettiva (in formato string) che si vuole dare al controllo, calcolata sulla base della proprietà width assegnata all'oggetto options (indipendentemente da se essa sia osservabile, numerica o stringa).
```ts
public width: string | number;
```
La proprietà height contiente l'altezza effettiva (in formato string) che si vuole dare al controllo, calcolata sulla base della proprietà height assegnata all'oggetto options (indipendentemente da se essa sia osservabile, numerica o stringa).
```ts
public height: string | number;
```
Il getter containerClass contiene la lista delle classi css (trasformata da array in string) che si vogliono applicare al container del controllo (es. div principale), calcolata sulla base della proprietà containerClass assegnata all'oggetto options.
```ts
public containerClass() {
  return this.internalOptions.containerClass.join(' ');
}
```
Il getter inputClass contiene la lista delle classi css (trasformata da array in string) che si vogliono applicare all'input del controllo, calcolata sulla base della proprietà inputClass assegnata all'oggetto options. Disponibile se si estende una componente base che estende almeno l'ShBaseInputComponent.
```ts
public inputClass() {
  return this.internalOptions.inputClass.join(' ');
}
```
Rappresenta un servizio singleton (già iniettato) in grado di fornire un nuovo id (in formato stringa 'id##') incrementale semplicemente chiamando il metodo next.
```ts
protected idSequence: IdSequenceService;
```
Rappresenta l'id di default del controllo, generato dal servizio IdSequenceService. E' importante sempre fare riferimento all'id calcolato sulle internalOptions, in quanto se l'utente avrà specificato un id nelle options esso corrisponderà allo stesso, altrimenti corrisponderà a quello di default (id).
```ts
protected id: string;
```
Rappresenta il tabIndex di default del controllo (0). E' importante sempre fare riferimento al tabIndex calcolato sulle internalOptions, in quanto se l'utente avrà specificato un tabIndex nelle options esso corrisponderà allo stesso, altrimenti corrisponderà a quello di default (tabIndex).
```ts
protected tabIndex: string;
```

Rappresenta un subject che emette un evento nel momento in cui il componente viene distrutto. E' consigliato utilizzarlo soprattutto in presenza di sottoscrizioni (con la pipe takeUntil) in modo tale da evitare memory leaks.
```ts
protected destroy$ = new Subject();
```
Rappresenta un servizio singleton (già iniettato) utile per la gestione di policy e claim. Per maggior dettagli vedi la sezione 'Authorization'. Disponibile se si estende una componente base che estende almeno l'ShBaseAuthComponent.
```ts
protected policyEngineService: PolicyEngineService;
```
Rappresenta un servizio singleton (già iniettato) utile per recuperare una possibile resource legata ad un oggetto. Per maggior dettagli vedi la sezione 'Authorization'. Disponibile se si estende una componente base che estende almeno l'ShBaseAuthComponent.
```ts
protected resourceService: ResourceService;
```
Contiene le proprietà enable e show (ottenute dal policy engine) che verranno confrontate con gli input binding 'enable' e 'show' per gestire l'abilitazione e la visibilità del controllo. Entrambe hanno valore di default true, dunque se non si utilizza il policy engine, non ci sarà nessuna variazione nel comportamento. Per maggior dettagli vedi la sezione 'Authorization'. Disponibile se si estende una componente base che estende almeno l'ShBaseAuthComponent.
```ts
protected authorizations: IShAuthorizationActions = {
  enable: true,
  show: true
};
```
Rappresenta un servizio singleton (già iniettato) per la gestione dei formGroup e formControl (per maggiori dettagli vedi sezione 'Metadati & Decoratori'). Disponibile se si estende una componente base che estende almeno l'ShBaseInputComponent.
```ts
protected formHandler: FormHandlerService;
```
La proprietà formControl rappresenta il form control (generato dal FormHandler) legato al value. Disponibile se si estende una componente base che estende almeno l'ShBaseInputComponent.
```ts
protected formControl: ShFormControl;
```
La callback astratta onModelValueChanges viene chiamata ogni qualvolta la proprietà legata all'oggetto (prop di model) cambia. Alla callback vengono passati come parametri il vecchio (oldValue) ed il nuovo valore (value). Se si decide di implementare questo metodo, è importante non porre al suo interno logica pesante per il ricalcolo dell'interfaccia utente. Disponibile se si estende una componente base che estende almeno l'ShBaseInputComponent.
```ts
protected onModelValueChanges: (oldValue: T, value: T) => void;
```
La proprietà placeholder rappresenta il testo posto nell'input in assenza di testo. Se non specificata nelle options, la componente base proverà a popolarla assegnandole una possibile label ottenuta dai metadati legati al value (model[prop]). Disponibile se si estende una componente base che estende almeno l'ShBaseInputComponent.
```ts
protected placeholder: string | Mstring;
```
I seguenti metodi sono overridabili, avendo cura di richiamare sempre la relativa super.
```ts
/**
 * The injection of services is delegated to injector
 */
constructor(injector: Injector) {
  super(injector);
  ...
}

public ngOnInit() {
  ...
  super.ngOnInit();
  ...
}

public ngOnChanges(changes: SimpleChanges) {
  super.ngOnChanges(changes);
}

public ngOnDestroy() {
  super.ngOnDestroy();
}

public ngDoCheck() {
  ...
  super.ngDoCheck();
  ...
}

/**
 * Event fired when user options changes
 */
protected onOptionsChanges() {
  ...
  super.onOptionsChanges();
  ...
}

/**
 * Event fired when new policies roll in.
 * Subclass which allow policies roll in, can override this method
 */
protected onPoliciesChanges(policies: TPolicies | IShAuthorizationActions) {
  ...
}
```

## ShBaseComponent

Rappresenta la componente più atomica del framework. Essa contiene le informazioni minime necessarie per creare una componente.
### Inputs

| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **options** | Object      | See properties section for options details | undefined         |

### Options Properties
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **id** | string | Control identifier | auto-generated |
| **tabindex** | number | Control tab-index | 0 |
| **autofocus** | boolean | Specifies if control take focus when is created | false |
| **containerClass** | Array\<string> | List of css classes to be applied to control container | [] |
| **width** | string \| number \| BehaviorSubject<string \| number> | Width of the control | auto |
| **height** | string \| number \| BehaviorSubject<string \| number> | Height of the control | auto |
	
## ShBaseAuthComponent
Estende la componente ShBaseComponent aggiungendo altri tre input binding: resource, enable e show. La resource (identificata da un resource name) è collegata ad una specifica policy la quale, in funzione dei claims dell'utente corrente, applica le sue regole laddove la stesso resource è applicata. 'enable' (default: true) specifica se il componente è abilitato (andrà applicata nel template html della nuova componente per disabilitare il contenuto desiderato). 'show' (default: true) specifica se il componente è visibile (andrà applicata al top del template html). Dunque, quando si va a creare il template della componente, le actions (enable e show) vanno applicate sugli elementi html che possono adottare il comportamento (es: il template della nuova componente presenta un div contenitore ed al suo interno un input di testo, è quindi consigliabile applicare la action di show sul div e la action di enable sull'input). L'ShBaseAuthComponent utilizza il policy engine per gestire tali privilegi, combinando rispettivamente i valori di enable e di show con i privilegi stessi (in and).

### Inputs
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **options** | Object | See properties section for options details | undefined |
| **enable** | boolean | Specifies if the control is enabled | true |
| **show** | boolean | Specifies if the control is visible | true |
| **resource** | string | Resource linked to control | undefined |
	
### Options Properties
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **id** | string | Control identifier | auto-generated |
| **tabindex** | number | Control tab-index | 0 |
| **autofocus** | boolean | Specifies if control take focus when is created | false |
| **containerClass** | Array\<string> | List of css classes to be applied to control container | [] |
| **width** | string \| number \| BehaviorSubject<string \| number> | Width of the control | auto |
| **height** | string \| number \| BehaviorSubject<string \| number> | Height of the control | auto |

## ShBaseModelComponent
Estende la componente ShBaseAuthComponent ed aggiunge due input binding 'model' e 'prop' ed un output binding 'valueChanges'. Questa componente va utilizzata quando si vuole creare un binding tra il controllo e la proprietà di un oggetto. Es. si vuole creare una componente che permetta la modifica/acquisizione del cognome di una persona in una textbox. Dato che il model rappresenta l'oggetto contenente la proprietà da mettere in binding col controllo, ed il prop rappresenta il nome della proprietà (del model) da mettere in binding, avremo i seguenti binding: [model]="persona" prop="cognome". Internamente il controllo dunque ricaverà il value in questo modo: this.model[this.prop].
### Inputs
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **options** | Object | See properties section for options details | undefined |
| **enable** | boolean | Specifies if the control is enabled | true |
| **show** | boolean | Specifies if the control is visible | true |
| **resource** | string | Resource linked to control | undefined |
| **model** | { [id: string]: T; } | The object for which binds a property | undefined |
| **prop** | string | The model property which will match the value of the control | "" |
	
### Outputs
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **valueChanges** | EventEmitter\<T> | Event fired when model property value changes | EventEmitter |

### Options Properties
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **id** | string | Control identifier | auto-generated |
| **tabindex** | number | Control tab-index | 0 |
| **autofocus** | boolean | Specifies if control take focus when is created | false |
| **containerClass** | Array<string> | List of css classes to be applied to control container | [] |
| **width** | string \| number \| BehaviorSubject<string \| number> | Width of the control | auto |
| **height** | string \| number \| BehaviorSubject<string \| number> | Height of the control | auto |
| **onCanValueChanges** | <T>(previousValue: T, nextValue: T): boolean | Event fired just before the value changes. Asks if it's possible to change the value. Returning false, the value will not vary | ()=>true |
	
### ShBaseInputComponent
Estende la componente ShBaseModelComponent ed aggiunge un input binding 'icon' e nuove options. Questa componente va estesa quando si vuole sviluppare una componente caratterizzata da un controllo di input. La componente, con l'ausilio del formHandler fornirà il form-control associato al value in bindng (model[prop]). Il form-control gestirà autonomamente gli eventi di change e le validazioni. Il nuovo template dovrà dunque far riferimento all'oggetto formControl per accedere al value (formControl.value), per osservarne la sua validità (formControl.valid o formControl.invalid), per comprendere il suo stato (dirty, touched, ecc..), ecc.. Specificando l'input 'icon', l'input dovrà essere affiancato da una icona. Le nuove options includono il placeholder dell'input, la proprietà isReadonly per specificare se l'input è in sola lettura, e la proprietà inputClass che prevede un array di classi css fornibili all'input.
### Inputs
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **options** | Object | See properties section for options details | undefined |
| **enable** | boolean | Specifies if the control is enabled | true |
| **show** | boolean | Specifies if the control is visible | true |
| **resource** | string | Resource linked to control | undefined |
| **model** | { [id: string]: T; } | The object for which binds a property | undefined |
| **prop** | string | The model property which will match the value of the control | "" |
| **icon** | string | If specified, the component is flanked by an icon | undefined |
	
### Outputs
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **valueChanges** | EventEmitter\<T> | Event fired when model property value changes | EventEmitter |
	
### Options Properties
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| **id** | string | Control identifier | auto-generated |
| **tabindex** | number | Control tab-index | 0 |
| **autofocus** | boolean | Specifies if control take focus when is created | false |
| **containerClass** | Array\<string> | List of css classes to be applied to control container | [] |
| **width** | string \| number \| BehaviorSubject<string \| number> | Width of the control | auto |
| **height** | string \| number \| BehaviorSubject<string \| number> | Height of the control | auto |
| **onCanValueChanges** | <T>(previousValue: T, nextValue: T): boolean | Event fired just before the value changes. Asks if it's possible to change the value. Returning false, the value will not vary | ()=>true |
| **placeholder** | string | Input placeholder | "" |
| **inputClass** | Array\<string> | List of css classes to be applied to input control | [] |
| **maxLength** | number | Specifies the maximum length (in characters) of input |  |
| **isReadonly** | boolean | Specifies whether input is readonly | false |


## ShBaseFormattedComponent
Estende la componente ShBaseInputComponent aggiungendo la possibilità di formattare il value (model[prop]) tramite una nuova opzione: 'format'. Esempi di componenti formatted sono ShDateComponent ed ShNumberComponent.
### Inputs
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| ***options*** | Object      |See properties section for options details  | undefined       |
| ***enable*** | boolean |Specifies if the control is enabled|true|
|***show***|boolean|Specifies if the control is visible|true|
|***resource***|string|Resource linked to control|undefined|
|***model***|{ [id: string]: T; }|The object for which binds a property|undefined|
|***prop***|string|The model property which will match the value of the control|""|
|***icon***|string|If specified, the component is flanked by an icon|undefined|

### Outputs
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
|***valueChanges***|EventEmitter\<T>|Event fired when model property value changes	|EventEmitter|


### Options Properties
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| ***id***|string|Control identifier	auto-generated|
|***tabindex***|number|Control tab-index	|0|
| ***autofocus***|boolean|Specifies if control take focus when is created|	false|
| ***containerClass***|Array\<string>|List of css classes to be applied to control container|	[]|
| ***width***	|string \| number \| BehaviorSubject<string \| number>|Width of the control	|auto|
| ***height***|string \| number \| BehaviorSubject<string \| number>|Height of the control	|auto|
| ***onCanValueChanges***|<T>(previousValue: T, nextValue: T): boolean|Event fired just before the value changes. Asks if it's possible to change the value. Returning false, the value will not vary	|()=>true|
| ***placeholder***|string|Input placeholder	|""|
| ***inputClass***	|Array\<string>|List of css classes to be applied to input control	|[]|
| ***maxLength***	|number|Specifies the maximum length (in characters) of input	|[]|
| ***isReadonly***|boolean|Specifies whether input is readonly	|false|
| ***format***|string|The format of the text (just for formatted components)	|""|

## ShBaseLookupSingleComponent

Estende la componente ShBaseInputComponent aggiungendo quattro nuove options: 'values', 'valuesPipe', 'equalityFunc' e 'transform'. Questa componente va estesa quando si vuole sviluppare una componente caratterizzata da una lista di valori dai quali se ne può scegliere uno da impostare come value (model[prop]). La options 'values' dunque è un array che dovrà contenere la lista dei valori, mentre la options 'valuesPipe' è l'istanza della pipe che potrà essere applicata sulla lista 'values' per formattare gli elementi da mostrare. Esempi di componenti lookup-single sono ShRadio ed ShSelect.
### Inputs
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| ***options***|Object|See properties section for options details	|undefined|
|***enable***|boolean|Specifies if the control is enabled	|true|
|***show***|boolean|Specifies if the control is visible	true|
|***resource***|string|Resource linked to control	|undefined|
|***model***|{ [id: string]: T; }|The object for which binds a property	|undefined|
|***prop***|string|The model property which will match the value of the control|	""|
|***icon***|string|If specified, the component is flanked by an icon|	undefined

### Outputs
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| ***valueChanges***|EventEmitter\<T>|Event fired when model property value changes	|EventEmitter

### Options Properties
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| ***id***|string|Control identifier	|auto-generated|
|***tabindex***|number|Control tab-index|	0|
|***autofocus***|boolean|Specifies if control take focus when is created|	false|
|***containerClass***|Array\<string>|List of css classes to be applied to control container|	[]|
|***width***|string \| number \| BehaviorSubject<string \| number>|Width of the control|	auto|
|***height***|string \| number \| BehaviorSubject<string \| number>|Height of the control|	auto|
|***onCanValueChanges***|<T>(previousValue: T, nextValue: T): boolean |Event fired just before the value changes. Asks if it's possible to change the value. Returning false, the value will not vary	|()=>true|
|***placeholder***|string|Input placeholder	|""|
|***inputClass***|Array\<string>|List of css classes to be applied to input control|	[]|
|***maxLength***|number|Specifies the maximum length (in characters) of input	|[]|
|***isReadonly***|boolean|Specifies whether input is readonly	|false|
|***values***|Array\<V> | Observable\<Array\<V>>|List of values to use as lookup values	|[]|
|***valuesPipe***|PipeTransform|Pipe which will be applied to lookup values to format label	|undefined|
|***valuesPipeArgs***|Array\<any>|valuesPipeArgs-description|	undefined|
|***equalityFunc***|(modelValue: T, lookupValue: V) => boolean|Equality function which optimizes the process of comparing|(modelValue: T, lookupValue: V) => _.isEqual(modelValue, lookupValue)
|***transform***|(lookupValue: V) => T|Function which transforms control value to model property value|	(lookupValue: V) => <any>lookupValue as T|


## ShBaseLookupMultiComponent
Estende la componente ShBaseInputComponent aggiungendo quattro nuove options: 'values', 'valuesPipe', 'equalityFunc' e 'transform'. Questa componente va estesa quando si vuole sviluppare una componente caratterizzata da una lista di valori dai quali se ne possono scegliere uno o più da impostare come value (model[prop]). La options 'values' dunque è un array che dovrà contenere la lista dei valori, mentre la options 'valuesPipe' è l'istanza della pipe che potrà essere applicata sulla lista 'values' per formattare gli elementi da mostrare. Esempi di componenti lookup-multi sono ShCheckGroup ed ShMultiSelect.

### Inputs
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| ***options***|Object|See properties section for options details	undefined|enable|boolean|Specifies if the control is enabled	|true|
|***show***|boolean|Specifies if the control is visible|	true|
|***resource***|string|Resource linked to control|	undefined|
|***model***|{ [id: string]: T; }|The object for which binds a property	|undefined|
|***prop***|string|The model property which will match the value of the control	|""|
|***icon***|string|If specified, the component is flanked by an icon	|undefined|

### Outputs
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| ***valueChanges***|EventEmitter<T>|Event fired when model property value changes|	EventEmitter|

### Options Properties
| Nome        | Tipo        | Descrizione                                | Valore di default |
| ----------- | ----------- | -----------                                | -----------       |
| ***id***|string|Control identifier|	auto-generated|
|***tabindex***|number|Control tab-index	|0|
|***autofocus***|boolean|Specifies if control take focus when is created	|false|
|***containerClass***|Array\<string>|List of css classes to be applied to control container|	[]|
|***width***|string \| number \| BehaviorSubject<string \| number>|Width of the control	|auto|
|***height***|string \| number \| BehaviorSubject<string \| number>|Height of the control	|auto|
|***onCanValueChanges***|<T>(previousValue: T, nextValue: T): boolean|Event fired just before the value changes. Asks if it's possible to change the value. Returning false, the value will not vary	|()=>true|
|***placeholder***|string|Input placeholder	|""|
|***inputClass***|Array\<string>|List of css classes to be applied to input control|	[]|
|***maxLength***|number|Specifies the maximum length (in characters) of input	|[]|
|***isReadonly***|boolean|Specifies whether input is readonly|	false|
|***values***|Array\<V> | Observable\<Array\<V>>|List of values to use as lookup values|	[]|
|***valuesPipe***|PipeTransform|Pipe which will be applied to lookup values to format label	|undefined|
|***equalityFunc***|(modelValue: T, lookupValue: V) => boolean|Equality function which optimizes the process of comparing	|(modelValue: T, lookupValue: V) => _.isEqual(modelValue, lookupValue)|
|***transform***|(lookupValue: V[]) => T[]|Function which transforms control value to model property value|	(lookupValues: V[]) => lookupValues && lookupValues.map((value) => value as T)|