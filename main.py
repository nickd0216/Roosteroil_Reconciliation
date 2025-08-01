import csv
import sys
from dataclasses import dataclass
from typing import Dict, List, Set

#Set up a screen object to keep track of screen number and resolution
@dataclass
class Screen:
    screen_id: str
    screen_width: int
    screen_height: int
    screen_name: str


    def __str__(self):
        return f"Screen(id={self.screen_id}, width={self.width}, height={self.height}, name='{self.name}')"


#Use this to get the screens from each file
def load_vengo_screens(vengo_file, vengo_screens):
    try:
        with open(vengo_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                screenId = row.get('ad_unit_id', '').strip()
                height = row.get('screen_height', '').strip()
                width = row.get('screen_width', '').strip()
                screenName = row.get('ad_unit_name', '').strip()

                #Check is id actually filled
                if screenId:
                    screen = Screen(screen_id = screenId, screen_height = height, screen_width = width, screen_name = screenName)
                    vengo_screens[screenId] = screen
    
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def load_venueX_screens(venuex_file, venuex_screens):
    try:
        with open(venuex_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                screenId = row.get('screen_id', '').strip()
                height = row.get('screen_height', '').strip()
                width = row.get('screen_width', '').strip()
                screenName = row.get('screen_name', '').strip()

                #Check is id actually filled
                if screenId:
                    screen = Screen(screen_id = screenId, screen_height = height, screen_width = width, screen_name = screenName)
                    venuex_screens[screenId] = screen

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


        

def reconcile_screens(venuex, vengo):
    #Use these to compare the screen ids
    venuex_ids: Set[str] = set(venuex.keys())
    vengo_ids: Set[str] = set(vengo.keys())

    #in vengo but not venuex
    Delete_From_Vengo = vengo_ids - venuex_ids

    #In venuex but not vengo
    Add_to_Vengo = venuex_ids - vengo_ids

    resolution_Changes = []
    all_screens = venuex_ids & vengo_ids

    #Get the screens that have different resolutions for both
    for screen_id in all_screens:
        venuex_screen = venuex[screen_id]
        vengo_screen = vengo[screen_id]

        if venuex_screen.screen_width != vengo_screen.screen_width:
            resolution_Changes.append(id)
        elif venuex_screen.screen_height != vengo_screen.screen_height:
            resolution_Changes.append(id)

    
    if Add_to_Vengo:
        print("\nScreens that need to be added to Vengo\n")
        for screen_id in sorted(Add_to_Vengo):
                screen = venuex[screen_id]
                print(f"  {screen.screen_name} | {screen_id}")
    else:
        print("No screens need to be added to Vengo\n")

    if Delete_From_Vengo:
        print("\nScreens that need to be deleted from Vengo\n")
        for screen_id in sorted(Delete_From_Vengo):
                screen = vengo[screen_id]
                print(f"  {screen.screen_name} | {screen_id}")
    else:
        print("No screens need to be deleted from Vengo")

    if resolution_Changes:
        print("Screens that need to have resolutions updated")
        for screen_id in sorted(resolution_Changes):
                screen = venuex_screens[screen_id]
                print(f"  {screen.screen_name} | {screen_id}")
    else:
        print("\nNo screens need resolution changes")



def main():
    if len(sys.argv) != 3:
        print("Wrong Arguments")
        sys.exit(1)

    venuex_file = sys.argv[1]
    vengo_file = sys.argv[2]

    venuex_screens: Dict[str, Screen] = {}
    vengo_screens: Dict[str, Screen] = {}

    load_vengo_screens(vengo_file, vengo_screens)
    print("Loaded Vengo Screens\n")
    load_venueX_screens(venuex_file, venuex_screens)
    print("Loaded VenueX Screens\n")

    reconcile_screens(venuex_screens, vengo_screens)



if __name__ == "__main__":
    main()

