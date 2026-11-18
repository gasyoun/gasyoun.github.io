# MIT License — © 2026 Dr. Mārcis Gasūns — https://github.com/gasyoun/gasyoun.github.io
"""Console-popup watcher + negative-control canary (Windows only).

Polls EnumWindows every 80 ms, logs only NEW visible top-level windows with
class, title, pid, PEB command line and parent chain. Read-only; writes JSONL
to --out. Zero third-party dependencies (stdlib + ctypes).

Usage:
  pythonw console_watch_cal.py --negctl --out negctl.jsonl        # A/B canary, ~4 s
  pythonw console_watch_cal.py --duration 900 --out watch.jsonl   # 15-min interception

Why pythonw and why a canary:
  A console-attached parent (a terminal-hosted python.exe) gives its cmd child
  an inherited console — no NEW window appears and the canary reads 0/0
  (a documented false negative). Run under pythonw.exe (GUI subsystem, no
  console) and prove the watcher is not blind before trusting a quiet log.
  For a forced console even from a console-attached shell, spawn the control
  window with `cmd /c start "" cmd /c "ping -n 4 127.0.0.1 >nul"` while the
  watcher is running: the new window must be caught.

Exit: 0 on clean completion. JSONL event types: start, heartbeat,
new_visible_window, negative_control, negative_control_verdict, stop.
"""
import argparse
import ctypes
import ctypes.wintypes as wt
import datetime
import json
import os
import subprocess
import sys
import time

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
ntdll = ctypes.WinDLL("ntdll", use_last_error=True)

PROCESS_BASIC_INFORMATION = None


class UNICODE_STRING(ctypes.Structure):
    _fields_ = [("Length", wt.USHORT), ("MaximumLength", wt.USHORT),
                ("Buffer", ctypes.c_void_p)]


def _define_pbi():
    global PROCESS_BASIC_INFORMATION

    class PBI(ctypes.Structure):
        _fields_ = [("ExitStatus", wt.LONG), ("PebBaseAddress", ctypes.c_void_p),
                    ("AffinityMask", ctypes.c_void_p), ("BasePriority", wt.LONG),
                    ("UniqueProcessId", ctypes.c_void_p),
                    ("InheritedFromUniqueProcessId", ctypes.c_void_p)]
    PROCESS_BASIC_INFORMATION = PBI


_define_pbi()

