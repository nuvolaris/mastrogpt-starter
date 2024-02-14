# Codegen

## Code Generation Tool

CodeGen è il potente tool di Code Architects che permette di generare in pochi secondi più del 70% del codice che il developer scriverebbe manualmente. Con questo tool è possibile generare con un approccio assolutamente intuitivo (sia lato client che lato server) interi scenari applicativi, entità isomorfiche, enumerati, servizi e molto altro, definendo le metainformazioni in maniera guidata all'interno di file di tipo YAML. In questa sezione viene analizzato nello specifico il DSL (Domain Specific Language) utilizzato per modellare le applicazioni sviluppate con il CA-Platform. La libreria di riferimento per il suddetto DSL è "@ca-codegen/ng-aspnetcore-spa" ed i modelli YAML vengono definiti nella folder "codegen\\model" del progetto, mentre i template custom nella folder "codegen\\templates".

![](./assets/resources/logo-codegen.png)

## YAML

YAML è un linguaggio di serializzazione dei dati human-readable. È comunemente usato per i file di configurazione. YAML ha una sintassi minimal che intenzionalmente differisce da XML. L'estensione dei file YAML è .yml. Utilizza sia l'indentazione in stile Python per indicare l'annidamento, sia un formato più compatto che usa \[ \] per gli array e { } per le mappe, rendendo YAML un superset di JSON. Sono consentiti tipi di dati custom, ma YAML codifica nativamente scalari (come stringhe, numeri interi e float), elenchi e array associativi. Questi tipi di dati si basano sui linguaggi di programmazione di alto livello. Per definire le coppie chiave-valore, la sintassi utilizzata è quella dei due punti. Il wrapping di spazi bianchi per stringhe a più righe è ispirato all'HTML. Gli elenchi possono contenere a loro volta altri elenchi nidificati che formano una struttura ad albero. Alcuni editor di codice sorgente come Visual Studio Code forniscono estensioni che rendono più semplice la modifica di YAML, come ripiegare strutture nidificate o evidenziare automaticamente errori di sintassi.

YAML accetta l 'intero set di caratteri Unicode, ad eccezione di alcuni caratteri di controllo, e può essere codificato in UTF-8, UTF-16 e UTF-32. Di seguito le caratteristiche principali:

- Whitespace indentation: usati per denotare le strutture. E' necessario che le indentazioni siano rigorosamente rispettate, pena errori di definizione.

  ```yaml
  entities:
    - name: Person
      type: entity
      description: Person entity
      isTrackable: false
      fields:
        - name: name
          type: string
          description: Customer name
          isKey: true
          isPublic: true
          variableAlias: nameAlias
          decorators:
            - type: aspect
              default:
                template: text
                label:
                  key: name
                  default: Nome
          validations:
            - type: mandatory
              message:
                key: field-mandatory
                default: Campo obbligatorio
            - type: custom
              name: containNumbers
              message:
                key: string\-no-num
                default: La stringa non contiene un numero
  ```

- Comment: i commenti iniziano con l'hash (#) e possono iniziare ovunque su una riga e continuare fino alla fine della stessa.

  ```yaml
  # This is a comment
  # This is another comment
  ```

- List: ciascun elemento di una lista è indicato da un trattino iniziale (-). È inoltre possibile specificare un elenco racchiudendo il testo tra parentesi quadre ([ ]) con ciascuna voce separata da virgole.

  ```yaml
  validations:
    - type: mandatory
      message:
        key: field-mandatory
        default: Campo obbligatorio
    - type: custom
      name: containNumbers
      message:
        key: string\-no-num
        default: La stringa non contiene un numero
  ```

- Object: la proprietà di un oggetto è rappresentata utilizzando l'associazione chiave-valore. Chiave e valore devono essere separate dai due punti (:). YAML richiede che i due punti siano seguiti da uno spazio in modo che i valori scalari possano generalmente essere rappresentati senza la necessità di essere racchiusi tra virgolette. Un oggetto può anche essere definito utilizzando le parentesi graffe ({ }), con le proprietà separate da virgole, i valori testuali tra virgolette, senza la necessità di inserire spazi ed indentazioni (per la compatibilità con JSON).

  ```yaml
  name: Person
  type: entity
  description: Person entity
  isTrackable: false
  ```

