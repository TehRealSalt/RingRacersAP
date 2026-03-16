from __future__ import annotations

from typing import TYPE_CHECKING

import logging
import pkgutil
import json

# TODO: Get list of regions to create later
# from this data, as well.

location_name_to_id: dict[str, int] = {}
location_name_groups: dict[str, list[str]] = {}

item_name_to_id: dict[str, int] = {}
item_name_groups: dict[str, list[str]] = {}

rr_cup_defs = {}
rr_map_defs = {}

def load_all() -> None:
	# We have a manifest file purely because we can't iterate
	# a directory using pkgutil. But, defining this comes with
	# the added bonus of the file load order being deterministic
	# between our apworld code & the game code itself, so it's
	# not a terrible loss IMO
	manifest_data = pkgutil.get_data(__name__, "data/!manifest.json")
	manifest_json = json.loads(manifest_data)

	for file_name in manifest_json["files"]:
		file_data = pkgutil.get_data(__name__, "data/" + file_name)
		file_json = json.loads(file_data)

		locations_json = file_json.get("locations", None)
		if locations_json:
			for index_str, location_json in locations_json.items():
				index = int(index_str)
				assert(index > 0)
				assert(index not in location_name_to_id)

				name = location_json["name"]
				location_name_to_id[name] = index

				group_keys = location_json.get("group", None)
				if group_keys: # TODO: list of keys support
					location_name_groups.setdefault(group_keys, []).append(name)

		items_json = file_json.get("items", None)
		if items_json:
			for index_str, item_json in items_json.items():
				index = int(index_str)
				assert(index > 0)
				assert(index not in item_name_to_id)

				name = item_json["name"]
				item_name_to_id[name] = index

				group_keys = item_json.get("group", None)
				if group_keys: # TODO: list of keys support
					item_name_groups.setdefault(str(group_keys), []).append(name)

		cups_json = file_json.get("cups", None)
		if cups_json:
			for index_str, cup_json in cups_json.items():
				rr_cup_defs[index_str] = cup_json

		maps_json = file_json.get("maps", None)
		if maps_json:
			for index_str, map_json in maps_json.items():
				rr_map_defs[index_str] = map_json
