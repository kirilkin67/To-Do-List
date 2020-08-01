# print(issubclass(SuperRobot, (AstromechDroid, MedicalDroid,
#                               BattleDroid, PilotDroid)))

# print(issubclass(SuperRobot, AstromechDroid))
# print(issubclass(SuperRobot, MedicalDroid))
# print(issubclass(SuperRobot, BattleDroid))
# print(issubclass(SuperRobot, PilotDroid))

# droids = (AstromechDroid, MedicalDroid, BattleDroid, PilotDroid)
for droid in (AstromechDroid, MedicalDroid, BattleDroid, PilotDroid):
    print(issubclass(SuperRobot, droid))
