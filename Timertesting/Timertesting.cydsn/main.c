/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/
#include "project.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

// Parameters for motor 1
signed short int cnt1 = 0;
signed short int target1 = 0;
int error1 = 0;
int last_error1 = 0;
int derivative1 = 0;
int integral1 = 0;
int duty_cycle1 = 0;
char transmitbuffer1[2]; // transmit buffer taken out for testing purposes
char stopbyte1 = 'x';

// Parameters for motor 2
signed short int cnt2 = 0;
signed short int target2 = 0;
int error2 = 0;
int last_error2 = 0;
int derivative2 = 0;
int integral2 = 0;
int duty_cycle2 = 0;
char transmitbuffer2[2]; // transmit buffer taken out for testing purposes
int transmit2 = 0;
char stopbyte2 = 'y';

// Parameter for both
char new_get;
char new_target[16];
char concatination[2];
uint8 counts[8];
uint8 multitasking = 1;
int transmit = 0;

// The following function is a non-general implementation of 
// finding out how long the sending array is.
// Needed near the duty cycle calculaion
int bytesCharArrayNeeds(int dutyCycle) {
    int arrSize = 1;
    if (dutyCycle >= 10) {
      arrSize += 1;
    }
    if (dutyCycle >= 100) {
      arrSize += 1;
    }
    if (dutyCycle >= 1000) {
      arrSize += 1;
    }
    if (dutyCycle >= 10000) {
      arrSize += 1;
    }
  return arrSize;
}

// only works for a two byte integer, no nothing larger than 16000-ish
uint8 firstByte(short int number) {
    return (number & 0xFF00) >> 8;
}

uint8 forthByte(short int number) {
    return 0x00FF & number;
}

signed short int combineBytes(uint8 firstByte, uint8 secondByte) {
  return ((firstByte << 8) & 0xFF00) | (0x00FF & secondByte);
}


// PID Control for both motors
CY_ISR(MotorControl) {
    /*
        The code below is for contorl of motor1
    */
    
    // Get the current position
    cnt1 = QuadDec_1_GetCounter();
    //sprintf(transmitbuffer1,"Count1: %d \r\n",cnt1);
    //UART_PutString(transmitbuffer1);
    
    // Calculate the error
    error1 = target1 - cnt1;

    //Calculate the integral
    integral1 = integral1 + error1;
    
    // Calculate the Derivative
    derivative1 = error1 - last_error1;

    //Calculate the control variable
    duty_cycle1 = 100 * error1 + 0 * integral1 + 50 * derivative1;
    
    
    // Limit the control variable within 100
    if (duty_cycle1 > 32000){duty_cycle1 = 32000;}
    else if (duty_cycle1 < -32000){duty_cycle1 = -32000;}
    
    //Limit the dead zone
    if (duty_cycle1 < 50 && duty_cycle1 > -50){
        PWM_1_WriteCompare(0);
    }
    
    // If the control variable is positive, run the motor clockwise
    if (duty_cycle1 > 0){
        Direction_1_1_Write(0);
        Direction_1_2_Write(1);
        PWM_1_WriteCompare(duty_cycle1);
    }
    
    // If the control variable is negative, run the motor counterclockwise
    else if (duty_cycle1 < 0){
        Direction_1_1_Write(1);
        Direction_1_2_Write(0);
        PWM_1_WriteCompare(-1*duty_cycle1);
    }
    
    // If the control variable is zero, stop the motor
    else{
        Direction_1_1_Write(0);
        Direction_1_2_Write(0);
    }
    last_error1 = error1;
    
    /*
        The code below is for control of motor 2
    */
    
    // Get the current position
    cnt2 = QuadDec_2_GetCounter();
    //sprintf(transmitbuffer2,"Count2: %d \r\n",cnt2);
    //UART_PutString(transmitbuffer2);
    
    // Calculate the error
    error2 = target2 - cnt2;


    //Calculate the integral
    integral2 = integral2 + error2;
    
    // Calculate the Derivative
    derivative2 = error2 - last_error2;

    //Calculate the control variable
    duty_cycle2 = 100 * error2 + 0 * integral2 + 50 * derivative2;
    
    
    // Limit the control variable within 100
    if (duty_cycle2 > 32000){duty_cycle2 = 32000;}
    else if (duty_cycle2 < -32000){duty_cycle2 = -32000;}
    
    //Limit the dead zone
    if (duty_cycle2 < 50 && duty_cycle2 > -50){
        PWM_2_WriteCompare(0);
    }
    
    // If the control variable is positive, run the motor clockwise
    if (duty_cycle2 > 0){
        Direction_2_1_Write(0);
        Direction_2_2_Write(1);
        PWM_2_WriteCompare(duty_cycle2);
    }
    
    // If the control variable is negative, run the motor counterclockwise
    else if (duty_cycle2 < 0){
        Direction_2_1_Write(1);
        Direction_2_2_Write(0);
        PWM_2_WriteCompare(-1*duty_cycle2);
    }
    
    // If the control variable is zero, stop the motor
    else{
        Direction_2_1_Write(0);
        Direction_2_2_Write(0);
    }
    last_error2 = error2;
    
    // Scheduling for storing data into a 6 bytes array
    multitasking += 1;
    if (multitasking % 32 == 0) {
        if (transmit == 0){
            counts[0] = 0x00;
            counts[1] = 0x00;
            counts[2] = firstByte(cnt1);
            counts[3] = forthByte(cnt1);
            counts[4] = firstByte(cnt2);
            counts[5] = forthByte(cnt2);
            counts[6] = 0x00;
            counts[7] = 0x00;
            transmit = 1;
        }
    }

}

