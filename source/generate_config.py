import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section("DetectionSettings")
# ADD SETTINGS TO SECTION
config_file.set("DetectionSettings", "check_stacking_queries", "true")
config_file.set("DetectionSettings", "check_comment_at_the_end", "true")
config_file.set("DetectionSettings", "check_union", "true")
config_file.set("DetectionSettings", "check_always_true", "true")
config_file.set("DetectionSettings", "check_always_false", "true")
config_file.set("DetectionSettings", "blocked_keyword_list_enabled", "true")

# SAVE CONFIG FILE
with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

config_file.items()

print("Config file 'configurations.ini' created")

# PRINT FILE CONTENT
read_file = open("configurations.ini", "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()