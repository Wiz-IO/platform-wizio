/* Adafruit GFX compatible renderer with gtk backend */
#ifndef _GTK_GFX_H
#define _GTK_GFX_H

#include <Adafruit_GFX.h>

#undef min(a,b)
#undef max(a,b)

#include <gtk/gtk.h>
#include <iostream>

// color definitions for GxEPD, GxEPD2 and GxEPD_HD, values correspond to RGB565 values for TFTs
#define GxEPD_BLACK     0x0000
#define GxEPD_WHITE     0xFFFF
// some controllers for b/w EPDs support grey levels
#define GxEPD_DARKGREY  0x7BEF // 128, 128, 128
#define GxEPD_LIGHTGREY 0xC618 // 192, 192, 192
// values for 3-color or 7-color EPDs
#define GxEPD_RED       0xF800 // 255,   0,   0
#define GxEPD_YELLOW    0xFFE0 // 255, 255,   0 !!no longer same as GxEPD_RED!!
#define GxEPD_COLORED   GxEPD_RED
// values for 7-color EPDs only
#define GxEPD_BLUE      0x001F //   0,   0, 255
#define GxEPD_GREEN     0x07E0 //   0, 255,   0
#define GxEPD_ORANGE    0xFD20 // 255, 165,   0

#if CORE_DEBUG_LEVEL >= 4
#define GTK_GFX_DEBUG(str) do {std::cout << str << std::endl; } while (false)
#else
#define GTK_GFX_DEBUG(str) do { } while (false)
#endif

class GTK_GFX : public Adafruit_GFX {
    using Adafruit_GFX::Adafruit_GFX;
    public:
        GTK_GFX(uint16_t width, uint16_t height, uint16_t scale=2, bool color=false);
        ~GTK_GFX(void);
        void drawPixel(int16_t x, int16_t y, uint16_t color);
        void powerOff() { GTK_GFX_DEBUG("GTK_GFX::powerOff()"); };
        void hibernate() { GTK_GFX_DEBUG("GTK_GFX::hibernate()"); }
        void display(bool state=false) { sleep(0); };
        void displayWindow(uint16_t x, uint16_t y, uint16_t w, uint16_t h) {
            GTK_GFX_DEBUG("GTK_GFX::displayWindow(" << x << ", " << y << ", " << w << ", " << h << ")");
        };
        void setPartialWindow(uint16_t x, uint16_t y, uint16_t w, uint16_t h) {
            GTK_GFX_DEBUG("GTK_GFX::setPartialWindow(" << x << ", "<< y << ", " << w << ", " << h << ")");
        }
        void setFullWindow() { setPartialWindow(0, 0, width(), height()); };
        bool sleep(unsigned int millis);

    private:
        static gboolean timeout(gpointer data) {return true;};
        static gboolean wake_up(gpointer data);

        static void clear_surface(void);
        static void resize_cb(GtkWidget *widget, int width, int height, gpointer data);
        static void draw_cb(GtkDrawingArea *drawing_area, cairo_t *cr, int width, int height, gpointer data);
        static void draw_brush(GtkWidget *widget, double x, double y, uint16_t color=0);
        static void close_window(void);
        static void activate(GtkApplication *app, gpointer *user_data);
};

#endif