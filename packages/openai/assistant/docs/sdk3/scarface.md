# Scarface

INIZIALIZZA, GENERA E SUPPORTA IL TUO PROGETTO

## Scaffolding Tool

![Scarf-ace Scaffolding Tool](assets/resources/logo_scarf-ace.svg "Scarf-ace Scaffolding Tool")

La creazione / configurazione di un nuovo progetto comporta l'impiego di tempo e risorse.

Scarf-Ace è l'innovativo tool di Code Architects che supporta il developer nell'attività quotidiana grazie ad un set completo di task che ottimizzano il modus operandi e ne semplificano il lavoro.

È facilmente incorporabile negli IDE di sviluppo e consente lo svolgimento di operazioni che il programmatore gestisce manualmente. Con l'ausilio di prompt che "intervistano" il developer (scaffolding), questo potente tool permette di configurare in modo veloce e agevole sia l'applicazione che l'ambiente di sviluppo.

Lavorare con Scarf-Ace è un'esperienza innovativa che conferisce una marcia in più al programmatore.

Scarf-Ace è l'anagramma del titolo della celebre pellicola cinematografica e vuol dire "Sciarpa d'Assi", ovvero uno strumento che "avvolge" il developer durante la sua attività.

### Task Explorer

È possibile incorporare i task dello Scarf-Ace direttamente nel Task Explorer di VSCode (in modo tale da evitare di eseguire i comandi da console), installando l'apposita estensione raccomandata "spmeesseman.vscode-taskexplorer". Oltre ai task dello Scarf-Ace, potremo utilizzare altri task per il version control, per la generazione del codice, per il setup dei pacchetti, per le build, per l'avvio ed il debug dell'applicazione, ecc..

![Scarface in Task Explorer](assets/resources/task_explorer_ms-screen.png "Scarface in Task Explorer")

## Scaffold project
Per eseguire lo scaffolding di un nuovo progetto è necessario lanciare il seguente comando nella folder di destinazione. Scarf-Ace proporrà dei prompt al quale l'utente dovrà rispondere per configurare correttamente il progetto. Tra le informazioni più importanti che lo Scarf-Ace richiede, ci sono il nome del progetto, il prefisso dello stesso (che verrà utilizzato anche come prefisso delle componenti), un dominio ed uno scenario di partenza, l'utilizzo di React, ecc...
```bat
ca scarface
```
Shorthand syntax

```bat
ca scar
```
## Gateway

Genera un nuovo application gateway
```bat
ca scarface gateway
```
L'application Gateway è un servizio di bilanciamento del carico del traffico Web che consente di gestire il traffico verso i microservizi. Il gateway consente di prendere decisioni relative al routing basate su altri attributi di una richiesta HTTP, ad esempio il percorso dell'URI o le intestazioni host. Ad esempio, è possibile eseguire il rounting del traffico in base all'URL in ingresso. Lo YAML di tipo gateway permette di generare un application gateway con [ENVOY](https://www.envoyproxy.io/) e di aggiungerne/rimuovere dinamicamente microservizi.

## Microservice
Genera un nuovo microservizio
```bat
ca scarface microservice
```
Un'applicazione distribuita è tipicamente composta da vari microservizi che interagiscono tra loro, dividendosi le funzionalità esposte all'esterno del back-end. È possibile generare un intero microservizio a partire da un singolo file `yaml` che lo descrive.

## Partial
Genera uno YAML parziale che può essere utilizzato per comporre altri YAML di tipo "service"
```bat
ca scarface partial
```
Lo YAML parziale avrà le stesse informazioni dello YAML di tipo "service", ma non produrrà nessun risultato dal punto di vista della generazione. Per dare un senso ad uno yaml parziale, è necessario aggiungerlo sotto la voce "partials" ad un altro YAML di tipo "service". Così facendo, lo YAML parziale andrà a comporre lo YAML nel quale è incluso.

## Application
Genera una nuova applicazione all'interno del progetto
```bat
ca scarface application
```
Possiamo applicare il concetto di multi-applicazione generando una nuova applicazione nel nostro progetto. In questo modo potremo abilitare/disabilitare interi moduli applicativi, oltre che caricarli in modo lazy per non appesantire il caricamento inziale.

