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
    venue_id: str = ""
    venue_name: str = ""
    orientation: str = ""


    def __str__(self):
        return f"Screen(id={self.screen_id}, width={self.width}, height={self.height}, name='{self.name}')"


#Use this to get the screens from the vengo csv file
def load_vengo_screens(vengo_file, vengo_screens):
    try:
        with open(vengo_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                screenId = row.get('ad_unit_id', '').strip()
                height = row.get('screen_height', '').strip()
                width = row.get('screen_width', '').strip()
                screenName = row.get('ad_unit_name', '').strip()

                #Check if id actually filled
                if screenId:
                    screen = Screen(screen_id = screenId, screen_height = height, screen_width = width, screen_name = screenName)
                    vengo_screens[screenId] = screen
    
    #Basic error handing
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


#Use this to get the screens from the venueX csv file
def load_venueX_screens(venuex_file, venuex_screens):
    try:
        with open(venuex_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                screenId = row.get('screen_id', '').strip()
                height = row.get('screen_height', '').strip()
                width = row.get('screen_width', '').strip()
                screenName = row.get('screen_name', '').strip()
                venueId = row.get('venue_id', '').strip()
                venueName = row.get('venue_name', '').strip()
                Orientation = row.get('orientation', '').strip()

                #Check is id actually filled and if so create a new screen and store it in the venuex_screens array
                if screenId:
                    screen = Screen(
                        screen_id = screenId,
                        screen_height = height,
                        screen_width = width,
                        screen_name = screenName,
                        venue_id = venueId,
                        venue_name = venueName,
                        orientation = Orientation
                        )
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

    #Use this for differing resolutions - All screens is just all the screens in both venuex and vengo
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

    
    # Output for Screens to add to Vengo
    if Add_to_Vengo:
        print("\nScreens that need to be added to Vengo\n")
        for screen_id in sorted(Add_to_Vengo):
                screen = venuex[screen_id]
                print(f"  {screen.screen_name} | {screen_id}")
    else:
        print("No screens need to be added to Vengo\n")

    #Output for screens to delete from Vengo
    if Delete_From_Vengo:
        print("\nScreens that need to be deleted from Vengo\n")
        for screen_id in sorted(Delete_From_Vengo):
                screen = vengo[screen_id]
                print(f"  {screen.screen_name} | {screen_id}")
    else:
        print("No screens need to be deleted from Vengo")

    #Output for resolution changes
    if resolution_Changes:
        print("Screens that need to have resolutions updated")
        for screen_id in sorted(resolution_Changes):
                screen = venuex_screens[screen_id]
                print(f"  {screen.screen_name} | {screen_id}")
    else:
        print("\nNo screens need resolution changes")

    #If we have screens to add to vengo create a new csv for the screens that need to be added
    if Add_to_Vengo:
        generate_Vengo_CSV(Add_to_Vengo, venuex)

    return Add_to_Vengo, Delete_From_Vengo, resolution_Changes


def generate_Vengo_CSV(screens_to_add, venuex_screens, output_filename="screens_to_add_vengo.csv"):

    if not screens_to_add:
        print("No screens to add")
        return

    try:
        #Open a new csv file to write to
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ad_unit_id', 'ad_unit_name', 'screen_width', 'screen_height', 'orientation', 'venue_id', 'venue_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            #For each screen in screens to add - Find it in venuex screens and correctly add to the new csv in Vengo Format
            for screen_id in sorted(screens_to_add):
                venuex_screen = venuex_screens[screen_id]

            #Get orientation correct for the vengo format
                orientation = venuex_screen.orientation
                if orientation.lower() == "portrait":
                    orientation = "Portrait"
                elif orientation.lower() == "landscape":
                    orientation = "Landscape"
                elif orientation.lower() in ["portraitleft", "portraitright"]:
                 orientation = "Portrait"

            #Create correct rows within the Vengo CSV file
                writer.writerow({
                        'ad_unit_id': venuex_screen.screen_id,
                        'ad_unit_name': venuex_screen.screen_name,
                        'screen_width': venuex_screen.screen_width,
                        'screen_height': venuex_screen.screen_height,
                        'orientation': orientation,
                        'venue_id': venuex_screen.venue_id,
                        'venue_name': venuex_screen.venue_name
                    })
            
        #Output handling
        print(f"\nGenerated CSV file: {output_filename}")
        print(f"Contains {len(screens_to_add)} screens to be added to Vengo")

    #Basic Exception Handling
    except Exception as e:
        print(f"Error generating CSV file: {e}")

def main():
    #Use this for command line argument handling
    if len(sys.argv) != 3:
        print("Usage: python main.py [venuex-csv] [vengo-csv]")
        sys.exit(1)

    venuex_file = sys.argv[1]
    vengo_file = sys.argv[2]

    #Dictionaries using the screen id
    venuex_screens: Dict[str, Screen] = {}
    vengo_screens: Dict[str, Screen] = {}

    load_vengo_screens(vengo_file, vengo_screens)
    print("Loaded Vengo Screens\n")
    load_venueX_screens(venuex_file, venuex_screens)
    print("Loaded VenueX Screens\n")

    reconcile_screens(venuex_screens, vengo_screens)



if __name__ == "__main__":
    main()

