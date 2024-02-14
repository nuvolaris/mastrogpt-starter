# Autenticazione e autorizzazioni

Authorizations

In questa sezione è spiegato come può essere gestita l'autenticazione e le autorizzazioni con il framework Code Architects

## Claim

Una serie di claims definise l'identità e i privilegi dell'utente fornendo una maggiore flessibilità al sistema di autenticazione (rispetto ai vecchi ruoli di appartenenza). Un claim nello specifico è una particolare informazione relativa all'utente in questione (es. nome, email, telefono, zipcode), emessa da un'autorità 'trusted' e identificata come un dizionario di valori chiave, in cui la chiave è rappresentata dal namespace ed il valore da un dato particolare relativo all'utente.

```json
[{
  "type": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/sid",
  "valueType": "http://www.w3.org/2001/XMLSchema#string",
  "value": "20570589-1fd0-4b9f-abbb-1b3221884757"
}, {
  "type": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname",
  "valueType": "http://www.w3.org/2001/XMLSchema#string",
  "value": "Mario Rossi"
}, {
  "type": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",
  "valueType": "http://www.w3.org/2001/XMLSchema#string",
  "value": "mrossi@codearchitects.com"
}, {
  "type": "http://schemas.microsoft.com/ws/2008/06/identity/claims/role",
  "valueType": "http://www.w3.org/2001/XMLSchema#string",
  "value": "admin"
}, {
  "type": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier",
  "valueType": "http://www.w3.org/2001/XMLSchema#string",
  "value": "mrossi"
}]
```

```ts
constructor(
  private _http: HttpClient,
  private _policyEngineService: PolicyEngineService,
  private _serializer: SerializerService) {
    ...
}

private setupClaims() {
    this._http.get<string>(`${Config.API}/${claimsPath}`,
      {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this._accessToken}`
        }),
        responseType: 'text' as 'json'
      })
      .pipe(map<string, IJsonClaim[]>(jsonClaims => this._serializer.deserialize(jsonClaims)))
      .subscribe(claims => {
        this._policyEngineService.setJsonClaims(claims);
    }, this.catchAuthError.bind(this));
}
```

[Live Demo](https://storybook.codearchitects.com/#/storybook/business/authorization/40a991a4-6654-67fd-c78e-69df13a7058a/playground/$Claim)
## Policy

Una policy definisce una regola collegata ad un nome di risorsa. La regola è disponibile solo in presenza di un determinato claim.

Esempio di una lista di policies applicative fornita al client. In questo esempio tutti gli utenti non aventi il ruolo admin (prima policy) ritroverrano disabilitati tutti i componenti con come risorsa : 'property://Invoice/code'; solo l'utente con username abianchi (seconda policy) potrà vedere il pulsante di conferma con la resource 'component://invoices/button/confirm'; solo l'utente con ruolo admin e con sid c423011b-003a-4df0-b578-94cce80e1c41 (terza policy) potrà accedere allo scenario invoices (se pilotata da una guard con controllo su nome di risorsa 'scenario://invoices').

Per rendere disponibili le policies sarà necessario passarle al Policy Engine. Per farlo andrà iniettato nel costruttore il servizio PolicyEngineService e successivamente le policies andranno deserializzate e passate al metodo setJsonPolicies.
```json
[
  {
    "type": "authorization",
    "resource": "property://Invoice/code",
    "selector": "enable",
    "claim": {
      "claimType": "http://schemas.microsoft.com/ws/2008/06/identity/claims/role",
      "claimValue": "admin"
    }
  },
  {
    "type": "authorization",
    "resource": "component://invoices/button/confirm",
    "selector": "show",
    "claim": {
      "claimType": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier",
      "claimValue": "abianchi"
    }
  },
  {
    "type": "authorization",
    "resource": "scenario://invoices",
    "selector": "show",
    "and": {
      "claim": [{
        "claimType": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/sid",
        "claimValue": "c423011b-003a-4df0-b578-94cce80e1c41"
      }, {
        "claimType": "http://schemas.microsoft.com/ws/2008/06/identity/claims/role",
        "claimValue": "admin"
      }]
    }
  }
]
```


```ts
constructor(
  private _http: HttpClient,
  private _policyEngineService: PolicyEngineService,
  private _serializer: SerializerService) {
    ...
}

