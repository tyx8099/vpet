#include "lvgl_demo.h"
#include "sprite_data.h"
#include <stdio.h>

/* Global variables */
static lv_obj_t* screen_main;
static lv_obj_t* img_digimon;
static lv_obj_t* label_status;
static lv_obj_t* label_fps;
static lv_timer_t* animation_timer;

/* Animation state */
static int current_frame = 0;
static bool animation_playing = true;
static uint32_t last_frame_time = 0;

/* Demo configuration */
#define FRAME_DELAY_MS 100  // 10 FPS like the main game
#define SCREEN_WIDTH 320
#define SCREEN_HEIGHT 240

/* Animation timer callback */
static void animation_timer_cb(lv_timer_t* timer) {
    LV_UNUSED(timer);
    
    if (!animation_playing) return;
    
    uint32_t current_time = lv_tick_get();
    if (current_time - last_frame_time >= FRAME_DELAY_MS) {
        // Update animation frame
        current_frame = (current_frame + 1) % AGUMON_FRAME_COUNT;
        lv_img_set_src(img_digimon, agumon_frames[current_frame]);
        
        last_frame_time = current_time;
        
        // Update status
        static char status_buf[64];
        snprintf(status_buf, sizeof(status_buf), "Frame: %d/%d", 
                current_frame + 1, AGUMON_FRAME_COUNT);
        lv_label_set_text(label_status, status_buf);
    }
    
    // Update FPS counter
    static uint32_t fps_last_time = 0;
    static int fps_counter = 0;
    static char fps_buf[32];
    
    fps_counter++;
    if (current_time - fps_last_time >= 1000) { // Update every second
        snprintf(fps_buf, sizeof(fps_buf), "FPS: %d", fps_counter);
        lv_label_set_text(label_fps, fps_buf);
        fps_counter = 0;
        fps_last_time = current_time;
    }
}

/* Button event handlers */
static void btn_play_pause_cb(lv_event_t* e) {
    LV_UNUSED(e);
    animation_playing = !animation_playing;
    
    lv_obj_t* btn = lv_event_get_target(e);
    lv_obj_t* label = lv_obj_get_child(btn, 0);
    lv_label_set_text(label, animation_playing ? "Pause" : "Play");
}

static void btn_reset_cb(lv_event_t* e) {
    LV_UNUSED(e);
    current_frame = 0;
    lv_img_set_src(img_digimon, agumon_frames[current_frame]);
}

static void btn_next_frame_cb(lv_event_t* e) {
    LV_UNUSED(e);
    animation_playing = false;
    current_frame = (current_frame + 1) % AGUMON_FRAME_COUNT;
    lv_img_set_src(img_digimon, agumon_frames[current_frame]);
    
    // Update play/pause button
    lv_obj_t* play_btn = lv_obj_get_child(lv_scr_act(), 3); // Assuming button order
    lv_obj_t* label = lv_obj_get_child(play_btn, 0);
    lv_label_set_text(label, "Play");
}

