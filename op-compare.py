import json
import datetime as dt

COMMENT_CHAR = '#'

def read_file(filename):
    map_by_title = {}
    file = open(filename)
    data = json.load(file)
    for i in data:
        map_by_title[i['title']] = i
    file.close()
    return map_by_title

def delete_item_command(item):
    commands = "{comment_char} Deleting item '{item_name}' from vault '{vault_name}'\n"\
        .format(item_name=item['title'], comment_char=COMMENT_CHAR, vault_name=item['vault']['name'])
    commands += "op item delete {id} --archive --vault \"{vault_name}\""\
        .format(id=item['id'], vault_name=item['vault']['name'])
    return commands


def move_and_overwrite_item_command(legacy_item, latest_item):
    commands = "{comment_char} archive item '{title}' in newer repository, move item from old repository to new\n"\
        .format(title=legacy_item['title'], comment_char=COMMENT_CHAR)
    commands += "op item delete {id} --archive --vault \"{destination_vault}\"\n"\
        .format(id=latest_item['id'], destination_vault=latest_item['vault']['name'])
    commands += "op item move {id} --current-vault \"{current_vault}\" --destination-vault \"{destination_vault}\""\
        .format(id=legacy_item['id'], current_vault=legacy_item['vault']['name'], destination_vault=latest_item['vault']['name'])
    return commands

def move_item_command(legacy_item, destination_vault_name):
    commands = "{comment_char} move item '{title}' to '{destination_vault}\n"\
        .format(comment_char=COMMENT_CHAR, title=legacy_item['title'], destination_vault=destination_vault_name)
    commands += "op item move {id} --current-vault \"{current_vault}\" --destination-vault \"{destination_vault}\"" \
        .format(id=legacy_item['id'], current_vault=legacy_item['vault']['name'], destination_vault=destination_vault_name)
    return commands


latest_vault_map = read_file('personal.json')
legacy_vault_map = read_file('old.json')

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

print('# delete dupes')
for i in duplicated_entries_keys:
    print(delete_item_command(legacy_vault_map[i]))

print('\n# Move newer items from old to new')
for i in newer_legacy_entries:
    print(move_and_overwrite_item_command(legacy_vault_map[i], latest_vault_map[i]))

print('\n# move over items not in latest vault')
latest_vault_item = next(iter(latest_vault_map.items()))[1]
latest_vault_name = latest_vault_item['vault']['name']
for i in sorted(missing_keys):
    print(move_item_command(legacy_vault_map[i], latest_vault_name))
