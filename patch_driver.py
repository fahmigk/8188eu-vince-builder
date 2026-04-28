import re

filepath = "rtl8188eus/os_dep/linux/ioctl_cfg80211.c"
with open(filepath, "r") as f:
    content = f.read()

old = r'cfg80211_roamed\(padapter->pnetdev\s*\n#if LINUX_VERSION_CODE > KERNEL_VERSION\(2, 6, 39\) \|\| defined\(COMPAT_KERNEL_RELEASE\)\s*\n, notify_channel\s*\n#endif\s*\n, cur_network->network\.MacAddress\s*\n, pmlmepriv->assoc_req \+ sizeof\(struct rtw_ieee80211_hdr_3addr\) \+ 2\s*\n, pmlmepriv->assoc_req_len - sizeof\(struct rtw_ieee80211_hdr_3addr\) - 2\s*\n, pmlmepriv->assoc_rsp \+ sizeof\(struct rtw_ieee80211_hdr_3addr\) \+ 6\s*\n, pmlmepriv->assoc_rsp_len - sizeof\(struct rtw_ieee80211_hdr_3addr\) - 6\s*\n, GFP_ATOMIC\);'

new = 'cfg80211_roamed(padapter->pnetdev, &roam_info, GFP_ATOMIC);'

result, count = re.subn(old, new, content)
print(f"Replacements: {count}")

with open(filepath, "w") as f:
    f.write(result)

print("Done")
