# Sync Public IP with Google DDNS

This is a very simple python program that will sync your public IP address with your Google DDNS (Dynamic DNS) record. To use this you must have a registered Google domain and a configured Dynamic DNS entry for that domain.

```
$> python google_ddns_sync.py --credentials <your credentials file>
Syncing public ip <your public ip> with Google DDNS for url <your DDNS entry url>

$> python google_ddns_sync.py --credentials <your credentials file>
No change in IP found - no need to sync (current public IP <your public ip>)
```

Once synced, your public IP will stored inside your credentials file so future runs can decide if a sync request needs to be made to Google. A sync request is made only if the public IP address changes between runs (or there isn't a stored public IP in the credentials file)

## Credentials File

This is a json file of the form

```
{
  "url": "your DDNS entry url", 
  "username": "your DDNS entry username - assigned by Google for each entry", 
  "password": "your DDNS entry password - assigned by Google for each entry", 
}
```
