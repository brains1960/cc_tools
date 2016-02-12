import json
import cc_data
import cc_dat_utils
import sys

def make_field_from_json(field_type,field_data):
    #Check what field type then returning the corresponding Data
    if field_type == cc_data.CCMapTitleField.TYPE:
        return cc_data.CCMapTitleField(field_data)
    elif field_type == cc_data.CCMapHintField.TYPE:
        return cc_data.CCMapHintField(field_data)
    elif field_type == cc_data.CCPasswordField.TYPE:
        return cc_data.CCPasswordField(field_data)
    elif field_type == cc_data.CCEncodedPasswordField.TYPE:
        #Finds create the password field from data in json
        password = []
        for i in field_data:
            password.append(i)
        return cc_data.CCEncodedPasswordField(password)
    elif field_type == cc_data.CCTrapControlsField.TYPE:
        traps = []
        for i in field_data:
            button_x = i["trap"][0]["button"][0]
            button_y = i["trap"][0]["button"][1]
            
            trap_x = i["trap"][0]["trap"][0]
            trap_y = i["trap"][0]["trap"][1]
            
            traps.append(cc_data.CCTrapControl(button_x,button_y,
                                               trap_x,trap_y))
        
        return  cc_data.CCTrapControlsField(traps)
    elif field_type == cc_data.CCCloningMachineControlsField.TYPE:
        machines = []
        for i in field_data:
            button_x = i["machine"][0]["button"][0]
            button_y = i["machine"][0]["button"][1]
 
            trap_x = i["machine"][0]["machine"][0]
            trap_y = i["machine"][0]["machine"][1]
            
            machines.append(cc_data.CCCloningMachineControl(button_x,button_y,
                                                            trap_x,trap_y))
        
        return  cc_data.CCCloningMachineControlsField(machines)
    elif field_type == cc_data.CCMonsterMovementField.TYPE:
        monsters = []
        for i in field_data:
            monster_x = i["monster"][0]
            monster_y = i["monster"][1]
            monsters.append(cc_data.CCCoordinate(monster_x, monster_y))
        return cc_data.CCMonsterMovementField(monsters)
    else:
        if __debug__:
            raise AssertionError("Unknown field type: " + str(field_type))
        return cc_data.CCField(field_type, field_data)



def make_optional_fields_from_json(json_level):
    #Check for remaining optional fields from the level
    fields = []
    
    if("Map Title Field" in json_level):
        map_title = json_level['Map Title Field']
        fields.append(make_field_from_json(3,map_title))

    if("Encoded Password Field" in json_level):
        level_password = json_level['Encoded Password Field']
        fields.append(make_field_from_json(6, level_password))

    if("Password Field" in json_level):
        level_password = json_level['Password Field']
        fields.append(make_field_from_json(8, level_password))
    
    if("Map Hint Field" in json_level):
        level_hint = json_level['Map Hint Field']
        fields.append(make_field_from_json(7,level_hint))
    
    if("Trap Controls Field" in json_level):
        level_traps = json_level['Trap Controls Field']
        fields.append(make_field_from_json(4, level_traps))
    
    if("Cloning Machine Controls Field" in json_level):
        level_machines = json_level['Cloning Machines Controls Field']
        fields.append(make_field_from_json(5, level_machines))

    if("Monster Movement Field" in json_level):
        level_monsters = json_level['Monster Movement Field']
        fields.append(make_field_from_json(10, level_monsters))
    return fields

#Creates a layer from the json data
def make_layer_from_json(json_layer):
    layer_data = []
    index = 0
    while index < len(json_layer):
        tile = json_layer[index]
        index += 1
        layer_data.append(tile)
    return layer_data

#Creates level from given data
def make_level_from_json(json_level):
    level = cc_data.CCLevel()
    level.level_number = json_level["Level Number"]
    level.time = json_level["Time Limit"]
    level.num_chips = json_level["Chip Count"]
    level.upper_layer = make_layer_from_json(json_level["Upper Layer"])
    level.lower_layer = make_layer_from_json(json_level["Lower Layer"])
    level.optional_fields = make_optional_fields_from_json(json_level["Optional Fields"])
    return level

    
#Creates a cc_data file from json file
def make_cc_data_from_json(json_file):
    #Gets data from json file
    data = cc_data.CCDataFile()
    file = open(json_file, 'r')
    json_data = json.load(file)
    index = 1
    #Goes through data loaded from json file, makes levels from json
    #and adds to a list
    for i in range(len(json_data["Level Pack"])):
        level_heading = "Level #" + str(index)
        chosen_lvl = json_data["Level Pack"][i]
        level = make_level_from_json(chosen_lvl[level_heading])
        data.levels.append(level)
        index = index+1
    return data
