from __future__ import annotations

from typing import TYPE_CHECKING

import logging
import pkgutil
import json

location_name_to_id: Dict[str, int] = {}
location_name_groups: Dict[str, List[str]] = {}
location_descriptions: Dict[str, str] = {}

item_name_to_id: Dict[str, int] = {}
item_name_groups: Dict[str, List[str]] = {}
item_descriptions: Dict[str, str] = {}

rr_item_defs = {}
rr_location_defs = {}
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
			for location_json in locations_json:
				index = int(location_json["id"])
				assert(index > 0)
				assert(index not in location_name_to_id)

				name = location_json["name"]

				rr_location_defs[name] = location_json
				location_name_to_id[name] = index

				group_keys = location_json.get("tags", None)
				if group_keys:
					for key in group_keys:
						location_name_groups.setdefault(key, []).append(name)

				desc = location_json.get("description", None)
				if desc:
					location_descriptions[name] = desc

		items_json = file_json.get("items", None)
		if items_json:
			for item_json in items_json:
				index = int(item_json["id"])
				assert(index > 0)
				assert(index not in item_name_to_id)

				name = item_json["name"]

				rr_item_defs[name] = item_json
				item_name_to_id[name] = index

				group_keys = item_json.get("tags", None)
				if group_keys:
					for key in group_keys:
						item_name_groups.setdefault(key, []).append(name)

		cups_json = file_json.get("cups", None)
		if cups_json:
			for index_str, cup_json in cups_json.items():
				rr_cup_defs[index_str] = cup_json

		maps_json = file_json.get("maps", None)
		if maps_json:
			for index_str, map_json in maps_json.items():
				rr_map_defs[index_str] = map_json
