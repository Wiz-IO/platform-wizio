#include <Arduino.h>

// https://github.com/cesanta/mjs

#include <mjs.h>
struct mjs *JS;

extern "C" void *my_dlsym(void *handle, const char *name);

void setup()
{
  mjs_val_t exec_result;
  JS = mjs_create();
  mjs_set_ffi_resolver(JS, my_dlsym);

  mjs_exec(JS, "print('<JS> Hello World')", NULL);
  mjs_err err = mjs_exec_file(JS, "D:\\JS\\1.js", NULL);
  Serial.printf("\nEND %s\n", mjs_strerror(JS, err));
}

void loop()
{
  delay(1000);
}