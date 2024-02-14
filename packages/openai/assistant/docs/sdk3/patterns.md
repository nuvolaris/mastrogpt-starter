# Patterns

Il framework è stato progettato per essere utilizzato con design pattern come command, decorator, memento, observer, lazy initialization, singleton, ecc... . Questi concetti (strettamente correlati tra loro) riguardano parti specifiche del flusso dell'applicazione. In questa pagina ne sono illustrati i fondamentali.

### Decorators

In questa sezione vegono illustrate le features (offerte dal Framework) che implementano il concetto del Decorator Pattern.

Il Decorator è un design pattern strutturale che consente di aggiungere dinamicamente behaviors ad un oggetto e/o di estenderne le funzionalità.

#### @JsonObject

Il decoratore @JsonObject aggiunge meta-informazioni ad una classe, in modo tale da renderla serializzabile/deserializzabile senza perderne il tipo (indicato nella proprietà name). Prendiamo come esempio una classe "Person" definita a livello di applicazione (chiamata nell'esempio "ApplicationName"), decorandala con @JsonObject ed indicando come name il suo tipo, durante l'operazione di deserializzazione di una istanza della classe stessa, ci ritroveremo con un oggetto di tipo ApplicationName.Person invece che con un oggetto plain senza identità.

```ts
@JsonObject({ name: 'ApplicationName.Person' })
export class Person {
...
}
```

__@JsonIgnore__

Il decoratore @JsonIgnore applicato ad una proprietà di una classe decorata con @JsonObject, indica che durante l'operazione di serializzazione, tale proprietà verrà ignorata (non serializzata).

```ts
@JsonIgnore() private _propertyName: string;
```

__@Entity__

Il decoratore @Entity applicato su una classe, permette di applicare il concetto dell'Object Identity sulle relative istanze. Con il parametro "name" specifichiamo il tipo al quale l'oggetto verrà associato. Con il parametro keys invece andremo ad indicare quali sono le proprietà dell'oggetto che lo identificano univocamente rispetto agli altri oggetti dello stesso tipo. E' possibile aggiugnere più keys, ma generalmente la proprietà che identifica univocamente l'oggetto, è "id". L'object identity è un concetto fondamentale della programmazione ad oggetti. Con l'object identity, gli oggetti possono contenere o fare riferimento ad altri oggetti. L'identity dunque è una proprietà di un oggetto che lo contraddistingue da tutti gli altri.

```ts
@Entity({
    name: 'ApplicationName.Person',
    keys: ['id']
})
export class Person {
...
}
```

__@Aspect & @Validation__

Con i decoratori @Aspect e @Validation, è possibile descrivere il modo in cui una proprietà di un oggetto viene mostrata in una pagina, ed applicarne delle validazioni.

[Per maggior dettagli sul "Context", visita la sezione "Metadati & Decoratori"](https://caep.codearchitects.com/docs/sdk/metadati-decoratori)

```ts
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
```

__@Component__

Il decoratore @Component contrassegna una classe come componente Angular e fornisce metadati di configurazione che determinano il modo in cui il componente deve essere elaborato, istanziato e utilizzato in fase di esecuzione.

 [Per maggior dettagli sul decoratore @Component, visita la documentazione ufficiale di "Angular"](https://angular.io/api/core/Component)

```ts
@Component({
  selector: 'app-component-name',
  templateUrl: './component-name.component.html',
  styleUrls: ['./component-name.component.scss']
})
```

__@Injectable__

Il decoratore @Injectable contrassegna una classe come servizio singleton, disponibile per essere iniettato come dipendenza.

[Per maggior dettagli sul decoratore @Injectable, visita la documentazione ufficiale di "Angular"](https://angular.io/api/core/Injectable)

``` ts
@Injectable()
```

__@Input__

Il decoratore @Input contrassegna una proprietà di una classe come proprietà di input e le fornisce metadati di configurazione.

[Per maggior dettagli sul decoratore @Input, visita la documentazione ufficiale di "Angular"](https://angular.io/api/core/Input)

```ts
 @Input() public property: string; 
 ```

__@Output__

Il decoratore @Output contrassegna una proprietà di una classe come proprietà di output e le fornisce metadati di configurazione.

[Per maggior dettagli sul decoratore @Output, visita la documentazione ufficiale di "Angular"](https://angular.io/api/core/Output)

```ts
@Output() public eventName: new EventEmitter<EventType>();
```

__@Pipe__

Il decoratore @Pipe fornisce una soluzione rapida per implementare delle display-value transformations utilizzabili nel template HTML.

[Per maggior dettagli sul decoratore @Pipe, visita la documentazione ufficiale di "Angular"](https://angular.io/api/core/Pipe)

```ts
@Pipe({
  name: 'pipeName'
})
```

__@ApplicationComponent__

Il decoratore @ApplicationComponent contrassegna una classe come index di Applicazione e fornisce metadati di configurazione che determinano il modo in cui il componente deve essere elaborato, istanziato e utilizzato in fase di esecuzione.

```ts
@ApplicationComponent({
  application: 'storybook',
  shortDescription: 'Storybook application'
})
```

__@DomainComponent__

Il decoratore @DomainComponent contrassegna una classe come index di Dominio e fornisce metadati di configurazione che determinano il modo in cui il componente deve essere elaborato, istanziato e utilizzato in fase di esecuzione, specificandone l'applicazione di appartenenza.

```ts
@DomainComponent({
  application: 'storybook',
  domain: 'crm',
  shortDescription: 'Crm domain'
})
```

__@TaskComponent__

Il decoratore @TaskComponent contrassegna una classe come index di Scenario e fornisce metadati di configurazione che determinano il modo in cui il componente deve essere elaborato, istanziato e utilizzato in fase di esecuzione, specificandone l'applicazione ed il dominio di appartenenza.

```ts
@TaskComponent({
  application: 'storybook',
  domain: 'crm',
  task: 'customers',
  shortDescription: 'Customers scenario'
})
```


__@ActivityComponent__

Il decoratore @ActivityComponent contrassegna una classe come stato navigazionale di uno scenario e fornisce metadati di configurazione che determinano il modo in cui il componente deve essere elaborato, istanziato e utilizzato in fase di esecuzione, specificandone l'applicazione, il dominio, lo scenario di appartenenza ed il path relativo (es. 'browse'). Utilizzando il generatore di codice, il codice generato somiglierà al seguente:

```ts
@ActivityComponent({ extends: Base.BrowseComponent }) 
```

La proprietà "extend" estende le proprietà del decoratore con le proprietà del componente base generato (contenente i riferimenti identificativi ad applicazione, dominio e scenario, oltre che contenere il path relativo di base). E' tuttavia possibile estendere i path per raggiungere lo stato mediante url, aggiungendone altri (con ad esempio parametri), come nell'esempio seguente:

```ts
@ActivityComponent({ extends: Base.BrowseComponent, path: ['browse', 'browse/:id', 'browse/:param1/:param2'] })
```

__@Resource__

Il decoratore @Resource applica una resource name (come metadato) su una proprietà di una classe.
 
[Per maggior dettagli sul decoratore @Resource, visita la sezione "Authorization"](https://caep.codearchitects.com/docs/sdk/authorization/)

```ts
@Resource({ uri: 'property://Invoice/code' })
public property: string;
```

__@NgModule__

Il decoratore @NgModule configura l'injector ed il compiler, ed aiuta a modularizzare ed organizzare oggetti correlati.

[Per maggior dettagli sul decoratore @NgModule, visita la documentazione ufficiale di "Angular"](https://angular.io/api/core/NgModule)

```ts
@NgModule({
  imports: [],
  declarations: [],
  providers: [],
  exports: [],
  entryComponents: [],
  bootstrap: []
})
```

### Payload
In questa sezione vengono illustrate le features messe a disposizione da un oggetto fondamentale chiamato "Payload" (reso disponibile dal Framework) che implementa il concetto del Memento Pattern. E' importante sapere che navigando verso un nuovo scenario, il sistema avvia un nuovo task, assegnandogli un identificativo univoco chiamato "taskId". Navigando tra i vari stati dello scenario e anche verso stati di altri scenari (indipendentemente dal fatto che essi siano appartenenti allo stesso od ad un altro dominio), il task non viene interrotto. L'interruzione del task avviene effettuando una navigazione assoluta verso un altro scenario (es. router link). In tutto il suo ciclo di vita, il task è accompagnato dal suddetto Payload.
Il Memento è un design pattern comportamentale che ha il compito di estrarre lo stato interno di un oggetto (senza violarne l'incapsulamento) e memorizzarlo, per poterlo poi ripristinare in un secondo momento.


Immaginiamo di avere una entità "Employee" così definita:

```ts
@JsonObject({ name: 'ApplicationName.Employee, ' })
@Entity({
    name: 'ApplicationName.Employee',
    keys: ['id']
})
export class Employee {
    id = UUID.UUID();
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

Il payload implementa un contratto software legato allo scenario. Tale contratto software risiede nella cartella models dello specifico scenario, ed è estendibile (fuori dalle zone di iniezione) con altre proprietà (di qualsiasi tipo). Immaginiamo di essere in uno scenario chiamato "invoices" e di voler persistere un oggetto di tipo "Employee", il contratto software sarà molto simile al seguente:

```ts
export interface InvoicesPayload extends IActivityPayload {
  /**
  * optional version of payload data
  */
  version?: number;
  // --inject:classDeclaration--
  /**
   * Object to persist
   */
  employee: Employee;
}
```

Ogni ActivityComponent (componente rappresentante un singolo stato di uno scenario) ha accesso al payload, con la possibilità di leggerne e modificarne le proprietà.

```ts
@ActivityComponent({ extends: Base.BrowseComponent })
@Component({ templateUrl: 'browse.html', providers: [Base.InvoicesServices] })
export class BrowseComponent extends Base.BrowseComponent implements IOnInit {
  ...
  public constructor(
    injector: Injector,
    services: Base.InvoicesServices
  ) {
    super(injector, services);
  }
  onInit(params: {}) {
    ...
    this.payload.employee = this.payload.employee || new Employee();
    ...
    this.payload.employee.name = 'Francesco';
    ...
  }
  ...
}
```
Il salvataggio dello stato non è automatico, ma è banalmente effettuabile richiamando il metodo saveState (presente in ogni ActivityComponent):

```ts
...
this.saveState();
...
```

La politica di salvataggio dello stato va decisa con attenzione, pensando sia alle prestazioni che al proprio dominio applicativo. E' possibile dunque salvare lo stato nel momento in cui si abbandona una pagina, o quando la validity del form cambia, o addirittura al cambio di un singolo carattere in un input di testo (sottoscrivendosi ad esempio all'evento valueChanges dei componenti di base), o in qualsiasi altro modo. Nell'esempio seguente (live **) viene mostrato in un blocco il nome dell'employee, mentre con il componente ShFormControl viene messa in binding la stessa proprietà "name" dell'istanza dell'entità "Employee" (risiedente nel payload) e si effettua il salvataggio dello stato ad ogni cambiamento di quest'ultima (sottoscrivendosi all'evento valueChanges):

```HTML
...
<div>{{payload.employee?.name}}</div>
<sh-form-control [model]="payload.employee" prop="name" (valueChanges)="saveState()"></sh-form-control>
...
```
Ogni applicazione è costituita da un file delegates (application-name_delegates.ts) che estende la classe base BaseDelegates. La classe BaseDelegates richiede l'implementazione dei seguenti metodi astratti legati al Payload:

```ts
...
abstract getLastPayloads<T extends IPayloadBrowse>(): Observable<T[]>;
abstract getPayloadByTaskId<T extends IActivityPayload>(taskId: string): Observable<T>;
abstract savePayload(payload: IActivityPayload): Observable<boolean>;
abstract deletePayload(taskId: string): Observable<boolean>;
...
```

"getPayloadByTaskId" e "savePayload" sono chiamati automaticamente dal sistema rispettivamente per ripristinare uno stato e per salvarne uno nuovo. "getLastPayloads" e "deletePayload" invece possono essere chiamati manualmente rispettivamente per ricevere la lista degli ultimi payloads salvati e per cancellarne uno. Di default tutti questi metodi agiscono sul localStorage, ma le loro implementazioni possono essere facilmente modificabili per puntare ad un eventuale server.


** Di seguito è riportato un esempio live di binding con il payload. Inserisci del testo e ricarica la pagina, oppure esegui il seguente comando "taskkill /f /im chrome.exe" (se si sta utilizzando chrome) per chiudere forzatamente il browser ed alla riapertura ripristinare la pagina. Riaprendo la pagina con lo stesso taskid, si può notare come lo stato viene ripristinato.

[Naviga verso una pagina di esempio](https://storybook.codearchitects.com/#/storybook/business/patterns/57ee7349-37ef-8a01-daeb-6ee92feda3ed/sample)


### Commands

In questa sezione viene illustrato come applicare il command pattern utilizzando il framework.
Il Command è un design pattern comportamentale che permette di isolare la porzione di codice che effettua un'azione, dal codice che ne richiede l'esecuzione. L'azione è incapsulata nell'oggetto Command. L'obiettivo è rendere variabile l'azione del client senza però conoscere i dettagli dell'operazione stessa. Inoltre il destinatario della richiesta può non essere deciso staticamente all'atto dell'istanziazione del command ma ricavato a tempo di esecuzione.


E' possibile applicare il command pattern su un metodo di una classe, utilizzando il decoratore @Command, come nell'esempio seguente:
```ts
@Command({
  name: 'save',
  label: 'save',
  iconClassName: 'uploader',
  family: 'action'
})
private showToast(){
  this._toastService.pop({ message: 'saved' });
}
```
Il contratto software da rispettare quando si utilizza il decoratore @Command è il seguente:
```ts
interface ICommandParams {
  /**
   * Command identifier
   */
  name: string;
  /**
   * The label of the command
   */
  label?: any;
  /**
   * The caption of the command
   */
  caption?: any;
  /**
   * Icon css associated class name
   */
  iconClassName?: any;
  /**
   * Html css associated class name
   */
  htmlClassName?: string;
  /**
   * Specifies whether command is visible.
   * It's possibile to specifies directly the boolean value
   * to show/hide command. By specifing a string instead (as property name),
   * system tries to found it on target
   * (e.g. @Command({ visible: 'targetPropertyName' }) => command.visible = target[visible])
   * @default true
   */
  visible?: boolean | string;
  /**
   * Specifies whether command is enabled.
   * It's possibile to specifies directly the boolean value
   * to enable/disable command. By specifing a string instead (as property name),
   * system tries to found it on target
   * (e.g. @Command({ enabled: 'targetPropertyName' }) => command.enabled = target[enabled])
   * @default true
   */
  enabled?: boolean | string;
  /**
   * Resource name linked to command
   */
  resource?: string;
  /**
   * Family that command belongs to
   */
  family?: string;
  /**
   * Command properties
   */
  properties?: { [key: string]: any };
}
```
E' possibile eseguire un command in tutti gli stati di uno scenario ed in tutti i file di index (applicazione,dominio e scenario) chiamando il metodo "command" e fornendo come parametro il name del comando stesso, come nell'esempio seguente:
```HTML
<sh-button (clicked)="command('save')">save</sh-button>
```

Indipendentemente dal contesto nel quale abbiamo definito un commands, mediante l'utilizzo del servizio CommandDispatcher già iniettato in tutti gli stati degli scenari e nei file di index (applicazione, dominio e scenario) e da iniettare invece nei componenti, è possibile sottoscriversi al Subject "changes" per ricevere la lista dei comandi contestuali e/o facenti parte di un livello superiore.

```ts
...
protected commands: ICommand[] = [];
...
onInit() {
    ...
    this.commandDispatcher.changes
      .subscribe((commands: ICommand[]) => this.commands = commands);
    ...
}
...
```

Di seguito un esempio di utilizzo dei commands (ricavati con il codice soprastante) interpolati con il componente ShButton:

```HTML
<sh-caption>Commands (**)</sh-caption>

<div button-group-v>
  <sh-button *ngFor="let c of commands" [icon]="c.iconClassName" [primary]="true" (clicked)="c.handler()">
    {{c.label | translate}}</sh-button>
</div>
```
Commands (**)

E' possibile utilizzare la funzione "addCommands" del pacchetto ng-components, per aggiungere dinamicamente comandi al contesto corrente, rispettando sempre il contratto software ICommandParams. Per rendere effettive le modifiche è necessario chiamare il metodo "apply" del servizio CommandDispatcher, come nell'esempio seguente:

```ts
import { addCommands } from '@ca-webstack/ng-components';
...
protected add() {
  addCommands(this, {
    name: 'done', label: 'Done', iconClassName: 'architecture', handler: () => {
      this._toastService.pop({ title: 'Done', type: 'success' });
    }
  });
  this.commandDispatcher.apply();
}
...
```

Esiste un componente built-in del framework in grado di recuperare autonomamente tutti i comandi relativi ad un contesto, filtrandoli (o no) in funzione di una family e renderizzandoli mediante un template definito dall'utente con hash-key "commandsTemplate". Nell'esempio seguente il componente viene utilizzato filtrando i commands per la family "action" e renderizzandoli con una ShCaption:

```HTML
<sh-commands-bar family="action">
  <ng-template #commandsTemplate let-command="$implicit">
    <div>
      <sh-caption>{{command.label}}</sh-caption>
    </div>
  </ng-template>
 </sh-commands-bar>
```
[Live Demo](https://storybook.codearchitects.com/#/storybook/business/patterns/57ee7349-37ef-8a01-daeb-6ee92feda3ed/playground/$Commands)


### Shared Modules

In questa sezione vengono illustrati i moduli condivisi ed il modo con cui vengono caricati (lazy-initialization).
Il Lazy-Initialization è un design pattern creazionale che permette di istanziare un oggetto, una variabile, effettuare un calcolo od eseguire un processo, solo nel momento in cui tale operazione è realmente necessaria o richiesta.


La creazione di moduli condivisi consente di organizzare e modularizzare il codice. Un modulo condiviso non è altro che un semplicissimo modulo con all'intero direttive, pipe, componenti e moduli di uso comune, con lo scopo di essere importato in altri moduli per evitare sopratutto dichiarazioni e import ripetuti.

Consideriamo il seguente modulo esistente in una applicazione di esempio:
```ts
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ShComponentsModule } from '@ca-webstack/ng-components';
import { TranslateModule } from '@ngx-translate/core';
import { DxButtonModule } from 'devextreme-angular';
import { ButtonIconComponent } from './button-icon/button-icon.component';

@NgModule({
  declarations: [
    ...
    ButtonIconComponent,
    ...
  ],
  imports: [
    ...
    CommonModule,
    ShComponentsModule,
    TranslateModule,
    DxButtonModule,
    ...
  ],
  exports: [
    ShComponentsModule,
    ButtonIconComponent,
    TranslateModule,
    ...
  ]
})
export class SharedModule { }
```
Notiamo quanto segue:

- Tutti gli imports sono utilizzabili in tutti i files presenti nel modulo. Viene dunque importato CommonsModule (per utilizzare le direttive comuni di Angular), ShComponentsModule (per utilizzare le componenti del framework), TranslateModule (per utilizzare all'interno del modulo le features di internazionalizzazione), DxButtonModule (per utilizzare il componente Button della libreria DevExtreme)

- Tutte le declarations riguardano componenti e pipes presenti nel modulo, utilizzabili tra loro (es. dichiarando component x e component y, sarà possibile utilizzare x in y e viceversa). Viene dunque dichiarata la componente ButtonIconComponent per essere riconosciuta nei template html presenti nel modulo con il suo selettore (es. <app-button-icon></app-button-icon>)

- Eseguendo l'export di moduli, componenti, pipes e direttive, qualsiasi altro modulo che importerà il modulo SharedModule, avrà accesso a (e quindi potrà utilizzare) questi ultimi. Viene dunque esportato il modulo ShComponentsModule (per permettere di utilizzare le componenti del framework), ButtonIconComponent (per permettere di utilizzare la componente ButtonIconComponent) e TranslateModule (per permettere di utilizzare le features di internazionalizzazione)

Importando SharedModule in un altro modulo, sarà possibile dunque utilizzare tutti gli oggetti esportati dal modulo (exports).

```ts
@NgModule({
  ...
  imports: [
    ...
    SharedModule,
    ...
  ]
  ...
})
export class OtherModule { }
```

### Services

In questa sezione vengono illustrati i Servizi (che implementano il concetto di Singleton Pattern).
Il Singleton è un design pattern creazionale che ha lo scopo di assicurare che di una classe possa essere creata una sola istanza. Tutti gli oggetti che richiederanno successivamente una istanza della classe, avranno accesso all'istanza precedentemente creata.


Un servizio Singleton è dunque una classe per la quale esiste una sola istanza e che rappresenta un ottimo modo per condividere informazioni tra classi che non si conoscono. Per trasformare una classe in un servizio, è sufficiente applicarne il decoratore @Injectable.

```ts
import { Injectable } from '@angular/core';
@Injectable()
export class LoginService {
}
```

Il servizio, per risultare tale in uno specifico contesto applicativo, va inserito nell'array "providers" del relativo NgModule. Questa operazione permette di comunicare al motore di effettuare il provide del servizio nello specifico contesto identificato dal modulo.

```ts
@NgModule({
  ...
  providers: [LoginService],
  ...
})
```

Tuttavia la strada preferita per creare un servizio, è quella di comunicare al motore di effettuare il provide del servizio nell'application root, in modo tale da renderlo disponibile in tutta l'applicazione senza dover inserirlo in alcun modulo. Per ottenere questo risultato è sufficiente aggiungere la proprietà "providedIn" con valore "root" nell'applicazione del decoratore @Injectable sulla classe coinvolta, come nell'esempio seguente:

```ts
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
}
```

### Observables

In questa sezione vengono illustrate le features (offerte dal framework) che implementano il concetto dell'Observer Pattern.
L'Observer è un design pattern comportamentale che permette di definire una dipendenza uno a molti fra oggetti, in modo tale che se un oggetto cambia il suo stato interno, ciascuno degli oggetti dipendenti da esso viene notificato e aggiornato automaticamente. L’Observer nasce dall’esigenza di mantenere un alto livello di consistenza fra classi correlate, senza produrre situazioni di forte dipendenza e di accoppiamento elevato. Il pattern Observer trova applicazione nei casi in cui diversi oggetti (Observer) devono conoscere lo stato di un oggetto (Subject o Observable). In poche parole abbiamo un oggetto che viene "osservato" (il subject) e tanti oggetti che "osservano" i cambiamenti di quest’ultimo (gli observers).


Gli Observables o Subjects forniscono il supporto per il passaggio di messaggi tra publishers e subscribers all'interno di una applicazione. Gli observables offrono vantaggi significativi rispetto ad altre tecniche per la gestione degli eventi, la programmazione asincrona e la gestione valori multipli. Gli observables sono dichiarativi: permettono di definire una funzione (per pubblicare valori) che non viene eseguita fino a quando un consumer non si sottoscrive ad essa. Il consumer sottoscritto (subscriber), riceve quindi le notifiche fino al completamento della funzione o fino all'annullamento della sottoscrizione (unsubscribe). L'observer è in grado di fornire valori di qualsiasi tipo. L'API per la ricezione di valori resta sempre la stessa indipendentemente dal fatto che i valori vengano consegnati in modo sincrono o asincrono. Considerando che la logica di setup e teardown sono entrambe gestite dall'observable, il codice dell'applicazione deve solo preoccuparsi della sottoscrizione per consumare valori e, al termine eseguire l'unsubscribe. Indipendentemente dal fatto che il flusso sia rappresentato da una sequenza di tasti, una HTTP Response o altro, il contratto software resta lo stesso.

```ts
...
protected subject$ = new Subject<string>();
...
```
Un'istanza di un observable inizia ad emettere notifiche solo dal momento in cui qualcuno si sottoscrive ad esso (subscriber). Per sottoscriversi ad un observable, è sufficiente richiamare il metodo subscribe dell'istanza dello stesso, passando come parametro l'observer.
```ts
...
this.subject$
  .subscribe(e=> {
    console.log(e);
  })
...
```
Per notificare tutti i subscribers (emettendo anche valori, se previsti dall'observable), è sufficiente chiamare il metodo "next" dell'istanza del subject. Nell'esempio seguente, tutti i subscribers dell'observable event$ riceveranno una notifica con valore "new event!":

```ts
...
this.subject$.next('new event!');
...
```
La libreria utilizzata dal framework per implementare questo concetto, si chiama RxJS (Reactive Extensions Library for JavaScript).

[Per maggior dettagli sugli observables, visita la documentazione ufficiale di "Angular"](https://angular.io/guide/observables)
 

[Per maggior dettagli su RxJS, visita la sua documentazione ufficiale](https://rxjs-dev.firebaseapp.com/guide/overview)

 