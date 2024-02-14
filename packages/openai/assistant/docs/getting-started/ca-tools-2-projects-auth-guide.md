# Projects authentication

- Una volta generato il token e installato il CAEP seguendo la [Guida all'installazione](./ca-tools-2-install-guide/) ;
- Oppure ri-generato il token perché scaduto e aggiornate le credenziali tramite la sezione `Tools` dell'installer seguendo la [Guida alla generazione del token e aggiornamento delle credenziali](./ca-tools-2-token-and-crededentials-update-guide/) .

sarà possibile autenticarsi o ri-autenticarsi ai progetti con le nuove credenziali mediante la funzione:

## Autenticazione progetto
- Per sbloccarla sarà prima necessario usare la funzione `Controlla files` ( vedi la sezione `TAB 4 - Tools` di [Guida all'installazione](./ca-tools-2-install-guide/) ).
- Selezionando una cartella di progetto, questa funzione controllerà che all'interno vi siano file .npmrc o NuGet.Config e popolerà i rispettivi file a livello di utente con i registry presenti a livello di progetto.
- Nel caso siano progetti solo client o solo server, non è da considerare un errore il fatto che NON abbia trovato uno dei due file.

**`N.B.`** Il controllo **NON** funziona in modo ricorsivo, va quindi selezionata la cartella in cui sono effettivamente presente i file.


