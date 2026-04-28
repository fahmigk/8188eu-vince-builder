filepath = "rtl8188eus/os_dep/linux/ioctl_cfg80211.c"
with open(filepath, "r") as f:
    lines = f.readlines()

# Find old-style multi-arg cfg80211_roamed call
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
    new_lines = [
        "\t\tstruct cfg80211_roam_info roam_info = {};\n",
        "\t\troam_info.bssid = cur_network->network.MacAddress;\n",
        "\t\troam_info.req_ie = pmlmepriv->assoc_req + sizeof(struct rtw_ieee80211_hdr_3addr) + 2;\n",
        "\t\troam_info.req_ie_len = pmlmepriv->assoc_req_len - sizeof(struct rtw_ieee80211_hdr_3addr) - 2;\n",
        "\t\troam_info.resp_ie = pmlmepriv->assoc_rsp + sizeof(struct rtw_ieee80211_hdr_3addr) + 6;\n",
        "\t\troam_info.resp_ie_len = pmlmepriv->assoc_rsp_len - sizeof(struct rtw_ieee80211_hdr_3addr) - 6;\n",
        "\t\tcfg80211_roamed(padapter->pnetdev, &roam_info, GFP_ATOMIC);\n",
    ]
    lines[start:end+1] = new_lines
    print("Replaced successfully")
else:
    print("WARNING: Could not find old-style call")

with open(filepath, "w") as f:
    f.writelines(lines)

print("Done")
