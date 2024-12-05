
import csv
import datetime
from Truck import Truck
from builtins import ValueError
import HashTable
import Package

# Read the file info from CSVs
with open("CSV/Distance_File.csv") as csvfile:
    CSV_Distance = csv.reader(csvfile)
    CSV_Distance = list(CSV_Distance)

with open("CSV/Address_File.csv") as csvfile1:
    CSV_Address = csv.reader(csvfile1)
    CSV_Address = list(CSV_Address)

with open("CSV/Package_File.csv") as csvfile2:
    CSV_Package = csv.reader(csvfile2)
    CSV_Package = list(CSV_Package)


# Create package objects from the CSV package file
# Load package objects into the hash table: package_hash_table
def load_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            ID = int(package[0])
            Address = package[1]
            City = package[2]
            State = package[3]
            Zipcode = package[4]
            Time_to_deliver = package[5]
            Weight = package[6]
            Status = "At Hub"
            Truck = None
            #Create package object
            package = Package.Package(ID, Address, City, State, Zipcode, Time_to_deliver, Weight, Status, Truck)
            

            package_hash_table.insert(ID, package)


# Method for finding distance between two addresses
def distance_in_between(x_value, y_value):
    distance = CSV_Distance[x_value][y_value]
    if distance == '':
        distance = CSV_Distance[y_value][x_value]

    return float(distance)


# Method to get address number from string literal of address
def extract_address(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])


# Create trucks (manually loading them with packages)
truck1 = Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8),1)

truck2 = Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20),2)

truck3 = Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=9, minutes=5),3)

# Create hash table
package_hash_table = HashTable.HashTable()



# Load packages into hash table
load_package_data("CSV/Package_File.csv", package_hash_table)


# Method for ordering packages on a given truck using the nearest neighbor algo
def delivering_packages(truck):
    not_delivered = []
    for packageID in truck.packages:
        package = package_hash_table.search(packageID)
        if package.ID == 9:
                ID = 9
                Address = "410 S State St"
                City = "Salt Lake City"
                State = "UT"
                Zipcode = "84111"
                Time_to_deliver = "EOD"
                Weight = "2 Kilos"
                Status = "At Hub"
                Truck = 3
                newpackage = Package.Package(ID,Address,City,State,Zipcode,Time_to_deliver,Weight,Status,Truck)
                package = newpackage
                package_hash_table.insert(ID,package)
        #Update package that truck is on
        package.truck = truck.id
        not_delivered.append(package)

    truck.packages.clear()

    #While there are packages to be delivered
    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None
        for package in not_delivered:
            if distance_in_between(extract_address(truck.address), extract_address(package.address)) <= next_address:
                next_address = distance_in_between(extract_address(truck.address), extract_address(package.address))
                next_package = package
        truck.packages.append(next_package.ID)
        not_delivered.remove(next_package)

        #add truck statuses
        truck.mileage += next_address
        truck.address = next_package.address
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time

#Deliver packages
delivering_packages(truck1)
delivering_packages(truck2)

#Delay the start of the third truck for packages that come in late
truck3.depart_time = min(truck1.time, truck2.time)

delivering_packages(truck3)


class Main:
    # User Interface
    print("Package delivery system")
    print("The mileage for the route is:")
    print(truck1.mileage + truck2.mileage + truck3.mileage)  # Print total mileage for all trucks

    text = input("To start please type '1' (Any other input will exit the program): \n")

    if text == "1":
        try:
            #Take time to look up
            user_time = input("Please enter a time to check the status of. Use the following format, HH:MM:SS: \n")
            (h, m, s) = user_time.split(":")

            convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            # Determine whether to look up a single package or all.
            second_input = input("To view the status of an individual package please type '1'. For all"
                                 " packages please type '2'.\n")
            
            #Single Package lookup
            if second_input == "1":
                try:
                    # The user will be asked to input a package ID. Invalid entry will cause the program to quit 
                    solo_input = input("Enter the numeric package ID\n")
                    package = package_hash_table.search(int(solo_input))
                    if package is None:
                        print("No package with that ID\n")
                        exit()
                    if package.ID == 9:
                        if convert_timedelta < datetime.timedelta(hours=10,minutes=20,seconds=0):
                            package.address = "300 State St"
                            package.city = "Salt Lake City"
                            package.state = "UT"
                            package.zip = "84103"
                            
                    package.update_status(convert_timedelta)
                    print(str(package))
                  
                    print()
                except ValueError:
                    print("Invalid Entry. Closing program.\n")
                    exit()

            #All package lookup
            elif second_input == "2":
                try:
                    print("Packages for",convert_timedelta)

                    for packageID in range(1, 41):
                        package = package_hash_table.search(packageID)
                        if convert_timedelta < datetime.timedelta(hours=10,minutes=20,seconds=0):
                            if package.ID == 9:
                                package.address = "300 State St"
                                package.city = "Salt Lake City"
                                package.state = "UT"
                                package.zip = "84103"
                        package.update_status(convert_timedelta)
                        print(str(package))
                        
                except ValueError:
                    print("Invalid Entry. Closing program.\n")
                    exit()
            else:
                exit()
        except ValueError:
            print("Invalid Entry. Closing program.\n")
            exit()
    elif input != "time":
        print("Invalid Entry. Closing program.\n")
        exit()