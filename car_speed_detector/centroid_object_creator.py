import cv2
from constants import MIN_CONFIDENCE, CLASSES, MAX_NUM_OF_CONSECUTIVE_FRAMES_FOR_ACTION, MAX_DISTANCE_FROM_THE_OBJECT
from logger import Logger
import numpy as np
from centroid_tracker import CentroidTracker


class CentroidObjectCreator:
    def __init__(self):
        # initialize our list of bounding box rectangles returned by
        # either (1) our object detector or (2) the correlation trackers
        self.rects = []
        self.rect = None
        self.objects = None

        self.frame = None
        # keep the count of total number of frames
        self.total_frames = 0
        self.ct = CentroidTracker(maxDisappeared=MAX_NUM_OF_CONSECUTIVE_FRAMES_FOR_ACTION,
                                  maxDistance=MAX_DISTANCE_FROM_THE_OBJECT)

    def convert_frame_to_detections(self):
        """
        Convert frame to detections.
        """
        blob = cv2.dnn.blobFromImage(self.frame, size=(300, 300), ddepth=cv2.CV_8U)
        self.net.setInput(blob, scalefactor=1.0 / 127.5, mean=[127.5, 127.5, 127.5])
        detections = self.net.forward()
        self.rects = []
        return detections

    def loop_over_detections_fetch_tracker_update_trackers_list(self, detections):
        """
        Loop over the detections.
        If confidence in the detections is greater than minimum confidence level,
            1. Extract the index of the class label from the detections list.
            2. Make sure that the class label is a person.
            3. Compute the (x,y) coordinates of the bounding box.
            4. Construct a dlib rectangle object from the bounding box.
            5. Start dlib correlation tracker.
            6. Append the tracker to the list of trackers.
        """
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated
            # with the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence`
            # is greater than the minimum confidence
            if confidence > MIN_CONFIDENCE:
                # extract the index of the class label from the
                # detections list
                idx = int(detections[0, 0, i, 1])

                # if the class label is not a car, ignore it
                if CLASSES[idx] != "car":
                    Logger.logger().debug("class label {} is not a person.".format(CLASSES[idx]))
                    continue
                self.total_frames += 1
                # compute the (x, y)-coordinates of the bounding box
                # for the object
                box = detections[0, 0, i, 3:7] * np.array([self.W, self.H, self.W, self.H])
                (startX, startY, endX, endY) = box.astype("int")

                cv2.rectangle(self.frame, (startX, startY), (endX, endY),
                              (0, 255, 0), 2)

                # update the bounding box rectangles list
                self.rects.append(box.astype("int"))

    def create_centroid_tracker_object(self, H, W, rgb, net, frame):
        """
        This function does the following:
        1. Computes the tracker and appends it to trackers list.
        2. Appends the coordinates from trackers to rects list.
        3. Updates the object centroids with the newly computed rects list.
        """

        self.H = H
        self.W = W
        self.rgb = rgb
        self.net = net
        self.frame = frame
        # initialize our list of bounding box rectangles returned by
        # either (1) our object detector or (2) the correlation trackers
        self.rects = []
        detections = self.convert_frame_to_detections()
        if detections is not None:
            self.loop_over_detections_fetch_tracker_update_trackers_list(detections)
        # use the centroid tracker to associate the (1) old object
        # centroids with (2) the newly computed object centroids
        self.objects = self.ct.update(self.rects)

        return self.objects
