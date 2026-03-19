import json
import sys

if len(sys.argv) < 2:
	print("soc_to_json <file>: convert Ring Racers' SOC to JSON meant for Archipelago")
	quit()

# Get raw text blob
raw_lines = []

with open(sys.argv[1], "rt") as f:
	raw_lines = f.readlines()

# Parse out comments
lines = []
for line in raw_lines:
	if line.startswith("#"):
		continue

	line = line.split(" #")[0]
	line = line.strip()
	if line:
		lines.append(line)


# Parse into generic object representing the SOC.
# Don't concern ourselves with correcting the types yet,
# just work on getting it all tokenized.
soc = {}


class SOCWork:
	def __init__(self, obj_type, key):
		print(f"SOCWORK key: {key}")
		self.obj_type = obj_type.lower()
		if key:
			self.key = key.lower()
		else:
			self.key = None
		self.obj = {}

	def set_val(self, key, val):
		if key in self.obj:
			prev_val = self.obj[key]

			val_list = prev_val
			if not isinstance(val_list, list):
				val_list = list()
				val_list.append(prev_val)

			val_list.append(val)
			self.obj[key] = val_list
			return

		self.obj[key] = val


working: SOCWork = None


def commit_working_obj():
	global working

	if working is not None:
		if working.obj_type not in soc:
			soc[working.obj_type] = {}

		soc[working.obj_type][working.key] = working.obj

	working = None


for line in lines:
	line = line.strip()

	if not line:
		commit_working_obj()
		continue

	parts = line.split()
	if "=" not in line:
		commit_working_obj()

		if len(parts) < 1:
			continue

		key = parts[0]
		print(key)

		try:
			value = parts[1]
		except:
			value = None
		print(value)

		working = SOCWork(key, value)
	elif working is not None:
		key, value = [i.strip() for i in line.split("=", 1)]
		working.set_val(key.lower(), value)

commit_working_obj()


# Print values directly to ensure correctness
print("==== SOC INPUT ====")
print(json.dumps(soc, indent="\t", allow_nan=False))


# Put everything into a format that is less crappy
# and into structures better suited for AP
logic = {}

for id_str, condition_set in soc.get("conditionset", {}).items():
	id_int = int(id_str)

	logic_set = []
	set_id = 0

	while(True):
		set_id += 1
		set_key = "condition{}".format(set_id)

		if not set_key in condition_set:
			break

		this_condition = condition_set[set_key]
		if isinstance(this_condition, list):
			logic_set.append("; ".join(this_condition))
		else:
			logic_set.append(this_condition)

	logic[id_int] = logic_set

locations = []
items = []

num_colors = 0
num_cds = 0

for id_str, unlockable in soc.get("unlockable", {}).items():
	type_name = unlockable["type"].lower()
	if type_name == "skin":
		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["id"] = id_int
		location["name"] = "Challenge - Driver: {}".format(parsed_name)
		location["label"] = parsed_name
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile
		location["tags"] = ["Challenges", "Drivers"]

		item = {}
		item["id"] = id_int
		item["name"] = "Driver: {}".format(parsed_name)
		item["label"] = parsed_name
		item["unlockable"] = id_int
		item["skin"] = unlockable["var"].lower()
		item["tags"] = ["Drivers"]

		locations.append(location)
		items.append(item)
	elif type_name == "follower":
		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["id"] = id_int
		location["name"] = "Challenge - Follower: {}".format(parsed_name)
		location["label"] = parsed_name
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile
		location["tags"] = ["Challenges", "Followers"]

		item = {}
		item["id"] = id_int
		item["name"] = "Follower: {}".format(parsed_name)
		item["label"] = parsed_name
		item["unlockable"] = id_int
		item["follower"] = unlockable["var"].lower().replace("_", " ")
		item["tags"] = ["Followers"]

		locations.append(location)
		items.append(item)
	elif type_name == "color":
		num_colors += 1

		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["id"] = id_int
		location["name"] = "Challenge - Spray Can #{}".format(num_colors)
		location["label"] = "Spray Can #{}".format(num_colors)
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile
		location["tags"] = ["Challenges", "Spray Can Milestones"]

		item = {}
		item["id"] = id_int
		item["name"] = "Spray Can: {}".format(parsed_name)
		item["label"] = parsed_name
		item["unlockable"] = id_int
		item["color"] = unlockable["var"].lower()
		item["tags"] = ["Spray Cans"]

		locations.append(location)
		items.append(item)
	elif type_name == "cup":
		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["id"] = id_int
		location["name"] = "Challenge - {}".format(parsed_name)
		location["label"] = parsed_name
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile
		location["tags"] = ["Challenges", "Cups"]

		item = {}
		item["id"] = id_int
		item["name"] = "{} Access".format(parsed_name)
		item["label"] = parsed_name
		item["unlockable"] = id_int
		item["cup"] = unlockable["var"]
		item["tags"] = ["Cups"]
		item["icon"] = unlockable["icon"]

		locations.append(location)
		items.append(item)
	elif type_name == "map":
		# These may need a tiny bit of manual cleanup
		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["id"] = id_int
		location["name"] = "Challenge - {}".format(parsed_name)
		location["label"] = parsed_name
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile
		location["tags"] = ["Challenges", "Maps"]

		item = {}
		item["id"] = id_int
		item["name"] = "{} Access".format(parsed_name)
		item["label"] = parsed_name
		item["unlockable"] = id_int
		item["map"] = unlockable["var"]
		item["tags"] = ["Maps"]

		locations.append(location)
		items.append(item)
	elif type_name == "altmusic":
		# These need a LOT of manual cleanup.
		# Doesn't even account for the special time attack alt music.
		num_cds += 1

		id_int = int(id_str)
		temp_name = "Alt. Music (index {})".format(id_int)
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["id"] = id_int
		location["name"] = "Challenge - Prison Egg CD #{}".format(num_cds)
		location["label"] = "Prison Egg CD #{}".format(num_cds)
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile
		location["tags"] = ["Challenges", "CD Milestones"]

		item = {}
		item["id"] = id_int
		item["name"] = temp_name
		item["label"] = temp_name
		item["unlockable"] = id_int
		item["color"] = unlockable["var"].lower()
		item["tags"] = ["Alt. Music"]

		locations.append(location)
		items.append(item)
	else:
		# These may need a tiny bit of manual cleanup
		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["id"] = id_int
		location["name"] = "Challenge - {}".format(parsed_name)
		location["label"] = parsed_name
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile
		location["tags"] = ["Challenges", "Extras"]

		item = {}
		item["id"] = id_int
		item["name"] = parsed_name
		item["label"] = parsed_name
		item["unlockable"] = id_int
		item["item_type"] = type_name
		item["tags"] = ["Extras"]

		locations.append(location)
		items.append(item)


