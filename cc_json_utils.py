"""
cc_dat_utils modified to read and convert json data
"""
import json
import cc_data

# Constructs fields (title, traps, cloning machines, password (enc/reg), hint, monsters)
def make_field_from_json(field_type, field_data):
    """Constructs and returns the appropriate optional field
    Args:
        field_type (int) : what type of field to construct
        field_data : the json data to be used to create the field
    """
    # field_data is title
    if field_type == cc_data.CCMapTitleField.TYPE:
        return cc_data.CCMapTitleField(field_data)

    # field_data is list-dict(button/trap)-list(coordinates)
    elif field_type == cc_data.CCTrapControlsField.TYPE:
        traps = []
        # account for more than 1 trap
        for i in field_data:
            trap = i["trap"][0]
            #button coordinate (bx, by)
            bx = trap["button"][0]
            by = trap["button"][1]
            #trap coordinate (tx, ty)
            tx = trap["trap"][0]
            ty = trap["trap"][1]
            #add coordinates to the list of traps
            traps.append(cc_data.CCTrapControl(bx,by,tx,ty))
        return  cc_data.CCTrapControlsField(traps)
    
    
    elif field_type == cc_data.CCCloningMachineControlsField.TYPE:
        machines = []
        # account for more than 1 machine
        for i in field_data:
            machine = i["machine"][0]
            #button coordinates (bx, by)
            bx = machine["button"][0]
            by = machine["button"][1]
            #trap coordinates (tx, ty)
            tx = machine["machine"][0]
            ty = machine["machine"][1]
            #add coordinates to the list of traps
            machines.append(cc_data.CCCloningMachineControl(bx,by,tx,ty))
        return  cc_data.CCCloningMachineControlsField(machines)

    # field_data is list of ints
    elif field_type == cc_data.CCEncodedPasswordField.TYPE:
        return cc_data.CCEncodedPasswordField(field_data)

    # field_data is hint string
    elif field_type == cc_data.CCMapHintField.TYPE:
        return cc_data.CCMapHintField(field_data)

    # field_data is pass string
    elif field_type == cc_data.CCPasswordField.TYPE:
        return cc_data.CCPasswordField(field_data)

    # field_data is list-dict("monster")- list (coordinates)
    elif field_type == cc_data.CCMonsterMovementField.TYPE:
        monsters = []
        for i in field_data:
            monster = i["monster"]
            mx = monster[0]
            my = monster[1]
            monsters.append(cc_data.CCCoordinate(mx, my))
        return cc_data.CCMonsterMovementField(monsters)

    # Unknown field type
    else:
        if __debug__:
            raise AssertionError("Unknown field type: " + str(field_type))
        return cc_data.CCField(field_type, field_data)

#Finds fields to make from level data
def make_optional_fields_from_json(level_data):
    
    fields = []
    # map title
    if ("Map Title Field" in level_data):
        map_title = level_data["Map Title Field"]
        fields.append(make_field_from_json(3, map_title))
    # traps
    if ("Trap Controls Field" in level_data):
        traps = level_data["Trap Controls Field"]
        fields.append(make_field_from_json(4, traps))
    # clone machines
    if ("Cloning Machine Controls Field" in level_data):
        clones = level_data["Cloning Machine Controls Field"]
        fields.append(make_field_from_json(5, clones))
    # encoded password
    if ("Encoded Password Field" in level_data):
        encpass = level_data["Encoded Password Field"]
        fields.append(make_field_from_json(6, encpass))
    # string password (not part of requirements but was in dat_utils)
    if ("Password Field" in level_data):
        strpass = level_data["Password Field"]
        fields.append(make_field_from_json(8, strpass))
    # hint
    if ("Map Hint Field" in level_data):
        hint = level_data["Map Hint Field"]
        fields.append(make_field_from_json(7, hint))
    # monsters
    if ("Monster Movement Field" in level_data):
        monsters = level_data["Monster Movement Field"]
        fields.append(make_field_from_json(10, monsters))
    return fields

def make_level_from_json(level_data):
    
    level = cc_data.CCLevel()
    level.level_number = level_data["Level Number"]
    level.time = level_data["Time Limit"]
    level.num_chips = level_data["Chip Count"]
    level.upper_layer = level_data["Upper Layer"]
    level.lower_layer = level_data["Lower Layer"]
    # Optional fields: MapTitle, Traps, Cloning, Password, Hint, Monsters
    level.optional_fields = make_optional_fields_from_json(level_data)
   
    print("Level #"+str(level_data["Level Number"])+" complete\n")
    return level

# Creates data from json file using other functions
def make_cc_data_from_json(json_file):
    data = cc_data.CCDataFile()
    reader = open(json_file, "r")

    #Open File
    json_data = json.load(reader)

    for i in range(len(json_data["Level Pack"])):
        level_key = "Level #"+str(i+1)
       
        level_data = json_data["Level Pack"][i][level_key]
        level = make_level_from_json(level_data)
        data.levels.append(level)

    print("cc_data Creation Complete")
    return data
