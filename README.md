# 1Password Vault Merge

## About

### Disclaimer
I'm just writing a script to solve my problems. I take no responsibility whatsoever for what you run or do with your vaults with or without my code or documentation. You do everything at your own risk.

### Why?
After migrating from a file-based 1Password vault to 1Password in the cloud and some imports of old vaults and some laziness, I found myself with 2 vaults, "Old" and "Personal".

What I ended up with is 2 vaults with many duplicates and some entries in the older vault containing newer passwords and some entries that weren't in the newer vault at all.

In 1Password when I need to choose a Login item I often get many choices with the same name which is very frustrating.

### What Problem Does It Solve?
This script will generate commands to:-
* Delete duplicate entries from the old vault
* Move more recently updated entries with the same title from the old to the new vault. Entries that were overwritten in the new vault are archived first in 1Password.
* Move unique entries in the old vault to the new vault

This should help to get to the stage where you can have just one vault and no duplicates.

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
   2. 'Legacy' Vault is your older vault that you want to delete eventually. For me the vault name was 'Old'

### Generating the commands

You'll need to extract the metadata for each vault using:-
```
op item list --vault='Old' --format=json > legacy.json
op item list --vault='Personal' --format=json > latest.json
``` 
1Password for the Mac prompts me for whether to allow this action, you'll need to accept the action to continue.

Now, run the script in your Terminal window, PowerShell or command line prompt:-

```
python3 generate-1p-merge-commands.py --legacy-file=legacy.json --latest-file=latest.json --output-prefix=20231029-0954
```
where:-
* `--legacy-file` is the old vault you eventually want to remove,
* `--latest-file` is the vault you want to keep and
* `--output-prefix` is the prefix given to the multiple output files, so you can seem them as a collection

The output files will be:-
* `<prefix>-duplicates.txt` - the commands needed to delete common items from the legacy repository.
* `<prefix>-newer.txt` - the commands needed to move common items where the legacy vault has a new updated date and by inference is newer and should supercede the entry in the latest vault
* `<prefix>-latest.txt`- the commands to move items which are in the legacy vault but not in the latest vault
* `<prefix>-<legacy-file>-warnings.txt` - items in the legacy vault which have duplicate titles. These need to be processed manually in 1Password before the comparison with another vault can take place. These items are not considered in the vault comparison.
* `<prefix>-<latest-file>-warnings.txt` - items in the latest vault which have duplicate titles. These need to be processed manually in 1Password before the comparison with another vault can take place. These items are not considered in the vault comparison.





Note that it can take many minutes to run as each 1Password operation can take almost 2 seconds. There's no way to speed this up.

When you run multiple 1Password CLI commands from a single shell script you only get prompted once.

This will create a file called `commands.txt` containing the changes to apply to your vaults.

### Analysing and running the generated commands

The 'commands.txt' file is divided into 3 sections:-
* deletion of duplicates from the legacy vault
* moving entries with the same title from the legacy vault to the latest vault while archiving the corresponding entry in the latest vault first
* moving entries to the latest vault that are present in the legacy vault but not in the latest vault

Sample command deletion of duplicate:-
```
echo "Deleting item 'Some Web Site' from vault 'Old'"
op item delete 52tvnplqhjajvnjizgvy5bdefr --archive --vault "Old"
```

Sample commands for moving an entry from legacy to latest and archiving the latest entry:-
```
echo "Archive item 'www.somewebsite.com' in newer repository, move item from legacy repository to latest"
op item delete lizlfgq6avg4nchlkekxzrahby --archive --vault "Personal"
op item move rktavdo54na4nhasisyd3k4xde --current-vault "Old" --destination-vault "Personal"
```

Sample command for moving item from legacy to latest:-
```
echo "Move item 'somwewebsite.com' to 'Personal'"
op item move tbipqgg2rnbstnkvmwlbrhmbqu --current-vault "Old" --destination-vault "Personal"
```

Review the commands that have been generated and you can either copy/paste the ones you want into a new script or rename the file to commands.sh and execute it as per your operating system.
