# Architettura
## C4 Model

Per rappresentare l'architettura di una applicazione sviluppata con il CA-Platform, viene utilizzato il C4Model, ovvero un approccio che semplifica la rappresentazione di una architettura software, scomponendo un sistema in container e componenti e mostrandone le relazioni tra essi e con eventuali sistemi esterni.

- **Level 1 (L1 - System Context)**: Astrazione del sistema. Include relazioni con gli utenti e sistemi esterni
- **Level 2 (L2 - Containers)**:Scompone un sistema in container interconnessi. Un container rappresenta una applicazione o un archivio dati
- **Level 3 (L3 - Components)**:Scompone i container in componenti correlati e mette in relazione questi ultimi con altri container o altri sistemi
- **Level 4 (L4 - Code)**:Fornisce ulteriori dettagli sulla progettazione degli elementi architetturali che possono essere mappati con il codice.

![C4 Model](./assets/resources/c4-layers-overview.png "C4 Model")

Il C4 Model si basa su notazioni esistenti come Unified Modeling Language (UML), Entity Relation Diagrams (ERD) o diagrammi generati da Integrated Development Environments (IDE). Per i livelli da 1 a 3, il modello C4 utilizza 5 elementi di diagrammi di base: persone, sistemi software, contenitori, componenti e relazioni. La tecnica non è prescrittiva per il layout, la forma, il colore e lo stile di questi elementi. Il C4Model consiglia di utilizzare semplici diagrammi basati su scatole nidificate per facilitare il disegno collaborativo interattivo. La tecnica promuove anche buone pratiche di modellazione come fornire un titolo e una legenda su ogni diagramma e un'etichettatura chiara e univoca per facilitare la comprensione da parte del pubblico previsto. Il C4Model facilita l'architettura visiva collaborativa e l'architettura evolutiva nel contesto di team agili in cui non sono desiderati metodi di documentazione più formali e progettazione architettonica iniziale.

