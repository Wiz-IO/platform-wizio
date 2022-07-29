#include <interface.h>

void foo(int x)
{
  printf("<JS> uno due tre = %d\n", x);
}

void *my_dlsym(void *handle, const char *name)
{
  if (strcmp(name, "foo") == 0)
    return foo;
  return NULL;
}