cups = {}
maps = {}

for id_str, cup_data in soc.get("cup", {}).items():
	cup = {}

	race_map_list = cup_data["levellist"].lower().split(",")
	battle_map_list = cup_data["bonusgame"].lower().split(",")
	special_map = cup_data["specialstage"].lower()

	bonus_modulo = max(1, (len(race_map_list) + 1) // (len(battle_map_list) + 1));

	all_maps = list()
	race_index = 0
	bonus_index = 0
	while race_index < len(race_map_list):
		for i in range(bonus_modulo):
			all_maps.append(race_map_list[race_index])
			race_index += 1

			if race_index >= len(race_map_list):
				break

		if (race_index < len(race_map_list) and bonus_index < len(battle_map_list)):
			all_maps.append(battle_map_list[bonus_index])
			bonus_index += 1

	all_maps.append(special_map)

	real_name = cup_data.get("realname", "")
	if not real_name:
		real_name = id_str.split("_", 1)[1]

	has_credits = bool(cup_data.get("playcredits", False))

	cup["label"] = real_name
	cup["map_list"] = all_maps
	if has_credits:
		cup["has_credits"] = has_credits

	cups[id_str] = cup


for id_str, map_data in soc.get("level", {}).items():
	cur_map = {}

	real_name = map_data.get("levelname", "")
	zone_title = map_data.get("zonetitle", "")
	if zone_title:
		real_name += " " + zone_title
	act_num = map_data.get("act", "")
	if act_num:
		real_name += " " + act_num

	short_name = real_name

	extra_title = map_data.get("menutitle", "")
	if extra_title:
		real_name += ": " + extra_title
		short_name = extra_title

	map_type = map_data["typeoflevel"].lower()
	time_attack_medals = 0
	prison_break_medals = 0
	spb_attack_medals = 0

	attached_locations = []
	if map_type == "race":
		time_attack_medals += 3 # Skip platinum (for now?)
		spb_attack_medals += 1
		attached_locations.append("Spray Can")
	elif map_type == "battle":
		prison_break_medals += 3 # Skip platinum (for now?)
		#attached_locations.append("Prison CD") # TODO

	no_visit_needed = bool(map_data.get("novisitneeded", False))

	# There isn't a way to detect Mystic Melody shrine
	# from the header alone, so there is some required
	# manual clean-up

	cur_map["label"] = real_name
	if short_name != real_name:
		cur_map["label_short"] = short_name
	cur_map["type"] = map_type

	if no_visit_needed:
		cur_map["no_visit_needed"] = no_visit_needed

	if time_attack_medals:
		cur_map["medals_time"] = time_attack_medals

	if spb_attack_medals:
		cur_map["medals_spb"] = spb_attack_medals

	if prison_break_medals:
		cur_map["medals_prisons"] = prison_break_medals

	if len(attached_locations):
		all_location_names = []

		for location_suffix in attached_locations:
			location_name = "{} - {}".format(real_name, location_suffix)
			all_location_names.append(location_name)

			location = {}
			location["id"] = 0 # Needs manual cleanup
			location["name"] = location_name
			location["label"] = "{}: {}".format(short_name, location_suffix)
			location["spray_can_map"] = id_str
			location["tags"] = ["Spray Cans"]
			locations.append(location)

		cur_map["locations"] = all_location_names

	maps[id_str] = cur_map


all_output = {
	#"logic": logic,
	"cups": cups,
	"maps": maps,
	"locations": locations,
	"items": items
}

output_file_name = "{}_output.json".format(sys.argv[1])

with open(output_file_name, "wt") as f:
    json.dump(all_output, f, indent="\t", allow_nan=False)

print("Done! Output is at {}".format(output_file_name))
