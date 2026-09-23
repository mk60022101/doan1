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

## Mục tiêu demo hiện tại có ý nghĩa gì?

Mục tiêu “chạy pytest trực tiếp và đạt 100% trong kịch bản Noiseless” là một
cổng kiểm tra nền tảng, chưa phải toàn bộ hệ thống đồng bộ hóa. Nó chứng minh
rằng phần sinh vector ban đầu đã đúng và ổn định:

1. Mỗi `N_ID^2` tạo ra đúng một PSS dài 127.
2. Mỗi cặp `N_ID^1, N_ID^2` tạo ra đúng một SSS dài 127.
3. Công thức PCI phủ đủ 1008 giá trị.
4. Cùng input luôn cho cùng output trong 100 lần lặp.

Nó chưa chứng minh bộ thu đã tìm được timing từ waveform thực tế. Để đạt mục
tiêu cuối của đồ án, cần phát triển tiếp theo thứ tự: OFDM và CP, kênh AWGN/
đa đường/Doppler/CFO, bộ phát hiện A0-A2, sau đó mới đo Pd/Pfa/RMSE và chạy
sweep. Mỗi bước cần thêm test trước khi chuyển sang bước kế tiếp.

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
.venv/bin/pytest -q
```

Test chính của G2 là:

```bash
.venv/bin/pytest -q tests/test_module_structure.py
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
pytest -q
```

Nếu đã cài dependency trước khi cập nhật README, cài lại pytest tương thích:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

## Tài liệu tham chiếu

Các công thức PSS, SSS và PCI được triển khai theo 3GPP TS 38.211, mục
7.4.2 về tín hiệu đồng bộ SS/PBCH block.
