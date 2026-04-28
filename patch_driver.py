import re

filepath = "rtl8188eus/os_dep/linux/ioctl_cfg80211.c"
with open(filepath, "r") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Find and show lines around cfg80211_roamed
for i, line in enumerate(lines):
    if "cfg80211_roamed" in line:
        print(f"Line {i+1}: {repr(line)}")

# Find the old-style multi-arg cfg80211_roamed call
# It starts with cfg80211_roamed(padapter->pnetdev and ends with , GFP_ATOMIC);
start = None
end = None
for i, line in enumerate(lines):
    if "cfg80211_roamed(padapter->pnetdev" in line and "&roam_info" not in line:
        start = i
    if start is not None and ", GFP_ATOMIC);" in line and i > start:
        end = i
        break

if start is not None and end is not None:
    print(f"Found old call from line {start+1} to {end+1}")
    print("Old content:")
    for l in lines[start:end+1]:
        print(repr(l))
    # Replace with new single line
    new_line = "\t\tcfg80211_roamed(padapter->pnetdev, &roam_info, GFP_ATOMIC);\n"
    lines[start:end+1] = [new_line]
    print("Replaced successfully")
else:
    print("WARNING: Could not find old-style call")

with open(filepath, "w") as f:
    f.writelines(lines)

print("Done")
