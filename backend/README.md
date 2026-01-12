# Backend API Documentation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file from `.env.example`

3. Run the application:
```bash
python app/main.py
```

## API Endpoints

### Sellers
- `GET /api/sellers` - Get all sellers
- `GET /api/sellers/<id>` - Get seller by ID
- `POST /api/sellers/scrape` - Scrape seller
- `PUT /api/sellers/<id>` - Update seller
- `DELETE /api/sellers/<id>` - Delete seller

### Brands
- `GET /api/brands` - Get all brands
- `GET /api/brands/<id>` - Get brand by ID
- `POST /api/brands/research` - Research brand

### QA Analysis
- `POST /api/qa/analyze` - Analyze brand
- `GET /api/qa/metrics/<brand_id>` - Get QA metrics

