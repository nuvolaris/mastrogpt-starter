 # React overview
Il framework offre la possibilità di sviluppare componenti React ed utilizzarle con Angular.

## Configurare React nel progetto

E' possibile eseguire il setup dell'applicazione per supportare React in fase di scaffolding del progetto. Scarface chiederà all'utente se si vuole che l'app supporti React, in caso si risponda positivamente, non ci sarà bisogno di eseguire gli steps di configurazione sottostanti

Installare il pacchetto nella cartella client
```cmd
npm i @ca-webstack/ng-react (folder client)
```
Importare/Esportare il modulo di React nel modulo ComponentsModule

```ts
...
import { ShReactComponentsModule } from '@ca-webstack/ng-react';
...
@NgModule({
  ...
  imports: [
    ...
    ShReactComponentsModule,
    ...
  ],
  exports: [
    ...
    ShReactComponentsModule,
    ...
  ],
  ...
})
export class ComponentsModule { }
```

Modificare i json tsconfig.app.json e tsconfig.spec.json inserendo in compilerOptions la proprietà 'jsx' con valore 'react', come segue:

```json
{
  ...
  "compilerOptions": {
    ...
    "jsx": "react",
    ...
  },
  ...
}
```
Dopo aver configurato React nel progetto (manualmente o mediante Scarface) sarà possibile utilizzare la componente sh-react-component (vedi API Reference per maggiori dettagli) passando in input il riferimento alla classe del componente, le props specifiche del componente e sottoscriversi ad un eventuale cambio di stato mediante l'output 'change', come di seguito:
```HTML
<sh-react-component [component]="componentRef" [props]="props" (change)="onStateChange($event)">
</sh-react-component>
``` 

## Estendere React Base Component

E' possibile creare una nuova componente react manualmente o mediante Scarface. In ogni caso, andrà estesa la componente base ShBaseReactComponent.  
  
  

Se si esegue la procedura manuale, sarà necessario importare la componente di base ShBaseReactComponent dal pacchetto ng-react.

```ts
import { ShBaseReactComponent } from '@ca\-webstack/ng-react';
```
Di seguito il contratto da rispettare estendendo ShBaseReactComponent:

```ts
export declare abstract class ShBaseReactComponent<TProps = {}, TState = {}> extends React.Component<TProps, TState> {
    /**
     * Observable of state changes
     */
    change$: Subject<TState>;
    /**
     * Reference to react component element.
     * If you want to refere to this element, you must link
     * this property to rendering element with ref prop in
     * render method (<div ref={this.element}></div>)
     */
    protected element: React.RefObject<HTMLDivElement>;
    /**
     * Subject which notifies subscribers when component destroy itself
     */
    protected destroy$: Subject<{}>;
    /**
     * Base React Component
     * @param props React component properties
     */
    constructor(props: TProps);
    /**
     * Method to call to update state
     * @param state New state
     */
    setState(state: TState | any): void;
}
```

## Esempio di utilizzo di una componente React

Nell'esempio seguente è stata generata una componente react avente come properties una label ed un oggetto di tipo Person. L'esempio evidenzia com'è semplice far comunicare una componente Angular con una componente React.

Genera una nuova componente utilizzando Scarface (o direttamente dal task explorer di VSCode) e scegli 'React' come tipologia di componente. Verrà dunque generata una nuova componente (.tsx).

```tsx
ca scarface component (React)
```

La componente presa come esempio ha come props una label ed un oggetto di tipo Person. A video verrà mostrata dunque una label ed il nome e cognome della persona (passata come prop). Inoltre sarà possibile attivare/disattivare la persona mediante un pulsante. Questo modificherà semplicemente lo stile (da bold a standard e viceversa).
```ts
import * as React from 'react';
import { ShBaseReactComponent } from '@ca-webstack/ng-react';
import { Person } from '../../models/storybook_custom';

/**
 * React component properties contract
 */
export interface ISampleProps {
  label?: string;
  person?: Person;
}
/**
 * React component state contract
 */
export interface ISampleState {
  isActive: boolean;
}

/**
 * Sample React Component
 */
export default class SampleComponent extends ShBaseReactComponent<ISampleProps, ISampleState> {

  constructor(props) {
    super(props);
    this.state = { isActive: false };
  }

  public componentDidMount() {
    console.log('Component Mounted');
  }

  public componentWillReceiveProps(nextProps: ISampleProps) {
    console.log(`Component will receive props: ${nextProps}`);
  }

  private changeState = () => {
    this.setState({ isActive: !this.state.isActive });
  }

  render() {
    return <div>
      <label>{this.props.label}</label>
      {
        this.props.person ?
          <div>
            {this.state.isActive
              ? <b>{this.props.person.name} {this.props.person.surname}</b>
              : <i>{this.props.person.name} {this.props.person.surname}</i>
            }
            <button onClick={this.changeState}>{this.state.isActive ? 'Deactivate' : 'Activate'}</button>
          </div>
          : <div><i>No person selected</i></div>
      }
    </div>;
  }
}
```
Per utilizzare la nostra componente, sarà necessario importarla nel nostro file .ts ed assegnarla ad una variabile che passeremo al componente ShReact che dinamicamente riuscirà a mostrarla. Nell'esempio, riceveremo una notifica al cambio dello stato, reagendo con un toast, e mediante una select-input Angular potremo selezionare una persona da una lista ed all'evento di selezione modificare le props.
```HTML
<div input-group-h>
    <sh-react-component [component]="componentRef" [props]="props" (change)="onStateChange($event)">
    </sh-react-component>
    <sh-select [model]="this" prop="person" (valueChanges)="changeProps()"
      [options]="{values: people, valuesPipe: personPipe, placeholder: 'Angular component'}"></sh-select>
</div>
```
```ts
...
import SampleComponent, { ISampleProps, ISampleState } from '..../components/sample/sample.component';
...
componentRef = SampleComponent;
props: ISampleProps = {
  label: 'React Component'
};
person: Person;
people: Person[] = [
  { name: 'Mario', surname: 'Bianchi' },
  { name: 'Luca', surname: 'Rossi' },
  { name: 'Francesco', surname: 'Verdi' }
];
personPipe = new PersonPipe();
...
onStateChange(state: ISampleState) {
  this._toastService.pop({ title: `React Component state changed. Now person is ${state.isActive ? '' : 'not'} active`, type: state.isActive ? 'success' : 'error' });
}

changeProps() {
  this.props = { ...this.props, person: this.person };
}
...
```

## REACT API REFERENCE
### Inputs
| Nome        | Tipo        | Descrizione | Valore di default |
| ----------- | ----------- | ----------  | -----------  |
|***component***|React.ComponentClass<TProps,TState>|React component class reference|undefined|
|***props***|TProps|React component properties|undefined|
|***debounceTime***|number s|Emits a change event only after a particular time span has passed without another source emission|0|
|***throttleTime***|number|Emits a change event, then ignores subsequent source values for duration milliseconds, then repeats this process.|0|

### Outputs
| Nome        | Tipo        | Descrizione | Valore di default |
| ----------- | ----------- | ----------  | -----------  |
|***change***|EventEmitter<TState>|Event fired when react component state changes.|EventEmitter|
