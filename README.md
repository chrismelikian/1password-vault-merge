# 1Password Cleanup

## About

### Disclaimer
I'm just writing a script to solve my problems. I take no responsibility whatsoever for what you run or do with your vaults. You do everything at your own risk.

### Why?
After migrating from a file-based 1Password vault to 1Password in the cloud, I found myself with 2 vaults, "Old" and "Personal".

"Personal" was just a copy of "Old" and I never deleted it. Over time as 1Password displayed both vaults when searching for entries, the old vault entries got edited instead of the new and my whole password collection became a bit of a mess and I'm tired of seeing duplicate entries.... hence this script! :-)

### What Problem Does It Solve?
This script will:-
* Delete duplicate entries from the old vault
* Move more recently updated entries with the same title from the old to the new vault
* Move unique entries in the old vault to the new vault

### Terrible idea, I don't trust your script!
I don't blame you, you should be worried! :-)

The approach I've come up with is to generate a set of 1Password CLI commands which will perform the changes but this script doesn't run them.

Instead, it's left for you, dear reader, to execute the generated scripts in part or whole as you see fit.

There are 2 scripts you can run, one is a script to extract the password vault entry metadata to a file, the other is a script to parse the metadata and generate the script.

## How To Use

### Pre-requisities

1. You'll need Python 3 installed and configured
2. Edit the op-compare.py script at line 4 to make sure the comment character is appropriate for your environment when the commands are generated
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





