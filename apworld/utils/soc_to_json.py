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
		self.obj_type = obj_type.lower()
		self.key = key.lower()
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
		assert len(parts) == 2
		key, value = parts[0], parts[1]
		working = SOCWork(parts[0], parts[1])
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

for id_str, condition_set in soc["conditionset"].items():
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

locations = {}
items = {}

num_colors = 0
num_cds = 0

for id_str, unlockable in soc["unlockable"].items():
	type_name = unlockable["type"].lower()
	if type_name == "skin":
		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["label"] = "Challenge - Driver: {}".format(parsed_name)
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile

		item = {}
		item["label"] = "Driver: {}".format(parsed_name)
		item["skin"] = unlockable["var"].lower()
		item["group"] = "Drivers"

		locations[id_int] = location
		items[id_int] = item
	elif type_name == "follower":
		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["label"] = "Challenge - Follower: {}".format(parsed_name)
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile

		item = {}
		item["label"] = "Follower: {}".format(parsed_name)
		item["follower"] = unlockable["var"].lower()
		item["group"] = "Followers"

		locations[id_int] = location
		items[id_int] = item
	elif type_name == "color":
		num_colors += 1

		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["label"] = "Challenge - Spray Can #{}".format(num_colors)
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile

		item = {}
		item["label"] = "Spray Can: {}".format(parsed_name)
		item["color"] = unlockable["var"].lower()
		item["group"] = "Spray Cans"

		locations[id_int] = location
		items[id_int] = item
	elif type_name == "cup":
		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["label"] = "Challenge - {}".format(parsed_name)
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile

		item = {}
		item["label"] = "{} Access".format(parsed_name)
		item["cup"] = unlockable["var"].lower()
		item["group"] = "Cup Access"

		locations[id_int] = location
		items[id_int] = item
	elif type_name == "map":
		# These may need a tiny bit of manual cleanup
		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["label"] = "Challenge - {}".format(parsed_name)
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile

		item = {}
		item["label"] = "{} Access".format(parsed_name)
		item["map"] = unlockable["var"]
		item["group"] = "Map Access"

		locations[id_int] = location
		items[id_int] = item
	elif type_name == "altmusic":
		# These need a LOT of manual cleanup.
		# Doesn't even account for the special time attack alt music.
		num_cds += 1

		id_int = int(id_str)
		temp_name = "Alt. Music (index {})".format(id_int)
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["label"] = "Challenge - Prison Egg CD #{}".format(num_cds)
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile

		item = {}
		item["label"] = temp_name
		item["color"] = unlockable["var"].lower()
		item["group"] = "Alt. Music"

		locations[id_int] = location
		items[id_int] = item
	else:
		# These may need a tiny bit of manual cleanup
		id_int = int(id_str)
		parsed_name = unlockable["name"].replace("_", " ")
		condition_set_id = int(unlockable.get("conditionset", 0))
		big_tile = bool(unlockable.get("majorunlock", False))

		location = {}
		location["label"] = parsed_name
		if condition_set_id:
			location["condition_set"] = condition_set_id
		if big_tile:
			location["big_tile"] = big_tile

		item = {}
		item["label"] = parsed_name
		item["item_type"] = type_name

		locations[id_int] = location
		items[id_int] = item


all_output = {
	#"logic": logic,
	"locations": locations,
	"items": items
}

output_file_name = "{}_output.json".format(sys.argv[1])

with open(output_file_name, "wt") as f:
    json.dump(all_output, f, indent="\t", allow_nan=False)

print("Done! Output is at {}".format(output_file_name))