private setupPolicies() {
    this._http.get<string>(`${Config.API}/${policiesPath}`,
      {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this._accessToken}`
        }),
        responseType: 'text' as 'json'
      })
      .pipe(map<string, IJsonPolicy[]>(jsonPolicies => this._serializer.deserialize(jsonPolicies)))
      .subscribe(policies => {
        this._policyEngineService.setJsonPolicies(policies);
    }, this.catchAuthError.bind(this));
}
```
[Live Demo](https://storybook.codearchitects.com/#/storybook/business/authorization/40a991a4-6654-67fd-c78e-69df13a7058a/playground/$Policy)
 
## Resource
Una resource (identificata da un resource name) è collegata ad una specifica policy la quale, in funzione dei claims dell'utente corrente, applica le sue regole dove lo stesso resource name è applicato

```HTML
<sh-textarea resource="property://Invoice/code" [model]="invoice" prop="code"></sh-textarea>
```

```ts
@Resource({ uri: 'property://Invoice/code' }) protected code: number;
```

```ts
this.policyEngineService.observePolicies('property://Invoice/code', 'enable', 'show')
.pipe(takeUntil(this.destroy$), distinct())
.subscribe(policies => {
    console.log(`Policy says that enable is ${policies.enable} and show is ${policies.show}`);
});
```

[Live Demo](https://storybook.codearchitects.com/#/storybook/business/authorization/40a991a4-6654-67fd-c78e-69df13a7058a/playground/$Resource)

## Esempi di utilizzo

Eseguire il login con differenti utenti per osservare i differenti comportamenti

```json
[
  {
    "type": "authorization",
    "resource": "property://Invoice/code",
    "selector": "enable",
    "claim": {
      "claimType": "http://schemas.microsoft.com/ws/2008/06/identity/claims/role",
      "claimValue": "admin"
    }
  },
  {
    "type": "authorization",
    "resource": "component://invoices/button/confirm",
    "selector": "show",
    "claim": {
      "claimType": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier",
      "claimValue": "abianchi"
    }
  },
  {
    "type": "authorization",
    "resource": "scenario://invoices",
    "selector": "show",
    "and": {
      "claim": [{
        "claimType": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/sid",
        "claimValue": "c423011b-003a-4df0-b578-94cce80e1c41"
      }, {
        "claimType": "http://schemas.microsoft.com/ws/2008/06/identity/claims/role",
        "claimValue": "admin"
      }]
    }
  }
]
```

```HTML
<div>
  Current logged user:
  <sh-caption [model]="profile" prop="username"></sh-caption>
</div>


<sh-text resource="property://Invoice/code" [model]="this" prop="code"
  [options]="{ placeholder: 'input-resource', width: 350 }">
</sh-text>


<sh-text [model]="this" prop="code1" [options]="{ placeholder: 'decorator-resource', width: 350 }">
</sh-text>


<sh-caption>just-abianchi-show</sh-caption>
<sh-button resource="component://invoices/button/confirm" [primary]="true">confirm</sh-button>


<sh-caption>just-admin-sid-navigate</sh-caption>
<sh-button [primary]="true" (clicked)="router.navigate(['/storybook','business', 'invoices'])">
  navigate-invoices-without-return
</sh-button>
```
```ts
@Resource({ uri: 'property://Invoice/code' })
protected code1 = UUID.UUID();
```
```ts
@Injectable()
export class InvoicesGuard implements CanActivate {
  constructor(
    private router: Router
    , private _policyEngineService: PolicyEngineService
    , private _toastService: ShToastService
  ) {
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    return this._policyEngineService.observePolicies<{ enable: boolean, show: boolean }>('scenario://invoices', 'enable', 'show')
      .pipe(map(resp => {
        if (resp.show) {
          return true;
        } else {
          this._toastService.pop({ title: 'no-permissions-navigate', type: 'error' });
          return false;
        }
      }));
  }
}
```
[Live Demo](https://storybook.codearchitects.com/#/storybook/business/authorization/40a991a4-6654-67fd-c78e-69df13a7058a/playground/$sample-resource-policy-claim)


## Esempio di login


L'esempio seguente mostra com'è stato implementato nell'applicazione Storybook il login (con relative autorizzazioni) utilizzando le features offerte dal framework. In questo esempio (per semplicità) le policies, i claims e l'access token vengono presi da files json all'interno degli assets.

__[STEP 0]__ Utilizziamo Scarface per generare un nuovo servizio chiamato 'auth' all'interno di un repository shared (in questo esempio il nostro repo shared è shell).

__[STEP 1]__ All'interno del nostro repository shared, nella folder 'models' creiamo un nuovo modello chiamato ShProfile (che rappresenterà il profilo del nostro utente applicativo).

__[STEP 2]__ Implementiamo ora la nostra logica di autenticazione ed autorizzazioni con policies e claims come da esempio.

__[STEP 3]__ Utilizziamo Scarface per generare una nuova applicazione chiamata 'auth' e successivamente al suo interno un nuovo dominio chiamato 'login'. In questo dominio andremo ad inserire il nostro componente di login che avrà il compito di interfacciarsi col servizio di AuthService e gestire quindi l'autenticazione.

__[STEP 4]__ Modifichiamo le routes dell'applicazione 'auth' (come da esempio), in modo tale da reindirizzare l'utente direttamente alla pagina di login quando si atterra nell'applicazione 'auth'.

__[STEP 5]__ Modifichiamo la guard dell'applicazione 'auth' in modo tale da reindirizzare l'utente all'applicazione 'storybook' in caso esso sia già loggato.

__[STEP 6]__ Modifichiamo la guard dell'applicazione 'storybook' in modo tale da reindirizzare l'utente all'applicazione 'auth' in caso esso non sia già loggato.

```bat
[STEP 0]

ca scarface service (auth)
```

```ts
// [STEP 1]
export class ShProfile {
    /**
     * Security Identifier namespace
     */
    private static __sidKey = 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/sid';
    /**
     * Email namespace
     */
    private static __emailKey = 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress';
    /**
     * Given Name namespace
     */
    private static __givennameKey = 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname';
    /**
     * Role namespace
     */
    private static __roleKey = 'http://schemas.microsoft.com/ws/2008/06/identity/claims/role';
    /**
     * Username namespace
     */
    private static __usernameKey = 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier';
    /**
     * Security identifier
     */
    private _sid: string;
    /**
     * Email
     */
    private _email: string;
    /**
     * Given name
     */
    private _givenname: string;
    /**
     * Role
     */
    private _role: string;
    /**
     * Username
     */
    private _username: string;
    /**
     * Security identifier
     */
    public get sid() { return this._sid; }
    /**
     * Email
     */
    public get email() { return this._email; }
    /**
     * Given name
     */
    public get givenname() { return this._givenname; }
    /**
     * Role
     */
    public get role() { return this._role; }
    /**
     * Username
     */
    public get username() { return this._username; }

    /**
     * User profile
     * @param claims List of user claims
     */
    public constructor(claims: IJsonClaim[]) {
        claims.forEach(claim => {
            switch (claim.type) {
                case ShProfile.__sidKey:
                    this._sid = claim.value;
                    break;
                case ShProfile.__emailKey:
                    this._email = claim.value;
                    break;
                case ShProfile.__givennameKey:
                    this._givenname = claim.value;
                    break;
                case ShProfile.__roleKey:
                    this._role = claim.value;
                    break;
                case ShProfile.__usernameKey:
                    this._username = claim.value;
                    break;
            }
        });
    }
}
```
```ts
// [STEP 2]

import { ShProfile } from './../models/shell_custom';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { PolicyEngineService } from '@ca-webstack/ng-policy-engine';
import { SerializerService } from '@ca-webstack/ng-serializer';
import { IShHttpRequestOptions } from '@ca-webstack/ng-shell';
import { IJsonClaim, IJsonPolicy } from '@ca-webstack/policy-engine';
import { Observable, Subject } from 'rxjs';
import { map, publishReplay, refCount, takeUntil, throttleTime } from 'rxjs/operators';
import { Config } from '../../env.config';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  /**
   * Authentication token key
   */
  private static readonly __TOKEN_KEY = 'auth_token';
  /**
   * User Claims Identifier key (just for sample purposes)
   */
  private static readonly __USERID_KEY = 'auth_user-claims-identifier';
  /**
   * Authorization path
   */
  private static readonly __authorizationPath = 'api/authorization';
  /**
   * Url di reidirezione
   */
  public redirectUrl: string;
  /**
   * Observable which emits an event when application requires an user logout
   */
  public logout$ = new Subject<boolean>();
  /**
   * Observable which emits an event when an user is logged out
   */
  private _loggedOut$ = new Subject();
  /**
   * Authentication access token
   */
  private _accessToken = '';
  /**
   * User claims identifier (just for sample purposes)
   */
  private _userIdentifier: string;
  /**
   * User profile
   */
  private _profile: Observable<ShProfile>;
  /**
   * Specifies whether user is logged in
   */
  public get isLoggedIn() { return !!this._accessToken && !!this._userIdentifier; }

  public constructor(
    private _http: HttpClient,
    private _policyEngineService: PolicyEngineService,
    private _serializer: SerializerService,
    private _router: Router) {
    this._accessToken = this._serializer.deserialize(localStorage.getItem(AuthService.__TOKEN_KEY));
    this._userIdentifier = this._serializer.deserialize(localStorage.getItem(AuthService.__USERID_KEY));
    if (this._accessToken && this._userIdentifier) {
      this.init();
    } else {
      this._router.navigate(['/auth']);
    }
  }

  /**
   * Retrieves info about logged user
   */
  public getProfile(refresh = false) {
    if (refresh || !this._profile) {
      this._profile = this._http.get<string>(`${Config.API}/${AuthService.__authorizationPath}/${this._userIdentifier}-claims.json`, this.getAuthOptions())
        .pipe(
          map(jsonClaims => new ShProfile(this._serializer.deserialize(jsonClaims))),
          publishReplay(1),
          refCount()
        );
    }
    return this._profile;
  }

  /**
   * Initializes policies and claims
   */
  public setupClaimsAndPolicies() {
    this.setupClaims();
    this.setupPolicies();
  }

  /**
   * Performs user login, holding access token
   * @param userIdentifier User claims identifier (just for sample purposes)
   */
  public login(userIdentifier = this._userIdentifier) {
    return new Promise((resolve, reject) => {
      const options: IShHttpRequestOptions = { headers: new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' }) };
      if (options) {
        options.observe = 'response' as 'body';
        options.responseType = 'text' as 'json';
        options.withCredentials = true;
      }
      this._http.get<string>(`${Config.API}/${AuthService.__authorizationPath}/token.json`, this.getAuthOptions())
        .pipe(map<string, { token: string }>(jsonToken => this._serializer.deserialize(jsonToken)))
        .subscribe(response => {
          const accessToken = response && response.token;
          if (accessToken) {
            localStorage.setItem(AuthService.__TOKEN_KEY, this._serializer.serialize(accessToken));
            localStorage.setItem(AuthService.__USERID_KEY, this._serializer.serialize(userIdentifier));
            this.init(accessToken, userIdentifier);
            resolve();
            this._router.navigate([this.redirectUrl || '/storybook']);
          } else {
            reject('No access token found');
          }
        }, (err: HttpErrorResponse) => {
          reject(err && err.message);
          this.catchAuthError(err);
        });
    });
  }

  /**
   * Performs user logout
   */
  private logout() {
    localStorage.removeItem(AuthService.__TOKEN_KEY);
    localStorage.removeItem(AuthService.__USERID_KEY);
    delete this._accessToken;
    delete this._userIdentifier;
    delete this._profile;
    this._policyEngineService.resetClaims();
    this._policyEngineService.resetPolicies();
    this._loggedOut$.next();
    this._router.navigate(['']);
  }

  /**
   * Initializes claims and policies
   */
  private init(token = this._accessToken, userIdentifier = this._userIdentifier) {
    this._accessToken = token;
    this._userIdentifier = userIdentifier;
    this.logout$
      .pipe(takeUntil(this._loggedOut$), throttleTime(1000))
      .subscribe(this.logout.bind(this));
    this.setupClaimsAndPolicies();
  }

  /**
   * Provides claims to policy engine.
   * A series of claims define the identity and priviliges of the user by
   * providing greater flexiblity to the authentication system comparet to
   * the old membership roles.
   * A claim is a particular information related to the user in question
   * (example: name, email, telephone, zipcode), issued by a "trusted" authority
   * and identified as a key value dictionary, where the key is represented by the namespace
   * of the claim and the value from a particular data relating to the user.
   */
  private setupClaims() {
    this._http.get<string>(`${Config.API}/${AuthService.__authorizationPath}/${this._userIdentifier}-claims.json`, this.getAuthOptions())
      .pipe(map<string, IJsonClaim[]>(jsonClaims => this._serializer.deserialize(jsonClaims)))
      .subscribe(claims => {
        this._policyEngineService.setJsonClaims(claims);
      }, this.catchAuthError.bind(this));
  }

  /**
   * Provides policies to policy engine.
   * A policy defines a rule linked to a resource name.
   * The rule is available just in presence of a specified claim.
   */
  private setupPolicies() {
    this._http.get<string>(`${Config.API}/${AuthService.__authorizationPath}/policies.json`, this.getAuthOptions())
      .pipe(map<string, IJsonPolicy[]>(jsonPolicies => this._serializer.deserialize(jsonPolicies)))
      .subscribe(policies => {
        this._policyEngineService.setJsonPolicies(policies);
      }, this.catchAuthError.bind(this));
  }

  /**
   * Provides http headers mixed with access token
   */
  private getAuthOptions() {
    return { headers: new HttpHeaders({ 'Content-Type': 'application/json', 'Authorization': `Bearer ${this._accessToken}` }), responseType: 'text' as 'json' };
  }

  /**
   * Catches http errors
   * @param error Http error response
   */
  private catchAuthError(error: HttpErrorResponse) {
    console.error(error.message);
    this.logout$.next();
  }
}
```

```cmd
[STEP 3]

ca scarface application (auth)
ca scarface domain (auth->login)
```

```ts
// [STEP 4]

export const AUTH_ROUTES: Routes = [
  {
    path: '', component: AuthIndexComponent, canActivate: [AuthGuard],
    children: [
      { path: '', redirectTo: 'login' },
      // --inject:routesList--
      { path: '', component: AuthLandingComponent },
      { path: 'login', loadChildren: () => import('./login/login.module').then(m => m.LoginModule) }
      // --inject:routesList--
    ]
  },
];
```

```ts
// [STEP 5]

@Injectable({
    providedIn: 'root'
})
export class AuthGuard implements CanActivate {
    constructor(private _router: Router, private _authService: AuthService
    ) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        const canActivate = !this._authService.isLoggedIn;
        if (!canActivate) {
            this._router.navigate(['/storybook']);
        }
        return canActivate;
    }
}
```

```ts
// [STEP 6]

@Injectable({
    providedIn: 'root'
})
export class StorybookGuard implements CanActivate {
    constructor(private _router: Router, private _authService: AuthService
    ) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        const canActivate = this._authService.isLoggedIn;
        if (!canActivate) {
            this._authService.redirectUrl = state.url;
            this._router.navigate(['/auth']);
        }
        return canActivate;
    }
}
```
[Live Demo](https://storybook.codearchitects.com/#/storybook/business/authorization/40a991a4-6654-67fd-c78e-69df13a7058a/playground/$login-sample)
