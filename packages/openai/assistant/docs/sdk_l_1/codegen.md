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

## Data

Questa sezione viene utilizzata per indicare il tipo di ORM (Object Relational Mapping) utilizzato dal microservizio, insieme al supporto per la multitenancy, utilizzando le seguenti proprietà:

**orm:** È possibile specificare l'ORM desiderato per il microservizio. Gli ORM attualmente supportati sono:

- **EntityFrameworkCore:** [Entity Framework Core](https://learn.microsoft.com/en-us/ef/core/);
- **Dapper:** [Dapper](https://github.com/DapperLib/Dapper).

**multitenancy:** Se specificato a true (di default è false), aggiunge la segregazione per tenant all'interno delle entità persistite nel database. Per maggiori dettagli sulla multitenancy, visita la sezione [multitenancy](#multitenancy).

```yml
data:
  orm: EntityFrameworkCore
  multitenancy: true
```

## Identity

Questa sezione consente di configurare l'identity profile all'interno di un microservizio. In questo modo sarà possibile utilizzare una rappresentazione fortemente tipizzata dei claims associati ad un utente autenticato. L'identity profile è utilizzabile dopo aver configurato il metodo "AddAuthentication" di ASP.NET Core, la cui documentazione è disponibile [qui](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/?view=aspnetcore-7.0). La sezione di identity contiene:

**claims:** Lista dei claims, ciascuno caratterizzato da:

- **name**: Nome del claim, ovvero della proprietà.
- **type**: Tipo del claim.
- **key**: Chiave del claim utilizzata nella serializzazione.
- **isOptional**: Specifica se il claim è opzionale o meno.

**userId:** Specifica il tipo del claim "UserId". Di default è "Guid".

```yml
identity:
  claims:
    - name: name
      type: string
      key: name
      isOptional: true
    - name: surname
      type: string
      key: surname
      isOptional: false
  userId:
    type: string
```

Questa sezione genererà l'interfaccia, che eredita `IIdentityProfile<Guid>`, contenente i claims specificati:

```cs
public interface IApplicationIdentityProfile : IIdentityProfile<Guid>
{
    string? Name { get; }
    string Surname { get; }
}
```

Sarà possibile accedere ad essi, come proprietà, tramite la classe `ApplicationClaimsIdentityProfile`:

```cs
public class ApplicationClaimsIdentityProfile : ClaimsIdentityProfile<Guid>, IApplicationIdentityProfile
{
    public ApplicationClaimsIdentityProfile(IHttpContextAccessor httpContextAccessor)
        : base(httpContextAccessor)
    {
    }

    public string? Name => ...;
    public string Surname => ...;
}
```

Il servizio verrà registrato nel container di IoC e sarà possibile richiedere un'istanza dell'interfaccia `IApplicationIdentityProfile` normalmente tramite Dependency Injection.

## Multitenancy

La multitenancy è configurabile dopo aver impostato [l'identity profile](#identity) all'interno del microservizio. Dopo averla abilitata, impostando a `true` l'omonima opzione della sezione "data", è possibile specificare l'opzione "tenantId" all'interno della sezione "identity". Al suo interno si può opzionalmente indicare anche il tipo della chiave, che di default è "Guid".

```yaml
identity:
  claims: ...
  userId: ...
  tenantId:
    key: http://schemas.microsoft.com/identity/claims/tenantid
```

L'indentity profile precedentemente generato diventerà:

```yaml
public interface IApplicationIdentityProfile : IIdentityProfile<string>, ITenantIdProfile<Guid>
{
    string GivenName { get; }
}

public class ApplicationClaimsIdentityProfile : ClaimsIdentityProfile<string>, IApplicationIdentityProfile
{
    public ApplicationClaimsIdentityProfile(IHttpContextAccessor httpContextAccessor)
        : base(httpContextAccessor)
    {
    }

    public string GivenName => ...;

    public Guid TenantId => ...;
}
```

Per tutte le entità per la quale si desidera la segregazione per tenant è necessario aggiungere la proprietà `isTenantEntity: true` e, successivamente, lanciare una migrazione:

```yaml
entities:
  - name: Customer
    description: Customer Entity
    useRepository: true
    isTenantEntity: true
    fields: ...
```

Tutte le query che coinvolgeranno queste entità saranno caratterizzate da un filtro che utilizzerà il valore del tenant id dell'utente che effettua la richiesta. È possibile, tuttavia, disabilitare il filtro puntualmente (a livello della singola query) utilizzando il metodo di estensione "AsNoMultitenancy()" di "IQuerable\<T\>":

```cs
var bobCustomers = context.Set<Customer>()
  .AsNoMultitenancy()
  .Where(name => name == "Bob")
  .ToList();
```

## Messaging

Questa sezione configura la funzione di messaging (pub/sub) del microservizio. Qui, viene indicata la lista dei messaggi che possono essere ricevuti dal microservizio e gli handlers che li gestiranno:

```yaml
messaging:
  handlers:
    - name: MyMessageHandler
      description: Handler of MyMessage1 and MyMessage2
      messages:
        - name: MyMessage1
        - name: MyMessage2
          result:
            - PingMessage
      metadata:
        topic: MyTopic
        bus: MyBus
  messages:
    - name: MyMessage1
      description: My message 1
      fields:
        - name: id
          description: The id of the message
          type: uuid
        - name: name
          description: The name of the message
          type: string
    - name: MyMessage2
      description: My message 2
      fields:
        - name: id
          description: The id of the message
          type: uuid
        - name: name
          description: The name of the message
          type: string
```

I messaggi (MyMessage1, MyMessage2) dovranno esistere anche in altri microservizi che provvederanno a pubblicarli, così che il message broker possa inoltrarli al microservizio di cui questo YAML fa parte.

## Components

Questa sezione dello YAML contiene la lista dei componenti dell'infrastruttura (ad esempio: database, messagebus, ecc.) utilizzati dal microservizio. Ciascun componente deve avere un tipo, un nome ed un provider. Il provider è l'implementazione scelta del tipo di componente (ad esempio: Sql Server come database, RabbitMQ come message broker, ecc.). Al momento, sono supportati 3 diversi tipi di components:

**database:** Descrive il database utilizzato dal microservizio. Includendo un component di tipo "database", verrà creato un container docker contenente un'istanza del database scelto, insieme ad un volume che ospiterà i suoi dati per persisterli su disco.

```yaml
components:
  - name: sqlserver
    type: database
    provider: sqlserver
```

I provider per il tipo "database" attualmente supportati sono:

- **sqlserver:** SQL Server;
- **postgres:** Postgres Server;
- **oracle:** Oracle Server.

**messagebus:** Descrive il message bus utilizzato dal microservizio. Includendo un component di tipo "messagebus", verrà creato un container docker contenente un'istanza del message broker scelto.

```yaml
components:
  - name: rabbit
    type: messagebus
    provider: rabbitmq
```

I provider per il tipo "messagebus" attualmente supportati sono:

- **rabbit:** RabbitMQ;
- **redis:** Redis Streams.

**statestore:** Descrive lo state store utilizzato dal microservizio. Includendo un component di tipo "statestore", verrà creato un container docker contenente un'istanza dello state store scelto.

```yaml
components:
  - name: redis
    type: statestore
    provider: redis
```

I provider per il tipo "statestore" attualmente supportati sono:

- **redis:** Redis.

## Contracts

Contiene le definizioni dell'API e dei Consumer Driven Contracts esposti dal microservizio (procedure e DTO).

```yaml
contracts:
  operations: ...
  dto: ...
  services:
    - name: MyController
      description: Custom controller
      operations: ...
      dto: ...
```

[**operations**:](#operations) Definisce la lista di actions del controller del microservizio.

[**dto**:](#dto) Definisce la lista dei DTOs (Data Transfer Objects) utilizzati all'interno delle operations.

**services:** Definisce una lista di controller, composti da dto ed operations:

- **name:** Nome del controller (in PascalCase);
- **description:** Descrizione del controller;
- **operations:** Lista di operazioni esposte dal controller del microservizio;
- **dto:** Lista dei DTOs utilizzati all'interno delle operations del controller.

## DTO

La proprietà "dto" permette di definire una lista di DTO (Data Transfer Object) e/o una lista di enumerati relativi al microservizio.

```yml
dto:
  - name: Person
    type: entity
    description: Person entity
    isTrackable: true
    isAbstract: true
    authPolicies: true
  - name: Customer
    type: entity
    description: Customer entity
    authPolicies:
      - Policy1
      - Policy2
    ancestor: Person
    disableMappingTestGeneration: true
    enableGetVariablesGeneration: true
    resource: class://Crm/Customers
    fields: ...
    validations: ...
    warnings: ...
  - name: JobState
    type: enum
    description: Customer job state
    generationMode: client
    position: 0
    enumeratorList:
      - name: Started
        description: Job started
      - name: Fired
        description: Job fired
        value: 0
```

Le classi generate lato Typescript e lato C# saranno isomorfiche. Trasferendole da client a server e viceversa attraverso le operations, i DTO manterranno la loro identità e non sarà necessario effettuare alcuna operazione di conversione. Ciascun DTO potrà essere composto dalle seguenti proprietà:

**name:** Nome del DTO. Il nome deve rispettare la notazione PascalCase (NomeCampo).

**type:** Tipologia di oggetto (entity o enum).

**description:** Descrizione del DTO.

**isTrackable:** Se impostato a true, tale impostazione renderà il DTO Trackable abilitandone il [Change Tracking](#changetracking).

**isAbstract:** Se impostato a true, rende la classe astratta.

**authPolicies:** Applica policy autorizzative sul metodo del controller. Può assumere i seguenti valori:

- **Booleano:** Se true, applica l'attributo [Authorize] sul metodo del controller;
- **Lista di stringhe:** Applica tale lista come "Policy" nell'attributo [Authorize] del metodo del controller.

**ancestor:** Con questa proprietà è possibile impostare come classe padre una delle classi definite nello stesso file YAML (ancestor: NomeClasse).

**disableMappingTestGeneration:** Se impostato a true, disabilita la generazione dei test unitari del mapping per il DTO in questione.

**enableGetVariablesGeneration:** Se impostato a true, crea un metodo a livello di classe che restituisce un dizionario in cui la chiave è il nome della proprietà della classe ed il valore è il valore della proprietà stessa.

**resource:** Resource name da associare alla classe. [Per maggior dettagli sulle resource, policy e claims, visita la sezione "Authorization"](.\authorization.md).

[**fields**:](#fields) Lista di proprietà della classe (concetto approfondito nel paragrafo successivo "DTO Fields").

**generationMode:** Se valorizzato imposta come generare il DTO:

- **client:** Genera il DTO solo lato client.
- **server:** Genera il DTO solo lato server.

**position:** gRPC position, da valorizzare solo quando si utilizza il DTO in una operation di tipo gRPC. Valore del parametro del messaggio (0,1,2,...).

[**enumeratorList**:](#enumeratorList) Proprietà presente solo con `type: enum`. Permette di definire la lista dei valori dell'enumerato, fornendo un nome in PascalCase ed un eventuale value.

[**validations**:](#validations) Lista di regole di validazione da applicare alla classe (concetto approfondito nel paragrafo successivo "DTO Fields").

[**warnings**:](#warnings) Lista di regole di warnings da applicare alla classe (concetto approfondito nel paragrafo successivo "DTO Fields").

## DTO Fields

La proprietà "fields" di una classe (proprietà "dto") permette di definire la lista delle proprietà che definiscono le caratteristiche di un DTO.

```yml
dto:
- name: Customer
  ...
  fields:
  - name: code
    type: numeric
    description: Codice readonly
    isNullable: true
    isReadOnly: true
    annotations: ...
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
          key: string-no-num
          default: La stringa non contiene un numero
  - name: email
    type: string
    description: Customer email
    decorators:
      - type: aspect
        default:
          template: textarea
          label: Email
    validations:
      - type: pattern
        pattern: ^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$
        message: Mail format error
    warnings:
      - type: mandatory
        message: It's advisable to populate the field
  - name: manager
    type: Customer
    description: Customer Work Manager
  - name: myDictionary
    type: dictionary
    description: myDictionary dictionary
  - name: myCustomDictionary
    type: dictionary
    description: myCustomDictionary dictionary
    dictionaryOptions:
      key: integer
      value: integer
```

**NOTE IMPORTANTI: Ciascun DTO eredita implicitamente tutte le caratteristiche della classe EntityDTO del platform. Tale classe, fornisce tra le proprietà una proprietà id (id lato typescript, Id lato C#) di formato Guid (string lato typescript, System.Guid lato C#). E' imporante dunque non definire nuove proprietà con il nome "id" all'interno delle classi e tenerne conto nei mapping (lato C#, mappando l'eventuale proprietà equivalente dell'entità del DB o inizializzando la proprietà almeno con un nuovo Guid) e nelle inizializzazioni (lato Typescript, utilizzando UUID.UUID()). La proprietà "id" (come indicato poco più sopra), è implicitamente impostata come chiave primaria (isKey: true) della classe; questo (per l'Object Identity, che il platform applica automaticamente) permette di distinguere una istanza della classe descritta da un'altra istanza. Se dunque, due istanze della stessa classe avranno lo stesso id, faranno riferimento alla medesima istanza. Tra gli errori più comuni nell'utilizzo del CA-Platform, c'è quella di ricevere sul client istanze di una medesima classe con lo stesso guid (generalmente guid empty) e vederle come identiche. E' importante dunque avere sempre chiavi differenti per le stesse istanze.**

**name:** Nome della proprietà della classe. Il nome deve rispettare la notazione camelCase (nomeCampo).

**type:** Tipologia della proprietà. Può essere scelto dalla lista dei suggerimenti o può essere identificata in una entità definita nello stesso YAML. La lista dei suggerimenti invece, presenta dei "tipi" rappresentanti una sorta di astrazione rispetto al linguaggio nel quale vengono generati. Di seguito tutti i tipi:

- **boolean:** Boolean (C#) - boolean (Typescript)
- **byte:** System.Byte (C#) - number (Typescript)
- **date:** DateTime? (C#) - Date (Typescript)
- **datetime:** DateTime? (C#) - DateTime (Typescript)
- **dateonly:** DateOnly? (C#) - DateOnly (Typescript)
- **decimal:** decimal (C#) - number (Typescript)
- **float:** float (C#) - number (Typescript)
- **integer:** Int32 (C#) - number (Typescript)
- **numeric:** Double (C#) - number (Typescript)
- **sequence:** Int64 (C#) - number (Typescript)
- **string:** String (C#) - string (Typescript)
- **time:** DateTime? (C#) - Date (Typescript)
- **uint8array:** System.Byte[] (C#) - Uint8Array (Typescript)
- **uuid:** System.Guid (C#) - string (Typescript)
- **short:** short (C#) - number (Typescript)
- **any:** System.Object (C#) - any (Typescript)
- **dictionary:** Dictionary<string, object> (C#) - Map<string, any> (Typescript)

**description:** Descrizione del field.

**isArray:** Se impostato a true, rende la proprietà una lista della tipologia indicata nel campo "type".

**isAbstract:** Se impostato a true, rende la proprietà astratta.

**isStatic:** Se impostato a true, rende la proprietà statica.

**isNullable:** **_[DEPRECATED]_** - Usare la proprietà isOptional.

**isOptional:** Se impostato a true, rende il campo nullable lato C#.

**isReadOnly:** Se impostato a true, rende il campo readonly, rimuovendo i relativi setter lato C# e lato Typescript.

**isKey:** Se impostato a true, rende il campo chiave primaria (insieme alle altre key). Questa proprietà permette di applicare i concetti dell'Object Identity alla classe, rendendo esattamente identici gli oggetti che avranno lo stesso valore della proprietà impostata come key.

**isPublic:** Se impostato a false, rende il campo private.

**resource:** Nome della risorsa da associare al field. [Per maggior dettagli sulle resource, policy e claims, visita la sezione "Authorization"](.\authorization.md).

**variableAlias:** **_[OBSOLETE]_**

**position:** Indica la posizionte gRPC.

**dictionaryOptions:** Permette di modificare chiave e valore del dizionario utilizzando le proprietà "key" e "value". Esempio:

```yml
dictionaryOptions:
  key: string
  value:
    type: any
    isArray: true
```

**decorators:** Decoratore Typescript che permette di applicare il paradigma dell'Aspect Programming ai field dell'entità, associandone delle meta-informazioni. Utilizzando il componente `sh-form-control` con model binding l'istanza della classe e come prop binding il nome del field in questione, ad applicazione avviata, il suddetto componente leggerà le metainformazioni applicate sul field della classe e dinamicamente allocherà il corretto template e l'eventuale label associata. Il decoratore trattato è il decoratore `@Aspect`. [Per maggior dettagli sul "Context", visita la sezione "Metadati & Decoratori"](.\metadata.md).

- **type:** "aspect".
- **default/browse/edit:** Generalmente viene utilizzata la voce "default" per definire le regole Aspect indipendentemente dal "Context". Nel caso in cui si utilizzi il "Context", è possibile definire una regola Aspect per il context "Browse" e per il context "Edit". [Per maggior dettagli sui decoratori @Aspect e @Validation, visita la sezione "Metadati & Decoratori"](.\metadata.md)
  - **label:** Label da associare al template del campo. Può essere una semplice stringa, od una stringa localizzata. La stringa localizzata ha le seguenti proprietà:
    - **key:** Chiave di traduzione da inserire nel dizionario della lingua (generalmente inserito negli assets [es. it.json])
    - **default:** Stringa di fallback, in caso di assenza della chiave
  - **template:** Aspect key del componente da associare al field. L'Aspect Key è indicata al top di ogni playground dei componenti (es. Textarea => Aspect Key: textarea)

**validations:** Decoratore Typescript che permette di applicare regole di validazione ai field dell'entità, associandone delle meta-informazioni. Utilizzando il componente `sh-form-control` con model binding l'istanza della classe e come prop binding il nome del field in questione, ad applicazione avviata, il suddetto componente leggerà le metainformazioni applicate sul field della classe e dinamicamente applicherà la regola di validazione e l'eventuale messaggio di errore associato. Il decoratore trattato è il decoratore `@Validation`. [Per maggior dettagli sui decoratori @Aspect e @Validation, visita la sezione "Metadati & Decoratori"](.\metadata.md).

- **type:** Tipologia di regola di validazione. E' possibile scegliere tra "mandatory" (il campo sarà obbligatorio), "pattern" (il campo deve rispettare la regular expression indicata) o "custom" (validazione custom creata nel progetto)
- **name:** Campo abilitato solo scegliendo come tipologia "custom". Indica il nome del validatore custom. I validatori custom vanno inseriti nel file "validators.ts" situato nella folder "client\\src\\app\\nome-app\\services". [Per maggior dettagli sui custom validators, visita la documentazione ufficiale di "Angular"](https://angular.io/guide/form-validation#defining-custom-validators) .
- **pattern:** Campo abilitato solo scegliendo `type: pattern`. Indica la regular expression da applicare come regola sul campo.
- **value:** Campo abilitato solo scegliendo come tipologia "custom". Campo non obbligatorio che indica l'eventuale valore statico da passare al validatore.
- **message:** Messaggio di errore da associare al template del campo. Il campo comparirà solo in caso di regola di validazione non rispettata. Può essere una semplice stringa, od una stringa localizzata. La stringa localizzata ha le seguenti proprietà:
  - **key:** Chiave di traduzione da inserire nel dizionario della lingua (generalmente inserito negli assets \[es. it.json\]).
  - **default:** Stringa di fallback, in caso di assenza della chiave.

**warnings:** Decoratore Typescript che permette di applicare regole di validazione NON bloccanti ai field dell'entità, associandone delle meta-informazioni. Utilizzando il componente `sh-form-control` con model binding l'istanza della classe e come prop binding il nome del field in questione, ad applicazione avviata, il suddetto componente leggerà le metainformazioni applicate sul field della classe e dinamicamente applicherà la regola di validazione NON bloccante e l'eventuale messaggio di warning associato. Il decoratore trattato è il decoratore `@Warning`. [Per maggior dettagli sui decoratori @Aspect e @Validation, visita la sezione "Metadati & Decoratori"](.\metadata.md)

- **type:** Tipologia di regola di validazione. E' possibile scegliere tra "mandatory" (il campo sarà obbligatorio), "pattern" (il campo deve rispettare la regular expression indicata) o "custom" (validazione custom creata nel progetto).
- **name:** Campo abilitato solo scegliendo come tipologia "custom". Indica il nome del validatore custom. I validatori custom vanno inseriti nel file "validators.ts" situato nella folder "client\\src\\app\\nome-app\\services". [Per maggior dettagli sui custom validators, visita la documentazione ufficiale di "Angular"](https://angular.io/guide/form-validation#defining-custom-validators).
- **pattern:** Campo abilitato solo scegliendo come tipologia "pattern". Indica la regular expression da applicare come regola sul campo.
- **value:** Campo abilitato solo scegliendo come tipologia "custom". Campo non obbligatorio che indica l'eventuale valore statico da passare al validatore.
- **message:** Messaggio di errore da associare al template del campo. Il campo comparirà solo in caso di regola di validazione non rispettata. Può essere una semplice stringa, od una stringa localizzata. La stringa localizzata ha le seguenti proprietà:
  - **key:** Chiave di traduzione da inserire nel dizionario della lingua (generalmente inserito negli assets [es. it.json]).
  - **default:** Stringa di fallback, in caso di assenza della chiave.

## Operations

Definisce una lista di operazioni, ovvero actions, esposte dal servizio e invocabili dall'esterno tramite richieste HTTP.

```yml
operations:
  - name: getCustomers
    type: http_auto
    description: Recupera i customers
    disableContextAttach: true
    disableActionResult: true
    generationMode: ...
    binding: ...
    parameters: ...
    annotations: ...
```

Le operations lato client sono invocabili mediante l'oggetto "delegates" (this.delegates.nomeOperation) ad ogni livello. I delegates ereditano i metodi delegates dei container genitori. Una operation è composta dalle seguenti proprietà:

**name:** Nome dell'operation. Il nome deve rispettare la notazione camelCase (nomeOperation).

**type:** Tipologia di operation (http verb, subscription, ...). E' possibile scegliere tra le seguenti tipologie:

- **http_delete:** Il metodo DELETE richiede che il server di origine elimini la risorsa identificata dall'URI della richiesta.
- **http_get:** Il metodo GET permette di recuperare qualsiasi informazione (sotto forma di entità) identificata dall'URI della richiesta.
- **http_head:** Il metodo HEAD è identico a GET tranne per il fatto che il server NON DEVE restituire il corpo del messaggio nella risposta.
- **http_jsonp:** **_[OBSOLETE]_**
- **http_options:** Il metodo OPTIONS rappresenta una richiesta di informazioni sulle opzioni di comunicazione disponibili sulla catena di richiesta / risposta identificata dalla Request-URI.
- **http_patch:** Il metodo PATCH viene utilizzato per applicare modifiche parziali alle entità.
- **http_post:** Il metodo POST viene utilizzato per richiedere che il server di origine accetti l'entità racchiusa nella richiesta come nuovo subordinato della risorsa identificata dall'URI della richiesta nella riga della richiesta.
- **http_put:** Il metodo PUT richiede che l'entità racchiusa venga archiviata nell'URI di richiesta fornito. Se l'URI della richiesta fa riferimento a una risorsa già esistente, l'entità racchiusa DOVREBBE essere considerata come una versione modificata di quella che risiede sul server di origine.
- **http_auto:** **_[OBSOLETE]_**
- **signalr_subscription:** Genera un metodo nell'Hub di riferimento.
- **grpc**: Se non ancora generato, genera un file .proto nella cartella "Grpc" e nello stesso file genera i messaggi di request e reply in funzione dei parameters inseriti. Se non ancora generato, genera inoltre il Controller.cs nel quale eseguire l'override dei metodi generati. Aggiunge inoltre le dipendenze necessarie al file .csproj. E' fondamentale che tutti i parametri dell'operation grpc valorizzino la proprietà "position" (0,1,2,...) e, se tra i parametri è presente un DTO, anche i field del DTO in questione devono popolare la proprietà "position".
- **graphql_query:** Definisce una query di GraphQL. Per ulteriori informazioni, visionare la sezione su [GraphQL](#graphql).
- **graphql_mutation:** Definisce una mutation di GraphQL. Per ulteriori informazioni, visionare la sezione su [GraphQL](#graphql).

**description:** Descrizione del metodo del controller.

**disableContextAttach:** Disabilita l'attach del data context. Impostando il valore a true, feature come l'Object Identity verranno disabilitate.

**disableActionResult:** Se true, rimuove "ActionResult" dalla firma della response lato server.

**generationMode:** Se valorizzato imposta come generare l'operation:

- **client:** Genera il DTO solo lato client.
- **server:** Genera il DTO solo lato server.

**auth-policies:** Applica l'attributo "Authorize" con "Policy" sul metodo del controller C#.

**resource:** **_[OBSOLETE]_**

**mode:** sync: metodo del controller sincrono - async (default): metodo del controller asincrono.

**binding:** Permette di specificare se i parametri sono query parameter (fromQuery), se provengono dal body (fromBody) o se sono inseriti nell’header della richiesta (fromHeader):

- fromQuery: in operation con type "http_post" (o altri type che prevedono il body), sarà possibile specificare parametri esterni alla envelop, decorati con [FromQuery], che verranno aggiunti tra i query parameter. Esempio di generazione:

  ```cs
  public async Task<ActionResult<SaveCustomerResponse>> SaveCustomer(SaveCustomerRequest request, [FromQuery] string pIva, CancellationToken requestAborted)
  {
    ...
  }
  ```

- fromBody: in operation con type "http_post" (o altri type che prevedono il body), sarà possibile passare un unico parametro "fromBody", decorato con [FromBody], che non verrà inserito all’interno di una envelop. Esempio di generazione:

  ```cs
  public async Task<ActionResult<SaveCustomerResponse>> SaveCustomer([FromBody] Customer customer, CancellationToken requestAborted)
  {
    ...
  }
  ```

- fromHeader: i parametri di questo tipo verranno aggiunti direttamente nell’header della richiesta e saranno messi a disposizione dello specifico metodo dell’API, decorandoli con l’attributo [FromHeader]. Esempio di generazione:

  ```cs
  public async Task<ActionResult<SaveCustomerResponse>> SaveCustomer(SaveCustomerRequest request, [FromQuery] string pIva, [FromHeader] string codFisc, CancellationToken requestAborted)
  {
    ...
  }
  ```

[**parameters**:](#parameters) Lista dei parametri del metodo.

## Operation Parameters

La proprietà "parameters" di una operation, permette di definire la lista dei parametri del metodo del controller.

```yml
operations:
  - name: getCustomers
    type: http_get
    description: Recupera i customers
    parameters:
      - name: customers
        type: Customer
        description: Customers
        direction: retval
        isArray: true
  - name: getCustomerById
    type: http_get
    description: Recupera il customer per identificativo
    parameters:
      - name: id
        type: uuid
        description: Identificativo del customre
        direction: in
      - name: customer
        type: Customer
        description: Customer
        direction: retval
  - name: updateCustomer
    type: http_post
    description: Applica le modifiche al customer
    parameters:
      - name: customer
        description: Customer da modificare
        direction: in
        type: Customer
      - name: success
        description: Risultato operazione
        direction: retval
        type: boolean
  - name: updateCustomerName
    type: http_put
    description: Cambia il nome del customer
    parameters:
      - name: customer
        type: Customer
        description: Customer per il quale cambiare il nome
        direction: inout
        position: 0
      - name: success
        type: boolean
        description: Risultato operazione
        direction: retval
        position: 1
      - name: message
        type: string
        description: Messaggio di ritorno
        direction: out
        position: 2
```

Le proprietà disponibili sono le seguenti:

**name:** Nome del parametro. Il nome deve rispettare la notazione camelCase (nomeParametro).

**description:** Descrizione del parametro.

**type:** Tipologia della proprietà. Può essere scelto dalla lista dei suggerimenti o può essere identificata in una entità definita nello stesso YAML, in uno YAML shared incluso o in un container genitore (lo scenario eredita tutte le entities del dominio e dell'applicazione, come il dominio eredita tutte le entities dell'applicazione). La lista dei suggerimenti invece, presenta dei "tipi" rappresentanti una sorta di astrazione rispetto al linguaggio nel quale vengono generati. Di seguito tutti i tipi:

- **boolean:** Boolean (C#) - boolean (Typescript)
- **byte:** System.Byte (C#) - number (Typescript)
- **date:** DateTime? (C#) - Date (Typescript)
- **datetime:** DateTime? (C#) - DateTime (Typescript)
- **dateonly:** DateOnly? (C#) - DateOnly (Typescript)
- **decimal:** decimal (C#) - number (Typescript)
- **float:** float (C#) - number (Typescript)
- **integer:** Int32 (C#) - number (Typescript)
- **numeric:** Double (C#) - number (Typescript)
- **sequence:** Int64 (C#) - number (Typescript)
- **string:** String (C#) - string (Typescript)
- **time:** DateTime? (C#) - Date (Typescript)
- **uint8array:** System.Byte[] (C#) - Uint8Array (Typescript)
- **uuid:** System.Guid (C#) - string (Typescript)
- **short:** short (C#) - number (Typescript)
- **any:** System.Object (C#) - any (Typescript)
- **dictionary:** Dictionary<string, object> (C#) - Map<string, any> (Typescript)

**direction:** Definisce la tipologia di parametro. Può essere identificato in una delle seguenti tipologie:

- **in:** Parametro inserito nella "busta" (envelop) della richiesta del metodo.
- **out:** Parametro inserito nella "busta" (envelop) della risposta del metodo.
- **inout:** Parametro inserito sia nella "busta" (envelop) della richiesta che nella busta della risposta del metodo. Simula la feature del by-ref da client a server.

**isArray:** Se impostato a true, rende la proprietà una lista della tipologia indicata nel campo "type".

**isOptional:** Se true, rende il campo opzionale.

**position:** gRPC position, da valorizzare solo quando si utilizza una operation di tipo gRPC. Rappresenta il valore del parametro del messaggio (0,1,2,...).

## Entities

In questa sezione è possibile definire una lista di entità di dominio. Le entity sono le classi che modellano la struttura del database, e sono dunque anche gli oggetti che vengono persistiti in esso.

```yml
entities:
  - name: MyEntity
    type: entity
    description: My entity
    annotations: ...
    useRepository: true
    isTenantEntity: true
    repositoryName: MyRepository
    ancestor: MyAncestorEntity
    annotations: ...
    fields: ...
```

Le proprietà disponibili sono le seguenti:

**name:** Nome dell'entità. Il nome deve rispettare la notazione PascalCase.

**type:** Tipologia di oggetto, può essere 'entity' o 'enum'.

**description:** Descrizione dell'entità.

**useRepository:** Se true, verrà generato un repository per l'entità.

**isTenantEntity:** Se true, indica che l'entità verrà segregata per tentant.

**repositoryName:** Se specificato, imposta il nome del repository.

**ancestor:** Con questa proprietà è possibile impostare come classe padre, una delle classi definite nello stesso file YAML appartenente allo stesso dominio.

[**fields**:](#entityfields) Lista di proprietà dell'entità.

## Entity Fields

La proprietà "fields" di una entity, permette di definire la lista delle proprietà che definiscono le caratteristiche di una entità.

```yml
entities:
- name: MyEntity
  ...
  fields:
  - name: myProperty
    type: string
    description: My property
    annotations: ...
```

Le proprietà disponibili sono le seguenti:

**name:** Nome della proprietà dell'entità. Il nome deve rispettare la notazione camelCase.

**description:** Descrizione del field.

**isNullable:** **_[DEPRECATED]_** - usare la proprietà isOptional.

**isOptional:** Se impostato a true, rende il campo nullable lato C#.

**type:** Tipologia della proprietà. Può essere scelto dalla lista dei suggerimenti o può essere identificata in una entità definita nello stesso YAML. La lista dei suggerimenti invece, presenta dei "tipi" rappresentanti una sorta di astrazione rispetto al linguaggio nel quale vengono generati. Di seguito tutti i tipi:

- **boolean:** Boolean (C#) - boolean (Typescript)
- **byte:** System.Byte (C#) - number (Typescript)
- **date:** DateTime? (C#) - Date (Typescript)
- **datetime:** DateTime? (C#) - DateTime (Typescript)
- **dateonly:** DateOnly? (C#) - DateOnly (Typescript)
- **decimal:** decimal (C#) - number (Typescript)
- **float:** float (C#) - number (Typescript)
- **integer:** Int32 (C#) - number (Typescript)
- **numeric:** Double (C#) - number (Typescript)
- **sequence:** Int64 (C#) - number (Typescript)
- **string:** String (C#) - string (Typescript)
- **time:** DateTime? (C#) - Date (Typescript)
- **uint8array:** System.Byte[] (C#) - Uint8Array (Typescript)
- **uuid:** System.Guid (C#) - string (Typescript)
- **short:** short (C#) - number (Typescript)
- **any:** System.Object (C#) - any (Typescript)
- **dictionary:** Dictionary<string, object> (C#) - Map<string, any> (Typescript)

## Mappings

Questa sezione permette di definire i mappings tra i DTO e le entity. Il risultato è la generazione di classi di configurazione dei mappings, utilizzando la liberia AutoMapper. Nell'esempio, viene creato il mapping dall'entità MyProperty al DTO MyDto. Il mapping è unidirezionale; è possibile invertire la direzione del mapping utilizzando il campo "inverse".

```yml
mappings:
  - entity: MyProperty
    contract: MyDto
    inverse: false
    fields:
      - from: entityFieldName
        to: dtoFieldName
    annotations: ...
```

Le proprietà disponibili sono le seguenti:

**entity:** Nome della entità.

**contract:** Nome del DTO.

**inverse:** Se true, inverte il mapping, definendolo dal DTO alla entità.

**fields:** La sezione permette di mappare una specifica coppia di campi quando i loro nomi differiscono.

## Partials

Questa sezione permette di specificare diverse entità di un microservizio descritte in file YAML separati, in modo da rendere più leggibili e navigabili i file YAML di un microservizio.
È possibile creare un file partial attraverso il task "Generate Partial" di "Scarface". Eseguendo il task verrà richiesto di inserire il nome del file da creare e di selezionare il servizio "padre" a cui verranno aggiunte le proprietà definite all'interno del file YAML parziale. Al termine del task verrà creato il file YAML parziale all'interno della cartella "codegen/model/NomeDelMicroservizioPadre/":

```yaml
name: Operations
type: partial
description: Partial service related to Shell service
```

e, al file yaml del microservizio padre, verrà aggiunta la sezione partials con il riferimento al file creato:

```yaml
name: Shell
type: service
description: Shell microservice
partials:
  - file: operations
```

**Nota:** Poichè i file partial non sono altro che dei file che modellano una parte del microservizio, è possibile utilizzare `service` come valore della proprietà `type`. Tuttavia, consigliamo di utilizzare il valore `partial` per una questione di leggibilità. Analogamente, per i microservizi è possibile utilizzare `partial` come valore della proprietà `type`. Tuttavia, per i motivi sopra descritti, sconsigliamo di farlo.

È possibile, inoltre, creare un file partial manualmente, senza utilizzare il task di Scarface. Per farlo, bisognerà creare un file YAML con estensione `.partial.yml` all'interno della cartella model. È consigliato creare questo file all'interno di una sotto cartella avente come nome il nome del microservizio a cui il file partial fa riferimento. Per aggiungere il riferimento del file partial creato, bisognerà aggiungere la sezione `partials` al microservizio padre insieme ai nomi dei file partial in kebab case. Tutti i file partial creati e non referenziati all'interno della sezione "partials" non verranno considerati ai fini della generazione:

```yaml
name: Shell
type: service
description: Shell service
---
partials:
  - file: operations
  - file: dtos
```

## Dependencies

Questa sezione consente di generare dei business services all'interno del microservizio. Ad esempio, è possibile creare un servizio denominato "Cart" al cui interno contiene il metodo "getProductById" di tipo "Transient":

```yml
name: Shell
type: service
author: CodeArchitects
description: Shell system repository
namespace: App.Segregation.Shell
dependencies:
  - name: Cart
    type: Transient # Scoped | Singleton
    namespace: Administration
    mode: async # sync (Default: async)
    methods:
      - name: getProductById
        description: Get product by id
        parameters:
          - name: id
            description: Product identifier
            direction: in
            type: uuid
          - name: product
            type: Product
            direction: out
            description: Product
```

Nello specifico verrà generata una interfaccia e la relativa classe all'interno della cartella "Domain/Services/Administration". Nel caso in cui NON venga specificato il namespace, i file verranno generati nella cartella "Domain/Services".

Contratto software:

```cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Ca.Segregation.Model.Dto;

namespace App.Segregation.Shell.Domain.Services
{
  // --inject:RESPONSES--

  // --inject:RESPONSES--

  // --inject:SERVICE_NAME--
  public interface ICartService
  // --inject:SERVICE_NAME--
  {
    // --inject:METHODS--
    /// <summary>
    /// Get Product by Id
    /// </summary>
    /// <param name="id">Product identifier</param>
    Task<ProductDto> GetProductByIdAsync(Guid id);

    // --inject:METHODS--
  }
}
```

Nel caso in cui ci siano più parametri aventi `direction: retval`, verranno generate delle interfacce (nella zona di iniezione "RESPONSES" contenente tutti i parametri indicati come response). Invece, i parametri con `direction: out` saranno inseriti come parametri del metodi, ma saranno preceduti dalla parola chiave "out". Ad esempio:

```yml
methods:
  - name: getProductById
    description: Get product by id
    parameters:
      - name: id
        description: Product identifier
        direction: in
        type: uuid
      - name: foo
        type: string
        direction: retval
        description: foo
      - name: bar
        type: string
        direction: retval
        description: bar
      - name: fooBar
        type: string
        direction: out
        description: fooBar
```

```cs
// --inject:RESPONSES--
public interface ICartGetProductByIdAsyncResponse
{
  public string Foo {get; set;}
  public string Bar {get; set;}
}
// --inject:RESPONSES--
Task<ICartGetProductByIdAsyncResponse> GetProductByIdAsync(Guid id, out string fooBar);
```

Classe concreta, la cui implementazione è lasciata allo sviluppatore:

```cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace App.Segregation.Shell.Domain.Services
{
  // --inject:SERVICE_NAME--
  public class CartService : ICartService
  // --inject:SERVICE_NAME--
  {
    public CartService()
    { }
  }
}
```

Oltre alla generazione di questi file, verrà predisposta la Dependency Injection per il servizio creato:

- **.NET 5:** all'interno del file "EspServiceCollectionExtensions.cs":

```cs
namespace App.Segregation.Shell
{
  public static class EspServiceCollectionExtensions
  {
    public static void AddEspServices(this IServiceCollection services)
    {
      services.AddTransient<Domain.Services.Administration.ICartService, Domain.Services.Administration.CartService>();
    }
  }
}
```

- **.NET 6:** e 7 all'interno del file "App.cs":

```cs
namespace App.Segregation.Shell
{
  public static class EspServiceCollectionExtensions
  {
    public static WebApplicationBuilder AddData(this WebApplicationBuilder builder)
    {
      builder.Services.AddTransient<Domain.Services.Administration.ICartService, Domain.Services.Administration.CartService>();
    }
  }
}
```

## Secrets

Questa sezione permette di utilizzare i secrets tramite Dapr utilizzando un provider specificato. I provider attualmente supportati sono:

- **azurekeyvault:** [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault/).

```yml
secrets:
  - provider: azurekeyvault
```

Tra i file generati vi sarà un file json atto a contenere i secrets, dal path "server/Dapr/components/nome-microservizio-secrets-azurekeyvault.json":

```json
{
  "sample-key": "This is a sample secret"
}
```

Una volta inseriti i secret desiderati, è necessario effettuare una clean della solution di Visual Studio (Barra degli strumenti > Build > Clean Solution) per poter caricare correttamente i file di configurazione Dapr durante l'esecuzione dell'ambiente Docker.
La modalità di accesso ai secrets all'interno dell'applicazione è identico a quello dei dati presenti all'interno di appsettings.json.
Di seguito un esempio di utilizzo del secret all’interno del file "Program.cs" di un microservizio:

```cs
string? sampleKey = app.Configuration["sample-key"];
if (sampleKey == "This is a sample secret")
{
  app.Run();
}

app.Run();
```

%% Sezione actors omessa perché duplicata di actors.md

## Configurable indentation

È possibile configurare l’indentazione dei file generati:

- Per impostare una indentazione custom per il codice generato lato server, sarà sufficiente modificare i seguenti file come segue (dove 4 è il valore di indentazione di esempio):

  - Aggiungere la seguente riga nel file "codegen/configs/all.yml":

    ```yml
    server.indentSize: 4
    ```

  - Aggiungere la seguente riga nel file "codegen/configs/server.yml":

    ```yml
    indentSize: 4
    ```

  Dopo aver salvato i precedenti file, lanciare il comando "Scarface: Format server" per formattare il codice dei file esistenti lato server. Questo comando andrà lanciato solamente al cambio dell’indentSize.

- Per impostare una indentazione custom per il codice generato lato client, sarà sufficiente modificare i seguenti file come segue (dove 4 è il valore di indentazione di esempio):

  - Aggiungere la seguente riga nel file "codegen/configs/all.yml":

    ```yml
    client.indentSize: 4
    ```

  - Aggiungere la seguente riga nel file "codegen/configs/client.yml":

    ```yml
    indentSize: 4
    ```

  Dopo aver salvato i precedenti file, lanciare il comando "Scarface: Format client" per formattare il codice dei file esistenti lato client. Questo comando andrà lanciato solamente al cambio dell’indentSize.

- Per ri-formattare tutti i file (sia lato client che lato server), basterà lanciare il comando "Scarface: Format all".

## Payloads

Questa sezione consente di specificare vari payloads relativi ad uno scenario, in modo da consentire la condivisione di payload diversi tra differenti scenari. È, tuttavia, preservata la possibilità di modellare il payload manualmente.

```yml
name: CustomerPayload
type: payload
description: Customer payload
fields:
  - name: ...
  - type: ...
  - description: ...
  - isArray: ...
  - isOptional: ...
  - container: ...
  - dictionaryOptions: ...
```

Le proprietà disponibili sono le seguenti:

**name:** Nome del payload.

**type:** Tipo del file yaml, in questo caso "payload".

**description:** Descrizione del payload.

**fields:** Lista di oggetti desiderati all'interno del payload, caratterizzati da:

- **name:** Nome dell'oggetto.
- **type:** Tipo dell'oggetto, identici ai tipi disponibili per i [dto fields](#fields).
- **description**: Descrizione dell'oggetto.
- **isArray:** Se impostato a true, rende la proprietà una lista della tipologia indicata nel campo "type".
- **isOptional:** Se impostato a true, rende il campo nullable lato C#.
- **container:** Indica il tipo di container da cui recuperare le informazioni dell'oggetto indicato, indicando:
  - **type:** Tipo del container (applicazione, dominio, scenario).
  - **service:** Nome del servizio del container.
- **dictionaryOptions:** Permette di modificare chiave e valore del dizionario utilizzando le proprietà "key"e "value".

Come esempio, ipotizziamo che uno scenario "customers" debba proseguire il suo flusso nello scenario "suppliers" inserendo nel payload una stringa di ricerca e il customer selezionato (DTO del servizio Business):

```yml
name: CustomerPayload
type: payload
description: Customer payload
fields:
  - name: customer
    type: Customer
    description: Customer DTO
    container:
      type: application
      service: Business
  - name: searchText
    type: string
    description: Search Text
```

In questa situazione, sarà necessario definire la proprietà customer sia nel contratto software del payload dello scenario "customers" che in quello dello scenario "suppliers":

```yml
name: Customers
type: task
description: Customers scenario
domain: Crm
namespace: Ca.BackOffice.Crm.Customers
activity: CustomersActivity
payloads:
  - name: CustomerPayload
```

```yml
name: Suppliers
type: task
description: Suppliers scenario
domain: Crm
namespace: Ca.BackOffice.Crm.Suppliers
activity: SuppliersActivity
payloads:
  - name: CustomerPayload
```

Il codice generato sarà il seguente:

```ts
import * as ApplicationModels from '../../../models/index';
...
export interface CustomersPayload extends IActivityPayload {
  /**
  * optional version of payload data
  */
  version?: number;
  /**
   * Customer DTO
   */
  customer: ApplicationModels.BusinessModels.Customer;
  /**
   * Search Text
   */
  searchText: string;
  // --inject:classDeclaration--
}
```

## GraphQL

GraphQL è un linguaggio di interrogazione e manipolazione dei dati open-source per API e un runtime per soddisfare query con dati esistenti.
GraphQL può essere utitilizzato in alternativa ed in combinazione con le API REST; infatti, è possibile definire le query e le mutations utilizzando la sezione `contracts.operations`.

Come esempio si definisce una query base per leggere una lista di `Customer` dal database specificando il tipo di operazione come `graphql_query`:

```yml
contracts:
  operations:
    - name: customers
      type: graphql_query
      description: Get customers
      entity:
        name: Customer
        isArray: true
```

Ciò genererà, nella classe `RootQuery` nella cartella `GraphQL` il metodo che implementerà la query:

```cs
public partial class RootQuery
{
  public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context
  // <custom:customersParameters>
  // </custom:customersParameters>
  )
  {
    // <custom:customersImplementation>
    // </custom:customersImplementation>
  }
}
```

L'implementazione di questo metodo restituirà la lista di `Customer`, ad esempio utilizzando un repository (iniettandolo all’interno del metodo) oppure Entity Framework Core (i cui esempi sono riportati sotto).

È possibile definire dei parametri da passare alla query. Ad esempio, se si vuole filtrare per nome, basta aggiungere un parametro, in questo caso chiamato `name`.

```yml
contracts:
  operations:
    - name: customers
      type: graphql_query
      description: Get customers
      entity:
        name: Customer
        isArray: true
      parameters:
        - name: name
          type: string
          description: Name
          direction: in
          isOptional: true
```

E ciò aggiungerà un parametro utilizzabile all'interno della query.

```cs
public partial class RootQuery
{
  public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context, string name
  // <custom:customersParameters>
  // </custom:customersParameters>
  )
  {
    // <custom:customersImplementation>
    // </custom:customersImplementation>
  }
}
```

Sono supportati, tramite la sezione `annotations`, gli attributi `[UsePaging]`, `[UseProjection]`, `[UseFiltering]`, `[UseSorting]`:

```yml
contracts:
  operations:
    - name: customers
      type: graphql_query
      description: Get customers
      entity:
        name: Customer
        isArray: true
      annotations:
        - name: usePaging
          namespace: GraphQL
          value:
            inclueTotalCount: true
            maxPageSize: 500
        - name: useProjection
          namespace: GraphQL
        - name: useFiltering
          namespace: GraphQL
        - name: useSorting
          namespace: GraphQL
      parameters:
        - name: name
          type: string
          description: Name
          direction: in
          isOptional: true
```

Di seguito è riportata una possibile implementazione di questo metodo utilizzando Entity Framework Core.

```yml
public partial class RootQuery
{
[UsePaging(MaxPageSize = 500)]
[UseProjection]
[UseFiltering]
[UseSorting]
public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context, string name
// <custom:customersParameters>
, [Service] IMapper mapper
// </custom:customersParameters>
)
{
// <custom:customersImplementation>
return context.Customer.Where(customer => customer.Name == name).ProjectTo<Dto.Customer>(mapper.ConfigurationProvider);
// </custom:customersImplementation>
}
}
```

Di seguito invece, una possibile implementazione di questo metodo utilizzando un repository.

```cs
public partial class RootQuery
{
  [UsePaging(MaxPageSize = 500)]
  [UseProjection]
  [UseFiltering]
  [UseSorting]
  public async Task<IEnumerable<Dto.Customer>> Customers([Service] BusinessDataContext context, string name
  // <custom:customersParameters>
, [Service] ICustomerEntityRepository repository, [Service] IMapper mapper
  // </custom:customersParameters>
  )
  {
    // <custom:customersImplementation>
var customerEntity = await repository.GetAllAsync();
      return mapper.Map<IEnumerable<Dto.Customer>>(customerEntity);
    // </custom:customersImplementation>
  }
}
```

Le mutations sono gestite in maniera simile, specificando `graphql_mutation` come tipo di operazione.

```yml
contracts:
  operations:
    - name: updateCustomer
      type: graphql_mutation
      description: Update customer
      parameters:
        - name: customer
          type: Customer
          description: Customer to be updated
          direction: in
        - name: success
          type: boolean
          description: Operation result
          direction: out
```

In questo caso, vengono specificati dei parametri `in` e `out`: il primo contiene i dati del `Customer` da aggiornare, mentre il secondo indica se l'operazione è andata a buon fine. Anche le mutation possono utilizzare gli attributi, esattamente come le query.

```cs
public partial class Mutation
{
  // <custom:updateCustomerAttributes>
  // </custom:updateCustomerAttributes>
  public async Task<bool> UpdateCustomer(Customer customer, [Service] BusinessDataContext context
  // <custom:updateCustomerParameters>
  , [Service] IMapper mapper
  // </custom:updateCustomerParameters>
  )
  {
    // <custom:updateCustomerImplementation>
    var customerEntity = mapper.Map<CustomerEntity>(customer);
    context.Update(customerEntity);
    await context.SaveChangesAsync();
    return true;
    // </custom:updateCustomerImplementation>
  }
}
```

Lato client, le operazioni graphql saranno invocabili in maniera molto simile alle operation REST. Aggiungendo almeno una operation di tipo graphql ad un microservizio raggiungibile dal client, verrà generato un servizio "graphQL", direttamente raggiungibile dall’istanza del servizio relativo al microservizio, e così facendo si potrà accedere alle query ed alle mutation disponibili
"this.delegates.business.graphQL.customer".
Prendendo come esempio i seguenti DTO:

```yml
dto:
  - name: Customer
    type: entity
    description: Customer entity
    fields:
      - name: name
        description: Customer name
        type: string
      - name: surname
        description: Customer surname
        type: string
      - name: fiscalCode
        description: Customer fiscal code
        type: string
        isOptional: true
      - name: email
        description: Customer email
        type: string
      - name: version
        description: Customer version
        type: numeric
      - name: updateDate
        type: dateOnly
        description: Update Date
        isOptional: true
      - name: demographics
        type: Demographic
        isArray: true
        description: Customer demographics
        value: default
  - name: Demographic
    description: Demographic
    type: entity
    fields:
      - name: name
        type: string
        description: Name
      - name: value
        type: string
        description: Value
```

e definendo la seguente operation:

```yml
operations:
  - name: customers
    type: graphql_query
    description: Get customers
    entity:
      name: Customer
      isArray: true
    annotations:
      - name: usePaging
        namespace: GraphQL
        value:
          inclueTotalCount: true
          maxPageSize: 500
      - name: useProjection
        namespace: GraphQL
      - name: useFiltering
        namespace: GraphQL
```

lato client si potrà effettuare la query graphql, come nell’esempio seguente:

```ts
await this.delegates.business.graphQL
  .customers(
    'id',
    'email',
    x => x.surname,
    c => ShGraphQL.queryArray(c.demographics, 'name', 'value')
  )
  .paginate()
  .toPromise();
```

Osservando la query, possiamo porre l’attenzione su alcuni punti:

- Si stanno selezionando solamente i campi diretti id, email e surname del customer.
- I campi possono essere selezionati semplicemente indicandone il nome (ovviamente in maniera guidata), oppure definendo una callback (come per surname).
- I campi di tipo array (come demographics), dovranno essere selezionati definendo una callback ed utilizzando la funzione queryArray di ShGraphQL.
- Considerando che nella modellazione si è inserita la paginazione, è necessario inserire il metodo paginate prima di lanciare la query.
  - Nel metodo paginate potranno essere definiti opzionalmente il pageIndex ed il pageSize (es. .paginate({ pageSize: 2, pageIndex: 1}))
- Avendo abilitato il filtering ed il sorting, si potranno opzionalmente filtrare e ordinare i dati da ottenere, come nell’esempio seguente

  ```ts
  await this.delegates.business.graphQL
    .customers(
      'name',
      'id',
      'email',
      x => x.surname,
      'version',
      'updateDate',
      c => ShGraphQL.queryArray(c.demographics, 'name', 'value', 'trackingState', 'id')
    )
    .paginate({ pageSize: 2, pageIndex: 1 })
    .where({
      name: {
        operator: ShGraphQLWhereOperator.Like,
        value: this.payload.searchText
      }
    })
    .sortBy({ email: ShGraphQLSortDirection.DESC, name: ShGraphQLSortDirection.ASC })
    .toPromise();
  ```

Aggiungendo un parametro di input all’operation:

```yml
operations:
  - name: customers
    type: graphql_query
    description: Get customers
    entity:
      name: Customer
      isArray: true
    parameters:
      - name: name
        type: string
        description: name
        direction: in
        isOptional: true
    annotations:
      - name: usePaging
        namespace: GraphQL
        value:
          inclueTotalCount: true
          maxPageSize: 500
      - name: useProjection
        namespace: GraphQL
      - name: useFiltering
        namespace: GraphQL
```

il primo parametro dell’operation generata sarà proprio quello inserito nello YAML:

```ts
await this.delegates.business.graphQL.customers(‘PARAMETRO NAME’,'id', 'email', x => x.surname, c => ShGraphQL.queryArray(c.demographics, 'name', 'value')).paginate().toPromise()
```

è ovviamente possibile modellare una query che ritorni una sola istanza del DTO indicato, come nell’esempio di seguito:

```yml
- name: customer
      type: graphql_query
      description: Retrieves a customer
      entity:
        name: Customer
      parameters:
        - name: id
          type: uuid
          description: id
          direction: in
```

che permette di utilizzare l’operation generata come segue:

```ts
const result = await this.delegates.business.graphQL
  .customer(customer.id, 'id', 'email', 'surname', 'version', 'updateDate', c =>
    ShGraphQL.queryArray(c.demographics, 'name', 'value')
  )
  .toPromise();
```

dove result conterrà la envelop con all’interno il singolo customer.

**Nota:** Nelle modellazione delle operation di tipo graphql_query, non andranno mai specificati parametri di ritorno.

Per quanto riguarda invece la modellazione delle mutation, queste ultime potranno prevedere parametri di ritorno:

```yml
- name: updateCustomer
  type: graphql_mutation
  description: Update customer
  parameters:
    - name: customer
      type: Customer
      description: Customer to be updated
      direction: in
    - name: success
      type: boolean
      description: Operation result
      direction: out
```

La precedente mutation, potrà essere invocata dal client, come segue:

```ts
await this.delegates.business.graphQL.updateCustomer(this.payload.customer).toPromise();
```

Tra i parametri di ritorno, è possibile inserire anche un DTO sul quale effettuare una query, come nell’esempio seguente:

```yml
- name: updateCustomerAndReturn
  type: graphql_mutation
  description: Update customer and return it
  parameters:
    - name: customer
      type: Customer
      description: Customer to be updated
      direction: in
    - name: customer
      type: Customer
      description: Updated customer
      direction: out
```

che potrà essere invocata dal cliente, come segue:

```ts
await this.delegates.business.graphQL
  .updateCustomerAndReturn(this.payload.customer, 'email', 'name', 'updateDate')
  .toPromise();
```

Attenzione, se si ritorna un DTO, sarà sempre necessario inserire almeno un field sul quale effettuare la query.

## Change tracking

Il change tracking è una feature presente in alcune librerie di accesso ai dati che permette di tracciare lo stato delle entità persistite tramite database. Attraverso il change tracking, è possibile annotare le entità contrassegnandole con un valore che rappresenta lo stato corrente dell'entità, tipicamente:

- Modificata rispetto all'ultima lettura (Modified)
- Da rimuovere (Removed)
- Da aggiungere (Added)
- Inalterata (Unchanged)

All'interno della comunicazione client-server è possibile specificare lo stato delle entità annidate all'interno di un'altra entità, in modo tale da eseguire diverse operazioni per diverse entità, a seconda del loro stato.
Ad esempio, data una relazione 1 a N tra un'entità "padre" ed un'entità "figlio", si potrebbe, utilizzando il change tracking, aggiungere, modificare e rimuovere le entità figlie indipendentemente l'una dall'altra, all'interno di un'operazione di modifica del padre.
Definiamo un aggregato composto da due entità: `Customer`, rappresentante un cliente, e `Demographic` rappresentante un fatto riguardante tale cliente, come genere, età, etnia, eccetera. La relazione è 1 a N perché ad un `Customer` possono corrispondere diversi `Demographic`. Assumiamo di aver definito entità e DTO come nel seguente yml, con operazioni CRUD (omesse per brevità) su `Customer`:

```yml
entities:
  - name: Customer
    description: Customer Entity
    useRepository: true
    fields:
      - name: name
        type: string
        description: Customer name
      - name: surname
        type: string
        description: Customer surname
      - name: demographics
        type: DemographicEntity
        isArray: true
        description: Customer demographics
  - name: Demographic
    description: Demographic Entity
    fields:
      - name: name
        type: string
        description: Name
      - name: value
        type: string
        description: Value
associations:
  - type: aggregate
    multiplicity: one-to-many
    from:
      entity: Customer
      navigation: Demographics
    to:
      entity: Demographic
contracts:
  dto:
    - name: Customer
      type: entity
      description: Customer entity
      fields:
        - name: name
          description: Customer name
          type: string
        - name: surname
          description: Customer surname
          type: string
        - name: demographics
          type: Demographic
          isArray: true
          description: Customer demographics
          value: default
    - name: Demographic
      description: Demographic
      type: entity
      fields:
        - name: name
          type: string
          description: Name
        - name: value
          type: string
          description: Value
```

Immaginiamo di aver creato un `Customer` con 3 `Demographic`:

```json
{
  "customer": {
    "name": "John",
    "surname": "Doe",
    "demographics": [
      {
        "name": "age",
        "value": "32"
      },
      {
        "name": "address",
        "value": "858 Valley Farms Road Sioux Falls, SD 57103"
      },
      {
        "name": "ethnicity",
        "value": "Caucasian"
      }
    ]
  }
}
```

Adesso, supponiamo di aver bisogno di aggiornare, all'interno della stessa operazione (PUT), questo `Customer`, modificando (opzionalmente i campi `name` e `surname`) le sue `demographics` in modo tale da:

- Aggiornare il valore di `age` da 32 a 30;
- Rimuovere `address`;
- Aggiungere un nuovo `Demographic` con `name: gender` e `value: "Male"`;
- Lasciare invariato `ethnicity`.

Per far ciò, possiamo annotare il DTO `Demographic` con il campo `isTrackable: true`.

```yml
contracts:
  dto:
    - name: Demographic
      description: Demographic
      isTrackable: true
      type: entity
      fields:
        - name: name
          type: string
          description: Name
        - name: value
          type: string
          description: Value
```

A questo punto, il change tracker integrato all'interno del client farà in modo di aggiungere al DTO `Demographic` un campo, chiamato `trackingState`, che conterrà lo stato dell'oggetto. La richiesta `PUT` che verrà inoltrata al server sarà (supponendo di non aver modificato `name` e `surname`) del tipo:

```yml
{
  'customer':
    {
      'name': 'John',
      'surname': 'Doe',
      'demographics':
        [
          { 'name': 'age', 'value': '30', 'trackingState': 4 // MODIFIED = 4 },
          {
            'name': 'address',
            'value': '858 Valley Farms Road Sioux Falls, SD 57103',
            'trackingState': 8 // REMOVED = 8
          },
          { 'name': 'gender', 'value': 'Male', 'trackingState': 2 // ADDED = 2 }
        ]
    }
}
```

Il backend, se correttamente configurato, potrà interpretare questi stati in modo tale da produrre le corrette operazioni all'interno dello stesso update, utilizzando il repository di `Customer`.
Le operazioni necessarie lato backend ad interpretare il `trackingState` sono:

1. Mappare il DTO nell'entità preservando le informazioni di tracking. Esistono due metodi per preservare le informazioni di tracking all'interno del mapping, descritti in seguito.
2. Chiamare il metodo UpdateAsync del repository di `Customer`.

Se si utilizza AutoMapper per il mapping, il tracking è già preservato se è stato definito il mapping nello yml, come nel seguente esempio:

```yml
mappings:
  - entity: Customer
    contract: Customer
  - entity: Customer
    contract: Customer
    inverse: true
  - entity: Demographic
    contract: Demographic
  - entity: Demographic
    contract: Demographic
    inverse: true
```

Allora, dato che il DTO `Demographic` è stato indicato come trackable, verrà generato:

```cs
public void MapDemographicDtoToDemographicEntityEntity()
{
  CreateMap<Dto.Demographic, Domain.Model.Demographic>()
  /* Preserve tracking */
  .PreserveTracking()
  // <custom:mappings2>
  ; // </custom:mappings2>
}
```

L'istruzione `PreserveTracking` preserverà automaticamente le informazioni di tracking quando viene effettuato il mapping. L'operazione definita nel controller potrà essere di questo tipo:

```cs
public class CustomerController : ControllerBase
{
  private readonly IMapper _mapper;
  private readonly ICustomerRepository _repository;

  public CustomerController(IMapper mapper, ICustomerRepository repository)
  {
    _mapper = mapper;
    _repository = repository;
  }

  [HttpPut("updateCustomer")]
  public async Task<ActionResult<UpdateCustomerResponse>> UpdateCustomer(UpdateCustomerRequest request, CancellationToken requestAborted)
  {
    Customer customer = _mapper.Map<Customer>(request.Customer);

    await _repository.UpdateAsync(customer, requestAborted);

    return Ok();
  }
}
```

Se non si utilizza AutoMapper, allora è necessario utilizzare l'interfaccia `ITrackingContext` ed effettuare il mapping utilizzando il metodo di estensione `Map`/`MapList`/`MapArray`:

```cs
public class CustomerController : ControllerBase
{
  private readonly ITrackingContext _trackingContext;
  private readonly ICustomerRepository _repository;

  public CustomerController(ITrackingContext trackingContext, ICustomerRepository repository)
  {
    _trackingContext = trackingContext;
    _repository = repository;
  }

  [HttpPut("updateCustomer")]
  public async Task<ActionResult<UpdateCustomerResponse>> UpdateCustomer(UpdateCustomerRequest request, CancellationToken requestAborted)
  {
    Dto.Customer customerDto = request.Customer;
    Customer customer = new Customer
    {
      Id = customerDto.Id,
      Name = customerDto.Name,
      Surname = customerDto.Surname,
      Demographics = customerDto.Demographics.MapList(_trackingContext, demographicDto => new Demographic
      {
        Name = demographicDto.Name,
        Value = demographicDto.Value
      })
    };

    await _repository.UpdateAsync(customer, requestAborted);

    return Ok();
  }
}
```

Lato client, è possibile accedere allo stato della singola entità attraverso la proprietà `trackingState`:

```ts
const trackingState = this.payload.customer.trackingState;
```

Oppure, all'intero change tracker tramite la proprietà `changeTracker`.

Per modificare lo stato dell'entità, è sufficiente impostare il valore di `trackingState`. Ad esempio, per eliminare un'entità attraverso una callback sul click di un pulsante:

```html
<sh-button (clicked)="customer.trackingState = ObjectState.deleted">Delete</sh-button>
```

Una volta effettuata un'operazione (add, update, remove) su un'entità, si dovrebbe effettuare la chiamata al metodo `acceptChanges()` per reimpostare il valore del `trackingState` dopo che l'operazione è andata a buon fine. Ad esempio:

```ts
await this.delegates.business.saveCustomerAsync(this.payload.customer);
this.payload.customer.acceptChanges();
```

## EJS

EJS è un semplice "templating language" che consente di generare qualsiasi snippet di codice con JavaScript. Nessuna religiosità su come organizzare le cose. Nessuna reinvenzione dell'iterazione e del flusso di controllo. È solo un semplice JavaScript.

EJS è utilizzato nel platform per generare tutto il codice dei progetti. Il platform fornisce "out of the box" una libreria di template EJS che è possibile sovrascrivere in funzione delle esigenze del progetto. Di seguito un esempio di template EJS del platform:

```js
<%# /* Context = { entity: Entity, container: RootContainer } */ %>
<%
  const rootNamespace = rootNamespaceOfContainer(container);
  const name = entity.name;
  const namespace = fullNamespaceOfContainer(container);
  const fullName = `${namespace}.${name}`;
  const keys = entityKeysSequence(entity);
  const validations = entity.validations;
  const hasValidations = !!validations && validations.length > 0;
  const isAbstract = entity.isAbstract;
  const isTrackable = entity.isTrackable;
  const resource = entity.resource;
-%>
<%- render('documentation/entity.ejs', { entity: entity }); %>
@JsonObject({ name: '<%- fullName %>, <%- rootNamespace %>' })
@Entity({
  name: '<%- fullName %>',
  keys: [<%- keys %>]
})
<% if (hasValidations) { -%>
  <%- render('model/entity/validation-collection.ejs', { validations: validations }); %>
<% } -%>
<% if (resource) { -%>
  <%- render('module/resource.ejs', { uri: resource }); %>
<% } -%>
export <%- isAbstract ? 'abstract ' : '' %>class <%- name %> extends <%- getExtendsClass(entity, container); %> {
  <%- render('model/entity/entity-body.ejs', { entity: entity, container: container }); %>
}
```

[Per maggior dettagli sulla sintassi del linguaggio EJS, visita la documentazione ufficiale](https://ejs.co/)

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
