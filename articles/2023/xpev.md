---
layout: article
---
<div class="tags" markdown="1">

**Xonsh** <br> [software](/articles/tags/software)

</div>


[TOC]

<a class="prev" href="/articles/2023/otcd"> < </a> <a class="next" href="/articles/2023/marg"> > </a>
    
Xonsh is a "Python-powered, cross-platform, Unix-gazing shell language and command prompt."[^1]Many operations that are clumsy in Windows natively are comparatively simple using the Xonsh shell. Let's take a look at one example, modifying the PATH environment variable.In Windows 11 without Xonsh, modifying your PATH environment variable can be done in either the "Environment Variables" window or by updating this key [^2].

With Xonsh, the variable is [stored directly](https://xon.sh/tutorial.html#environment-variables) in a list of strings called <code>$PATH</code>. Part of the magic of Xonsh is that we can use this variable for built-in Python methods.First, I need to add this line in my Xonsh configuration file:

```python
$UPDATE_OS_ENVIRON = True
```

When <code>True</code>, the OS environment will always [be updated](https://xon.sh/envvars.html#update-os-environ) when the xonsh environment changes. This gives us a more efficient way to interact with the PATH.

For example, to remove the most recent entry from the list I can use the <code>pop()</code> method:

```python
$PATH.pop(-1)
```

Now let's say I change my mind. I can use the <code>append()</code> method and add the path back to the list:
    
```python
$PATH.append('C:\\Users\\wfurn\\Speedtest-cli')
```

How cool is that? Other methods would work as well of course, but these two seem the most useful to me at the moment.

Some other great examples of pythonobash can be found in this [overview video](https://www.youtube.com/watch?v=x85LSyCxiw8).

  [^1]: [https://xon.sh/](https://xon.sh/)
  [^2]: HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment

