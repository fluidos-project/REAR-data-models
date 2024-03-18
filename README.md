# Content of this repository

The repository is organized as follows:

```
.
├── models
    ├── examples
    |   ├── json              # contains JSON examples generated from JSON schemas
    |   ├── puml              # contains the puml files displayed in the README (do not edit)
    |   └── generate_puml.sh  # utility tool to generate the puml files from examples
    └── schemas               # contains all the JSON schemas
        ├── puml              # contains the puml files displayed in the README (do not edit)
        └── generate_puml.sh  # utility tool to generate the puml files from schemas
```

# How to use

A GitHub action automatically generates the images contained in the README starting from the JSON files contained both in the examples and schemas subfolders.

Still, the generation of examples of JSONs (starting from the schema) is not automated yet. Therefore, we suggest to use tools like ChatGPT or Gemini, providing the JSON schema to the prompt and asking for an example of compliant JSON. 

# Resources

The resource data model can be summarized in the following:
 - [Flavor](#flavor)
 - FlavorType
   - [K8Slice](#K8Slice)
   - [VM](#VM)
   - [Service](#Service)
     - [DB](#ServiceType-DB)
   - [Sensor](#Sensor)

In the following we represent some examples of JSON, you can find the original JSON schemas [here](https://raw.githubusercontent.com/fluidos-project/REAR-data-models/master/models/schemas).

## Flavor

The Flavor data model wraps the FlavorType and contains informations shared among all the different FlavorTypes.

![flavor](https://plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fluidos-project/REAR-data-models/master/models/examples/puml/flavor.txt&fmt=svg)

The Flavor has the following characteristics:
 - FlavorID, the unique identifier for the flavor [string].
 - ProviderID, the unique identifier for the provider [string].
 - Location, defines the flavor's location with:
   - latitude 
   - longitude
   - altitude (unit meters) [integer]
   - optional additional notes [string].
 - NetworkPropertyType, the type of network property ensured by the provider (e.g., "5G", "Wifi", "Ethernet") [list of string]
 - FlavorType, a reference to a specific flavor type schema using JSON references ($ref) to external files like "k8slice.json", "vm.json", etc. This allows defining details specific to each flavor type.
 - Price, defines the flavor's price with: 
   - amount [integer]
   - currency [string]
   - period [string].
 - Owner: Information about the node that owns the flavor, including:
   - domain [string]
   - node ID [string]
   - IP [string]
   - optional additional information with a property for "LiqoID" [string]
 - OptionalFields: Contains optional properties like "Availability" [bool] and "WorkerID" [string] for the worker providing the flavor.

## FlavorType

The FlavorType describes the actual flavor that is adverised.

> **The filtering mechanism implemented in REAR relies on the Flavortype. Therefore, any field for which we want to implement some filtering criteria should be included in the corresponding FlavorType (e.g., if I want to filter a FlavorType depending on the latency, I need to include that field in the related FlavorType).**

### K8Slice

![K8slice](https://plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fluidos-project/REAR-data-models/master/models/examples/puml/flavor-types/k8slice.txt&fmt=svg)

The K8Slice Flavor type has the following characteristics:
 - Characteristics: 
   - CPU, the number of CPU cores (unit core)[integer]
   - Pod, the number of pods that can be deployed in the remote K8Slice (unit number of pods)[integer]
   - Memory, the amount of RAM available (unit MB)[integer]
   - GPU, the number of GPU processing units (unit GPU processing cores)[integer]
   - Storage, the disk spacce reserved for the K8Slice (unit GB)[integer]
   - SecurityStandards, one or more security standards that the FlavorType is compliant with (TODO: [], define the list of acceptable values)
 - Policy:
   - Aggregatable, describing if multiple instances can be aggregated in one single virtual node
     - MinCount (unit count)[integer]
     - MaxCount (unit count)[integer]
   - Partitionable, describing if the specified K8Slice can be  partitioned, obtaining only a subset of the offered resources
     - CPUMin, the minimum number of CPUs that can be reserved from the K8Slice (unit core)[integer]
     - MemoryMin, the minimum amount of RAM that can be reserved from the K8Slice (unit Mbytes)[integer]
     - CPUStep, the step increase in CPU cores to be reserved (unit count)[integer]
     - MemoryStep, the step increase in RAM to be reserved (unit MB)[integer]


### VM

![vm](https://plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fluidos-project/REAR-data-models/master/models/examples/puml/flavor-types/vm.txt&fmt=svg)

The VM Flavor type has the following characteristics:
 - Characteristics:
   - Architecture, the architecture of the platform (TODO: [], define the list of acceptable values)
   - CPU, the number of CPU cores (unit core)[integer]
   - Pod, the number of pods that can be deployed in the remote K8Slice (unit number of pods)[integer]
   - Memory, the amount of RAM available (unit MB)[integer]
   - GPU, the number of GPU processing units (unit GPU processing cores)[integer]
   - Storage, the disk spacce reserved for the K8Slice (unit GB)[integer]
   - SecurityStandards, one or more security standards that the FlavorType is compliant with (TODO: [], define the list of acceptable values)
 - Policy:
   - Aggregatable, describing if multiple instances can be aggregated in one single virtual node
     - MinCount (unit count)[integer]
     - MaxCount (unit count)[integer]

### Sensor

![sensor](https://plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fluidos-project/REAR-data-models/master/models/examples/puml/flavor-types/sensor.txt&fmt=svg)
(TODO: I don't see anywhere the type of sensor (temperature, humidity, ...). If I understood correctly the sensor type describes the technology used, maybe we need another field in the datastructure describing that)
The Sensor Flavor type has the following characteristics:
 - Characteristics
   - SensorType, the type of sensor described by the FlavorType [one of][Environmental, Motion, Proximity, Infrared] 
   - SensorModel, the model of the sensor [string]
   - SensorManufacturer, the sensor manifacturer [string]
   - SensorMarket, (TODO: describe what that means) [string]
   - SamplingRate, the frequency of the measurements (unit sample/sec) [integer]
   - Accuracy, the accuracy reported for the measurements (unit percentage) [0-1]
   - Consumption, the power consumption of the reported sensor (unit mW) [integer]
   - Interface, (TODO: describe what that means)
   - AdditionalProperties
     - MeasurementUnit, further details the measurement unit
     - ConsumptionUnit
     - SamplingRateUnit
     - AccessProtocol
 - Policy
   - Aggregatable, describing if multiple instances can be aggregated in one single virtual node
     - MinCount (unit count)[integer]
     - MaxCount (unit count)[integer]

### Service

![service](https://plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fluidos-project/REAR-data-models/master/models/examples/puml/flavor-types/service.txt&fmt=svg)

The service FlavorType has the following characteristics:
 - Characteristics
   - Name, the name of the service flavor [string].
   - Description, a description of the service flavor [string].
   - Tags, an array of strings representing tags associated with the flavor.
   - Plan, the plan associated with the service flavor [string].
   - Latency, the latency of the service flavor in milliseconds [integer].
 - ServiceType: A reference to a specific service type schema using a JSON reference ($ref) to an external file like "service-types/db.json". This allows defining details specific to each service type.

#### ServiceType DB