- String: le stringhe sono normalmente non quotate, ma possono essere racchiuse tra virgolette doppie (") o virgolette singole ('). Tra virgolette, i caratteri speciali possono essere rappresentati con sequenze di escape in stile C che iniziano con una backslash (\\).

  ```yaml
  description: This is a sample description
  ```

I file YAML supportati dal CA-Platform sono controllati e validati da uno schema JSON che "lavora" dietro le quinte. JSON Schema è una specifica per la strutturazione di dati basati su JSON. La compilazione dello YAML è dunque semplificata e guidata grazie allo schema JSON del repository @ca-codegen contenente i modelli e le definizioni dell'architettura. L'estensione di Visual Studio Code che permette l'abbinamento di uno schema a degli specifici file YAML è la seguente:

[YAML from Redhat](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)

Utilizzando Scarface per lo scaffold dell'applicazione, per usufruire dei vantaggi della compilazione guidata, sarà sufficiente installare l'estensione. Per maggior dettagli su Scarf-Ace, visita la sezione ["Scarface"](..\sdk\scarface.md).

Il CA-Platform supporta 4 tipologie di layer: application, domain, scenario e shared. E' possibile definire ciascun layer in file YAML distinguendoli utilizzando la proprietà "type". Le proprietà utilizzabili varieranno a seconda del type specificato. Installando la seguente estensione, sarà possibile lanciare automaticamente la generazione del codice ad ogni modifica effettuata su un file YAML:

[Trigger Task on save](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.triggertaskonsave)

## Service

Un'applicazione distribuita è tipicamente composta da vari microservizi che interagiscono tra loro, dividendosi le funzionalità esposte all'esterno del back-end. È possibile generare un intero microservizio a partire da un singolo file YAML che lo descrive. Questo file ha la seguente struttura:

```yaml
name: Customers
type: service
description: Customers service
namespace: Ca.Crm.Customers
generationMode: default
target: ...
port: 5000
useVersioning: true
version: 1
data: ...
identity: ...
messaging: ...
components: ...
entities: ...
contracts:
  operations: ...
  dto: ...
  services: ...
mappings: ...
partials: ...
services: ...
dependencies: ...
paths: ...
secrets: ...
actors: ...
associations: ...
```

Impostando "service" come "type" nel file YAML, sarà possibile utilizzare le seguenti proprietà:

**name:** Nome del microservizio. Deve essere una stringa in PascalCase, ovvero con la prima lettera maiuscola seguita da eventuali caratteri alfabetici (esempi: "Suite", "Users", "ModelBase"). Utilizzando Scarface per la generazione del layer, l'unico vincolo da ripettare sarà quello che il name richiesto dovrà adottare la sintassi kebab-case, ovvero stringa in lowercase con ogni parola separata da un trattino (esempi: "suite", "users", "model-base") ed il tool si occuperà di convertirlo in PascalCase come valore del name stesso (esempi: "Suite", "ModelBase"), ed in camelCase come nome del file YAML (esempi: "suite.yml", "modelBase.yml").

**type:** Tipologia di layer.

**description:** Descrizione del layer.

**namespace:** Namespace del microservizio. Deve essere un set di parole separate da punti. Esempio: "Prefix.Project.Service".

**generationMode:** Se valorizzato, imposta come generare il microservizio:

- default: metodo di generazione di default. Genera il microservizio in un unico progetto.
- split: genera il microservizio in 4 differenti progetti (progetto principale, Domain, Dto, Infrastructure).

[**target**:](#target) Specifica il framework utilizzato dal microservizio.

**port:** Specifica la porta utilizzata dal microservizio.

**useVersioning:** Se impostato a true (di default è false), il codice che verrà generato supporterà il versioning sui controller del servizio. Per maggiori dettagli sul versioning, visita la sezione "Versioning" della pagina "Operations". TODO:

**version:** Se `useVersioning` è impostato a true, indica la versione dei controller del microservizio. Per maggiori dettagli sul versioning, visita la sezione "Versioning" della pagina "Operations". TODO:

[**data**:](#data) Specifica l'ORM utilizzato dal microservizio.

[**messaging**:](#messaging) Descrive una lista dei messaggi che possono essere ricevuti dal microservizio e degli handlers che li gestiranno.

[**components**:](#components) Descrive una lista di componenti infrastrutturali utilizzati dal microservizio.

[**entities**:](#entities) Descrive le classi rappresentanti gli oggetti persistiti nel database (Persistent Objects).

[**contracts**:](#contracts) Contiene le definizioni dell'API e dei Consumer Driven Contracts esposti dal microservizio (procedure e DTO).

[**mappings**:](#mappings) Lista dei mapping tra entità di dominio e DTO.

[**partials**:](#partials) Contiene i riferimenti a file YAML parziali, che vanno ad aggiungersi alle informazioni modellate nello specifico YAML.

[**services**:](#services) Definisce la lista dei servizi che è possibile invocare dal servizio corrente, mediante service-to-service invocation. Per ogni servizio incluso, codegen genererà una classe con i metodi atti ad invocare i suoi metodi, che potranno essere consumati mediante Dependency Injection della relativa interfaccia (anch'essa generata).

[**dependencies**:](#dependencies) Permette di generare dei business service all'interno del microservizio.

[**paths**:](#paths) Permette di modificare i percorsi di generazione di default dei building blocks (entities, dto, repositories, etc...) del microservizio.

[**secrets**:](#secrets) Permette di aggiungere il supporto ai secrets utilizzando il provider specificato.

[**actors**:](#actors) Consente di attivare il paradigma Actor Model per la creazione di sistemi distribuiti e concorrenti. Disponibile solo da .NET 6 in poi.

[**associations**:](#associations) Definisce eventuali tipi di associazioni tra diverse entità. Per maggiori dettagli sulle associations, visita la sezione "Associations" della pagina "DAL".

## Application

L'application layer rappresenta il container principale dell'applicazione. L'applicazione è costituita/descritta da domini applicativi. Le meta-informazioni dell'applicazione devono essere definite in un file YAML con il nome dell'applicazione in camelCase (applicationName.yml) nella folder model contenuta in codegen. Utilizzando Scarface non sarà necesario ricordare la posizione e la naming convention del file YAML dell'applicazione, ma basterà rispondere al prompt di Scarface con il nome dell'applicazione in kebab-case (application-name). Nell'esempio seguente viene definito lo YAML di una applicazione chiamata Suite:

```yaml
name: Suite
type: application
author: CodeArchitects
namspace: Prefix.ProjectName
rootNamespace: Prefix.ProjectName.Containers
modelNamespace: Prefix.ProjectName.Model
description: The registry management system application
baseApiUrl: ca/suite
services: ...
```

Impostando "application" come "type" nel file YAML, sarà possibile utilizzare le seguenti proprietà:

**name:** Nome del layer. Deve essere una stringa in PascalCase, ovvero con la prima lettera maiuscola seguita da eventuali caratteri alfabetici (esempi: "Suite", "Users", "ModelBase"). Utilizzando Scarface per la generazione del layer, l'unico vincolo da ripettare sarà quello che il name richiesto dovrà adottare la sintassi kebab-case, ovvero stringa in lowercase con ogni parola separata da un trattino (esempi: "suite", "users", "model-base") ed il tool si occuperà di convertirlo in PascalCase come valore del name stesso (esempi: "Suite", "ModelBase"), ed in camelCase come nome del file YAML (esempi: "suite.yml", "modelBase.yml").

**type:** Tipologia di layer.

**author:** Nome dell'autore del progetto. Deve essere una stringa con la prima lettera maiuscola seguita da eventuali caratteri alfanumerici. Esempi: "Bross", "Bross31".

**namespace:** Namespace dell'applicazione. Deve essere un set di parole separate da punti. Esempio: "Prefix.Project".

**description:** Descrizione del layer.

**baseApiUrl:** **_[DEPRECATED]_**

[**services**:](#services) Lista dei microservizi che è possibile interrogare da tutti i livelli dell'applicazione (tutti i domini e tutti gli scenari).

## Domain

Il domain layer rappresenta il container più prossimo all'application layer e delinea uno specifico contesto applicativo, ovvero un particolare contesto in cui l'applicazione opera. Ogni dominio è rappresentato dagli scenari. Le meta-informazioni del dominio devono essere definite in un file YAML con il nome del dominio in camelCase preceduto dal nome dell'applicazione di riferimento sempre in camelCase e separati da un trattino (applicationName-domainName.yml) nella folder model contenuta in codegen. Utilizzando Scarface non sarà necesario ricordare la posizione e la naming convention del file YAML del dominio, ma basterà rispondere al prompt di Scarface con il nome del dominio in kebab-case (domain-name) e scegliendo da una lista l'applicazione di riferimento. Nell'esempio seguente viene definito lo YAML di un dominio dell'applicazione Suite chiamato Crm:

```yaml
name: Crm
type: domain
description: Customer relationship management domain
application: Suite
namespace: Prefix.ProjectName.Domain
services: ...
```

Impostando "domain" come "type" nel file YAML, sarà possibile utilizzare le seguenti proprietà:

**name:** Nome del layer. Deve essere una stringa in PascalCase, ovvero con la prima lettera maiuscola seguita da eventuali caratteri alfabetici (esempi: 'Suite', 'Users', 'ModelBase'). Utilizzando Scarface per la generazione del layer, l'unico vincolo da ripettare sarà quello che il name richiesto dovrà adottare la sintassi kebab-case, ovvero stringa in lowercase con ogni parola separata da un trattino (esempi: 'suite', 'users', 'model-base') ed il tool si occuperà di convertirlo in PascalCase come valore del name stesso (esempi: 'Suite', 'ModelBase'), ed in camelCase come nome del file YAML (esempi: 'suite.yml', 'modelBase.yml').

**type:** Tipologia di layer.

**description:** Descrizione del layer.

**application:** Riferimento all'applicazione di appartenenza (name specificato nello YAML dell'applicazione).

**namespace:** Namespace del dominio. Deve essere un set di parole separate da punti. Esempio: "Prefix.Project.Domain".

[**services**:](#services) Lista dei microservizi che è possibile interrogare dallo specifico dominio e da tutti i suoi scenari

## Scenario

Lo scenario layer rappresenta il container più atomico dell'applicazione e descrive un particolare contesto applicativo legato ad uno specifico dominio (esempio: scenario: anagrafica-persona -> dominio: anagrafiche). A ciascun scenario è legata una Activity di Workflow (navigazionale). Si tratta (nello specifico) di una macchina a stati costituita da stati/nodi rappresentanti le viste dello scenario effettivamente navigabili. Il caricamento di uno scenario corrisponderà all'avvio di un task (identificato da un GUID assegnato dinamicamente) che terminerà solamente al verificarsi di navigazioni assolute (routerLink o router service) \[vedi paragrafo Navigation per maggiori dettagli\]. Le meta-informazioni dello scenario devono essere definite in un file YAML con il nome dello scenario in camelCase preceduto dal nome del dominio di appartenenza in camelCase, a sua volta preceduto dal nome dell'applicazione di riferimento sempre in camelCase e separati da un trattino (applicatioName-domainName-scenarioName.yml) nella folder model contenuta in codegen. Utilizzando Scarface non sarà necesario ricordare la posizione e la naming convention del file YAML dello scenario, ma basterà rispondere al prompt di Scarface con il nome dello scenario in kebab-case (scenario-name) e scegliendo da una lista l'applicazione ed il dominio di riferimento. Nell'esempio seguente viene definito lo YAML di uno scenario Customers appartenente al dominio Crm dell'applicazione Suite:

```yaml
name: Customers
type: task
description: Customers scenario
domain: Crm
namespace: Prefix.ProjectName.Crm.Scenario
activity: CustomersActivity
services: ...
payloads: ...
```

Impostando "task" come "type" nel file YAML, sarà possibile utilizzare le seguenti proprietà:

**name:** Nome del layer. Deve essere una stringa in PascalCase, ovvero con la prima lettera maiuscola seguita da eventuali caratteri alfabetici (esempi: "Suite", "Users", "ModelBase"). Utilizzando Scarface per la generazione del layer, l'unico vincolo da ripettare sarà quello che il name richiesto dovrà adottare la sintassi kebab-case, ovvero stringa in lowercase con ogni parola separata da un trattino (esempi: "suite", "users", "model-base") ed il tool si occuperà di convertirlo in PascalCase come valore del name stesso (esempi: "Suite", "ModelBase"), ed in camelCase come nome del file YAML (esempi: "suite.yml", "modelBase.yml").

**type:** Tipologia di layer.

**domain:** Riferimento al dominio di appartenenza (`name` specificato nello YAML del dominio).

**description:** Descrizione del layer.

**namespace:** Namespace dello scenario. Deve essere un set di parole separate da punti. Esempio: "Prefix.Project.Domain.Scenario".

[**activity**:](#activity) Riferimento all'activity del workflow dello scenario (definita nel file NOMNOML abbinato "scenario-repo.nomnoml").

[**services**:](#services) Lista dei microservizi che è possibile interrogare dallo specifico dominio e da tutti i suoi scenari.

[**payloads:**](#payloads) Lista dei payloads dello scenario corrente.

## Gateway

L'application Gateway è un servizio di bilanciamento del carico del traffico Web che consente di gestire il traffico verso i microservizi. Il gateway consente di prendere decisioni relative al routing basate su altri attributi di una richiesta HTTP, ad esempio il percorso dell'URI o le intestazioni host. Ad esempio, è possibile eseguire il rounting del traffico in base all'URL in ingresso. Lo YAML di tipo gateway permette di generare un application gateway con [ENVOY](https://www.envoyproxy.io/) e di aggiungerne/rimuoverne dinamicamente i microservizi.

```yaml
name: SPA
type: gateway
description: SPA gateway
port: 10000
proxy: ...
services: ...
```

**name:** Nome del gateway.

**type:** Tipologia di layer.

**description:** Descrizione del layer.

**port:** Porta locale sulla quale lanciare il gateway.

**proxy:** Tipo di proxy utilizzato dal gateway. I proxy attualmente supportati sono:

- **envoy:** Proxy Envoy.
- **nginx:** Procy Nginx.

[**services**:](#services) Lista dei microservizi esposti sul gateway.

## NOMNOML

NOMNOML è un tool per disegnare diagrammi UML basati su una semplice sintassi. Nella platform permette di definire gli stati del workflow navigazionale di uno scenario e le relative transizioni.

```nomnoml
[<activity>CustomersActivity|
  [<start>start]
  [<state>browse]
  [<state>add]
  [<state>update]

  [start] browse -> [browse]
  [browse] add -> [add]
  [browse] update -> [update]
  [browse] foo -> [update]
]
```

Utilizzando Scarface (per la generazione dello scenario e degli stati) non sarà necessaria la modifica dei file NOMNOML. E' tuttavia possibile editare questi tipi di file rispettando la seguente sintassi:

- La definizione dell'activity (stati ed associazioni) deve avvenire all'interno di parentesi quadre [...].
- La prima informazione da inserire tra le parentesi quadre è il nome dell'activity dello scenario (in PascalCase) preceduta dall'attributo `<activity>` ed seguita da una pipe "|". Il nome assegnato all'activity deve essere univoco in tutto il progetto (non devono esserci altri file NOMNOML che definiscano una activity con lo stesso nome).
- Tra gli stati dello scenario ce ne deve essere sempre uno di partenza: lo stato start. Tale stato deve essere preceduto dall'attributo `<start>` e rappresenta il nodo di partenza del workflow navigazionale. Quando si avvia un nuovo task tramite navigazione assoluta (es. routerLink: ["suite","crm", "customers"]), si dovrà obbligatoriamente passare dal nodo start; quando invece si effettua una navigazione relativa (es. this.navigateWithReturn(...)) non bisognerà passarci.
- Tutti gli altri stati del workflow devono essere preceduti dall'attributo `<state>`.
  - A ciascuno stato (incluso start) sarà legata una componente adornata con il decoratore `@ActivityComponent`. Con l'applicazione di questo decorator, la classe non sarà più una semplice componente, ma sarà una componente legata ad una specifica activity. Per maggior dettagli sul decoratore [@ActivityComponent, visita la sezione "Patterns"](.\Patterns.md);
- Con la sintassi "[x] action -> [y]" si definisce una transizione tra due stati dello stesso scenario, dove "x" rappresenta lo stato di partenza, "y" lo stato di arrivo ed "action" il nome del nuovo command da eseguire nello stato "x" per navigare verso lo stato "y".

La generazione dell'activity definita all'interno del file NOMNOML, produrrà una componente per ciascuno stato, come nell'esempio seguente (scenario: agenda, stati: start, browse):

![](./assets/resources/activity-folder.PNG)

Ciascuno stato sarà composto da un file html, un file scss, un file ts ed un file spec.ts. Nel file html andrà inserito il template legato allo stato, mentre nel file ts la logica dello stesso. Il file typescript sarà simile al seguente (esempio con lo stato browse):

```ts
@ActivityComponent({ extends: Base.BrowseComponent })
@Component({ templateUrl: 'browse.html', providers: [Base.AgendaServices] })
export class BrowseComponent extends Base.BrowseComponent implements IOnInit {
  public constructor(injector: Injector, services: Base.AgendaServices) {
    super(injector, services);
  }

  public async onInit(params: {}) {}
}
```

Il file \*.spec.ts conterrà gli hook per effettuare i test unitari sul relativo componente/stato dello scenario. Il file sarà già incluso nella suite di test applicativa, prevederà già la configurazione del modulo di testing e sarà simile al seguente (esempio con lo stato browse):

```ts
// --inject:IMPORTS--
describe('Suite/Crm/Customers/browse action', () => {
  let component: BrowseComponent;
  let fixture: ComponentFixture<BrowseComponent>;
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        // --inject:TESTIMPORTS--
        ComponentsModule,
        HttpClientModule,
        RouterTestingModule,
        TranslateModule.forRoot()
        // --inject:TESTIMPORTS--
      ],
      declarations: [
        // --inject:TESTDECLARATIONS--
        // --inject:TESTDECLARATIONS--
        BrowseComponent
      ],
      providers: [
        // --inject:TESTPROVIDERS--
        CommandDispatcherService,
        ContextService,
        DataContextService,
        SerializerService,
        { provide: ShHttp, useClass: ShAuthHttp },
        // --inject:TESTPROVIDERS--
        InvoicesActivity,
        InvoicesDelegates
      ]
    }).compileComponents();
  }));
  beforeEach(() => {
    // --inject:BEFOREACH-BEGIN--
    fixture = TestBed.createComponent(BrowseComponent);
    component = fixture.componentInstance;
    // --inject:BEFOREACH-BEGIN--
    component.activity.payload = <CustomersPayload>{};
    component.delegates.getUniqueIdentifier = () => {
      const subject = new Subject<string>();
      setTimeout(() => subject.next('8aca28c1-9754-446e-8930-92cb3d66be66'), 100);
      return subject;
    };
    component.onInit = () => {};
    component.onInit({});
    fixture.detectChanges();
    // --inject:BEFOREACH-END--
    // --inject:BEFOREACH-END--
  });
  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
```

Il file \*.scss potrà contenere lo stile incapsulato per il componente/stato ad esso associato. Sconsigliamo l'utilizzo di questi file per evitare di avere uno stile differente per ciascuna pagina dell'applicazione. Consigliamo invece l'utilizzo di componenti con stile già definito (come la libreria di componenti del CA Platform), in modo tale da limitarsi a montare le interfacce con i componenti messi a disposizione invece di scriverne ogni volta lo stile. E' tuttavia possibile utilizzare questo file, legandone lo style nell'attributo `styleUrls` del decoratore `Component`, come di seguito (esempio con lo stato browse):

```scss
@ActivityComponent({ extends: Base.BrowseComponent })
@Component({ templateUrl: 'browse.html', providers: [Base.InvoicesServices], styleUrls: ['./browse.scss'] })
export class BrowseComponent extends Base.BrowseComponent implements IOnInit {
```

## Services Inclusion

La proprietà "services" permette di importare (all'interno del container nel quale è applicato) tutte le informazioni definite in un container di tipo "service". Importando un service in un container di tipo "application", "domain", "scenario" o "task", il generatore di codice genererà i DTO nel file "nome-servizio.ts" della cartella models (del container stesso) e i metodi delegati nel file "nome-servizio_service.ts" della cartella services (del container) e sarà dunque possibile accedere ai metodi proxy generati tramite il servizio delegates (`this.delegates.nomeServizio.nomeMetodo`). Importando un service in un container di tipo "gateway", quest'ultimo verrà esposto sull'application gateway.

```yaml
services:
  - service: Store
  - service: Logistics
  - ...
```

**service:** Nome identificativo del container di tipo 'service' da importare.

## Paths

Questa sezione permette di modificare i percorsi di generazione di default dei building blocks (entities, dto, repositories, etc...) del microservizio. Al suo interno è possibile indicare il building block di cui si vuole sovrascrivere il percorso, specificandone le seguenti proprietà:

**path:** Indica il percorso dei file da generare, relativo alla root folder del server.

**projectNamespace:** Indica il namespace del progetto in cui generare.

**namespace:** Indica, all'interno del progetto, in quale cartella deve essere generato il codice.

Ciascun building block può presentare direttamente le 3 proprietà di cui sopra, oppure può indicare altri sottolivelli (ad esempio la voce "repositories", presenta le sottovoci "declarations" e "definitions", che indicano rispettivamente le impostazioni di generazione dei contratti software dei repository e le classi concrete di questi ultimi).

```yaml
paths:
  serviceInvocations:
    declarations:
      namespace: Declaration
      projectNamespace: Ca.Remote
      path: Ca.Remote
    definitions:
      namespace: Definitions
      projectNamespace: Ca.Remote
      path: Ca.Remote
  entities:
    domainEntities:
      namespace: Entities.Domain.Model
      path: App.Segregation.Ent
      projectNamespace: App.Segregation.Ent
    tableEntities:
      namespace: Entities.Domain.Model.Table
      path: App.Segregation.Ent
      projectNamespace: App.Segregation.Ent
  dto:
    namespace: Dto
    path: Ca.Segregation.Model
    projectNamespace: Ca.Segregation.Model
  dependencies:
    namespace: ''
    path: Ca.Common.Services
    projectNamespace: Ca.Common.Services
  repositories:
    declarations:
      namespace: Common.Interfaces.Repositories
      path: App.Segregation.Common/src
      projectNamespace: App.Segregation.Common
    definitions:
      namespace: ''
      path: App.Segregation.Repo
      projectNamespace: App.Segregation.Repo
  data:
    namespace: Storage.Databases
    projectNamespace: App.Segregation.Data
    path: App.Segregation.Data
  operations:
    namespace: Controller
    path: App.Segregation.API
    projectNamespace: App.Segregation.API
  graphQL:
    query:
      namespace: Queries
      path: Ca.Queries
      projectNamespace: Ca.Queries
    type:
      namespace: Types
      path: Ca.Queries
      projectNamespace: Ca.Queries
    entityBase:
      namespace: ''
      path: Ca.Queries
      projectNamespace: Ca.Queries
  hubs:
    namespace: SignalR
    path: App.Communication
    projectNamespace: App.Communication
  messaging:
    messages:
      namespace: Msg
      path: App.Communication
      projectNamespace: App.Communication
    handlers:
      namespace: Infrastructure.Handler
      path: Ca.Gestione
      projectNamespace: Ca.Gestione
  services:
    - name: Shipment
      dto:
        namespace: Dto
        path: Ca.Segregation.Model
        projectNamespace: Ca.Segregation.Model
      hubs:
        namespace: SignalR
        path: App.Communication
        projectNamespace: App.Communication
      operations:
        namespace: Controller
        path: App.Segregation.API
        projectNamespace: App.Segregation.API
```

## Target

Questa sezione dello yaml configura il framework utilizzato dal microservizio, utilizzando le seguenti proprietà:

**framework:** Indica il tipo di framework da utilizzare per il microservizio. I framework attualmente supportati sono:

- **net:** .NET.

**version:** Indica la versione del framework specificato. Le versioni attualmente supportate sono:

- **5:** .NET 5;
- **6:** .NET 6;
- **7:** .NET 7.

```yml
target:
  version: 7
  framework: net
```

## Port

Questa sezione viene utilizzata per associare manualmente una specifica porta ad un microservizio. Se non venisse specificata, la porta verrà scelta automaticamente. In particolare, la numerazione della porta inizia da 62760 (HTTP) e 62761 (HTTPS). I successivi microservizi creati senza una porta specificata manualmente avranno una numerazione pari alla porta del microservizio precedente + 2 (62762 e 62763 e così via).