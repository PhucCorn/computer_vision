#include <iostream>
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

int main() {
    cv::VideoCapture cap = cv::VideoCapture(0);
    if (cap.isOpened())  // check if we succeeded
    {
        cv::Mat frame;
        while (true)
        {
            cap >> frame;
            cv::imshow(windowName, frame);
            cv::waitKey(30);
        }
    }
    else
    {
        PrintError("Not found any camera");
    }
}