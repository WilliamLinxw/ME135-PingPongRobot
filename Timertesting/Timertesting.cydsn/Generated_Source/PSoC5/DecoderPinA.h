/*******************************************************************************
* File Name: DecoderPinA.h  
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

#if !defined(CY_PINS_DecoderPinA_H) /* Pins DecoderPinA_H */
#define CY_PINS_DecoderPinA_H

#include "cytypes.h"
#include "cyfitter.h"
#include "cypins.h"
#include "DecoderPinA_aliases.h"

/* APIs are not generated for P15[7:6] */
#if !(CY_PSOC5A &&\
	 DecoderPinA__PORT == 15 && ((DecoderPinA__MASK & 0xC0) != 0))


/***************************************
*        Function Prototypes             
***************************************/    

/**
* \addtogroup group_general
* @{
*/
void    DecoderPinA_Write(uint8 value);
void    DecoderPinA_SetDriveMode(uint8 mode);
uint8   DecoderPinA_ReadDataReg(void);
uint8   DecoderPinA_Read(void);
void    DecoderPinA_SetInterruptMode(uint16 position, uint16 mode);
uint8   DecoderPinA_ClearInterrupt(void);
/** @} general */

/***************************************
*           API Constants        
***************************************/
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup driveMode Drive mode constants
     * \brief Constants to be passed as "mode" parameter in the DecoderPinA_SetDriveMode() function.
     *  @{
     */
        #define DecoderPinA_DM_ALG_HIZ         PIN_DM_ALG_HIZ
        #define DecoderPinA_DM_DIG_HIZ         PIN_DM_DIG_HIZ
        #define DecoderPinA_DM_RES_UP          PIN_DM_RES_UP
        #define DecoderPinA_DM_RES_DWN         PIN_DM_RES_DWN
        #define DecoderPinA_DM_OD_LO           PIN_DM_OD_LO
        #define DecoderPinA_DM_OD_HI           PIN_DM_OD_HI
        #define DecoderPinA_DM_STRONG          PIN_DM_STRONG
        #define DecoderPinA_DM_RES_UPDWN       PIN_DM_RES_UPDWN
    /** @} driveMode */
/** @} group_constants */
    
/* Digital Port Constants */
#define DecoderPinA_MASK               DecoderPinA__MASK
#define DecoderPinA_SHIFT              DecoderPinA__SHIFT
#define DecoderPinA_WIDTH              1u

/* Interrupt constants */
#if defined(DecoderPinA__INTSTAT)
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup intrMode Interrupt constants
     * \brief Constants to be passed as "mode" parameter in DecoderPinA_SetInterruptMode() function.
     *  @{
     */
        #define DecoderPinA_INTR_NONE      (uint16)(0x0000u)
        #define DecoderPinA_INTR_RISING    (uint16)(0x0001u)
        #define DecoderPinA_INTR_FALLING   (uint16)(0x0002u)
        #define DecoderPinA_INTR_BOTH      (uint16)(0x0003u) 
    /** @} intrMode */
/** @} group_constants */

    #define DecoderPinA_INTR_MASK      (0x01u) 
#endif /* (DecoderPinA__INTSTAT) */


/***************************************
*             Registers        
***************************************/

/* Main Port Registers */
/* Pin State */
#define DecoderPinA_PS                     (* (reg8 *) DecoderPinA__PS)
/* Data Register */
#define DecoderPinA_DR                     (* (reg8 *) DecoderPinA__DR)
/* Port Number */
#define DecoderPinA_PRT_NUM                (* (reg8 *) DecoderPinA__PRT) 
/* Connect to Analog Globals */                                                  
#define DecoderPinA_AG                     (* (reg8 *) DecoderPinA__AG)                       
/* Analog MUX bux enable */
#define DecoderPinA_AMUX                   (* (reg8 *) DecoderPinA__AMUX) 
/* Bidirectional Enable */                                                        
#define DecoderPinA_BIE                    (* (reg8 *) DecoderPinA__BIE)
/* Bit-mask for Aliased Register Access */
#define DecoderPinA_BIT_MASK               (* (reg8 *) DecoderPinA__BIT_MASK)
/* Bypass Enable */
#define DecoderPinA_BYP                    (* (reg8 *) DecoderPinA__BYP)
/* Port wide control signals */                                                   
#define DecoderPinA_CTL                    (* (reg8 *) DecoderPinA__CTL)
/* Drive Modes */
#define DecoderPinA_DM0                    (* (reg8 *) DecoderPinA__DM0) 
#define DecoderPinA_DM1                    (* (reg8 *) DecoderPinA__DM1)
#define DecoderPinA_DM2                    (* (reg8 *) DecoderPinA__DM2) 
/* Input Buffer Disable Override */
#define DecoderPinA_INP_DIS                (* (reg8 *) DecoderPinA__INP_DIS)
/* LCD Common or Segment Drive */
#define DecoderPinA_LCD_COM_SEG            (* (reg8 *) DecoderPinA__LCD_COM_SEG)
/* Enable Segment LCD */
#define DecoderPinA_LCD_EN                 (* (reg8 *) DecoderPinA__LCD_EN)
/* Slew Rate Control */
#define DecoderPinA_SLW                    (* (reg8 *) DecoderPinA__SLW)

/* DSI Port Registers */
/* Global DSI Select Register */
#define DecoderPinA_PRTDSI__CAPS_SEL       (* (reg8 *) DecoderPinA__PRTDSI__CAPS_SEL) 
/* Double Sync Enable */
#define DecoderPinA_PRTDSI__DBL_SYNC_IN    (* (reg8 *) DecoderPinA__PRTDSI__DBL_SYNC_IN) 
/* Output Enable Select Drive Strength */
#define DecoderPinA_PRTDSI__OE_SEL0        (* (reg8 *) DecoderPinA__PRTDSI__OE_SEL0) 
#define DecoderPinA_PRTDSI__OE_SEL1        (* (reg8 *) DecoderPinA__PRTDSI__OE_SEL1) 
/* Port Pin Output Select Registers */
#define DecoderPinA_PRTDSI__OUT_SEL0       (* (reg8 *) DecoderPinA__PRTDSI__OUT_SEL0) 
#define DecoderPinA_PRTDSI__OUT_SEL1       (* (reg8 *) DecoderPinA__PRTDSI__OUT_SEL1) 
/* Sync Output Enable Registers */
#define DecoderPinA_PRTDSI__SYNC_OUT       (* (reg8 *) DecoderPinA__PRTDSI__SYNC_OUT) 

/* SIO registers */
#if defined(DecoderPinA__SIO_CFG)
    #define DecoderPinA_SIO_HYST_EN        (* (reg8 *) DecoderPinA__SIO_HYST_EN)
    #define DecoderPinA_SIO_REG_HIFREQ     (* (reg8 *) DecoderPinA__SIO_REG_HIFREQ)
    #define DecoderPinA_SIO_CFG            (* (reg8 *) DecoderPinA__SIO_CFG)
    #define DecoderPinA_SIO_DIFF           (* (reg8 *) DecoderPinA__SIO_DIFF)
#endif /* (DecoderPinA__SIO_CFG) */

/* Interrupt Registers */
#if defined(DecoderPinA__INTSTAT)
    #define DecoderPinA_INTSTAT            (* (reg8 *) DecoderPinA__INTSTAT)
    #define DecoderPinA_SNAP               (* (reg8 *) DecoderPinA__SNAP)
    
	#define DecoderPinA_0_INTTYPE_REG 		(* (reg8 *) DecoderPinA__0__INTTYPE)
#endif /* (DecoderPinA__INTSTAT) */

#endif /* CY_PSOC5A... */

#endif /*  CY_PINS_DecoderPinA_H */


/* [] END OF FILE */
