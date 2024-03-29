from ultralytics import YOLO
import cv2 as cv
import numpy as np
import pandas as pd


def countvehicle(filename):
    model = YOLO("yolov8m.pt")
    
    img = cv.imread(f"F:\\Mini-Project\\{filename}")
    results = model(img)
    class_ids = []
    car_count=0
    bus_count=0
    motorcycle_count=0
    truck_count=0
    person_count=0
    for result in results[0]:
        class_id = result.boxes.cls.cpu().numpy().astype(int)
        if class_id == 0:
            person_count += 1
        elif class_id == 2:
            car_count += 1
        elif class_id == 3:
            motorcycle_count += 1
        elif class_id == 5:
            bus_count += 1
        elif class_id == 7:
            truck_count += 1
    total_motorcycle_count = person_count+motorcycle_count
    total = car_count+total_motorcycle_count+bus_count+truck_count
    # print("Person count:-",person_count)
    print("Car_Count:- ",car_count)
    print("MotorCycle_Count:- ",total_motorcycle_count)
    print("Bus_Count:- ",bus_count)
    print("Truck_Count:- ",truck_count)
    print("Total:-",total)
    return car_count,total_motorcycle_count,bus_count,truck_count
if __name__=='__main__':
    countvehicle()