ENUM_PROC = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
TH32CS_SNAPPROCESS = 0x2
MAX_PATH = 260


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [("dwSize", wt.DWORD), ("cntUsage", wt.DWORD),
                ("th32ProcessID", wt.DWORD), ("th32DefaultHeapID", ctypes.POINTER(wt.ULONG)),
                ("th32ModuleID", wt.DWORD), ("cntThreads", wt.DWORD),
                ("th32ParentProcessID", wt.DWORD), ("pcPriClassBase", wt.LONG),
                ("dwFlags", wt.DWORD), ("szExeFile", ctypes.c_char * MAX_PATH)]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def peb_cmdline(pid):
    """Return PEB ProcessParameters->CommandLine for a live pid, or ''."""
    try:
        h = kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return ""
        pbi = PROCESS_BASIC_INFORMATION()
        ntdll.NtQueryInformationProcess(h, 0, ctypes.byref(pbi), ctypes.sizeof(pbi), None)
        peb = pbi.PebBaseAddress
        if not peb:
            kernel32.CloseHandle(h)
            return ""
        pp = ctypes.c_void_p()
        ctypes.windll.kernel32.ReadProcessMemory(
            h, ctypes.c_void_p(peb + 0x20), ctypes.byref(pp), ctypes.sizeof(pp), None)
        if not pp.value:
            kernel32.CloseHandle(h)
            return ""
        off = 0x70 if ctypes.sizeof(ctypes.c_void_p) == 8 else 0x40
        us = UNICODE_STRING()
        ctypes.windll.kernel32.ReadProcessMemory(
            h, ctypes.c_void_p(pp.value + off), ctypes.byref(us), ctypes.sizeof(us), None)
        buf = ctypes.create_unicode_buffer(max(1, us.Length // 2 + 1))
        ctypes.windll.kernel32.ReadProcessMemory(
            h, ctypes.c_void_p(us.Buffer), buf, us.Length, None)
        kernel32.CloseHandle(h)
        return buf.value
    except Exception:
        return ""


def exe_name(pid):
    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap == -1:
        return ""
    e = PROCESSENTRY32()
    e.dwSize = ctypes.sizeof(e)
    out = ""
    ok = kernel32.Process32First(snap, ctypes.byref(e))
    while ok:
        if e.th32ProcessID == pid:
            out = e.szExeFile.decode("utf-8", "replace")
            break
        ok = kernel32.Process32Next(snap, ctypes.byref(e))
    kernel32.CloseHandle(snap)
    return out


def parent_of(pid):
    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap == -1:
        return 0
    e = PROCESSENTRY32()
    e.dwSize = ctypes.sizeof(e)
    pp = 0
    ok = kernel32.Process32First(snap, ctypes.byref(e))
    while ok:
        if e.th32ProcessID == pid:
            pp = e.th32ParentProcessID
            break
        ok = kernel32.Process32Next(snap, ctypes.byref(e))
    kernel32.CloseHandle(snap)
    return pp


def ancestry(pid, depth=6):
    chain = []
    seen = set()
    for _ in range(depth):
        if not pid or pid in seen:
            break
        seen.add(pid)
        pp = parent_of(pid)
        chain.append({"pid": pid, "parent": pp, "process": exe_name(pid),
                      "cmdline_peb": peb_cmdline(pid)})
        if not pp or pp == pid:
            break
        pid = pp
    return chain


def visible_windows():
    found = []

    @ENUM_PROC
    def cb(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        n = user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(n + 1)
        user32.GetWindowTextW(hwnd, buf, n + 1)
        cls = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(hwnd, cls, 256)
        pid = wt.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        found.append({"hwnd": hwnd, "class": cls.value, "title": buf.value, "pid": pid.value})
        return True

    user32.EnumWindows(cb, 0)
    return found


def write(path, obj):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def probe(label, flags, out, baseline):
    # Keep the console alive ~3 s: an instant `echo` exits inside one 80 ms poll.
    cmd = "echo " + label + " & ping -n 4 127.0.0.1 >nul"
    p = subprocess.Popen(["cmd.exe", "/d", "/s", "/c", cmd],
                         creationflags=flags, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    time.sleep(1.0)  # let the window appear while the watcher is polling
    p.wait()
    time.sleep(0.5)
    new = [w for w in visible_windows() if w["hwnd"] not in baseline]
    write(out, {"utc": utc(), "type": "negative_control", "phase": label,
                "creationflags": flags, "new_visible_windows": len(new),
                "windows": [{"class": w["class"], "title": w["title"],
                             "ancestry": ancestry(w["pid"])} for w in new]})
    baseline.update(w["hwnd"] for w in visible_windows())
    return len(new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, default=900.0)
    ap.add_argument("--interval", type=float, default=0.08)
    ap.add_argument("--heartbeat", type=float, default=30.0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--negctl", action="store_true")
    a = ap.parse_args()

    out = os.path.abspath(a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.exists(out):
        os.remove(out)

    base = visible_windows()
    baseline = {w["hwnd"] for w in base}
    write(out, {"utc": utc(), "type": "start", "duration_target_s": a.duration,
                "baseline_visible_windows": len(base), "process_count": 0,
                "note": "console-popup watcher (gasyoun.github.io/console-popup-watch)"})
    if a.negctl:
        bad = probe("default-spawn", 0, out, baseline)
        good = probe("create-no-window", 0x08000000, out, baseline)
        write(out, {"utc": utc(), "type": "negative_control_verdict",
                    "default_spawn_windows": bad, "create_no_window_windows": good,
                    "watcher_not_blind": bad > 0 and good == 0})
        print(f"NEGCTL default_spawn={bad} create_no_window={good} "
              f"watcher_not_blind={bad > 0 and good == 0}")
        return

    t0 = time.time()
    last_hb = t0
    while time.time() - t0 < a.duration:
        now = time.time()
        for w in visible_windows():
            if w["hwnd"] not in baseline:
                baseline.add(w["hwnd"])
                write(out, {"utc": utc(), "type": "new_visible_window",
                            "elapsed_s": round(now - t0, 3), "pid": w["pid"],
                            "class": w["class"], "title": w["title"],
                            "ancestry": ancestry(w["pid"])})
        if now - last_hb >= a.heartbeat:
            last_hb = now
            write(out, {"utc": utc(), "type": "heartbeat",
                        "elapsed_s": round(now - t0, 3),
                        "visible_window_count": len(visible_windows())})
        time.sleep(a.interval)
    write(out, {"utc": utc(), "type": "stop", "elapsed_s": round(time.time() - t0, 3)})


if __name__ == "__main__":
    main()
