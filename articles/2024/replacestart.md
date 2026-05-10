---
layout: article
---
<div class="tags" markdown="1">

**Replace Start Menu on Windows** <br> [software](/articles/tags/software)

</div>


[TOC]

<a class="prev" href="/articles/2024/whynottrump"> < </a>
<a class="next" href="/articles/2024/dont-talk-unless-you-can-improve-the-silence"> > </a>

I use two main tools to replace the start menu:
- [Powertoys Run](https://learn.microsoft.com/en-us/windows/powertoys/run) (or [Flow Launcher](https://www.flowlauncher.com/))
- [Everything for Windows](https://www.voidtools.com/downloads/)

There is also an [Everything plugin](https://github.com/lin-ycv/EverythingPowerToys) for both Powertoys Run and Flow Launcher. This allows me to use a hotkey to search for any file on my system, and because of the way Everything indexing works, it's very fast.

I also use this Autohotkey Script to disable the Windows key, but retain its combinations (such as WIN+Arrow Keys):

```c      
;Disable LWin press and retain its combos
~LWin::vk07
```

And this script to hide the taskbar, in combination with the vanilla auto-hide functionality. This hides the taskbar or shows it again when CTRL + ALT + = is pressed.

```c
^!=:: ;Ctrl + Alt + = : Hitaskbar
If WinExist("ahk_claShell_TrayWnd")
{
 WinHide, ahk_claShell_TrayWnd
 WinHide, ahk_claShell_SecondaryTrayWnd
}
Else
{
 WinShow, ahk_claShell_TrayWnd
 WinShow, ahk_claShell_SecondaryTrayWnd
}
```

You can find the rest of my Autohotkey Scripts on my [Github](https://github.com/wfurney13/dotfiles/blob/master/ahk/hotkeys.ahk). I've tried to leave comments so that it's obvious what everything does. If you want a more stylish taskbar replacement, I recommend [Zebar](https://github.com/glzr-io/zebar) in combination with [GlazeWM](https://github.com/glzr-io/glazewm). 

I may make a seperate post about Zebar and GlazeWM when I have a better configuration and Zebar has been updated some more. I've also experimented with PowerToys Fancy Zones as well for this purpose.