# kaiduan

定期将 [iptv v2](https://api.kaiduan.fun/kd/json/v2/iptv.json) / [iptv v1](https://api.kaiduan.fun/kd/json/v1/iptv.json) 转为 DIYP 风格播放列表：

- `iptv_v2.txt`
- `iptv_v1.txt`

GitHub Actions 工作流：`.github/workflows/update-iptv.yml`（定时每 6 小时 + 手动触发）。

本地转换：

```bash
python scripts/json_to_iptv_txt.py data/iptv_v2.json iptv_v2.txt
```
