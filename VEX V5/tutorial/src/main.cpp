#include "main.h"
#include "myrobot.hpp"

void autonomous() {

	switch (auto_start_point) {
	case AUTO_RED_LEFT:
		auto_red_left();
		break;
	case AUTO_RED_RIGHT:
		auto_red_right();
		break;
	case AUTO_BLUE_LEFT:
		auto_blue_left();
		break;
	case AUTO_BLUE_RIGHT:
		auto_blue_right();
		break;
	default:
		auto_example();
		break;
	}
	
}

void auto_red_left() {

}

void auto_red_right() {
}

void auto_blue_left() {
	
}

void auto_blue_right() {

}

void auto_example() {
	inertial.tare_heading(); // you can move this function to autonomous stage
	gps.set_position(-0.45, -1.55, inertial.get_heading()); // starting position
	chassis.drive_set(64, 64);			// move forward
	while (gps.get_position_x() < 0.5); // wait until robot moves 50cm forward
	chassis.drive_set(0, 0);			// stop robot

	// 50cm
	// PID 50.05cm
	// GPS+Inertial 50.1cm
	// Drvie train PID control 50.12cm
	// Block coding 51cm

	// inertial can calculate pitch, yaw, roll
	// but we just need yaw
	// inertial.get_yaw()

	chassis.pid_drive_set(24.0, 64, true); // move forward at 50% power
	chassis.pid_wait_until(6.0);           // don't execute the next code(wait) until robot moves 6.0(in inch)

	intake.move(127); // turn on the intaker

	chassis.pid_wait_quick_chain(); // don't execute the next code(wait) until the motor power reaches to 100%
	intake.move(0); // turn off the intaker

	chassis.pid_turn_set(45.0, 64); // you can set value negative if you want to turn counter-clockwise
	chassis.pid_wait_quick_chain(); // don't execute the next code(wait) until...

	chassis.pid_turn_set(-45.0, 64); // you can set value positive if you want to turn clockwise
	chassis.pid_wait_quick_chain(); // don't execute the next code(wait) until...

	chassis.pid_turn_set(0, 64); // set rotation to zero-point
	chassis.pid_wait();

	intake.move(-127);
	chassis.pid_drive_set(-24.0, 64, true);
	chassis.pid_wait();
	intake.move(0);
}

void tracking_initialize() {
	if (TRACKING_ENABLED) {
		leftEncoder.reset();
		rightEncoder.reset();
		backEncoder.reset();
		
		leftEncoderValue = leftEncoder.get_value();
		rightEncoderValue = rightEncoder.get_value();
		backEncoderValue = backEncoder.get_value();

		deltaLeft = deltaRight = deltaBack = 0.0f;
		// orientation should be radian, but inertial value is degree
		// to change deg to rad, we should multiply (M_PI/180.0f) == (0.017453f)
		initialOrientation = inertial.get_heading() * 0.017453f;
	}
}

float tracking_check() {
	int currentLeft = leftEncoder.get_value() - leftEncoderValue;
	int currentRight = rightEncoder.get_value() - rightEncoderValue;
	int currentBack = backEncoder.get_value() - backEncoderValue;

	// need wheel diameter
	deltaLeft = currentLeft * trackingWheelDiameter * M_PI;
	deltaRight = currentRight * trackingWheelDiameter * M_PI;
	deltaBack = currentBack * trackingWheelDiameter * M_PI;

	float totalLeft = leftEncoder.get_value() * trackingWheelDiameter * M_PI;
	float totalRight = rightEncoder.get_value() * trackingWheelDiameter * M_PI;

	float ceta = initialOrientation + (totalLeft - totalRight) / (leftFromCenter + rightFromCenter);
	float changeInAngle = ceta - globalOrientation;

	float deltaX = 0.0f, deltaY = 0.0f;
	if (ceta == 0.0f || abs(deltaLeft - deltaRight) < 0.01f) {
		deltaX = deltaBack; // NOTE: based on purduesigbots wiki. what means $$$$?
		deltaY = deltaRight;
	} else {
		deltaX = 2 * sinf(ceta/2.0f) * (deltaBack/ceta) + backFromCenter;
		deltaY = (deltaRight/ceta) + rightFromCenter;
	}

	float averageOrientation = globalOrientation + (ceta/2.0f);

	// calculate global offset (Vector D) rotated by -(averageOrientation).
	// this can be done by converting your existing Cartesian coords to polar coords,
	// changeing the angle, then converting back.

	// calculate new absolute position (Vector current) = (Vector before) + (Vector D)

	// update previous value for next calculation
	leftEncoderValue += currentLeft;
	rightEncoderValue += currentRight;
	backEncoderValue += currentBack;
	globalOrientation = ceta;
}

