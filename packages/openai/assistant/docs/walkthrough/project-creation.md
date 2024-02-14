# Project creation

In this walkthrough, we will create a complete eCommerce application using the CAEP framework. We'll start by generating the initial project structure using the "ca scarface" command. For more in-depth explainations of the scaffolding, see the [Scarface docs](../sdk/scarface.md).

## Running the scarface command

To begin, open your command-line interface and navigate to the directory where you want to create your eCommerce project. Then, run the following command:

```bash
ca scarface
```

The "ca scarface" command will prompt you to provide a project name. Make sure to choose a name in kebab-case or lowercase. For our example, we'll use "shopping-cart."

? Please provide a project name (in kebab-case or lowercase, e.g.: back-office, backoffice) `shopping-cart`

? Please provide shopping-cart prefix (in lowercase or PascalCase, e.g.: app, APP) `app`

? Please provide domain name (in kebab-case or lowercase, e.g.: customers-relations, crm) `store`

? Please provide scenario name (in kebab-case or lowercase, e.g.: dev-settings, customers) `products`

? Please provide author name (in PascalCase, e.g.: CodeArchitects): `CodeArchitects`

After completing the guided procedure, Scarface will scaffold the application structure for your eCommerce project. This includes creating the necessary folders and files for both the front-end (Angular) and back-end (.NET) components.

You'll now have a basic project structure in place, ready for further customization and development. We will start by opening the project folder in Visual Studio Code.

## Adding a microservice

To generate and add a new microservice, you can utilize a specific task in Visual Studio Code. In the sidebar, navigate to the "Tasks" section, then locate and click on "Scarface: Generate microservice."

Upon clicking the "Scarface: Generate microservice" task, you will be prompted to enter some info about the microservice. Firstly, will need to specify the name of the project and its namespace (we will use the default one). Then, the tool will ask for specifications about the technologies and the structure of the service: in this example, we will use .NET 7 and Entity Framework Core; the microservice will be composed by a single C# project and will be accessible through a gateway (there is already one, spa-gateway, which is the gateway for the Single Page Application).

? Please insert the microservice name `Store`

? Please insert the microservice namespace `App.ShoppingCart.Store`

? Which framework do you want to adopt for the microservice? `.NET7`

? Which ORM do you want to use for the microservice? `EntityFrameworkCore`

? Would you like to split the Store service into four projects (App.ShoppingCart.Store, App.ShoppingCart.Store.Domain, App.ShoppingCart.
Store.Dto, App.ShoppingCart.Store.Infrastructure)? `No`

? Would you like to add Store service to a gateway? `Yes`

? Please choose the gateways to which to add the service `spa-gateway.yml`

We can now start customizing and developing this microservice to handle specific functionalities of our eCommerce application.

Next step: [Entities and database](dal/entities-and-database.md)
