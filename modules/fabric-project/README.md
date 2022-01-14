# Google Cloud Simple Project Creation

This module allows simple Google Cloud Platform project creation, with minimal service and project-level IAM binding management. It's designed to be used for architectural design and rapid prototyping, as part of the [Cloud Foundation Fabric](https://github.com/terraform-google-modules/cloud-foundation-fabric) environments.

The resources/services/activations/deletions that this module will create/trigger are:

- one project
- zero or one project metadata items for OSLogin activation
- zero or more project service activations
- zero or more project-level IAM bindings
- zero or more project-level custom roles
- zero or one project liens

## Usage

Basic usage of this module is as follows:

```hcl
module "project_myproject" {
  source                    = "terraform-google-modules/project-factory/google//modules/fabric-project"
  parent                    = "folders/1234567890"
  billing_account           = "ABCD-1234-ABCD-1234"
  prefix                    = "staging"
  name                      = "myproject"
  oslogin                   = true
  owners                    = ["group:admins@example.com"]
  oslogin_admins            = ["group:admins@example.com"]
  gce_service_account_roles = ["foo-project:roles/compute.networkUser"]
}
```

<!-- BEGIN TFDOC -->
## Variables

| name | description | type | required | default |
|---|---|:---: |:---:|:---:|
| name | Project name and id suffix. | <code title="">string</code> | ✓ |  |
| parent | The resource name of the parent Folder or Organization. Must be of the form folders/folder_id or organizations/org_id. | <code title="">string</code> | ✓ |  |
| prefix | Prefix used to generate project id and name. | <code title="">string</code> | ✓ |  |
| *activate_apis* | Service APIs to enable. | <code title="list&#40;string&#41;">list(string)</code> |  | <code title="">[]</code> |
| *auto_create_network* | Whether to create the default network for the project. | <code title="">bool</code> |  | <code title="">false</code> |
| *billing_account* | Billing account ID. | <code title="">string</code> |  | <code title=""></code> |
| *custom_roles* | Map of role name => comma-delimited list of permissions to create in this project. | <code title="map&#40;string&#41;">map(string)</code> |  | <code title="">{}</code> |
| *editors* | Optional list of IAM-format members to set as project editor. | <code title="list&#40;string&#41;">list(string)</code> |  | <code title="">[]</code> |
| *extra_bindings_members* | List of comma-delimited IAM-format members for additional IAM bindings, one item per role. | <code title="list&#40;string&#41;">list(string)</code> |  | <code title="">[]</code> |
| *extra_bindings_roles* | List of roles for additional IAM bindings, pair with members list below. | <code title="list&#40;string&#41;">list(string)</code> |  | <code title="">[]</code> |
| *gce_service_account_roles* | List of project id=>role to assign to the default GCE service account. | <code title="list&#40;string&#41;">list(string)</code> |  | <code title="">[]</code> |
| *labels* | Resource labels. | <code title="map&#40;string&#41;">map(string)</code> |  | <code title="">{}</code> |
| *lien_reason* | If non-empty, creates a project lien with this description. | <code title="">string</code> |  | <code title=""></code> |
| *oslogin* | Enable oslogin. | <code title="">bool</code> |  | <code title="">false</code> |
| *oslogin_admins* | List of IAM-format members that will get OS Login admin role. | <code title="list&#40;string&#41;">list(string)</code> |  | <code title="">[]</code> |
| *oslogin_users* | List of IAM-format members that will get OS Login user role. | <code title="list&#40;string&#41;">list(string)</code> |  | <code title="">[]</code> |
| *owners* | Optional list of IAM-format members to set as project owners. | <code title="list&#40;string&#41;">list(string)</code> |  | <code title="">[]</code> |
| *viewers* | Optional list of IAM-format members to set as project viewers. | <code title="list&#40;string&#41;">list(string)</code> |  | <code title="">[]</code> |

## Outputs

| name | description | sensitive |
|---|---|:---:|
| cloudsvc_service_account | Cloud services service account (depends on services). |  |
| custom_roles | Ids of the created custom roles. |  |
| gce_service_account | Default GCE service account (depends on services). |  |
| gke_service_account | Default GKE service account (depends on services). |  |
| name | Name (depends on services). |  |
| number | Project number (depends on services). |  |
| project_id | Project id (depends on services). |  |
<!-- END TFDOC -->
