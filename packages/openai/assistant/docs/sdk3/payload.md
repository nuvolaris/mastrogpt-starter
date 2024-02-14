# Payload Modeling

One of the advantages of this approach is the ability to easily share a payload with specific information across different scenarios without redefining the software contract. Consider the scenario where a "customers" scenario needs to continue its flow in the "suppliers" scenario by including a search string and the selected customer in the payload. In this situation, it would be necessary to define the "customer" property in both the payload contract of the "customers" scenario and the "suppliers" scenario. With this new feature, you can manage this type of scenario by modeling shared information in a payload YAML, as shown in the following example:

```yml
name: CustomerPayload
type: payload
description: Customer payload
fields:
  - name: customer
    type: Customer
    description: Customer DTO
    container:
      type: application
      service: Business
  - name: searchText
    type: string
    description: Search Text
```

In this example, the modeled payload includes a "searchText" property of type string and a "customer" property of type Customer. The "container" entry indicates where to retrieve the type of information (in this case, the Customer DTO). In the example, it is indicated that the type "Customer" should be retrieved from the models of the Business microservice, which is included in the "application" container.

By including the modeled payload within the new "payloads" section in "task" containers for the "customers" scenario, like this:

```yaml
name: Customers
type: task
description: Customers scenario
domain: Crm
namespace: Ca.BackOffice.Crm.Customers
activity: CustomersActivity
payloads:
  - name: CustomerPayload
The generated code will look like this:
```

```typescript
import * as ApplicationModels from '../../../models/index';
…
export interface CustomersPayload extends IActivityPayload {
  /**
  * optional version of payload data
  */
  version?: number;
  /**
   * Customer DTO
   */
  customer: ApplicationModels.BusinessModels.Customer;
  /**
   * Search Text
   */
  searchText: string;
  // --inject:classDeclaration--
}
```

As observed from the YAML for the "Customers" scenario, you can include not only one payload but a series of payloads, indicating that the payload of a specific scenario can contain different shared information. In all cases, the option to manually model the payload is preserved (as currently done).