[Per maggior dettagli sul C4Model, visita la documentazione ufficiale](https://c4model.com/)


## L1 - System Context

**Astrazione del sistema. Include relazioni con gli utenti e sistemi esterni**
I progetti sviluppati con il CA-Platform, sono costituiti da:

- una Single Page Application basata su Angular (per la parte client), ovvero un'applicazione web consultabile su una singola pagina web con l'obiettivo di fornire una esperienza utente più fluida e simile alle applicazioni desktop dei sistemi operativi tradizionali; applicazione il quale codice (HTML, JavaScript e CSS) è recuperato in un singolo caricamento della pagina o le risorse appropriate sono caricate dinamicamente e aggiunte alla pagina quando necessario, di solito in risposta ad azioni dell'utente
- una serie di microservizi .NET 5 (per la parte server)

![L1 - System Context](./assets/resources/c4-l1.png "L1 - System Context")

La comunicazione tra client e server avviene tramite approccio REST. La definizione dei modelli, dei container, dei metodi dei controller, dei delegati per la comunicazione, etc.. avviene all'interno di file YAML, utilizzando il DSL (Domain Specific Language) del Platform per meta-modellarne le informazioni. I file YAML contenenti le meta-informazioni vengono infine utilizzati per generare codice sia lato client che lato server.

[Per maggior dettagli sulla generazione del codice, visita la sezione "Codegen"](/codegen.md)

## L2 - Containers

**Scompone un sistema in container interconnessi. Un container rappresenta una applicazione o un archivio dati**

Le SPA o Single Page Application sono applicazioni web fruibili come singola pagina senza necessità di caricamento per pagine: scopriamone i vantaggi! Applicazioni che permettono di ricreare nel web esperienze utenti simili alle applicazioni tradizionali hanno lo scopo di fornire una user experience fluida e rapida, senza interruzioni né fastidiose pause di caricamento. Di fatto, una single page app ha comportamenti simili alle applicazioni desktop su qualunque pc – perdendo alcune caratteristiche tipiche dei siti Web tradizionali (tempi di caricamento di pagina, necessità di caricamento completo dei dati etc), ma mantiene i vantaggi di essere perfettamente disponibile sul Web senza bisogno d’installazione. In sostanza, funziona in questo modo: l’applicazione SPA contiene in sé l’intero codice necessario per funzionare e le risorse ad essa associate vengono caricate dinamicamente solo quando servono, in risposta a precise azioni da parte dell’utente.

Di seguito i vantaggi della Single Page Application:

- Velocità: l’app s’interfaccia direttamente con il server, ne richiede i dati all’occorrenza e li restituisce in tempo reale senza necessità di dover ricaricare la pagina
- Performance: grazie alla velocità di risposta, l’intera esperienza utente è più fluida, immediata. L’utente può gestire più operazioni simultaneamente senza interruzioni, il lavoro scorre rapido e senza intoppi
- Scalabilità: le single Page application sono progettate per essere modulari, permettendo di aggiungere in maniera progressiva nuove funzionalità e far crescere nel tempo una soluzione sempre più tagliata ad hoc su ciò di cui hai realmente bisogno, nel momento in cui ne hai bisogno
- Acessibilità: non devi installare né aggiornare. Una Single Page Application è disponibile in modalità responsive da qualunque device sia collegato ad Internet: desktop, smartphone o tablet
- Risparmio: nessun costo di formazione e assistenza. L’app è creata per essere davvero user-friendly anche per un utente con competenze tecnologiche elementari
![L2 - Containers and SPA](./assets/resources/c4-l2-fe.png "L2 - Containers and SPA")

Nell'architettura delle applicazioni sviluppate con il CA-Platform, la Single Page Application comunica con i servizi back-end tramite un API Gateway (implementato tramite EnvoyProxy). Un API Gateway si comporta come un reverse proxy per accettare tutte le chiamate API, aggregare i vari servizi richiesti per gestirle e restituire i risultati appropriati. La maggior parte delle API enterprise vengono distribuite tramite API Gateway. L'API Gateway intercetta tutte le richieste in entrata e le invia attraverso il sistema di gestione delle API, che elabora una serie di funzioni necessarie. La digital transformation e altri importanti cambiamenti organizzativi spingono le aziende a fornire applicazioni cross-device e multipiattaforma che non sarebbero possibili senza le giuste API che permettono di collegare queste piattaforme. Tradizionalmente, le interfacce del programma applicativo sono state utilizzate per gestire il traffico tra applicazioni monolitiche e client. Nella cosiddetta app economy, gli sviluppatori possono integrare sistemi interni eterogenei per creare applicazioni costituite da tanti microservizi distribuiti. Rispetto a un approccio monolitico tradizionale, dunque, un’architettura basata sui microservizi consente di suddividere una app nelle sue funzioni di base. Questo consente allo sviluppatore di poter compilare e implementare ogni funzione in modo indipendente. Il vantaggio di questo tipo di programmazione è che i singoli servizi possono funzionare o non funzionare senza che gli altri servizi ne siano impattati. Supponiamo di avere un’architettura basata su un sistema che può contare anche più di un centinaio di microservizi. Come si fornisce un punto di accesso unificato a ciascun servizio? La risposta è che il processo viene risolto facilmente con l’aiuto di un API gateway. In un’architettura a microservizi, ogni microservizio è predisposto per un set di endpoint specifici. Questo può influire sulla comunicazione da client a microservizio. Quando ogni microservizio ha un endpoint pubblico, non solo si ottiene una migliore integrazione ma si stanno supportando al meglio tutti gli obiettivi aziendali. I microservizi sono ospitati all'interno di Kubernetes e alimentati da Dapr, il Distributed Application Runtime. Dapr offre una raccolta di utilità e blocchi predefiniti che aiutano gli sviluppatori a creare applicazioni distribuite scalabili e resilienti.
![L2 - Containers](./assets/resources/c4-l2-be.png "L2 - Containers")

## L3 - Progressive Web Application Components

**Scompone i container in componenti correlati e mette in relazione questi ultimi con altri container o altri sistemi**

L'architettura del client di un progetto sviluppato con il CA-Platform, prevede la suddivisione in 3 differenti layer: "Application", "Domain" e "Scenario". Il progetto può essere costituito da più "Application", descritte da più "Domain", a loro volta rappresentati da più "Scenario". Ciascun layer può definire al suo interno componenti grafici, servizi singleton, pipes per la trasformazione di dati per la visualizzazione, HUB SignalR, Data Transfer Object ed operations, oltre a poter instaurare comunicazioni specifiche con determinati microservizi (es. solo lo scenario "Clienti" utilizza il microservizio "AnagraficheClienti"). Ciascun container condivide tutte queste informazioni con i container figli, ad esempio definendo un componente grafico a livello di applicazione, tutti i domini e tutti gli scenari potranno utilizzarlo; definendolo invece a livello di dominio, solo il dominio stesso e gli scenari di quest ultimo potranno utilizzarlo; definendolo infine a livello di scenario, solo quest ultimo sarà in grado di istanziarlo; la medesima ereditarietà vale per l'inclusione dei servizi: includendo un microservizio nella definizione di una applicazione, tutti gli scenari e tutti i domini saranno in grado di interrogarlo; includendolo invece in uno scenario, solo tale scenario sarà in grado di interrogarlo, e così via.
![L3 - Progressive Web Application Components](./assets/resources/c4-l3-fe.png "L3 - Progressive Web Application Components")

## L3 - Back-End Components

**Scompone i container in componenti correlati e mette in relazione questi ultimi con altri container o altri sistemi**

Il CA-Platform sposa il modello dei microservizi e il back-end generato sarà composto da molti microservizi indipendenti. Un microservizio è definito da un insieme di caratteristiche. Un microservizio dovrebbe essere:

- **Piccolo**: è abbastanza semplice da comprendere con poco sforzo; come regola generale, dovrebbe essere riscrivibile in poche settimane
- **Focalizzato su un task**: se visto dall'esterno, un microservizio dovrebbe affrontare un'unica preoccupazione del dominio del problema; tuttavia, se visto dall'interno, può svolgere tale compito eseguendo operazioni complesse
- **Allineato con un bounded context**: ogni microservizio ha la sua parte del dominio del problema e la sua rappresentazione interna dovrebbe essere indipendente dagli altri microservizi
Autonomo: può cambiare la sua attuazione e crescere senza coordinarsi e interferire con gli altri
- **Distribuibile in modo indipendente**: può essere costruito, testato e distribuito indipendentemente dagli altri
- **Debolmente accoppiato**: la sua rappresentazione interna del modello non perde all'esterno; la comunicazione con altri microservizi avviene tramite API e contratti pubblici

![L3 - Back-End Components](./assets/resources/c4-l3-be.png "L3 - Back-End Components")

Queste caratteristiche rendono il modello di microservizi un'ottima strategia di disaccoppiamento per le applicazioni distribuite. Il CA-Platform permette di generare e configurare una service mesh. In una service mesh, le richieste sono indirizzate tra i microservizi attraverso proxy presenti nel livello dell'infrastruttura. I singoli proxy che compongono una service mesh sono chiamati "sidecar": si muovono a fianco di ogni servizio, anziché al loro interno. Tutti questi proxy "sidecar", disaccoppiati da ogni servizio, formano insieme una rete di mesh.

## Envoy Proxy

Envoy è un proxy distribuito C++ ad alte prestazioni progettato per singoli servizi e applicazioni, nonché un bus di comunicazione e un "piano dati universale" progettato per architetture "service mesh" di grandi microservizi. Basato sull'apprendimento di soluzioni come NGINX, HAProxy, bilanciamento del carico hardware e bilanciamento del carico cloud, Envoy viene eseguito insieme ad ogni applicazione ed astrae la rete fornendo funzionalità comuni in modo indipendente dalla piattaforma. Quando tutto il traffico dei servizi in un'infrastruttura scorre attraverso una mesh di Envoy, diventa facile visualizzare le aree problematiche tramite un'osservabilità coerente, ottimizzare le prestazioni complessive e aggiungere funzionalità di substrato in un'unica posizione. 
Envoy funziona con qualsiasi linguaggio. Una singola distribuzione di Envoy può formare una rete tra Java, C++, Go, PHP, Python, ecc. Sta diventando sempre più comune per le architetture orientate ai servizi utilizzare più framework e linguaggi applicativi. 
Envoy colma il divario in modo trasparente. In un'architettura orientata ai servizi, l'implementazione degli aggiornamenti delle librerie può essere incredibilmente doloroso. Envoy può essere distribuito e aggiornato rapidamente su un'intera infrastruttura in modo trasparente. Altre funzionalità incluse con Envoy sono: Service discovery and dynamic configuration, Health checking, Advanced load balancing, Observability, gRPC. 
![Envoy Proxy](./assets/resources/envoy.png "Envoy Proxy")
Il CA-Platform usa Envoy per generare senza sforzo API Gateway da un file di configurazione YAML. Per ogni modello di un gateway, verrà generato un nuovo file Envoy; il nome del gateway sarà il prefisso del file YAML di Envoy, che contiene le istruzioni per la generazione del gateway. Ogni file genererà un processo costituito da un singolo gateway, le cui caratteristiche sono definite nella sezione `listener` del file. I servizi invocati dal gateway sono definiti nella sezione `cluster`. Un API proxy è un boundary service che funge da intermediario tra un client e i microservizi. Il suo obiettivo è incapsulare il cluster di microservizi, nascondendo la vera origine delle risorse richieste: questo permette di disaccoppiare ulteriormente il client dal server, permettendo a quest ultimo di cambiare strutturalmente senza rompere il client. Il CA-Platform implementa due tipi di proxy: gateway e aggregator.

## API Proxies - The Gateway pattern

Un gateway è un tipo di reverse proxy che funge da punto di ingresso nell'applicazione da tutto ciò che è esterno al cluster di microservizi. Un client esegue una richiesta al gateway e vedrà la risposta proveniente dal gateway come se fosse prodotta da quest ultimo; invece, il gateway reindirizza la richiesta al microservizio in grado di gestirla e restituisce al client qualsiasi risposta prodotta dal microservizio. È simile a una façade nella programmazione orientata agli oggetti. Il motivo principale per cui è necessario un gateway in un'applicazione distribuita è che nasconde la struttura interna del cluster di microservizi, nonché altre feature, come i protocolli utilizzati dai servizi. 
![API Proxies - The Gateway pattern](./assets/resources/gatewayms.png "API Proxies - The Gateway pattern")
Immaginiamo di avere un microservizio esposto direttamente al client e che quest ultima inizi a crescere man mano che l'applicazione viene sviluppata, al punto da diventare troppo grande per essere considerato un microservizio. Nascerebbe quindi l'esigenza di voler dividerlo in più parti, ma creando grossi problemi a qualsiasi client che utilizza il servizio stesso. Un API gateway risolve il problema: il suo contratto non cambia, cambierà solo il comportamento di routing in modo da reindirizzare le richieste ai microservizi appena creati. Per applicazioni relativamente semplici, un singolo gateway può essere sufficiente. Tuttavia, poiché un'applicazione cresce in dimensioni, utilizzo e funzionalità, avere un solo gateway non è pratico, poiché l'applicazione avrà bisogno di sempre più funzionalità, come bilanciamento del carico, composizione API, autenticazione, traduzione del protocollo, ecc. Vediamo come possiamo estendere il modello gateway introducendo gateway sempre più specializzati nel paragrafo successivo.

## API Proxies - The BFF pattern

Il pattern Backends For Frontends (BFF) entra in gioco quando ad un server accede più di un client. Supponiamo che un team front-end sviluppi un client SPA e un client mobile. Questi client molto spesso avranno esigenze diverse, che non possono essere affrontate facilmente da un unico gateway generico. Ad esempio, il client mobile potrebbe aver bisogno di meno dati e utilizzare DTO più leggeri rispetto al client SPA, oltre a essere coinvolto in flussi di dati e operazioni completamente diversi. Di conseguenza, l'unico gateway si gonfierà di tutte queste funzionalità e il team che lavora sul gateway avrà un'esperienza di sviluppo peggiore. 
![API Proxies - The BFF pattern](./assets/resources/bff.png "API Proxies - The BFF pattern")
Un modo per risolvere questo problema consiste nell'avere un gateway per esperienza utente. Ciascun gateway, divenuto ormai un back-end per il front-end, sarà specializzato su un'unica esperienza utente che, tuttavia, potrebbe essere la stessa per più client (ad esempio, un'app iOS e un'app Android potrebbero utilizzare lo stessa gateway se le loro esigenze sono simili). L'utilizzo del modello BFF offre altri vantaggi. I gateway sono separati l'uno dall'altro, il che migliora l'affidabilità: se uno di essi si guasta, non influisce sull'altro. Migliora anche la disponibilità, perché è in esecuzione più di un processo gateway. Anche l'osservabilità è migliorata, perché le chiamate al back-end sono separate e raggruppate per tipo di client. Il modello di un gateway è molto semplice. Basta fornire un nome, una descrizione e un elenco di servizi a cui concederà l'accesso. Il file bff.yaml conterrà l'elenco dei gateway che verranno generati.
```yaml
- name: Mobile
  type: gateway
  description: Mobile BFF
  services:
    - Couriers
    - Logistics
- name: SPA
  type: gateway
  description: SPA BFF
  services:
    - Store
    - Logistics
```

## API Proxies - The Aggregator pattern

In un'architettura a microservizi, non sono rare le situazioni in cui più di un servizio è coinvolto in una singola operazione. Spesso i dati devono essere recuperati da diversi microservizi e combinati. Sebbene questa operazione possa essere eseguita da un client, a volte è meglio avere un servizio separato del cluster che lo faccia. Supponiamo che un client debba combinare oggetti dati provenienti da tre servizi separati per visualizzarli in un'unica pagina. In alcuni casi, ciò potrebbe causare problemi di prestazioni che si tradurranno in una scarsa esperienza utente. Internet ha una latenza molto più alta di una LAN. Sebbene questo possa non essere un problema quando le tre richieste possono essere eseguite in parallelo, ci sono occasioni in cui le richieste devono essere emesse in sequenza; in tali scenari, avere un servizio dedicato che esegue questo lavoro può velocizzare notevolmente l'intera operazione. Inoltre, l'implementazione della composizione API all'interno del codice client è una distrazione per uno sviluppatore client, il cui compito principale è creare un'ottima esperienza utente. 
![API Proxies - The Aggregator pattern](./assets/resources/aggregator.png "API Proxies - The Aggregator pattern")
Un aggregatore è un servizio come un altro, pur essendo più semplice di un normale servizio e più complesso di un semplice gateway. Gli aggregatori non hanno un modello di dominio e, quindi, entità di database. Ecco un esempio di come modellare un aggregatore:

```yaml
name: MyAggregator
type: service
aggregator: true
description: Aggregates some services
namespace: Ca.ShoppingCart.MyAggregator
services:
  - Store
  - Logistics
contracts:
  - name: Product
    description: Product entity
    type: entity
    fields:
      - name: name
        type: string
        description: The name of the product
      - name: description
        type: string
        description: A description of the product
      - name: price
        type: decimal
        description: How much the product costs
      - name: imageId
        type: uuid
        description: The id of the image representing the product
      - name: imageDescription
        type: string
        description: The description of the image representing the product
operations:
  - name: getProductWithWeight
    type: http_get
    description: Gets a product with its weight
    parameters:
      - name: id
        type: uuid
        description: The id of the product
        direction: in
      - name: product
        type: Product
        description: The found product
        direction: retval
      - name: weight
        type: float
        description: The weight of the product
```

Questo YAML genera un servizio con classi proxy predefinite che possono essere utilizzate per accedere ai microservizi elencati nella sezione servizi di YAML, nonché a DTO e metodi di controllo come in qualsiasi altro servizio.

## DAPR

Dapr, o Distributed Application Runtime, è un nuovo modo per creare applicazioni distribuite moderne. Ciò che è iniziato come prototipo si è evoluto in un progetto open source di grande successo. Il suo sponsor, Microsoft, ha stretto una stretta collaborazione con i clienti e la community open source per progettare e creare Dapr. Il progetto Dapr riunisce sviluppatori di qualsiasi background per risolvere alcune delle sfide più difficili dello sviluppo di applicazioni distribuite. Dapr risolve una sfida di grandi dimensioni intrinseca nelle applicazioni distribuite moderne: complessità. Grazie a un'architettura di componenti collegabili, Dapr semplifica notevolmente il plumbing dietro le applicazioni distribuite. 

![DAPR](./assets/resources/dapr.png "DAPR")

Fornisce un collante dinamico che associa l'applicazione alle funzionalità dell'infrastruttura del runtime Dapr. Considerare un requisito per rendere uno dei servizi con stato? Quale sarebbe la progettazione. È possibile scrivere codice personalizzato destinato a un archivio stati, ad esempio Cache Redis. Tuttavia, Dapr offre funzionalità di gestione dello stato integrate. Il servizio richiama il blocco predefinito di gestione dello stato Dapr che viene associato dinamicamente a un componente dell'archivio stati tramite un file yaml di configurazione del componente Dapr. Dapr viene fornito con diversi componenti predefiniti dell'archivio stati, tra cui Redis. Con questo modello, il servizio delega la gestione dello stato al runtime Dapr. Il servizio non dispone di SDK, libreria o riferimento diretto al componente sottostante. È anche possibile modificare gli archivi stati, ad esempio, da Redis a MySQL o Cassandra, senza modifiche al codice. Dapr include il supporto per Go, Node.js, Python, .NET, Java e JavaScript. Mentre gli SDK specifici del linguaggio migliorano l'esperienza degli sviluppatori, Dapr è indipendente dalla piattaforma. Il modello di programmazione dapr espone le funzionalità tramite protocolli di comunicazione HTTP/gRPC standard. Qualsiasi piattaforma di programmazione può chiamare Dapr tramite le API HTTP e gRPC native. Dapr fornisce i seguenti servizi di infrastruttura:

- **State Management**: Supporto di informazioni contestuali per i servizi con stato a esecuzione lunga
- **Service Invocation**: Richiamare chiamate da servizio a servizio dirette e sicure usando protocolli indipendenti dalla piattaforma ed endpoint noti
- **Pub/Sub**: Implementare la messaggistica pub/sub sicura e scalabile tra i servizi
- **Bindings**: Attivare il codice dagli eventi generati da risorse esterne con comunicazione bidirezionale
- **Actors**: Incapsulare la logica e i dati in oggetti actor riutilizzabili
- **Secrets**: Accedere in modo sicuro agli archivi segreti esterni
- **Observability**: Monitorare e misurare le chiamate ai messaggi tra servizi in rete

## Docker

Docker è una tecnologia di containerizzazione che consente la creazione e l'utilizzo dei container Linux. Docker, considera i container come macchine virtuali modulari estremamente leggere, offrendo la flessibilità di creare, distribuire, copiare e spostare i container da un ambiente all'altro, ottimizzando così le app per il cloud. La tecnologia Docker utilizza il kernel di Linux e le sue funzionalità, come Cgroups e namespace, per isolare i processi in modo da poterli eseguire in maniera indipendente. Questa indipendenza è l'obiettivo dei container: la capacità di eseguire più processi e applicazioni in modo separato per sfruttare al meglio l'infrastruttura esistente pur conservando il livello di sicurezza che sarebbe garantito dalla presenza di sistemi separati. Gli strumenti per la creazione di container, come Docker, consentono il deployment a partire da un'immagine. Ciò semplifica la condivisione di un'applicazione o di un insieme di servizi, con tutte le loro dipendenze, nei vari ambienti. Docker automatizza anche la distribuzione dell'applicazione (o dei processi che compongono un'applicazione) all'interno dell'ambiente containerizzato. Gli strumenti sviluppati partendo dai container Linux, responsabili dell'unicità e della semplicità di utilizzo di Docker, offrono agli utenti accesso alle applicazioni, la capacità di eseguire un deployment rapido, e il controllo sulla distribuzione di nuove versioni. L'approccio Docker alla containerizzazione si basa sulla capacità di estrarre i singoli componenti di un'applicazione, da aggiornare o riparare. Oltre a questo approccio basato sui microservizi, è possibile condividere i processi tra più applicazioni in modo molto simile a quello usato dalla Service-Oriented Architecture (SOA). 
![Docker](./assets/resources/docker.png "Docker")
Ogni file immagine Docker è composto da più strati, che insieme costituiscono una singola immagine. Uno strato viene creato ad ogni modifica dell'immagine. Ogni volta in cui un utente specifica un comando (es. run o copy), viene creato un nuovo strato. Docker riutilizza questi strati per velocizzare il processo di creazione dei container. Le modifiche sono condivise tra le immagini, migliorando ulteriormente la velocità, la dimensione e l'efficienza. Il controllo delle versioni fa parte del processo di stratificazione. Ogni volta che viene apportata una modifica, il registro delle modifiche offre il controllo totale sulle immagini containerizzate. Uno dei maggiori vantaggi della stratificazione è la capacità di eseguire il rollback. Ogni immagine è composta da strati. Se l'iterazione di un'immagine non è soddisfacente, è possibile riportala alla versione precedente. Ciò consente uno sviluppo agile e aiuta a ottenere l'integrazione e il deployment continui (CI/CD). In passato, la configurazione, l'esecuzione e il provisioning di un nuovo hardware richiedevano giorni e notevoli investimenti. I container basati su Docker possono ridurre il deployment a pochi secondi. Creando un container per ogni processo, puoi condividere con rapidità i processi simili con le nuove applicazioni. Poiché non è necessario riavviare un sistema operativo per aggiungere o spostare un container, i tempi per il deployment sono sostanzialmente più brevi. Inoltre, grazie alla velocità del deployment, attraverso i container è possibile creare ed eliminare dati in modo sicuro, semplice ed economico. Dunque, la tecnologia Docker è caratterizzata da un approccio basato sui microservizi granulare e controllabile, per un ambiente IT più efficiente.

