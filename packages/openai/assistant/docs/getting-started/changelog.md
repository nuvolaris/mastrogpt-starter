# Changelog

## All CAEP changes are documented here

This changelog follows the format outlined in the article [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Additionally, we adhere to the [Semantic Versioning](https://semver.org/spec/v2.0.0.html) standard.

### Types of Changes:

- **Added** for new features.
- **Changed** for changes to existing features.
- **Deprecated** for soon-to-be removed features.
- **Removed** for removed features.
- **Fixed** for bug fixes.
- **Security** in case of vulnerabilities.
- **Breaking** for breaking changes.

**NOTE FOR EXISTING PROJECTS**

For existing projects (or simple test projects), after installing the above-mentioned version, run the "Scarface: Migrate project" command from the VSCode Task Explorer. This command should be executed only once on the project.

If a developer runs the migrate project on their machine and then commits and pushes the changes, other developers who pull the changes should install the correct versions of Node, Npm, and Angular, and then run the Scarface version installation command without having to run the migrate project again. Finally, perform a package restore on their project.

## Release 2.1.3 - April 21, 2023

### Installation

```shell
npm i -g @ca/generator-scarface@2.1.3
ca plugins:install @ca/cli-plugin-scarface@0.2.25
```

### Security

- These updates address some vulnerabilities introduced by dependencies, namely @microsoft/signalr, @angular/devkit, and protractor:
  - Updated to version 14.1.3 of @ca-webstack/ng-shell.
  - Updated to version 14.1.1 of @ca-webstack/ng-signalr.
  - Updated to version 14.2.11 of @angular-devkit/build-angular.
  - Removed the protractor package.

## Release 2.1.2 - April 20, 2023

### Installation

```shell
npm i -g @ca/generator-scarface@2.1.2
ca plugins:install @ca/cli-plugin-scarface@0.2.25
```

### Added

- Added support for .NET 7 templates.
- Added support for the Dapr building block "Secret." The supported provider in this version of CAEP is Azure Key Vault.
- Added basic support for GraphQL.
- Added support for client-side DTO initializers. It is now possible to instantiate a DTO with initialization properties.
- Added the ability to configure change tracking on DTOs for each microservice.
- Added support for the DateOnly data type on DTOs. This data type allows passing DTOs with DateOnly-type fields between the client and server, representing dates without time. Automatic mapping between DateOnly-type fields (on DTOs) and DateTime-type fields (on Entities) has also been handled.
- Added the ability to specify an ancestor on domain entities.
- Added support for the Actor Model.
- Operation Bindings: Added a new property (binding) to operation parameters. It is now possible to specify directly from the YAML whether parameters are query parameters (fromQuery), from the request body (fromBody), or included in the request header (fromHeader).
- Identity Profile: Added the ability to configure the identity profile within each microservice.
- Multitenancy: Added the ability to configure multitenancy within each microservice.
- Configurable Indentation: Added the ability to configure the indentation of generated files.
- Payload Modeling: Added the ability to model the payload within YAML files.

### Removed

- Removed direct dependencies on CodeArchitects.Platform.CodeAnalysis and CodeArchitects.Platform.Analyzer (packages included in CodeArchitects.Platform.Common).

### Changed

- Updated to version 10.0.4 of @ca-codegen/ms-gen.
- Updated to version 4.0.3 of @ca-codegen/core.
- Updated to version 1.0.4 of @ca/cli-plugin-codegen.
- Updated packages @ca-webstack and @caep to version 14.1.x.
- Updated packages CodeArchitects.Platform to version 2.1.2.
- For .NET 6 target microservices, added "using System;" at the top of each file outside the import injection zone for INJECT files and inside the custom import zone for CUSTOM files. This addition will allow for automatic import suggestions immediately below "using System."

### Fixed

- Accelerated scaffold generation.

### Breaking

During migration, Scarface will attempt to resolve the main breaking changes automatically. Below are the breaking changes related to the addition of new injection zones and the insertion of small snippets of code. Scarface will try to automatically resolve the following breaking changes:

1. App.cs

   - Added an injection zone SECRETS and IDENTITY_PROFILE before the AddSwaggerGen method.
   - Added the following line of code in the AddAutoMapper method as the second parameter: `typeof (AutoMapperTracking).Assembly`.
   - Wrapped the AddDaprInfrastructure method within the DAPR injection zone.

2. Program.cs

   - Added an injection zone ACTORS after the MapControllers method.
   - Added an injection zone AUTHENTICATION before the line of code `app.UseAuthorization()`.
   - Only for .NET5 microservices: Added an injection zone SECRETS after the UseStartup method.

3. Startup.cs (for .NET5 microservices)

   - Added the `services.AddIdentityProfile()` method before the `services.AddAutoMapper(...)` line.
   - Added the following line of code in the AddAutoMapper method as the second parameter: `typeof(AutoMapperTracking).Assembly`.
   - Added an injection zone AUTHENTICATION before the line of code `app.UseAuthorization()`.
   - Added an injection zone ACTORS after the MapControllers method.

4. docker-compose.yml and docker-compose.override.yml

   - Added an injection zone PLACEMENT before the BFF injection zone.

5. Csproj

   - Updated all CodeArchitects.Platform packages to version 2.1.2.

6. base-delegate-service.ts

   - Updated the request method to support parameters fromQuery and fromHeader.

If any of the above breaking changes are not resolved automatically by Scarface, it is recommended to delete and regenerate the relevant files (taking care to include custom changes using Git Diff).

The following two breaking changes cannot be resolved automatically by Scarface:

1.  During migration, the npm packages of CAEP will be updated to the latest patch of version 14.1.x. Any custom packages developed with CAEP npm packages in their dependencies should simply update the version indicated in the peers from 14.0.x to 14.1.x.

    For example:
    Before:

    ```json
    "@ca-webstack/ng-components": "~14.0.5"
    ```

    After:

    ```json
    "@ca-webstack/ng-components": "~14.1.0"
    ```

    It is important to resolve this breaking change because with the new npm versions, legacy peer dependencies are not supported. If it is not immediately possible to resolve this breaking change, simply run the npm i command in the client folder, adding the --legacy-peer-deps flag: cd client && npm i --legacy-peer-deps.

2.  If EJS template overrides have been made, it is advisable to compare them with the new generated templates to avoid generation issues or missing information.

    For example, if you have overridden the server/microservice-root/infrastructure/data/model/entity.ejs template, follow these steps to check for differences:

      - Run the Scarface: Override codegen template task.
      - Choose the correct path (for example, server/microservice-root/infrastructure/data/model/entity.ejs).
      - Compare the changes using Git Diff and adjust the template if necessary.

## Release 2.0.3 - January 30, 2023

### Installation

```shell
npm i -g @ca/generator-scarface@2.0.3
```

### Prerequisites

- Install NodeJS version 16.13.1.
  - This version is required for the proper functioning of Angular 14.
  - Install npm version 8.1.2.
  - You can use nvm to switch between Node versions by running the following commands in the console:
    ```shell
    nvm install 16.13.1
    nvm use 16.13.1
    ```
  - Verify the correct versions of Node and npm by running the following commands in the console:
    ```shell
    node -v
    npm -v
    ```
- Install Angular CLI version 14.
  - Scarface will attempt to install the new version of @angular/cli during the initial scaffold or migration. If it fails, it will display an error message, and the procedure will not be successful for the scaffold or will execute the migration erroneously. In case of an error, follow these steps:
    - If it exists, remove the "angular" folder from the path "C:\Users\yourname\AppData\Roaming\npm\node_modules."
    - Copy the "angular" folder from the path "C:\Users\yourname\AppData\Local\npm\node_modules" to the path "C:\Users\yourname\AppData\Roaming\npm\node_modules."
    - Rerun the scaffold or migrate on the project.
    - If the new version of @angular is not yet installed globally, try installing it manually by running the following command:
      ```shell
      npm i @angular/cli@^14 -g
      ```
    - Rerun the scaffold or migrate on the project.
    - If none of the above steps resolves the issue, contact Code Architects support.
  - Verify the correct Angular version by running the following command in the console (in any folder other than the project's): ng version.
- For existing projects, any npm packages (using a different version of Angular than version 14) not included in the initial scaffold will need to be manually updated, ensuring they align with Angular version 14.
  - In this case, the final step of migration (re-installation of packages) will not be successful. It will be necessary to correctly update the versions of third-party packages, rerun the setup, and regenerate the code.
- For some existing projects, the package.json file in the "client" folder may become corrupted after the migration process, causing the last installation step to fail. Fix the issue, rerun the setup, and regenerate the code. - One of the reasons the package.json file might become corrupted is the addition of a comma after the last dependency package. To fix it, simply remove the comma.

For other types of issues, contact Code Architects technical support.

### Added

- Added support for a new DAL (documentation: DAL with Entity Framework Core 7).
- DAL with Entity Framework Core 7:
- Added support for Multitenancy.
- Added support for Soft Delete.
- DAL with Dapper.
- Added support for Upsert (documentation: Upsert Support).
- Added support for Relational Model (documentation: Relational Model Support).
- Added support for Table Entity (documentation: Table Entity Support).
- Added support for Custom Layers Segregation
- Added support for Business Services

### Changed

- Updated to Angular version 13.
- Updated to Angular version 14.
- Updated to version 9.0.3 of @ca-codegen/ms-gen.
- Updated to version 3.0.5 of @ca-codegen/core.
- Updated packages @ca-webstack and @caep to version 14.
- Updated TypeScript to version 4.7.4.
- Revisited and updated the Messaging system.
- Added support for .NET 6.
- During the creation of a new microservice, you will be asked whether to target .NET 6 (requires Visual Studio 2022) or the default .NET 5.
  It will be possible to change the target of an existing microservice from .NET 5 to .NET 6 by following these simple steps:
  - Insert the following code snippet into the microservice's YAML:
    ```yaml
    target:
    framework: net
    version: 6
    ```
    - Delete the Startup.cs and Program.cs files.
    - Delete the microservice's csproj file.
    - Run code generation.
    - Restore any custom implementations from the Program.cs file.
    - Restore any custom implementations from the Startup.cs and EspServiceCollection.cs files into the new generated App.cs file.
    - Restore any custom package references in the csproj file.

### Removed

- Removed the generation of the UnitOfWork implementation (service that exposed all repositories).

### Security

- Removed warnings, deprecations, and vulnerabilities related to npm packages specified by the scaffold.
- Added the ability to enable strict mode on the client side.

### Breaking

During migration, Scarface will create a branch from develop since it will perform two initial commits after the migrations to Angular 13 and 14. Ensure there are no local changes before running the migration.

Here are the main breaking changes:

- Client

  - Replaced the TranslateModule with the ShTranslateModule.
    - Scarface will attempt to resolve this breaking change automatically by modifying the import and forRoot in app.module.ts.
  - Replaced the ToasterModule (angular2-toaster no longer supported by Angular 14) with ToastrModule (from the ngx-toastr library).
    - Scarface will attempt to resolve this breaking change automatically by modifying the import and forRoot in app.module.ts.
  - Replaced the dependency on lodash with lodash-es (same software contracts as lodash).
    - Scarface will attempt to resolve this breaking change automatically by modifying the imports in all files.
  - Updated the components.module.ts of the application:
    - For replacement of TranslateModule with ShTranslateModule.
    - For imports in the ShTranslateModule and ContextMenuModule (from the @perfectmemory/ngx-contextmenu library).
    - For exports in the ShTranslateModule and ContextMenuModule.
    - Scarface will attempt to resolve this breaking change automatically by modifying the application's components.module.ts file.
  - Updated the components.module.ts files of the domains to remove TranslateModule.
    - Scarface will attempt to resolve this breaking change automatically.
  - Updated the karma.conf.js file.
    - If you used the jasmine random option for tests, only this option needs to be restored (see diffs at the end of migration).
  - Removed "~" from the @ca-webstack styles imports in the styles.scss file.
    - Scarface will attempt to resolve this breaking change automatically by modifying the imports in the styles.scss file.
  - Updated the tsconfig.json file to replace "module es2017" with "module es2020" (options "module" and "lib").
    - Scarface will attempt to resolve this breaking change automatically.
  - Removed the tslint.json file in favor of .eslintrc.json.
    - Scarface will attempt to resolve this breaking change automatically.
  - Updated the polyfills.ts file to include the following snippet: import 'core-js/proposals/reflect-metadata'.
    - Scarface will attempt to resolve this breaking change automatically.
  - Replaced all occurrences of ToasterService service injection with ShToastService.
    Before:
    ```typescript
    import { ToasterService } from "angular2-toaster";
    ...
    constructor(..., private \_toastService: ToasterService) { }
    ```
    After:
    ```typescript
    ...
    import { ShToastService } from '@ca-webstack/ng-components';
    ...
    constructor(..., private \_toastService: ShToastService) { }
    ```
    The "pop" method of the new service accepts an object as a parameter. Adjust the calls accordingly.

- Server

    - Removed all generated UnitOfWork files.
          - The UnitOfWork can be used by adding the following using statement to your file:
            ```cs
              using CodeArchitects.Platform.Data;
            ```

    - The new UnitOfWork no longer contains references to repositories, so you will need to inject the desired repositories into your file. For example:
            
        Previous Version:
        ```cs
        await _uow.CustomerEntities.GetAllAsync(requestAborted)
        ```

        New Version:
        ```cs
        ...
        private readonly ICustomerEntityRepository _repo;
        ...
        public BusinessController(..., ICustomerEntityRepository repo)
        ...
        _repo = repo;
        ...
        await _repo.GetAllAsync(requestAborted);
        ```

    - The main csproj files will be completely regenerated.
          - It is recommended to compare (using VSCode's Diff system) the previous version of the csproj filewith the new version. This way, you can restore any custom packages that the migration has removed.
    - In the presence of highly customized files, some new injection zones may end up at the bottom of thefile. In such cases, it is advisable to delete the file and regenerate it. This procedure will standardizethe generated file again. Then, use the VSCode Diff system to check the overwritten changes and manuallyrestore them.
    - The IntegrationTestFixture.cs file will be overwritten.
