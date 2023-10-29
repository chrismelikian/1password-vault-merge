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

### Generating the commands (running the script!)

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
* `<prefix>-overwrite.txt` - the commands needed to move common items where the legacy vault has a newer updated date and by inference is newer and should supercede the entry in the latest vault. The item in the latest vault is archived first.
* `<prefix>-missing.txt`- the commands to move items which are in the legacy vault but not in the latest vault
* `<prefix>-<legacy-file>-warnings.txt` - items in the legacy vault which have duplicate titles. These need to be processed manually in 1Password before the comparison with another vault can take place. These items are not considered in the vault comparison.
* `<prefix>-<latest-file>-warnings.txt` - items in the latest vault which have duplicate titles. These need to be processed manually in 1Password before the comparison with another vault can take place. These items are not considered in the vault comparison.

## Analysing and running the generated commands
Now that you've generated the commands, it's time for you to review them and do some checks to see if they match your expectations.

### Check for duplicates in each vault and fix them

Check the 2 warning files to see if there are any duplicate entries in each of the vaults. It's worth fixing these first and then re-running the script until there are no more warnings.

### Review Proposed Changes

Go through the generated duplicates, missing and overwrite files and check to see if you're happy with the changes. Comment out or delete the ones you don't want to enact.

To reiterate, only action these commands at your own risk. Do all the good things like backup etc before you do anything.

To run the scripts on Linux/Mac:-
```
sh <prefix>-duplicates.txt
sh <prefix>-overwrite.txt
sh <prefix>-missing.txt
```

To run on Windows. (This is a guess, I don't have Windows):-
```
powershell -f <prefix>-duplicates.txt
powershell -f <prefix>-overwrite.txt
powershell -f <prefix>-missing.txt
```

Note that it can take many minutes to run as each 1Password operation can take almost 2 seconds. There's no way to speed this up.

You may get prompted by 1Password one or more times to allow the CLI commands to execute.

# Background

### Duplicate Deletion
Sample command deletion of duplicate:-
```
echo "Deleting item 'Some Web Site' from vault 'Old'"
op item delete 52tvnplqhjajvnjizgvy5bdefr --archive --vault "Old"
```
### Overwriting of latest vault item
Sample commands for moving an entry from legacy to latest and archiving the latest entry:-
```
echo "Archive item 'www.somewebsite.com' in newer repository, move item from legacy repository to latest"
op item delete lizlfgq6avg4nchlkekxzrahby --archive --vault "Personal"
op item move rktavdo54na4nhasisyd3k4xde --current-vault "Old" --destination-vault "Personal"
```

### Migration Of Missing Item To Latest Vault 
Sample command for moving item from legacy to latest:-
```
echo "Move item 'somwewebsite.com' to 'Personal'"
op item move tbipqgg2rnbstnkvmwlbrhmbqu --current-vault "Old" --destination-vault "Personal"
```