## Domain
Genera un nuovo dominio applicativo
```bat
ca scarface domain
```
Lo Scarf-Ace chiederà all'utente in che applicazione generare il nuovo dominio. In questo modo potremo identificare uno specifico contesto applicativo raggruppando successivamente al suo interno scenari concettualmente legati al dominio di appartenenza.

## Scenario
Genera un nuovo scenario a partire da uno specifico dominio
```bat
ca scarface scenario
```
Lo Scarf-Ace chiederà all'utente in che applicazione ed in che dominio generare il nuovo scenario. Lo scenario dunque ci aiuterà a rappresentare in modo specifico un determinato argomento del dominio. In fase di generazione dello scenario, Scarf-Ace ci chiederà di inserire uno o più stati navigazionali e di creare le relative associazioni.

## Scenario State
Genera un nuovo stato (vista navigabile) del workflow navigazionale di uno specifico scenario
```bat
ca scarface state
```
Lo Scarf-Ace chiederà all'utente in che applicazione, in che dominio ed in che scenario generare il nuovo stato navigazionale. In fase di generazione dello stato, Scarf-Ace ci chiederà di associare quest ultimo ad un altro (o più) stato navigazionale.

## Client Component
Genera una nuova ca-component (componente angular che estende una delle componenti base CA)
```bat
ca scarface component
```
Lo Scarf-Ace chiederà all'utente in che modulo generare la nuova componente. E' importante sottolineare che se vogliamo una componente condivisa da tutti i domini e gli scenari dell'applicazione, sarà necessario scegliere il modulo 'Components' (che contiene le componenti applicative). Inoltre l'utente dovrà scegliere di estendere una delle componenti base di framework. Se si sceglie l'opzione entryComponent, la componente sarà utilzzabile con gli aspect decorators (campo template) con il nome delle stessa in lowercase e senza trattini o underscore.

## Client Pipe
Genera una nuova pipe angular
```bat
ca scarface pipe
```
Lo Scarf-Ace chiederà all'utente in che modulo generare la nuova pipe.

## Client Directive
Genera una nuova direttiva angular
```bat
ca scarface directive
```
Lo Scarf-Ace chiederà all'utente in che modulo generare la nuova direttiva.

## Client Service
Genera un nuovo servizio angular
```bat
ca scarface service
```
Lo Scarf-Ace chiederà all'utente in che modulo generare il nuovo servizio. Tutti i servizi saranno "injected in root".

## Override Codegen template
Permette di sovrascrivere un template EJS esistente.
```bat
ca scarface templates
```
Lo Scarf-Ace chiederà all'utente quale template EJS sovrascrivere. L'utente attraverso un prompt, dovrà indicare step by step come arrivare al template corretto (client/server => component/model/... => ...).

## Install BETA
Effettua l'installazione dell'ultima versione BETA di Scarface
```bat
Scarface: Install beta version
```
La versione BETA che si andrà ad installare non è da considersi stabile. Installare solo su precisa indicazione.

## Install STABLE
Effettua l'installazione dell'ultima versione STABLE di Scarface
```bat
Scarface: Install latest version
```

## Migrate Project
Effettua la migrazione del progetto all'ultima versione installata di Scarface
```bat
ca scarface update
```
La migrazione avrà effetto solamente nel caso in cui il file scarface.json del progetto presenti una versione precedente a quella installata sulla macchina. Il task di migrazione potrà apportare modifiche a file esistenti, aggiornare pacchetti e rimuovere file.

## Lint
Esegue i controlli di linting sul progetto del client
```bat
Analyze: Lint
```
Strumento di analisi del codice statico, che viene utilizzato per contrassegnare il codice sorgente con alcuni elementi sospetti e non strutturali.

## Build
Esegue la build dell'applicazione client
```bat
Build: Build Application
```
La build (in dev mode) produce un bundle e tutti i relativi chunk, oltre ai file di source-map per permetterne il debug

