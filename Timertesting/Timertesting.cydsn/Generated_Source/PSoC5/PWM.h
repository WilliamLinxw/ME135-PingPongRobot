/*******************************************************************************
* File Name: PWM.h  
* Version 2.20
*
* Description:
*  This file contains Pin function prototypes and register defines
*
* Note:
*
********************************************************************************
* Copyright 2008-2015, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#if !defined(CY_PINS_PWM_H) /* Pins PWM_H */
#define CY_PINS_PWM_H

#include "cytypes.h"
#include "cyfitter.h"
#include "cypins.h"
#include "PWM_aliases.h"

/* APIs are not generated for P15[7:6] */
#if !(CY_PSOC5A &&\
	 PWM__PORT == 15 && ((PWM__MASK & 0xC0) != 0))


/***************************************
*        Function Prototypes             
***************************************/    

/**
* \addtogroup group_general
* @{
*/
void    PWM_Write(uint8 value);
void    PWM_SetDriveMode(uint8 mode);
uint8   PWM_ReadDataReg(void);
uint8   PWM_Read(void);
void    PWM_SetInterruptMode(uint16 position, uint16 mode);
uint8   PWM_ClearInterrupt(void);
/** @} general */

/***************************************
*           API Constants        
***************************************/
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup driveMode Drive mode constants
     * \brief Constants to be passed as "mode" parameter in the PWM_SetDriveMode() function.
     *  @{
     */
        #define PWM_DM_ALG_HIZ         PIN_DM_ALG_HIZ
        #define PWM_DM_DIG_HIZ         PIN_DM_DIG_HIZ
        #define PWM_DM_RES_UP          PIN_DM_RES_UP
        #define PWM_DM_RES_DWN         PIN_DM_RES_DWN
        #define PWM_DM_OD_LO           PIN_DM_OD_LO
        #define PWM_DM_OD_HI           PIN_DM_OD_HI
        #define PWM_DM_STRONG          PIN_DM_STRONG
        #define PWM_DM_RES_UPDWN       PIN_DM_RES_UPDWN
    /** @} driveMode */
/** @} group_constants */
    
/* Digital Port Constants */
#define PWM_MASK               PWM__MASK
#define PWM_SHIFT              PWM__SHIFT
#define PWM_WIDTH              1u

/* Interrupt constants */
#if defined(PWM__INTSTAT)
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup intrMode Interrupt constants
     * \brief Constants to be passed as "mode" parameter in PWM_SetInterruptMode() function.
     *  @{
     */
        #define PWM_INTR_NONE      (uint16)(0x0000u)
        #define PWM_INTR_RISING    (uint16)(0x0001u)
        #define PWM_INTR_FALLING   (uint16)(0x0002u)
        #define PWM_INTR_BOTH      (uint16)(0x0003u) 
    /** @} intrMode */
/** @} group_constants */

    #define PWM_INTR_MASK      (0x01u) 
#endif /* (PWM__INTSTAT) */


/***************************************
*             Registers        
***************************************/

/* Main Port Registers */
/* Pin State */
#define PWM_PS                     (* (reg8 *) PWM__PS)
/* Data Register */
#define PWM_DR                     (* (reg8 *) PWM__DR)
/* Port Number */
#define PWM_PRT_NUM                (* (reg8 *) PWM__PRT) 
/* Connect to Analog Globals */                                                  
#define PWM_AG                     (* (reg8 *) PWM__AG)                       
/* Analog MUX bux enable */
#define PWM_AMUX                   (* (reg8 *) PWM__AMUX) 
/* Bidirectional Enable */                                                        
#define PWM_BIE                    (* (reg8 *) PWM__BIE)
/* Bit-mask for Aliased Register Access */
#define PWM_BIT_MASK               (* (reg8 *) PWM__BIT_MASK)
/* Bypass Enable */
#define PWM_BYP                    (* (reg8 *) PWM__BYP)
/* Port wide control signals */                                                   
#define PWM_CTL                    (* (reg8 *) PWM__CTL)
/* Drive Modes */
#define PWM_DM0                    (* (reg8 *) PWM__DM0) 
#define PWM_DM1                    (* (reg8 *) PWM__DM1)
#define PWM_DM2                    (* (reg8 *) PWM__DM2) 
/* Input Buffer Disable Override */
#define PWM_INP_DIS                (* (reg8 *) PWM__INP_DIS)
/* LCD Common or Segment Drive */
#define PWM_LCD_COM_SEG            (* (reg8 *) PWM__LCD_COM_SEG)
/* Enable Segment LCD */
#define PWM_LCD_EN                 (* (reg8 *) PWM__LCD_EN)
/* Slew Rate Control */
#define PWM_SLW                    (* (reg8 *) PWM__SLW)

/* DSI Port Registers */
/* Global DSI Select Register */
#define PWM_PRTDSI__CAPS_SEL       (* (reg8 *) PWM__PRTDSI__CAPS_SEL) 
/* Double Sync Enable */
#define PWM_PRTDSI__DBL_SYNC_IN    (* (reg8 *) PWM__PRTDSI__DBL_SYNC_IN) 
/* Output Enable Select Drive Strength */
#define PWM_PRTDSI__OE_SEL0        (* (reg8 *) PWM__PRTDSI__OE_SEL0) 
#define PWM_PRTDSI__OE_SEL1        (* (reg8 *) PWM__PRTDSI__OE_SEL1) 
/* Port Pin Output Select Registers */
#define PWM_PRTDSI__OUT_SEL0       (* (reg8 *) PWM__PRTDSI__OUT_SEL0) 
#define PWM_PRTDSI__OUT_SEL1       (* (reg8 *) PWM__PRTDSI__OUT_SEL1) 
/* Sync Output Enable Registers */
#define PWM_PRTDSI__SYNC_OUT       (* (reg8 *) PWM__PRTDSI__SYNC_OUT) 

/* SIO registers */
#if defined(PWM__SIO_CFG)
    #define PWM_SIO_HYST_EN        (* (reg8 *) PWM__SIO_HYST_EN)
    #define PWM_SIO_REG_HIFREQ     (* (reg8 *) PWM__SIO_REG_HIFREQ)
    #define PWM_SIO_CFG            (* (reg8 *) PWM__SIO_CFG)
    #define PWM_SIO_DIFF           (* (reg8 *) PWM__SIO_DIFF)
#endif /* (PWM__SIO_CFG) */

/* Interrupt Registers */
#if defined(PWM__INTSTAT)
    #define PWM_INTSTAT            (* (reg8 *) PWM__INTSTAT)
    #define PWM_SNAP               (* (reg8 *) PWM__SNAP)
    
	#define PWM_0_INTTYPE_REG 		(* (reg8 *) PWM__0__INTTYPE)
#endif /* (PWM__INTSTAT) */

#endif /* CY_PSOC5A... */

#endif /*  CY_PINS_PWM_H */


/* [] END OF FILE */
