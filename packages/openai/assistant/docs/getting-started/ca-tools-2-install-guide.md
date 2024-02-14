# I Tools Setup
## Tools Setup

`Code Architects Enterprise Platform` è un framework creato da Code Architects per lo sviluppo RAD di applicazioni di classe enterprise. \

## Requisiti minimi
🗹 Windows 10<sup>`1`</sup> o Windows 10 in Hyper-V<sup>`2`</sup>

🗹 RAM 16 GB

🗹 CPU quad-core (1,85 GHz)

🗹 SSD con 40 GB di spazio disponibile<sup>`3`</sup>

<sup>`1`</sup> Esclusa la versione Windows Insider. \
<sup>`2`</sup> Vedi [Ambienti virtualizzati](#ambienti-virtualizzati).
<sup>`3`</sup> Escluso lo spazio su disco da dedicare ai progetti di sviluppo.



## Elenco dei Tools

Durante l'esecuzione di CaTools.exe verranno installati automaticamente i seguenti tools:<sup>`1`</sup>

**Tools**

🗹 Git `Latest`

🗹 <sup>`1`</sup> Node.js `16.13.1`

🗹 <sup>`2`</sup> npm `8.1.2` 

🗹 DotNet Core `5` e `6 Latest`

🗹 Visual Studio `22`

🗹 Visual Studio Code `Latest`

🗹 WSL: Ubuntu `22.04`

🗹 Docker Desktop `Latest`

<sup>`1`</sup> Alcune versioni potrebbero differire dal tipo di installazione. \
<sup>`2`</sup> Tools di version management per Node.js ed npm ( quali **nvm** o **nodist** ) **NON** sono supportati.



**Windows Features**

🗹  Windows Subsystem for Linux ( `WSL 2` )

🗹  Virtual Machine Platform



**Variabili d'ambiente**

🗹  `PATH`<sup>`1`</sup>
```txt
C:\\windows                           
C:\\windows\\system32                 
C:\\windows\\system32\\wbem                                      
C:\\windows\\system32\\windowspowershell\\v1.0
C:\\Program Files\\Git\\usr\\bin
  ```

<sup>`1`</sup>Puoi visualizzare tali env var digitando su Powershell `$env:PATH`

**Estensioni VS Code**

🗹 Mikael.Angular-BeastCode

🗹 HookyQR.beautify

🗹 donjayamanne.githistory

🗹 christian-kohler.path-intellisense

🗹 vscode-icons-team.vscode-icons

🗹 redhat.vscode-yaml

🗹 ms-vscode.vscode-typescript-tslint-plugin

🗹 msjsdiag.debugger-for-chrome

🗹 spmeesseman.vscode-taskexplorer

🗹 Gruntfuggly.triggertaskonsave

🗹 Angular.ng-template



<div style="page-break-after: always;"></div>

# Check preliminari
🗹 Utente con permessi di amministratore;

🗹 Connessione ad internet attiva;

🗹 Antivirus e/o firewall non devono bloccare il processo di installazione e l'uso dei programmi installati;

🗹 E' necessario scollegarsi dalle VPN


**Raggiungibilità endpoint:**

🗹 https://devops.codearchitects.com:444

🗹 https://registry.npmjs.org

🗹 `ftps://casftp.blob.core.windows.net:22` (repository dei log)<sup>`1`</sup>

<sup>`1`</sup>Non bisogna connettersi con WinSCP per testare la connessione!

**Autenticazione:**

🗹 `Username` e `password` su Azure DevOps forniti da Code Architects.

🗹 Password di default cambiata. Vedi Policy di rinnovo della password

🗹 Un `token` valido generato. Vedi Generazione del Token



# Controllo e Generazione del Token

L’uso dei registry privati su Azure DevOps è concesso solo a chi ha diritti di accesso e credenziali valide grazie all'utilizzo del token.

### Controllo dello stato del Token

Per controllare se sia stato generato correttamente o scaduto, accedere a [questo link](https://devops.codearchitects.com:444/Code\%20Architects/_usersSettings/tokens").
  ![](assets/resources/testToken.jpg)

### Generazione del Token

1. Per crearne uno nuovo nella stessa schermata cliccare su **`+ NEW TOKEN`**.

2. Configurarlo con i seguenti parametri:
 
 🗹 **Organization: `All accessible organization`**.
 
 🗹 **Expiration: `1 anno`**.
 
 🗹 **Scope: `Custom Defined`**, quindi **Packaging: `Read`** (**Creazione Pacchetto: `Lettura`**)
  ![](assets/resources/createToken.jpg)

3. Cliccare **`CREATE`** per confermare.

4. Al termine, assicurarsi di **copiare e salvare il token** in un posto sicuro, servirà in seguito! Per motivi di sicurezza il token **NON** verrà più visualizzato.



# Ambienti virtualizzati
E' supportata l'installazione in ambiente virtualizzato, purchè sia Microsoft **`Hyper-V`** e sia stata abilitata la funzionalità **Nested Virtualization** sulla macchina host.

1. **Assicurarsi che la Macchina Virtuale sia spenta!**
2. Lanciare il seguente comando sulla macchina host:
    ```Powershell
    Set-VMProcessor -VMName <VMName> -ExposeVirtualizationExtensions $true
    ```
     sostituendo **`<VMName>`** con il nome della Virtual Machine su cui si intende installare CAEP.

Per maggiori informazioni, fare riferimento alla [documentazione Microsoft](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/user-guide/nested-virtualization).



# Powershell setup
E' necessario abilitare la macchina (sui cui si installerà il CAEP) all'esecuzione degli script Powershell:

1. Aprire `Powershell 5` ( **assicurarsi di NON lanciare Powershell 7 o le versioni x86** ).
2. Per verificare che sia la versione corretta, lanciare il comando **`$PSVersionTable`**
3. Lanciare il seguente comando:
    ```Powershell
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```
    ![](assets/resources/exePolicy.png)
    Confermare digitando **`A`** (Always Run) e premere invio.

4. Per evitare che l'output si blocchi:
    - Aprire Powershell come amministratore.

        ![](assets/resources/psAdmin.png)
    - Cliccare sulla barra in alto col tasto destro e quindi su **`Properties`**.
        ![](assets/resources/psProperties.png)
    - Disabilitare i flag **`QuickEdit Mode`** e **`Insert Mode`**
        ![](assets/resources/psOptions.jpg)



# Download e run dell'installer

1.  Scaricare `CaTools.zip` da [questo link](https://castorybookbloblwebsite.blob.core.windows.net/caep/latest/Caep.zip).
2. Cliccare col tasto destro sulla cartella scaricata e scegliere **`Extract All...`**
3. Cliccare su **`Browse...`** e scegliere un path di destinazione, infine cliccare su **`Extract`**.
4. Cliccare su `CaTools.exe` per avviarlo



**`N.B.`** La prima volta che viene avviato l'installer comparirà una finestra popup in cui bisognerà inserire `username` e `token` (corrispondente al token in chiaro generato nella sezione `Controllo e Generazione del token` ) :
  
  ![](assets/resources/tokenPrompt.jpg)



# TAB 1 - Check Preliminari

Premendo `[INIZIA]` verranno effettuate le seguenti verifiche sulla tab `[Check Preliminari]` :

🗹 Raggiungibilità endpoint

🗹 Vaiabili d'ambiente

🗹 Windows Features ( WSL2 e VMP )

| Requisito | Esito | Descrizione |
| --- |:---| :--- |
| **WSL** | **X** | Terminato il flusso di installazione verrà eseguito il RIAVVIO della macchina e bisognerà rilanciare l'installer. |


🗹 Proxy

🗹 Virtual Machine

Ciascun requisito darà in output uno **Stato**, che se non soddisfatto verrà segnalato dall'installer e se possibile riparato (come nel caso delle Variabili d'ambiente).<sup>`1`</sup>

<sup>`1`</sup> Nel caso della Virtual Machine bisognerà agire manualmente ( vedi la sezione `Ambienti virtualizzati` ) ;

In caso non vengano raggiunti gli endpoint bisognerà contattare il proprio reparto sistemistico.



# TAB 2 - Check Requisiti

Verranno svolte anche altre operazioni sulla tab `[Check Requisiti]` dopo aver premuto `[INIZIA]` sulla tab `[Check Preliminari]`.

- Una volta terminati i check, si procederà automaticamente ad installare i requisiti segnati in rosso.


A seguire, le legenda sugli step più rilevanti:

| Requisito | Esito | Descrizione |
| --- |:---| :--- |
| Qualsiasi | **Giallo** | E' stata rilevata una versione diversa di un tool già presente sulla macchina ma **NON** soddisfa i requisiti. Disinstallando preventivamente a mano tale versione, sarà possibile rilanciare l'installer per far installare quella corretta. |
| Qualsiasi | **Rosso** | Il tool NON è abilitato/installato sulla macchina. Verrà installato proseguendo con l'installazione.|
| **Docker** | **Rosso** | Se il requisito WSL risulta verde nella stessa sezione di Check, allora al termine del flusso verrà eseguito il LOGOFF se l'installazione va a buon fine. |

Ogni tool all'interno dell'installer genera un otput in cui descrive nello specifico lo stato relativo al tool stesso.



# TAB 3 - Installazione requisiti mancanti

In questa tab verranno svolte operazioni di installazione dei requisiti segnati in rosso nella tab precedente.
- Nel caso non ci fosse alcun requisito non soddisfatto, l'installer eseguirà unicamente il comando `ca scar -s`, generando un progetto di test per verificare che tutto funzioni correttamente.
- Se l'installazione di uno o più requisiti dovesse fallire, nella stessa tab sarà possibile premere il pulsante `[ RETRY ]` .

## Ubuntu
Qualora l'installer debba configurare la distro Ubuntu, comparirà una shell relativa alla sua installazione, in cui nella stessa chiederà di inserire username e password relative alla distro.

**N.B.** **NON** inserire username, password di Code Architects o token come credenziali di Ubuntu!

**N.B.** **`AL TERMINE DELL'INSERIMENTO DELLE CREDENZIALI, CHIUDERE LA SHELL DI UBUNTU PER PROSEGUIRE AUTOMATICAMENTE CON LE ALTRE INSTALLAZIONI!`**



# TAB 4 - Tools

Questa sezione **NON** è disponibile la prima volta che si lancia l'installer, sarà quindi necessario avviare il Check dei Requisiti e l'eventuale ciclo di installazione che partirà in automatico.

Una volta sbloccata, si potranno fare una serie di operazioni:

## Controlla files
Questa funzione permette di controllare la presenza dei seguenti file:

- `.npmrc`
  - ```C:\\Users\\mrossi\\```
- `NuGet.Config`
    - ```C:\\Users\\mrossi\\AppData\\Roaming\\NuGet\\```
- `scarface.config.json`
    - ```C:\\dev\\scarface\\```

Qualora dovessero risultare NON presenti, i file verranno creati VUOTI ( ovvero senza credenziali ) e all'occorrenza apparirà la modale che chiederà di inserire `username` e `token`.



# Autenticazione ai progetti
**A questo punto bisognerà autenticarsi ai progetti mediante la** [Guida di autenticazione ai progetti](./ca-tools-2-projects-auth-guide) .









