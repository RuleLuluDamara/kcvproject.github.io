import cv2
import numpy as np
import pandas as pd
import math

pixel_sampling_x = 0
pixel_sampling_y = 0
contour_list = []
yuv_list = []
cut_sampling = []
contour_arr = np.zeros(shape=(1, 2))
size = 1200, 1200, 1
frame_yuv = np.zeros(shape=(1, 2))

# predifine yuv value
y_min = 255
y_max = 0
u_min = 255
u_max = 0
v_min = 255
v_max = 0


def click_event(event, x, y, flags, params):
    # get image coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        global pixel_sampling_x, pixel_sampling_y, contour_arr, yuv_list, y_min, y_max, u_min, u_max, v_min, v_max
        # print(x, ' ', y)
        font = cv2.FONT_HERSHEY_SIMPLEX

        if pixel_sampling_x != x and pixel_sampling_y != y:

            cut_sampling.append([x, y])
            pixel_sampling_x = x
            pixel_sampling_y = y

            y_c = frame_yuv[y, x, 0]
            u_c = frame_yuv[y, x, 1]
            v_c = frame_yuv[y, x, 2]

            yuv_list.append([y_c, u_c, v_c])

            p = [pixel_sampling_x, pixel_sampling_y]
            contour_list.append(p)
            # cv2.circle(frame_yuv, p, 2, (0, 0, 255), 2)

            if y_c < y_min:
                y_min = y_c
            if y_c > y_max:
                y_max = y_c
            if u_c < u_min:
                u_min = u_c
            if u_c > u_max:
                u_max = u_c
            if v_c < v_min:
                v_min = v_c
            if v_c > v_max:
                v_max = v_c

        # print(y_min, u_min, v_min, y_max, u_max, v_max)
        if len(contour_list) >= 6:
            # print(contour_list)
            contour_arr = np.array(contour_list, np.int32)
            cv2.fillPoly(frame_yuv, pts=[contour_arr], color=(0, 255, 255))
        # print("this is: ", cut_sampling)
        # cv2.putText(frame_yuv, str(x) + ',' + str(y), (x, y), font, 0.5, (255, 0, 0), 1)
        # cv2.imshow('image', frame_yuv)


def get_lane_width():
    x_min_px = 1200
    x_max_px = 0
    print(cut_sampling)
    for sampling in cut_sampling:
        if sampling[0] < x_min_px:
            x_min_px = sampling[0]
        if sampling[0] > x_max_px:
            x_max_px = sampling[0]
    print("lebarrrrr:" + str(x_max_px - x_min_px))
    return (x_max_px - x_min_px)


def export_yuv():
    # print("melbu yuv nyimpen nilai")
    data_yuv = np.array(yuv_list)
    rows = ["{},{},{}".format(i, j, k) for i, j, k in data_yuv]
    text = "\n".join(rows)
    with open('hmmm.csv', 'w') as f:
        f.write("Y,U,V\n")
        f.write(text)


