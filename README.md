# endless-pastabilities

## Orchestrator

### gets

`/users/garfield/all`

Arguements: None

Returns: All Garfields (JSON format)

`/users/garfield/id/:id`

Arguements: ID (string of ObjectId)

Returns: Garfields matching passed ID (JSON format)

`/users/garfield/cohort/:cohort`

Arguements: Cohort string

Returns: Garfields matching passed cohort (JSON format)

`/users/mama/all`

Arguements: None

Returns: All Mamas (JSON format)

`/users/mama/id/:id`

Arguements: ID (string of ObjectId)

Returns: Mamas matching passed ID (JSON format)

`/users/mama/cohort/:cohort`

Arguements: Cohort string

Returns: Mamas matching passed cohort (JSON format)

`/optimize/status/:id`

Arguements: Optimizer run ID

Returns: Optimizer control table entry (JSON Format)

`/optimize/results/:id`

Arguements: Optimizer run ID

Returns: Result table entry (JSON Format)

`/optimize/list`

Arguements: None

Returns: Optimizer Control Table entries (JSON Format)

`/optimize/list/idonly`

Arguements: None

Returns: Optimizer Control Table IDs (JSON Format)

`/info/regions`

Arguements: None

Returns: List of distinct regions

`/info/regionalleaders`

Arguements: None

Returns: List of regional leaders

### posts

`/users/garfield/create`

Arguements: Fields for Garfield

Returns: Inserted Object ID

`/users/mama/create`

Arguements: Fields for Mama

Returns: Inserted Object ID

`/optimize/request`

Arguements: List of Garfields and list of Mamas to include

Returns: New optimize run ID