## Contracts

I contratti software sono l'insieme delle definizioni delle operazioni e della struttura dei dati utilizzati per tali operazioni. Lo scopo di un contratto è stabilire una descrizione obiettiva e indipendente dalla lingua di un'API, ovvero quali dati accetta e restituisce e in quale forma. I contratti sono usati per aiutare a disaccoppiare lo sviluppo delle API e dei loro consumer: un'API può evolversi internamente e cambiare il suo comportamento interno ma, fintanto che onora i contratti stabiliti, non infrangerà alcun codice di consumo.

![Contracts](./assets/resources/contracts.png "Contracts")

## DTOs

I Data Transfer Objects (DTO) sono oggetti che contengono solo i dati che vengono trasferiti tra i processi. Non hanno alcun comportamento, tranne che per l'archiviazione dei dati e per la serializzazione e la deserializzazione. I DTO vengono generati nella cartella "Contracts" del progetto applicativo. Normalmente prendono il nome dall'operazione in cui sono coinvolti, con il suffisso 'Request' o 'Response', a seconda della loro natura. Alcuni DTO rappresentano entità e non hanno tali suffissi: possono essere utilizzati in più di un'operazione per evitare che il numero di classi DTO esploda durante lo sviluppo dell'API. Normalmente ereditano dalla classe `EntityDTO`, che contiene solo l'id dell'entità a cui è associato il DTO.