def coloring_image(frame_bgr, img_path, index):
    # cv2.imshow('kuning', frame_yuv)
    # img_threshold = frame_yuv.copy()
    img_threshold = cv2.imread('static/picture_sample/sample1.jpg')
    # threshold hsv coba-coba
    hsv_image = cv2.cvtColor(img_threshold, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([0, 195, 254])
    upper_bound = np.array([30, 255, 255])

    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    kernel = np.ones((7, 7), np.uint8)

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    segmented_img = cv2.bitwise_and(img_threshold, img_threshold, mask=mask)

    contours, hierarchy = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = cv2.drawContours(frame_bgr, contours, -1, (0, 0, 255), 3)
    # cv2.imshow("output", output)
    vehicle_detection(contours, mask, img_path, index)



def threshold_picture(frame_bgr):
    # lower_bound = np.array([y_min, u_min, v_min])
    # upper_bound = np.array([y_max, u_max, v_max])
    lower_bound = np.array([0, 195, 254])
    upper_bound = np.array([30, 255, 255])
    frame_yuv_thres = cv2.cvtColor(frame_yuv.copy(), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_yuv_thres, lower_bound, upper_bound)

    # cv2.imshow("mask", mask)
    # using convexhull
    kernel = np.ones((7, 7), dtype=np.uint8)
    mask = cv2.inRange(frame_yuv_thres, lower_bound, upper_bound)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # get convex hull
    points = np.column_stack(np.where(mask.transpose() > 0))
    hull = cv2.convexHull(points)

    # draw convex hull on input image in red
    result = frame_bgr.copy()
    cv2.polylines(result, [hull], True, (0, 0, 255), 2)

    # draw white filled hull polygon on black background
    cv2.fillPoly(mask, [hull], 255)

    # get the largest contour from result
    contours = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    big_contour = max(contours, key=cv2.contourArea)

    # draw contour on copy of input
    contr = frame_bgr.copy()
    contr = cv2.drawContours(contr, [big_contour], 0, [0, 0, 255], 2)

    # show result
    # cv2.imshow('result', contr)

    vehicle_detection(big_contour, mask)

    # segmen only the detected region
    segmented_img = cv2.bitwise_and(frame_bgr, frame_bgr, mask=mask)

    # draw boundary of the detected object
    contours, hierarchy = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    area = cv2.contourArea(cnt)
    output = cv2.drawContours(segmented_img, contours, -1, (0, 0, 255), 3)
    print(area)

    # cv2.imshow("output", output)


def vehicle_detection(contours, mask, img_path, index):
    net = cv2.dnn.readNet('static/yolo/yolov3.weights', 'static/yolo/yolov3.cfg')

    classes = []

    with open('static/yolo/coco.names', 'r') as f:
        classes = f.read().splitlines()

    img_ = cv2.imread(str(img_path))
    img = cv2.resize(img_, (1200, 600)) 
    # cap = cv2.VideoCapture('vb.mp4')

    # frame_video_width = int(cap.get(3))
    # frame_video_height = int(cap.get(4))

    # saved_frame = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc(
    #     'M', 'J', 'P', 'G'), 10, (1200, 600))

    # ret, img_ = cap.read()

    # img = cv2.resize(img_, (1200, 600))
    img = cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    blur = cv2.blur(img, (40, 40), 0)
    out = img.copy()
    out[mask == 0] = blur[mask == 0]
    # cv2.imshow("mask",)

    height_original, width_original, color = img.shape

    blob = cv2.dnn.blobFromImage(
        out, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

    net.setInput(blob)

    # get the output layers names
    output_layers_names = net.getUnconnectedOutLayersNames()
    # passing the output layers name into the net forward function
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    # lane_width = get_lane_width()
    lane_width = 1189
    lane_width_m = round((lane_width/100) * 2)

    biggest_vehicle_px_width = 0
    vehicle_id = ''

    for output in layerOutputs:
      for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > 0.4:
            center_x = int(detection[0] * width_original)
            center_y = int(detection[1] * height_original)
            width = int(detection[2] * width_original)
            height = int(detection[3] * height_original)

            x = int(center_x - width/2)
            y = int(center_y - height/2)

            boxes.append([x, y, width, height])
            confidences.append((float(confidence)))
            class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)  # get the index
          # print(indexes.flatten())

    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))
    vehicle_total = 0
    for i in indexes.flatten():
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        # print(classes[class_ids[i]])
        confidence = str(round(confidences[i], 2))
        color = colors[i]
        cv2.rectangle(out, (x, y), (x+w, y+h), color, 2)
        if x+w > biggest_vehicle_px_width:
            biggest_vehicle_px_width = w
            vehicle_id = label
        vehicle_total += 1
        cv2.putText(out, label + " " + confidence,
                    (x, y+20), font, 2, (255, 255, 255), 2)

    # cv2.imshow("offce", out)
    cv2.putText(out, "total vehicle: " + str(vehicle_total),
                (20, 50), font, 2, (255, 255, 255), 2)
    cv2.putText(out, "lane width: " + str(lane_width) +
                " px", (20, 100), font, 2, (255, 255, 255), 2)
    cv2.putText(out, "lane width: " + str(lane_width_m) +
                " m", (20, 150), font, 2, (255, 255, 255), 2)

    # if ret == True:
    #     saved_frame.write(out)
    cv2.imwrite('media/images/result' + str(index) + '.jpg', out)
    # cv2.imshow('video', out)
    # key = cv2.waitKey(0)
    # if key == ord('e'):
        #     break


def run_all(img_path, index):
  global frame_yuv
  img = cv2.imread(str(img_path))
  frame_bgr = cv2.resize(img, (1200, 600))
  frame_yuv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
  coloring_image(frame_bgr, img_path, index)
  # k = cv2.waitKey(0) & 0xFF



# if __name__ == "__main__":
#     img = cv2.imread('pict1.png')
#     frame_bgr = cv2.resize(img, (1200, 600))
#     # cv2.imshow('image', frame_bgr)
#     frame_yuv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

#     # cv2.setMouseCallback('image', click_event)
#     # while True:
#         # k = cv2.waitKey(0) & 0xFF

#     #     if k == ord('c'):
#     #         get_lane_width()
#     #     elif k == ord('x'):
#     #         # print(yuv_list)
#     #         # export_yuv()
#     #         vehicle_detection()
#     #     elif k == ord('t'):
#     #         threshold_picture()
#     #     elif k == ord('w'):
#     #         coloring_image()
#     #     elif k == ord('e'):
#     #         cv2.destroyAllWindows()
#     coloring_image()
#     k = cv2.waitKey(0) & 0xFF

