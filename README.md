# 📈 Stock Tracker Application

A sleek, real-time stock tracker built with **Tkinter** and **Matplotlib**, fetching data from **Finnhub API**. This application displays live stock prices, percentage changes, market status, and price history graphs.

---

## 🚀 Features

- **Real-Time Stock Data** (Updates every 3 seconds)
- **Dynamic Graph** with color-coded trends (Green = Up, Red = Down)
- **Smooth Animations** for price and percentage changes
- **Market Status Indicator** (Open/Closed)
- **Dark Themed Modern UI**

---

## ⚙️ Requirements

- Python **3.7+**
- Works on **Raspberry Pi** and **Windows**

---

## 🖥️ Installation Instructions

### 1️⃣ Create a Virtual Environment

Using a virtual environment is recommended to avoid dependency conflicts. Learn more here: [Virtual Environments Primer](https://realpython.com/python-virtual-environments-a-primer/).

#### **On Raspberry Pi / Linux:**

```bash
sudo apt update
sudo apt install python3-venv python3-pip -y
python3 -m venv stock-env
source stock-env/bin/activate
```

#### **On Windows:**

```bash
python -m venv stock-env
stock-env\Scripts\activate
```

---

### 2️⃣ Install Dependencies

After activating your virtual environment:

#### **Common Dependencies (Raspberry Pi & Windows):**

```bash
pip install tkinter
pip install matplotlib
pip install finnhub-python
```

#### **Additional Steps for Raspberry Pi:**

For **Tkinter** (if you encounter issues):

```bash
sudo apt-get install python3-tk
```

For **Matplotlib:**

```bash
sudo apt install libatlas3-base
```

---

## 🗂️ How to Run the Application

1. Clone or download the project files.
2. Activate the virtual environment.
3. Run the Python script:
   ```bash
   python stock_tracker.py
   ```

The app will open in a window showing live updates for the stock **S&P 500 (VOO)**.

---

## 🔑 Setting Up Your Finnhub API Key

1. Sign up at [https://finnhub.io/](https://finnhub.io/) to get your free API key.
2. Replace the API key in the script:
   ```python
   self.finnhub_client = finnhub.Client("YOUR_API_KEY_HERE")
   ```

---

## 🛠️ Troubleshooting

- **Matplotlib Errors:**

  - Ensure `matplotlib` is properly installed.
  - For Raspberry Pi:
    ```bash
    sudo apt-get install libatlas-base-dev
    sudo apt install libatlas3-base
    ```

- **Slow Performance on Raspberry Pi:**

  - Reduce the update frequency (change `self.root.after(3000, self.update_data)` to a higher value).

- **Time Zone Issues:**

  - The app assumes **EST**. Adjust time logic if needed.

---

## 🔩 Parts Used

1. **[Mini Aluminum Heat Sink](https://www.adafruit.com/product/3084)**\
   Helps dissipate heat from the Raspberry Pi, improving thermal performance.

2. **[Ribbon Micro USB with 90-Degree Angle](https://www.amazon.com/dp/B077M5NW1M/ref=pd_aw_subss_hxwSS2_sspa_mw_detail_sbl_s_ds1_pn_n_3?_encoding=UTF8\&pd_rd_i=B077M5NW1M\&pd_rd_w=ua1Mw\&content-id=amzn1.sym.635c4b6f-81ac-43aa-915c-60449794a522\&pf_rd_p=635c4b6f-81ac-43aa-915c-60449794a522\&pf_rd_r=A0M7E6MHXFXWQN1BT5RF\&pd_rd_wg=pnaR4\&pd_rd_r=8dece910-3321-4131-9f1e-b344e71e4edf\&sp_csd=d2lkZ2V0TmFtZT1zcF9waG9uZV9kZXRhaWxfdGhlbWF0aWM=)**\
   A flexible USB cable with a right-angle connector for compact Raspberry Pi setups.

3. **[Raspberry Pi Case](https://www.adafruit.com/product/2258?gQT=2)**\
   A durable protective case to house and safeguard your Raspberry Pi.

4. **[3.5 Inch TFT LCD Touch Screen Monitor](https://www.microcenter.com/product/632693/35_Inch_TFT_LCD_Touch_Screen_Monitor)**\
   A compact, responsive touch display great for embedded systems and monitoring dashboards.

---

## 📜 License

This project is open-source and free to modify as needed. :)

