# KillCloud

**Replace $20/mo cloud AI subscriptions with a 1-click, 100% offline local AI workspace (`0 GPU`, `0 bytes` sent to cloud).**

Powered by [MYCA-Modchip](https://github.com/brienteth/myca-ghr-modchip) (`78+ tok/s` pure CPU C99 + SIMD, `69 MB` model).

## Quick Start

```bash
git clone https://github.com/brienteth/killcloud.git
cd killcloud
python3 killcloud.py
# Open http://127.0.0.1:8989/
```

### Install the 0-GPU Offline Engine (One Time)

```bash
curl -fsSL https://raw.githubusercontent.com/brienteth/myca-ghr-modchip/main/install.sh | sh
myca-modchip pull smollm2-135m
```

## Included Offline Tools
- **Private Chat:** Zero-telemetry local assistant.
- **Note & Log Summarizer:** Summarize sensitive docs/emails without leaving your machine.
- **Offline Code Helper:** Local C/Python/systems helper with `$0/mo` cost.

## License
MIT

