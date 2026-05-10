---
layout: article
---
<div class="tags" markdown="1">

**OpenTrack Crash Troubleshooting** <br> [software](/articles/tags/software), [debugging](/articles/tags/debugging)

</div>


[TOC]

<a class="prev"> < </a>
<a class="next" href="/articles/2023/xpev"> > </a>

<p> <em>Recently, I collaborated in diagnosing and resolving an issue with OpenTrack (OT), a FOSS
        head-tracking
        program for games like DCS, Star Citizen and Microsoft Flight Simulator. I used WinDbg to analyze the crash
        files and then extrapolated to draw conclusions
        based on the source code. Here's a bit about what I learned. This is all documented in the <a
          href="https://github.com/opentrack/opentrack/issues/1661"  target="_blank"  class="inline">issue #1661 on
          GitHub</a>.</em></p>
<p style="text-align: center">∅</p>

## The Issue

<p>OpenTrack starts and then immediately closes. This also happens on the portable version and in
      prior
      OT releases. There is no error message or information displayed to the user about why the crash occurs. A
      crash dump file is stored in <code><em>\AppData\Local\CrashDumps</em></code> when the application exits.</p>

## Troubleshooting

<p>
      First, to try and get a sense of what the problem actually is, I open the crash dump file in Visual Studio to
      look for an exception message or error code. I find this error:
    </p>

```
Exception Message: 0xc0000409
```

<p>
      The message associated with this code is
      <code>"Security check failure or stack buffer overrun"</code>. Next, I check whether
      other users of the app have experienced similar issues, and I find the other issues mentioned in <a
        href="https://github.com/opentrack/opentrack/issues/1661"  target="_blank"  class="inline">#1661</a>.
</p>

Without much else to go on I begin to debug and analyze the crash using WinDbg. Here are the results from the initial WinDbg trace:


```
STACK_TEXT:
WARNING: Stack unwind information not available. Following frames may be wrong
0019fbfc 70cfbdbd ... opentrack_user_interface!process_detector_worker::qt_metacall+0x6d36
0019fc44 70cfbe53 ... opentrack_user_interface!process_detector_worker::qt_metacall+0x6c8d
0019fc6c 70ce1646 ... opentrack_user_interface!process_detector_worker::qt_metacall+0x6d23
0019fcb8 70ce1802 ... opentrack_user_interface+0x1646
0019fd48 0061c1ab ... opentrack_user_interface!otr_main+0x92
0019fd8c 0061d8e2 ... opentrack+0xc1ab
0019fdd8 762e7d59 ... opentrack+0xd8e2
0019fde8 7771b74b ... kernel32!BaseThreadInitThunk+0x19
0019fe40 7771b6cf ... ntdll!__RtlUserThreadStart+0x2b
0019fe50 00000000 ... ntdll!_RtlUserThreadStart+0x1b
```

<p>This didn't really help me much. A few hours of troubleshooting later, I took to the repo's "issues" page with
      the stack details and not much else.</p>
      
## The Resolution      
      
That's when I learned from the repo's owner that OT contains a handy debug package with symbols from the application stored as .pdb (Program Database) files. Essentially these files allow you to see more details around the operations being performed in the trace. After loading the .pdb files in the WinDbg symbols section, I ran the back trace again, and was presented with this stack. Check out how many more details we can see in the trace now:

```
STACK_TEXT:
000000f1`d52ff3c0 00007ffa`cc9f313a ... opentrack_user_interface!_invoke_watson+0x18>
000000f1`d52ff3f0 00007ffa`cc9f3022 ... opentrack_user_interface!_invalid_parameter_internal+0xce
000000f1`d52ff430 00007ffa`cc9f3155 ... opentrack_user_interface!_invalid_parameter+0x52
000000f1`d52ff4b0 00007ffa`cc9f2c71 ...
      opentrack_user_interface!_invalid_parameter_noinfo+0x19
000000f1`d52ff4f0 00007ffa`cc9d17c0 ... opentrack_user_interface!strcat_s+0x2d
000000f1`d52ff520 00007ffa`cc9d1a07 ... opentrack_user_interface! add_win32_path+0x180
000000f1`d52ff5c0 00007ff7`1f45ddb9 ... opentrack_user_interface!otr_main+0x107
000000f1`d52ff7a0 00007ff7`1f45f676 ... opentrack!WinMain+0x39
000000f1`d52ff810 00007ffb`7d7226ad ... opentrack!__scrt_common_main_seh+0x106
000000f1`d52ff850 00007ffb`7ee6a9f8 ... KERNEL32!BaseThreadInitThunk+0x1d<br>
000000f1`d52ff880 00000000`00000000 ... ntdll!RtlUserThreadStart+0x28
```

The issue is much more clear with this stack. Notice the call to the function <code>strcat_s</code>. If we search the OT repo for this function, we can find the source of the issue:

```cpp
for (const char* ptr : contents)
  {
  if (ptr)
  strcat_s(env_path, sizeof(env_path), ptr);
  if (!ptr || ptr[0] == '\0' || env_path[0] == '\0')
    {
    qDebug() << "bad path element" << (ptr==nullptr ? " null " : ptr); ok=false; break; 
    } 
  }
```


<p>
      An invalid parameter is passed to the <code>strcat_s</code> function, which means there's a problem with my
      PATH
      environment variable. It can only have a max of 2047 characters. I'll let my comment from the GitHub issue
      explain further:<br><br><em> "Loading the trace file (with the symbols from the win32-dbginfo package) and
        running "!analyze -v".
        There are now references to "invalid_parameter" around a strcat_s function call. Looking in the source code,
        strcat_s is used one time in init.cpp in the method add_win32_path. That is
        also referenced in the
        stack. So the parameter passed to strcat_s (env_path) is invalid. My environment path variable is overflowing,
        which is why we see the c0000409 exception for stack buffer overrun."
      </em>
    </p>
<p>
      Once I saw that the <code>strcat_s</code> function in the source code was called with a variable
      <code>env_path</code>, the
      solution
      clicked. My environment path variable is greater than 2047 characters, leading to the crash. Changes were made
      to init.cpp to resolve this issue and those will be included in OT's new release. This
      issue was quite
      interesting and a rewarding one to finally solve. Special thanks to the OpenTrack owner Stanislaw for working
      with me to resolve it.
    </p>