## Build (Production Mode)
Esegue la build in modalità "production" dell'applicazione client
```bat
Build: Build Application (production mode)
```
La build (in prod mode) produce un bundle e tutti i relativi chunk, eseguendo anche operazioni di "uglifiying", "minification" ed ottimizzazioni. NON produce file source-map per il debug.

## Clean Solution
Esegue la clean del progetto client
```bat
Build: Clean Solution
```
Con questa operazione, verranno rimossi tutti i pacchetti ed i file di lock del progetto client e del progetto codegen.

## Check for CLI updates
Controlla se ci sono aggiornamenti della CLI di Code Architects
```bat 
CLI: Check for updates
```
La Command Line Interface (CLI) è un tool alimentato da plugin. Tra i plugin troviamo soprattutto Scarface e Codegen.

## Setup CLI
Esegue il setup della CLI di Code Architects
```bat
CLI: Setup
```
La Command Line Interface (CLI) è un tool alimentato da plugin. Tra i plugin troviamo soprattutto Scarface e Codegen.

## Update CLI plugins
Aggiorna tutti i plugin della CLI di Code Architects all'ultima versione disponibile
```bat
CLI: Update plugins
```
La Command Line Interface (CLI) è un tool alimentato da plugin. Tra i plugin troviamo soprattutto Scarface e Codegen.

## Generate all code
Esegue la generazione del codice su tutto il progetto
```bat
Codegen: Generate all code
```
Il plugin Codegen leggerà i file YAML presenti nella folder "models" del progetto "codegen" e genererà il codice sia per la parte client che per la parte server del progetto

## Generate client code
Esegue la generazione del codice sul client del progetto
```bat
Codegen: Generate client code
```
Il plugin Codegen leggerà i file YAML presenti nella folder "models" del progetto "codegen" e genererà il codice per la parte client del progetto

## Generate server code
Esegue la generazione del codice sul server del progetto
```bat
Codegen: Generate server code
```
Il plugin Codegen leggerà i file YAML presenti nella folder "models" del progetto "codegen" e genererà il codice per la parte server del progetto

## Start Application
Avvia il client dell'applicazione
```bat
Debug: Start Application
```
Il client dell'applicazione verrà avviato in DEV Mode

## Start Application for production
Avvia il client dell'applicazione in modalità "Production"
```bat
Debug: Start Application (production mode)
```
Il client dell'applicazione verrà avviato in PROD Mode producendo un bundle e tutti i relativi chunk, eseguendo operazioni di "uglifiying", "minification" ed ottimizzazioni. NON produce file source-map per il debug.

## Debug VSCode Debug
Lancia il client dell'applicazione in modalità DEBUG con VSCode
```bat
Debug: Start Debugging
```
Dopo aver lanciato lo script, sarà necessario recarsi nella sezione "Run and Debug (CTRL+Shift+D)" di VSCode e lanciare la configurazione "Attach Debug". Dopo questi due passaggi sarà possibile eseguire il debugging direttamente in VSCode.

## Login
Esegue il login sul registry
```bat
Project: Login
```
Lanciando questo comando, verrà effettuato il login (npm-login.ps1) sul registry indicato nel file .npmrc dell'applicazione.

## Restore Packages
Esegue il restore di tutti i pacchetti del client e di codegen
```bat
Project: Restore Packages
```
Lanciando questo comando, verranno reinstallati tutti i pacchetti del client dell'applicazione e del progetto codegen

## Setup Packages
Esegue il setup di tutti i pacchetti del client e di codegen
```bat
Project: Setup Packages
```
Lanciando questo comando, verranno installati tutti i pacchetti del client dell'applicazione e del progetto codegen

## Run All Tests
Lancia i test del client dell'applicazione
```bat
Test: Run All Tests
```
Eseguendo il comando, verranno lanciati una sola volta tutti i test del client dell'applicazione

## Watch All Tests
Lancia i test del client dell'applicazione in modalità "watch"
```bat
Test: Watch All Tests
```
Eseguendo il comando, verranno lanciati tutti i test del client dell'applicazione. Dopodichè, lo script non terminerà e resterà in ascolta di eventuali altre modifiche ai test od al codice sorgente. Ad ogni modifica, i test verranno rilanciati.