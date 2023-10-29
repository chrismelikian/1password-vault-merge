import json
import datetime as dt
import getopt
import sys

latest_vault_map = {}
legacy_vault_map = {}


def read_file(filename, output_prefix):
    map = {}
    warnings_file = open(f"{output_prefix}-{filename}-warnings.txt", "w")
    file = open(filename)
    data = json.load(file)
    for i in data:
        key = i['title'] + ":::" + i['created_at']
        if key in map.keys():
            warnings_file.write("Item with title '{title}' and created date '{date}' has duplicates in file '{file}. Items with this title/created date will NOT be processed.\n"
                            .format(title = i['title'], date=i['created_at'], file=filename))
            del map[key]
        else:
            map[key] = i
    file.close()
    warnings_file.close()
    return map

def delete_item_command(item):
    commands = "echo \"Deleting item '{item_name}' from vault '{vault_name}'\"\n"\
        .format(item_name=item['title'], vault_name=item['vault']['name'])
    commands += "op item delete {id} --archive --vault \"{vault_name}\""\
        .format(id=item['id'], vault_name=item['vault']['name'])
    return commands


def move_and_overwrite_item_command(legacy_item, latest_item):
    commands = "echo \"Archive item '{title}' in latest repository, move item from legacy repository to latest\"\n"\
        .format(title=legacy_item['title'])
    commands += "op item delete {id} --archive --vault \"{destination_vault}\"\n"\
        .format(id=latest_item['id'], destination_vault=latest_item['vault']['name'])
    commands += "op item move {id} --current-vault \"{current_vault}\" --destination-vault \"{destination_vault}\""\
        .format(id=legacy_item['id'], current_vault=legacy_item['vault']['name'], destination_vault=latest_item['vault']['name'])
    return commands


def move_item_command(legacy_item, destination_vault_name):
    commands = "echo \"Move item '{title}' to '{destination_vault}'\"\n"\
        .format(title=legacy_item['title'], destination_vault=destination_vault_name)
    commands += "op item move {id} --current-vault \"{current_vault}\" --destination-vault \"{destination_vault}\"" \
        .format(id=legacy_item['id'], current_vault=legacy_item['vault']['name'], destination_vault=destination_vault_name)
    return commands

def calculate_differences():
    common_keys = filter(lambda x: x in latest_vault_map, legacy_vault_map)
    duplicated_entries_keys = set()
    newer_legacy_entries = set()
    for key in sorted(common_keys):
        latest_ts = dt.datetime.strptime(latest_vault_map[key]['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        legacy_ts = dt.datetime.strptime(legacy_vault_map[key]['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        if latest_ts == legacy_ts:
            duplicated_entries_keys.add(key)
        else:
            if legacy_ts > latest_ts:
                newer_legacy_entries.add(key)
    missing_keys = legacy_vault_map.keys() - latest_vault_map.keys()

    return common_keys, duplicated_entries_keys, missing_keys, newer_legacy_entries

def main(argv):
    opts, args = getopt.getopt(argv,"h",["legacy-file=","latest-file=","output-prefix="])
    latest_file_name = None
    legacy_file_name = None
    output_prefix = None
    for opt, arg in opts:
        if opt == '-h':
            print("generate-1p-merge.py --legacy-file=<old-metadata-file> --latest-file=<newer-metadata-file> --output-prefix=<prefix for output files>")
            sys.exit()
        elif opt == '--legacy-file':
            legacy_file_name = arg
        elif opt == '--latest-file':
            latest_file_name = arg
        elif opt == '--output-prefix':
            output_prefix = arg
    latest_vault_map = read_file(latest_file_name, output_prefix)
    legacy_vault_map = read_file(legacy_file_name, output_prefix)

    common_keys, duplicated_entries_keys, missing_keys, newer_legacy_entries = calculate_differences()

    dupes_file = open(f"{output_prefix}-duplicates.txt", "w")
    for i in duplicated_entries_keys:
        dupes_file.write(delete_item_command(legacy_vault_map[i]))
    dupes_file.close()

    newer_file = open(f"{output_prefix}-newer.txt", "w")
    for i in newer_legacy_entries:
        newer_file.write(move_and_overwrite_item_command(legacy_vault_map[i], latest_vault_map[i]))
    newer_file.close()

    latest_file = open(f"{output_prefix}-latest.txt", "w")
    latest_vault_item = next(iter(latest_vault_map.items()))[1]
    latest_vault_name = latest_vault_item['vault']['name']
    for i in sorted(missing_keys):
        latest_file.write(move_item_command(legacy_vault_map[i], latest_vault_name))
    latest_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])
