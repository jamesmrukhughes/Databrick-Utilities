# Databricks notebook source
# DBTITLE 1,Notebook Functions
import requests

def displaySecretScopePermissions(token: str, databricksInstanceUrl: str, scopeName: str):
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Make the request
    response = requests.get(
        f"{databricksInstanceUrl}/api/2.0/secrets/acls/list",
        headers=headers,
        params={"scope": scopeName}
    )

    # Check response
    if response.status_code == 200:
        acls = response.json().get("items", [])

        display(acls)

    else:
        print(f"❌ Failed to retreive permissions on the {scopeName} scope: {response.status_code} - {response.text}")

# COMMAND ----------

# DBTITLE 1,Initiate Widgets to Collect Input
# Build the full Url for the Databricks workspace to be used in the REST API calls
workspaceUrl = f"""https://{spark.conf.get("spark.databricks.workspaceUrl")}"""

# Retrieve a list of Secret Scopes that have been configured for the workspace and
# iterate through them to build a list of choices to be displayed in the dropdown
scopes = dbutils.secrets.listScopes()
scopeNames = [scope.name for scope in scopes]

# Add a Default (None Selected) option to the Secret Scope dropdown as the first item
scopeNames.insert(0, "None Selected")

# Display Widget to Collect Personal Access Token
dbutils.widgets.text("Personal Access Token", "", "01 - Enter Access Token")

# Display Widget to Choose Secret Scope
dbutils.widgets.dropdown(
    name="Secret Scope",
    defaultValue="None Selected",
    choices=scopeNames if scopeNames else ["None Selected"],
    label="02 - Select Secret Scope"
)

# COMMAND ----------

# DBTITLE 1,Retrieve and Display the Secret Scope Permissions
# Retrieve the access token and selected secret scope values from the notebook widgets
token = dbutils.widgets.get("Personal Access Token")
selectedScope = dbutils.widgets.get("Secret Scope")

# Ensure an Access Token has been provided
if token != "":
    # Ensure a Secret Scope was chosen
    if selectedScope != "None Selected":
        displaySecretScopePermissions(token, workspaceUrl, selectedScope)
    else:
        print("❌ Please choose a Secret Scope.")
else: 
    print("❌ Please enter a valid Access Token.")