![DTO](./assets/resources/dto.png "DTO")

## Operations

Una operations è un'azione che viene eseguita sull'API quando viene inviata una richiesta all'endpoint dell'operazione. Sono implementati tramite il protocollo HTTP, quindi ogni operation è composta da una richiesta HTTP e da una risposta HTTP. La richiesta è definita dal suo url, dal suo verbo HTTP (ad es. GET, POST, DELETE) e da ogni possibile parametro con cui può arrivare, come il corpo della richiesta. La risposta viene fornita con un codice di stato HTTP e, possibilmente, un corpo della risposta. La richiesta e la risposta dell'operazione, insieme ai loro membri descritti in precedenza, definiscono il contratto per quell'operazione.

![Operations](./assets/resources/operations.png "Operations")

## Data Context

Una classe DataContext (che è un alias per DbContext) estende la classe DbContext e fornisce i mapping tra le entità del modello e le tabelle del database, nonché altre funzionalità di configurazione; può anche contenere proprietà `DbSet`.

![Data Context](./assets/resources/datacontext.png "Data Context")

## Data Seed

Una classe DataSeed è responsabile del seeding del database con i valori iniziali. Contiene un metodo `Init` in cui avviene l'operazione di seeding. Questo metodo accetta un'istanza `ISeeder` che espone un metodo `Seed`. Questo metodo popolerà il database con un numero di entità di qualsiasi tipo mappate su una tabella.