void initialize(void) {
	inertial.reset(true);

	//chassis.pid_drive_constants_forward_set(0.0f, 0.0f, 0.0f, 0.0f);
	//chassis.pid_drive_constants_backward_set(0.0f, 0.0f, 0.0f, 0.0f);
	chassis.pid_drive_constants_set(0.11f, 0.15f, 0.1f, 0.5f);
	chassis.pid_turn_constants_set(0.0f, 0.0f, 0.0f, 0.0f);
	chassis.pid_heading_constants_set(0.0f, 0.0f, 0.0f, 0.0f);

	tracking_initialize();
}

void disabled(void) {}

void competition_initialize(void) {
	std::string output = "";

	while(auto_start_point == NONE) {
		if (master.get_digital_new_press(DIGITAL_X)) {
			auto_start_point = AUTO_RED_LEFT;
			output = "RED LEFT";
		} else if (master.get_digital_new_press(DIGITAL_Y)) {
			auto_start_point = AUTO_RED_RIGHT;
			output = "RED RIGHT";
		} else if (master.get_digital_new_press(DIGITAL_A)) {
			auto_start_point = AUTO_BLUE_LEFT;
			output = "BLUE LEFT";
		} else if (master.get_digital_new_press(DIGITAL_B)) {
			auto_start_point = AUTO_BLUE_RIGHT;
			output = "BLUE RIGHT";
		}
	}
	master.print(2, 0, ("set: " + output).c_str());
	//master.print(2, 0, "set: %s", output.c_str());
}

void opcontrol(void) {
	chassis.drive_brake_set(MOTOR_BRAKE_HOLD);
	
	int intakeVal = 127;
	while(true) {
		// PID Tuner
		if (USE_PID && !pros::competition::is_connected()) {
			if (master.get_digital_new_press(DIGITAL_X)) {
				chassis.pid_tuner_toggle(); // use A/Y to increment/decrement the constants of PID
			}
			// Check current PID constants value
			auto constants = chassis.pid_drive_constants_get();
			master.print(0, 0, "P: %.2lf", constants.kp);
			master.print(1, 0, "I: %.2lf, %.2lf", constants.ki, constants.start_i);
			master.print(2, 0, "D: %.2lf", constants.kd);
			// controller will display like below (example values)
			// ------------------------------
			// |P: 0.11                     |
			// |I: 0.13, 0.01               |
			// |D: 0.05                     |
			// ------------------------------
			// use these values when initialize PID constants(in void initialize())
			chassis.pid_tuner_iterate(); // iterates through PID Tuner to allow gui naviagtion and constant 
		}

		chassis.opcontrol_arcade_standard(ez::SPLIT);
		//chassis.opcontrol_arcade_flipped(ez::SINGLE);

		// Intake motor will move while press button
		if (master.get_digital(DIGITAL_R2)) {
			intake.move(127);
		} else if (master.get_digital(DIGITAL_L2)) {
			intake.move(-127);
		} else {
			intake.move(0);
		}

		/*
		// Toggle intake motor
		if (mater.get_digital_new_press(DIGITAL_R2)) {
			intakeVal *= -1;
			intake.move(intakeVal);
		} else if (master.get_digital(DIGITAL_R1)) {
			intake.move(0);
		}
		*/

		pros::delay(ez::util::DELAY_TIME);
	}
}