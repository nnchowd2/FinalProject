# Name: Nafisa Chowdhury
# PSID: 1591144

import csv  # import CSV module
import datetime  # import datetime module


# 1 (a) Create FullInventory report from Manufacturer, Price, and Service Date list

def get_Full_Inventory(file_name1, file_name2, file_name3):
    # Create an output file to write (FullInventory file)
    with open("FullInventory.csv", "w", newline="") as writeFile:
        # create csv writer object
        outputFile = csv.writer(writeFile)

        # read the csv input file (Manufacturer list)
        with open(file_name1, "r") as readFile1:
            # create csv reader object
            inputFile1 = csv.reader(readFile1)

            # Create an empty list
            list1 = []

            # iterate over the rows of the input file
            for row in inputFile1:
                # Append the rows to list1
                list1.append(row)
                # sort the list by manufacturer name
                list1 = sorted(list1, key=lambda col: col[1], reverse=False)

            readFile1.close()  # close the file

            # Read and append Price List
            with open(file_name2, "r") as readFile2:
                inputFile2 = csv.reader(readFile2)

                list2 = []

                for row in inputFile2:
                    list2.append(row)

                readFile2.close()

                # Read and append Service Date list
                with open(file_name3, "r") as readFile3:
                    inputFile3 = csv.reader(readFile3)

                    list3 = []

                    for row in inputFile3:
                        list3.append(row)

                    readFile3.close()

                    # write to file
                    for item1 in list1:  # iterate over each row of the lists
                        for item2 in list2:
                            for item3 in list3:
                                # map item IDs for each list
                                if item1[0:1] == item2[0:1] == item3[0:1]:
                                    # slice and concatenate all the lists and write to FullInventory file (ID, manufacturer name, item type, price, service date list, and damage indicator)
                                    outputFile.writerow(item1[0:3] + item2[1:] + item3[1:] + item1[-1:])


# 1 (b) Create a file for each of the item types

def get_Item_Inventory(file_name):
    # read the full inventory file that was created in 1(a)
    with open(file_name, "r") as readFile:
        reader = csv.reader(readFile)

        readList = []

        for row in reader:
            readList.append(row)
            # sort by ID
            readList = sorted(readList, key=lambda col: col[0], reverse=False)

        readFile.close()

        for item in readList:
            # declare a variable for item types as strings
            p = str(item[2])
            # create an output file for each item type
            with open(p + "Inventory.csv", "w", newline="") as invFile:
                writeFile = csv.writer(invFile)

                # check if the item types exist in the list and populate the inventory files with their respective items
                for i in readList:
                    if p in i:
                        writeFile.writerow(i[0:2] + i[3:6])


# 1 (c) Create a file for items that past the service date

def get_Item_Past_Service_Date(file_name):
    #  read FullInventory file
    with open(file_name, "r") as readFile:
        reader = csv.reader(readFile)

        # sort the file by dates
        reader = sorted(reader, key=lambda col: datetime.datetime.strptime(col[4], "%m/%d/%Y"))

        # create a new file for the expired items
        with open("PastServiceDateInventory.csv", "w", newline="") as dateFile:
            serviceDate = csv.writer(dateFile)

            for row in reader:
                # convert the dates to datetime
                row[4] = datetime.datetime.strptime(row[4], "%m/%d/%Y").date()
                # write the dates that are past the current date
                if row[4] < datetime.date.today():
                    serviceDate.writerow(row)


# 1 (d) Create a file for items that are damaged

def get_Damage_Report(file_name):
    # read the full inventory file that was created in 1(a)
    with open(file_name, "r") as readFile:
        reader = csv.reader(readFile)

        readList = []

        for row in reader:
            readList.append(row)
            # sort the file by price (most expensive to least expensive
            readList.sort(key=lambda col: float(col[3], ), reverse=True)

        readFile.close()

        with open("DamagedInventoryList.csv", "w", newline="") as damagedFile:
            damaged = csv.writer(damagedFile)

            for row in readList:
                # check if the damage indicator cell is populated
                if row[5]:
                    damaged.writerow(row[0:5])


# call the functions

get_Full_Inventory("ManufacturerList.csv", "PriceList.csv", "ServiceDatesList.csv")
get_Item_Inventory("FullInventory.csv")
get_Item_Past_Service_Date("FullInventory.csv")
get_Damage_Report("FullInventory.csv")


# Create menu

def menu():
    print("MENU\n"
          "a- Enter item\n"
          "q- Quit")


# Read and search the Full Inventory file for the desired input

def csvReader(file_name):
    with open(file_name, "r") as readFile:
        reader = csv.reader(readFile)

        readList = []

        for row in reader:
            row[4] = datetime.datetime.strptime(row[4], "%m/%d/%Y").date()
            # find items that are not expired (service dates not past the current date)
            if row[4] > datetime.date.today():
                # find items that are not damaged
                if not row[5]:
                    # append the items that meet the above conditions
                    readList.append(row[0:4])
                    # sort by prices (most expensive to least)
                    # the program will find the most expensive item that meet all the conditions, first and display that item to the user
                    readList.sort(key=lambda col: float(col[3], ), reverse=True)

        readFile.close()

        # declare a global variable
        found = False

        for line in readList:
            # convert manufacturer name and item type data to lowercase
            line[1] = line[1].lower()
            line[2] = line[2].lower()
            # check if the desired item type is found in the list
            if line[2] in name:
                # check if the desired manufacturer is found in the list
                if line[1] in name:
                    # if the item with the desired manufacturer name and item type is found return True
                    found = True
                    # Capitalize manufacturer names and item types
                    line[1] = line[1].capitalize()
                    line[2] = line[2].capitalize()
                    # print the found item
                    print("Your item is: {}, {}, {}, ${}".format(line[0], line[1], line[2], line[3]))
                    break
        # if the item is found
        if found:
            for item in readList:
                # if the list has the desired item type
                if item[2] in name:
                    # if the list does not have he desired manufacturer
                    if item[1] not in name:
                        item[1] = item[1].capitalize()
                        item[2] = item[2].capitalize()
                        # print and suggest similar items from different manufacturer
                        print("You may also consider: {}, {}, {}, ${}".format(item[0], item[1], item[2], item[3]))
                        break
        # if item is not found
        if not found:
            print("No such item in inventory")


# call the menu function
# prompt user to enter an option from the menu
menu()
option = input("Choose an option:\n")

while option != "q":
    if option == "a":
        # prompt user to enter the manufacturer name and item type
        name = input("Enter item:\n")
        # user input is converted to lowercase
        name = name.lower()
        # call function to search the csv file for the desired item
        csvReader("FullInventory.csv")
    else:
        print("Invalid option")

    # display the menu again and prompt the user to either Quit the program or enter another item
    menu()
    option = input("Choose an option:\n")
