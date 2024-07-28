#pragma once
#ifndef _MY_ROBOT_HPP_
#define _MY_ROBOT_HPP_

#include "api.h"
#include "EZ-Template/api.hpp"

const bool USE_PID = true;          // if true, PID control is enabled
const bool TRACKING_ENABLED = true; // if true, tracking is enabled

// Sensors
pros::v5::GPS gps(15, -0.221, 0.223); // (PORT_NUM, xOffset, yOffset)
                                      // Offset is the distance of GPS sensor is how far from robot's center
pros::IMU inertial(8);

// Encoder top wire should be port in 1('A'),3('C'),5('E'),7('G').
pros::ADIEncoder leftEncoder('A', 'B', false); // left tracking wheel (vertical)
pros::ADIEncoder rightEncoder('C', 'D', true); // right tracking wheel (vertical)
pros::ADIEncoder backEncoder('E', 'F', false); // back tracking wheel (horizontal)

// Drive train
ez::Drive chassis({
    {1, 2}, // left motors ports
    {-4, -5}, // right motors ports
    7, // IMU (a.k.a Inertial or Gyroscope) port
    4.125, // Wheel Diameter (4" is actually 4.125")
    200, // Wheel RPM (Red is 100, Green is 200, Blue is 600)
    1.0 // Gear ratio (of wheels)
    //, 8  // Left Rotation Port (negative port will reverse it!)
    //,-9  // Right Rotation Port (negative port will reverse it!)
});

// Motors
// pros::Motor MOTOR_VAR_NAME(PORT_NUMBER, COLOR_OF_MOTOR_GEAR, TYPE_OF_MOTOR_DETECTS(usally used in statics of brain))
pros::Motor intake1(10, pros::v5::MotorGears::green, pros::v5::MotorUnits::counts);
pros::Motor intake2(11, pros::v5::MotorGears::green, pros::v5::MotorUnits::counts);
pros::Motor intake3(12, pros::v5::MotorGears::blue, pros::v5::MotorUnits::rotations);
pros::Motor intake4(13, pros::v5::MotorGears::red, pros::v5::MotorUnits::degrees);

// controller
pros::Controller master(pros::E_CONTROLLER_MASTER);
//pros::Controller partner(pros::E_CONTROLLER_PARTNER); // uncomment to use partner controller
#endif