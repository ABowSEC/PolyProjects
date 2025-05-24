from lodgingSites.expedia import scrape_lodging
from skiSites.ski_com import scrape_ski_com
# from liftopia import scrape_lodging as scrape_liftopia  # When ready
# from onthesnow import scrape_lodging as scrape_onthesnow  # When ready

resort_mapping = {
    'copper mountain': 'copper-mountain-resort',
    'vail': 'vail',
    'breckenridge': 'breckenridge',
    'aspen': 'aspen-snowmass'
}

def main():
    print("Welcome to Ski Trip Planner!")
    print("Supported resorts:", ", ".join(resort_mapping.keys())," You may enter others as long as proper format for site links")

    resort = input("Enter the resort you are planning to visit: ").strip().lower()

#error handling
    if resort not in resort_mapping:
        print(f"Sorry, '{resort}' is not supported yet.")
        return

    resort_slug = resort_mapping[resort]
#process for Lodging
    print(f"\nFetching lodging info for {resort.title()}...\n")

    expedia_results = scrape_lodging(resort_slug)

    if not expedia_results:
        print("No results found on Expedia.")
    else:
        for hotel in expedia_results:
            print(f"Expedia: {hotel['name']} — {hotel['price']}")
#process for skiPackages
    print(f"\nSearching for ski packages with {resort.title()}...\n")           #ADD signifier for site being used possibly loop when each sites can be collected

    skiPackageResult = scrape_ski_com(resort.title()) #Title case for ski.com search box maybe better here//analyze//


    if not skiPackageResult:
        print("No ski packages found.")
    else:
        print("\nSki.com Results:")
        for result in skiPackageResult:
            print(f"{result['name']} — {result['price']}")


    # Combine/ process results 
    # liftopia_results = scrape_liftopia(resort_slug)
    # onthesnow_results = scrape_onthesnow(resort_slug)


if __name__ == "__main__":
    main()
