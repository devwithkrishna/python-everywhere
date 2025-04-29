from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient, StorageSharedKeyCredential

# Inputs
key_vault_name = "<your-keyvault-name>"
secret_name = "<your-secret-name>"  # The name of the secret storing the storage account key
storage_account_name = "<your-storage-account-name>"
container_name = "<your-container-name>"
blob_name = "<your-blob-name>"

# Construct the Key Vault URI
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"

# Authenticate to Key Vault and retrieve the secret
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)
retrieved_secret = secret_client.get_secret(secret_name)
storage_account_key = retrieved_secret.value

# Authenticate to Azure Blob Storage
shared_key_credential = StorageSharedKeyCredential(storage_account_name, storage_account_key)
blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net",
    credential=shared_key_credential
)

# Get the blob client and read the blob content
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
blob_content = blob_client.download_blob().readall()

print(blob_content.decode('utf-8'))
