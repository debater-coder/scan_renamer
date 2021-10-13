import os
from datetime import date
from time import sleep


class ScanRenamer:
    def __init__(self, scan_directory, class_list_directory):
        self.scan_directory = scan_directory
        self.class_list_directory = class_list_directory
        self.classes = os.listdir(self.class_list_directory)
        self.scans = os.listdir(self.scan_directory)
        self.class_name = None
        self.task_name = None

    def present_classes(self):
        print("CLASSES:")
        for _class in self.classes:
            print("\t" + _class[:-4])

    @staticmethod
    def is_valid_scan_name(scan_name):
        try:
            int(scan_name[:-4])
            return scan_name[-4:] == ".pdf" and len(scan_name) == 12
        except ValueError:
            return False

    def preview_and_rename(self):
        with open(os.path.join(self.class_list_directory, self.class_name + ".txt")) as class_list:
            students = class_list.readlines()

        valid_scans = []
        for scan in self.scans:
            if self.is_valid_scan_name(scan):
                valid_scans.append(scan)

        print()
        print("RENAMING PREVIEW:")
        print("CURRENT NAME\tNAME AFTER RENAME")
        renamed_scans = []
        if len(valid_scans) == len(students):
            for index, valid_scan in enumerate(valid_scans):
                name = students[index].split("\t")[1]
                iso_date = date.today().isoformat()
                renamed_scan = f"{name}_{self.class_name}_{self.task_name}_{iso_date[:4] + iso_date[5:7] + iso_date[8:10]}.pdf"
                renamed_scans.append(renamed_scan)
                print(valid_scan, end="\t")
                print(renamed_scan)
        else:
            print("Invalid scan directory: not enough scans for every student")
            return

        should_continue = ""
        while should_continue not in ["y", "Y", "yes", "Yes", "YES"]:
            should_continue = input("Continue? [Y/n] ")
            if should_continue in ["n", "N", "no", "No", "NO"]:
                return
        print()
        print("Renaming", end="")
        for i in range(3):
            sleep(0.5)
            print(".", end="")
        print()
        for index, valid_scan in enumerate(valid_scans):
            os.rename(
                os.path.join(self.scan_directory, valid_scan),
                os.path.join(self.scan_directory, renamed_scans[index])
            )
        print("Rename complete!")


if __name__ == "__main__":
    scans_dir = input("Enter scan directory: ")
    classes_dir = input("Enter class list directory: ")
    renamer = ScanRenamer(scans_dir, classes_dir)
    renamer.present_classes()
    renamer.class_name = input("Enter class name: ")
    renamer.task_name = input("Enter task name: ")
    renamer.preview_and_rename()
