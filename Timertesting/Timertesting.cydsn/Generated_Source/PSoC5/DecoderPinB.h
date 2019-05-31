/*******************************************************************************
* File Name: DecoderPinB.h  
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

#if !defined(CY_PINS_DecoderPinB_H) /* Pins DecoderPinB_H */
#define CY_PINS_DecoderPinB_H

#include "cytypes.h"
#include "cyfitter.h"
#include "cypins.h"
#include "DecoderPinB_aliases.h"

/* APIs are not generated for P15[7:6] */
#if !(CY_PSOC5A &&\
	 DecoderPinB__PORT == 15 && ((DecoderPinB__MASK & 0xC0) != 0))


/***************************************
*        Function Prototypes             
***************************************/    

/**
* \addtogroup group_general
* @{
*/
void    DecoderPinB_Write(uint8 value);
void    DecoderPinB_SetDriveMode(uint8 mode);
uint8   DecoderPinB_ReadDataReg(void);
uint8   DecoderPinB_Read(void);
void    DecoderPinB_SetInterruptMode(uint16 position, uint16 mode);
uint8   DecoderPinB_ClearInterrupt(void);
/** @} general */

/***************************************
*           API Constants        
***************************************/
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup driveMode Drive mode constants
     * \brief Constants to be passed as "mode" parameter in the DecoderPinB_SetDriveMode() function.
     *  @{
     */
        #define DecoderPinB_DM_ALG_HIZ         PIN_DM_ALG_HIZ
        #define DecoderPinB_DM_DIG_HIZ         PIN_DM_DIG_HIZ
        #define DecoderPinB_DM_RES_UP          PIN_DM_RES_UP
        #define DecoderPinB_DM_RES_DWN         PIN_DM_RES_DWN
        #define DecoderPinB_DM_OD_LO           PIN_DM_OD_LO
        #define DecoderPinB_DM_OD_HI           PIN_DM_OD_HI
        #define DecoderPinB_DM_STRONG          PIN_DM_STRONG
        #define DecoderPinB_DM_RES_UPDWN       PIN_DM_RES_UPDWN
    /** @} driveMode */
/** @} group_constants */
    
/* Digital Port Constants */
#define DecoderPinB_MASK               DecoderPinB__MASK
#define DecoderPinB_SHIFT              DecoderPinB__SHIFT
#define DecoderPinB_WIDTH              1u

/* Interrupt constants */
#if defined(DecoderPinB__INTSTAT)
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup intrMode Interrupt constants
     * \brief Constants to be passed as "mode" parameter in DecoderPinB_SetInterruptMode() function.
     *  @{
     */
        #define DecoderPinB_INTR_NONE      (uint16)(0x0000u)
        #define DecoderPinB_INTR_RISING    (uint16)(0x0001u)
        #define DecoderPinB_INTR_FALLING   (uint16)(0x0002u)
        #define DecoderPinB_INTR_BOTH      (uint16)(0x0003u) 
    /** @} intrMode */
/** @} group_constants */

    #define DecoderPinB_INTR_MASK      (0x01u) 
#endif /* (DecoderPinB__INTSTAT) */


/***************************************
*             Registers        
***************************************/

/* Main Port Registers */
/* Pin State */
#define DecoderPinB_PS                     (* (reg8 *) DecoderPinB__PS)
/* Data Register */
#define DecoderPinB_DR                     (* (reg8 *) DecoderPinB__DR)
/* Port Number */
#define DecoderPinB_PRT_NUM                (* (reg8 *) DecoderPinB__PRT) 
/* Connect to Analog Globals */                                                  
#define DecoderPinB_AG                     (* (reg8 *) DecoderPinB__AG)                       
/* Analog MUX bux enable */
#define DecoderPinB_AMUX                   (* (reg8 *) DecoderPinB__AMUX) 
/* Bidirectional Enable */                                                        
#define DecoderPinB_BIE                    (* (reg8 *) DecoderPinB__BIE)
/* Bit-mask for Aliased Register Access */
#define DecoderPinB_BIT_MASK               (* (reg8 *) DecoderPinB__BIT_MASK)
/* Bypass Enable */
#define DecoderPinB_BYP                    (* (reg8 *) DecoderPinB__BYP)
/* Port wide control signals */                                                   
#define DecoderPinB_CTL                    (* (reg8 *) DecoderPinB__CTL)
/* Drive Modes */
#define DecoderPinB_DM0                    (* (reg8 *) DecoderPinB__DM0) 
#define DecoderPinB_DM1                    (* (reg8 *) DecoderPinB__DM1)
#define DecoderPinB_DM2                    (* (reg8 *) DecoderPinB__DM2) 
/* Input Buffer Disable Override */
#define DecoderPinB_INP_DIS                (* (reg8 *) DecoderPinB__INP_DIS)
/* LCD Common or Segment Drive */
#define DecoderPinB_LCD_COM_SEG            (* (reg8 *) DecoderPinB__LCD_COM_SEG)
/* Enable Segment LCD */
#define DecoderPinB_LCD_EN                 (* (reg8 *) DecoderPinB__LCD_EN)
/* Slew Rate Control */
#define DecoderPinB_SLW                    (* (reg8 *) DecoderPinB__SLW)

/* DSI Port Registers */
/* Global DSI Select Register */
#define DecoderPinB_PRTDSI__CAPS_SEL       (* (reg8 *) DecoderPinB__PRTDSI__CAPS_SEL) 
/* Double Sync Enable */
#define DecoderPinB_PRTDSI__DBL_SYNC_IN    (* (reg8 *) DecoderPinB__PRTDSI__DBL_SYNC_IN) 
/* Output Enable Select Drive Strength */
#define DecoderPinB_PRTDSI__OE_SEL0        (* (reg8 *) DecoderPinB__PRTDSI__OE_SEL0) 
#define DecoderPinB_PRTDSI__OE_SEL1        (* (reg8 *) DecoderPinB__PRTDSI__OE_SEL1) 
/* Port Pin Output Select Registers */
#define DecoderPinB_PRTDSI__OUT_SEL0       (* (reg8 *) DecoderPinB__PRTDSI__OUT_SEL0) 
#define DecoderPinB_PRTDSI__OUT_SEL1       (* (reg8 *) DecoderPinB__PRTDSI__OUT_SEL1) 
/* Sync Output Enable Registers */
#define DecoderPinB_PRTDSI__SYNC_OUT       (* (reg8 *) DecoderPinB__PRTDSI__SYNC_OUT) 

/* SIO registers */
#if defined(DecoderPinB__SIO_CFG)
    #define DecoderPinB_SIO_HYST_EN        (* (reg8 *) DecoderPinB__SIO_HYST_EN)
    #define DecoderPinB_SIO_REG_HIFREQ     (* (reg8 *) DecoderPinB__SIO_REG_HIFREQ)
    #define DecoderPinB_SIO_CFG            (* (reg8 *) DecoderPinB__SIO_CFG)
    #define DecoderPinB_SIO_DIFF           (* (reg8 *) DecoderPinB__SIO_DIFF)
#endif /* (DecoderPinB__SIO_CFG) */

/* Interrupt Registers */
#if defined(DecoderPinB__INTSTAT)
    #define DecoderPinB_INTSTAT            (* (reg8 *) DecoderPinB__INTSTAT)
    #define DecoderPinB_SNAP               (* (reg8 *) DecoderPinB__SNAP)
    
	#define DecoderPinB_0_INTTYPE_REG 		(* (reg8 *) DecoderPinB__0__INTTYPE)
#endif /* (DecoderPinB__INTSTAT) */

#endif /* CY_PSOC5A... */

#endif /*  CY_PINS_DecoderPinB_H */


/* [] END OF FILE */
