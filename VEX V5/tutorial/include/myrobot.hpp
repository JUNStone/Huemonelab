#pragma once
#ifndef _MY_ROBOT_HPP_
#define _MY_ROBOT_HPP_

#include "api.h"
#include "EZ-Template/api.hpp"

pros::v5::GPS gps(15, -0.221, 0.223); // (PORT_NUM, xOffset, yOffset)
                                      // Offset is the distance of GPS sensor is how far from robot's center
pros::IMU inertial(8);

ez::Drive chassis({
    {1, 2, 3}, // left motors ports
    {-4, -5, -6}, // right motors ports
    7, // IMU (a.k.a Inertial or Gyroscope) port
    4.125, // Wheel Diameter (4" is actually 4.125")
    200, // Wheel RPM (Red is 100, Green is 200, Blue is 600)
    1.0 // Gear ratio (of wheels)
    //, 8  // Left Rotation Port (negative port will reverse it!)
    //,-9  // Right Rotation Port (negative port will reverse it!)
});

// pros::Motor MOTOR_VAR_NAME(PORT_NUMBER, COLOR_OF_MOTOR_GEAR, TYPE_OF_MOTOR_DETECTS(usally used in statics of brain))
pros::Motor intake(10, pros::v5::MotorGears::green, pros::v5::MotorUnits::counts);

// controller
pros::Controller master(pros::E_CONTROLLER_MASTER);
//pros::Controller partner(pros::E_CONTROLLER_PARTNER); // uncomment to use partner controller
#endif