/* Create UI elements */
static void create_ui() {
    /* Create main screen */
    screen_main = lv_obj_create(NULL);
    lv_scr_load(screen_main);
    
    /* Set background color to dark blue */
    lv_obj_set_style_bg_color(screen_main, lv_color_hex(0x001122), 0);
    
    /* Create title label */
    lv_obj_t* label_title = lv_label_create(screen_main);
    lv_label_set_text(label_title, "LVGL VPet Demo - Agumon");
    lv_obj_set_style_text_color(label_title, lv_color_white(), 0);
    lv_obj_align(label_title, LV_ALIGN_TOP_MID, 0, 10);
    
    /* Create Digimon sprite image */
    img_digimon = lv_img_create(screen_main);
    lv_img_set_src(img_digimon, agumon_frames[0]);
    lv_obj_align(img_digimon, LV_ALIGN_CENTER, 0, -20);
    
    /* Create status label */
    label_status = lv_label_create(screen_main);
    lv_label_set_text(label_status, "Frame: 1/15");
    lv_obj_set_style_text_color(label_status, lv_color_white(), 0);
    lv_obj_align_to(label_status, img_digimon, LV_ALIGN_OUT_BOTTOM_MID, 0, 10);
    
    /* Create FPS label */
    label_fps = lv_label_create(screen_main);
    lv_label_set_text(label_fps, "FPS: --");
    lv_obj_set_style_text_color(label_fps, lv_color_yellow(), 0);
    lv_obj_align(label_fps, LV_ALIGN_TOP_RIGHT, -10, 10);
    
    /* Create control buttons */
    lv_obj_t* btn_play_pause = lv_btn_create(screen_main);
    lv_obj_set_size(btn_play_pause, 80, 30);
    lv_obj_align(btn_play_pause, LV_ALIGN_BOTTOM_LEFT, 10, -10);
    lv_obj_add_event_cb(btn_play_pause, btn_play_pause_cb, LV_EVENT_CLICKED, NULL);
    
    lv_obj_t* label_play = lv_label_create(btn_play_pause);
    lv_label_set_text(label_play, "Pause");
    lv_obj_center(label_play);
    
    lv_obj_t* btn_reset = lv_btn_create(screen_main);
    lv_obj_set_size(btn_reset, 80, 30);
    lv_obj_align(btn_reset, LV_ALIGN_BOTTOM_MID, 0, -10);
    lv_obj_add_event_cb(btn_reset, btn_reset_cb, LV_EVENT_CLICKED, NULL);
    
    lv_obj_t* label_reset = lv_label_create(btn_reset);
    lv_label_set_text(label_reset, "Reset");
    lv_obj_center(label_reset);
    
    lv_obj_t* btn_next = lv_btn_create(screen_main);
    lv_obj_set_size(btn_next, 80, 30);
    lv_obj_align(btn_next, LV_ALIGN_BOTTOM_RIGHT, -10, -10);
    lv_obj_add_event_cb(btn_next, btn_next_frame_cb, LV_EVENT_CLICKED, NULL);
    
    lv_obj_t* label_next = lv_label_create(btn_next);
    lv_label_set_text(label_next, "Next");
    lv_obj_center(label_next);
    
    /* Create info panel */
    lv_obj_t* panel_info = lv_obj_create(screen_main);
    lv_obj_set_size(panel_info, 200, 60);
    lv_obj_align(panel_info, LV_ALIGN_TOP_LEFT, 10, 40);
    lv_obj_set_style_bg_color(panel_info, lv_color_hex(0x333333), 0);
    lv_obj_set_style_border_width(panel_info, 1, 0);
    lv_obj_set_style_border_color(panel_info, lv_color_white(), 0);
    
    lv_obj_t* label_info = lv_label_create(panel_info);
    lv_label_set_text(label_info, 
        "Size: 48x48px\\n"
        "Frames: 15\\n"
        "Format: RGBA8888");
    lv_obj_set_style_text_color(label_info, lv_color_white(), 0);
    lv_obj_set_style_text_font(label_info, &lv_font_montserrat_12, 0);
    lv_obj_align(label_info, LV_ALIGN_TOP_LEFT, 5, 5);
}

/* Initialize the demo */
void lvgl_demo_init() {
    printf("Initializing LVGL VPet Demo...\\n");
    printf("Agumon sprites: %d frames, %dx%d pixels\\n", 
           AGUMON_FRAME_COUNT, AGUMON_WIDTH, AGUMON_HEIGHT);
    
    /* Create UI */
    create_ui();
    
    /* Start animation timer */
    animation_timer = lv_timer_create(animation_timer_cb, 16, NULL); // ~60Hz update rate
    last_frame_time = lv_tick_get();
    
    printf("Demo initialized successfully!\\n");
}

/* Cleanup demo */
void lvgl_demo_cleanup() {
    if (animation_timer) {
        lv_timer_del(animation_timer);
        animation_timer = NULL;
    }
    printf("Demo cleanup completed.\\n");
}