![Data Seed](./assets/resources/dataseed.png "Data Seed")

## Migrations

![Migrations](./assets/resources/migrations.png "Migrations")

Le migrazioni contengono istruzioni per la creazione e il seeding del database e possono essere salvate e ripristinate. Vengono generati automaticamente da Entity Framework Core con il comando "Add-Migration". Per garantire che il database venga migrato correttamente, puoi utilizzare il metodo `Migrate` sulla proprietà `Database` del contesto dei dati. Quindi è possibile eseguire il seeding del database utilizzando il metodo di estensione "Seed" dell'ambito.

```cs
public static void Main(string[] args)
{
    IHost host = CreateHostBuilder(args).Build();

    using (IServiceScope scope = host.Services.CreateScope())
    {
        IServiceProvider services = scope.ServiceProvider;

        StoreDataContext context = services.GetRequiredService<StoreDataContext>();
        context.Database.Migrate();

        scope.Seed<StoreDataSeed>();
    }

    host.Run();
}
```
## Microservice Architecture

Il CA-Platform sposa il modello dei microservizi e il back-end generato sarà composto da molti microservizi indipendenti. Un microservizio è definito da un insieme di caratteristiche. Un microservizio dovrebbe essere:

- **Piccolo**: è abbastanza semplice da comprendere con poco sforzo; come regola generale, dovrebbe essere riscrivibile in poche settimane
- **Focalizzato su un task**: se visto dall'esterno, un microservizio dovrebbe affrontare un'unica preoccupazione del dominio del problema; tuttavia, se visto dall'interno, può svolgere tale compito eseguendo operazioni complesse
- **Allineato con un bounded context**: ogni microservizio ha la sua parte del dominio del problema e la sua rappresentazione interna dovrebbe essere indipendente dagli altri microservizi
- **Autonomo**: può cambiare la sua attuazione e crescere senza coordinarsi e interferire con gli altri
- **Distribuibile in modo indipendente**: può essere costruito, testato e distribuito indipendentemente dagli altri
- **Debolmente accoppiato**: la sua rappresentazione interna del modello non perde all'esterno; la comunicazione con altri microservizi avviene tramite API e contratti pubblici

