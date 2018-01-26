/**************************************
 * @file:mb_hardware.c
 * @brief:Fuctions related to the hardware layer.
 * ***********************************/

#include "mb_hardware.h"
#include "stm32f10x.h"
#include "stm32f10x_conf.h"
#include "hard_init.h"
#include "moore.h"
#include <stdio.h>


/****************************************
 * @fn:KeyboardGPIO_Config
 * @brief:initialize the keyboard pin map
 * @keymap:
 *   0 1 2
 *   - - -
 * 3|1 2 3
 * 4|4 5 6
 * 5|7 8 9
 * 6|s 0 g
 *
 * s--store  g--get
 ****************************************/
static void KeyboardGPIO_Config(void)
{
  GPIO_InitTypeDef GPIO_InitStructure;

  RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);

  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0|GPIO_Pin_1|GPIO_Pin_2;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_Init(GPIOC, &GPIO_InitStructure);

  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3|GPIO_Pin_4|GPIO_Pin_5|GPIO_Pin_6;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPD;
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_Init(GPIOC, &GPIO_InitStructure);

  GPIO_SetBits(GPIOC, GPIO_Pin_0|GPIO_Pin_1|GPIO_Pin_2);
  GPIO_ResetBits(GPIOC, GPIO_Pin_3|GPIO_Pin_4|GPIO_Pin_5|GPIO_Pin_6);
}

/***************************************
 * @fn:KeyboardDetect
 * @brief:Scan the keyboard and get the key value
 * ************************************/
int KeyboardDetect(void)
{
  int KeyValue=0xFF;
  KeyboardGPIO_Config();
  //dbg_printf("%02X\r\n",(GPIO_ReadInputData(GPIOC)&0x78));
  if((GPIO_ReadInputData(GPIOC)&0x78) != 0x00){
    delay_ms(10);
    if((GPIO_ReadInputData(GPIOC)&0x78) != 0x00){
      //	dbg_printf("key pressed!!!\r\n");
      GPIO_SetBits(GPIOC, GPIO_Pin_0);
      GPIO_ResetBits(GPIOC, GPIO_Pin_1|GPIO_Pin_2);
      //	dbg_printf("touch%02X\r\n",(GPIO_ReadInputData(GPIOC)&0x78));
      switch(GPIO_ReadInputData(GPIOC)&0x78)
      {
        case 0x08: KeyValue = 1; break;
        case 0x10: KeyValue = 4; break;
        case 0x20: KeyValue = 7; break;
        case 0x40: KeyValue = 's'; break;
                   //default: KeyValue = 0xFF; break;
      }

      GPIO_SetBits(GPIOC, GPIO_Pin_1);
      GPIO_ResetBits(GPIOC, GPIO_Pin_0|GPIO_Pin_2);
      //	dbg_printf("touch%02X\r\n",(GPIO_ReadInputData(GPIOC)&0x78));
      switch(GPIO_ReadInputData(GPIOC)&0x78)
      {
        case 0x08: KeyValue = 2; break;
        case 0x10: KeyValue = 5; break;
        case 0x20: KeyValue = 8; break;
        case 0x40: KeyValue = 0; break;
                   //default: KeyValue = 0xFF; break;
      }

      GPIO_SetBits(GPIOC, GPIO_Pin_2);
      GPIO_ResetBits(GPIOC, GPIO_Pin_0|GPIO_Pin_1);
      //	dbg_printf("touch%02X\r\n",(GPIO_ReadInputData(GPIOC)&0x78));
      switch(GPIO_ReadInputData(GPIOC)&0x78)
      {
        case 0x08: KeyValue = 3; break;
        case 0x10: KeyValue = 6; break;
        case 0x20: KeyValue = 9; break;
        case 0x40: KeyValue = 'g'; break;
                   //default: KeyValue = 0xFF; break;
      }

      GPIO_SetBits(GPIOC, GPIO_Pin_0|GPIO_Pin_1|GPIO_Pin_2);
      GPIO_ResetBits(GPIOC, GPIO_Pin_3|GPIO_Pin_4|GPIO_Pin_5|GPIO_Pin_6);
      while((GPIO_ReadInputData(GPIOC)&0x78) != 0x00);
      //return KeyValue;
    }
  }


  return KeyValue;
}

/******************************************
 * @fn platform_set_online
 * @brief
 * ***************************************/

void platform_set_online(bool online)
{}
