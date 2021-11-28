/* Adafruit GFX compatible renderer with gtk backend */
#include "GTK_GFX.h"
#include <gtk/gtk.h>
#include <string>
#include <iostream>
#include <stdlib.h>     /* exit, EXIT_FAILURE */

namespace GTK_GFX_GLOBAL {
    uint16_t width;
    uint16_t height;
    uint16_t scale;
    bool color;

    bool application_running = false;
    bool sleeping = false;

    cairo_surface_t *surface = NULL;

    GtkApplication *app = NULL;
    GMainContext *context = NULL;
    GtkWidget *drawing_area = NULL;
}

GTK_GFX::GTK_GFX(uint16_t width, uint16_t height, uint16_t scale, bool color) : Adafruit_GFX(width, height) {
    // Setup GTK environment
    GTK_GFX_GLOBAL::width = width;
    GTK_GFX_GLOBAL::height = height;
    GTK_GFX_GLOBAL::scale = scale;
    GTK_GFX_GLOBAL::color = color;

    // The nice people from GTK automatically set the locale,
    // yet we want to remain international :=)
    gtk_disable_setlocale();

    GTK_GFX_GLOBAL::app = gtk_application_new ("com.github.dloeckx", G_APPLICATION_FLAGS_NONE);
    g_signal_connect (GTK_GFX_GLOBAL::app, "activate", G_CALLBACK (GTK_GFX::activate), NULL);
    g_timeout_add_seconds (1, GTK_GFX::timeout, NULL); // Make sure g_main_context_iteration gets back to us every second

    gboolean acquired_context;
    GTK_GFX_GLOBAL::context = g_main_context_default ();
    g_main_context_acquire (GTK_GFX_GLOBAL::context);

    GError *error = NULL;
    if (!g_application_register (G_APPLICATION (GTK_GFX_GLOBAL::app), NULL, &error))
      {
        g_printerr ("Failed to register: %s\n", error->message);
        g_error_free (error);
      }

    g_application_activate (G_APPLICATION (GTK_GFX_GLOBAL::app));
    GTK_GFX_GLOBAL::application_running = true;

    // Run window setup events
    while (g_main_context_iteration (GTK_GFX_GLOBAL::context, FALSE)) {
    };
}

GTK_GFX::~GTK_GFX() {
  // Release
  g_settings_sync ();
  while (g_main_context_iteration (GTK_GFX_GLOBAL::context, FALSE)) {
  };
  g_main_context_release (GTK_GFX_GLOBAL::context);

  // status = g_application_run (G_APPLICATION (app), argc, argv);
  g_object_unref (GTK_GFX_GLOBAL::app);
}

bool GTK_GFX::sleep(unsigned int millis) {
  if (millis == 0) {
    // Run once
    g_main_context_iteration(GTK_GFX_GLOBAL::context, TRUE);
  }
  else 
  {
    GTK_GFX_GLOBAL::sleeping = millis > 0;
    g_timeout_add(millis, GTK_GFX::wake_up, NULL);

    while (GTK_GFX_GLOBAL::application_running && GTK_GFX_GLOBAL::sleeping) {
      g_main_context_iteration(GTK_GFX_GLOBAL::context, TRUE);
    }
  }
  return GTK_GFX_GLOBAL::application_running;
}

void GTK_GFX::drawPixel(int16_t x, int16_t y, uint16_t color) {
    GTK_GFX::draw_brush(GTK_GFX_GLOBAL::drawing_area, x * GTK_GFX_GLOBAL::scale, y * GTK_GFX_GLOBAL::scale, color);
}

gboolean GTK_GFX::wake_up(gpointer data) {
  GTK_GFX_GLOBAL::sleeping = false;
  return false;
}

void GTK_GFX::clear_surface(void) {
  cairo_t *cr;

  cr = cairo_create (GTK_GFX_GLOBAL::surface);

  cairo_set_source_rgb (cr, 0.5, 0.5, 0.5);
  cairo_paint (cr);

  cairo_destroy (cr);
}