![Microservice Architecture](./assets/resources/microservice_architecture.png "Microservice Architecture")
Queste caratteristiche rendono il modello di microservizi un'ottima strategia di disaccoppiamento per le applicazioni distribuite. Il CA-Platform permette di generare e configurare una service mesh. In una service mesh, le richieste sono indirizzate tra i microservizi attraverso proxy presenti nel livello dell'infrastruttura. I singoli proxy che compongono una service mesh sono chiamati "sidecar": si muovono a fianco di ogni servizio, anziché al loro interno. Tutti questi proxy "sidecar", disaccoppiati da ogni servizio, formano insieme una rete di mesh.

Un unico servizio contiene normalmente le cartelle Domain e Infrastructure, che possono essere eventualmente estratte in progetti separati.

![Microservicea project structure](./assets/resources/microservice-structure-proj.png "Microservicea project structure")

### Domain Layer
Il progetto Domain (Ca.ShoppingCart.Store.Domain) contiene tutte le conoscenze relative al dominio, ad es. concetti e regole aziendali. Questo è il nucleo del progetto e non dovrebbe dipendere da altri livelli, ovvero questo progetto non dovrebbe fare riferimento agli altri due. Per questo progetto vengono generate automaticamente tre cartelle.

#### Model
Questa cartella contiene entità di dominio, oggetti valore e così via. Il modello dovrebbe seguire i principi "persistence ignorance" e "infrastructure ignorance": le entità non dovrebbero avere dipendenze dal livello di accesso ai dati (ad esempio, implementando qualsiasi tipo definito dal framework di persistenza). Normalmente si desidera progettare il proprio modello indipendentemente dal livello di persistenza, ma ciò non è sempre possibile: possono esserci dei vincoli che possono essere dovuti sia alla tecnologia di archiviazione che alla tecnologia ORM.

#### Messaging
Ospita le classi di messaggi, ovvero i contratti che rappresentano le informazioni scambiate tra i microservizi durante la messaggistica (pub/sub). Ogni microservizio definisce i propri messaggi e, per una comunicazione efficace, tali contratti devono concordare. Avere classi separate invece di definirle in un progetto comune è fondamentale in un'architettura basata su microservizi per consentire a ciascun microservizio di evolversi in modo indipendente. Gli sviluppatori sono responsabili di mantenere sincronizzati i contratti in tutti i microservizi mentre l'applicazione cresce.

#### Repositories
Se utilizzi il modello del repository, le interfacce del repository verranno generate automaticamente. Questa cartella contiene le interfacce dei repository generati.

### Infrastructure Layer
Infrastructure riguarda principalmente la persistenza dei dati. La cartella conterrà la logica relativa a ORM e le implementazioni dei repository, nel caso in cui venga utilizzato il repository pattern. Il CA-Platform e Dapr si occupano della maggior parte dell'infrastruttura, ma questo livello può contenere utilità personalizzate relative all'infrastruttura. Questo progetto può contenere anche le implementazioni delle classi di servizio se si utilizza un livello di servizio; tuttavia, tali implementazioni possono essere definite anche nella folder Domain, se non devono dipendere dalle implementazioni dell'infrastruttura. Ad esempio, se si stanno usando il repository pattern ed EntityFramework Core, si utilizzeranno repository astratti, che sono definiti all'interno della cartella Domain, invece del DbContext direttamente: in questo caso, le implementazioni del servizio possono risiedere anche all'interno del cartella Domain; viceversa, se si fa riferimento all'applicazione DbContext direttamente all'interno del proprio livello di servizio, questa deve essere implementata nella cartella Infrastructure, per mantenere le corrette dipendenze tra i progetti. Per impostazione predefinita, viene generata automaticamente solo la cartella Repository.

#### Repositories
Questa cartella conterrà le implementazioni del repository e l'implementazione di UnitOfWork. Le implementazioni predefinite sono basate su Entity Framework Core, ma questa cartella può contenere anche altre implementazioni

