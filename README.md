# CN-DNS-Split

Loon DNS 分流插件。按服务商归属为域名指定 DNS，尽量保留 CDN 本地调度。

## 文件
- `plugins/CN-DNS-Split.plugin`：精选规则，建议先启用。
- `scripts/build_accelerated_plugin.py`：从国内加速域名库生成可选补充插件。
- `dist/CN-DNS-Accelerated.plugin`：GitHub Actions 生成的大型补充插件。
- `.github/workflows/update-domains.yml`：每周更新工作流。

## 安装
1. 在 Loon 中打开插件 Raw 链接或下载后导入。
2. 先只启用精选插件，观察常用网站解析。
3. 自动生成的大型补充插件是可选项，生成后先检查体积和加载表现，再决定是否启用。
4. 本插件只含 `[Host]`，不覆盖主配置中的全局 DNS、代理、策略组或分流规则。

## DNS 归属
- 阿里系及通用国内服务：阿里 DoH
- 腾讯 / 微信 / QQ / 腾讯云：DNSPod DoH
- 百度：百度公共 DNS
- 字节系：火山引擎 DNS
- 360：360 DoH
- Apple：Apple DoH
- 京东、Bilibili：系统 DNS，尽量保留本地 CDN 调度

注意：服务商映射是按公开域名归属整理，不代表每个 DNS 服务在所有网络环境都完成实测。遇到解析异常时，先停用对应映射，不要盲目修改全局 DNS。

## 自动生成的数据源
可选补充插件使用 [felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list) 的 `accelerated-domains.china.conf`。该列表依据国内 NS 或中国 DNS 返回大陆 CDN/地址等标准筛选，不等于所有 `.cn` 域名。

服务商分类思路参考 [GetSomeFries DNS Wiki](https://github.com/VirgilClyne/GetSomeFries/wiki/%F0%9F%8C%90-DNS)。

## 自动更新
GitHub Actions 每周一 UTC 02:30 自动生成补充插件，也可在 Actions 页面手动运行。

## 免责声明
DNS 结果受运营商、地区、出口和缓存影响。本项目不保证所有网络环境都获得最优 CDN 节点。启用前请备份 Loon 配置。
