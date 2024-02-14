# Configurable Indentation

You can configure the indentation of generated files using YAML. There are options to set custom indentation for server-side and client-side code.

## Server-Side Code Indentation

To set a custom indentation for the generated server-side code, follow these steps:

1. Add the following line to the `codegen/configs/all.yml` file, specifying your desired indentation size (e.g., 4):

   ```yml
   server.indentSize: 4
   ```

2. Add the following line to the `codegen/configs/server.yml` file:

   ```yml
   indentSize: 4
   ```

3. After saving these files, run the command `Scarface: Format server` to format the existing server-side code. This command should be executed only when changing the indentSize.

## Client-Side Code Indentation

To set a custom indentation for the generated client-side code, follow these steps:

1. Add the following line to the `codegen/configs/all.yml` file, specifying your desired indentation size (e.g., 4):

   ```yml
   client.indentSize: 4
   ```

2. Add the following line to the `codegen/configs/client.yml` file:

   ```yml
   indentSize: 4
   ```

3. After saving these files, run the command `Scarface: Format client` to format the existing client-side code. This command should be executed only when changing the indentSize.

## Reformatting Both Client and Server Code

To reformat all files, both on the client and server side, you can simply run the `Scarface: Format all` command.

These configuration options allow you to control the indentation of your generated code according to your preferences and maintain a consistent coding style.