### Application Layer
Definisce l'API pubblica che il servizio espone al mondo esterno. Questo livello non dovrebbe contenere business logic o logica di dominio: è responsabile della delega del lavoro in risposta alle interazioni con altri sistemi e dovrebbe essere mantenuto sottile. Per questo progetto vengono generate automaticamente tre cartelle.

#### Dto
Questa cartella contiene tutti i Data Transfer Objects (DTO) che un client potrebbe utilizzare per comunicare con il servizio. Un DTO è una struttura di dati il ​​cui unico scopo è trasportare dati tra il client e il server. Un DTO è un oggetto POCO che contiene solo proprietà (getter e setter) e non ha alcun comportamento.

#### Controllers
Questa cartella ospita le classi del controller ASP.NET Core. I metodi di un controller vengono generati dal file yaml del microservizio. Una classe controller di base astratta conterrà le definizioni del metodo astratto, in modo che possano essere implementate nel controller concreto.

#### Hubs
Questa cartella contiene gli Hub SignalR del microservizio

#### Mappings
Questa cartella contiene le classi di mapping. Per impostazione predefinita, qui vengono generati i profili di AutoMapper, ma questa cartella può contenere anche classi e funzioni di mapping personalizzate

## Project structure
L'architettura del client di un progetto sviluppato con il CA-Platform, prevede la suddivisione in 3 differenti layer: "Application", "Domain" e "Scenario". Il progetto può essere costituito da più "Application", descritte da più "Domain", a loro volta rappresentati da più "Scenario". Ciascun layer può definire al suo interno componenti grafici, servizi singleton, pipes per la trasformazione di dati per la visualizzazione, HUB SignalR, Data Transfer Object ed operations, oltre a poter instaurare comunicazioni specifiche con determinati microservizi (es. solo lo scenario "Clienti" utilizza il microservizio "AnagraficheClienti"). Ciascun container condivide tutte queste informazioni con i container figli, ad esempio definendo un componente grafico a livello di applicazione, tutti i domini e tutti gli scenari potranno utilizzarlo; definendolo invece a livello di dominio, solo il dominio stesso e gli scenari di quest ultimo potranno utilizzarlo; definendolo infine a livello di scenario, solo quest ultimo sarà in grado di istanziarlo; la medesima ereditarietà vale per l'inclusione dei servizi: includendo un microservizio nella definizione di una applicazione, tutti gli scenari e tutti i domini saranno in grado di interrogarlo; includendolo invece in uno scenario, solo tale scenario sarà in grado di interrogarlo, e così via.

![Project structure](./assets/resources/scaffold.PNG "Project structure")

- **Application Layer/Container**: L'Application rappresenta il layer/container principale del progetto. Tale container condivide le sue informazioni con tutti i Domain e gli Scenarios figli.
- **Domain Layer/Container**: Il Domain rappresenta uno specifico ambito funzionale dell'Application. Tale container condivide le sue informazioni con tutti gli Scenarios figli ed eredita le informazione dell'Application.

- **Scenario Layer/Container**: Lo Scenario rappresenta il container più atomico dell'architettura ed eredita tutte le informazioni dal Domain e dell'Application di appartenenza.

- **Service**: Il Service rappresenta il microservizio vero e proprio. Può essere aperto nella solution del back-end o semplicemente singolarmente nella solution che mette a disposizione.

- **Struttura del progetto**: Lo scaffold del progetto è costituito da 3 folder principali:


  - *client*: la folder client contiene la single page application basata sull'ultima versione di Angular e Typescript. Le SPA o Single Page Application sono applicazioni web fruibili come singola pagina senza necessità di caricamento per pagine. Applicazioni che permettono di ricreare nel web esperienze utenti simili alle applicazioni tradizionali hanno lo scopo di fornire una user experience fluida e rapida, senza interruzioni né fastidiose pause di caricamento. Di fatto, una single page app ha comportamenti simili alle applicazioni desktop su qualunque pc – perdendo alcune caratteristiche tipiche dei siti Web tradizionali (tempi di caricamento di pagina, necessità di caricamento completo dei dati etc), ma mantiene i vantaggi di essere perfettamente disponibile sul Web senza bisogno d’installazione. In sostanza, l’applicazione SPA contiene in sé l’intero codice necessario per funzionare e le risorse ad essa associate vengono caricate dinamicamente solo quando servono, in risposta a precise azioni da parte dell’utente.
  ![Client structure](./assets/resources/client-scaffold.png "Client structure")
  - *server*: la folder server contiene il back-end dell'applicazione. Il back-end è scritto in .NET 5 ed implementa il modello dei microservizi. Un microservizio è una parte piccola e indipendente dell'applicazione focalizzata su una singola attività. Questo approccio rende l'intera applicazione modulare, altamente manutenibile, facilmente testabile e debolmente accoppiata.
  ![Server structure](./assets/resources/server-ms-scaffold.png "Server structure")
  - *codegen*: la folder codegen contiene tutti i file YAML che verranno inviati al Codegen Engine per generare una congrua parte del codebase dell'applicazione nella folder "model", gli override dei template nella folder "templates" e le configurazioni di generazione nella folder "configs"..  Per maggior dettagli sulla generazione del codice, visita la sezione "Codegen"
  ![Codegen](./assets/resources/codegen-scaffold.PNG "Codegen")
- **Struttura dei container**: tutti i container presenti sul client (application,domain e scenario) sono strutturalmente omogenei. Anche i servizi generati lato back-end presentano una struttura standard ed omogenea con gli altri servizi
  - application
  ![Application container](./assets/resources/container-application-fe-sample.png "Application container")
  - domain
  ![Domain container](./assets/resources/container-domain-fe-sample.png "Domain container")
  - scenario
  ![Scenario container](./assets/resources/container-scenario-fe-sample.png "Scenario container")
  - service
  ![Service container](./assets/resources/container-service-sample.png "Service container")


Lato Server i file generati sono i seguenti:

