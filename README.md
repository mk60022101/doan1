# Đồ án đồng bộ hóa tín hiệu 5G NR

Repository mô phỏng và kiểm thử bài toán đồng bộ hóa tín hiệu 5G NR. Mã nguồn
được tổ chức theo kiến trúc `src`, có môi trường Python riêng, test tự động và
cấu hình cho các thí nghiệm quét tham số.

## Trạng thái các cổng

### G1 - Thiết lập môi trường và kiến trúc mã nguồn

Đã hoàn thành:

- Khởi tạo Git repository trên Linux/Ubuntu.
- Tổ chức mã lõi trong `src/nr_sync`.
- Tổ chức kiểm thử trong `tests`.
- Tổ chức thí nghiệm và cấu hình chạy hàng loạt trong `experiments`.
- Tạo môi trường ảo `.venv`.
- Khai báo NumPy, SciPy, Matplotlib, Jupyter và pytest trong
	`requirements.txt`.
- Cấu hình đóng gói editable bằng `pyproject.toml`.

### G2 - Sinh và kiểm thử tín hiệu đồng bộ

Đã hoàn thành module `src/nr_sync/sequences.py`:

- Sinh đủ 3 chuỗi PSS theo `N_ID^2` trong miền `{0, 1, 2}`.
- Sinh đủ 336 chuỗi SSS theo `N_ID^1` trong miền `[0, 335]` kết hợp với
	3 giá trị `N_ID^2`.
- Ánh xạ chính xác `PCI = 3 * N_ID^1 + N_ID^2`, phủ toàn bộ 1008 PCI từ 0
	đến 1007.
- Chuỗi đầu ra có 127 phần tử BPSK trong `{-1, +1}` và xác định hoàn toàn
	theo input.

Cổng C1/C3 được kiểm thử trong môi trường lý tưởng, không nhiễu và không CFO.
Bộ test kiểm tra toàn bộ miền PSS, SSS và PCI trong tối thiểu 100 lần lặp.

## Cấu trúc thư mục

```text
CODE/
├── src/
│   └── nr_sync/
│       ├── sequences.py       # PSS, SSS và ánh xạ PCI - đã triển khai
│       ├── ofdm.py            # Tài nguyên, IFFT/FFT và CP - khung G3
│       ├── channel.py         # AWGN, đa đường, Doppler, CFO - khung G3
│       ├── synchronizer.py    # A0, A1, A2 - khung G4
│       └── metrics.py         # Pd, Pfa, RMSE, CI - khung G5
├── tests/
│   └── test_module_structure.py
├── experiments/
│   ├── run_sweep.py
│   └── sweep_config.yaml
├── notebooks/
│   └── 01_exploration.ipynb
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Yêu cầu môi trường

- Linux/Ubuntu
- Python 3.10 trở lên
- Internet trong lần cài dependency đầu tiên

## Cài đặt

Từ thư mục `CODE`:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -e .
```

Kích hoạt môi trường nếu muốn dùng lệnh `python` và `pytest` trực tiếp:

```bash
source .venv/bin/activate
```

## Chạy kiểm thử

Chạy toàn bộ test:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -m pytest -q
```

`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` giúp loại các plugin pytest hệ thống không
liên quan nếu máy đã cài ROS hoặc plugin bên ngoài. Trong môi trường sạch,
có thể chạy ngắn gọn:

```bash
.venv/bin/python -m pytest -q
```

Test chính của G2 là:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -m pytest -q tests/test_module_structure.py
```

Kết quả đã xác nhận: `3 passed`, bao gồm kiểm tra exhaustive 100 vòng và
kiểm tra đủ 1008 giá trị PCI.

## Chạy notebook

Khởi động Jupyter từ thư mục `CODE`:

```bash
.venv/bin/jupyter lab
```

Sau đó mở `notebooks/01_exploration.ipynb`. Notebook hiện dùng để kiểm tra
khả năng import các module và sẽ được mở rộng khi hoàn thành các cổng OFDM,
kênh truyền và bộ đồng bộ.

## Thí nghiệm quét tham số

Cấu hình mẫu nằm ở `experiments/sweep_config.yaml`. Bộ chạy hàng loạt nằm ở
`experiments/run_sweep.py` và đã có giao diện cho seed, thư mục kết quả và
resume; phần mô phỏng chi tiết sẽ được nối vào các module ở các cổng tiếp theo.

## Lệnh nhanh

```bash
cd CODE
source .venv/bin/activate
python -m pytest -q
```

## Tài liệu tham chiếu

Các công thức PSS, SSS và PCI được triển khai theo 3GPP TS 38.211, mục
7.4.2 về tín hiệu đồng bộ SS/PBCH block.