// Logic of getting new target position, implemented in UART_Rx_Interrupt
CY_ISR(Targetchanging){
    
    // Once receive a new byte, start building a new target position
    new_get = UART_GetChar();
    
    // If the new byte is the stopbyte of target1, assign target1 with the new_target string
    if (new_get == stopbyte1){
        target1 = atoi(new_target);
        new_target[0] = '\0';
        concatination[0] = '\0';
        UART_ClearRxBuffer();
    }
    // If the new byte is the stopbyte of target2, assign target2 with the new_target string
    else if (new_get == stopbyte2){
        target2 = atoi(new_target);
        new_target[0] = '\0';
        concatination[0] = '\0';
        UART_ClearRxBuffer();
    }
    // If the new byte is not the stopbyte of anyone, concatinate the new byte to the new_target string
    else {
        concatination[0] = new_get;
        concatination[1] = '\0';
        char* concat = concatination;
        strcat(new_target, concat);
    }
}

int main(void)
{
    /* Place your initialization/startup code here (e.g. MyInst_Start()) */
    PWM_1_Start();
    QuadDec_1_Start();
    QuadDec_1_SetCounter(0);
    PWM_2_Start();
    QuadDec_2_Start();
    QuadDec_2_SetCounter(0);
    UART_Start();
    Timer_Start(); // Configure and enable timer
    isr_motor_Start(); // Start the timer interrupt
    isr_motor_StartEx(MotorControl); // Point to MY_ISR_1 to carry out the interrupt sub-routine of PID control
    isr_1_Start(); // Start the control variable changing interrupt
    isr_1_StartEx(Targetchanging); // Point to MY_ISR_2 to carry out the interrupt sub-routine of changing target postiion
    CyGlobalIntEnable; /* Enable global interrupts. */

    for(;;)
    {
        
        /* Place your application code here. */
        
        // Background routine for sending data back to laptop, 32 times slower than the PID routine
        if (transmit == 1){
            uint8* p = counts;
            UART_PutArray(p, sizeof(counts));
            transmit = 0;
        }
    }   
}


/* [] END OF FILE */
