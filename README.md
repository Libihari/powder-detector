# Powder Detection System 🧪
*A Raspberry Pi-based project to classify powders (talcum, baking soda, cornstarch) using a  particle sensor.*

---

## **Features**
- Real-time PM1.0/PM2.5/PM10 monitoring.
- Machine learning classification (Random Forest).
- CSV data logging for training.

## **Hardware Requirements**
- Raspberry Pi 4 (4GB)
- PM5 sensor
- USB-UART adapter (e.g., CP2102)

## **Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/powder-detector.git
   ```
2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Run the data logger:
   ```bash
   python3 pm5003_data_logger.py
   ```

## **File Structure**
```
powder-detector/
├── pm_data_logger.py  # Collects sensor data
├── train_model.py         # Trains ML model
├── classify.py            # Real-time classification
├── requirements.txt       # Python dependencies
└── powder_data.csv        # Labeled dataset (example)
```

## **Usage**
- **Data Collection**:
  ```bash
  python3 pm_data_logger.py
  ```
- **Training** (after labeling data):
  ```bash
  python3 train_model.py
  ```
- **Classification**:
  ```bash
  python3 classify.py
  ```
  
---
*Created by [Libihari](https://github.com/libihari)*
