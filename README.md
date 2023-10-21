# 1Password Vault Merge

## About

### Disclaimer
I'm just writing a script to solve my problems. I take no responsibility whatsoever for what you run or do with your vaults. You do everything at your own risk.

### Why?
After migrating from a file-based 1Password vault to 1Password in the cloud, I found myself with 2 vaults, "Old" and "Personal".

"Personal" was just a copy of "Old" and I never deleted it. Over time as 1Password displayed both vaults when searching for entries, the old vault entries got edited instead of the new and my whole password collection became a bit of a mess and I'm tired of seeing duplicate entries.... hence this script!

### What Problem Does It Solve?
This script will:-
* Delete duplicate entries from the old vault
* Move more recently updated entries with the same title from the old to the new vault. Entries that were overwritten in the new vault are archived first in 1Password.
* Move unique entries in the old vault to the new vault


### Terrible idea, I don't trust your script!
I don't blame you, you should be worried! :-)

The approach I've come up with is to generate a set of 1Password CLI commands which will perform the changes but this script doesn't run them.

Instead, it's left for you, dear reader, to review and execute the generated script in part or whole as you see fit.

## How To Use

### Pre-requisities

1. You'll need Python 3 [installed and configured](https://wiki.python.org/moin/BeginnersGuide/Download)
2. Set up 1Password CLI as per https://developer.1password.com/docs/cli/get-started
2. Run `op vault list` to ensure your 1Password CLI is working correctly
3. Get the names of your 2 vaults and apply the terminology I'm going to be using:- 
   1. 'Latest' Vault is the newer vault, the one that you want to keep eventually. For me the vault name was 'Personal'
   2. 'Legacy' Vault is your original vault that you want to delete eventually. For me the vault name was 'Old'

### Generating the commands

You'll need to extract the metadata for each vault using:-
```
op item list --vault='Old' --format=json > legacy.json
op item list --vault='Personal' --format=json > latest.json
``` 
1Password for the Mac prompts me for whether to allow this action, you'll need to accept the action to continue.

Now, run the script in your Terminal window, PowerShell or command line prompt:-

```
python3 generate-1p-merge-commands.py legacy.json latest.json > commands.txt
```
where 'legacy.json' is the old vault you eventually want to remove and latest.json is the vault you want to keep.

This will create a file called `commands.txt` containing the changes to apply to your vaults.

### Analysing and running the generated commands

The 'commands.txt' file is divided into 3 sections:-
* deletion of duplicates from the legacy vault
* moving entries with the same title from the legacy vault to the latest vault while archiving the corresponding entry in the latest vault first
* moving entries to the latest vault that are present in the legacy vault but not in the latest vault

Sample command deletion of duplicate:-
```
# Deleting item 'Some Web Site' from vault 'Old'
op item delete 52tvnplqhjajvnjizgvy5bdefr --archive --vault "Old"
```

Sample commands for moving an entry from legacy to latest and archiving the latest entry:-
```
# archive item 'www.somewebsite.com' in newer repository, move item from old repository to new
op item delete lizlfgq6avg4nchlkekxzrahby --archive --vault "Personal"
op item move rktavdo54na4nhasisyd3k4xde --current-vault "Old" --destination-vault "Personal"
```

Sample command for moving item from legacy to latest:-
```
# move item 'somwewebsite.com' to 'Personal
op item move tbipqgg2rnbstnkvmwlbrhmbqu --current-vault "Old" --destination-vault "Personal"
```

Review the commands that have been generated and you can either copy/paste the ones you want into a new script or rename the file to commands.sh and execute it as per your operating system.
