# Token generation and credentials update

L’uso dei registry privati su Azure DevOps è concesso solo a chi ha diritti di accesso e credenziali valide grazie all'utilizzo del token.

Un token scaduto restituirà un errore `401`, pertanto sarà necessario crearne uno nuovo.

Per controllare che un token sia stato generato correttamente o scaduto, accedere a [questo link](https://devops.codearchitects.com:444/Code\%20Architects/_usersSettings/tokens").
  ![](assets/resources/testToken.jpg)

## Generazione del Token

1. Per crearne uno nuovo nella stessa schermata cliccare su **`+ NEW TOKEN`**.

2. Configurarlo con i seguenti parametri:
 
 🗹 **Organization: `All accessible organization`**.
 
 🗹 **Expiration: `1 anno`**.
 
 🗹 **Scope: `Custom Defined`**, quindi **Packaging: `Read`** (**Creazione Pacchetto: `Lettura`**)
  ![](assets/resources/createToken.jpg)

3. Cliccare **`CREATE`** per confermare.

4. Al termine, assicurarsi di **copiare e salvare il token** in un posto sicuro, servirà in seguito! Per motivi di sicurezza il token **NON** verrà più visualizzato.



## Aggiorna credenziali

Una volta che il token è stato aggiornato e il CAEP è stato installato in precedenza mediante la [Guida all'installazione](./ca-tools-2-install-guide/), sarà possibile aggiornare le credenziali mediante la funzione `Aggiorna Credenziali` presente nella sezione `Tools` dell'installer.



- Per sbloccare questa funzione sarà prima necessario usare la funzione `Controlla files` ( vedi la sezione `TAB 4 - Tools` di [Guida all'installazione](./ca-tools-2-install-guide/) ).
- Serve a sovrascrivere `username` e `token` con quelli attualmente presenti nei file **.npmrc** **NuGet.Config** e **scarface.config.json** .



**`N.B.`** Una volta aggiornate le credenziali sarà necessario ri-autenticarsi ai progetti.
Per fare ciò, bisognerà seguire la* [Guida di autenticazione ai progetti](./ca-tools-2-projects-auth-guide)






