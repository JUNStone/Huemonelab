#ifndef _PROS_MAIN_H_
#define _PROS_MAIN_H_

#define PROS_USE_SIMPLE_NAMES

#define PROS_USE_LITERALS

#include "api.h"
#include "EZ-Template/api.hpp"

#ifdef __cplusplus
extern "C" {
#endif

enum AUTO_START_POINT {
	NONE = 0,
	AUTO_RED_LEFT = 1,
	AUTO_RED_RIGHT = 2,
	AUTO_BLUE_LEFT = 3,
	AUTO_BLUE_RIGHT = 4,
};

AUTO_START_POINT auto_start_point = NONE;

void autonomous(void);

void auto_red_left();
void auto_red_right();
void auto_blue_left();
void auto_blue_right();

void auto_example(void);

void initialize(void);
void disabled(void);
void competition_initialize(void);
void opcontrol(void);

#ifdef __cplusplus
}
#endif

#ifdef __cplusplus
/**
 * You can add C++-only headers here
 */
//#include <iostream>
#endif

#endif  // _PROS_MAIN_H_
