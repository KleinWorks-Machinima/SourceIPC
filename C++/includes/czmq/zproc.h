/*  =========================================================================
    zproc - process configuration and status

    Copyright (c) the Contributors as noted in the AUTHORS file.
    This file is part of CZMQ, the high-level C binding for 0MQ:
    http://czmq.zeromq.org.

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
    =========================================================================
*/

#ifndef ZPROC_H_INCLUDED
#define ZPROC_H_INCLUDED

#ifdef __cplusplus
extern "C" {
#endif


//  @warning THE FOLLOWING @INTERFACE BLOCK IS AUTO-GENERATED BY ZPROJECT
//  @warning Please edit the model at "api/zproc.api" to make changes.
//  @interface
//  This is a draft class, and may change without notice. It is disabled in
//  stable builds by default. If you use this in applications, please ask
//  for it to be pushed to stable state. Use --enable-drafts to enable.
#ifdef CZMQ_BUILD_DRAFT_API
//  *** Draft method, for development use, may change without warning ***
//  Create a new zproc.
//  NOTE: On Windows and with libzmq3 and libzmq2 this function
//  returns NULL. Code needs to be ported there.
CZMQ_EXPORT zproc_t *
    zproc_new (void);

//  *** Draft method, for development use, may change without warning ***
//  Destroy zproc, wait until process ends.
CZMQ_EXPORT void
    zproc_destroy (zproc_t **self_p);

//  *** Draft method, for development use, may change without warning ***
//  Return command line arguments (the first item is the executable) or
//  NULL if not set.
//  Caller owns return value and must destroy it when done.
CZMQ_EXPORT zlist_t *
    zproc_args (zproc_t *self);

//  *** Draft method, for development use, may change without warning ***
//  Setup the command line arguments, the first item must be an (absolute) filename
//  to run.
CZMQ_EXPORT void
    zproc_set_args (zproc_t *self, zlist_t **arguments);

//  *** Draft method, for development use, may change without warning ***
//  Setup the command line arguments, the first item must be an (absolute) filename
//  to run. Variadic function, must be NULL terminated.
CZMQ_EXPORT void
    zproc_set_argsx (zproc_t *self, const char *arguments, ...);

//  *** Draft method, for development use, may change without warning ***
//  Setup the environment variables for the process.
CZMQ_EXPORT void
    zproc_set_env (zproc_t *self, zhash_t **arguments);

//  *** Draft method, for development use, may change without warning ***
//  Connects process stdin with a readable ('>', connect) zeromq socket. If
//  socket argument is NULL, zproc creates own managed pair of inproc
//  sockets.  The writable one is then accessible via zproc_stdin method.
CZMQ_EXPORT void
    zproc_set_stdin (zproc_t *self, void *socket);

//  *** Draft method, for development use, may change without warning ***
//  Connects process stdout with a writable ('@', bind) zeromq socket. If
//  socket argument is NULL, zproc creates own managed pair of inproc
//  sockets.  The readable one is then accessible via zproc_stdout method.
CZMQ_EXPORT void
    zproc_set_stdout (zproc_t *self, void *socket);

//  *** Draft method, for development use, may change without warning ***
//  Connects process stderr with a writable ('@', bind) zeromq socket. If
//  socket argument is NULL, zproc creates own managed pair of inproc
//  sockets.  The readable one is then accessible via zproc_stderr method.
CZMQ_EXPORT void
    zproc_set_stderr (zproc_t *self, void *socket);

//  *** Draft method, for development use, may change without warning ***
//  Return subprocess stdin writable socket. NULL for
//  not initialized or external sockets.
CZMQ_EXPORT void *
    zproc_stdin (zproc_t *self);

//  *** Draft method, for development use, may change without warning ***
//  Return subprocess stdout readable socket. NULL for
//  not initialized or external sockets.
CZMQ_EXPORT void *
    zproc_stdout (zproc_t *self);

//  *** Draft method, for development use, may change without warning ***
//  Return subprocess stderr readable socket. NULL for
//  not initialized or external sockets.
CZMQ_EXPORT void *
    zproc_stderr (zproc_t *self);

//  *** Draft method, for development use, may change without warning ***
//  Starts the process, return just before execve/CreateProcess.
CZMQ_EXPORT int
    zproc_run (zproc_t *self);

//  *** Draft method, for development use, may change without warning ***
//  process exit code
CZMQ_EXPORT int
    zproc_returncode (zproc_t *self);

//  *** Draft method, for development use, may change without warning ***
//  PID of the process
CZMQ_EXPORT int
    zproc_pid (zproc_t *self);

//  *** Draft method, for development use, may change without warning ***
//  return true if process is running, false if not yet started or finished
CZMQ_EXPORT bool
    zproc_running (zproc_t *self);

//  *** Draft method, for development use, may change without warning ***
//  The timeout should be zero or greater, or -1 to wait indefinitely.
//  wait or poll process status, return return code
CZMQ_EXPORT int
    zproc_wait (zproc_t *self, int timeout);

//  *** Draft method, for development use, may change without warning ***
//  send SIGTERM signal to the subprocess, wait for grace period and
//  eventually send SIGKILL
CZMQ_EXPORT void
    zproc_shutdown (zproc_t *self, int timeout);

//  *** Draft method, for development use, may change without warning ***
//  return internal actor, useful for the polling if process died
CZMQ_EXPORT void *
    zproc_actor (zproc_t *self);

//  *** Draft method, for development use, may change without warning ***
//  send a signal to the subprocess
CZMQ_EXPORT void
    zproc_kill (zproc_t *self, int signal);

//  *** Draft method, for development use, may change without warning ***
//  set verbose mode
CZMQ_EXPORT void
    zproc_set_verbose (zproc_t *self, bool verbose);

//  *** Draft method, for development use, may change without warning ***
//  Self test of this class.
CZMQ_EXPORT void
    zproc_test (bool verbose);

#endif // CZMQ_BUILD_DRAFT_API
//  @end


#ifdef __cplusplus
}
#endif

#endif