void GTK_GFX::resize_cb(GtkWidget *widget, int width, int height, gpointer data) {
  if (GTK_GFX_GLOBAL::surface)
    {
      cairo_surface_destroy (GTK_GFX_GLOBAL::surface);
      GTK_GFX_GLOBAL::surface = NULL;
    }

  if (gtk_native_get_surface (gtk_widget_get_native (widget)))
    {
      GTK_GFX_GLOBAL::surface = gdk_surface_create_similar_surface (gtk_native_get_surface (gtk_widget_get_native (widget)),
                                                   CAIRO_CONTENT_COLOR,
                                                   gtk_widget_get_width (widget),
                                                   gtk_widget_get_height (widget));

      /* Initialize the surface to white */
      GTK_GFX::clear_surface();
    }
}

void GTK_GFX::draw_cb(GtkDrawingArea *drawing_area, cairo_t *cr, int width, int height, gpointer data) {
  cairo_set_source_surface (cr, GTK_GFX_GLOBAL::surface, 0, 0);
  cairo_paint (cr);  
}

void GTK_GFX::draw_brush(GtkWidget *widget, double x, double y, uint16_t color) {
  cairo_t *cr;

  double color_r, color_g, color_b;

  if (GTK_GFX_GLOBAL::color) {
    // We have RGB565 (bits), and want the original R, G and B values
    color_r = double(color & 0b1111100000000000) / 0b1111100000000000;
    color_g = double(color & 0b0000011111100000) / 0b0000011111100000; 
    color_b = double(color & 0b0000000000011111) / 0b0000000000011111;
  } else {
    color_r = color_g = color_b = double(color & 255) / 255;
  }

  /* Paint to the surface, where we store our state */
  cr = cairo_create (GTK_GFX_GLOBAL::surface);

  cairo_set_source_rgb (cr, color_r, color_g, color_b);

  cairo_rectangle (cr, x, y, GTK_GFX_GLOBAL::scale, GTK_GFX_GLOBAL::scale);
  cairo_fill (cr);

  cairo_destroy (cr);

  /* Now invalidate the drawing area. */
  gtk_widget_queue_draw (widget);
}

void GTK_GFX::close_window(void) {
  if (GTK_GFX_GLOBAL::surface)
    cairo_surface_destroy (GTK_GFX_GLOBAL::surface);
    GTK_GFX_GLOBAL::surface = NULL;
  
  GTK_GFX_GLOBAL::application_running = FALSE;
  exit(-1);  // Apparantly considered bad behaviour, yet I don't know better. We can't throw exceptions for some reason.
}

void GTK_GFX::activate(GtkApplication *app, gpointer *user_data) {
  GtkWidget *window;
  GtkWidget *frame;

  window = gtk_application_window_new (app);
  std::string window_title = "Mock Display " + std::to_string(GTK_GFX_GLOBAL::width) + "x"+ std::to_string(GTK_GFX_GLOBAL::height);
  gtk_window_set_title (GTK_WINDOW (window), window_title.c_str());
  g_signal_connect (window, "destroy", G_CALLBACK (GTK_GFX::close_window), NULL);

  frame = gtk_frame_new (NULL);
  gtk_window_set_child (GTK_WINDOW (window), frame);

  GTK_GFX_GLOBAL::drawing_area = gtk_drawing_area_new();

  gtk_widget_set_size_request (GTK_GFX_GLOBAL::drawing_area, GTK_GFX_GLOBAL::width * GTK_GFX_GLOBAL::scale, GTK_GFX_GLOBAL::height * GTK_GFX_GLOBAL::scale);
  gtk_frame_set_child (GTK_FRAME (frame), GTK_GFX_GLOBAL::drawing_area);
  gtk_drawing_area_set_draw_func (GTK_DRAWING_AREA (GTK_GFX_GLOBAL::drawing_area), GTK_GFX::draw_cb, NULL, NULL);
  g_signal_connect_after (GTK_GFX_GLOBAL::drawing_area, "resize", G_CALLBACK (GTK_GFX::resize_cb), NULL);
  gtk_widget_show (window);
}