- **Dapr**: Contiene i file di configurazione di Dapr, organizzati in due sottocartelle (components e configuration). La prima sottocartella (components) contiene i file di configurazione per i building block predefiniti di Dapr, ad esempio state store, pubsub, ecc., mentre la seconda sottocartella (configuration) contiene i file di configurazione globali.
- **Envoy**: Contiene i file di configurazione di Envoy, necessari per la configurazione delle API Gateway
- **docker-compose**: File necessari per il deploy dei container su docker
- **Microservices**: Solution che referenzia i progetti generati per ogni microservizio. Ogni microservizio ha la propria sottocartella e la propria soluzione Visual Studio, che farà riferimento a uno o più progetti di origine e ai progetti di test. Inoltre, ogni sottocartella avrà il proprio modulo Github, per consentire lo sviluppo di ogni progetto separatamente.
  - *ControllerBase*: file contenente la classe astratta relativa al controller principale del microservizio. La classe contiene i metodi astratti relativi alle operations definite nello YAML del servizio di riferimento. Il file non deve essere modificato, in quanto ad ogni ciclo di generazione verrà sovrascritto
  - *Controller*: file che estende la classe astratta del controller e permette l'implementazione dei metodi di quest ultimo. La cartella Controllers contiene inoltre una sottocartella per ciascun controller definito all'interno dei contracts (proprietà "operations" sotto la voce "services" della voce "contracts" dello YAML del servizio).
  - *Hubs*: cartella contenente tutti gli hub signalR del microservizio
  - *Domain*: cartella contenente la logica di persistenza relativa all'infrastruttura come DbContext di Entity Framework Core, la logica di seeding e le migrazioni
  - *Domain/Model*: cartella contenente tutte le entità di dominio definite nello YAML del servizio (voce "entities")
  - *Domain/Services*: cartella contenente tutte le interfacce dei servizi di dominio, tra i quali i servizi generati dal CodeGen per permettere la service-to-service invocation
  - *Dto*: cartella contenente tutti i dto definiti nello YAML del servizio (sotto la voce dto di contracts). La cartella Controllers contiene inoltre una sottocartella per ciascun controller definito all'interno dei contracts (proprietà "dto" sotto la voce "services" della voce "contracts" dello YAML del servizio).
  - *Infrastructure/Data*: cartella contenente i file del DataContext e del DataSeed del microservizio.
  - *Infrastructure/Services*: cartella contenente tutte le classi concrete dei servizi di dominio, tra i quali i servizi generati dal CodeGen per permettere la service-to-service invocation
  - *EspServiceCollectionExtensions**: file contenente le configurazioni/registrazioni dei servizi messi a disposizione nel microservizio
  - *Program*: file contenente la configurazione dell'host builder
  - *Startup*: file di startup del microservizio
  - *DockerFile*: file di configurazione di docker per il singolo microservizio

Lato Client invece:

- **components**: folder contenente tutte le componenti angular utilizzabili nel container e nei container figli.
 **È consigliabile estendere le componenti base messe a disposizione dal CA-Platform. Maggiori dettagli nella sezione "Base Components"**
 **Le componenti base supportano inoltre la sicurezza. Maggiori dettagli sulla sicurezza, nella sezione "Authorization"**
- **hubs**: folder contenente tutti i riferimenti agli Hub SignalR del container e dei container genitori
- **models**: folder contenente tutte le entities del container (file nome-container.ts)
 **Le applicazioni sviluppate con questo strumento, sono nativamente "restartable", grazie ad un oggetto chiamato "Payload", messo a disposizione in ogni scenario. Per maggior dettagli sul payload, visita la sezione "Patterns"**
- **pipes**: folder contenente tutte le pipe angular utilizzabili nel container e nei container figli
- **services**: folder contenente tutte i servizi angular utilizzabili nel container e nei container figli. La folder inoltre contiene (nel file *.common.ts) i delegati per chiamare i metodi dei controller
- **index-component**: componente contenente il router outlet del container. Tutte le rotte di navigazione figlie del container, saranno inglobate all'interno di tale file. Il file è customizzabile liberamente
- **landing-component**: componente di fallback per le rotte
- **module**: ciascun container lato client è rappresentato da un modulo angular caricato dinamicamente al matching della rotta di corrispondenza. Il modulo è pre-configurato con i moduli minimi necessari per rendere il container funzionante e navigabile. E' possibile modificare il modulo (tranne che nei punti di iniezione)
- **routes**: ciascun container lato client è pre-configurato con le rotte di navigazione relative ai container figli, in modo tale da poter permetterne agevolmente la navigazione, senza ulteriori implementazioni. E' possibile modificare il file di rotte (tranne che nei punti di iniezione)

**Macchina a stati dello scenario**: A ciascuno scenario (a differenza degli altri container) è associato una macchina a stati, nella quale uno stato corrisponde alla vista che effettivamente l'utente navigherà ed una transizione tra due stati definisce una azione che viene tradotta in un command. Tale command, quando invocato esegue la navigazione dallo stato di partenza allo stato di arrivo. Tali navigazioni popolano automaticamente uno stack navigazionale memorizzato in un oggetto chiamato "payload". E' possibile invocare il metodo "return" per effettuare un passo indietro nello stack navigazionale. Per effettuare una navigazione da uno stato di uno scenario ad uno stato di un differente scenario, è possibile invocare il metodo "navigate" passando come parametri le informazioni relative al dominio di appartenenza (solo se diverso dal dominio dello stato dello scenario di partenza), allo scenario ed allo stato di arrivo (identificati rispettivamente con le keyword "scenario" e "action").

 **Per maggior dettagli sulle transizioni della macchina a stati di uno scenario, consulta la sezione "Codegen" al paragrafo "NOMNOML"**

 **Le applicazioni sviluppate con il CA-Platform supportano nativamente l'internazionalizzazione. Maggiori dettagli nella sezione "i18n"**

 **Il CA-Platform supporta lo sviluppo di componenti React. Vedi sezione "React"**