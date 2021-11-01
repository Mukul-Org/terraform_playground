# Simple Project

This example illustrates how to create a simple project using the `fabric-project` submodule.


<!-- BEGIN TFDOC -->
## Variables

| name | description | type | required | default |
|---|---|:---: |:---:|:---:|
| billing_account | Billing account id. | <code title="">string</code> | ✓ |  |
| parent | Organization or folder id, in the `organizations/nnn` or `folders/nnn` format. | <code title="">string</code> | ✓ |  |
| *activate_apis* | Service APIs to enable. | <code title="list&#40;string&#41;">list(string)</code> |  | <code title="">["compute.googleapis.com"]</code> |
| *name* | Project name, joined with prefix. | <code title="">string</code> |  | <code title="">fabric-project</code> |
| *owners* | Optional list of IAM-format members to set as project owners. | <code title="list&#40;string&#41;">list(string)</code> |  | <code title="">[]</code> |
| *prefix* | Prefix prepended to project name, uses random id by default. | <code title="">string</code> |  | <code title=""></code> |

## Outputs

<!-- END TFDOC -->
