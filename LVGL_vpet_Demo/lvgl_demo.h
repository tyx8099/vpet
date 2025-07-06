#ifndef LVGL_DEMO_H
#define LVGL_DEMO_H

#include "lvgl/lvgl.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Initialize the LVGL VPet demo */
void lvgl_demo_init(void);

/* Cleanup demo resources */
void lvgl_demo_cleanup(void);

#ifdef __cplusplus
}
#endif

#endif /* LVGL_DEMO_H */
