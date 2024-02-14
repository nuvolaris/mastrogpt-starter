# Troubleshooting

Risoluzione dei Problemi e Soluzioni Raccomandate.

La struttura delle componenti necessarie per il corretto funzionamento del CAEP è la seguente:
```bash
C:\
|
├─ Windows
|  ├─ npm-login.ps1     # file necessario al funzionamento di scarface.
|
├─ dev\
|  ├─ scarface\
│     ├─ .ca\            # cartella dei log generata dall'installer.
│     ├─ back-office\    # folder in cui viene generato il progetto di prova.
│     ├─ download\       # folder di download dei Requirement.
│     ├─ scarface.config.json    # file di configurazione di scarface.
|
Users\
├─ tuoUtente\
|  ├─ .ca             # cartella dei log generata dall'installer.
|  ├─ .npmrc          # file per autenticazione ai pacchetti npm.
│  ├─ AppData\
│  │  ├─ Roaming\
│  │  │  ├─ npm\
│  │  │  ├─ npm-cache\
│  │  │  ├─ NuGet\
│  │  │  │  ├─ Nuget.Config # file per autenticazione ai pacchetti NuGet.
```
In caso di malfunzionamenti, si consiglia di procedere quanto segue:
1. Disinstallare **Node.js**
2. Cancellare le cartelle **`npm`** ed **`npm-cache`** in `C:\\Users\\tuoUtente\\AppData\\Roaming\\` (altrimenti raggiungibili con` %appdata%`).
3. Riavviare l'installer.




### npm ERR! code E401 NTLM
![npm ERR! code E401 NTLM](assets/resources/npm-E401-NTLM.png)
Questo errore si presenta quando il token utilizzato per il login npm:
  - **NON** ha come scope **Tutte le accessibili organizzazioni accessibili**.
  - è scaduto e quindi è stato eliminato.



### npm ERR! code E401 Invalid Token
  
  ![npm ERR! code E401 Invalid Token](assets/resources/npm-E401-TokenInvalid.png)
  Questo errore si presenta quando il token utilizzato per il login npm **non esiste** o **non è corretto**.

### npm ERR! code E403 Forbidden

![npm ERR! code E403 Forbidden](assets/resources/npm-E403-Forbidden.png)
Questo errore si presenta quando non si hanno i permessi per i registry npm. Pertanto bisognerà inviare un'email al seguente indirizzo _**supportoframework@codearchitects.com**_ per richiedere assistenza.


  
### CA-CLI-PLUGIN-CODEGEN non è riconosciuto

![CA-CLI-PLUGIN-CODEGEN non è riconosciuto](assets/resources/ca-cli-plugin-NotRecognized.png)
Questo errore si presenta quando si cerca di eseguire il comando `npm run gen` prima che si sia eseguito il comando `npm i` nella cartella codegen e client.
Pertanto per risolvere l'errore eseguire il comando `npm i` nella cartella codegen e client oppure eseguire il _Task vscode_ **Project: Setup Packages**

## JS heap out of memory

![JS heap out of memory](assets/resources/JS-heap-out-of-memory.png)
Questo errore si presenta quando si supera la Memoria RAM massima a disposizione. In caso si presenta tale errore rieseguire il comando precedente, in quanto non è un problema del Generatore o del CAEP.



## Your Git rm is broken

![your git rm is broken](assets/resources/git-rm-IsBroken.png)

Questo errore si presenta in tre occasioni:

1) E' stato installato **Git a 32-bit**.
   - Per verificare, eseguire il comando `where git` da **CMD**:
     Se l'output è `C:\\Program Files (x86)\\Git\\cmd\\git.exe`, la versione di Git installata è a 32-bit.
    
    Per _risolvere_ il problema disintallare Git dal computer e scaricare la versione a 64-bit dal seguente link [https://git-scm.com/downloads](https://git-scm.com/downloads).

2) Git è installato su u disco diverso da **`C:`**
   - Per verificare, eseguire il comando `where git` da **CMD**:
     - Se l'output è diverso da `C:\\Program Files\\Git\\cmd\\git.exe` :
      
      1) Disinstallare Git e installarlo sul disco C. È possibile scaricare Git dal seguente link [https://git-scm.com/downloads](https://git-scm.com/downloads).
       2) Aggiungere tra le variabili d'ambiente **PATH del Sistema** il percorso **_\<TUO-DISCO>_:\\Program Files\\Git\\usr\\bin**

1) Nelle variabili d'ambiente **PATH del Sistema** non è presente il path `C:\\Program Files\\Git\\usr\\bin\\`.
   - In caso si sia installata la versione di Git a 64-bit sul disco C, ma si presenta ancora questo errore, significa che non è presente la variabile d'ambiente `C:\\Program Files\\Git\\usr\\bin\\` tra le variabili **PATH del Sistema**
    
    Per _risolvere_ questo problema aggiungere il percorso **C:\\Program Files\\Git\\usr\\bin\\** tra le variabili d'ambiente **PATH del Sistema**

## cp is not recognized as an internal command windows

![cp is not recognized](assets/resources/cp-Notrecognized.png)
Questo errore è causato dalla mancanza del percorso **C:\\Program Files\\Git\\usr\\bin\\** nelle variabili d'ambiente **PATH del sistema**.
Per risolvere questo errore bisognerà aggiungere il percorso **C:\\Program Files\\Git\\usr\\bin\\** tra le variabili d'ambiente **PATH del Sistema**
